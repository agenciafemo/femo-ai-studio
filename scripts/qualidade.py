"""Conferir contraste de cores e diferenças de copy; não substitui a revisão visual."""
import argparse
import difflib
import json
import re
import unicodedata
from pathlib import Path
import sys


def luminance(hex_color):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', hex_color):
        raise ValueError('Use cor hexadecimal completa, como #40352E.')
    values = [int(hex_color[i:i+2], 16)/255 for i in (1, 3, 5)]
    linear = [v/12.92 if v <= 0.04045 else ((v+0.055)/1.055)**2.4 for v in values]
    return .2126*linear[0]+.7152*linear[1]+.0722*linear[2]


def contrast(front, back, target=4.5):
    if not 1 <= target <= 21:
        raise ValueError('Meta de contraste deve estar entre 1 e 21.')
    light, dark = sorted((luminance(front), luminance(back)), reverse=True)
    ratio = (light+.05)/(dark+.05)
    return {'ratio': round(ratio, 3), 'target': target, 'passes_pair': ratio >= target,
            'limitation': 'Avalia apenas o par de cores sólidas. Foto, textura, fonte fina e redução exigem inspeção da prévia final.'}


def normalize_copy(value):
    if not isinstance(value, str):
        raise ValueError('A copy deve ser texto.')
    return re.sub(r'\s+', ' ', unicodedata.normalize('NFC', value)).strip()


def compare_copy(reference, output):
    a, b = normalize_copy(reference), normalize_copy(output)
    return {'same_ignoring_spacing': a == b,
            'differences': list(difflib.ndiff(a.split(), b.split())) if a != b else [],
            'limitation': 'Diferença requer revisão contra o pedido. Texto extraído não comprova que está legível ou visível na arte.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='mode', required=True)
    colors = sub.add_parser('contraste');colors.add_argument('--frente', required=True)
    colors.add_argument('--fundo', required=True);colors.add_argument('--meta', type=float, default=4.5)
    copy = sub.add_parser('copy');copy.add_argument('arquivo', help='JSON com reference e output')
    args = parser.parse_args()
    try:
        if args.mode == 'contraste':
            result = contrast(args.frente, args.fundo, args.meta)
            passed = result['passes_pair']
        else:
            value = json.loads(Path(args.arquivo).read_text(encoding='utf-8-sig'))
            result = compare_copy(value['reference'], value['output'])
            passed = result['same_ignoring_spacing']
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if passed else 2
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print('Erro: '+str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
