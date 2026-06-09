from __future__ import annotations

import hashlib
import json
import time
import urllib.request
from pathlib import Path
from typing import Any, Callable

from .config import Settings

MAX_RESPONSE_BYTES = 5 * 1024 * 1024


class HttpClient:
    def __init__(self, settings: Settings):
        self.settings = settings

    def get_json(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        ttl_seconds: int | Callable[[Any], int] | None = None,
    ) -> tuple[Any, bool]:
        cache_key = hashlib.sha256((url + json.dumps(headers or {}, sort_keys=True)).encode()).hexdigest()
        cache_path = self.settings.cache_dir / (cache_key + ".json")
        if not self.settings.no_cache and cache_path.exists():
            try:
                cached_payload = json.loads(cache_path.read_text())
                ttl = resolve_ttl(ttl_seconds, cached_payload, self.settings.cache_ttl_default)
                age = time.time() - cache_path.stat().st_mtime
                if ttl < 0 or age <= ttl:
                    return cached_payload, True
            except (OSError, json.JSONDecodeError):
                pass

        req = urllib.request.Request(url, headers=headers or {})
        with urllib.request.urlopen(req, timeout=self.settings.timeout) as res:
            payload = decode_json_response(res.read(MAX_RESPONSE_BYTES + 1), url)

        if not self.settings.no_cache:
            self.settings.cache_dir.mkdir(parents=True, exist_ok=True)
            write_json(cache_path, payload)
        return payload, False


def decode_json_response(body: bytes, url: str) -> Any:
    if len(body) > MAX_RESPONSE_BYTES:
        raise ValueError(f"response too large for {url}")
    try:
        return json.loads(body.decode("utf-8"))
    except UnicodeDecodeError as exc:
        raise ValueError(f"response is not valid UTF-8 for {url}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"response is not valid JSON for {url}") from exc


def resolve_ttl(ttl_seconds: int | Callable[[Any], int] | None, payload: Any, default: int) -> int:
    if ttl_seconds is None:
        return default
    if callable(ttl_seconds):
        return ttl_seconds(payload)
    return ttl_seconds


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
