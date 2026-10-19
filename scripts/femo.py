"""FEMO AI Studio: helpers locais. Python 3.10+, FFmpeg e FFprobe."""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import textwrap
import uuid
from datetime import datetime, timezone

VIDEO = {'.mp4', '.mov', '.mkv', '.webm', '.m4v', '.avi'}
AUDIO = {'.wav', '.mp3', '.m4a', '.aac', '.flac', '.ogg'}
FOLDERS = ['01_brutos', '02_referencias', '03_marca', '04_audio', '05_projeto', '06_entregas', '07_design']

class ProjectError(ValueError):
    pass

def emit(value):
    print(json.dumps(value, ensure_ascii=False, indent=2))

def executable(name):
    value = os.environ.get(name.upper() + '_BIN') or shutil.which(name)
    if not value or not Path(value).is_file():
        raise ProjectError(f'{name} ausente. Instale pela fonte oficial ou informe {name.upper()}_BIN.')
    return value

def run(args, cwd=None, timeout=3600):
    result = subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True,
                            text=True, encoding='utf-8', errors='replace', timeout=timeout)
    if result.returncode:
        raise ProjectError(f'Comando falhou ({Path(str(args[0])).name}): {result.stderr[-2500:]}')
    return result.stdout

def probe(path):
    return json.loads(run([executable('ffprobe'), '-v', 'error', '-show_format',
                           '-show_streams', '-of', 'json', path], timeout=90))

def source_info(path):
    data = probe(path)
    video = next((s for s in data.get('streams', []) if s.get('codec_type') == 'video'), None)
    audio = next((s for s in data.get('streams', []) if s.get('codec_type') == 'audio'), None)
    raw_duration = (video or {}).get('duration') or data.get('format', {}).get('duration')
    try:
        duration = float(raw_duration)
    except (TypeError, ValueError):
        raise ProjectError(f'Duração não identificada: {path.name}')
    if not math.isfinite(duration) or duration <= 0:
        raise ProjectError(f'Duração inválida: {path.name}')
    rotation = 0
    for side in (video or {}).get('side_data_list', []):
        if 'rotation' in side:
            rotation = float(side['rotation'])
    return {'duration': duration, 'video': video, 'audio': audio, 'rotation': rotation}

def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')

def stamp():
    return datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:6]

def contained(root, relative, must_exist=True):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ProjectError('Use um caminho relativo dentro do projeto.')
    result = (root / relative).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ProjectError('Caminho fora da pasta do projeto.')
    if must_exist and not result.is_file():
        raise ProjectError(f'Arquivo não encontrado: {relative}')
    return result

def init_project(path):
    root = Path(path).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    for name in FOLDERS:
        (root / name).mkdir(exist_ok=True)
    brief = root / 'briefing.md'
    if not brief.exists():
        brief.write_text('# Briefing\n\nMarca:\nObjetivo:\nPúblico:\nMensagem central:\nFormato e duração:\nReferência principal:\nO que preservar:\nEntregas:\nUso de serviços externos autorizado:\n', encoding='utf-8')
    memory = root / '05_projeto/project.md'
    if not memory.exists():
        memory.write_text('# Memória do projeto\n\n## Decisões\n\n## Ferramentas e versões\n\n## Entregas e revisão\n', encoding='utf-8')
    return {'project': str(root), 'folders': FOLDERS, 'status': 'pastas prontas; nenhum corte decidido'}

def doctor():
    result = {'python': sys.version.split()[0], 'python_executable': sys.executable, 'tools': {}}
    for name in ['ffmpeg', 'ffprobe', 'node', 'claude', 'codex']:
        value = os.environ.get(name.upper() + '_BIN') or shutil.which(name)
        entry = {'available': bool(value), 'path': value}
        if value and name in ['ffmpeg', 'ffprobe', 'node']:
            try:
                entry['version'] = run([value, '--version' if name == 'node' else '-version'], timeout=15).splitlines()[0]
            except (ProjectError, subprocess.TimeoutExpired) as exc:
                entry['error'] = str(exc)
        result['tools'][name] = entry
    result['local_edit_ready'] = all(result['tools'][x]['available'] and 'error' not in result['tools'][x] for x in ['ffmpeg', 'ffprobe'])
    result['note'] = 'Nenhum programa, modelo, conta ou conector foi instalado por este comando.'
    return result

def inventory(root, with_hash=False):
    root = Path(root).resolve()
    raw = root / '01_brutos'
    if not raw.is_dir():
        raise ProjectError('Pasta 01_brutos não encontrada. Execute init ou confira o projeto.')
    items = []
    for path in sorted(raw.rglob('*')):
        if not path.is_file() or path.suffix.lower() not in VIDEO | AUDIO:
            continue
        if not path.resolve().is_relative_to(raw.resolve()):
            raise ProjectError('Um link em 01_brutos aponta para fora do projeto.')
        stat = path.stat()
        info = source_info(path)
        v = info['video'] or {}
        a = info['audio'] or {}
        item = {'source': path.relative_to(root).as_posix(), 'bytes': stat.st_size,
                'mtime_ns': stat.st_mtime_ns, 'duration': info['duration'],
                'width': v.get('width'), 'height': v.get('height'), 'fps': v.get('avg_frame_rate'),
                'rotation': info['rotation'], 'color_transfer': v.get('color_transfer'),
                'color_space': v.get('color_space'), 'has_audio': bool(a), 'sample_rate': a.get('sample_rate')}
        if with_hash:
            digest = hashlib.sha256()
            with path.open('rb') as stream:
                for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                    digest.update(chunk)
            item['sha256'] = digest.hexdigest()
        items.append(item)
    output = root / '05_projeto' / f'inventario-{stamp()}.json'
    write_json(output, {'sources': items})
    return {'manifest': str(output), 'sources': items}

def number(value, name):
    if isinstance(value, bool) or not isinstance(value, (float, int)) or not math.isfinite(value):
        raise ProjectError(f'{name} precisa ser um número finito.')
    return float(value)

def load_edl(path):
    path = Path(path).resolve()
    data = json.loads(path.read_text(encoding='utf-8-sig'))
    if data.get('schema_version') != 1:
        raise ProjectError('schema_version deve ser 1.')
    root_value = data.get('project_root')
    if not isinstance(root_value, str) or not root_value:
        raise ProjectError('project_root é obrigatório.')
    root = (path.parent / root_value).resolve()
    if not (root / '01_brutos').is_dir() or not (root / '05_projeto').is_dir():
        raise ProjectError('project_root não é um projeto FEMO inicializado.')
    output = data.get('output', {})
    for key in ['width', 'height']:
        value = output.get(key)
        if isinstance(value, bool) or not isinstance(value, int) or value < 16 or value > 7680 or value % 2:
            raise ProjectError(f'{key} deve ser inteiro par entre 16 e 7680.')
    fps = number(output.get('fps', 30), 'fps')
    if not 1 <= fps <= 60:
        raise ProjectError('fps precisa estar entre 1 e 60.')
    if output.get('fit', 'contain') not in ['contain', 'cover']:
        raise ProjectError('fit deve ser contain ou cover.')
    if not re.fullmatch('[0-9A-Fa-f]{6}', output.get('background', '071E18')):
        raise ProjectError('background deve conter seis dígitos hexadecimais, sem #.')
    raw_segments = data.get('segments')
    if not isinstance(raw_segments, list) or not raw_segments:
        raise ProjectError('Inclua ao menos um segmento.')
    segments, cache = [], {}
    offset = 0.0
    raw_root = (root / '01_brutos').resolve()
    for index, segment in enumerate(raw_segments):
        if not isinstance(segment, dict):
            raise ProjectError('Segmento inválido.')
        src = contained(root, segment.get('source'))
        if not src.is_relative_to(raw_root):
            raise ProjectError('Origens de segmentos devem ficar em 01_brutos.')
        start = number(segment.get('start'), 'start')
        end = number(segment.get('end'), 'end')
        if start < 0 or end - start < 1 / fps - 1e-8:
            raise ProjectError('Intervalo inválido ou menor que um quadro.')
        if src not in cache:
            cache[src] = source_info(src)
        info = cache[src]
        if not info['video']:
            raise ProjectError('A montagem básica requer vídeo em cada segmento.')
        if end > info['duration'] + 0.001:
            raise ProjectError(f'Segmento {index + 1} termina fora da origem.')
        if info['video'].get('color_transfer') in ['smpte2084', 'arib-std-b67']:
            raise ProjectError('Origem HDR detectada. Use um pipeline de tone mapping revisado antes desta montagem.')
        segments.append({'path': src, 'source': src.relative_to(root).as_posix(),
                         'start': start, 'end': end, 'source_duration': end - start,
                         'duration': math.ceil((end - start) * fps - 1e-8) / fps,
                         'offset': offset, 'has_audio': bool(info['audio'])})
        offset += segments[-1]['duration']
    caption = None
    if data.get('caption_srt'):
        caption = contained(root, data['caption_srt'])
        if caption.suffix.lower() != '.srt' or '-->' not in caption.read_text(encoding='utf-8-sig'):
            raise ProjectError('caption_srt não é um SRT reconhecível.')
    font = data.get('caption_font', 'Inter')
    if not isinstance(font, str) or not re.fullmatch(r'[A-Za-z0-9 _-]{1,80}', font):
        raise ProjectError('Nome de fonte inválido.')
    return data, root, segments, caption, offset

def validate(path):
    data, root, segments, caption, duration = load_edl(path)
    return {'valid': True, 'segments': len(segments), 'expected_seconds': duration,
            'output': data['output'], 'caption_srt': str(caption) if caption else None,
            'note': 'Validação de arquivos e intervalos; não verifica sentido da fala ou qualidade visual.'}

def srt_time(value):
    millis = max(0, round(value * 1000))
    seconds, ms = divmod(millis, 1000)
    minutes, sec = divmod(seconds, 60)
    hours, minute = divmod(minutes, 60)
    return f'{hours:02}:{minute:02}:{sec:02},{ms:03}'

def remap_words(segments, words):
    result = []
    for segment in segments:
        for word in words:
            if word.get('source') != segment['source']:
                continue
            start = number(word.get('start'), 'word.start')
            end = number(word.get('end'), 'word.end')
            if end <= start:
                raise ProjectError('Palavra com duração inválida.')
            if end <= segment['start'] or start >= segment['end']:
                continue
            if start < segment['start'] - 0.001 or end > segment['end'] + 0.001:
                raise ProjectError('Um corte atravessa uma palavra. Revise corte ou alinhamento antes de legendar.')
            text = ' '.join(str(word.get('text', '')).split()).replace('-->', '')
            if not text:
                continue
            result.append({'start': max(segment['offset'], start - segment['start'] + segment['offset']),
                           'end': end - segment['start'] + segment['offset'], 'text': text})
    result.sort(key=lambda x: x['start'])
    return result

def words_to_srt(words):
    groups, group = [], []
    for word in words:
        if group and (word['start'] - group[-1]['end'] > 0.6 or
                      len(' '.join(x['text'] for x in group)) + len(word['text']) > 58 or
                      word['end'] - group[0]['start'] > 3.0):
            groups.append(group); group = []
        group.append(word)
        if len(group) >= 5 or word['text'].endswith(('.', '!', '?')):
            groups.append(group); group = []
    if group:
        groups.append(group)
    lines = []
    for index, group in enumerate(groups, 1):
        text = '\n'.join(textwrap.wrap(' '.join(w['text'] for w in group), width=36, break_long_words=False))
        lines.append(f'{index}\n{srt_time(group[0]["start"])} --> {srt_time(group[-1]["end"])}\n{text}\n')
    return '\n'.join(lines)

def captions(edl, transcript):
    data, root, segments, _, _ = load_edl(edl)
    raw = json.loads(Path(transcript).read_text(encoding='utf-8-sig'))
    words = raw.get('words')
    if not isinstance(words, list):
        raise ProjectError('JSON de transcrição precisa conter words como lista.')
    mapped = remap_words(segments, words)
    if not mapped:
        raise ProjectError('Nenhuma palavra temporizada coincide com os segmentos.')
    out = root / '05_projeto' / f'legendas-{stamp()}.srt'
    out.write_text(words_to_srt(mapped), encoding='utf-8')
    return {'srt': str(out), 'caption_srt_for_edl': out.relative_to(root).as_posix(), 'words': len(mapped)}

def render(edl, preview=False):
    data, root, segments, caption, expected = load_edl(edl)
    ffmpeg = executable('ffmpeg')
    options = data['output']
    width, height = options['width'], options['height']
    if preview and width > 540:
        height = max(16, round(height * 540 / width / 2) * 2)
        width = 540
    fps = options.get('fps', 30)
    bg = options.get('background', '071E18')
    run_id = stamp()
    work = root / '05_projeto' / ('render-' + run_id)
    work.mkdir(parents=True)
    target = root / '06_entregas' / (('previa-' if preview else 'final-') + run_id + '.mp4')
    target.parent.mkdir(exist_ok=True)
    fit = options.get('fit', 'contain')
    if fit == 'contain':
        geometry = f'scale={width}:{height}:force_original_aspect_ratio=decrease:force_divisible_by=2,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2:color=0x{bg}'
    else:
        geometry = f'scale={width}:{height}:force_original_aspect_ratio=increase:force_divisible_by=2,crop={width}:{height}'
    manifest = []
    for index, segment in enumerate(segments):
        duration = segment['duration']
        fade = min(0.03, duration / 4)
        cmd = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n',
               '-ss', segment['start'], '-t', segment['source_duration'], '-i', segment['path']]
        if not segment['has_audio']:
            cmd += ['-f', 'lavfi', '-i', 'anullsrc=r=48000:cl=stereo']
        audio_index = '0:a:0' if segment['has_audio'] else '1:a:0'
        af = f'aresample=48000,aformat=sample_fmts=s16:channel_layouts=stereo,apad,atrim=duration={duration},asetpts=PTS-STARTPTS,afade=t=in:st=0:d={fade},afade=t=out:st={duration-fade}:d={fade}'
        name = f'segment-{index:04}.mkv'
        cmd += ['-map', '0:v:0', '-map', audio_index, '-vf',
                f'setpts=PTS-STARTPTS,{geometry},setsar=1,tpad=stop_mode=clone:stop_duration={1/float(fps)},fps={fps},format=yuv420p',
                '-af', af, '-t', duration, '-c:v', 'ffv1', '-level', '3',
                '-c:a', 'pcm_s16le', '-ar', '48000', '-ac', '2', '-map_metadata', '-1', work / name]
        run(cmd)
        manifest.append(f"file '{name}'")
    (work / 'segments.txt').write_text('\n'.join(manifest), encoding='utf-8')
    cmd = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n', '-f', 'concat',
           '-safe', '1', '-i', 'segments.txt', '-map', '0:v:0', '-map', '0:a:0']
    if caption:
        shutil.copy2(caption, work / 'legendas.srt')
        (work / 'fonts').mkdir(exist_ok=True)
        font_dir = root / '03_marca' / 'fontes'
        if font_dir.is_dir():
            (work / 'fonts').mkdir(exist_ok=True)
            for src in font_dir.iterdir():
                if src.is_file() and src.suffix.lower() in {'.ttf', '.otf'}:
                    shutil.copy2(src, work / 'fonts' / src.name)
        font = data.get('caption_font', 'Inter')
        cmd += ['-vf', f"subtitles=filename=legendas.srt:fontsdir=fonts:force_style='FontName={font},FontSize=18,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,Outline=1.5,Shadow=0,Alignment=2,MarginV=45'"]
    cmd += ['-c:v', 'libx264', '-preset', 'fast' if preview else 'medium', '-crf', '23' if preview else '18',
            '-pix_fmt', 'yuv420p', '-r', fps, '-c:a', 'aac', '-b:a', '192k',
            '-ar', '48000', '-ac', '2', '-map_metadata', '-1', '-movflags', '+faststart', target]
    run(cmd, cwd=work)
    output = source_info(target)
    actual = output['duration']
    tolerance = max(0.12, len(segments) / float(fps) + 0.05)
    passed = (abs(actual - expected) <= tolerance and bool(output['audio']) and
              output['video'].get('width') == width and output['video'].get('height') == height)
    report = {'output': str(target), 'expected_seconds': expected, 'actual_seconds': actual,
              'tolerance_seconds': tolerance, 'width': width, 'height': height,
              'has_audio': bool(output['audio']), 'technical_checks_passed': passed,
              'creative_review_pending': True, 'caption_font_visual_check_pending': bool(caption),
              'scope': 'Montagem básica local; sem ASR, trilha, overlays ou correção de cor avançada.'}
    write_json(target.with_suffix('.json'), report)
    if not passed:
        raise ProjectError(f'Revisão técnica falhou. Saída e relatório preservados em {target.parent}')
    return report

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('doctor')
    p = sub.add_parser('init'); p.add_argument('project')
    p = sub.add_parser('inventory'); p.add_argument('project'); p.add_argument('--hash', action='store_true')
    p = sub.add_parser('validate'); p.add_argument('edl')
    p = sub.add_parser('captions'); p.add_argument('edl'); p.add_argument('transcript')
    p = sub.add_parser('render'); p.add_argument('edl'); p.add_argument('--preview', action='store_true')
    args = parser.parse_args()
    try:
        if args.command == 'doctor': result = doctor()
        elif args.command == 'init': result = init_project(args.project)
        elif args.command == 'inventory': result = inventory(args.project, args.hash)
        elif args.command == 'validate': result = validate(args.edl)
        elif args.command == 'captions': result = captions(args.edl, args.transcript)
        else: result = render(args.edl, args.preview)
        emit(result)
    except (ProjectError, OSError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
        emit({'error': str(exc)}); return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
