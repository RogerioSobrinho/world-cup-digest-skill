# Output Format Details

Use these when the user asks for a reusable artifact, a dashboard feed, or a more structured output.

## JSON Match Digest

```json
{
  "match": {
    "home": "Team A",
    "away": "Team B",
    "score": "2-1",
    "stage": "Group A",
    "date": "2026-06-11",
    "venue": "Estadio Azteca"
  },
  "summary": "Short narrative.",
  "timeline": [
    {"minute": "12", "event": "Goal", "team": "Team A", "player": "Player"}
  ],
  "standouts": [
    {"player": "Player", "team": "Team A", "reason": "Goal and chance creation"}
  ],
  "stats": {
    "shots": {"home": 12, "away": 8},
    "shotsOnTarget": {"home": 5, "away": 3},
    "xg": {"home": 1.8, "away": 0.9}
  },
  "implications": ["Team A leads Group A"],
  "watchRecommendation": "Highlights enough / worth full replay",
  "sources": ["https://..."]
}
```

Only include stats fields when verified.

## Short Push-Style Digest

Useful for daily notifications:

```text
Team A 2-1 Team B: Team A won a tight match after a late goal. Player X was decisive, Team B created pressure but lacked finishing. Team A now controls the group; highlights are enough unless you follow either team.
```

## "Worth Watching" Scale

Use sparingly:

- `Full replay`: high-quality game, major upset, tactical drama, or very relevant to user's team.
- `Extended highlights`: good moments but not essential full match.
- `Score only`: low-event or low-impact game.

Explain the recommendation in one sentence.

## Catch-Up Briefing

Use when the user wants to get current quickly.

```text
Resumo em 30 segundos:
Essential state of the day/week.

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

## Team Radar

Use for any team the user names. Do not default to Brazil unless requested.

```text
Radar - Team

Estado atual:
- Latest result/status.

O que mudou:
- Group/bracket impact.

Próximo jogo:
- Opponent/date/stakes.

Pontos de atenção:
- Injuries/suspensions/form/tactical concern if verified.

Rivais e cruzamentos:
- Relevant paths or opponents.

O que vale assistir:
- Replay/highlights/score-only recommendation.
```
