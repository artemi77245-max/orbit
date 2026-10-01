# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files
from PyInstaller.utils.hooks import collect_all

datas = [('C:/Users/artem/Downloads/orbit_assistant/orbit_assistant/icon.ico', '.'), ('C:/Users/artem/Downloads/orbit_assistant/orbit_assistant/config.toml', '.'), ('C:/Users/artem/Downloads/orbit_assistant/orbit_assistant/models/vosk-model-small-ru-0.22', 'models/vosk-model-small-ru-0.22')]
binaries = []
hiddenimports = []
datas += collect_data_files('certifi')
tmp_ret = collect_all('vosk')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('edge_tts')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['C:/Users/artem/Downloads/orbit_assistant/orbit_assistant/assistant_app.py'],
    pathex=['C:/Users/artem/Downloads/orbit_assistant/orbit_assistant'],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
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
    name='Orbit Assistant',
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
    icon=['C:/Users/artem/Downloads/orbit_assistant/orbit_assistant/icon.ico'],
)
