from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Query:
    season: str = "2026"
    date: str = ""
    start_date: str = ""
    end_date: str = ""
    live: bool = False
    team: str = ""
    match: str = ""
    match_id: str = ""
    providers: list[str] = field(default_factory=list)
    mock: bool = False


@dataclass
class Source:
    provider: str
    url: str
    ok: bool
    error: str = ""


@dataclass
class TeamRef:
    name: str
    id: str = ""


@dataclass
class MatchEvent:
    minute: str
    type: str
    team: str = ""
    player: str = ""
    detail: str = ""


@dataclass
class TeamStats:
    possession: float | None = None
    shots: int | None = None
    shots_on_target: int | None = None
    xg: float | None = None
    corners: int | None = None


@dataclass
class Match:
    id: str
    home: TeamRef
    away: TeamRef
    kickoff: str = ""
    status: str = ""
    stage: str = ""
    venue: str = ""
    score_home: int | None = None
    score_away: int | None = None
    events: list[MatchEvent] = field(default_factory=list)
    stats: dict[str, TeamStats] = field(default_factory=dict)
    source_provider: str = ""
    source_url: str = ""

    @property
    def label(self) -> str:
        return f"{self.home.name} vs {self.away.name}"

    @property
    def score_text(self) -> str:
        if self.score_home is None or self.score_away is None:
            return "TBD"
        return f"{self.score_home} x {self.score_away}"


@dataclass
class ProviderResult:
    provider: str
    url: str
    ok: bool
    data: Any = None
    matches: list[Match] = field(default_factory=list)
    error: str = ""
    cached: bool = False
    source_only: bool = False


@dataclass
class DigestBundle:
    generated_at: str
    query: Query
    results: list[ProviderResult]
    warnings: list[str] = field(default_factory=list)

    @classmethod
    def create(cls, query: Query, results: list[ProviderResult], warnings: list[str] | None = None) -> "DigestBundle":
        return cls(
            generated_at=datetime.now(timezone.utc).isoformat(),
            query=query,
            results=results,
            warnings=warnings or [],
        )

    def matches(self) -> list[Match]:
        seen: set[str] = set()
        matches: list[Match] = []
        for result in self.results:
            for match in result.matches:
                key = match.id or f"{match.home.name}|{match.away.name}|{match.kickoff}"
                if key in seen:
                    continue
                seen.add(key)
                matches.append(match)
        return matches


def to_jsonable(value: Any) -> Any:
    if hasattr(value, "__dataclass_fields__"):
        return {k: to_jsonable(v) for k, v in asdict(value).items()}
    if isinstance(value, list):
        return [to_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {k: to_jsonable(v) for k, v in value.items()}
    return value
