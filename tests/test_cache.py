import json
import hashlib
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

from world_cup_digest.config import Settings
from world_cup_digest.http import HttpClient
from world_cup_digest.providers.api_football import ApiFootballProvider, fixture_state


class CacheTests(unittest.TestCase):
    def test_http_cache_uses_valid_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(cache_dir=Path(tmp), timeout=1, env={}, cache_ttl_default=60)
            client = HttpClient(settings)
            url = "https://example.test/match"

            with patch("urllib.request.urlopen", return_value=fake_response({"value": 1})()) as open_mock:
                self.assertEqual(client.get_json(url), ({"value": 1}, False))
                self.assertEqual(client.get_json(url), ({"value": 1}, True))

            self.assertEqual(open_mock.call_count, 1)

    def test_http_cache_refreshes_expired_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(cache_dir=Path(tmp), timeout=1, env={}, cache_ttl_default=0)
            client = HttpClient(settings)
            url = "https://example.test/match"

            with patch("urllib.request.urlopen", side_effect=[fake_response({"value": 1})(), fake_response({"value": 2})()]):
                self.assertEqual(client.get_json(url), ({"value": 1}, False))
                time.sleep(0.01)
                self.assertEqual(client.get_json(url), ({"value": 2}, False))

    def test_http_cache_ignores_corrupt_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = Settings(cache_dir=Path(tmp), timeout=1, env={}, cache_ttl_default=60)
            client = HttpClient(settings)
            url = "https://example.test/match"
            cache_key = hashlib.sha256((url + json.dumps({}, sort_keys=True)).encode()).hexdigest()
            (Path(tmp) / f"{cache_key}.json").write_text("{not-json")

            with patch("urllib.request.urlopen", return_value=fake_response({"value": 3})()):
                self.assertEqual(client.get_json(url), ({"value": 3}, False))

    def test_api_football_cache_ttl_follows_fixture_state(self):
        settings = Settings(
            cache_dir=Path("/tmp/world-cup-digest-test"),
            timeout=1,
            env={},
            cache_ttl_live=20,
            cache_ttl_scheduled=300,
            cache_ttl_final=86400,
        )
        provider = ApiFootballProvider(settings, HttpClient(settings))

        live = {"fixture": {"status": {"short": "2H", "long": "Second Half"}}}
        final = {"fixture": {"status": {"short": "FT", "long": "Match Finished"}}}

        self.assertEqual(fixture_state(live), "live")
        self.assertEqual(provider.cache_ttl_for_fixture(live), 20)
        self.assertEqual(fixture_state(final), "final")
        self.assertEqual(provider.cache_ttl_for_fixture(final), 86400)


def fake_response(payload):
    class Response:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def read(self, _size=-1):
            return json.dumps(payload).encode()

    return Response


if __name__ == "__main__":
    unittest.main()
