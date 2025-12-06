from src.math_renderer import MathRenderer
import os

def test_renderer():
    print("Testing MathRenderer...")
    renderer = MathRenderer(cache_dir='.md2pdf_cache/math')
    
    # Test inline
    latex1 = "E = mc^2"
    path1 = renderer.render(latex1)
    print(f"Rendered '{latex1}' to {path1}")
    
    if path1 and os.path.exists(path1):
        print("Success: Image file exists.")
    else:
        print("Failure: Image file does not exist.")

    # Test complex
    latex2 = r"\int_0^\infty x^2 dx"
    path2 = renderer.render(latex2)
    print(f"Rendered '{latex2}' to {path2}")
    
    if path2 and os.path.exists(path2):
        print("Success: Image file exists.")
    else:
        print("Failure: Image file does not exist.")

if __name__ == "__main__":
    test_renderer()
