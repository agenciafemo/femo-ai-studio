"""Fixtures fictícias: verificar lacunas reais, histórico e portabilidade."""
from copy import deepcopy
from datetime import date, timedelta
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import clientes
import install_skill

TEST_TMP = ROOT/'work/tests'
TEST_TMP.mkdir(parents=True, exist_ok=True)


class ClientTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=TEST_TMP)
        self.base = Path(self.temp.name)
        self.folder = clientes.create_client('atelier-ficticio', 'Ateliê Fictício', base=self.base)
        self.source = {'id': 'BRIEF-001', 'kind': 'user_brief', 'locator': 'entradas/briefing.md',
                       'collected_at': clientes.today(), 'access': 'full',
                       'observation': 'Fixture fictícia: objetivo, serviço e identidade recebidos da equipe.'}

    def tearDown(self):
        self.temp.cleanup()

    def loaded(self):
        return clientes.load(self.folder)[1:]

    def complete(self):
        data, model = self.loaded()
        data['evidence'] = [deepcopy(self.source)]
        for spec in model['fields']:
            if spec['required_for']:
                data['fields'][spec['id']] = {'value': 'Informação fictícia para teste estrutural.',
                    'status': 'confirmado', 'evidence_ids': ['BRIEF-001'],
                    'reviewed_at': clientes.today(), 'note': ''}
        return data, model

    def test_new_client_has_precise_blockers(self):
        data, model = self.loaded()
        result = clientes.evaluate(data, model, 'planejamento')
        self.assertFalse(result['ready'])
        objective = next(item for item in result['gaps'] if item['field'] == 'objetivo')
        self.assertTrue(objective['blocking'])
        self.assertIn('período', objective['question'])
        self.assertTrue(objective['owner'])
        self.assertTrue((self.folder/'LACUNAS.md').is_file())

    def test_required_complete_optional_metrics_do_not_block(self):
        data, model = self.complete()
        result = clientes.evaluate(data, model)
        self.assertTrue(result['ready'])
        self.assertTrue(any(item['field'] == 'metricas' for item in result['gaps']))

    def test_hypothesis_and_missing_source_cannot_count_as_confirmed(self):
        data, model = self.complete()
        data['fields']['voz']['status'] = 'hipotese'
        data['fields']['objetivo']['evidence_ids'] = ['INEXISTENTE']
        result = clientes.evaluate(data, model)
        self.assertFalse(result['ready'])
        gaps = {item['field']: item for item in result['gaps']}
        self.assertIn('fonte citada não registrada', gaps['objetivo']['reasons'])
        self.assertIn('estado: hipotese', gaps['voz']['reasons'])

    def test_blocked_sources_do_not_confirm_a_fact(self):
        data, model = self.complete()
        data['evidence'][0]['access'] = 'blocked'
        self.assertFalse(clientes.evaluate(data, model)['ready'])

    def test_conflict_blocks_even_with_a_confirmed_field(self):
        data, model = self.complete()
        data['conflicts'] = [{'id': 'C1', 'fields': ['identidade'], 'status': 'aberto',
                             'note': 'Manual e orientação recebida divergem.'}]
        clientes.validate(data, model)
        self.assertFalse(clientes.evaluate(data, model)['ready'])
        self.assertTrue(clientes.evaluate(data, model, 'planejamento')['ready'])
        data['conflicts'][0]['status'] = 'resolvido'
        self.assertTrue(clientes.evaluate(data, model)['ready'])

    def test_review_deadline_and_future_collection(self):
        data, model = self.complete()
        data['fields']['voz']['reviewed_at'] = (date.today()-timedelta(days=1000)).isoformat()
        self.assertFalse(clientes.evaluate(data, model)['ready'])
        data, model = self.complete()
        data['evidence'][0]['collected_at'] = (date.today()+timedelta(days=5)).isoformat()
        self.assertFalse(clientes.evaluate(data, model)['ready'])

    def test_na_cannot_bypass_commercial_objective(self):
        data, model = self.complete()
        data['fields']['objetivo'].update(status='nao_aplicavel', note='Não definido ainda.')
        self.assertFalse(clientes.evaluate(data, model)['ready'])

    def test_updates_preserve_history_and_prior_snapshot(self):
        clientes.add_evidence(self.folder, self.source)
        clientes.set_field(self.folder, 'objetivo', 'Priorizar avaliações do serviço fictício.',
                           'confirmado', ['BRIEF-001'])
        clientes.set_field(self.folder, 'objetivo', 'Nova proposta, ainda não aprovada.',
                           'hipotese', ['BRIEF-001'])
        data, _ = self.loaded()
        change = data['history'][-1]
        self.assertEqual(change['before']['status'], 'confirmado')
        self.assertEqual(change['after']['status'], 'hipotese')
        snapshots = [clientes.read_json(p) for p in (self.folder/'historico').glob('*.json')]
        self.assertTrue(any(s['fields']['objetivo']['status'] == 'confirmado' for s in snapshots))
        self.assertIn('Nova proposta', (self.folder/'DOSSIÊ.md').read_text(encoding='utf-8'))

    def test_evidence_import_is_idempotent_and_rejects_id_reuse(self):
        self.assertTrue(clientes.add_evidence(self.folder, self.source))
        self.assertFalse(clientes.add_evidence(self.folder, self.source))
        before = (self.folder/'dossie.json').read_bytes()
        with self.assertRaises(ValueError):
            clientes.add_evidence(self.folder, {**self.source, 'observation': 'Outra informação.'})
        self.assertEqual(before, (self.folder/'dossie.json').read_bytes())
        self.assertFalse((self.folder/'.femo.lock').exists())

    def test_new_does_not_overwrite_existing_client_or_escape_base(self):
        before = (self.folder/'dossie.json').read_bytes()
        with self.assertRaises(FileExistsError):
            clientes.create_client('atelier-ficticio', 'Outro nome', base=self.base)
        self.assertEqual(before, (self.folder/'dossie.json').read_bytes())
        for slug in ('../outro', 'CON', 'con', 'a/b', 'nome.'):
            with self.assertRaises(ValueError):
                clientes.create_client(slug, 'Teste', base=self.base)

    def test_invalid_evidence_rejected_before_mutation(self):
        before = (self.folder/'dossie.json').read_bytes()
        with self.assertRaises(ValueError):
            clientes.add_evidence(self.folder, {**self.source, 'collected_at': 'ontem'})
        self.assertEqual(before, (self.folder/'dossie.json').read_bytes())

    def test_installer_retries_temporary_windows_lock(self):
        from unittest.mock import patch
        original = Path.rename
        calls = []
        def temporarily_locked(source, target):
            calls.append(str(source))
            if len(calls) < 3:
                raise PermissionError('Lock temporário simulado no Windows')
            return original(source, target)
        with patch('install_skill.Path.rename', new=temporarily_locked):
            result = install_skill.install(self.base/'lock-test', 'codex')
        self.assertEqual(len(calls), 3)
        self.assertTrue((Path(result[0]['path'])/'scripts/norteia.py').is_file())

    def test_installed_package_can_create_client_without_source_repo(self):
        install_skill.install(self.base/'destino', 'codex')
        package = self.base/'destino/.agents/skills/femo-ai-studio'
        for rel in ('scripts/clientes.py', 'scripts/norteia.py', 'scripts/qualidade.py', 'docs/NORTEIA.md', 'examples/norteia-minimo.json', 'templates/cliente/campos.json', 'docs/CATALOGO.md',
                    'third_party/instagram-agent/skills/ig-viral/swipe.py',
                    'third_party/instagram-skills/lib/apify_client.py',
                    'skills/femo-direcao-carrosseis/SKILL.md'):
            self.assertTrue((package/rel).is_file(), rel)
        import subprocess
        result = subprocess.run([sys.executable, '-X', 'utf8', str(package/'scripts/clientes.py'), 'novo',
                                 'cliente-portavel', '--nome', 'Cliente Fictício',
                                 '--base', str(self.base/'dados')], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        dossier = self.base/'dados/cliente-portavel/dossie.json'
        self.assertTrue(dossier.is_file())
        check = subprocess.run([sys.executable, '-X', 'utf8', str(package/'scripts/clientes.py'), 'verificar',
                                str(dossier.parent), '--etapa', 'design'],
                               capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(check.returncode, 2, check.stderr)
        self.assertFalse(json.loads(check.stdout)['ready'])


if __name__ == '__main__':
    unittest.main()
