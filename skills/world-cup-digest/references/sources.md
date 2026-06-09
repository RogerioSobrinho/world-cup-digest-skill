# Source Guidance

Use sources according to the question and available harness tools. Prefer primary/official sources for identity and score, then richer data/reporting for synthesis.

## Primary Identity Sources

- FIFA tournament pages: fixture identity, venue, stage, kickoff, official score.
- Official team/federation channels: lineups, injuries, suspensions, press conference quotes.

## Free/Public Source Mode

The bundled engine includes public source guides:

- `fifa-public`: official FIFA search/schedule links for identity, kickoff, venue, stage, score, and tournament context.
- `youtube-public`: CazéTV/YouTube search links for legal free Brazil broadcast discovery, replays, and official highlights when available.
- `mediawiki`: MediaWiki search API for public post-match/tournament context.

These are not structured live-stat providers. They should trigger web verification and synthesis, not direct statistical claims.

Never bypass anti-bot systems, login walls, app-only endpoints, Cloudflare, private APIs, or video access controls. Do not download or transcribe full broadcasts.

## Match Data Sources

Potential providers to verify at runtime:

- FIFA official match centre.
- BALLDONTLIE FIFA World Cup API: matches, standings, lineups, events, player/team stats, ratings when available.
- API-FOOTBALL/API-SPORTS: fixtures, lineups, events, player ratings, team/player statistics when coverage exists.
- TheStatsAPI: match events, possession, shots, xG where available.
- Sofascore, FotMob, WhoScored, ESPN, BBC/Sky/Guardian match centres when accessible.

Do not assume any provider has complete coverage. Check each match.

## Interpretation Sources

Use reputable reports and analysis for "how the game felt" and tactical interpretation:

- ESPN, BBC Sport, The Guardian, Sky Sports, AP, Reuters, The Athletic, FIFA match reports.
- Team press conferences for coach/player quotes.
- Tactical blogs/channels only when clearly sourced and post-match.

## Community Sources

Use Reddit/X/YouTube fan reaction only as flavor:

- label it as reaction
- do not use it as proof of performance
- avoid over-weighting viral takes

## Verification Checklist

For a specific match, try to verify:

- final score and stage
- scorers and minute
- major cards/penalties/VAR
- starting lineups
- substitutions that changed the match
- shots, shots on target, possession
- xG and player ratings only if available from a stats provider
- group/bracket implications

If sources disagree:

1. Trust official score/events first.
2. Mention uncertainty for non-official stats.
3. Avoid precise claims that depend on disputed data.
