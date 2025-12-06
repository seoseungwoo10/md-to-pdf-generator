from src.parser import MarkdownParser
from src.math_renderer import MathRenderer
import os

def test_extension():
    print("Testing Math Extension for Multi-line...")
    
    # Setup
    cache_dir = '.md2pdf_cache/math'
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
        
    renderer = MathRenderer(cache_dir)
    parser = MarkdownParser()
    parser.set_math_renderer(renderer)
    
    # Test 3: Block Math (Multi line)
    text3 = """
$$
\\int_0^\\infty x^2 dx
$$
"""
    html3, _ = parser.parse(text3)
    print(f"\nInput: {text3}")
    print(f"Output: {html3}")
    
    if '<img' in html3 and 'math-img' in html3:
        print("Success: Multiline block math detected.")
    else:
        print("Failure: Multiline block math NOT detected.")

if __name__ == "__main__":
    test_extension()
