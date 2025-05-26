# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['desktop_app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('backend', 'backend'),
        ('frontend/templates', 'frontend/templates'),     # ← your Flask templates
        ('frontend/static', 'frontend/static'),  
        ],
    hiddenimports=[
        'requests',
        'flask',
        'flask_socketio',
        'engineio.async_drivers.threading',
        'socketio',
        'h5py',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='desktop_app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='desktop_app',
)

app = BUNDLE(
    coll,
    name='SSJOD.app',
    icon='frontend/static/ssjodShip.icns',
    bundle_identifier=None,
)