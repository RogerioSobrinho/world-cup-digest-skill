from __future__ import annotations

import urllib.parse
from abc import ABC, abstractmethod
from typing import Any

from ..config import Settings
from ..http import HttpClient
from ..models import Match, ProviderResult, Query


class Provider(ABC):
    name = "provider"

    def __init__(self, settings: Settings, http: HttpClient):
        self.settings = settings
        self.http = http

    @abstractmethod
    def build_request(self, query: Query) -> tuple[str, dict[str, str]]:
        raise NotImplementedError

    def fetch(self, query: Query) -> ProviderResult:
        url, headers = self.build_request(query)
        data, cached = self.http.get_json(url, headers, ttl_seconds=self.settings.cache_ttl_default)
        return ProviderResult(
            provider=self.name,
            url=url,
            ok=True,
            data=data,
            matches=self.normalize(data, url),
            cached=cached,
        )

    def normalize(self, data: Any, url: str) -> list[Match]:
        return []

    def url(self, path: str, params: dict[str, str | None]) -> str:
        clean = {k: v for k, v in params.items() if v not in (None, "")}
        base = self.settings.base_url(self.name)
        return base.rstrip("/") + path + ("?" + urllib.parse.urlencode(clean) if clean else "")
