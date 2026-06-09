import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from world_cup_digest.config import Settings


class ConfigTests(unittest.TestCase):
    def test_settings_loads_dotenv_file_and_masks_os_env_precedence(self):
        with tempfile.TemporaryDirectory() as tmp:
            env_file = Path(tmp) / ".env"
            env_file.write_text(
                "\n".join([
                    "API_FOOTBALL_KEY=from-file",
                    "WORLD_CUP_DIGEST_CACHE_TTL_LIVE=15",
                    "WORLD_CUP_DIGEST_TIMEOUT=7",
                ])
            )

            with patch.dict(os.environ, {"API_FOOTBALL_KEY": "from-os"}, clear=True):
                settings = Settings.from_env(env_file=str(env_file))

            self.assertEqual(settings.env_value("API_FOOTBALL_KEY"), "from-os")
            self.assertEqual(settings.timeout, 7)
            self.assertEqual(settings.cache_ttl_live, 15)
            self.assertEqual(settings.env_file, env_file)

    def test_invalid_numeric_env_falls_back_to_bounded_defaults(self):
        with patch.dict(os.environ, {
            "WORLD_CUP_DIGEST_TIMEOUT": "not-a-number",
            "WORLD_CUP_DIGEST_CACHE_TTL_LIVE": "-10",
            "WORLD_CUP_DIGEST_CACHE_TTL_FINAL": "999999999",
        }, clear=True):
            settings = Settings.from_env()

        self.assertEqual(settings.timeout, 20)
        self.assertEqual(settings.cache_ttl_live, 0)
        self.assertEqual(settings.cache_ttl_final, 604800)


if __name__ == "__main__":
    unittest.main()
