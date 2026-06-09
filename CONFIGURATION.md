# Configuration

`world-cup-digest` works in two layers:

1. The bundled Python engine gathers a research bundle.
2. The hosting agent verifies current sources and synthesizes the final recap.

The engine is intentionally best-effort. Providers differ in API shape, auth, coverage, and rate limits.

## Environment

Copy the sample file:

```bash
cp .env.example .env
```

Set any optional paid/stat provider keys you have:

```bash
API_FOOTBALL_KEY=
BALLDONTLIE_FIFA_KEY=
THESTATSAPI_KEY=
WC2026_API_KEY=
WORLDCUPAPI_KEY=
```

The CLI loads `.env` automatically from the current working directory or the repository root when present. If the agent/harness runs from another directory, pass it explicitly:

```bash
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --env-file /path/to/.env --diagnose
```

Runtime options:

```bash
WORLD_CUP_DIGEST_CACHE_DIR=~/.cache/world-cup-digest
WORLD_CUP_DIGEST_TIMEOUT=20
WORLD_CUP_DIGEST_CACHE_TTL_DEFAULT=300
WORLD_CUP_DIGEST_CACHE_TTL_LIVE=20
WORLD_CUP_DIGEST_CACHE_TTL_SCHEDULED=300
WORLD_CUP_DIGEST_CACHE_TTL_FINAL=86400
```

## Provider Priority

Default free/public order:

1. `fifa-public`
2. `mediawiki`
3. `youtube-public`

Optional paid/stat providers:

1. `api-football`
2. `balldontlie`
3. `thestatsapi`
4. `wc2026`
5. `worldcupapi`

Use public/free providers only:

```bash
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --free --today
```

Force one provider:

```bash
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --provider api-football --today
```

Fetch live/in-progress matches when supported by the provider:

```bash
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --live --provider api-football --emit compact
```

Test historical data when a provider supports it:

```bash
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --provider api-football --season 2022 --date 2022-11-24 --emit compact
```

Observed API-Football Free-plan limitation:

- `season 2014` is rejected by the API with a plan error.
- historical date filters may also be rejected depending on the current free-plan window.
- use `--mock --season 2022 --match "Brazil vs Serbia"` for deterministic local tests.
- use `--free` for public-source testing without paid API access.

Use offline fixture mode:

```bash
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --mock --emit markdown
```

## Diagnostics

```bash
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --diagnose
```

This prints Python version, cache path, timeout, provider base URLs, and masked key status.

## Cache

HTTP GET responses are cached by URL+headers in:

```text
~/.cache/world-cup-digest
```

Cache TTLs are intentionally different by match state:

- live/in-progress match: `WORLD_CUP_DIGEST_CACHE_TTL_LIVE`, default `20` seconds
- scheduled match: `WORLD_CUP_DIGEST_CACHE_TTL_SCHEDULED`, default `300` seconds
- final match: `WORLD_CUP_DIGEST_CACHE_TTL_FINAL`, default `86400` seconds
- generic/unknown provider response: `WORLD_CUP_DIGEST_CACHE_TTL_DEFAULT`, default `300` seconds

For API-Football, the engine reads the fixture status from the cached payload. If the cached match is still live and the live TTL has expired, the next request fetches fresh events/stats instead of reusing the old cache.

Disable cache:

```bash
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --today --no-cache
```

## Output Modes

```bash
--emit markdown
--emit json
--emit compact
```

Use `--save-dir DIR` to save the raw normalized bundle as `world-cup-bundle.json`.

## Troubleshooting

- If public providers return only source guides, the agent must browse/verify the linked sources before final synthesis.
- If all providers fail, the skill should still browse FIFA and reputable match reports.
- If no normalized matches are present, inspect provider raw payloads in the bundle.
- If a stat is missing from the bundle and web sources do not verify it, omit it from the final recap.
- If sources disagree, trust official FIFA score/events first and label non-official stats as provider-specific.
