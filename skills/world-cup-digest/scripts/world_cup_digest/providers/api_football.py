from __future__ import annotations

from typing import Any

from ..models import Match, MatchEvent, ProviderResult, Query, TeamRef, TeamStats
from .base import Provider


LIVE_STATUS_CODES = {"1H", "HT", "2H", "ET", "BT", "P", "SUSP", "INT"}
FINAL_STATUS_CODES = {"FT", "AET", "PEN"}
SCHEDULED_STATUS_CODES = {"TBD", "NS"}


class ApiFootballProvider(Provider):
    name = "api-football"

    def build_request(self, query: Query) -> tuple[str, dict[str, str]]:
        params = {
            "league": "1",
            "season": query.season or "2026",
            "date": query.date,
            "from": query.start_date,
            "to": query.end_date,
            "team": query.team,
            "id": query.match_id,
            "live": "all" if query.live else "",
        }
        key = self.settings.env_value("API_FOOTBALL_KEY")
        headers = {"x-apisports-key": key} if key else {}
        return self.url("/fixtures", params), headers

    def fetch(self, query: Query) -> ProviderResult:
        url, headers = self.build_request(query)
        data, cached = self.http.get_json(url, headers, ttl_seconds=self.cache_ttl_for_payload)
        error = format_api_errors(data.get("errors") if isinstance(data, dict) else None)
        if error:
            return ProviderResult(provider=self.name, url=url, ok=False, data=data, error=error, cached=cached)
        detail_cached = cached
        response = data.get("response") if isinstance(data, dict) else None
        should_hydrate = isinstance(response, list) and (query.match_id or query.match or len(response) <= 6)
        if should_hydrate:
            for item in response:
                fixture_id = str(((item.get("fixture") or {}).get("id")) or "")
                if not fixture_id:
                    continue
                details = {}
                for key, path in {
                    "events": "/fixtures/events",
                    "statistics": "/fixtures/statistics",
                    "lineups": "/fixtures/lineups",
                    "players": "/fixtures/players",
                }.items():
                    detail_url = self.url(path, {"fixture": fixture_id})
                    try:
                        detail_data, was_cached = self.http.get_json(
                            detail_url,
                            headers,
                            ttl_seconds=self.cache_ttl_for_fixture(item),
                        )
                        detail_cached = detail_cached and was_cached
                        details[key] = detail_data
                    except Exception as exc:
                        details[key] = {"error": str(exc), "url": detail_url}
                item["_world_cup_digest_details"] = details
                for key in ("events", "statistics", "lineups", "players"):
                    payload = details.get(key)
                    if isinstance(payload, dict) and isinstance(payload.get("response"), list):
                        item[key] = payload["response"]
        return ProviderResult(
            provider=self.name,
            url=url,
            ok=True,
            data=data,
            matches=self.normalize(data, url),
            cached=detail_cached,
        )

    def cache_ttl_for_fixture(self, fixture_payload: dict[str, Any]) -> int:
        state = fixture_state(fixture_payload)
        if state == "live":
            return self.settings.cache_ttl_live
        if state == "final":
            return self.settings.cache_ttl_final
        if state == "scheduled":
            return self.settings.cache_ttl_scheduled
        return self.settings.cache_ttl_default

    def cache_ttl_for_payload(self, payload: Any) -> int:
        response = payload.get("response") if isinstance(payload, dict) else None
        if not isinstance(response, list) or not response:
            return self.settings.cache_ttl_default
        states = {fixture_state(item) for item in response}
        if "live" in states:
            return self.settings.cache_ttl_live
        if states == {"final"}:
            return self.settings.cache_ttl_final
        if states == {"scheduled"}:
            return self.settings.cache_ttl_scheduled
        return self.settings.cache_ttl_default

    def normalize(self, data: Any, url: str) -> list[Match]:
        response = data.get("response") if isinstance(data, dict) else None
        if not isinstance(response, list):
            return []
        matches = []
        for item in response:
            fixture = item.get("fixture") or {}
            teams = item.get("teams") or {}
            goals = item.get("goals") or {}
            league = item.get("league") or {}
            match = Match(
                id=str(fixture.get("id") or ""),
                home=TeamRef(name=(teams.get("home") or {}).get("name") or "Home", id=str((teams.get("home") or {}).get("id") or "")),
                away=TeamRef(name=(teams.get("away") or {}).get("name") or "Away", id=str((teams.get("away") or {}).get("id") or "")),
                kickoff=fixture.get("date") or "",
                status=(fixture.get("status") or {}).get("long") or "",
                stage=league.get("round") or "",
                venue=(fixture.get("venue") or {}).get("name") or "",
                score_home=goals.get("home"),
                score_away=goals.get("away"),
                events=normalize_events(item.get("events") or []),
                stats=normalize_stats(item.get("statistics") or []),
                source_provider=self.name,
                source_url=url,
            )
            matches.append(match)
        return matches


def normalize_events(events: list[dict[str, Any]]) -> list[MatchEvent]:
    normalized = []
    for event in events:
        time = event.get("time") or {}
        minute = str(time.get("elapsed") or "")
        extra = time.get("extra")
        if extra:
            minute = f"{minute}+{extra}"
        player = event.get("player") or {}
        team = event.get("team") or {}
        normalized.append(MatchEvent(
            minute=minute,
            type=event.get("type") or "",
            team=team.get("name") or "",
            player=player.get("name") or "",
            detail=event.get("detail") or "",
        ))
    return normalized


def normalize_stats(statistics: list[dict[str, Any]]) -> dict[str, TeamStats]:
    result: dict[str, TeamStats] = {}
    for team_stats in statistics:
        team = (team_stats.get("team") or {}).get("name") or ""
        values = {entry.get("type"): entry.get("value") for entry in team_stats.get("statistics") or []}
        if not team:
            continue
        result[team] = TeamStats(
            possession=parse_percent(values.get("Ball Possession")),
            shots=parse_int(values.get("Total Shots")),
            shots_on_target=parse_int(values.get("Shots on Goal")),
            corners=parse_int(values.get("Corner Kicks")),
        )
    return result


def fixture_state(item: dict[str, Any]) -> str:
    status = ((item.get("fixture") or {}).get("status") or {})
    short = str(status.get("short") or "").upper()
    long = str(status.get("long") or "").lower()
    if short in LIVE_STATUS_CODES or any(term in long for term in ("progress", "halftime", "live")):
        return "live"
    if short in FINAL_STATUS_CODES or "finished" in long:
        return "final"
    if short in SCHEDULED_STATUS_CODES or any(term in long for term in ("not started", "notstarted", "scheduled")):
        return "scheduled"
    return "unknown"


def format_api_errors(errors: Any) -> str:
    if not errors:
        return ""
    if isinstance(errors, dict):
        return "; ".join(f"{key}: {value}" for key, value in errors.items())
    if isinstance(errors, list):
        return "; ".join(str(error) for error in errors if error)
    return str(errors)


def parse_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(str(value).replace("%", "").strip())
    except ValueError:
        return None


def parse_percent(value: Any) -> float | None:
    parsed = parse_int(value)
    return float(parsed) if parsed is not None else None
