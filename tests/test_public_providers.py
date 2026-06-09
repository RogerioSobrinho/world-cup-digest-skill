import unittest
from pathlib import Path
from unittest.mock import patch

from world_cup_digest.config import Settings
from world_cup_digest.http import HttpClient
from world_cup_digest.models import ProviderResult, Query
from world_cup_digest.pipeline import PUBLIC_PROVIDERS, run_pipeline
from world_cup_digest.providers.public import FifaPublicProvider, MediaWikiProvider, YouTubePublicProvider


class PublicProviderTests(unittest.TestCase):
    def test_public_provider_urls_are_source_guides(self):
        settings = Settings(cache_dir=Path("/tmp/world-cup-digest-test"), timeout=1, env={})
        http = HttpClient(settings)
        query = Query(match="Brazil vs Germany", live=True)

        fifa = FifaPublicProvider(settings, http).fetch(query)
        youtube = YouTubePublicProvider(settings, http).fetch(query)

        self.assertTrue(fifa.source_only)
        self.assertIn("fifa.com", fifa.url)
        self.assertIn("Brazil+vs+Germany", fifa.url)
        self.assertTrue(youtube.source_only)
        self.assertIn("youtube.com", youtube.url)
        self.assertIn("Caz%C3%A9TV", youtube.url)

    def test_mediawiki_request_uses_user_agent(self):
        settings = Settings(cache_dir=Path("/tmp/world-cup-digest-test"), timeout=1, env={})
        provider = MediaWikiProvider(settings, HttpClient(settings))

        _url, headers = provider.build_request(Query(match="Brazil vs Germany"))

        self.assertIn("User-Agent", headers)
        self.assertIn("world-cup-digest-skill", headers["User-Agent"])

    def test_public_pipeline_does_not_warn_like_failed_structured_provider(self):
        settings = Settings(cache_dir=Path("/tmp/world-cup-digest-test"), timeout=1, env={}, no_cache=True)
        query = Query(providers=PUBLIC_PROVIDERS)

        with patch("world_cup_digest.providers.public.MediaWikiProvider.fetch") as mediawiki_fetch:
            mediawiki_fetch.return_value = ProviderResult(
                provider="mediawiki",
                url="https://en.wikipedia.org/w/api.php",
                ok=True,
                data={"query": {"search": []}},
                source_only=True,
            )

            bundle = run_pipeline(query, settings)

        self.assertIn("Only public source guides are available", " ".join(bundle.warnings))
        self.assertNotIn("mediawiki returned no normalized matches", " ".join(bundle.warnings))

    def test_pipeline_defaults_to_public_providers(self):
        settings = Settings(cache_dir=Path("/tmp/world-cup-digest-test"), timeout=1, env={}, no_cache=True)

        with patch("world_cup_digest.providers.public.MediaWikiProvider.fetch") as mediawiki_fetch:
            mediawiki_fetch.return_value = ProviderResult(
                provider="mediawiki",
                url="https://en.wikipedia.org/w/api.php",
                ok=True,
                data={"query": {"search": []}},
                source_only=True,
            )
            bundle = run_pipeline(Query(), settings)

        self.assertEqual(bundle.query.providers, PUBLIC_PROVIDERS)


if __name__ == "__main__":
    unittest.main()
