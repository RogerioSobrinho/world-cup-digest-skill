# World Cup Digest Skill

Manual AI-agent skill for following the FIFA World Cup when you cannot watch every match.

It helps an agent produce concise, sourced summaries for:

- one specific match
- all matches today
- a matchday/day recap
- a weekly tournament digest
- group and knockout context
- "what should I watch later?" recommendations

The skill includes a bundled fetcher script, similar in spirit to `last30days` using its own Python engine. The script gathers a research bundle from public sources and optional football data providers, then the agent verifies and synthesizes the final recap.

The default mode is free/public-source oriented. Paid sports-data APIs are optional.

## Install

### Codex, Cursor, Copilot, Gemini CLI, Claude Code, and other Agent Skills hosts

Install globally:

```bash
npx skills add RogerioSobrinho/world-cup-digest-skill -g
```

Install for Codex only:

```bash
npx skills add RogerioSobrinho/world-cup-digest-skill -g -a codex
```

Install for multiple harnesses:

```bash
npx skills add RogerioSobrinho/world-cup-digest-skill -g -a codex -a cursor -a gemini-cli
```

Update:

```bash
npx skills update world-cup-digest -g
```

List/remove:

```bash
npx skills list -g
npx skills remove world-cup-digest -g
```

### Manual local install

Clone the repo and symlink the skill folder into your Codex skills directory:

```bash
git clone https://github.com/RogerioSobrinho/world-cup-digest-skill.git
mkdir -p ~/.codex/skills
ln -s "$(pwd)/world-cup-digest-skill/skills/world-cup-digest" ~/.codex/skills/world-cup-digest
```

For other hosts, symlink or copy `skills/world-cup-digest` into that host's skills directory.

### Build a `.skill` archive

```bash
bash skills/world-cup-digest/scripts/build-skill.sh
```

The archive is written to `dist/world-cup-digest.skill`.

## Data providers

The bundled engine lives at:

```bash
skills/world-cup-digest/scripts/world-cup-fetch.py
```

It supports optional provider env vars:

```bash
cp .env.example .env
```

Then configure one or more:

- `WC2026_API_KEY`
- `THESTATSAPI_KEY`
- `API_FOOTBALL_KEY`
- `BALLDONTLIE_FIFA_KEY`
- `WORLDCUPAPI_KEY`

Run manually:

```bash
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --free --match "Brazil vs Morocco" --date 2026-06-13 --emit markdown
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --mock --emit markdown
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --mock --season 2022 --match "Brazil vs Serbia" --emit markdown
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --today --emit markdown
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --date 2026-06-12 --emit json
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --team Brazil --provider api-football --emit markdown
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --live --provider api-football --emit compact
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --diagnose
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --env-file .env --diagnose
```

The script is deliberately best-effort because football data providers differ in endpoint shape, auth, and coverage. Treat its output as a research bundle, not as the final user-facing digest.

See [CONFIGURATION.md](CONFIGURATION.md) for provider setup, cache, diagnostics, and troubleshooting.

See [CONCEPTS.md](CONCEPTS.md) for the data model and free/public-mode philosophy.

## Free/public mode

Free mode uses:

- `fifa-public` for official schedule/search guidance
- `youtube-public` for CazéTV/YouTube stream and highlights discovery
- `mediawiki` for public post-match and tournament context

It is good for editorial recaps, daily digests, and "what should I watch?" guidance. It is not a replacement for paid live-stat APIs when you need xG, shot maps, ratings, or guaranteed minute-by-minute structured data.

## Tests

The test suite uses only Python standard library:

```bash
PYTHONPATH=skills/world-cup-digest/scripts python3 -m unittest discover -s tests -v
```

CI also builds `dist/world-cup-digest.skill` and smoke-tests the extracted archive with `--mock`.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup, provider guidelines, security expectations, and release checklist.

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Release

Create a GitHub release by pushing a version tag:

```bash
git tag v0.5.0
git push origin v0.5.0
```

The release workflow runs tests, builds the `.skill` archive, smoke-tests it, and uploads `dist/world-cup-digest.skill`.

## Example prompts

```text
Use world-cup-digest: previa de Brasil x Marrocos na estreia do Brasil na Copa 2026.
```

```text
Use world-cup-digest: jogos de hoje da Copa, com placar, contexto e o que vale assistir.
```

```text
Use world-cup-digest: resumo da semana da Copa. Quero saber quem jogou bem e quais narrativas importam.
```

```text
Use world-cup-digest: me explica o Grupo G depois dos jogos de hoje.
```

Historical test fixture:

```bash
python3 skills/world-cup-digest/scripts/world-cup-fetch.py --mock --season 2022 --match "Brazil vs Serbia" --emit compact
```

API-Football Free-plan note: tests against World Cup 2014 are rejected by the provider plan. Keep old World Cup regression tests in fixtures/mocks or public-source mode unless a paid provider plan is configured.

## Notes

- The agent must browse/currently verify match data. World Cup results, lineups, injuries, standings, and stats change constantly.
- The skill should not invent xG, player ratings, possession, or tactical claims when a source does not provide them.
- Prefer official FIFA data for schedule/result identity, then use reputable match reports and stats providers for interpretation.
