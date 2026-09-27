import importlib.util
from datetime import datetime, timezone
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'update_profile_stats.py'

class ProfileStatsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not SCRIPT.exists():
            raise AssertionError('The automatic profile statistics updater has not been implemented.')
        spec = importlib.util.spec_from_file_location('profile_stats', SCRIPT)
        cls.stats = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.stats)

    def test_calendar_windows_do_not_overlap_or_skip_a_contribution_year(self):
        now = datetime(2026, 9, 27, 9, 30, tzinfo=timezone.utc)
        self.assertEqual(self.stats.year_windows([2026, 2024, 2021], now), [
            (2021, '2021-01-01T00:00:00Z', '2021-12-31T23:59:59Z'),
            (2024, '2024-01-01T00:00:00Z', '2024-12-31T23:59:59Z'),
            (2026, '2026-01-01T00:00:00Z', '2026-09-27T09:30:00Z'),
        ])

    def test_private_contributions_are_not_added_twice_or_counted_as_commits(self):
        rows = [
            {'year': 2025, 'commits': 10, 'contributions': 105, 'restricted': 90},
            {'year': 2026, 'commits': 15, 'contributions': 220, 'restricted': 200},
        ]
        totals = self.stats.summarize(rows, 2026)
        self.assertEqual(totals, {'commits_year': 15, 'commits_all_time': 25,
                                 'contributions_year': 220, 'contributions_all_time': 325})

    def test_api_failure_preserves_last_successful_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'brand').mkdir()
            (root / 'brand/public-stats.json').write_text('last-good-data')
            with patch.object(self.stats, 'collect', side_effect=RuntimeError('API unavailable')):
                with self.assertRaisesRegex(RuntimeError, 'API unavailable'):
                    self.stats.refresh(root, 'FasHub', datetime.now(timezone.utc))
            self.assertEqual((root / 'brand/public-stats.json').read_text(), 'last-good-data')

    def test_month_totals_ignore_calendar_padding_and_keep_future_months_absent(self):
        days = [{'date':'2025-12-31','contributionCount':99},
                {'date':'2026-01-01','contributionCount':2},
                {'date':'2026-01-31','contributionCount':3},
                {'date':'2026-02-01','contributionCount':7},
                {'date':'2026-03-01','contributionCount':44}]
        now = datetime(2026, 2, 10, tzinfo=timezone.utc)
        self.assertEqual(self.stats.monthly_counts(days, now), [5, 7])

if __name__ == '__main__':
    unittest.main()
