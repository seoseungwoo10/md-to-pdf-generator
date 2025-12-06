from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
import xml.etree.ElementTree as etree
import re

import pathlib

class MathImgTreeprocessor(Treeprocessor):
    def __init__(self, md, renderer):
        super().__init__(md)
        self.renderer = renderer


    def run(self, root):
        # Find all elements with class 'arithmatex'
        # Note: arithmatex produces <span class="arithmatex">\(...\)</span> for inline
        # and <div class="arithmatex">\[...\]</div> for block
        
        # We need to traverse recursively
        for parent in root.iter():
            for child in list(parent):
                if child.get('class') == 'arithmatex':
                    self.process_element(child)
                # Also check if the element itself is arithmatex (though usually it's a child)
                
        # Also check root children directly (iter() covers all)
        return root

    def process_element(self, el):
        text = el.text
        if not text:
            return

        # Strip wrappers
        # Inline: \( ... \)
        # Block: \[ ... \]
        is_block = False
        if text.startswith('\\[') and text.endswith('\\]'):
            latex = text[2:-2].strip()
            is_block = True
        elif text.startswith('\\(') and text.endswith('\\)'):
            latex = text[2:-2].strip()
        else:
            # Maybe raw?
            latex = text.strip()

        # Heuristic validation to detect currency collisions
        if not self._is_valid_latex(latex):
            img_path = None
        else:
            # Increase font size for better quality
            img_path = self.renderer.render(latex, fontsize=18)

        if img_path:
            # Replace content of el with img
            el.text = ''
            el.tag = 'img'
            # Convert absolute path to file URI for WeasyPrint
            img_uri = pathlib.Path(img_path).as_uri()
            el.set('src', img_uri)
            el.set('alt', latex)
            el.set('class', 'math-img')
            if not is_block:
                el.set('style', 'vertical-align: middle; max-height: 1.5em;')
            else:
                el.set('style', 'display: block; margin: 1em auto; max-height: 2.5em;')
        else:
            # Rendering failed (likely not math, e.g., currency)
            # Restore original text with delimiters
            if is_block:
                el.text = f"$${latex}$$"
            else:
                el.text = f"${latex}$"
            
            # Remove arithmatex class to prevent styling issues
            classes = el.get('class', '').split()
            if 'arithmatex' in classes:
                classes.remove('arithmatex')
                if classes:
                    el.set('class', ' '.join(classes))
                else:
                    del el.attrib['class']

    def _is_valid_latex(self, latex):
        """
        Heuristic check to see if the string is likely valid math 
        and not a currency collision (e.g. '10 = ', '30) > 3등 (').
        """
        if not latex:
            return False
            
        # Check 1: Should not end with '=' (common in '$10 = $30')
        if latex.strip().endswith('='):
            return False
            
        # Check 2: Parentheses balance
        # Ignore escaped parentheses \( \)
        clean_latex = latex.replace(r'\(', '').replace(r'\)', '')
        balance = 0
        for char in clean_latex:
            if char == '(':
                balance += 1
            elif char == ')':
                balance -= 1
                if balance < 0:
                    return False
        if balance != 0:
            return False
            
        return True
            
        # print("HTML output : " + html_output)

class MathImgExtension(Extension):
    def __init__(self, renderer=None, **kwargs):
        self.renderer_obj = renderer
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        renderer = self.renderer_obj
        if not renderer:
            return

        # Register Treeprocessor with high priority (after arithmatex)
        # Arithmatex runs as an inline processor. Treeprocessors run after inline.
        math_proc = MathImgTreeprocessor(md, renderer)
        md.treeprocessors.register(math_proc, 'math_img', 10)

def makeExtension(**kwargs):
    return MathImgExtension(**kwargs)
