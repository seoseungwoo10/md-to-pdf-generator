import unittest
from src.parser import MarkdownParser

class TestMarkdownParser(unittest.TestCase):
    def setUp(self):
        self.parser = MarkdownParser()

    def test_parse_basic(self):
        text = "# Hello\n\nWorld"
        html, meta = self.parser.parse(text)
        self.assertIn('<h1 id="hello">Hello</h1>', html)
        self.assertIn("<p>World</p>", html)
        self.assertEqual(meta, {})

    def test_parse_metadata(self):
        text = "---\ntitle: Test Doc\nauthor: Me\n---\n\nContent"
        html, meta = self.parser.parse(text)
        self.assertIn("<p>Content</p>", html)
        self.assertEqual(meta.get('title'), ['Test Doc'])
        self.assertEqual(meta.get('author'), ['Me'])

    def test_toc_generation(self):
        # TOC is enabled by default in parser if extension is loaded, 
        # but usually requires [TOC] marker or specific config.
        # Our parser loads 'toc' extension by default.
        text = "[TOC]\n\n# Header 1\n## Header 2"
        html, _ = self.parser.parse(text)
        self.assertIn('class="toc"', html)
        self.assertIn('href="#header-1"', html)

if __name__ == '__main__':
    unittest.main()
