# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for DevToolKit.
Build with: pyinstaller devtoolkit.spec
"""

import os
import glob

block_cipher = None

# Collect all tool modules
tool_files = glob.glob(os.path.join('devtoolkit', 'tools', '*.py'))
tool_datas = [(f, os.path.join('devtoolkit', 'tools')) for f in tool_files]

a = Analysis(
    ['devtoolkit_app.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'devtoolkit',
        'devtoolkit.cli',
        'devtoolkit.tools',
        'devtoolkit.tools.file_organizer',
        'devtoolkit.tools.duplicate_finder',
        'devtoolkit.tools.password_gen',
        'devtoolkit.tools.converter',
        'devtoolkit.tools.text_search',
        'devtoolkit.tools.sysinfo',
        'devtoolkit.tools.todo_manager',
        'devtoolkit.tools.hash_calc',
        'devtoolkit.tools.timestamp',
        'devtoolkit.tools.http_server',
        'devtoolkit.tools.regex_tester',
        'devtoolkit.tools.snippet_mgr',
        'devtoolkit.tools.encoder',
        'devtoolkit.tools.file_diff',
        'devtoolkit.tools.lorem',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'tkinter', '_tkinter', 'unittest', 'pydoc',
        'doctest', 'pdb', 'profile', 'pstats',
    ],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='devtoolkit',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    icon=None,
)
