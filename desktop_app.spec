# -*- mode: python ; coding: utf-8 -*-
import os

# Get the absolute path to the project directory
project_dir = os.path.abspath('.')

a = Analysis(
    ['desktop_app.py'],
    pathex=[project_dir],  # Add project directory to path
    binaries=[],
    datas=[
        ('backend', 'backend'),  # Include the entire backend directory
        ('frontend', 'frontend'),  # Include frontend templates/static files
    ],
    hiddenimports=[
        'requests',
        'flask',
        'flask_socketio',
        'engineio.async_drivers.threading',
        'socketio',
        'h5py',
        'webview',
        'backend',
        'backend.app',
        'backend.extractor',
        'backend.inspector',
        'backend.extract_snapshots',
        'backend.filter_endpoints',
        'werkzeug.security',
        'pkg_resources.py2_warn',
        'tkinter',
        'tkinter.filedialog',
        'tkinter.constants',
        'tkinter.ttk',
        'tkinter.messagebox'
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
    exclude_binaries=True,
    name='SSJOD',
    debug=True,                # Enable debug output
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,             # <-- set this to True temporarily to see output/error
    icon='frontend/static/ssjodShip.icns',
    bundle_files=1,
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


app = BUNDLE(
    exe,
    a.binaries,
    a.datas,
    console=True,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='SSJOD.app',
    icon='frontend/static/ssjodShip.icns',
    bundle_identifier='com.ucc.ssjod',  # Use your own bundle ID
    info_plist={
        'CFBundleName': 'SSJOD',
        'CFBundleDisplayName': 'SSJOD',
        'CFBundleIdentifier': 'com.ucc.ssjod',
        'CFBundleVersion': '0.1',
        'CFBundleShortVersionString': '0.1',
        'NSHighResolutionCapable': 'True',
    }
)
