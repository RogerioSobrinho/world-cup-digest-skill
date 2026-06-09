from __future__ import annotations

from pathlib import Path

from .config import Settings
from .http import HttpClient, write_json
from .models import DigestBundle, ProviderResult, Query, to_jsonable
from .providers import PROVIDERS


PUBLIC_PROVIDERS = ["fifa-public", "mediawiki", "youtube-public"]
API_PROVIDERS = ["api-football", "balldontlie", "thestatsapi", "wc2026", "worldcupapi"]
DEFAULT_PROVIDERS = PUBLIC_PROVIDERS
ALL_PROVIDERS = PUBLIC_PROVIDERS + API_PROVIDERS


def run_pipeline(query: Query, settings: Settings, save_dir: str = "") -> DigestBundle:
    providers = ["mock"] if query.mock else (query.providers or DEFAULT_PROVIDERS)
    query.providers = providers
    http = HttpClient(settings)
    results: list[ProviderResult] = []
    warnings: list[str] = []

    for provider_name in providers:
        provider_cls = PROVIDERS[provider_name]
        provider = provider_cls(settings, http)
        try:
            result = provider.fetch(query)
        except Exception as exc:
            result = ProviderResult(provider=provider_name, url="unknown", ok=False, error=str(exc))
        if not result.ok:
            warnings.append(f"{provider_name} failed: {result.error}")
        elif not result.matches and not result.source_only:
            warnings.append(f"{provider_name} returned no normalized matches; inspect raw payload or use web fallback.")
        results.append(result)

    if not any(result.ok for result in results):
        warnings.append("No provider succeeded. Browse official FIFA pages and reputable match reports before synthesis.")
    if not any(result.matches for result in results):
        if any(result.source_only and result.ok for result in results):
            warnings.append("Only public source guides are available. Verify facts with web sources before final synthesis.")
        else:
            warnings.append("No normalized match data available. Do not produce final scores/stats unless verified via web sources.")

    bundle = DigestBundle.create(query=query, results=results, warnings=warnings)
    if save_dir:
        out = Path(save_dir).expanduser()
        write_json(out / "world-cup-bundle.json", to_jsonable(bundle))
    return bundle
