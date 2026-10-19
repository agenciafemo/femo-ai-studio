"""Copia a skill completa para Claude Code e/ou Codex, sem instalar programas."""
from __future__ import annotations
import argparse
import filecmp
import json
from pathlib import Path
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[1]

def package_files():
    names = ['SKILL.md', 'LICENSE', 'THIRD_PARTY.md', 'scripts/femo.py', 'scripts/install_skill.py', 'scripts/transcribe_local.py', 'scripts/femo.ps1',
             'docs/PESQUISA.md', 'examples/carrossel-sobrancelhas.md']
    result = [Path(n) for n in names]
    for folder in ['references', 'assets']:
        result += [p.relative_to(ROOT) for p in (ROOT/folder).rglob('*') if p.is_file()]
    if not all((ROOT/n).is_file() for n in result):
        raise ValueError('Pacote incompleto. Baixe e extraia o repositório inteiro.')
    return result

def install(target, agent='both', user=False):
    selected = ['claude', 'codex'] if agent == 'both' else [agent]
    base = Path.home() if user else Path(target).expanduser().resolve()
    files = package_files()
    outputs = []
    destinations = [base/('.claude' if a == 'claude' else '.agents')/'skills'/'femo-ai-studio' for a in selected]
    for dest in destinations:
        if dest.exists():
            identical = all((dest/n).is_file() and filecmp.cmp(ROOT/n,dest/n,shallow=False) for n in files)
            if not identical:
                raise ValueError(f'Já existe uma instalação diferente em {dest}. Faça backup e atualize conscientemente; nada foi substituído.')
    for dest in destinations:
        if dest.exists():
            outputs.append({'path':str(dest),'status':'já instalado, conteúdo conferido'});continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        staging = Path(tempfile.mkdtemp(prefix='.femo-install-',dir=dest.parent))
        try:
            for name in files:
                out = staging/name;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,out)
            staging.rename(dest)
        except Exception:
            # Preservar staging para diagnóstico, sem remover conteúdo do usuário.
            raise
        outputs.append({'path':str(dest),'status':'instalado','files':len(files)})
    return outputs

def main():
    p=argparse.ArgumentParser(description=__doc__)
    group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--target');group.add_argument('--user',action='store_true')
    p.add_argument('--agent',choices=['claude','codex','both'],default='both')
    a=p.parse_args()
    try:
        print(json.dumps(install(a.target,a.agent,a.user),ensure_ascii=False,indent=2))
    except (ValueError,OSError) as exc:
        p.exit(2,str(exc)+'\n')
if __name__=='__main__':main()
