import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_showcase.py"
FIXTURE = ROOT / "examples" / "catalog.example.json"


class RendererTest(unittest.TestCase):
    def run_renderer(self, language="both"):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "showcase.html"
            result = subprocess.run(
                ["python3", str(SCRIPT), str(FIXTURE), "--output", str(output), "--language", language],
                check=True,
                capture_output=True,
                text=True,
            )
            return output.read_text(encoding="utf-8"), result.stdout

    def test_bilingual_page_contains_switch_and_all_skills(self):
        page, stdout = self.run_renderer("both")
        data = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertIn("English", page)
        self.assertIn("中文", page)
        self.assertIn("版本与镜像", page)
        for project in data["projects"]:
            for skill in project["skills"]:
                self.assertIn(skill["name"], page)
        self.assertIn("2 skills, both", stdout)

    def test_english_page_omits_language_switch(self):
        page, _ = self.run_renderer("en")
        self.assertIn('const DATA=', page)
        self.assertIn('ALLOWED=["en"]', page)
        self.assertNotIn("/Users/", page)

    def test_chinese_page_uses_chinese_only_mode(self):
        page, _ = self.run_renderer("zh-CN")
        self.assertIn('ALLOWED=["zh-CN"]', page)
        self.assertIn("Agent Skills 能力展示", page)
        self.assertNotIn("/Users/", page)

    def test_invalid_catalog_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text('{"title":"Bad","projects":[]}', encoding="utf-8")
            result = subprocess.run(["python3", str(SCRIPT), str(bad)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("must not be empty", result.stderr)


if __name__ == "__main__":
    unittest.main()
