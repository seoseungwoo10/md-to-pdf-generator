import markdown

text = """
Math: $E=mc^2$
Currency: $10 = $30
Table:
| Col1 | Col2 |
|---|---|
| $10 | $30 |

List:
- 2등: 2명 × $30 = $60 총액
"""

md = markdown.Markdown(extensions=[
    'extra',
    'codehilite',
    'tables',
    'toc',
    'meta',
    'pymdownx.arithmatex'
], extension_configs={
    'pymdownx.arithmatex': {
        'generic': True,
        'smart_dollar': True
    }
})

html = md.convert(text)
print(html)
