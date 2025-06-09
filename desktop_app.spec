# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules
import os

project_dir = os.path.abspath('.')

a = Analysis(
    ['desktop_app.py'],
    pathex=[project_dir],
    binaries=[],
    datas=[
        ('backend', 'backend'),
        ('frontend', 'frontend'),
        ('frontend/static/SSjodBoat.ico', 'frontend/static'),
    ],
    hiddenimports=collect_submodules('webview') + [
        'requests',
        'flask',
        'flask_socketio',
        'engineio.async_drivers.threading',
        'socketio',
        'webview',
        'h5py',
        'backend',
        'backend.app',
        'backend.extractor',
        'backend.inspector',
        'backend.extract_snapshots',
        'backend.filter_endpoints',
        'werkzeug.security',
        'pkg_resources.py2_warn',
    ],
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
    [],
    exclude_binaries=False,
    name='SSJOD.exe',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # ← might help icon appear
    icon='frontend/static/SSjodBoat.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SSjodex',
)
