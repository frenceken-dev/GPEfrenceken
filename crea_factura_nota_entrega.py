# crea_factura_nota_entrega.py

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from db import cargador_clientes, cargador_productos, validar_stock_del_producto, detalle_producto_venta, guarda_venta_bd, agregar_detalle_factura, actualizar_stock_producto_venta, nuevo_cliente
from db import guardar_nota_entrega, agregar_detalle_nota_entrega
from datetime import datetime


class VentanaVentas:
    def __init__(self, root, usuario_actual, volver_menu, mostra_pantalla=True):
        self.root = root
        self.usuario_actual = usuario_actual  # ID del usuario logueado

        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame para los botones (lado izquierdo)
        frame_menu = tk.Frame(self.root, bg="#2C3E50", width=200, height=800, bd=3, relief="solid")
        frame_menu.pack(side=tk.LEFT, fill=tk.Y)
        frame_menu.pack_propagate(False)
        
        tk.Button(
        frame_menu,
        text="Volver al Menú",
        command=volver_menu,
        width=18,
        bg="#913131"
        ).pack(side=tk.LEFT, padx=30, pady=40)
        
        self.id_venta_actual = None
        
        # Frames principales
        self.frame_clientes = tk.LabelFrame(self.root, text="Cliente", padx=10, pady=10)
        self.frame_clientes.pack(fill="x", padx=10, pady=5)

        self.frame_productos = tk.LabelFrame(self.root, text="Productos", padx=10, pady=10)
        self.frame_productos.pack(fill="x", padx=10, pady=5)
        
        tk.Label(self.frame_productos, text="Descuento (%):").grid(row=0, column=5, sticky="w", padx=5)
        self.entry_descuento = tk.Entry(self.frame_productos, width=5)
        self.entry_descuento.grid(row=0, column=6, padx=5, pady=5)
        self.entry_descuento.insert(0, "0")  # Valor por defecto

        self.frame_resumen = tk.LabelFrame(self.root, text="Resumen de Venta", padx=10, pady=10)
        self.frame_resumen.pack(fill="both", expand=True, padx=10, pady=5)

        self.frame_botones = tk.Frame(self.root)
        self.frame_botones.pack(fill="x", padx=10, pady=10)
        
        # Bótn para imprimir.
        self.boton_imprimir = tk.Button(
        self.frame_botones,
        )
        
        # Boton para limpiar el formulario
        self.boton_nueva_venta = tk.Button(
            self.frame_botones,
            text="Limpiar Ventana",
            command=self.limpiar_pantalla
        )
        self.boton_nueva_venta.pack(side="left", padx=5, pady=5)

        # Bóton para eliminar Item de la factura.
        self.boton_eliminar = tk.Button(
            self.frame_botones,
            text="Eliminar Producto",
            command=self.eliminar_producto_seleccionado
        )
        self.boton_eliminar.pack(side="left", padx=5, pady=5)
        
        # Variables de control
        self.cliente_seleccionado = tk.IntVar()
        self.producto_seleccionado = tk.IntVar()
        self.cantidad = tk.IntVar(value=1)
        self.lista_productos_venta = []  # Lista temporal para guardar productos antes de generar la venta

        # Interfaz para selección de cliente
        self.etiqueta_cliente = tk.Label(self.frame_clientes, text="Seleccione un cliente:")
        self.etiqueta_cliente.grid(row=0, column=0, sticky="w")

        # Combobox clientes
        self.combobox_clientes = ttk.Combobox(
            self.frame_clientes,
            textvariable=self.cliente_seleccionado,
            state="readonly"
        )
        self.combobox_clientes.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.boton_nuevo_cliente = tk.Button(
            self.frame_clientes,
            text="Nuevo Cliente",
            command=self.abrir_formulario_nuevo_cliente
        )
        self.boton_nuevo_cliente.grid(row=0, column=2, padx=5, pady=5)

        # Interfaz para selección de productos
        self.etiqueta_producto = tk.Label(self.frame_productos, text="Seleccione un producto:")
        self.etiqueta_producto.grid(row=0, column=0, sticky="w")

        # Combobox productos
        self.combobox_productos = ttk.Combobox(
            self.frame_productos,
            #textvariable=self.producto_seleccionado,
            state="readonly"
        )
        self.combobox_productos.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.combobox_productos.bind("<<ComboboxSelected>>", self.on_producto_seleccionado)

        # Cargar datos iniciales
        self.cargar_clientes()
        self.cargar_productos()
        
        self.etiqueta_cantidad = tk.Label(self.frame_productos, text="Cantidad:")
        self.etiqueta_cantidad.grid(row=0, column=2, sticky="w")

        self.entry_cantidad = tk.Entry(
            self.frame_productos,
            textvariable=self.cantidad,
            width=5
        )
        self.entry_cantidad.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        self.boton_agregar = tk.Button(
            self.frame_productos,
            text="Agregar Producto",
            command=self.agregar_producto_a_venta
        )
        self.boton_agregar.grid(row=0, column=4, padx=5, pady=5)

        # Tabla para resumen de venta
        self.tree_resumen = ttk.Treeview(
            self.frame_resumen,
            columns=("Producto", "Cantidad", "Precio Unitario", "Subtotal"),
            show="headings"
        )
        self.tree_resumen.heading("Producto", text="Producto")
        self.tree_resumen.heading("Cantidad", text="Cantidad")
        self.tree_resumen.heading("Precio Unitario", text="Precio Unitario")
        self.tree_resumen.heading("Subtotal", text="Subtotal")
        self.tree_resumen.pack(fill="both", expand=True, padx=5, pady=5)

        # Etiqueta para total
        self.etiqueta_total = tk.Label(self.frame_resumen, text="Total: € 0.00", font=("Arial", 10, "bold"))
        self.etiqueta_total.pack(pady=5)

        # Botones de acción
        # Botón para generar factura
        self.boton_generar_factura = tk.Button(self.frame_botones, text="Generar Factura", command=self.generar_venta)
        self.boton_generar_factura.pack(side="left", padx=5, pady=5)

        # Botón para generar nota de entrega
        self.boton_generar_nota_entrega = tk.Button(self.frame_botones, text="Generar Nota de Entrega", command=self.generar_nota_entrega)
        self.boton_generar_nota_entrega.pack(side="left", padx=5, pady=5)

        self.boton_cancelar = tk.Button(
            self.frame_botones,
            text="Cancelar",
            command=volver_menu
        )
        self.boton_cancelar.pack(side="right", padx=5, pady=5)
    
    # Método para manejar la selección del producto
    def on_producto_seleccionado(self, event):
        self.producto_seleccionado = self.combobox_productos.get()
    
    # Cargar los clientes.
    def cargar_clientes(self):
        clientes = cargador_clientes()
        
        self.combobox_clientes["values"] = [f"{id_cliente} - {nombre}" for id_cliente, nombre in clientes]
        
        self.boton_nuevo_cliente = tk.Button(
        self.frame_clientes,
        text="Nuevo Cliente",
        command=self.abrir_formulario_nuevo_cliente
        )

    # Cargar los Productos.
    def cargar_productos(self):  # MODIFICAR AQUI QUITAR NOMBRE
        productos = cargador_productos()
        print(productos)  # donde esta tipo estaba nombre igualmente en el for
        self.combobox_productos["values"] = [f"{id_producto} - {codigo} - {tipo} (Stock: {cantidad})" for id_producto, codigo, tipo, precio_venta, cantidad in productos]

    # Aquí puedes abrir una ventana emergente para registrar un nuevo cliente
    def abrir_formulario_nuevo_cliente(self):
        # Ventana emergente
        ventana_cliente = tk.Toplevel(self.root)
        ventana_cliente.title("Registrar Nuevo Cliente")
        ventana_cliente.geometry("400x400")

        # Frame para el formulario
        frame_formulario = tk.LabelFrame(ventana_cliente, text="Datos del Cliente", padx=10, pady=10)
        frame_formulario.pack(fill="both", expand=True, padx=10, pady=10)

        # Campos del formulario
        tk.Label(frame_formulario, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        entry_nombre = tk.Entry(frame_formulario, width=30)
        entry_nombre.grid(row=0, column=1, pady=5)

        tk.Label(frame_formulario, text="Dirección:").grid(row=1, column=0, sticky="w", pady=5)
        entry_direccion = tk.Entry(frame_formulario, width=30)
        entry_direccion.grid(row=1, column=1, pady=5)

        tk.Label(frame_formulario, text="Casa N°:").grid(row=2, column=0, sticky="w", pady=5)
        entry_casa_num = tk.Entry(frame_formulario, width=30)
        entry_casa_num.grid(row=2, column=1, pady=5)

        tk.Label(frame_formulario, text="Zona Postal:").grid(row=3, column=0, sticky="w", pady=5)
        entry_zona_postal = tk.Entry(frame_formulario, width=30)
        entry_zona_postal.grid(row=3, column=1, pady=5)
        
        tk.Label(frame_formulario, text="ID Fiscal:").grid(row=4, column=0, sticky="w", pady=5)
        entry_id_fiscal = tk.Entry(frame_formulario, width=30)
        entry_id_fiscal.grid(row=4, column=1, pady=5)

        tk.Label(frame_formulario, text="Email:").grid(row=5, column=0, sticky="w", pady=5)
        entry_email = tk.Entry(frame_formulario, width=30)
        entry_email.grid(row=5, column=1, pady=5)

        tk.Label(frame_formulario, text="Teléfono:").grid(row=6, column=0, sticky="w", pady=5)
        entry_telefono = tk.Entry(frame_formulario, width=30)
        entry_telefono.grid(row=6, column=1, pady=5)

        # Función para guardar el cliente
        def guardar_cliente():
            nombre = entry_nombre.get()
            direccion = entry_direccion.get()
            casa_num = entry_casa_num.get()
            zona_postal = entry_zona_postal.get()
            id_fiscal = entry_id_fiscal.get()
            email = entry_email.get()
            telefono = entry_telefono.get()

            if not nombre:
                messagebox.showerror("Error", "El nombre del cliente es obligatorio.")
                return

            try:
                # guarda en bd clientes.
                nuevo_cliente(nombre, direccion, casa_num, zona_postal, id_fiscal, email, telefono)
                
                messagebox.showinfo("Éxito", "Cliente registrado correctamente.")
                ventana_cliente.destroy()
                self.cargar_clientes()  # Actualizar la lista de clientes
            except sqlite3.Error as e:
                messagebox.showerror("Error", f"No se pudo registrar el cliente: {e}")

        # Botón para guardar
        boton_guardar = tk.Button(
            frame_formulario,
            text="Guardar Cliente",
            command=guardar_cliente,
            bg="#22e74c"
        )
        boton_guardar.grid(row=7, column=1, pady=10, sticky="e")
        
    # Validar que se haya seleccionado un producto y un cliente
    def agregar_producto_a_venta(self):
         # Validar cliente
        if not self.combobox_clientes.get():
            messagebox.showerror("Error", "Debe seleccionar un cliente de la lista.")
            return
        # Validar que se haya seleccionado un producto
        if not hasattr(self, 'producto_seleccionado') or not self.producto_seleccionado:
            messagebox.showerror("Error", "Debe seleccionar un producto de la lista.")
            return

        # Validar que se haya seleccionado un cliente
        if not self.combobox_clientes.get():
            messagebox.showerror("Error", "Debe seleccionar un cliente.")
            return

        # Extraer el ID del producto desde el texto seleccionado
        try:
            producto_str = self.producto_seleccionado
            id_producto = int(producto_str.split(" - ")[0])
        except (ValueError, IndexError, AttributeError):
            messagebox.showerror("Error", "Seleccione un producto válido de la lista.")
            return

        # Obtener detalles del producto
        codigo, precio_unitario = detalle_producto_venta(id_producto)
        
        self.iva_incluido = tk.BooleanVar(value=True)  # Por defecto: sí incluye IVA
        self.check_iva = tk.Checkbutton(
            self.frame_productos,
            text="Incluir IVA (19%)",
            variable=self.iva_incluido
        )
        self.check_iva.grid(row=1, column=0, columnspan=2, sticky="w", padx=5)
        

        # Calcular subtotal
        # Obtener el descuento
        try:
            descuento = float(self.entry_descuento.get() or 0)
        except ValueError:
            descuento = 0
        subtotal = self.cantidad.get() * precio_unitario * (1 - descuento / 100)

        # Agregar a la lista temporal y al Treeview
        self.lista_productos_venta.append({
            "id_producto": id_producto,
            "codigo": codigo, # El articulo queda vacio si no hay nombre.
            "cantidad": self.cantidad.get(),
            "precio_unitario": precio_unitario,
            "subtotal": subtotal
        })

        self.tree_resumen.insert("", "end", values=(codigo, self.cantidad.get(), f"€ {precio_unitario:.2f}", f"€ {subtotal:.2f}"))

        # Actualizar total
        subtotal = sum(item["subtotal"] for item in self.lista_productos_venta)
        iva = subtotal * 0.19 if self.iva_incluido.get() else 0
        total = subtotal + iva
        self.etiqueta_total.config(text=f"Total: € {total:.2f}")

        # Limpiar selección
        self.cantidad.set(1)            
             
    # Generar Factura
    def generar_venta(self):
        if not self.lista_productos_venta:
            messagebox.showerror("Error", "Debe agregar al menos un producto a la venta.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de generar esta factura?")
        if not confirmar:
            return

        # Obtener el ID del cliente
        id_cliente = int(self.combobox_clientes.get().split(" - ")[0])

        # Calcular el subtotal, descuento, impuesto y total
        subtotal = sum(item["subtotal"] for item in self.lista_productos_venta)
        descuento = float(self.entry_descuento.get() or 0)
        impuesto = subtotal * 0.19  # IVA del 19%
        total = subtotal - descuento + impuesto

        # Conectar a la base de datos
        conn = sqlite3.connect("ikigai_inventario.db")
        cursor = conn.cursor()

        # Obtener el siguiente número de factura
        cursor.execute("SELECT ultimo_numero_factura FROM Configuracion WHERE id_configuracion = 1")
        ultimo_numero = cursor.fetchone()[0]
        nuevo_numero = ultimo_numero + 1
        cursor.execute("UPDATE Configuracion SET ultimo_numero_factura = ? WHERE id_configuracion = 1", (nuevo_numero,))
        id_venta = nuevo_numero

        conn.commit()
        conn.close()

        # Guardar la factura en la base de datos
        factura = guarda_venta_bd(id_venta, id_cliente, datetime.now().strftime("%Y-%m-%d"), "factura", round(subtotal, 2), descuento, round(impuesto, 2), round(total, 2))

        # Guardar los detalles de la factura
        for item in self.lista_productos_venta:
            # Guarda los datos en la base de datos
            agregar_detalle_factura(id_venta, item["id_producto"], item["cantidad"], item["precio_unitario"], item["subtotal"])
            actualizar_stock_producto_venta(item["cantidad"], item["id_producto"])

        # Mostrar el botón de imprimir
        self.id_venta_actual = id_venta
        self.boton_imprimir.config(text="Imprimir Factura", command=lambda: imprimir_factura(self.id_venta_actual))
        self.boton_imprimir.pack(side="left", padx=5, pady=5)
        

    # Generar nosta de entrega
    def generar_nota_entrega(self):
        if not self.lista_productos_venta:
            messagebox.showerror("Error", "Debe agregar al menos un producto a la nota de entrega.")
            return

        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de generar esta nota de entrega?")
        if not confirmar:
            return

        # Obtener el ID del cliente
        id_cliente = int(self.combobox_clientes.get().split(" - ")[0])

        # Calcular el subtotal, descuento, impuesto y total
        subtotal = sum(item["subtotal"] for item in self.lista_productos_venta)
        descuento = float(self.entry_descuento.get() or 0)
        impuesto = subtotal * 0.19  # IVA del 19%
        total = subtotal - descuento + impuesto

        # Guardar la nota de entrega en la base de datos
        nota_entrega = guardar_nota_entrega(id_cliente, datetime.now().strftime("%Y-%m-%d"), round(subtotal, 2), descuento, round(impuesto, 2), round(total, 2))

        # Guardar los detalles de la nota de entrega
        for item in self.lista_productos_venta:
            agregar_detalle_nota_entrega(nota_entrega, item["id_producto"], item["cantidad"], item["precio_unitario"], item["subtotal"])

        # Mostrar el botón de imprimir
        self.id_nota_entrega_actual = nota_entrega
        self.boton_imprimir.config(text="Imprimir Nota", command=lambda: imprimir_nota_entrega(self.id_nota_entrega_actual))
        self.boton_imprimir.pack(side="left", padx=5, pady=5)
        messagebox.showinfo("Éxito", f"Nota de entrega generada con éxito. ID: {nota_entrega}")
   
    
    def limpiar_pantalla(self):
        # Limpiar formulario
        self.lista_productos_venta = []
        self.tree_resumen.delete(*self.tree_resumen.get_children())
        self.etiqueta_total.config(text="Total: € 0.00")
        self.cantidad.set(1)
        self.boton_imprimir.pack_forget()  # Oculta el botón
        self.id_venta_actual = None  # Reinicia la variable
        
    
    # Función para eliminar Items de la factura.
    def eliminar_producto_seleccionado(self):
        # Obtener el item seleccionado en el Treeview
        selected_item = self.tree_resumen.selection()
        if not selected_item:
            messagebox.showerror("Error", "Debe seleccionar un producto para eliminar.")
            return

        # Confirmar eliminación
        confirmar = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este producto?")
        if not confirmar:
            return

        # Obtener el índice del producto en la lista
        for item in selected_item:
            values = self.tree_resumen.item(item, "values")
            codigo_producto = values[0]

            # Buscar y eliminar el producto de la lista
            for i, producto in enumerate(self.lista_productos_venta):
                if producto["codigo"] == codigo_producto:
                    del self.lista_productos_venta[i]
                    break

        # Actualizar el Treeview y el total
        self.tree_resumen.delete(selected_item)
        total = sum(item["subtotal"] for item in self.lista_productos_venta)
        self.etiqueta_total.config(text=f"Total: € {total:.2f}")    
        
        
    # Guardar el PDF en un archivo.
    def guardar_factura(self, id_venta):
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        from datetime import datetime
        from tkinter import filedialog
        import webbrowser
        import os
        # ... (código existente para generar el PDF)

        # Diálogo para guardar el archivo
        ruta_pdf = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            initialfile=f"factura_{id_venta}"
        )

        if not ruta_pdf:
            return  # El usuario canceló el guardado

        # Generar el PDF en la ruta seleccionada
        doc = SimpleDocTemplate(ruta_pdf, pagesize=letter)

        # Abrir el PDF automáticamente
        if os.path.exists(ruta_pdf):
            webbrowser.open(ruta_pdf)
        else:
            messagebox.showerror("Error", "No se pudo generar el PDF.")

        messagebox.showinfo("Éxito", f"Documento guardado en: {ruta_pdf}") 
        

# Función para facturan una Nota de Entrega
def convertir_nota_a_factura(id_nota_entrega):
    confirmar = messagebox.askyesno("Confirmar", "¿Estás seguro de que deseas convertir esta nota de entrega en una factura?")
    if not confirmar:
        return

    try:
        conn = sqlite3.connect("ikigai_inventario.db")
        cursor = conn.cursor()

        # Verificar si la nota de entrega ya está facturada
        cursor.execute("SELECT estado FROM NotasEntrega WHERE id_nota_entrega = ?", (id_nota_entrega,))
        estado = cursor.fetchone()[0]

        if estado == "Facturado":
            messagebox.showerror("Error", "Esta nota de entrega ya ha sido facturada.")
            return

        # Obtener los datos de la nota de entrega
        cursor.execute("""
            SELECT id_cliente, fecha, subtotal, descuento, impuesto, total
            FROM NotasEntrega
            WHERE id_nota_entrega = ?
        """, (id_nota_entrega,))

        nota_data = cursor.fetchone()
        if not nota_data:
            messagebox.showerror("Error", "No se encontró la nota de entrega.")
            return

        id_cliente, fecha, subtotal, descuento, impuesto, total = nota_data

        # Obtener el siguiente número de factura
        cursor.execute("SELECT ultimo_numero_factura FROM Configuracion WHERE id_configuracion = 1")
        ultimo_numero = cursor.fetchone()[0]
        nuevo_numero = ultimo_numero + 1
        cursor.execute("UPDATE Configuracion SET ultimo_numero_factura = ? WHERE id_configuracion = 1", (nuevo_numero,))

        # Guardar la factura en la base de datos
        cursor.execute("""
            INSERT INTO Ventas (id_venta, id_cliente, fecha, tipo_documento, subtotal, descuento, impuesto, total)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (nuevo_numero, id_cliente, fecha, "Factura", subtotal, descuento, impuesto, total))

        id_venta = nuevo_numero

        # Copiar los detalles de la nota de entrega a la factura
        cursor.execute("SELECT id_producto, cantidad, precio_unitario, subtotal FROM DetalleNotaEntrega WHERE id_nota_entrega = ?", (id_nota_entrega,))
        detalles = cursor.fetchall()

        for detalle in detalles:
            id_producto, cantidad, precio_unitario, subtotal_detalle = detalle
            cursor.execute("""
                INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad, precio_unitario, subtotal)
                VALUES (?, ?, ?, ?, ?)
            """, (id_venta, id_producto, cantidad, precio_unitario, subtotal_detalle))

        # Actualizar el estado de la nota de entrega a 'Facturado'
        cursor.execute("""
            UPDATE NotasEntrega
            SET estado = 'Facturado'
            WHERE id_nota_entrega = ?
        """, (id_nota_entrega,))

        conn.commit()
        messagebox.showinfo("Éxito", f"Nota de entrega #{id_nota_entrega} convertida en factura #{id_venta}.")

        # Preguntar si desea imprimir la nueva factura
        imprimir = messagebox.askyesno("Imprimir Factura", "¿Deseas imprimir la nueva factura ahora?")
        if imprimir:
            imprimir_factura(id_venta, es_copia=False)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo convertir la nota de entrega en factura: {e}")
    finally:
        conn.close()


# Función para imprimir facturas
def imprimir_factura(id_venta, es_copia=False):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_RIGHT, TA_LEFT
    import webbrowser
    import os

    # Consulta los datos de la venta
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()

    # Datos de la venta
    cursor.execute("""
        SELECT
            v.id_venta,
            v.fecha,
            c.nombre,
            c.direccion,
            c.identificacion_fiscal,
            v.total,
            v.tipo_documento,
            t.nombre AS tienda_nombre,
            t.direccion AS tienda_direccion,
            t.identificacion_fiscal AS tienda_identificacion_fiscal,
            v.descuento,
            v.subtotal,
            v.impuesto
        FROM
            Ventas v
        JOIN
            Clientes c ON v.id_cliente = c.id_cliente
        CROSS JOIN
            Tienda t
        WHERE
            v.id_venta = ?
    """, (id_venta,))

    venta_data = cursor.fetchone()
    if not venta_data:
        messagebox.showerror("Error", "No se encontró la venta.")
        return

    (id_venta, fecha, nombre_cliente, direccion_cliente, identificacion_fiscal_cliente,
    total, tipo_documento, tienda_nombre, tienda_direccion, tienda_identificacion_fiscal,
    descuento, subtotal, impuesto) = venta_data

    # Ruta del archivo PDF
    try:
        if es_copia:
            os.makedirs("factura_copia", exist_ok=True)
            ruta_pdf = f"factura_copia/factura_{id_venta}_COPIA.pdf"
        else:
            os.makedirs("factura_original", exist_ok=True)
            ruta_pdf = f"factura_original/factura_{id_venta}.pdf"
    except Exception as e:
        messagebox.showerror("Error", "Error al guardar la factura en carpeta.")
        

    # Detalles de la venta
    cursor.execute("""
        SELECT p.codigo, dv.cantidad, dv.precio_unitario, dv.subtotal
        FROM Detalle_Venta dv
        JOIN Productos p ON dv.id_producto = p.id_producto
        WHERE dv.id_venta = ?
    """, (id_venta,))
    detalles = cursor.fetchall()
    conn.close()

    # Preguntar al usuario si desea una copia de la factura
    if not es_copia:
        imprimir_copia = messagebox.askyesno("Copia de Factura", "¿Deseas imprimir una copia de esta factura?")
        if imprimir_copia:
            imprimir_factura(id_venta, es_copia=True)

    # Configuración del PDF
    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=100, bottomMargin=50)
    styles = getSampleStyleSheet()

    # Estilo personalizado para alinear a la derecha
    right_aligned_style = ParagraphStyle(
        name="RightAligned",
        fontName="Helvetica-Bold",
        fontSize=10,
        alignment=TA_RIGHT,
    )
    right_aligned_style_title = ParagraphStyle(
        name="RightAligned",
        fontName="Helvetica-Bold",
        fontSize=14,
        alignment=TA_RIGHT,
    )

    # Estilo personalizado para alinear a la izquierda
    left_aligned_style = ParagraphStyle(
        name="LeftAligned",
        fontName="Helvetica-Bold",
        fontSize=10,
        alignment=TA_LEFT,
    )
    left_aligned_style_detalle = ParagraphStyle(
        name="LeftAligned",
        fontName="Helvetica-Bold",
        fontSize=12,
        alignment=TA_LEFT,
    )

    story = []

    # Logo de la tienda
    logo_path = "Img/logo/logo_ikigai.png"

    # Título del documento
    if tipo_documento == "notaentrega":  # correcto es nota_entrega
        titulo_doc = f"NOTA DE ENTREGA: {id_venta}"
    else:
        titulo_doc = f"RECHNUNG: {id_venta}"
    if es_copia:
        titulo_doc += " \n -K"

    titulo_pdf = Paragraph(f"{titulo_doc}", right_aligned_style_title)
    story.append(titulo_pdf)
    story.append(Spacer(1, 25)) # 25 el espacio libre que deja debajo

    # Datos de la tienda alineados a la derecha
    datos_tienda = [
        [Paragraph(f"{tienda_nombre}", right_aligned_style)],
        [Paragraph(f"{tienda_direccion}", right_aligned_style)],
        [Paragraph(f"{tienda_identificacion_fiscal}", right_aligned_style)]
    ]
    tabla_tienda = Table(datos_tienda, colWidths=[450])
    tabla_tienda.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ]))
    story.append(tabla_tienda)
    story.append(Spacer(1, 30))

    # Información del cliente
    info_factura_cliente = [
        [Paragraph(f"Kunde:  {nombre_cliente}", left_aligned_style)],
        [Paragraph(f"Adresse:  {direccion_cliente}", left_aligned_style)],
        [Paragraph(f"Identifikationsnummer:  {identificacion_fiscal_cliente}", left_aligned_style)],
        [Paragraph(f"Ausgabedatum:  {fecha}", left_aligned_style)],
        [Paragraph(f"Dokumenttyp:  Rechnung", left_aligned_style)]
    ]
    tabla_factura_cliente = Table(info_factura_cliente, colWidths=[465])
    tabla_factura_cliente.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    story.append(tabla_factura_cliente)
    story.append(Spacer(1, 30))

    # Detalles de la venta
    titulo_detalles = [[Paragraph("Verkaufsdetails", left_aligned_style_detalle)]]
    tabla_detalles_titulo = Table(titulo_detalles, colWidths=[465])
    tabla_detalles_titulo.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    story.append(tabla_detalles_titulo)
    story.append(Spacer(1, 5))

    columnas = ["Produkt", "Menge", "Einzelpreis", "Zwischensumme"]
    detalles_data = [columnas]
    for producto, cantidad, precio, subtotal_detalle in detalles:
        detalles_data.append([producto, str(cantidad), f"€ {precio:.2f}", f"€ {subtotal_detalle:.2f}"])

    tabla_detalles = Table(detalles_data, colWidths=[180, 80, 100, 100])
    tabla_detalles.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(tabla_detalles)
    story.append(Spacer(1, 100))

    # Resumen de la factura alineado a la derecha
    resumen_data = [
        [Paragraph(f"Zwischensumme: € {subtotal:.2f}", right_aligned_style)],
        [Paragraph(f"Rabatt: € {descuento:.2f}", right_aligned_style)],
        [Paragraph(f"Steuer (MwSt. 19%): € {impuesto:.2f}", right_aligned_style)],
        [Paragraph(f"Gesamt: € {total:.2f}", right_aligned_style)]
    ]
    tabla_resumen = Table(resumen_data, colWidths=[450])
    tabla_resumen.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ]))
    story.append(tabla_resumen)

    # Función para agregar header y footer
    def header_footer(canvas, doc):
        # Header con logo
        if logo_path and os.path.exists(logo_path):
            logo = Image(logo_path, width=90, height=40)
            logo.drawOn(canvas, 50, letter[1] - 70)

        # Marca de agua "COPIA" si es una copia
        if es_copia:
            canvas.saveState()
            canvas.setFont("Helvetica", 100)
            canvas.setFillColorRGB(0.8, 0.8, 0.8)  # Color gris claro
            canvas.rotate(45)  # Rotar el texto 45 grados
            canvas.drawString(150, -100, "KOPIE")  # Posición del texto
            canvas.restoreState()

        # Footer con número de página
        canvas.saveState()
        canvas.setFont("Helvetica", 10)
        canvas.drawCentredString(letter[0] / 2.0, 20, f"Seite {doc.page}")
        canvas.restoreState()

    # Generar el PDF
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)

    # Abrir el PDF automáticamente
    if os.path.exists(ruta_pdf):
        webbrowser.open(ruta_pdf)
    else:
        messagebox.showerror("Error", "No se pudo generar el PDF.")  
        

# Función para imprimir Notas de Entregas
def imprimir_nota_entrega(id_nota_entrega, es_copia=False):
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_RIGHT, TA_LEFT
    import webbrowser
    import os

    # Consulta los datos de la nota de entrega
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ne.id_nota_entrega,
            ne.fecha,
            c.nombre,
            c.direccion,
            c.identificacion_fiscal,
            ne.total,
            ne.subtotal,
            ne.descuento,
            ne.impuesto,
            t.nombre AS tienda_nombre,
            t.direccion AS tienda_direccion,
            t.identificacion_fiscal AS tienda_identificacion_fiscal
        FROM
            NotasEntrega ne
        JOIN
            Clientes c ON ne.id_cliente = c.id_cliente
        CROSS JOIN
            Tienda t
        WHERE
            ne.id_nota_entrega = ?
    """, (id_nota_entrega,))

    nota_data = cursor.fetchone()

    if not nota_data:
        messagebox.showerror("Error", "No se encontró la nota de entrega.")
        return

    (id_nota_entrega, fecha, nombre_cliente, direccion_cliente, identificacion_fiscal_cliente,
    total, subtotal, descuento, impuesto, tienda_nombre, tienda_direccion, tienda_identificacion_fiscal) = nota_data

    # Detalles de la nota de entrega
    cursor.execute("""
        SELECT p.codigo, dne.cantidad, dne.precio_unitario, dne.subtotal
        FROM DetalleNotaEntrega dne
        JOIN Productos p ON dne.id_producto = p.id_producto
        WHERE dne.id_nota_entrega = ?
    """, (id_nota_entrega,))

    detalles = cursor.fetchall()
    conn.close()

    # Ruta del archivo PDF
    try:
        if es_copia:
            os.makedirs("factura_copia", exist_ok=True)
            ruta_pdf = f"factura_copia/factura_{id_nota_entrega}_COPIA.pdf"
        else:
            os.makedirs("factura_original", exist_ok=True)
            ruta_pdf = f"factura_original/factura_{id_nota_entrega}.pdf"
    except Exception as e:
        messagebox.showerror("Error", "Error al guardar la factura en carpeta.")
    
    # Preguntar al usuario si desea una copia de la factura
    if not es_copia:
        imprimir_copia = messagebox.askyesno("Copia Nota de Entrega", "¿Deseas imprimir una copia de esta nota de entrega?")
        if imprimir_copia:
            imprimir_nota_entrega(id_nota_entrega, es_copia=True)

    # Configuración del PDF
    doc = SimpleDocTemplate(ruta_pdf, pagesize=letter, leftMargin=30, rightMargin=30, topMargin=100, bottomMargin=50)
    styles = getSampleStyleSheet()

    # Estilo personalizado para alinear a la derecha
    right_aligned_style = ParagraphStyle(
        name="RightAligned",
        fontName="Helvetica-Bold",
        fontSize=10,
        alignment=TA_RIGHT,
    )
    right_aligned_style_title = ParagraphStyle(
        name="RightAligned",
        fontName="Helvetica-Bold",
        fontSize=14,
        alignment=TA_RIGHT,
    )

    # Estilo personalizado para alinear a la izquierda
    left_aligned_style = ParagraphStyle(
        name="LeftAligned",
        fontName="Helvetica-Bold",
        fontSize=10,
        alignment=TA_LEFT,
    )
    left_aligned_style_detalle = ParagraphStyle(
        name="LeftAligned",
        fontName="Helvetica-Bold",
        fontSize=12,
        alignment=TA_LEFT,
    )

    story = []

    # Logo de la tienda
    logo_path = "Img/logo/logo_ikigai.png"

    # Título de la nota de entrega
    titulo_doc = f"LIEFERSCHEIN: {id_nota_entrega}"
    if es_copia:
        titulo_doc += f" \n -K"

    titulo_pdf = Paragraph(f"{titulo_doc}", right_aligned_style_title)
    story.append(titulo_pdf)
    story.append(Spacer(1, 20)) # Mover aqui la etiqueta FACTURA

    # Datos de la tienda alineados a la derecha
    datos_tienda = [
        [Paragraph(f"{tienda_nombre}", right_aligned_style)],
        [Paragraph(f"{tienda_direccion}", right_aligned_style)],
        [Paragraph(f"{tienda_identificacion_fiscal}", right_aligned_style)]
    ]
    tabla_tienda = Table(datos_tienda, colWidths=[450])
    tabla_tienda.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ]))
    story.append(tabla_tienda)
    story.append(Spacer(1, 30))

    # Información del cliente
    info_factura_cliente = [
        [Paragraph(f"Kunde:  {nombre_cliente}", left_aligned_style)],
        [Paragraph(f"Adresse:  {direccion_cliente}", left_aligned_style)],
        [Paragraph(f"Identifikationsnummer:  {identificacion_fiscal_cliente}", left_aligned_style)],
        [Paragraph(f"Ausgabedatum:  {fecha}", left_aligned_style)],
        [Paragraph(f"Dokumenttyp:  Lieferschein", left_aligned_style)]
    ]
    tabla_factura_cliente = Table(info_factura_cliente, colWidths=[465])
    tabla_factura_cliente.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    story.append(tabla_factura_cliente)
    story.append(Spacer(1, 30))

    # Detalles de la venta
    titulo_detalles = [[Paragraph("Verkaufsdetails", left_aligned_style_detalle)]]
    tabla_detalles_titulo = Table(titulo_detalles, colWidths=[465])
    tabla_detalles_titulo.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    story.append(tabla_detalles_titulo)
    story.append(Spacer(1, 5))

    columnas = ["Produkt", "Menge", "Einzelpreis", "Zwischensumme"]
    detalles_data = [columnas]
    for producto, cantidad, precio, subtotal_detalle in detalles:
        detalles_data.append([producto, str(cantidad), f"€ {precio:.2f}", f"€ {subtotal_detalle:.2f}"])

    tabla_detalles = Table(detalles_data, colWidths=[180, 80, 100, 100])
    tabla_detalles.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(tabla_detalles)
    story.append(Spacer(1, 100))

    # Resumen de la factura alineado a la derecha
    resumen_data = [
        [Paragraph(f"Zwischensumme: € {subtotal:.2f}", right_aligned_style)],
        [Paragraph(f"Rabatt: € {descuento:.2f}", right_aligned_style)],
        [Paragraph(f"Steuer (MwSt. 19%): € {impuesto:.2f}", right_aligned_style)],
        [Paragraph(f"Gesamt: € {total:.2f}", right_aligned_style)]
    ]
    tabla_resumen = Table(resumen_data, colWidths=[450])
    tabla_resumen.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
    ]))
    story.append(tabla_resumen)

    # Función para agregar header y footer
    def header_footer(canvas, doc):
        if logo_path and os.path.exists(logo_path):
            logo = Image(logo_path, width=90, height=40)
            logo.drawOn(canvas, 50, letter[1] - 70)

        # Marca de agua "COPIA" si es una copia
        if es_copia:
            canvas.saveState()
            canvas.setFont("Helvetica", 100)
            canvas.setFillColorRGB(0.8, 0.8, 0.8)  # Color gris claro
            canvas.rotate(45)  # Rotar el texto 45 grados
            canvas.drawString(150, -100, "KOPIE")  # Posición del texto
            canvas.restoreState()

        # Footer con número de página
        canvas.saveState()
        canvas.setFont("Helvetica", 10)
        canvas.drawCentredString(letter[0] / 2.0, 20, f"Seite {doc.page}")
        canvas.restoreState()

    # Generar el PDF
    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)

    # Abrir el PDF automáticamente
    if os.path.exists(ruta_pdf):
        webbrowser.open(ruta_pdf)
    else:
        messagebox.showerror("Error", "No se pudo generar el PDF.") 
            