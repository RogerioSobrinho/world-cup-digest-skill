from __future__ import annotations

import json
import platform
import sys

from . import __version__
from .config import DEFAULT_BASES, Settings, mask


PROVIDER_KEYS = {
    "fifa-public": [],
    "mediawiki": [],
    "youtube-public": [],
    "api-football": ["API_FOOTBALL_KEY"],
    "balldontlie": ["BALLDONTLIE_FIFA_KEY", "BALLDONTLIE_API_KEY"],
    "thestatsapi": ["THESTATSAPI_KEY"],
    "wc2026": ["WC2026_API_KEY"],
    "worldcupapi": ["WORLDCUPAPI_KEY"],
}


def diagnose(settings: Settings) -> dict[str, object]:
    providers = {}
    for provider, keys in PROVIDER_KEYS.items():
        base_url = "public-source-guide"
        if provider in DEFAULT_BASES:
            base_url = settings.env_value(provider.upper().replace("-", "_") + "_BASE", DEFAULT_BASES[provider])
        providers[provider] = {
            "base_url": base_url,
            "keys": {key: mask(settings.env_value(key)) for key in keys},
        }
    return {
        "world_cup_digest_version": __version__,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "env_file": str(settings.env_file) if settings.env_file else None,
        "cache_dir": str(settings.cache_dir),
        "timeout": settings.timeout,
        "cache_ttl": {
            "default": settings.cache_ttl_default,
            "live": settings.cache_ttl_live,
            "scheduled": settings.cache_ttl_scheduled,
            "final": settings.cache_ttl_final,
        },
        "providers": providers,
    }


def render_diagnose(settings: Settings) -> str:
    return json.dumps(diagnose(settings), indent=2, ensure_ascii=False) + "\n"
