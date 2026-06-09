import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "world-cup-digest" / "scripts" / "world-cup-fetch.py"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), *args], cwd=ROOT, text=True, capture_output=True, check=True)


class CliTests(unittest.TestCase):
    def test_mock_markdown_contains_normalized_match(self):
        result = run_cli("--mock", "--emit", "markdown")
        self.assertIn("Mexico 1 x 2 Brazil", result.stdout)
        self.assertIn("Forward Three", result.stdout)
        self.assertIn("Stats:", result.stdout)

    def test_mock_2022_uses_brazil_serbia_world_cup_opener(self):
        result = run_cli("--mock", "--season", "2022", "--match", "Brazil vs Serbia", "--emit", "markdown")
        self.assertIn("Brazil 2 x 0 Serbia", result.stdout)
        self.assertIn("Richarlison", result.stdout)
        self.assertIn("Lusail Stadium", result.stdout)

    def test_mock_json_has_dataclass_shape(self):
        result = run_cli("--mock", "--emit", "json")
        payload = json.loads(result.stdout)
        self.assertTrue(payload["query"]["mock"])
        self.assertEqual(payload["query"]["season"], "2026")
        self.assertEqual(payload["results"][0]["provider"], "mock")
        self.assertEqual(payload["results"][0]["matches"][0]["home"]["name"], "Mexico")

    def test_diagnose_masks_provider_keys(self):
        result = run_cli("--diagnose")
        payload = json.loads(result.stdout)
        self.assertIn("providers", payload)
        self.assertIn("api-football", payload["providers"])

    def test_range_and_all_provider_arguments_are_reflected(self):
        result = run_cli("--mock", "--range", "2026-06-11", "2026-06-18", "--provider", "all", "--emit", "json")
        payload = json.loads(result.stdout)
        self.assertEqual(payload["query"]["start_date"], "2026-06-11")
        self.assertEqual(payload["query"]["end_date"], "2026-06-18")
        self.assertEqual(payload["query"]["providers"], ["mock"])

    def test_save_dir_writes_research_bundle(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = run_cli("--mock", "--save-dir", tmp, "--emit", "compact")
            self.assertIn("Mexico vs Brazil", result.stdout)

            bundle_path = Path(tmp) / "world-cup-bundle.json"
            self.assertTrue(bundle_path.exists())
            payload = json.loads(bundle_path.read_text())
            self.assertEqual(payload["results"][0]["provider"], "mock")


if __name__ == "__main__":
    unittest.main()
