from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import clientes
import entregas

ROOT = Path(__file__).resolve().parents[1]
TMP = ROOT/'work/tests'
TMP.mkdir(parents=True, exist_ok=True)


class DeliveryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=TMP)
        self.folder = clientes.create_client('marca-ficticia', 'Marca Fictícia', base=self.temp.name)
        clientes.add_evidence(self.folder, {'id': 'BRIEF-01', 'kind': 'user_brief',
            'locator': 'entradas/briefing.md', 'collected_at': clientes.today(), 'access': 'full',
            'observation': 'Dados fictícios para testar preparação por entrega.'})
        for field in ('perfil', 'objetivo', 'publico', 'voz', 'limites', 'posicionamento'):
            clientes.set_field(self.folder, field, 'Contexto fictício confirmado.', 'confirmado', ['BRIEF-01'])

    def tearDown(self):
        self.temp.cleanup()

    def test_copy_and_key_visual_have_different_dependencies(self):
        copy = entregas.context_for(self.folder, 'carrossel', 'Uma dúvida do público')
        visual = entregas.context_for(self.folder, 'key-visual', 'Campanha fictícia')
        self.assertTrue(copy['required_context_ready'])
        self.assertFalse(visual['required_context_ready'])
        self.assertIn('identidade', [gap['field'] for gap in visual['blockers']])
        self.assertIn('identidade', [gap['field'] for gap in copy['warnings']])

    def test_only_relevant_evidence_is_selected(self):
        clientes.add_evidence(self.folder, {'id': 'METRICA-01', 'kind': 'analytics',
            'locator': 'pesquisa/numeros.json', 'collected_at': clientes.today(), 'access': 'full',
            'observation': 'Métrica fictícia.'})
        clientes.set_field(self.folder, 'metricas', 'Dado fictício.', 'confirmado', ['METRICA-01'])
        context = entregas.context_for(self.folder, 'briefing', 'Pedido fictício')
        self.assertEqual([e['id'] for e in context['evidence']], ['BRIEF-01'])
        self.assertNotIn('metricas', context['fields'])

    def test_preparation_is_versioned_and_does_not_change_dossier(self):
        original = (self.folder/'dossie.json').read_bytes()
        first = entregas.prepare(self.folder, 'reels', 'Tema fictício', 'Só direção de gravação.')
        second = entregas.prepare(self.folder, 'reels', 'Tema fictício')
        self.assertNotEqual(first['folder'], second['folder'])
        self.assertEqual(original, (self.folder/'dossie.json').read_bytes())
        self.assertTrue((Path(first['folder'])/'CONTEXTO.json').is_file())
        text = (Path(first['folder'])/'BRIEFING.md').read_text(encoding='utf-8')
        self.assertIn('Só direção de gravação.', text)
        self.assertIn('ainda deve ser desenvolvida', text)

    def test_open_conflict_remains_blocking_for_relevant_output(self):
        clientes.set_field(self.folder, 'identidade', 'Manual fictício.', 'confirmado', ['BRIEF-01'])
        data = clientes.read_json(self.folder/'dossie.json')
        data['conflicts'].append({'id': 'C1', 'fields': ['identidade'], 'status': 'aberto'})
        clientes.atomic_json(self.folder/'dossie.json', data)
        context = entregas.context_for(self.folder, 'key-visual', 'Campanha fictícia')
        self.assertFalse(context['required_context_ready'])
        self.assertTrue(context['conflicts'])

    def test_unknown_type_and_blank_theme_do_not_create_deliveries(self):
        for kind, theme in (('../../fora', 'Tema'), ('reels', ' ')):
            with self.assertRaises(ValueError):entregas.prepare(self.folder, kind, theme)
        self.assertEqual(list((self.folder/'producao').iterdir()), [])

    def test_catalog_fields_exist_and_all_products_define_a_result(self):
        model = clientes.read_json(clientes.TEMPLATE)
        known = {field['id'] for field in model['fields']}
        for product in entregas.catalog().values():
            self.assertTrue(set(product['required_fields']+product['context_fields']).issubset(known))
            self.assertTrue(product['sections'])
            self.assertTrue(product['completion'])


if __name__ == '__main__':
    unittest.main()
