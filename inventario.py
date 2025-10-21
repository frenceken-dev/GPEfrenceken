# inventario.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, simpledialog
from db import obtener_nombres_proveedores, insertar_factura, insertar_material, obtener_id_proveedor_por_nombre, obtener_id_factura_por_numero, obtener_id_material_por_codigo, insertar_detalle_factura


# Variables globales para almacenar datos temporales
materiales_temporales = []  # Lista para almacenar los materiales antes de guardar
datos_factura = {
    "proveedor": "",
    "numero_factura": "",
    "fecha": ""
}

def ingresar_inventario(frame_contenido, frame_botones, imagen_panel_tk, volver_menu):
    # Limpiar el frame de contenido
    for widget in frame_contenido.winfo_children():
        widget.destroy()

    frame_titulo = tk.Frame(frame_contenido, bg="#a0b9f0")
    frame_titulo.pack(side=tk.TOP, fill=tk.X, pady=15)
    
    # Frame para los botones (lado izquierdo)
    frame_botones = tk.Frame(frame_botones, bg="#2C3E50", width=200, height=800)
    frame_botones.pack(side=tk.LEFT, fill=tk.Y)
    frame_botones.pack_propagate(False)
    
    frame_imagen_panel = tk.Frame(frame_botones, bg="#2C3E50", height=70)
    frame_imagen_panel.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
    
    # Imagen del Logo para el panel izquierdo
    if imagen_panel_tk:
        label_imagen = tk.Label(frame_imagen_panel, image=imagen_panel_tk, bg="#2C3E50")
        label_imagen.pack(side=tk.LEFT, padx=70)
    else:
        label_texto = tk.Label(frame_imagen_panel, text="Ikigai", font=("Arial", 10), bg="#2C3E50")
        label_texto.pack(side=tk.LEFT, padx=30)

    # Formulario para ingresar factura
    form_frame = tk.Frame(frame_contenido, bg="#a0b9f0", padx=20, pady=20)
    form_frame.place(relx=0.5, rely=0.1, anchor=tk.N)

    # Título
    title_label = tk.Label(
        frame_titulo,
        text="Aumento de inventario por facturas",
        font=("Arial", 16, "bold"),
        bg="#a0b9f0",
        fg="#2C3E50"
    )
    title_label.pack(pady=15)

    # Campos de la factura
    tk.Label(form_frame, text="Proveedor:", bg="#a0b9f0").grid(row=0, column=0, sticky="e") # ajustar entry mostrar lista
    proveedor_entry = tk.Entry(form_frame, width=30)
    proveedor_entry.grid(row=0, column=1, pady=5)
    
    # Obtener nombres de proveedores desde BD
    nombres_proveedores = obtener_nombres_proveedores(proveedor_entry.get())
    
    # Crear el Combox
    proveedor_combobox = ttk.Combobox(form_frame, values=nombres_proveedores, width=28)
    proveedor_combobox.grid(row=0, column=1, pady=5)
    
    # Funcion para actualizar las funciones del combobox según lo que se escriba.
    def actualizar_opciones(event):
        texto = proveedor_combobox.get()
        proveedores_filtrados = obtener_nombres_proveedores(texto)
        proveedor_combobox['values'] = proveedores_filtrados
        
    # Vincular la funcion al evento de escritura.
    proveedor_combobox.bind('<KeyRelease>', actualizar_opciones)    
    
    # Ingreso Número de fectura
    tk.Label(form_frame, text="Número de Factura:", bg="#a0b9f0").grid(row=1, column=0, sticky="e")
    factura_entry = tk.Entry(form_frame, width=30)
    factura_entry.grid(row=1, column=1, pady=5)

    # Fecha de ingreso al sistema
    tk.Label(form_frame, text="Fecha (DD/MM/AAAA):", bg="#a0b9f0").grid(row=2, column=0, sticky="e")
    fecha_entry = tk.Entry(form_frame, width=30)
    fecha_entry.grid(row=2, column=1, pady=5)
    
    # Botones (inicialmente deshabilitados)
    btn_agregar_material = tk.Button(
        form_frame,
        text="Agregar Material",
        command=lambda: agregar_material_temporal(frame_contenido),
        bg="#a0b9f0",
        state=tk.DISABLED
    )
    btn_agregar_material.grid(row=3, column=0, pady=10)

    btn_mostrar_datos = tk.Button(
        form_frame,
        text="Mostrar Datos Ingresados",
        command=lambda: [
            datos_factura.update({
                "proveedor": proveedor_combobox.get(),
                "numero_factura": factura_entry.get(),
                "fecha": fecha_entry.get()
            }),
            mostrar_datos_ingresados()
        ],
        bg="#a0b9f0",
        state=tk.DISABLED
    )
    btn_mostrar_datos.grid(row=3, column=1, pady=10)

    btn_guardar_factura = tk.Button(
        form_frame,
        text="Guardar Factura",
        command=lambda: [
            datos_factura.update({
                "proveedor": proveedor_combobox.get(),
                "numero_factura": factura_entry.get(),
                "fecha": fecha_entry.get()
            }),
            guardar_factura_y_materiales(frame_contenido)
        ],
        bg="#4283fa",
        state=tk.DISABLED
    )
    btn_guardar_factura.grid(row=4, column=0, columnspan=2, pady=10)

    # Función para validar campos al cambiar su contenido
    def on_campo_cambiado(*args):
        actualizar_estado_botones(
            proveedor_combobox.get(),
            factura_entry.get(),
            fecha_entry.get(),
            btn_agregar_material,
            btn_mostrar_datos,
            btn_guardar_factura
        )

    # Vincular la función a los cambios en los campos
    proveedor_combobox.bind("<<ComboboxSelected>>", lambda _: on_campo_cambiado())
    proveedor_combobox.bind("<KeyRelease>", lambda _: on_campo_cambiado())
    factura_entry.bind("<KeyRelease>", lambda _: on_campo_cambiado())
    fecha_entry.bind("<KeyRelease>", lambda _: on_campo_cambiado())

    
    # Función para validar campos obligatorios
    def agregar_material_temporal(frame_contenido, ):
        # Crear una ventana emergente para ingresar los datos del material
        material_window = tk.Toplevel(frame_contenido)
        material_window.title("Agregar Material")
        material_window.geometry("400x400")

        # Campos para el material
        tk.Label(material_window, text="Código:").grid(row=0, column=0, padx=10, pady=5)
        codigo_entry = tk.Entry(material_window)
        codigo_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Nombre:").grid(row=1, column=0, padx=10, pady=5)
        nombre_entry = tk.Entry(material_window)
        nombre_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(material_window, text="Tipo:").grid(row=2, column=0, padx=10, pady=5)
        tipo_entry = tk.Entry(material_window)
        tipo_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Tamaño:").grid(row=3, column=0, padx=10, pady=5)
        tamaño_entry = tk.Entry(material_window)
        tamaño_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Color:").grid(row=4, column=0, padx=10, pady=5)
        color_entry = tk.Entry(material_window)
        color_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Cantidad:").grid(row=5, column=0, padx=10, pady=5)
        stock_entry = tk.Entry(material_window)
        stock_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(material_window, text="Precio:").grid(row=6, column=0, padx=10, pady=5)
        precio_entry = tk.Entry(material_window)
        precio_entry.grid(row=6, column=1, padx=10, pady=5)

        # Función para guardar el material temporalmente
        def guardar_material():
            precio = convertir_a_float(precio_entry.get())
            cantidad = convertir_a_float(stock_entry.get())
            costo_unitario = precio / cantidad
            
            material = {
                "codigo": codigo_entry.get(),
                "nombre": nombre_entry.get(),
                "tipo": tipo_entry.get(),
                "tamaño": tamaño_entry.get(),
                "color": color_entry.get(),
                "stock": stock_entry.get(),
                "precio": precio_entry.get(),
                "costo_unitario": costo_unitario
            }
            materiales_temporales.append(material)
            messagebox.showinfo("Éxito", "Material agregado temporalmente.")
            material_window.destroy()

        # Botón para guardar el material
        tk.Button(material_window, text="Guardar Material", command=guardar_material).grid(row=7, column=0, columnspan=2, pady=10)


def validar_campos_obligatorios(proveedor, num_factura, fecha):
    return proveedor.strip() != "" and num_factura.strip() != "" and fecha.strip() != ""


# Función para actualizar el estado de los botones
def actualizar_estado_botones(proveedor, num_factura, fecha, btn_agregar_material, btn_mostrar_datos, btn_guardar_factura):
    if validar_campos_obligatorios(proveedor, num_factura, fecha):
        btn_agregar_material.config(state=tk.NORMAL)
        btn_mostrar_datos.config(state=tk.NORMAL)
        btn_guardar_factura.config(state=tk.NORMAL)
    else:
        btn_agregar_material.config(state=tk.DISABLED)
        btn_mostrar_datos.config(state=tk.DISABLED)
        btn_guardar_factura.config(state=tk.DISABLED)
        

def limpiar_campos(frame_contenido):
    # Limpiar los campos de la factura
    for widget in frame_contenido.winfo_children():
        if isinstance(widget, tk.Frame):
            for child in widget.winfo_children():
                if isinstance(child, tk.Entry):
                    child.delete(0, tk.END)
                elif isinstance(child, ttk.Combobox):
                    child.set('')


def guardar_factura_y_materiales(frame_contenido):
    # Validar que los datos de la factura estén completos
    if not datos_factura["proveedor"] or not datos_factura["numero_factura"] or not datos_factura["fecha"]:
        messagebox.showerror("Error", "Faltan datos de la factura (proveedor, número o fecha).")
        return

    # Validar que haya al menos un material ingresado
    if not materiales_temporales:
        messagebox.showerror("Error", "No se han ingresado materiales.")
        return
    
    try:
        # 1. Guardar la factura en la base de datos
        insertar_factura(
            datos_factura["numero_factura"],
            datos_factura["fecha"],
            datos_factura["proveedor"]
        )

        # 2. Obtener el id_proveedor para guardar los materiales
        id_proveedor = obtener_id_proveedor_por_nombre(datos_factura["proveedor"])
        print("Este es el id del proveedor: ",id_proveedor)
        
        # 3. Obtener el id_factura recién ingresado
        id_factura = obtener_id_factura_por_numero(datos_factura["numero_factura"])
        print("Este es el id de la factura: ", id_factura)
        # 3. Guardar los materiales Base da datos
        for material in materiales_temporales:
            try:
                material["costo_unitario"] = round(material["costo_unitario"], 2)
            except:
                print(f"Error: El valor {material['costo_unitario']} no es un número válido.")
                material["costo_unitario"]
                
            insertar_material(
                material["codigo"],
                material["nombre"],
                material["tipo"],  
                material["tamaño"],
                material["color"],
                material["stock"],
                material["precio"],
                material["costo_unitario"],
                id_proveedor
            )

            # Obtener el id_material recién ingresado
            id_material = obtener_id_material_por_codigo(material["codigo"])
            print(f" Este es el id del material: {id_material}")
            # Verificar que id_material no sea None
            if id_material is not None:
                # Insertar en Detalle_Factura
                insertar_detalle_factura(id_factura, id_material, material["stock"], material["precio"], material["costo_unitario"])
            else:
                messagebox.showinfo("No encontrado", f"No se encontró el material con código {material['codigo']}")
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", "Factura y materiales guardados correctamente.")
        
        # Limpiar las entradas.
        limpiar_campos(frame_contenido)
        
        # Limpiar la lista temporal
        materiales_temporales.clear()        

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar: {e}")
        

# Esta función cambia la coma por el punto si el usuario usa coma.
def convertir_a_float(valor_str):
    try:
        valor_str = valor_str.replace(",", ".")
        return float(valor_str)
    except ValueError:
        print(f"Error: '{valor_str}' no es un número válido.")
        return None
    
    
def mostrar_datos_ingresados():
    if not materiales_temporales:
        messagebox.showwarning("Advertencia", "No hay materiales ingresados.")
        return

    id_proveedor = obtener_id_proveedor_por_nombre(datos_factura["proveedor"])
    
    datos = f"""
    == DATOS INGRESADOS EN LA FACTURA ==
    Proveedor: {datos_factura["proveedor"]}
    Factura N°: {datos_factura["numero_factura"]}
    Fecha: {datos_factura["fecha"]}

    == MATERIALES INGRESADOS ==
    """
    for material in materiales_temporales:
        precio = convertir_a_float(material["precio"])
        cantidad = convertir_a_float(material["stock"])
        
        if precio is not None and cantidad is not None and cantidad != 0:
            precio_uni = precio / cantidad
            datos += f"""
            Código: {material["codigo"]}
            Nombre: {material["nombre"]}
            Tipo: {material["tipo"]}
            Tamaño: {material["tamaño"]}
            Color: {material["color"]}
            Cantidad: {material["stock"]}
            Precio: {material["precio"]}
            Precio_unitario: {precio_uni:.2f}
            ID Proveedor: {id_proveedor}
            ----------------------------
            """
        else:
            datos += f"""
            Código: {material["codigo"]}
            Nombre: {material["nombre"]}
            Error: No se pudo calcular el precio unitario.
            ----------------------------
            """

    messagebox.showinfo("Datos Ingresados", datos)
       