import tkinter as tk
from tkinter import ttk, messagebox
from db import obtener_productos, incrementar_stock_producto
from recursos import LOGO_PATH

class VentanaIncrementarStock:
    def __init__(self, root, frame_contenido, volver_menu):
        for widget in frame_contenido.winfo_children():
            widget.destroy()

        self.root = root
        
        # Crear frame_contenido (para formularios)
        self.frame_contenido = tk.Frame(self.root, bg="#a0b9f0", width=600, height=800)
        self.frame_contenido.place(relx=0.5, rely=0.3, anchor=tk.N)

        self.frame_titulo = tk.Frame(self.root, bg="#a0b9f0")
        self.frame_titulo.place(relx=0.5, rely=0.02, anchor=tk.N)
        
        # Título
        self.title_label = tk.Label(
            self.frame_titulo,
            text="Incrementar Stock de Producto",
            font=("Arial", 16, "bold"),
            bg="#a0b9f0",
            fg="#2C3E50"
        )
        self.title_label.pack(pady=15)
        
        self.label_producto = ttk.Label(self.frame_contenido, text="Seleccione el producto:")
        self.label_producto.grid(row=0, column=0, padx=10, pady=10)

        self.combobox_productos = ttk.Combobox(self.frame_contenido, state="readonly")
        self.combobox_productos.grid(row=0, column=1, padx=10, pady=10)

        self.label_cantidad = ttk.Label(self.frame_contenido, text="Cantidad a incrementar:")
        self.label_cantidad.grid(row=1, column=0, padx=10, pady=10)

        self.entry_cantidad = ttk.Entry(self.frame_contenido)
        self.entry_cantidad.grid(row=1, column=1, padx=10, pady=10)

        self.boton_incrementar = ttk.Button(self.frame_contenido, text="Incrementar Stock", command=self.incrementar_stock)
        self.boton_incrementar.grid(row=2, column=0, columnspan=2, pady=10)

        self.cargar_productos()

    def cargar_productos(self):
        productos = obtener_productos()
        self.combobox_productos['values'] = [f"{producto[0]} - {producto[1]}" for producto in productos]

    def incrementar_stock(self):
        producto_seleccionado = self.combobox_productos.get()
        cantidad = self.entry_cantidad.get()

        if not producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto.")
            return

        if not cantidad or not cantidad.isdigit() or int(cantidad) <= 0:
            messagebox.showerror("Error", "Debe ingresar una cantidad válida.")
            return

        id_producto = int(producto_seleccionado.split(" - ")[0])
        cantidad = int(cantidad)

        incrementar_stock_producto(id_producto, cantidad)