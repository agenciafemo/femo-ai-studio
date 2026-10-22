"""Comparar posts por conta/formato/métrica, sem substituir mediana por seguidores.

Entrada JSON: period {start,end} e posts. Não coleta conteúdo nem comprova viralização.
"""
import argparse
from collections import defaultdict
from datetime import date
import json
import math
from pathlib import Path
import statistics
import sys


def iso(value):
    return date.fromisoformat(value)


def analyse(sample, minimum=5):
    if isinstance(minimum, bool) or not isinstance(minimum, int) or minimum < 2:
        raise ValueError('Mínimo deve ser inteiro >= 2; é convenção operacional, não prova estatística.')
    start, end = iso(sample['period']['start']), iso(sample['period']['end'])
    if start > end:
        raise ValueError('Período invertido.')
    groups = defaultdict(list)
    excluded = []
    ids = set()
    for item in sample['posts']:
        identifier = item.get('id')
        if not isinstance(identifier, str) or not identifier or identifier in ids:
            raise ValueError('Cada post precisa de ID único.')
        ids.add(identifier)
        for key in ('account', 'format', 'metric', 'locator', 'collected_at'):
            if not isinstance(item.get(key), str) or not item[key].strip():
                raise ValueError(f'Post {identifier} sem {key}.')
        collected = iso(item['collected_at'])
        value = item.get('value')
        if value is None:
            excluded.append({'id': identifier, 'reason': 'métrica ausente/oculta, não é zero'})
            continue
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
            raise ValueError(f'Métrica inválida em {identifier}.')
        if not item.get('published_at'):
            excluded.append({'id': identifier, 'reason': 'data da publicação desconhecida'})
            continue
        published = iso(item['published_at'])
        if collected < published:
            raise ValueError(f'Coleta anterior à publicação em {identifier}.')
        if not start <= published <= end:
            excluded.append({'id': identifier, 'reason': 'publicação fora do período'})
            continue
        for key in ('paid', 'collab'):
            if item.get(key) is not None and not isinstance(item[key], bool):
                raise ValueError(f'{key} precisa ser booleano ou null.')
        key = (item['account'].lower(), item['format'], item['metric'], item.get('phase'),
               item.get('paid'), item.get('collab'))
        groups[key].append(item)
    results = []
    for key, rows in sorted(groups.items(), key=lambda pair: repr(pair[0])):
        account, form, metric, phase, paid, collab = key
        median = statistics.median(row['value'] for row in rows)
        limitations = ['Amostra observacional: associação não demonstra causa.',
                       'Idade das publicações e contexto de distribuição podem alterar a comparação.']
        if len(rows) < minimum:
            limitations.append('Amostra abaixo do mínimo operacional configurado; multiplicadores omitidos.')
        if median == 0:
            limitations.append('Mediana zero; multiplicadores indefinidos.')
        if None in (phase, paid, collab):
            limitations.append('Há contexto de marca, anúncio ou collab desconhecido.')
        usable = len(rows) >= minimum and median > 0
        results.append({'account': account, 'format': form, 'metric': metric, 'phase': phase,
                        'paid': paid, 'collab': collab, 'n': len(rows), 'median': median,
                        'baseline_ids': [row['id'] for row in rows], 'limitations': limitations,
                        'posts': [{'id': row['id'], 'value': row['value'], 'locator': row['locator'],
                                   'published_at': row['published_at'], 'collected_at': row['collected_at'],
                                   'multiple': round(row['value']/median, 4) if usable else None}
                                  for row in sorted(rows, key=lambda row: row['value'], reverse=True)]})
    return {'period': sample['period'], 'minimum': minimum, 'groups': results, 'excluded': excluded,
            'note': 'Multiplicador é descritivo da amostra. Não classifica viral, não mede venda nem garante repetição.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('arquivo');parser.add_argument('--minimo', type=int, default=5)
    parser.add_argument('--saida')
    args = parser.parse_args()
    try:
        with open(args.arquivo, encoding='utf-8-sig') as stream:
            result = analyse(json.load(stream), args.minimo)
        output = json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False)+'\n'
        if args.saida:
            with Path(args.saida).open('x', encoding='utf-8') as stream:
                stream.write(output)
        else:
            print(output, end='')
        return 0
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('Erro: '+str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
