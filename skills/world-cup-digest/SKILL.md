---
name: world-cup-digest
version: "0.5.0"
description: Use when the user wants FIFA World Cup match summaries, daily recaps, weekly digests, group context, player/team performance takeaways, or "what happened today" tournament briefings. Runs a bundled research script to fetch match data from configured football providers, then guides the agent to verify and synthesize sourced recaps without inventing statistics.
argument-hint: 'world-cup-digest Brazil vs Morocco | world-cup-digest today | world-cup-digest week'
allowed-tools: Bash, Read, Write, WebSearch
homepage: https://github.com/RogerioSobrinho/world-cup-digest-skill
repository: https://github.com/RogerioSobrinho/world-cup-digest-skill
author: rogerio
license: MIT
user-invocable: true
metadata:
  short-description: Summarize World Cup matches and matchdays
  requires:
    env: []
    optionalEnv:
      - WC2026_API_KEY
      - THESTATSAPI_KEY
      - API_FOOTBALL_KEY
      - BALLDONTLIE_FIFA_KEY
      - WORLDCUPAPI_KEY
    bins:
      - python3
    files:
      - "scripts/*"
      - "references/*"
      - "fixtures/*"
---

# World Cup Digest

Use this skill to help a user stay current with the FIFA World Cup when they cannot watch every match.

The output should answer: who won, how the match unfolded, who played well, what mattered tactically, what changed in the tournament, and what the user needs to know to stay current without watching every match.

## Mandatory Engine Step

Before synthesizing any recap, run the bundled fetcher. Do not answer from web search alone unless the engine is unavailable.

The default mode uses public/free source guides. Paid/stat APIs are optional and should only be selected explicitly.

```bash
python3 "$SKILL_DIR/scripts/world-cup-fetch.py" --free --today --emit markdown
```

Adjust flags based on the user request:

```bash
python3 "$SKILL_DIR/scripts/world-cup-fetch.py" --date 2026-06-12 --emit markdown
python3 "$SKILL_DIR/scripts/world-cup-fetch.py" --team "Brazil" --emit markdown
python3 "$SKILL_DIR/scripts/world-cup-fetch.py" --match "Brazil vs Morocco" --date 2026-06-13 --emit markdown
python3 "$SKILL_DIR/scripts/world-cup-fetch.py" --free --match "Brazil vs Morocco" --date 2026-06-13 --emit markdown
python3 "$SKILL_DIR/scripts/world-cup-fetch.py" --mock --season 2022 --match "Brazil vs Serbia" --emit markdown
python3 "$SKILL_DIR/scripts/world-cup-fetch.py" --match-id "PROVIDER_FIXTURE_ID" --provider api-football --emit markdown
python3 "$SKILL_DIR/scripts/world-cup-fetch.py" --live --provider api-football --emit markdown
```

If `$SKILL_DIR` is not defined by the harness, resolve it as the directory containing this `SKILL.md`.

The fetcher is a data-gathering engine, not the final answer. It produces a research bundle from configured providers. After it runs:

1. Read the bundle.
2. Browse/search for official FIFA confirmation and at least one match report when the bundle is thin.
3. Synthesize using the formats below.

If no API keys are configured or providers return no data, still use the skill: browse current sources and clearly state that the fetcher had no provider data.

Run diagnostics when setup looks wrong:

```bash
python3 "$SKILL_DIR/scripts/world-cup-fetch.py" --diagnose
```

If provider keys live in a dotenv file, pass it explicitly when the harness runs from another working directory:

```bash
python3 "$SKILL_DIR/scripts/world-cup-fetch.py" --env-file /path/to/.env --diagnose
```

Valid skill output must be based on:

1. engine bundle evidence
2. official/current verification from web/API sources
3. clear caveats for missing or conflicting data

If the engine fails entirely, say so briefly and use web fallback. Do not hide engine failure.

## Free/Public Mode

Free mode is intended for personal tournament following without paid sports-data APIs. It provides public source guides, not guaranteed structured live statistics.

Use it for:

- official fixture identity and schedule verification
- free CazéTV/YouTube stream or highlight discovery in Brazil
- post-match public summaries and encyclopedic context
- daily/weekly editorial digests

Do not use it as proof for:

- xG
- player ratings
- live shot maps
- minute-by-minute statistics
- full broadcast transcription

Never bypass anti-bot controls, login walls, Cloudflare, app-only APIs, or private endpoints.

## Core Rules

- Always verify current match data before answering. Results, lineups, standings, injuries, cards, and player stats are time-sensitive.
- Use multiple sources for post-match interpretation when possible: official match data plus at least one reputable report or stats source.
- Do not invent xG, ratings, possession, shots, or player performance data. If a source does not provide a number, omit it or say it was not found.
- Distinguish fact from interpretation. Example: "Stats show..." versus "The reports suggest..."
- Prefer concise Portuguese when the user writes in Portuguese.
- Cite/link sources used in the response when the harness supports browsing/citations.
- Keep summaries useful for a fan who did not watch the match, not for betting.

## Request Types

### Specific Match

Examples:

- "Resumo de Brasil x Marrocos"
- "Quem jogou bem em Argentina x França?"
- "Como foi México x África do Sul?"

Workflow:

1. Identify the exact fixture, date, competition stage, and final score.
2. Gather match events: goals, assists if available, cards, substitutions, penalties, VAR, extra time/penalties.
3. Gather team stats if available: shots, shots on target, possession, xG, big chances, corners.
4. Gather lineups and player stats/ratings if available.
5. Read at least one match report for narrative and tactical context.
6. Synthesize using the "Specific Match Output" format below.

### Daily Digest

Examples:

- "Jogos de hoje da Copa"
- "Resumo dos jogos de ontem"
- "O que aconteceu hoje na Copa?"

Workflow:

1. Resolve the user's date/timezone. If relative, use the user's locale when known.
2. List all completed, live, and scheduled matches for that date.
3. For completed matches, summarize each in 3-6 bullets.
4. Identify the most important outcomes, biggest surprises, standout players, key injuries/suspensions, controversies, and table/bracket implications.
5. Rank what is worth a full replay, extended highlights, short highlights, or score-only based on stakes, drama, upset, quality, and relevance.
6. Include a radar section for any team the user names. If no team is named, include a general tournament radar.

### Weekly Digest

Examples:

- "Resumo da semana da Copa"
- "Me coloca por dentro do que rolou essa semana"

Workflow:

1. Define the exact date range.
2. Cluster matches by narrative: upsets, favorites confirming, tactical trends, injuries/suspensions, standout players.
3. Highlight tournament implications: qualified teams, eliminated teams, group scenarios, bracket changes.
4. Include a short watchlist: full replays, highlights, score-only matches, best players, biggest stories.

### Catch-Up Briefing

Examples:

- "Nao vi nada da Copa hoje, me coloca por dentro"
- "Resumo dos jogos de hoje em 5 minutos"
- "O que eu preciso saber da rodada?"

Workflow:

1. Start with the shortest useful overview: the day/week in one paragraph.
2. Prioritize signal over equal coverage. Not every match deserves the same space.
3. Include results that changed group/bracket context, best games, standout players, injuries/suspensions, controversies, and what is worth watching later.
4. Avoid framing this as social conversation. Focus on what matters to know.

### Team Radar

Examples:

- "Radar do Brasil"
- "Radar da Argentina"
- "O que importa para Marrocos nessa rodada?"
- "Como os jogos de hoje impactam a Franca?"

Workflow:

1. Use the team named by the user. Do not assume Brazil unless the user asks for Brazil or context clearly implies it.
2. Verify the team's latest match, next match, group/bracket status, injuries/suspensions, and likely implications.
3. Include relevant rivals and possible bracket paths when useful.
4. Keep it practical: what changed, what matters next, and what to watch.

### Group/Bracket Context

Examples:

- "Como ficou o grupo do Brasil?"
- "Quem pode cruzar com Argentina?"

Workflow:

1. Verify current standings/bracket.
2. Explain points, goal difference, next matches, qualification/elimination scenarios.
3. Avoid overcomplicating; present the practical outcomes.

## Specific Match Output

Use this structure unless the user asks otherwise:

```text
Team A 2 x 1 Team B
Stage, date, venue

Resumo rapido:
One short paragraph with the match story.

Como foi o jogo:
- First phase/key pattern.
- Goals and momentum shifts.
- Second half/endgame.

Quem jogou bem:
- Player: why they mattered.
- Player: why they mattered.
- Player: why they mattered.

Numeros que explicam:
- Shots / shots on target, if available.
- xG, if available.
- Possession, if meaningful.
- Cards/set pieces/keeper saves, if meaningful.

Impacto na Copa:
- Group/knockout implications.
- Next match or qualification status.

Vale ver highlights/replay?
Short recommendation.
```

## Daily Digest Output

```text
Resumo da Copa - DD/MM

Panorama:
Short synthesis of the day.

Placar do dia:
- Team A 2 x 1 Team B - one-line story.
- Team C 0 x 0 Team D - one-line story.

Principais pontos:
- Biggest result/upset.
- Standout player/team.
- Injury/suspension/controversy if relevant.

Jogos que mais importaram:
1. Match - why.
2. Match - why.
3. Match - why.

Melhores atuações:
- Player / team - evidence.

Tabela e contexto:
- Group/bracket implications.

Radar:
- Team-specific or tournament-wide note.

O que vale assistir:
- Full replay: Match - why.
- Extended highlights: Match - why.
- Short highlights/score only: Match - why.
```

## Weekly Digest Output

```text
Resumo da semana da Copa - DD/MM a DD/MM

O panorama:
Short synthesis.

Principais histórias:
- Story with evidence.
- Story with evidence.
- Story with evidence.

Melhores jogos:
- Match - why it matters.

Melhores jogadores/time:
- Player/team - evidence.

Quem subiu / quem preocupou:
- Team/player notes.

O que vale assistir:
- Full replay / highlights / score-only recommendations.

Agenda do que vem:
- Next important matches.
```

## Catch-Up Output

```text
Resumo em 30 segundos:
One paragraph with the essential state of the day/week.

O que realmente importa:
- Result/story with impact.
- Result/story with impact.
- Result/story with impact.

Nomes para guardar:
- Player/team - why.

Impacto na Copa:
- Group/bracket implications.

Radar:
- Team-specific or tournament-wide note.

O que vale assistir:
- Full replay: Match - why.
- Extended highlights: Match - why.
- Score only: Match - why.
```

## Source Strategy

Read `references/sources.md` when you need source/provider guidance.

Use this priority:

1. Official fixture/result identity: FIFA or official competition pages.
2. Match data: reliable sports data APIs/sites with events, lineups, standings, and stats.
3. Interpretation: reputable match reports, tactical reports, press conferences.
4. Fan/community reaction: optional and clearly labeled as reaction, not fact.

## Quality Bar

A good digest:

- makes the user feel caught up in under two minutes
- names the decisive moments
- identifies standout players with evidence
- explains tournament implications
- is honest about missing stats
- links to sources

A bad digest:

- gives only the score
- invents player ratings
- treats rumor/reaction as fact
- ignores group/bracket implications
- overuses generic phrases like "dominated the match" without evidence
