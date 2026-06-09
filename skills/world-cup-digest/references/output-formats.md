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
