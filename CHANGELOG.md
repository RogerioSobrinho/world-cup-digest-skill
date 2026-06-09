# Changelog

All notable changes to `world-cup-digest-skill` are documented here.

This project uses semantic versioning where practical.

## 0.5.1 - Catch-Up and Team Radar

### Added

- Catch-up briefing guidance for users who want to get current quickly.
- Team radar guidance for any national team, not only Brazil.
- Watch-priority format covering full replay, extended highlights, short highlights, and score-only matches.
- Daily digest guidance for biggest outcomes, surprises, standouts, injuries/suspensions, controversies, and tournament impact.

## 0.5.0 - First Public Release

### Added

- Public/free source mode as the default path:
  - `fifa-public`
  - `mediawiki`
  - `youtube-public`
- Optional paid/stat provider support:
  - API-Football/API-Sports
  - BALLDONTLIE FIFA
  - TheStatsAPI
  - WC2026 API
  - WorldCupAPI
- Bundled Python research engine at `skills/world-cup-digest/scripts/world-cup-fetch.py`.
- CLI support for:
  - `--today`
  - `--date`
  - `--range`
  - `--season`
  - `--live`
  - `--team`
  - `--match`
  - `--match-id`
  - `--provider`
  - `--free`
  - `--mock`
  - `--diagnose`
  - `--save-dir`
  - `--emit markdown|json|compact`
- Deterministic mock fixtures, including Brazil 2 x 0 Serbia from the 2022 World Cup.
- Cache policy with different TTLs for live, scheduled, final, and generic responses.
- Dotenv loading with masked diagnostics.
- CI workflow that runs tests, builds the `.skill` archive, and smoke-tests the extracted artifact.
- Release workflow that uploads `dist/world-cup-digest.skill` on version tags.

### Hardened

- `.env` and local secret files are ignored by git.
- API keys are only shown masked in diagnostics.
- Corrupt cache files are ignored and refreshed.
- Invalid timeout/TTL env values fall back to bounded defaults.
- HTTP responses have a size limit and explicit JSON/UTF-8 validation errors.
- `.skill` build excludes `__pycache__`, `.pyc`, and local noise.

### Documented

- Free/public mode versus optional paid providers.
- API-Football Free-plan limitations observed during testing.
- Cache behavior for live matches.
- Release process and local/manual install paths.

### Known Limits

- Free/public mode does not provide guaranteed live structured statistics, xG, player ratings, or shot maps.
- API-Football Free-plan access is limited and rejected World Cup 2014 during testing.
- Agents must still verify current match facts with official/current sources before final synthesis.
