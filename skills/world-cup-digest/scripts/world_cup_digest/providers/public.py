from __future__ import annotations

import urllib.parse

from .. import __version__
from ..models import ProviderResult, Query
from .base import Provider


def query_text(query: Query) -> str:
    parts = [f"FIFA World Cup {query.season or '2026'}"]
    if query.match:
        parts.append(query.match)
    if query.team:
        parts.append(query.team)
    if query.date:
        parts.append(query.date)
    if query.live:
        parts.append("live")
    if not any((query.match, query.team, query.date, query.live)):
        parts.append("today matches")
    return " ".join(parts)


def search_url(base: str, term: str) -> str:
    return base + urllib.parse.quote_plus(term)


def source_result(provider: str, url: str, data: dict[str, object]) -> ProviderResult:
    return ProviderResult(provider=provider, url=url, ok=True, data=data, source_only=True)


class FifaPublicProvider(Provider):
    name = "fifa-public"
    source_only = True

    def build_request(self, query: Query) -> tuple[str, dict[str, str]]:
        term = query_text(query)
        return search_url("https://www.fifa.com/en/search?q=", term), {}

    def fetch(self, query: Query) -> ProviderResult:
        url, _headers = self.build_request(query)
        data = {
            "kind": "public_source_guide",
            "official_schedule": "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026",
            "official_search": url,
            "query": query_text(query),
            "use_for": [
                "fixture identity",
                "kickoff time",
                "venue",
                "official score when available",
                "group or knockout context",
            ],
            "limits": [
                "Do not assume structured live stats are available.",
                "Verify exact match pages with web search before final synthesis.",
            ],
        }
        return source_result(self.name, url, data)


class YouTubePublicProvider(Provider):
    name = "youtube-public"
    source_only = True

    def build_request(self, query: Query) -> tuple[str, dict[str, str]]:
        term = "CazéTV " + query_text(query)
        return search_url("https://www.youtube.com/results?search_query=", term), {}

    def fetch(self, query: Query) -> ProviderResult:
        url, _headers = self.build_request(query)
        data = {
            "kind": "public_source_guide",
            "search": url,
            "channel_hint": "CazéTV",
            "use_for": [
                "free Brazil broadcast availability",
                "live stream or replay discovery",
                "official highlights when published",
            ],
            "limits": [
                "Do not download or transcribe full broadcasts.",
                "Use metadata, official descriptions, and available highlights only.",
            ],
        }
        return source_result(self.name, url, data)


class MediaWikiProvider(Provider):
    name = "mediawiki"
    source_only = True

    def build_request(self, query: Query) -> tuple[str, dict[str, str]]:
        term = query_text(query)
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srlimit": "5",
            "srsearch": term,
        }
        headers = {"User-Agent": f"world-cup-digest-skill/{__version__} (+https://github.com/RogerioSobrinho/world-cup-digest-skill)"}
        return "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(params), headers

    def fetch(self, query: Query) -> ProviderResult:
        url, headers = self.build_request(query)
        data, cached = self.http.get_json(url, headers, ttl_seconds=self.settings.cache_ttl_scheduled)
        return ProviderResult(provider=self.name, url=url, ok=True, data=data, cached=cached, source_only=True)
