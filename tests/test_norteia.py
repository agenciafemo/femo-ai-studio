from copy import deepcopy
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import clientes
import norteia

ROOT = Path(__file__).resolve().parents[1]
TEST_TMP = ROOT/'work/tests'
TEST_TMP.mkdir(parents=True, exist_ok=True)
ORG = 'org-ficticia'
ID = '11111111-1111-4111-8111-111111111111'


class NorteiaTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=TEST_TMP)
        self.base = Path(self.tmp.name)/'clientes'
        self.record = {'id': ID, 'organization_id': ORG, 'name': 'Ateliê Fictício',
                       'segment': None, 'traffic_only': False, 'ended_at': None,
                       'updated_at': clientes.today(), 'public_link_token': 'NAO-COPIAR',
                       'contact_email': 'privado@example.org',
                       'content_profile': {'positioning': 'Serviço cuidadoso e artesanal.',
                                           'voice_personality': 'Clara e acolhedora.',
                                           'products_services': ['Serviço fictício'],
                                           'formality': 'balanced', 'emoji_limit': 2,
                                           'unknown_secret': 'NAO-COPIAR'}}
        self.export = {'schema_version': 1, 'source': 'norteia', 'collected_at': clientes.today(),
                       'organization_id': ORG, 'clients': [deepcopy(self.record)]}

    def tearDown(self):
        self.tmp.cleanup()

    def run_import(self):
        return norteia.prepare_portfolio(self.export, ORG, self.base)

    def folder(self):
        registry = clientes.read_json(self.base/'carteira-norteia.json')
        return self.base/registry['clients'][ID]['folder']

    def test_prepare_seeds_sources_but_does_not_approve_strategy(self):
        result = self.run_import()
        self.assertEqual(result['created'], 1)
        _, data, model = clientes.load(self.folder())
        self.assertEqual(data['fields']['perfil']['status'], 'confirmado')
        self.assertEqual(data['fields']['voz']['status'], 'hipotese')
        self.assertEqual(data['fields']['objetivo']['status'], 'ausente')
        self.assertFalse(clientes.evaluate(data, model, 'design')['ready'])
        self.assertTrue((self.base/'CARTEIRA-NORTEIA.md').is_file())

    def test_private_allowlist_excludes_tokens_and_contacts(self):
        self.run_import()
        text = '\n'.join(p.read_text(encoding='utf-8') for p in self.base.rglob('*.json'))
        self.assertNotIn('NAO-COPIAR', text)
        self.assertNotIn('privado@example.org', text)
        self.assertIn('Serviço cuidadoso', text)

    def test_repeat_does_not_duplicate_history_or_client(self):
        self.run_import()
        before = (self.folder()/'dossie.json').read_bytes()
        result = self.run_import()
        self.assertEqual(result['created'], 0)
        self.assertEqual(result['unchanged'], 1)
        self.assertEqual(before, (self.folder()/'dossie.json').read_bytes())

    def test_new_source_preserves_approved_local_voice_and_opens_conflict(self):
        self.run_import()
        folder = self.folder()
        data = clientes.read_json(folder/'dossie.json')
        source_id = data['evidence'][0]['id']
        clientes.set_field(folder, 'voz', {'regra': 'Decisão aprovada pela cliente.'}, 'confirmado', [source_id])
        self.export['clients'][0]['content_profile']['voice_personality'] = 'Outra orientação recebida.'
        self.run_import()
        _, data, _ = clientes.load(folder)
        self.assertEqual(data['fields']['voz']['value'], {'regra': 'Decisão aprovada pela cliente.'})
        self.assertTrue(any(c['status'] == 'aberto' and 'voz' in c['fields'] for c in data['conflicts']))
        self.assertTrue(data['norteia_imports'][-1]['proposals'])

    def test_wrong_organization_or_path_id_fails_before_creating_base(self):
        self.export['clients'][0]['organization_id'] = 'outra'
        with self.assertRaises(ValueError):self.run_import()
        self.assertFalse(self.base.exists())
        self.export['clients'][0] = deepcopy(self.record)
        self.export['clients'][0]['id'] = '../../fora'
        with self.assertRaises(ValueError):self.run_import()
        self.assertFalse(self.base.exists())

    def test_ended_skipped_and_default_voice_is_not_imported_as_brand(self):
        self.export['clients'][0]['ended_at'] = '2020-01-01'
        self.assertEqual(self.run_import()['ended_skipped'], 1)
        self.export['clients'][0]['ended_at'] = None
        self.export['clients'][0]['content_profile'] = {'formality': 'balanced', 'emoji_limit': 2}
        self.run_import()
        _, data, _ = clientes.load(self.folder())
        self.assertEqual(data['fields']['voz']['status'], 'ausente')

    def test_rename_keeps_same_workspace_by_external_identity(self):
        self.run_import()
        folder = self.folder()
        self.export['clients'][0]['name'] = 'Novo nome fictício'
        self.run_import()
        self.assertEqual(folder, self.folder())
        registry = clientes.read_json(self.base/'carteira-norteia.json')
        self.assertEqual(registry['clients'][ID]['name'], 'Novo nome fictício')

    def test_public_destination_rejected(self):
        with self.assertRaises(ValueError):
            norteia.prepare_portfolio(self.export, ORG, ROOT/'docs/clientes')


if __name__ == '__main__':
    unittest.main()
