import os
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

CARDS_DIR = Path(__file__).resolve().parent.parent / "cards"

class TestProfileSVGs(unittest.TestCase):
    def test_all_generated_cards_exist_and_valid_xml(self):
        expected_cards = [
            "hero.svg",
            "build.svg",
            "stack.svg",
            "focus.svg",
            "activity.svg",
            "heatmap.svg",
            "title-coding-dark.svg",
            "title-coding-light.svg",
            "repo-EmployeeCommunicationSystem.svg",
            "repo-CONSTRUCTION-LIBRARY.svg",
            "repo-DishaSutra.svg",
        ]
        
        for card_name in expected_cards:
            path = CARDS_DIR / card_name
            self.assertTrue(path.exists(), f"Missing expected card: {card_name}")
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            root = ET.fromstring(content)
            self.assertEqual(root.tag.split("}")[-1], "svg")
            self.assertIn("viewBox", root.attrib)

    def test_hero_card_content(self):
        with open(CARDS_DIR / "hero.svg", "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("Priyanshu", content)
        self.assertIn("Thakur", content)
        self.assertIn("FULLSTACK &amp; AI ENGINEER", content)

    def test_world_tiles_content(self):
        for name, label in [("build.svg", "BUILD"), ("stack.svg", "STACK"), ("focus.svg", "FOCUS")]:
            with open(CARDS_DIR / name, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn(label, content)

if __name__ == "__main__":
    unittest.main()
