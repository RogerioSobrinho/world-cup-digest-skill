# Concepts

`world-cup-digest-skill` helps an AI agent follow the FIFA World Cup when the user cannot watch every match.

It is not a betting tool and it is not a replacement for a professional paid live-stat feed.

## Two-Layer Model

The project works in two layers:

1. The bundled Python engine gathers a research bundle.
2. The hosting AI agent verifies sources and writes the final recap.

This separation is intentional. The engine should be deterministic and cautious; the agent should synthesize, cite, and explain.

## Research Bundle

The fetcher returns a bundle containing:

- query metadata
- provider results
- normalized matches when available
- source-only guidance when structured data is not available
- data quality warnings

The bundle is evidence for the final answer, not the final answer itself.

## Free/Public Mode

Free/public mode is the default.

It uses:

- `fifa-public` for official FIFA schedule/search guidance
- `mediawiki` for public tournament and post-match context
- `youtube-public` for CazéTV/YouTube stream, replay, and highlight discovery

This mode is designed for personal tournament following without paying for a sports-data API.

Good fit:

- daily recaps
- weekly digests
- match previews
- post-match summaries
- "what should I watch?" recommendations

Not a good fit:

- guaranteed live xG
- player ratings
- shot maps
- complete live event feeds
- minute-by-minute structured dashboards

## Optional Stat Providers

Paid/stat providers can enrich the bundle with structured data:

- fixtures
- goals/events
- lineups
- cards
- team statistics
- player statistics

Provider access, coverage, and pricing vary. The engine treats them as optional and best-effort.

## Source-Only Providers

Some providers intentionally return `source_only=True`.

That means they provide links, guidance, or search targets, but do not claim normalized match facts.

Agents must browse and verify those sources before stating scores, events, or statistics.

## Normalized Matches

When a provider gives structured data, the engine can normalize it into:

- match identity
- teams
- score
- kickoff
- status
- stage
- venue
- events
- team stats

Only normalized fields should be treated as structured provider evidence.

## Cache Policy

Cache TTL depends on match state:

- live: short TTL
- scheduled: medium TTL
- final: long TTL
- unknown/generic: default TTL

This avoids stale live-match updates while still reducing repeated network calls for finished games.

## Data Quality Rules

The skill should always be honest about evidence.

- Official score and fixture identity should come from FIFA or another current authoritative source.
- Reports and analysis can explain how the match unfolded.
- Stats should only be used when the source actually provides them.
- xG, player ratings, and tactical claims should never be invented.
- Conflicting sources should be called out rather than silently merged.

## Scraping Boundary

The project may use public pages and public APIs as source discovery.

It should not:

- bypass anti-bot systems
- bypass login walls
- use private app endpoints
- evade Cloudflare or similar protections
- download or transcribe full broadcasts
- poll aggressively

The goal is a robust, respectful personal research assistant, not an unofficial data-extraction service.
