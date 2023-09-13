# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['src\\main.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tcl', '_bz2', '_decimal', '_hashlib', '_lzma', '_socket', '_ssl', 'bz2', 'concurrent', 'distribute', 'distutils', 'doctest', 'docutils', 'easy_install', 'email', 'gzip', 'IPython', 'lzma', 'nose', 'nose2', 'packaging', 'pip', 'pkg_resources', 'pydoc', 'pyreadline', 'pytest', 'queue', 'readline', 'readline', 'setuptools', 'setuptools', 'sqlite3', 'tarfile', 'test', 'unittest', 'unittest', 'wheel', 'zipfile', 'zlib'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
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
    name='main',
)
