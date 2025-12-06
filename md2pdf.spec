from PyInstaller.utils.hooks import collect_all

datas = [('templates', 'templates'), ('fonts', 'fonts'), ('fonts.conf', '.')]
binaries = []
hiddenimports = [
    'weasyprint',
    'markdown',
    'jinja2',
    'pygments',
    'pygments.lexers',
    'pygments.formatters',
    'yaml',
    'pymdownx',
    'pymdownx.arithmatex',
    'matplotlib',
    'src.extensions.math_img',
    'html5lib',
    'svglib',
    'xml.dom.minidom'
]

# Collect all data and binaries for complex packages
for package in ['weasyprint']:
    tmp_ret = collect_all(package)
    datas += tmp_ret[0]
    binaries += tmp_ret[1]
    hiddenimports += tmp_ret[2]

# Add MSYS2 GTK3 DLLs
import os
gtk_bin = r'C:\msys64\mingw64\bin'
if os.path.exists(gtk_bin):
    for f in os.listdir(gtk_bin):
        if f.endswith('.dll'):
            binaries.append((os.path.join(gtk_bin, f), '.'))

block_cipher = None

a = Analysis(
    ['md2pdf.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='md2pdf',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
