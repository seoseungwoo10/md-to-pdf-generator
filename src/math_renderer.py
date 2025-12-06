import matplotlib.pyplot as plt
import io
import hashlib
import os

class MathRenderer:
    def __init__(self, cache_dir=None):
        self.cache_dir = cache_dir
        if self.cache_dir and not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
            
        # Configure matplotlib for Korean support
        plt.rcParams['font.family'] = 'Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] = False
        # Ensure math text also uses the Korean font
        plt.rcParams['mathtext.fontset'] = 'custom'
        plt.rcParams['mathtext.rm'] = 'Malgun Gothic'
        plt.rcParams['mathtext.it'] = 'Malgun Gothic:italic'
        plt.rcParams['mathtext.bf'] = 'Malgun Gothic:bold'

    def render(self, latex, output_path=None, dpi=150, fontsize=12):
        """
        Render a LaTeX string to an image.
        """
        # Generate a hash for caching
        latex_hash = hashlib.md5(latex.encode('utf-8')).hexdigest()
        
        if self.cache_dir:
            filename = f"{latex_hash}.png"
            cached_path = os.path.join(self.cache_dir, filename)
            if os.path.exists(cached_path):
                return cached_path
            if not output_path:
                output_path = cached_path

        if not output_path:
            raise ValueError("Output path must be provided if cache_dir is not set")

        # Setup matplotlib
        fig = plt.figure(figsize=(0.1, 0.1))
        fig.text(0, 0, f"${latex}$", fontsize=fontsize)
        
        # Save to buffer first to crop
        buf = io.BytesIO()
        plt.axis('off')
        
        # We need to render it to get the bbox
        try:
            # This is a bit tricky with matplotlib to get tight bbox for text only
            # A simpler approach for 'mathtext' is to use mathtext directly or just save with bbox_inches='tight'
            plt.savefig(buf, format='png', dpi=dpi, bbox_inches='tight', pad_inches=0.05, transparent=True)
            plt.close(fig)
            
            with open(output_path, 'wb') as f:
                f.write(buf.getvalue())
                
            return output_path
        except Exception as e:
            plt.close(fig)
            # print(f"Failed to render math: {latex}. Error: {e}")
            return None
