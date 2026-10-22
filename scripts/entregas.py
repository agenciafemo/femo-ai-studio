"""Preparar contexto e briefing de uma entrega a partir da base privada do cliente.

Não gera arte, não pesquisa fontes e não publica. Mantém o dossiê intacto.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import uuid
import clientes

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT/'templates/entregas/catalogo.json'


def catalog():
    data = clientes.read_json(CATALOG)
    if data.get('schema_version') != 1:
        raise ValueError('Catálogo incompatível.')
    products = data.get('products')
    if not isinstance(products, list) or not products:
        raise ValueError('Catálogo vazio.')
    result = {item['id']: item for item in products}
    if len(result) != len(products):
        raise ValueError('Tipo de entrega duplicado.')
    return result


def context_for(folder, product_id, theme, request='', as_of=None):
    products = catalog()
    if product_id not in products:
        raise ValueError('Entrega desconhecida; use o comando tipos.')
    if not isinstance(theme, str) or not theme.strip():
        raise ValueError('Informe tema ou missão da entrega.')
    folder, data, model = clientes.load(folder)
    product = products[product_id]
    selected = list(dict.fromkeys(product['required_fields']+product['context_fields']))
    unknown = set(selected)-set(data['fields'])
    if unknown:
        raise ValueError('Catálogo cita campos desconhecidos: '+', '.join(sorted(unknown)))
    evaluated = clientes.evaluate(data, model, 'design', as_of)
    pending = {gap['field']: gap for gap in evaluated['gaps']}
    fields = {key: data['fields'][key] for key in selected}
    source_ids = {source for field in fields.values() for source in field['evidence_ids']}
    blockers = []
    warnings = []
    for key in selected:
        if key not in pending:
            continue
        gap = {**pending[key], 'blocking': key in product['required_fields']}
        (blockers if gap['blocking'] else warnings).append(gap)
    previous = folder/'entradas/BASE-ANTERIOR.md'
    return {'schema_version': 1, 'prepared_at': datetime.now(timezone.utc).isoformat(),
            'client': data['client'], 'client_base': str(folder), 'product': product,
            'mission': {'theme': theme.strip(), 'request': request},
            'dossier_sha256': hashlib.sha256((folder/'dossie.json').read_bytes()).hexdigest(),
            'fields': fields, 'evidence': [item for item in data['evidence'] if item['id'] in source_ids],
            'conflicts': [item for item in data['conflicts'] if set(item['fields']).intersection(selected)],
            'decision_paths': [str(folder/'decisoes')]+([str(previous)] if previous.exists() else []),
            'required_context_ready': not blockers, 'blockers': blockers, 'warnings': warnings,
            'limits': 'Preparação de contexto; não é pesquisa nova, validação das fontes, entrega final nem aprovação.'}


def brief_markdown(context):
    product = context['product']
    lines = ['# '+product['name']+' · '+context['client']['name'], '',
             '**Missão:** '+context['mission']['theme'], '',
             context['mission']['request'] or 'Sem instrução adicional nesta preparação.', '',
             'Esta pasta prepara o trabalho. A entrega criativa ainda deve ser desenvolvida e revisada pela IA/equipe.', '',
             '## Como usar a base', '',
             'Ler CONTEXTO.json, fontes citadas e decisões vigentes antes de compor. Preservar estados de hipótese e conflito. '
             'Comparar o dossiê atual com o hash registrado se a base tiver sido alterada. Não publicar ou enviar arquivos por dedução.', '',
             '## Contexto necessário', '']
    for key, field in context['fields'].items():
        lines.append('- '+key+': '+field['status']+' · fontes '+(', '.join(field['evidence_ids']) or 'pendentes'))
    lines += ['', '## Lacunas que impedem concluir a direção', '']
    if not context['blockers']:
        lines += ['Os campos exigidos pelo tipo estão preenchidos estruturalmente. Conferir conteúdo, fontes e dependências da peça.']
    for gap in context['blockers']:
        lines += ['- '+gap['label']+': '+'; '.join(gap['reasons'])+'. '+gap['question']]
    lines += ['', '## Lacunas complementares', '']
    for gap in context['warnings']:
        lines += ['- '+gap['label']+': '+'; '.join(gap['reasons'])+'.']
    lines += ['', '## Perguntas específicas desta peça', '',
              'São pontos para conferir no pedido e no material; só perguntar à equipe o que ainda não foi respondido.', '']
    lines += ['- '+question for question in product['questions']]
    lines += ['', '## Contrato da entrega criativa', '']
    lines += ['- '+section for section in product['sections']]
    lines += ['', '**Critério de conclusão:** '+product['completion'], '',
              '## Retorno à base', '',
              'Ao concluir, registrar fontes utilizadas, proposta, versão, feedback e decisões com seu escopo. '
              'Só promover a regra da marca o que foi confirmado nesse escopo. Medição posterior não deve ser inventada.', '']
    return '\n'.join(lines)


def prepare(folder, product_id, theme, request=''):
    context = context_for(folder, product_id, theme, request)
    folder = Path(context['client_base'])
    production = (folder/'producao').resolve()
    if not production.is_relative_to(folder):
        raise ValueError('Pasta de produção fora da base do cliente.')
    production.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    destination = production/(stamp+'-'+product_id+'-'+uuid.uuid4().hex[:8])
    destination.mkdir(exist_ok=False)
    clientes.atomic_json(destination/'CONTEXTO.json', context)
    (destination/'BRIEFING.md').write_text(brief_markdown(context), encoding='utf-8')
    return {'folder': str(destination), 'required_context_ready': context['required_context_ready'],
            'blocking_fields': [item['field'] for item in context['blockers']],
            'status': 'contexto preparado; entrega criativa ainda não produzida'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('tipos')
    command = commands.add_parser('preparar');command.add_argument('pasta')
    command.add_argument('--tipo', required=True);command.add_argument('--tema', required=True)
    command.add_argument('--pedido', default='')
    args = parser.parse_args()
    try:
        if args.command == 'tipos':
            result = [{'id': key, 'name': value['name']} for key, value in catalog().items()]
        else:
            result = prepare(args.pasta, args.tipo, args.tema, args.pedido)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('Erro: '+str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
