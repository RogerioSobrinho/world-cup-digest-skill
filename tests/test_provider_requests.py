import unittest
from pathlib import Path

from world_cup_digest.config import Settings
from world_cup_digest.http import HttpClient
from world_cup_digest.models import Query
from world_cup_digest.providers.api_football import ApiFootballProvider


class ProviderRequestTests(unittest.TestCase):
    def test_api_football_live_request_uses_live_all(self):
        settings = Settings(cache_dir=Path("/tmp/world-cup-digest-test"), timeout=1, env={"API_FOOTBALL_KEY": "secret"})
        provider = ApiFootballProvider(settings, HttpClient(settings))

        url, headers = provider.build_request(Query(season="2022", live=True))

        self.assertIn("live=all", url)
        self.assertIn("league=1", url)
        self.assertIn("season=2022", url)
        self.assertEqual(headers["x-apisports-key"], "secret")


if __name__ == "__main__":
    unittest.main()
