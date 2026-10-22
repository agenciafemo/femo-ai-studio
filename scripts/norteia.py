"""Preparar bases privadas a partir de exportação mínima do Norteia.

Somente arquivos locais: este helper não acessa nem altera o app/banco de dados.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import date
import hashlib
import json
from pathlib import Path
import re
import unicodedata
import uuid
import sys

import clientes

PROFILE_KEYS = {
    'brand_summary', 'segment', 'specialties', 'positioning', 'differentiators',
    'location_scope', 'products_services', 'personas', 'audience_pains',
    'audience_desires', 'audience_objections', 'audience_language', 'sensitive_topics',
    'voice_personality', 'formality', 'preferred_words', 'forbidden_words',
    'emoji_limit', 'preferred_ctas', 'forbidden_ctas', 'mandatory_disclosures', 'updated_at',
}
CLIENT_KEYS = {'id', 'organization_id', 'name', 'segment', 'traffic_only', 'ended_at', 'updated_at'}
MAP = {
    'oferta': ('products_services', 'specialties'),
    'publico': ('personas', 'audience_pains', 'audience_desires', 'audience_objections', 'audience_language'),
    'posicionamento': ('brand_summary', 'positioning', 'differentiators'),
    'voz': ('voice_personality', 'formality', 'preferred_words', 'forbidden_words', 'emoji_limit'),
    'limites': ('sensitive_topics', 'forbidden_ctas', 'mandatory_disclosures'),
    'conversao': ('preferred_ctas',),
}


def digest(value):
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()[:16]


def clean_record(record):
    result = {key: record.get(key) for key in CLIENT_KEYS}
    result['id'] = str(uuid.UUID(result['id']))
    if not isinstance(result.get('name'), str) or not result['name'].strip():
        raise ValueError('Cadastro sem nome.')
    result['name'] = result['name'].strip()
    if result['traffic_only'] is not None and not isinstance(result['traffic_only'], bool):
        raise ValueError('traffic_only deve ser booleano ou null.')
    for key in ('ended_at', 'updated_at'):
        if result[key]:
            clientes.parse_date(result[key])
    profile = record.get('content_profile')
    if profile is not None and not isinstance(profile, dict):
        raise ValueError('content_profile inválido.')
    result['content_profile'] = {key: value for key, value in (profile or {}).items()
                                 if key in PROFILE_KEYS and clientes.has_value(value)}
    return result


def prepare_export(export, organization_id):
    if export.get('schema_version') != 1 or export.get('source') != 'norteia':
        raise ValueError('Exportação mínima Norteia versão 1 esperada.')
    if not organization_id or export.get('organization_id') != organization_id:
        raise ValueError('Organização da exportação não corresponde ao escopo solicitado.')
    collected = clientes.parse_date(export['collected_at']).isoformat()
    if collected > clientes.today():
        raise ValueError('Coleta no futuro.')
    if not isinstance(export.get('clients'), list):
        raise ValueError('clients deve ser lista.')
    records = []
    seen = set()
    for item in export['clients']:
        record = clean_record(item)
        if record['organization_id'] != organization_id:
            raise ValueError('Cadastro de outra organização encontrado; nada será preparado.')
        if record['id'] in seen:
            raise ValueError('Cliente duplicado na exportação.')
        seen.add(record['id'])
        records.append(record)
    return collected, records


def client_slug(record):
    text = unicodedata.normalize('NFKD', record['name']).encode('ascii', 'ignore').decode().lower()
    stem = re.sub(r'[^a-z0-9]+', '-', text).strip('-')[:28].rstrip('-') or 'cliente'
    return stem+'-'+record['id'].replace('-', '')[:12]


def candidates(record):
    profile = record['content_profile']
    result = {'perfil': {'name': record['name'], 'segment': record.get('segment') or profile.get('segment'),
                         'location_scope': profile.get('location_scope')}}
    for field, keys in MAP.items():
        value = {key: profile[key] for key in keys if key in profile}
        # Formalidade e limite de emoji podem ser defaults da interface, não uma voz estudada.
        if field == 'voz' and not any(key in profile for key in ('voice_personality', 'preferred_words', 'forbidden_words')):
            continue
        if value:
            result[field] = value
    return result


def import_record(folder, record, collected):
    identifier = 'NOR-'+record['id'].replace('-', '')[:8]+'-'+digest({'record': record, 'collected': collected})
    source_file = 'entradas/'+identifier+'.json'
    evidence = {'id': identifier, 'kind': 'internal_record', 'locator': source_file,
                'collected_at': collected, 'access': 'full',
                'observation': 'Cadastro e campos do perfil consultados no Norteia. Identificação é cadastral; conteúdo é base recebida, ainda sujeita a revisão. Não houve pesquisa de Instagram nesta importação.'}
    def apply(data):
        if any(item['id'] == identifier for item in data['evidence']):
            return None
        before = {}
        proposals = []
        for key, value in candidates(record).items():
            field = data['fields'][key]
            if field.get('value') == value:
                continue
            if field['status'] != 'ausente' or clientes.has_value(field.get('value')):
                proposals.append({'field': key, 'candidate': value, 'source_id': identifier})
                if not any(c.get('status') == 'aberto' and key in c['fields'] and c.get('source_id') == identifier
                           for c in data['conflicts']):
                    data['conflicts'].append({'id': identifier+'-'+key, 'fields': [key], 'status': 'aberto',
                                              'source_id': identifier,
                                              'note': 'Novo cadastro difere do valor local. Revisar proposta sem substituir a decisão vigente.'})
                continue
            before[key] = deepcopy(field)
            data['fields'][key] = {'value': value, 'status': 'confirmado' if key == 'perfil' else 'hipotese',
                                  'evidence_ids': [identifier], 'reviewed_at': collected,
                                  'note': 'Recebido do Norteia. Confirmar prioridade, atualidade e aplicação antes de produzir.'}
        data['client']['external_source'] = 'norteia'
        data['client']['external_id'] = record['id']
        data.setdefault('norteia_imports', []).append({'source_id': identifier, 'collected_at': collected,
                    'source_updated_at': record.get('updated_at'), 'traffic_only': record.get('traffic_only'),
                    'proposals': proposals})
        if not (Path(folder)/source_file).exists():
            clientes.atomic_json(Path(folder)/source_file, record)
        data['evidence'].append(evidence)
        return {'action': 'norteia_import', 'source_id': identifier, 'before': before,
                'seeded_fields': list(before), 'proposals': proposals}
    return clientes.mutate(folder, apply)


def prepare_portfolio(export, organization_id, base, include_ended=False):
    collected, records = prepare_export(export, organization_id)
    base = Path(base).expanduser().resolve()
    if base.is_relative_to(clientes.ROOT) and not any(base.is_relative_to(clientes.ROOT/name) for name in ('projetos', 'work')):
        raise ValueError('Dentro do Studio, use projetos/ ou work/ para dados privados.')
    base.mkdir(parents=True, exist_ok=True)
    ignore = base/'.gitignore'
    original = ignore.read_text(encoding='utf-8') if ignore.exists() else ''
    if '# FEMO Norteia privado' not in original:
        ignore.write_text(original+'\n# FEMO Norteia privado\n*\n', encoding='utf-8')
    registry_file = base/'carteira-norteia.json'
    registry = clientes.read_json(registry_file) if registry_file.exists() else {
        'schema_version': 1, 'organization_id': organization_id, 'clients': {}}
    if registry.get('organization_id') != organization_id:
        raise ValueError('A base já pertence a outra organização.')
    summary = {'created': 0, 'updated': 0, 'unchanged': 0, 'ended_skipped': 0}
    for record in records:
        if record.get('ended_at') and record['ended_at'] <= collected and not include_ended:
            summary['ended_skipped'] += 1
            continue
        previous = registry['clients'].get(record['id'])
        slug = previous['folder'] if previous else client_slug(record)
        folder = (base/slug).resolve()
        if not folder.is_relative_to(base) or folder == base:
            raise ValueError('Pasta registrada fora da base.')
        if not folder.exists():
            clientes.create_client(slug, record['name'], base=base)
            summary['created'] += 1
        else:
            _, existing, _ = clientes.load(folder)
            if existing['client'].get('external_id') != record['id']:
                raise ValueError('Pasta existente sem vínculo com este cadastro; nada será substituído.')
        changed = import_record(folder, record, collected)
        summary['updated' if changed else 'unchanged'] += 1
        registry['clients'][record['id']] = {'name': record['name'], 'folder': slug,
                'ended_at': record.get('ended_at'), 'traffic_only': record.get('traffic_only'),
                'last_seen': collected}
        clientes.atomic_json(registry_file, registry)
    registry['collected_at'] = collected
    registry['last_summary'] = summary
    clientes.atomic_json(registry_file, registry)
    lines = ['# Carteira Norteia · privada', '', 'Preparação cadastral; pesquisa individual ainda não concluída.', '',
             'Objetivo comercial, identidade vigente e aprovação continuam dependências específicas de cada cliente.', '']
    for entry in sorted(registry['clients'].values(), key=lambda item: item['name'].casefold()):
        scope = 'escopo cadastrado: tráfego' if entry['traffic_only'] else 'confirmar escopo e missão'
        lines.append('- ['+entry['name']+']('+entry['folder']+'/DOSSIÊ.md) · '+scope)
    (base/'CARTEIRA-NORTEIA.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arquivo');parser.add_argument('--organizacao', required=True)
    parser.add_argument('--base', default='projetos/clientes')
    parser.add_argument('--incluir-encerrados', action='store_true')
    args = parser.parse_args()
    try:
        result = prepare_portfolio(clientes.read_json(args.arquivo), args.organizacao,
                                   args.base, args.incluir_encerrados)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('Erro: '+str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
