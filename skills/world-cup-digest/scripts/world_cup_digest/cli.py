from __future__ import annotations

import argparse
import sys
from datetime import date

from .config import Settings
from .diagnose import render_diagnose
from .models import Query
from .pipeline import ALL_PROVIDERS, DEFAULT_PROVIDERS, PUBLIC_PROVIDERS, run_pipeline
from .providers import PROVIDERS
from .render import render_compact, render_json, render_markdown


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch World Cup data and produce a digest research bundle.")
    parser.add_argument("topic", nargs="*", help="Optional natural-language topic, e.g. 'Brazil vs Germany'.")
    parser.add_argument("--today", action="store_true", help="Use today's date as --date.")
    parser.add_argument("--season", default="2026", help="Tournament season/year, e.g. 2026 or 2022.")
    parser.add_argument("--date", default="", help="Date filter in YYYY-MM-DD.")
    parser.add_argument("--range", nargs=2, metavar=("START", "END"), help="Date range in YYYY-MM-DD YYYY-MM-DD.")
    parser.add_argument("--live", action="store_true", help="Fetch currently live/in-progress matches when the provider supports it.")
    parser.add_argument("--team", default="", help="Team name or provider-specific team id.")
    parser.add_argument("--match", default="", help="Human-readable match filter, e.g. 'Brazil vs Germany'.")
    parser.add_argument("--match-id", default="", help="Provider-specific fixture/match id.")
    parser.add_argument("--provider", action="append", choices=["all", *PROVIDERS.keys()], default=[], help="Provider to query. Repeatable.")
    parser.add_argument("--free", action="store_true", help="Use only public/free source providers.")
    parser.add_argument("--emit", "--format", dest="emit", choices=["markdown", "json", "compact"], default="markdown")
    parser.add_argument("--mock", action="store_true", help="Use local fixtures instead of network providers.")
    parser.add_argument("--diagnose", action="store_true", help="Print configuration diagnostics and exit.")
    parser.add_argument("--save-dir", default="", help="Optional directory to save world-cup-bundle.json.")
    parser.add_argument("--cache-dir", default="", help="Override cache directory.")
    parser.add_argument("--no-cache", action="store_true", help="Disable HTTP cache.")
    parser.add_argument("--env-file", default="", help="Load provider keys and settings from a dotenv-style file.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    settings = Settings.from_env(cache_dir=args.cache_dir, no_cache=args.no_cache, env_file=args.env_file)
    if args.diagnose:
        sys.stdout.write(render_diagnose(settings))
        return 0

    selected = args.provider or []
    if "all" in selected:
        selected = ALL_PROVIDERS
    if args.free:
        selected = PUBLIC_PROVIDERS
    start_date = ""
    end_date = ""
    if args.range:
        start_date, end_date = args.range
    query = Query(
        season=args.season,
        date=date.today().isoformat() if args.today and not args.date else args.date,
        start_date=start_date,
        end_date=end_date,
        live=args.live,
        team=args.team,
        match=args.match or " ".join(args.topic),
        match_id=args.match_id,
        providers=selected,
        mock=args.mock,
    )
    bundle = run_pipeline(query=query, settings=settings, save_dir=args.save_dir)
    if args.emit == "json":
        sys.stdout.write(render_json(bundle))
    elif args.emit == "compact":
        sys.stdout.write(render_compact(bundle))
    else:
        sys.stdout.write(render_markdown(bundle))
    return 0
