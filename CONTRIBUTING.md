# Contributing

Thanks for improving `world-cup-digest-skill`.

The project should stay reliable, honest about data quality, and useful without requiring paid APIs.

## Development Setup

Use Python 3.11+.

Run the test suite:

```bash
PYTHONPATH=skills/world-cup-digest/scripts python3 -m unittest discover -s tests -v
```

Build the skill archive:

```bash
bash skills/world-cup-digest/scripts/build-skill.sh
```

Smoke-test the archive:

```bash
tmp="$(mktemp -d)"
unzip -q dist/world-cup-digest.skill -d "$tmp/world-cup-digest"
python3 "$tmp/world-cup-digest/scripts/world-cup-fetch.py" --mock --season 2022 --match "Brazil vs Serbia" --emit compact
```

## Design Principles

- Keep free/public mode useful by default.
- Treat paid/stat APIs as optional enhancements, not hard dependencies.
- Do not invent statistics. If a source does not verify a number, omit it or mark it as unavailable.
- Prefer official FIFA identity/score data, then reputable reports, then optional stats providers.
- Keep engine output as a research bundle. The hosting agent still verifies and synthesizes the final answer.
- Avoid scraping that bypasses login, anti-bot systems, private endpoints, app-only APIs, or video access controls.

## Adding Providers

Provider code lives in:

```text
skills/world-cup-digest/scripts/world_cup_digest/providers/
```

When adding a provider:

- implement a small provider class
- add it to `providers/__init__.py`
- return `ProviderResult`
- set `source_only=True` if the provider only supplies links/guidance, not normalized match objects
- normalize into `Match` only when the provider payload is structured and tested
- add unit tests
- document required env vars in `.env.example` and `CONFIGURATION.md`

## Security

Never commit real API keys or tokens.

Local secrets belong in `.env`, which is ignored by git:

```bash
cp .env.example .env
```

Diagnostics must mask secrets. Do not print raw provider headers, raw env files, or full API keys.

## Testing Expectations

New behavior should include focused tests under `tests/`.

At minimum, run:

```bash
PYTHONPATH=skills/world-cup-digest/scripts python3 -m unittest discover -s tests -v
bash skills/world-cup-digest/scripts/build-skill.sh
```

For provider integrations, prefer deterministic fixtures. Live provider tests should be manual unless they can run without secrets and without network instability.

## Release Checklist

Before tagging:

- tests pass
- `.skill` builds
- extracted `.skill` smoke test passes
- `.env` is not tracked
- archive does not include `.env`, `__pycache__`, or `.pyc`
- version is updated in `SKILL.md` and `world_cup_digest/__init__.py`
- `CHANGELOG.md` has the release entry

Create a release:

```bash
git tag v0.5.0
git push origin v0.5.0
```
