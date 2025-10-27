# -*- mode: python ; coding: utf-8 -*-
import sys
import os

# Asegúrate de que las rutas sean absolutas o relativas al directorio del script
base_path = os.path.dirname(os.path.abspath(__file__))

a = Analysis(
    ['modulo_main.py'],
    pathex=[base_path],
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
    icon_path = os.path.join(base_path, 'iniciar.ico')
elif sys.platform == 'darwin':
    icon_path = os.path.join(base_path, 'iniciar.icns')
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
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    name='Gestion_frenceken'
)