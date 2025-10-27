# recursos.py

import sys
import os

def resource_path(relative_path):
    """ Obtiene la ruta absoluta al recurso, funciona para dev y para PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Rutas de imágenes
DB_PATH = resource_path('ikigai_inventario.db')
LOGO_PATH = resource_path("Img/logo/logo_ikigai.png")
IMAGEN_BUSQUEDA_PATH = resource_path('Img/busqueda/img-busqueda.png')
