# -*- mode: python ; coding: utf-8 -*-
import sys

a = Analysis(
    ['modulo_main.py'],
    pathex=['.'],
    binaries=[],
    datas=[
        ('ikigai_inventario.db', '.'),
        ('Img/busqueda/*', 'Img/busqueda'),
        ('Img/logo/*', 'Img/logo')
    ],
    hiddenimports=[
        'tkinter',
        'tkinter.simpledialog',
        'tkinter.messagebox',
        'sqlite3',
        'ctypes',
        'PIL',
        'multiprocessing',
        'queue',
        'os',
        'shutil',
        'datetime',
        'time',
        'pickle',
        'json',
        'csv',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

# Determinar el icono según el sistema operativo
if sys.platform == 'win32':
    icon_path = 'iniciar.ico'
elif sys.platform == 'darwin':
    icon_path = 'iniciar.icns'
else:
    icon_path = None  # Para otros sistemas operativos

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Gestion_frenceken',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=icon_path,
    target_arch='universal2'  # Construye para ambas arquitecturas (arm64 y x86_64)
)
