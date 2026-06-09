from __future__ import annotations

import json
from typing import Any

from .models import DigestBundle, Match, ProviderResult, TeamStats, to_jsonable


def render_json(bundle: DigestBundle) -> str:
    return json.dumps(to_jsonable(bundle), ensure_ascii=False, indent=2) + "\n"


def render_compact(bundle: DigestBundle) -> str:
    lines = [f"world-cup-digest bundle · {bundle.generated_at}", ""]
    for warning in bundle.warnings:
        lines.append(f"WARNING: {warning}")
    matches = bundle.matches()
    if not matches:
        lines.append("No normalized matches found. Use provider raw payloads and web fallback.")
    for match in matches:
        lines.append(f"- {match.label}: {match.score_text} · {match.status or 'unknown'} · {match.stage or 'stage unknown'}")
    return "\n".join(lines).rstrip() + "\n"


def render_markdown(bundle: DigestBundle) -> str:
    lines = [
        "# World Cup research bundle",
        "",
        f"- Generated: {bundle.generated_at}",
        f"- Season: {bundle.query.season}",
        f"- Date filter: {bundle.query.date or 'none'}",
        f"- Range filter: {format_range(bundle.query.start_date, bundle.query.end_date)}",
        f"- Live filter: {'yes' if bundle.query.live else 'no'}",
        f"- Team filter: {bundle.query.team or 'none'}",
        f"- Match filter: {bundle.query.match or bundle.query.match_id or 'none'}",
        f"- Providers: {', '.join(bundle.query.providers) or 'none'}",
        "",
    ]
    if bundle.warnings:
        lines.extend(["## Data quality warnings", ""])
        lines.extend(f"- {warning}" for warning in bundle.warnings)
        lines.append("")

    lines.extend(["## Normalized matches", ""])
    matches = bundle.matches()
    if not matches:
        lines.append("No normalized matches found. Browse official FIFA pages and match reports before synthesis.")
    else:
        for match in matches:
            lines.extend(render_match(match))

    lines.extend(["", "## Provider results"])
    for result in bundle.results:
        lines.extend(render_provider_result(result))

    lines.extend([
        "",
        "## Next verification steps",
        "",
        "- Verify official score/fixture identity with FIFA.",
        "- Search for at least one reputable match report.",
        "- Search for lineups/player ratings if the provider payload does not include them.",
        "- Do not synthesize unverified stats.",
    ])
    return "\n".join(lines).rstrip() + "\n"


def format_range(start: str, end: str) -> str:
    if not start and not end:
        return "none"
    return f"{start or '?'} to {end or '?'}"


def render_match(match: Match) -> list[str]:
    lines = [
        f"### {match.home.name} {match.score_text} {match.away.name}",
        "",
        f"- Match id: `{match.id or 'unknown'}`",
        f"- Kickoff: {match.kickoff or 'unknown'}",
        f"- Status: {match.status or 'unknown'}",
        f"- Stage: {match.stage or 'unknown'}",
        f"- Venue: {match.venue or 'unknown'}",
        f"- Source: {match.source_provider or 'unknown'} {match.source_url or ''}".rstrip(),
    ]
    if match.events:
        lines.extend(["", "Events:"])
        for event in match.events:
            actor = f" - {event.player}" if event.player else ""
            detail = f" ({event.detail})" if event.detail else ""
            lines.append(f"- {event.minute}' {event.type} · {event.team}{actor}{detail}")
    if match.stats:
        lines.extend(["", "Stats:"])
        for side, stats in match.stats.items():
            stat_text = stats_to_text(stats)
            if stat_text:
                lines.append(f"- {side}: {stat_text}")
    return lines + [""]


def stats_to_text(stats: TeamStats) -> str:
    parts: list[str] = []
    if stats.possession is not None:
        parts.append(f"possession {stats.possession}%")
    if stats.shots is not None:
        parts.append(f"shots {stats.shots}")
    if stats.shots_on_target is not None:
        parts.append(f"on target {stats.shots_on_target}")
    if stats.xg is not None:
        parts.append(f"xG {stats.xg}")
    if stats.corners is not None:
        parts.append(f"corners {stats.corners}")
    return ", ".join(parts)


def render_provider_result(result: ProviderResult) -> list[str]:
    lines = [
        "",
        f"### {result.provider}",
        "",
        f"- URL: `{result.url}`",
        f"- OK: {result.ok}",
        f"- Cached: {result.cached}",
        f"- Source only: {result.source_only}",
    ]
    if result.error:
        lines.append(f"- Error: `{result.error}`")
    elif result.data is not None:
        lines.extend(["", "```json", summarize_payload(result.data), "```"])
    return lines


def summarize_payload(payload: Any, max_chars: int = 1600) -> str:
    text = json.dumps(payload, ensure_ascii=False)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "... [truncated]"
