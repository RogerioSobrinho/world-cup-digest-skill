from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..models import ProviderResult, Query
from .api_football import ApiFootballProvider


class MockProvider(ApiFootballProvider):
    name = "mock"

    def fetch(self, query: Query) -> ProviderResult:
        fixture = fixture_path(query)
        data: Any = json.loads(fixture.read_text())
        return ProviderResult(
            provider=self.name,
            url=str(fixture),
            ok=True,
            data=data,
            matches=self.normalize(data, str(fixture)),
            cached=False,
        )

    def build_request(self, query: Query) -> tuple[str, dict[str, str]]:
        return "mock://fixture", {}


def fixture_path(query: Query) -> Path:
    filename = "api_football_fixture_sample.json"
    match_text = " ".join([query.match, query.team]).lower()
    if query.season == "2022" or ("brazil" in match_text and "serbia" in match_text):
        filename = "api_football_brazil_serbia_2022.json"
    fixture = Path(__file__).resolve().parents[3] / "fixtures" / filename
    if not fixture.exists():
        fixture = Path.cwd() / "tests" / "fixtures" / filename
        if not fixture.exists():
            raise FileNotFoundError(f"mock fixture not found: {filename}")
    return fixture
