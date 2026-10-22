from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import qualidade


class QualityTests(unittest.TestCase):
    def test_known_contrast_extremes_and_symmetry(self):
        self.assertEqual(qualidade.contrast('#000000', '#FFFFFF')['ratio'], 21)
        self.assertEqual(qualidade.contrast('#FFFFFF', '#FFFFFF')['ratio'], 1)
        self.assertEqual(qualidade.contrast('#AA7755', '#EEEEEE')['ratio'],
                         qualidade.contrast('#EEEEEE', '#AA7755')['ratio'])

    def test_low_contrast_does_not_pass(self):
        self.assertFalse(qualidade.contrast('#B7A189', '#D2C1AD')['passes_pair'])
        self.assertTrue(qualidade.contrast('#40352E', '#F5F1EA')['passes_pair'])

    def test_invalid_color_and_target(self):
        for color in ('#fff', 'white', '#ZZ3344'):
            with self.assertRaises(ValueError):qualidade.contrast(color, '#FFFFFF')
        with self.assertRaises(ValueError):qualidade.contrast('#000000', '#FFFFFF', float('nan'))

    def test_spacing_and_equivalent_accents_are_accepted(self):
        result = qualidade.compare_copy('Não é garantia.', 'Na\u0303o  é\ngarantia.')
        self.assertTrue(result['same_ignoring_spacing'])

    def test_negation_and_number_changes_are_detected(self):
        self.assertFalse(qualidade.compare_copy('Não substitui avaliação.', 'Substitui avaliação.')['same_ignoring_spacing'])
        result = qualidade.compare_copy('2 sessões podem ajudar.', '20 sessões podem ajudar.')
        self.assertFalse(result['same_ignoring_spacing'])
        self.assertTrue(result['differences'])


if __name__ == '__main__':
    unittest.main()
