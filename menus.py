# modulo_menus.py

import tkinter as tk
from tkinter import messagebox
from inventario import ingresar_inventario
from productos import crear_producto
from busqueda import busqueda_articulos #menu_buscar_articulo, formulario_buscar_por_proveedor, formulario_buscar_por_factura, formulario_buscar_por_codigo, formulario_buscar_por_articulo
from registrar_nuevo_proveedor import nuevo_proveedor

# menus.py
def menu_gestion_inventario(root, mostrar_menu_principal, imagen_panel_tk, rol, imagen_tk):
    
    # Limpiar el frame de cualquier contenido
    for widget in root.winfo_children():
        widget.destroy()

    # Crear frame_contenido (para formularios)
    frame_contenido = tk.Frame(root, bg="#a0b9f0", width=600, height=800)
    frame_contenido.pack(expand=True, fill=tk.BOTH, side=tk.RIGHT)
    
    # Frame para el título
    frame_titulo = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(root, bg="#2C3E50", width=200, height=800)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)        
    
    frame_imagen = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_imagen.pack(expand=True)
        
    if imagen_tk:
        tk.Label(frame_imagen, image=imagen_tk, bg="#a0b9f0").pack(pady=20)
    else:
        tk.Label(frame_imagen, text="Ikigai Designs", font=("Arial", 24), bg="#a0b9f0").pack(pady=20)
    
    # Botones del submenú nivel administrador.
    if rol == "administrador":
        
        # Título
        title_label = tk.Label(
            frame_titulo,
            text="Gestión de Inventario, Productos y Proveedores",
            font=("Arial", 16, "bold"),
            bg="#a0b9f0",
            fg="#2C3E50"
            )
        title_label.pack(pady=15)
        
        # Agregar metodos de eliminación y creacion de usuarios
        #tk.Label(frame_contenido, text="GESTIÓN DE INVENTARIO", bg="#a0b9f0", font=("Arial", 14)).pack(pady=10)
        tk.Button(
            frame_botones,
            text="Ingresar a Inventario",
            bg="#B1AE04",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: ingresar_inventario(frame_contenido, frame_botones, imagen_panel_tk, lambda: menu_gestion_inventario(root, mostrar_menu_principal, imagen_panel_tk)),
            width=18
        ).pack(pady=10)
        tk.Button(
            frame_botones,
            text="Crear Producto",
            bg="#EB11CE",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: crear_producto(frame_contenido, lambda: menu_gestion_inventario(root, mostrar_menu_principal, imagen_panel_tk)),
            width=18
        ).pack(pady=10)
        tk.Button(
            frame_botones,
            text="Registrar Proveedor",
            bg="#7148E0",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: nuevo_proveedor(frame_contenido, lambda: menu_gestion_inventario(root, mostrar_menu_principal)),
            width=18
        ).pack(pady=10)
        tk.Button(
            frame_botones,
            text="Menú Principal",
            bg="#913131",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=mostrar_menu_principal,
            width=18
        ).pack(pady=10)
    
    # Botones del submenú nivel usuario.  PENDIENTE PARA CAMBIOS
    elif rol == "usuario":
        
        # Título
        title_label = tk.Label(
            frame_titulo,
            text="Gestión de Inventario, Productos y Proveedores",
            font=("Arial", 16, "bold"),
            bg="#a0b9f0",
            fg="#2C3E50"
            )
        title_label.pack(pady=15)
        
        #tk.Label(frame_contenido, text="GESTIÓN DE INVENTARIO", bg="#a0b9f0", font=("Arial", 14)).pack(pady=10)
        tk.Button(
            frame_botones,
            text="Ingresar a Inventario",
            bg="#B1AE04",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: ingresar_inventario(frame_contenido, lambda: menu_gestion_inventario(root, mostrar_menu_principal)),
            width=18
        ).pack(pady=10)
        
        tk.Button(
            frame_botones,
            text="Crear Producto",
            bg="#EB11CE",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: crear_producto(frame_contenido, lambda: menu_gestion_inventario(root, mostrar_menu_principal, imagen_panel_tk)),
            width=18
        ).pack(pady=10)
        
        tk.Button(
            frame_botones,
            text="Registrar Proveedor",
            bg="#7148E0",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=lambda: nuevo_proveedor(frame_contenido, lambda: menu_gestion_inventario(root, mostrar_menu_principal)),
            width=18
        ).pack(pady=10)
        
        tk.Button(
            frame_botones,
            text="Menú Principal",
            bg="#913131",
            fg="white",
            font=("Arial", 11, "bold"),
            bd=0,
            relief=tk.FLAT,
            activebackground="#2ECC71",
            activeforeground="white",
            command=mostrar_menu_principal,
            width=18
        ).pack(pady=10)
    