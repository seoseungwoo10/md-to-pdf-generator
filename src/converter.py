import os
from .parser import MarkdownParser
from .renderer import PdfRenderer
from .styles import StyleManager
from .math_renderer import MathRenderer
import shutil

from .utils import get_resource_path

class Converter:
    def __init__(self):
        self.parser = MarkdownParser()
        # Assuming templates are in the package or relative to it. 
        # For now, let's assume we run from project root or handle paths in utils.
        # We'll make it robust later.
        template_dir = get_resource_path('templates')
        self.renderer = PdfRenderer(template_dir)
        self.style_manager = StyleManager()
        
        # Setup math renderer
        self.math_cache_dir = os.path.join(os.getcwd(), '.md2pdf_cache', 'math')
        self.math_renderer = MathRenderer(self.math_cache_dir)
        
        # Configure parser with math renderer
        self.parser.set_math_renderer(self.math_renderer)

    def cleanup(self):
        """Clean up temporary files"""
        if os.path.exists(self.math_cache_dir):
            try:
                shutil.rmtree(self.math_cache_dir)
            except Exception as e:
                print(f"Warning: Failed to cleanup cache: {e}")

    def convert_file(self, input_path, output_path, style='github', css_path=None, toc=False):
        """Convert a single file"""
        with open(input_path, 'r', encoding='utf-8') as f:
            text = f.read()
            
        if toc:
            text = "[TOC]\n\n" + text

        # Change working directory to input file's directory to resolve relative image paths
        original_cwd = os.getcwd()
        input_dir = os.path.dirname(os.path.abspath(input_path))
        os.chdir(input_dir)
        
        try:
            html_content, meta = self.parser.parse(text)
        finally:
            os.chdir(original_cwd)
        
        if css_path:
            final_css_path = css_path
        else:
            final_css_path = self.style_manager.get_style_path(style)
            
        # Get Pygments CSS
        pygments_css = self.style_manager.get_pygments_css()
        
        # Extract title from metadata if available
        title = os.path.basename(input_path)
        if meta and 'title' in meta:
            title = meta['title'][0]
            
        # Append Pygments CSS to existing CSS content
        css_content = ""
        if final_css_path and os.path.exists(final_css_path):
            with open(final_css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
        
        css_content += "\n" + pygments_css

        # We need to manually render here because we are modifying css_content
        # The renderer.render_to_pdf expects a path, but we have content.
        # Let's modify renderer to accept content or handle it here.
        # Actually renderer.render_to_pdf takes css_path.
        # We should modify renderer to accept css_content directly or write a temp file.
        # Better: Modify renderer to accept css_content string.
        
        self.renderer.render_to_pdf(
            content=html_content, 
            output_path=output_path, 
            css_content=css_content,
            title=title
        )

    def convert_directory(self, input_dir, output_dir, style='github', css_path=None, recursive=False, pattern="*.md", toc=False, workers=None):
        """Convert all files in a directory"""
        import glob
        from concurrent.futures import ProcessPoolExecutor, as_completed
        import multiprocessing
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            
        search_pattern = os.path.join(input_dir, "**", pattern) if recursive else os.path.join(input_dir, pattern)
        files = glob.glob(search_pattern, recursive=recursive)
        
        results = {'success': [], 'failed': []}
        
        # Determine number of workers
        if workers is None:
            workers = multiprocessing.cpu_count()
            
        # Helper function for parallel execution
        # Must be picklable, so it's better to be a standalone function or static method
        # But since we need self.convert_file, we can't easily make it standalone without refactoring.
        # However, ProcessPoolExecutor works with instance methods if the instance is picklable.
        # Converter has complex objects (renderer, parser) which might not be picklable.
        # It's safer to create a new Converter instance inside each process.
        
        with ProcessPoolExecutor(max_workers=workers) as executor:
            future_to_file = {}
            for file_path in files:
                # Calculate relative path to maintain structure in output
                rel_path = os.path.relpath(file_path, input_dir)
                out_path = os.path.join(output_dir, os.path.splitext(rel_path)[0] + ".pdf")
                
                # Ensure output subdirectory exists (this needs to be done in main process to avoid race conditions)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                
                # Submit task
                future = executor.submit(_convert_single_file, file_path, out_path, style, css_path, toc)
                future_to_file[future] = file_path
                
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    future.result()
                    results['success'].append(file_path)
                except Exception as e:
                    results['failed'].append((file_path, str(e)))
                
        return results

def _convert_single_file(input_path, output_path, style, css_path, toc):
    """Helper function for parallel conversion"""
    # Create a fresh converter instance for each process
    converter = Converter()
    converter.convert_file(input_path, output_path, style, css_path, toc)
