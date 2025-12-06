import markdown

class MarkdownParser:
    def __init__(self):
        self.md = markdown.Markdown(extensions=[
            'extra',
            'codehilite',
            'tables',
            'toc',
            'meta',
            'pymdownx.arithmatex'
        ], extension_configs={
            'pymdownx.arithmatex': {
                'generic': True
            }
        })
        self.math_renderer = None

    def set_math_renderer(self, renderer):
        self.math_renderer = renderer
        # Register our custom extension
        from .extensions.math_img import MathImgExtension
        math_ext = MathImgExtension(renderer=self.math_renderer)
        self.md.registerExtensions([math_ext], {})

    def parse(self, text):
        """Parse markdown text to HTML"""
        html = self.md.convert(text)
        return html, self.md.Meta if hasattr(self.md, 'Meta') else {}
