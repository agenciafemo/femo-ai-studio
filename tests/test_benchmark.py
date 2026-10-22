from copy import deepcopy
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import benchmark


class BenchmarkTests(unittest.TestCase):
    def sample(self):
        return {'period': {'start': '2026-10-01', 'end': '2026-10-20'},
                'posts': [{'id': f'P{i}', 'account': '@ficticio', 'format': 'carousel',
                           'metric': 'likes', 'value': value, 'locator': f'https://example.org/posts/{i}',
                           'published_at': '2026-10-02', 'collected_at': '2026-10-20',
                           'phase': 'atual', 'paid': False, 'collab': False}
                          for i, value in enumerate([10, 12, 10, 8, 100])]}

    def test_same_account_median_and_traceable_ids(self):
        result = benchmark.analyse(self.sample())
        group = result['groups'][0]
        self.assertEqual(group['median'], 10)
        self.assertEqual(group['posts'][0]['multiple'], 10)
        self.assertEqual(len(group['baseline_ids']), 5)

    def test_hidden_metric_excluded_zero_preserved(self):
        sample = self.sample()
        sample['posts'][0]['value'] = None
        sample['posts'][1]['value'] = 0
        result = benchmark.analyse(sample, 2)
        self.assertEqual(len(result['excluded']), 1)
        self.assertEqual(result['groups'][0]['n'], 4)
        self.assertEqual(result['groups'][0]['posts'][-1]['value'], 0)

    def test_different_metrics_and_collabs_do_not_share_baseline(self):
        sample = self.sample()
        extra = deepcopy(sample['posts'][0]);extra.update(id='PLAY', metric='plays', value=100000)
        collab = deepcopy(sample['posts'][0]);collab.update(id='COLLAB', collab=True)
        sample['posts'] += [extra, collab]
        result = benchmark.analyse(sample)
        self.assertEqual(len(result['groups']), 3)
        self.assertEqual(sorted(g['n'] for g in result['groups']), [1, 1, 5])
        self.assertTrue(all(g['posts'][0]['multiple'] is None for g in result['groups'] if g['n'] == 1))

    def test_no_ratio_if_zero_baseline_or_small_sample(self):
        sample = self.sample()
        for post in sample['posts']:
            post['value'] = 0
        self.assertTrue(all(p['multiple'] is None for p in benchmark.analyse(sample)['groups'][0]['posts']))
        small = self.sample();small['posts'] = small['posts'][:2]
        self.assertIsNone(benchmark.analyse(small)['groups'][0]['posts'][0]['multiple'])

    def test_publication_date_and_numeric_integrity(self):
        sample = self.sample();sample['posts'][0]['value'] = float('nan')
        with self.assertRaises(ValueError):benchmark.analyse(sample)
        sample = self.sample();sample['posts'][0]['published_at'] = None
        self.assertEqual(benchmark.analyse(sample)['excluded'][0]['id'], 'P0')


if __name__ == '__main__':
    unittest.main()
