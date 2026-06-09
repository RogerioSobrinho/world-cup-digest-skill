from .api_football import ApiFootballProvider
from .base import Provider
from .generic import BalldontlieProvider, TheStatsApiProvider, Wc2026Provider, WorldCupApiProvider
from .mock import MockProvider
from .public import FifaPublicProvider, MediaWikiProvider, YouTubePublicProvider

PROVIDERS = {
    "fifa-public": FifaPublicProvider,
    "mediawiki": MediaWikiProvider,
    "youtube-public": YouTubePublicProvider,
    "api-football": ApiFootballProvider,
    "balldontlie": BalldontlieProvider,
    "thestatsapi": TheStatsApiProvider,
    "wc2026": Wc2026Provider,
    "worldcupapi": WorldCupApiProvider,
    "mock": MockProvider,
}

__all__ = ["PROVIDERS", "Provider"]
