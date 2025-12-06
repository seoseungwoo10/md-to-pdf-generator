
import os
import sys
import pathlib
from jinja2 import Environment, FileSystemLoader
import weasyprint
from .utils import get_resource_path

class PdfRenderer:
    def __init__(self, template_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.font_family = 'sans-serif' # Default fallback
        self.font_css = ""
        
        # Register Noto Sans KR font with WeasyPrint via @font-face
        try:
            self.font_path = get_resource_path(os.path.join('fonts', 'NotoSansKR', 'NotoSansKR-Regular.ttf'))
            if os.path.exists(self.font_path):
                # Convert path to file URI for CSS
                font_uri = pathlib.Path(self.font_path).as_uri()
                
                self.font_family = 'NotoSansKR'
                # We add the @font-face rule. 
                # Note: We assign it to 'NotoSansKR' family.
                self.font_css = f"""
                    @font-face {{
                        font-family: 'NotoSansKR';
                        src: url('{font_uri}');
                    }}
                """
                print(f"Font registered successfully: {self.font_path}")
            else:
                print(f"Warning: Font file not found at {self.font_path}")
                self.font_family = 'Helvetica'
        except Exception as e:
            print(f"Warning: Failed to ensure font configuration: {e}")
            import traceback
            traceback.print_exc()
            self.font_family = 'Helvetica'
    
    def render_to_pdf(self, content, output_path, css_content=None, css_path=None, title="Document"):
        """Render HTML content to PDF"""
        template = self.env.get_template('default.html')
        
        # Start with font CSS
        final_css = self.font_css
        
        if css_path and os.path.exists(css_path):
            with open(css_path, 'r', encoding='utf-8') as f:
                final_css += "\n" + f.read()
        
        if css_content:
            final_css += "\n" + css_content

        html_string = template.render(
            content=content,
            title=title,
            css_content=final_css,
            font_family=self.font_family
        )
        
        # Debug: Print HTML to check for syntax errors (optional)
        # print(html_string[:1000])
        
        try:
            # WeasyPrint generation
            # base_url is set to current working directory to resolve relative paths in Markdown/HTML
            html = weasyprint.HTML(string=html_string, base_url=os.getcwd())
            html.write_pdf(output_path)
            
        except Exception as e:
            raise Exception(f"PDF generation failed: {e}")
