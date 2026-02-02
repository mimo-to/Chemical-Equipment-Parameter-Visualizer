# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# This spec file assumes it is run from the 'desktop' directory
# PATHTO/Chemical-Equipment-Parameter-Visualizer/desktop/

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=[],
    hiddenimports=[
        'main_window',
        'login_dialog',
        'theme',
        'worker',
        'logger',
        'charts_widget',
        'compare_widget',
        'history_widget',
        'upload_widget'
    ],
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
    name='Chemical_Equipment_Visualizer_Desktop',
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
)
