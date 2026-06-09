from __future__ import annotations

from ..models import Query
from .base import Provider


class Wc2026Provider(Provider):
    name = "wc2026"

    def build_request(self, query: Query) -> tuple[str, dict[str, str]]:
        key = self.settings.env_value("WC2026_API_KEY")
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        return self.url("/matches", {"date": query.date, "team": query.team, "match_id": query.match_id, "live": "true" if query.live else ""}), headers


class TheStatsApiProvider(Provider):
    name = "thestatsapi"

    def build_request(self, query: Query) -> tuple[str, dict[str, str]]:
        key = self.settings.env_value("THESTATSAPI_KEY")
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        return self.url("/football/matches", {
            "competition": "world-cup",
            "season": "2026",
            "date": query.date,
            "from": query.start_date,
            "to": query.end_date,
            "team": query.team,
            "match_id": query.match_id,
            "live": "true" if query.live else "",
        }), headers


class BalldontlieProvider(Provider):
    name = "balldontlie"

    def build_request(self, query: Query) -> tuple[str, dict[str, str]]:
        key = self.settings.env_value("BALLDONTLIE_FIFA_KEY") or self.settings.env_value("BALLDONTLIE_API_KEY")
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        return self.url("/matches", {"tournament": "2026", "date": query.date, "team": query.team, "match_id": query.match_id, "live": "true" if query.live else ""}), headers


class WorldCupApiProvider(Provider):
    name = "worldcupapi"

    def build_request(self, query: Query) -> tuple[str, dict[str, str]]:
        key = self.settings.env_value("WORLDCUPAPI_KEY")
        headers = {"Authorization": f"Bearer {key}"} if key else {}
        return self.url("/matches", {"date": query.date, "team": query.team, "match_id": query.match_id, "live": "true" if query.live else ""}), headers
