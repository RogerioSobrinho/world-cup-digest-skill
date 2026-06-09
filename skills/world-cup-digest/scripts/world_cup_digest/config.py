from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


DEFAULT_BASES = {
    "api-football": "https://v3.football.api-sports.io",
    "balldontlie": "https://fifa.balldontlie.io/api/v1",
    "thestatsapi": "https://api.thestatsapi.com/api",
    "wc2026": "https://api.wc2026api.com",
    "worldcupapi": "https://worldcupapi.com/api",
}

MIN_TIMEOUT = 1
MAX_TIMEOUT = 60
MIN_TTL = 0
MAX_TTL = 604800


@dataclass(frozen=True)
class Settings:
    cache_dir: Path
    timeout: int
    env: dict[str, str]
    no_cache: bool = False
    env_file: Path | None = None
    cache_ttl_default: int = 300
    cache_ttl_live: int = 20
    cache_ttl_scheduled: int = 300
    cache_ttl_final: int = 86400

    @classmethod
    def from_env(cls, cache_dir: str = "", no_cache: bool = False, env_file: str = "") -> "Settings":
        loaded_env, loaded_path = load_env(env_file)
        env = {**loaded_env, **dict(os.environ)}
        root = Path(cache_dir or env.get("WORLD_CUP_DIGEST_CACHE_DIR", "~/.cache/world-cup-digest")).expanduser()
        timeout = bounded_int(env.get("WORLD_CUP_DIGEST_TIMEOUT"), default=20, minimum=MIN_TIMEOUT, maximum=MAX_TIMEOUT)
        return cls(
            cache_dir=root,
            timeout=timeout,
            env=env,
            no_cache=no_cache,
            env_file=loaded_path,
            cache_ttl_default=bounded_int(env.get("WORLD_CUP_DIGEST_CACHE_TTL_DEFAULT"), default=300, minimum=MIN_TTL, maximum=MAX_TTL),
            cache_ttl_live=bounded_int(env.get("WORLD_CUP_DIGEST_CACHE_TTL_LIVE"), default=20, minimum=MIN_TTL, maximum=MAX_TTL),
            cache_ttl_scheduled=bounded_int(env.get("WORLD_CUP_DIGEST_CACHE_TTL_SCHEDULED"), default=300, minimum=MIN_TTL, maximum=MAX_TTL),
            cache_ttl_final=bounded_int(env.get("WORLD_CUP_DIGEST_CACHE_TTL_FINAL"), default=86400, minimum=MIN_TTL, maximum=MAX_TTL),
        )

    def env_value(self, key: str, default: str = "") -> str:
        return self.env.get(key, default).strip()

    def base_url(self, provider: str) -> str:
        env_key = provider.upper().replace("-", "_") + "_BASE"
        return self.env_value(env_key, DEFAULT_BASES[provider])

    def has_key(self, key: str) -> bool:
        return bool(self.env_value(key))


def mask(value: str) -> str:
    if not value:
        return "missing"
    if len(value) <= 6:
        return "***"
    return value[:2] + "***" + value[-2:]


def load_env(env_file: str = "") -> tuple[dict[str, str], Path | None]:
    path = resolve_env_file(env_file)
    if not path:
        return {}, None
    values: dict[str, str] = {}
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = strip_env_value(value.strip())
        if key:
            values[key] = value
    return values, path


def resolve_env_file(env_file: str = "") -> Path | None:
    candidates = []
    if env_file:
        candidates.append(Path(env_file).expanduser())
    else:
        candidates.append(Path.cwd() / ".env")
        candidates.append(Path(__file__).resolve().parents[4] / ".env")
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def strip_env_value(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
        return value[1:-1]
    return value


def bounded_int(value: str | None, default: int, minimum: int, maximum: int) -> int:
    try:
        parsed = int(value) if value not in (None, "") else default
    except ValueError:
        return default
    return max(minimum, min(maximum, parsed))
