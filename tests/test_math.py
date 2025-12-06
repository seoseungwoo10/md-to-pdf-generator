import unittest
import os
import shutil
from src.math_renderer import MathRenderer

class TestMathRenderer(unittest.TestCase):
    def setUp(self):
        self.cache_dir = 'tests/cache_math'
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)
        self.renderer = MathRenderer(self.cache_dir)

    def tearDown(self):
        if os.path.exists(self.cache_dir):
            shutil.rmtree(self.cache_dir)

    def test_render_math(self):
        latex = r"E=mc^2"
        image_path = self.renderer.render(latex)
        
        self.assertTrue(os.path.exists(image_path))
        self.assertTrue(image_path.endswith('.png'))
        # Check if cache dir is part of the path
        abs_cache = os.path.abspath(self.cache_dir)
        abs_img = os.path.abspath(image_path)
        self.assertTrue(abs_img.startswith(abs_cache))

    def test_caching(self):
        latex = r"\int x dx"
        path1 = self.renderer.render(latex)
        path2 = self.renderer.render(latex)
        
        self.assertEqual(path1, path2)
        # Should only be one file in cache
        files = os.listdir(self.cache_dir)
        self.assertEqual(len(files), 1)

if __name__ == '__main__':
    unittest.main()
