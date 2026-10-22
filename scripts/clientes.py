"""Base privada de clientes FEMO: criar, registrar fontes, atualizar e relatar lacunas.

Python 3.10+, apenas biblioteca padrão. Não coleta dados nem conecta contas.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from copy import deepcopy
from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import uuid

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / 'templates/cliente/campos.json'
STATES = {'ausente', 'hipotese', 'confirmado', 'conflito', 'nao_aplicavel'}
STAGES = ('pesquisa', 'planejamento', 'design')
FOLDERS = ('entradas', 'pesquisa', 'identidade', 'referencias', 'conteudo',
           'producao', 'entregas', 'decisoes', 'historico')


def today():
    return datetime.now(timezone.utc).date().isoformat()


def read_json(file):
    with Path(file).open(encoding='utf-8-sig') as stream:
        return json.load(stream)


def atomic_json(file, value):
    file = Path(file)
    descriptor, tmp = tempfile.mkstemp(prefix='.femo-', suffix='.json', dir=file.parent)
    try:
        with os.fdopen(descriptor, 'w', encoding='utf-8') as stream:
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False)
            stream.write('\n')
        os.replace(tmp, file)
    finally:
        if Path(tmp).exists():
            Path(tmp).unlink()


def parse_date(value):
    if not isinstance(value, str):
        raise ValueError('Data deve ser texto ISO (AAAA-MM-DD).')
    if len(value) == 10:
        return date.fromisoformat(value)
    return datetime.fromisoformat(value.replace('Z', '+00:00')).date()


def has_value(value):
    if isinstance(value, str):
        return bool(value.strip())
    return value is not None and value != [] and value != {}


def validate_evidence(item):
    if not isinstance(item, dict):
        raise ValueError('Evidência deve ser objeto.')
    for key in ('id', 'kind', 'locator', 'collected_at', 'access', 'observation'):
        if not isinstance(item.get(key), str) or not item[key].strip():
            raise ValueError(f'Evidência sem {key}.')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}', item['id']):
        raise ValueError('ID de evidência inválido.')
    parse_date(item['collected_at'])
    if item['access'] not in {'full', 'partial', 'blocked'}:
        raise ValueError('Acesso deve ser full, partial ou blocked.')
    if item['locator'].lstrip().lower().startswith(('javascript:', 'data:')):
        raise ValueError('Localizador de evidência inválido.')


def validate(data, model):
    if data.get('schema_version') != 1 or model.get('schema_version') != 1:
        raise ValueError('Versão de esquema não suportada.')
    if not isinstance(data.get('client'), dict) or not data['client'].get('name'):
        raise ValueError('Cliente sem identificação.')
    specs = model.get('fields')
    if not isinstance(specs, list) or not specs:
        raise ValueError('Critérios vazios.')
    ids = [item['id'] for item in specs]
    if len(ids) != len(set(ids)):
        raise ValueError('Critério duplicado.')
    if not isinstance(data.get('fields'), dict) or set(data['fields']) != set(ids):
        raise ValueError('Campos incompatíveis com criterios.json.')
    for spec in specs:
        if (not isinstance(spec.get('max_age_days'), int) or spec['max_age_days'] < 1
                or not set(spec.get('required_for', [])).issubset(STAGES)):
            raise ValueError('Prazo ou etapa inválidos nos critérios.')
    evidence = data.get('evidence')
    if not isinstance(evidence, list):
        raise ValueError('evidence deve ser lista.')
    for item in evidence:
        validate_evidence(item)
    if len({item['id'] for item in evidence}) != len(evidence):
        raise ValueError('ID de evidência duplicado.')
    for key, field in data['fields'].items():
        if not isinstance(field, dict) or field.get('status') not in STATES:
            raise ValueError(f'Estado inválido em {key}.')
        if (not isinstance(field.get('evidence_ids'), list)
                or not all(isinstance(x, str) for x in field['evidence_ids'])):
            raise ValueError(f'Fontes inválidas em {key}.')
        if field.get('reviewed_at') is not None:
            parse_date(field['reviewed_at'])
    if not isinstance(data.get('history'), list) or not isinstance(data.get('conflicts'), list):
        raise ValueError('Histórico/conflitos devem ser listas.')
    for conflict in data['conflicts']:
        if (not isinstance(conflict, dict) or conflict.get('status') not in {'aberto', 'resolvido'}
                or not isinstance(conflict.get('fields'), list)
                or not conflict['fields'] or not set(conflict['fields']).issubset(ids)):
            raise ValueError('Conflito inválido; informe status e fields conhecidos.')


def load(folder):
    folder = Path(folder).resolve()
    data, model = read_json(folder/'dossie.json'), read_json(folder/'criterios.json')
    validate(data, model)
    return folder, data, model


def create_client(slug, name, instagram=None, base=None):
    reserved = {'con', 'prn', 'aux', 'nul', *(f'com{i}' for i in range(1, 10)),
                *(f'lpt{i}' for i in range(1, 10))}
    if (not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', slug) or len(slug) > 64
            or slug in reserved):
        raise ValueError('Use identificador curto com letras minúsculas, números e hífens.')
    if not name.strip():
        raise ValueError('Nome vazio.')
    base = Path(base or Path.cwd()/'projetos/clientes').expanduser().resolve()
    folder = base/slug
    model = read_json(TEMPLATE)
    fields = {item['id']: {'value': None, 'status': 'ausente', 'evidence_ids': [],
                          'reviewed_at': None, 'note': ''} for item in model['fields']}
    data = {'schema_version': 1, 'client': {'id': slug, 'name': name, 'instagram': instagram},
            'updated_at': today(), 'fields': fields, 'evidence': [], 'research_runs': [],
            'conflicts': [], 'history': []}
    validate(data, model)
    folder.mkdir(parents=True, exist_ok=False)
    for name_ in FOLDERS:
        (folder/name_).mkdir()
    (folder/'.gitignore').write_text('# Base de cliente: manter fora do Git público.\n*\n', encoding='utf-8')
    instructions = ('# Base do cliente\n\nLeia dossie.json, DOSSIÊ.md, LACUNAS.md e as decisões recentes antes de produzir. '
                    'O cliente e a missão atual definem o escopo. Use o SKILL.md do FEMO AI Studio disponível no projeto. '
                    'Pesquisa, fontes, hipóteses e aprovações têm estados distintos. Não invente preenchimento. '
                    'Registre feedback e preserve materiais originais e versões aprovadas. '
                    'Esta pasta é privada; não a publique no repositório de distribuição.\n')
    for name_ in ('AGENTS.md', 'CLAUDE.md'):
        (folder/name_).write_text(instructions, encoding='utf-8')
    atomic_json(folder/'criterios.json', model)
    atomic_json(folder/'dossie.json', data)
    report(folder)
    return folder


def evaluate(data, model, stage='design', as_of=None):
    if stage not in STAGES:
        raise ValueError('Etapa desconhecida.')
    as_of = parse_date(as_of or today())
    evidence = {item['id']: item for item in data['evidence']}
    pending = []
    for spec in model['fields']:
        key = spec['id']
        field = data['fields'][key]
        reasons = []
        if field['status'] == 'nao_aplicavel':
            if not spec.get('allow_na') or not field.get('note', '').strip():
                reasons.append('não aplicável sem permissão ou justificativa')
        else:
            if field['status'] != 'confirmado':
                reasons.append('estado: '+field['status'])
            if not has_value(field.get('value')):
                reasons.append('sem conteúdo')
            refs = field['evidence_ids']
            if not refs:
                reasons.append('sem evidência vinculada')
            elif any(ref not in evidence for ref in refs):
                reasons.append('fonte citada não registrada')
            elif not any(evidence[ref]['access'] != 'blocked' for ref in refs):
                reasons.append('fontes somente bloqueadas')
            if not field.get('reviewed_at'):
                reasons.append('sem data de revisão')
            else:
                days = (as_of-parse_date(field['reviewed_at'])).days
                if days < 0:
                    reasons.append('revisão no futuro')
                elif days > spec['max_age_days']:
                    reasons.append('prazo de revisão vencido')
            if any(ref in evidence and parse_date(evidence[ref]['collected_at']) > as_of for ref in refs):
                reasons.append('coleta no futuro')
        if any(item['status'] == 'aberto' and key in item['fields'] for item in data['conflicts']):
            reasons.append('contradição aberta')
        if reasons:
            pending.append({'field': key, 'label': spec['label'], 'blocking': stage in spec['required_for'],
                            'reasons': reasons, 'question': spec['question'], 'owner': spec['owner'],
                            'attempts': field.get('note') or 'Tentativas ainda não registradas.',
                            'sources': field['evidence_ids']})
    return {'stage': stage, 'as_of': as_of.isoformat(),
            'ready': not any(item['blocking'] for item in pending), 'gaps': pending}


@contextmanager
def client_lock(folder):
    lock = folder/'.femo.lock'
    try:
        descriptor = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError as exc:
        raise ValueError('Outra atualização está em andamento. Confira o processo antes de remover .femo.lock.') from exc
    try:
        os.close(descriptor)
        yield
    finally:
        lock.unlink()


def mutate(folder, action):
    folder = Path(folder).resolve()
    with client_lock(folder):
        folder, old, model = load(folder)
        new = deepcopy(old)
        event = action(new)
        if event is None:
            return False
        new['updated_at'] = today()
        new['history'].append({'at': datetime.now(timezone.utc).isoformat(), **event})
        validate(new, model)
        snapshot = folder/'historico'/f'{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:8]}.json'
        atomic_json(snapshot, old)
        atomic_json(folder/'dossie.json', new)
        report(folder)
    return True


def add_evidence(folder, items):
    if isinstance(items, dict):
        items = [items]
    if not isinstance(items, list) or not items:
        raise ValueError('Informe objeto de evidência ou lista não vazia.')
    for item in items:
        validate_evidence(item)
    def apply(data):
        known = {item['id']: item for item in data['evidence']}
        added = []
        for item in items:
            previous = known.get(item['id'])
            if previous is not None:
                if previous != item:
                    raise ValueError(f'ID {item["id"]} já contém outra evidência; use ID novo.')
                continue
            known[item['id']] = item
            data['evidence'].append(deepcopy(item))
            added.append(item['id'])
        return {'action': 'evidence_added', 'ids': added} if added else None
    return mutate(folder, apply)


def set_field(folder, key, value, status='hipotese', sources=None, note=''):
    if status not in STATES:
        raise ValueError('Estado desconhecido.')
    def apply(data):
        if key not in data['fields']:
            raise ValueError('Campo desconhecido: '+key)
        previous = deepcopy(data['fields'][key])
        current = {'value': value, 'status': status, 'evidence_ids': sources or [],
                   'reviewed_at': today(), 'note': note}
        if current == previous:
            return None
        data['fields'][key] = current
        return {'action': 'field_updated', 'field': key, 'before': previous, 'after': current}
    return mutate(folder, apply)


def render_value(value):
    if value is None:
        return 'Ainda não preenchido.'
    if isinstance(value, str):
        return value
    return '\n~~~json\n'+json.dumps(value, ensure_ascii=False, indent=2)+'\n~~~\n'


def report(folder, as_of=None):
    folder, data, model = load(folder)
    lines = [f'# Dossiê · {data["client"]["name"]}', '',
             f'Atualizado: {data["updated_at"]}. Fonte estruturada: dossie.json.', '',
             'Estado estrutural não equivale a pesquisa validada ou aprovação humana.', '']
    for spec in model['fields']:
        field = data['fields'][spec['id']]
        lines += ['## '+spec['label'], '', '**Estado:** '+field['status'], '',
                  render_value(field['value']), '',
                  'Fontes: '+(', '.join(field['evidence_ids']) or 'nenhuma')+'.', '',
                  'Revisão: '+str(field.get('reviewed_at') or 'pendente')+'.', '',
                  'Nota/tentativas: '+(field.get('note') or 'não registradas')+'.', '']
    lines += ['## Evidências', '']
    for item in data['evidence']:
        lines += [f'- **{item["id"]}** · {item["kind"]} · {item["collected_at"]} · acesso {item["access"]}',
                  '  Origem: '+item['locator'], '  Observado: '+item['observation'], '']
    lines += ['## Conflitos', '', render_value(data['conflicts']), '',
              '## Rodadas de pesquisa', '', render_value(data.get('research_runs', [])), '']
    (folder/'DOSSIÊ.md').write_text('\n'.join(lines), encoding='utf-8')
    gap_lines = ['# Lacunas para a equipe', '',
                 'Verificação estrutural. Conferir também fontes, amostragem e qualidade das conclusões.', '']
    reports = {}
    for stage in STAGES:
        result = evaluate(data, model, stage, as_of)
        reports[stage] = result
        gap_lines += [f'## {stage} · '+('campos necessários preenchidos' if result['ready'] else 'pendências impeditivas'), '']
        for gap in result['gaps']:
            impact = 'Impede concluir esta etapa' if gap['blocking'] else 'Lacuna complementar; limita as conclusões relacionadas'
            gap_lines += ['### '+gap['label'], '', impact+'.', '',
                          'Motivo: '+'; '.join(gap['reasons'])+'.', '',
                          'Já consultado/tentado: '+gap['attempts'], '',
                          'Fontes vinculadas: '+(', '.join(gap['sources']) or 'nenhuma')+'.', '',
                          'Pedir à equipe: '+gap['question'], '',
                          'Responsável sugerido: '+gap['owner']+'.', '']
    (folder/'LACUNAS.md').write_text('\n'.join(gap_lines), encoding='utf-8')
    return reports


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    new = commands.add_parser('novo');new.add_argument('slug');new.add_argument('--nome', required=True)
    new.add_argument('--instagram');new.add_argument('--base')
    ev = commands.add_parser('evidencia');ev.add_argument('pasta');ev.add_argument('--arquivo', required=True)
    field = commands.add_parser('campo');field.add_argument('pasta');field.add_argument('campo')
    val = field.add_mutually_exclusive_group(required=True)
    val.add_argument('--valor');val.add_argument('--arquivo')
    field.add_argument('--estado', choices=sorted(STATES), default='hipotese')
    field.add_argument('--fontes', nargs='*', default=[]);field.add_argument('--nota', default='')
    check = commands.add_parser('verificar');check.add_argument('pasta')
    check.add_argument('--etapa', choices=STAGES, default='design')
    check.add_argument('--data', help='Data ISO de referência para verificar revisão')
    rep = commands.add_parser('relatorio');rep.add_argument('pasta')
    args = parser.parse_args(argv)
    try:
        if args.command == 'novo':
            print(create_client(args.slug, args.nome, args.instagram, args.base))
        elif args.command == 'evidencia':
            print('Atualizado.' if add_evidence(args.pasta, read_json(args.arquivo)) else 'Já registrado; preservado.')
        elif args.command == 'campo':
            value = read_json(args.arquivo) if args.arquivo else args.valor
            changed = set_field(args.pasta, args.campo, value, args.estado, args.fontes, args.nota)
            print('Atualizado.' if changed else 'Sem mudança.')
        elif args.command == 'verificar':
            _, data, model = load(args.pasta)
            result = evaluate(data, model, args.etapa, args.data)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result['ready'] else 2
        else:
            report(args.pasta)
            print('DOSSIÊ.md e LACUNAS.md atualizados.')
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('Erro: '+str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
