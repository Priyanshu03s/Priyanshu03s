import xml.etree.ElementTree as ET
import unittest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_cards import (
    generate_hero_svg,
    generate_pillars_svg,
    generate_stats_svg,
    generate_tech_matrix_svg,
    generate_spotlight_cards
)

class TestSVGRenderer(unittest.TestCase):
    def test_hero_svg_validity(self):
        svg = generate_hero_svg()
        root = ET.fromstring(svg)
        self.assertEqual(root.tag.split('}')[-1], 'svg')
        self.assertIn('viewBox', root.attrib)
        self.assertIn('PRIYANSHU THAKUR', svg)

    def test_pillars_svg_validity(self):
        svg = generate_pillars_svg()
        root = ET.fromstring(svg)
        self.assertEqual(root.tag.split('}')[-1], 'svg')
        self.assertIn('AI &amp; RAG SYSTEMS', svg)
        self.assertIn('ENTERPRISE BACKEND', svg)

    def test_stats_svg_fallback(self):
        svg = generate_stats_svg(None, None)
        root = ET.fromstring(svg)
        self.assertEqual(root.tag.split('}')[-1], 'svg')
        self.assertIn('GITHUB ACTIVITY', svg)
        self.assertIn('TOP REPOSITORY LANGUAGES', svg)

    def test_tech_matrix_svg_validity(self):
        svg = generate_tech_matrix_svg()
        root = ET.fromstring(svg)
        self.assertEqual(root.tag.split('}')[-1], 'svg')
        self.assertIn('Spring Boot', svg)
        self.assertIn('Python', svg)
        self.assertIn('Angular', svg)

    def test_spotlight_cards_validity(self):
        cards = generate_spotlight_cards()
        self.assertEqual(len(cards), 3)
        for name, content in cards.items():
            root = ET.fromstring(content)
            self.assertEqual(root.tag.split('}')[-1], 'svg')
            self.assertIn('viewBox', root.attrib)

if __name__ == '__main__':
    unittest.main()
