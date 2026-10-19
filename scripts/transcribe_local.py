"""ASR local opcional: requer faster-whisper e modelo disponível/explicitamente autorizado."""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
from pathlib import Path
from femo import contained, write_json, words_to_srt

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('project');p.add_argument('source',help='Caminho relativo em 01_brutos')
    p.add_argument('--model',required=True,help='Pasta local ou identificador faster-whisper')
    p.add_argument('--allow-model-download',action='store_true')
    p.add_argument('--language',default='pt');p.add_argument('--device',choices=['cpu','cuda'],default='cpu')
    a=p.parse_args()
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        p.exit(2,'ASR opcional ausente. Em ambiente isolado, instale faster-whisper e autorize o modelo.\n')
    root=Path(a.project).resolve();src=contained(root,a.source)
    if not src.is_relative_to((root/'01_brutos').resolve()):p.exit(2,'Origem precisa estar em 01_brutos.\n')
    digest=hashlib.sha256()
    with src.open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):digest.update(chunk)
    version=importlib.metadata.version('faster-whisper')
    key=hashlib.sha256((digest.hexdigest()+a.model+a.language+a.device+version).encode()).hexdigest()[:20]
    out=root/'05_projeto/transcricoes'/f'{src.stem}-{key}.json'
    if out.exists():
        print(json.dumps({'cached':True,'json':str(out)},ensure_ascii=False));return
    model=WhisperModel(a.model,device=a.device,compute_type='int8' if a.device=='cpu' else 'float16',local_files_only=not a.allow_model_download)
    segments,info=model.transcribe(str(src),language=a.language,word_timestamps=True,vad_filter=True)
    words=[]
    for segment in segments:
        for w in segment.words or []:
            words.append({'source':src.relative_to(root).as_posix(),'start':w.start,'end':w.end,'text':w.word.strip()})
    if not words:p.exit(2,'Nenhuma palavra reconhecida. Revise idioma, áudio e modelo.\n')
    write_json(out,{'source_sha256':digest.hexdigest(),'model':a.model,'asr_version':version,'language':info.language,'words':words,'review_pending':True})
    out.with_suffix('.srt').write_text(words_to_srt(words),encoding='utf-8')
    print(json.dumps({'json':str(out),'words':len(words),'review_pending':True},ensure_ascii=False))
if __name__=='__main__':main()
