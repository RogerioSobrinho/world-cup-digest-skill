import json
import unittest
from pathlib import Path

from world_cup_digest.config import Settings
from world_cup_digest.http import HttpClient
from world_cup_digest.providers.api_football import ApiFootballProvider, format_api_errors


class ApiFootballNormalizeTests(unittest.TestCase):
    def test_api_football_normalizes_events_and_stats(self):
        fixture = Path(__file__).resolve().parents[1] / "skills" / "world-cup-digest" / "fixtures" / "api_football_fixture_sample.json"
        settings = Settings.from_env(no_cache=True)
        provider = ApiFootballProvider(settings, HttpClient(settings))
        matches = provider.normalize(json.loads(fixture.read_text()), "fixture://sample")
        self.assertEqual(len(matches), 1)
        match = matches[0]
        self.assertEqual(match.score_text, "1 x 2")
        self.assertEqual(match.events[-1].player, "Forward Three")
        self.assertEqual(match.stats["Brazil"].shots, 14)
        self.assertEqual(match.stats["Mexico"].possession, 47.0)

    def test_format_api_errors_handles_plan_error(self):
        error = format_api_errors({"plan": "Free plans do not have access to this season."})
        self.assertEqual(error, "plan: Free plans do not have access to this season.")


if __name__ == "__main__":
    unittest.main()
