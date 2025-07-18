# -*- mode: python ; coding: utf-8 -*-

import re
import pathlib

# Get version from __init__.py
base_path = pathlib.Path(os.path.abspath('.'))
init_file = base_path / 'src' / '__init__.py'
with open(init_file, encoding='utf-8') as f:
    content = f.read()
    version = re.search(r"__version__\s*=\s*['\"]([^'\"]+)['\"]", content).group(1)

a = Analysis(
    ['src\\main.py'],
    pathex=['src\\'],
    binaries=[],
    datas=[
        ('SysmacSymbolExport.ico','.')
    ],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name=f'SysmacSymbolExport_v{version}',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='SysmacSymbolExport.ico'
)
