import os

from .utils import get_resource_path

class StyleManager:
    def __init__(self):
        self.styles_dir = get_resource_path(os.path.join('templates', 'styles'))

    def get_style_path(self, style_name):
        """Get path to CSS file for a given style"""
        # Simple mapping for now, assuming style_name matches filename
        css_path = os.path.join(self.styles_dir, f"{style_name}.css")
        if os.path.exists(css_path):
            return css_path
        return None

    def list_styles(self):
        """List available styles"""
        styles = []
        if os.path.exists(self.styles_dir):
            for f in os.listdir(self.styles_dir):
                if f.endswith('.css'):
                    styles.append(os.path.splitext(f)[0])
        return sorted(styles)

    def get_pygments_css(self, style_name='default'):
        """Get Pygments CSS for syntax highlighting"""
        from pygments.formatters import HtmlFormatter
        try:
            return HtmlFormatter(style=style_name).get_style_defs('.codehilite')
        except Exception:
            # Fallback to default if style not found
            return HtmlFormatter(style='default').get_style_defs('.codehilite')
