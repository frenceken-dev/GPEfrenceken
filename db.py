# modulo_db.py
"""Modulo Base de Datos de las Películas"""
import os
import sqlite3
import subprocess
from datetime import datetime
from zoneinfo import ZoneInfo
import pytz
from tkinter import messagebox, Toplevel


# database
def init_db():
    pass
    

# Registrar un nuevo Proveedor.
def insertar_proveedor(nombre, contacto, telefono, email, direccion):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Proveedores (nombre, contacto, telefono, email, direccion)
        VALUES (?, ?, ?, ?, ?)
    ''', (nombre, contacto, telefono, email, direccion))
    conn.commit()
    conn.close()
    

# Obtener todos los Proveedores .
def obtener_proveedores():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM Proveedores')
    proveedores = cursor.fetchall()
    conn.close()
    return proveedores


# Obtener ID del proveedor por su nombre. 
def obtener_id_proveedor_por_nombre(nombre_proveedor):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_proveedor FROM Proveedores
        WHERE nombre = ?
    ''', (nombre_proveedor,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Obtener ID de la Factura por su numero. 
def obtener_id_factura_por_numero(numero_factura):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_factura FROM Facturas
        WHERE numero_factura = ?
    ''', (numero_factura,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Obtener ID del material por su código.
def obtener_id_material_por_codigo(codigo):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id_material FROM Materiales WHERE codigo = ?', (codigo,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Obtener ID del nuevo producto por su código.
def obtener_id_producto_por_codigo(codigo):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id_producto FROM Productos WHERE codigo = ?', (codigo,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Ingresar los Items de las facturas.
def insertar_material(codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario, id_proveedor):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    try:
    # Obtener el id_proveedor usando el nombre
        #id_proveedor = obtener_id_proveedor_por_nombre(nombre)
        
        cursor.execute('''
            INSERT INTO Materiales (codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario, id_proveedor)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario, id_proveedor))
        conn.commit()
        print(f"Material guardado con id_proveedor: {id_proveedor}")  # Depuración
    except Exception as e:
        print(f"Error al guardar material: {e}")  # Depuración
        conn.rollback()
    finally:
        conn.close()
        

# Ingresar datos Basicos de la factura para el ingreso de Items.
def insertar_factura(numero_factura, fecha, nombre_proveedor):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()

    # Obtener el id_proveedor usando el nombre
    id_proveedor = obtener_id_proveedor_por_nombre(nombre_proveedor)

    # Si el proveedor no existe, crear uno nuevo
    if id_proveedor is None:
        # Aquí podrías pedir más detalles del proveedor, pero por simplicidad, solo usamos el nombre
        cursor.execute('''
            INSERT INTO Proveedores (nombre)
            VALUES (?)
        ''', (nombre_proveedor,))
        conn.commit()
        id_proveedor = cursor.lastrowid  # Obtener el id del proveedor recién insertado

    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO Facturas (numero_factura, fecha, fecha_registro, id_proveedor)
        VALUES (?, ?, ?, ?)
    ''', (numero_factura, fecha, fecha_registro, id_proveedor))
    conn.commit()
    conn.close()
    

#  Obtener los detalles de una factura.
def insertar_detalle_factura(id_factura, id_material, stock,  precio, costo_unitario):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Detalle_Factura (id_factura, id_material, stock, Precio, costo_unitario)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_factura, id_material, stock, precio, costo_unitario))
    conn.commit()
    conn.close()
    
    
# Se registra un nuevo producto creado por Ikigai GmbH.
def insertar_producto(codigo, nombre, tipo, costo_producto, precio_venta, materiales_usados, tiempo_fabricacion, cantidad, descripcion):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    fecha_registro = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO Productos (codigo, nombre, tipo, costo_producto, precio_venta, materiales_usados, tiempo_fabricacion, cantidad, fecha_registro, descripcion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (codigo, nombre, tipo, costo_producto, precio_venta, ", ".join(materiales_usados), tiempo_fabricacion, cantidad, fecha_registro, descripcion)) 
    conn.commit()
    conn.close()
    

# Obtener los materiales empleados en un producto creado.
def insertar_detalle_producto(id_producto, id_material, cantidad, tipo, tamaño):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Detalle_Producto
        (id_producto, id_material, cantidad, tipo_material, tamaño_material)
        VALUES (?, ?, ?, ?, ?)
    ''', (id_producto, id_material, cantidad, tipo, tamaño))
    conn.commit()
    conn.close()
    
    
# Obtener Materiales para creacion de producto.
def obtener_materiales():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Materiales')
    materiales = cursor.fetchall()
    conn.close()
    return materiales


# Obtener el nombre del material por el código
def obtener_nombre_material_por_codigo(codigo_material):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM Materiales WHERE codigo = ?', (codigo_material,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else "Desconocido"


# Obtener código del materia por su nombre
def obtener_codigo_material_por_nombre(nombre_material):
    print("Nombre para obtener el código del material: ", nombre_material)
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT codigo FROM Materiales WHERE nombre = ?', (nombre_material,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Materales por nombre, tipo, tamaño para crear producto nuevo.
def obtener_codigo_material_por_nombre_color_tipo_tamaño(nombre, color, tipo, tamaño):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT codigo
        FROM Materiales
        WHERE nombre = ? AND color = ? AND tipo = ? AND tamaño = ?
    ''', (nombre, color, tipo, tamaño))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None


# Obtener el costo Unitario del material
def obtener_costo_unitario_material(codigo_material):
    print("Código para obtener costo unitario del material: ",codigo_material)
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT costo_unitario FROM Materiales WHERE codigo = ?', (codigo_material,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else 0.0


# Función para actualizar el stock de un material en la base de datos
def actualizar_stock_material(codigo, cantidad):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE Materiales
        SET stock = stock - ?
        WHERE codigo = ?
    ''', (cantidad, codigo))
    conn.commit()
    conn.close()
    

# Obtener los productos ya creados.
def obtener_productos():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Productos')
    productos = cursor.fetchall()
    conn.close()
    return productos


# Seleccionar el color del material por nombre
def obtener_color_por_material(nombre_material):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT color
        FROM Materiales
        WHERE nombre = ? 
    ''', (nombre_material,))
    resultados = cursor.fetchall()
    conn.close()
    return [resultado[0] for resultado in resultados]


# Seleccionar el tipo del material por nombre
def obtener_tipos_por_material_y_color(nombre_material, color_material):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT tipo
        FROM Materiales
        WHERE nombre = ? AND color = ? 
    ''', (nombre_material, color_material))
    resultados = cursor.fetchall()
    conn.close()
    return [resultado[0] for resultado in resultados]


# Obtener tipo y tamaño de un material.
def obtener_tamaños_por_material_color_tipo(nombre_material, color_material, tipo_material):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT DISTINCT tamaño
        FROM Materiales
        WHERE nombre = ? AND color = ? AND tipo = ?
    ''', (nombre_material, color_material, tipo_material))
    resultados = cursor.fetchall()
    conn.close()
    print(f"Tamaños para {nombre_material}. color {color_material} y tipo {tipo_material}: {resultados}")  # Depuración
    return [resultado[0] for resultado in resultados]


# Datos seleccionados para el calculo de precio de venta
def obtener_productos_para_costoventa():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_producto, codigo, costo_producto FROM Productos''')
    _3_productos = cursor.fetchall()
    conn.close()
    return _3_productos


# Datos para actualizar el historial de ganancias.
def obtener_productos_para_acthistorial():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT id_producto, codigo, costo_producto, precio_venta FROM Productos''')
    productos_h = cursor.fetchall()
    conn.close()
    return productos_h


# Guardar en Historial_Ganancias
def guardar_historial(id_producto, mes_año, ganancia, margen):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO Historial_Ganancias
            (id_producto, mes, ganancia_total, margen_promedio)
            VALUES (?, ?, ?, ?)
            """,
            (id_producto, mes_año, ganancia, margen)
                )
    conn.commit()
    conn.close()


def registrar_historial_costo(id_producto, costo_anterior, costo_nuevo, es_por_lote, unidades=None, motivo=None):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO Historial_Costos
        (id_producto, fecha, costo_anterior, costo_nuevo, es_por_lote, unidades, motivo)
        VALUES (?, DATE('now'), ?, ?, ?, ?, ?)
        """,
        (id_producto, costo_anterior, costo_nuevo, es_por_lote, unidades, motivo)
    )
    conn.commit()
    conn.close()

# Mostrar el historial de costos por producto.
def mostrar_historial_costos_por_producto(codigo_producto):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT h.fecha, h.costo_anterior, h.costo_nuevo, h.es_por_lote, h.unidades, h.motivo
        FROM Historial_Costos h
        JOIN Productos p ON h.id_producto = p.id_producto
        WHERE p.codigo = ?
        ORDER BY h.fecha DESC
        """,
        (codigo_producto,)
        )
    historial_producto = cursor.fetchall()
    conn.commit()
    conn.close()
    return historial_producto

    
# Mostrar el historial de costos de todos los productos..
def mostrar_historial_costos_general():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute(
            """
            SELECT p.codigo, h.fecha, h.costo_anterior, h.costo_nuevo, h.es_por_lote, h.unidades, h.motivo
            FROM Historial_Costos h
            JOIN Productos p ON h.id_producto = p.id_producto
            ORDER BY h.fecha DESC
            """
        )
    historial_general = cursor.fetchall()
    conn.commit()
    conn.close()
    return historial_general


# Mostrar Historial de ganacias.
def mostrar_historial_ganancias_producto(codigo_producto):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute(
            """
            SELECT h.mes, h.ganancia_total, h.margen_promedio
            FROM Historial_Ganancias h
            JOIN Productos p ON h.id_producto = p.id_producto
            WHERE p.codigo = ?
            ORDER BY h.mes DESC
            """,
            (codigo_producto,)
        )
    historial = cursor.fetchall()
    conn.commit()
    conn.close()
    return historial


# Mostrar historial de ganancias mensual general.
def mostrar_historial_general_mensual(mes_str):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT p.codigo, h.ganancia_total, h.margen_promedio
        FROM Historial_Ganancias h
        JOIN Productos p ON h.id_producto = p.id_producto
        WHERE h.mes = ?
        ORDER BY p.codigo
        """,
        (mes_str,)
    )

    historial = cursor.fetchall()
    conn.commit()
    conn.close()
    return historial


# Obtener una lista de nombres de proveedores.
def obtener_nombres_proveedores(texto):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre FROM Proveedores WHERE nombre LIKE ?', (f'%{texto}%',))
    proveedores = [row[0] for row in cursor.fetchall()]
    conn.close()
    return proveedores


# Obtener los datos para el módulo de búsqueda.
def buscar_en_bd(tipo_busqueda, valor_busqueda):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    
    if tipo_busqueda == "Todos los Materiales":
       cursor.execute('SELECT codigo, nombre, tipo, tamaño, color, stock, precio, costo_unitario FROM Materiales')
    
    elif tipo_busqueda == "Proveedor":
        cursor.execute('''
             SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha, Materiales.codigo, Materiales.nombre, Materiales.stock, materiales.precio, materiales.costo_unitario
            FROM Proveedores
            JOIN Facturas ON Proveedores.id_proveedor = Facturas.id_proveedor
            JOIN Detalle_Factura ON Facturas.id_factura = Detalle_Factura.id_factura
            JOIN Materiales ON Detalle_Factura.id_material = Materiales.id_material
            WHERE Proveedores.nombre LIKE ?
        ''', (f"%{valor_busqueda}%",))

    elif tipo_busqueda == "Factura":
        cursor.execute('''
            SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha, Materiales.codigo, Materiales.nombre, Materiales.stock, materiales.precio, materiales.costo_unitario
            FROM Facturas
            JOIN Proveedores ON Facturas.id_proveedor = Proveedores.id_proveedor
            JOIN Detalle_Factura ON Facturas.id_factura = Detalle_Factura.id_factura
            JOIN Materiales ON Detalle_Factura.id_material = Materiales.id_material
            WHERE Facturas.numero_factura LIKE ?
        ''', (f"%{valor_busqueda}%",))
        
    elif tipo_busqueda == "Notas de Entregas":
        cursor.execute('''
            SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha, Materiales.codigo, Materiales.nombre, Materiales.stock, materiales.precio, materiales.costo_unitario
            FROM Facturas
            JOIN Proveedores ON Facturas.id_proveedor = Proveedores.id_proveedor
            JOIN Detalle_Factura ON Facturas.id_factura = Detalle_Factura.id_factura
            JOIN Materiales ON Detalle_Factura.id_material = Materiales.id_material
            WHERE Facturas.numero_factura LIKE ?
        ''', (f"%{valor_busqueda}%",))

    elif tipo_busqueda == "Código":
        cursor.execute('''
            SELECT Proveedores.nombre, Facturas.numero_factura, Facturas.fecha, Materiales.codigo, Materiales.nombre, Materiales.stock, materiales.precio, materiales.costo_unitario
            FROM Materiales
            JOIN Detalle_Factura ON Materiales.id_material = Detalle_Factura.id_material
            JOIN Facturas ON Detalle_Factura.id_factura = Facturas.id_factura
            JOIN Proveedores ON Facturas.id_proveedor = Proveedores.id_proveedor
            WHERE Materiales.codigo LIKE ?
        ''', (f"%{valor_busqueda}%",))

    elif tipo_busqueda == "Material":
        cursor.execute('''
            SELECT p.nombre, f.numero_factura, f.fecha, m.codigo, m.nombre, m.stock, m.precio, m.costo_unitario
            FROM Materiales m
            JOIN Detalle_Factura df ON m.id_material = df.id_material
            JOIN Facturas f ON df.id_factura = f.id_factura
            JOIN Proveedores p ON f.id_proveedor = p.id_proveedor
            WHERE m.nombre LIKE ?
        ''', (f"%{valor_busqueda}%",))

    elif tipo_busqueda == "Producto":
        cursor.execute('''
            SELECT p.codigo, p.tipo, p.costo_producto, p.precio_venta, p.materiales_usados, p.tiempo_fabricacion, p.cantidad, p.fecha_registro, p.descripcion
            FROM Productos p
            WHERE p.codigo LIKE ? OR p.nombre LIKE ?
        ''', (f"%{valor_busqueda}%", f"%{valor_busqueda}%"))
        
    elif tipo_busqueda == "Todos los Productos":
       cursor.execute('SELECT codigo, tipo, costo_producto, precio_venta, materiales_usados, tiempo_fabricacion, cantidad, fecha_registro, descripcion FROM Productos')


    resultados = cursor.fetchall()
    conn.close()
    print(f"Resultados encontrados en la db: {resultados}")
    return resultados
    
def verificar_datos():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()

    print("=== Facturas ===")
    cursor.execute('SELECT * FROM Facturas')
    facturas = cursor.fetchall()
    for factura in facturas:
        print(factura)

    print("\n=== Materiales ===")
    cursor.execute('SELECT * FROM Materiales')
    materiales = cursor.fetchall()
    for material in materiales:
        print(material)

    print("\n=== Detalle_Factura ===")
    cursor.execute('SELECT * FROM Detalle_Factura')
    detalle_factura = cursor.fetchall()
    for detalle in detalle_factura:
        print(detalle)

    print("\n=== Productos ===")
    cursor.execute('SELECT * FROM Productos')
    productos = cursor.fetchall()
    for producto in productos:
        print(producto)

    print("\n=== Detalle_Producto ===")
    cursor.execute('SELECT * FROM Detalle_Producto')
    detalle_producto = cursor.fetchall()
    for detalle in detalle_producto:
        print(detalle)

    conn.close()
    
    
def agregar_campo_():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()

    # Agregar el campo 'descripcion' a la tabla Productos
    cursor.execute('''
        ALTER TABLE Detalle_Factura
        ADD COLUMN Precio TEXT
    ''')

    conn.commit()
    conn.close()
    
    
def verificar_campo_en_bd():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()

    # Verificar la estructura de la tabla Productos
    cursor.execute("PRAGMA table_info(Proveedores)")
    columnas = cursor.fetchall()
    for columna in columnas:
        print(columna)

    conn.close()
    
# Crear nuevo usuario.
def insertar_usuario(usuario, clave, rol):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Usuarios (nombre_usuario, clave, rol) VALUES (?, ?, ?)', (usuario, clave, rol))
    conn.commit()
    conn.close()


# Validar entrada de un usuario.
def validar_credenciales(usuario, contrasena):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT clave, rol FROM Usuarios WHERE nombre_usuario = ?', (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado and resultado[0] == contrasena:
        return True, resultado[1]  # Retorna True y el rol del usuario
    else:
        return False, None

# Buscar usuarios en la base de datos.
def buscar_usuarios(texto_busqueda):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id_usuario, nombre_usuario, rol
        FROM Usuarios
        WHERE nombre_usuario LIKE ?
    ''', (f"%{texto_busqueda}%",))
    resultados = cursor.fetchall()
    conn.close()
    return resultados


# Actualizar datos de Usuarios.
def actualizar_usuario(id_usuario, nombre_usuario, rol, contrasena=None):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()

    if contrasena:
        cursor.execute('''
            UPDATE Usuarios
            SET nombre_usuario = ?, rol = ?, contraseña = ?
            WHERE id_usuario = ?
        ''', (nombre_usuario, rol, contrasena, id_usuario))
    else:
        cursor.execute('''
            UPDATE Usuarios
            SET nombre_usuario = ?, rol = ?
            WHERE id_usuario = ?
        ''', (nombre_usuario, rol, id_usuario))

    conn.commit()
    conn.close()


# Obtener los usuarios del sistema.
def obtener_nombres_usuarios():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('SELECT nombre_usuario FROM Usuarios')
    resultados = cursor.fetchall()
    conn.close()
    return [resultado[0] for resultado in resultados]


# Eliminar a usuarios de la base de datos por nombre.
def eliminar_usuario_bd_nombre(nombre_usuario):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Usuarios WHERE nombre_usuario = ?', (nombre_usuario,))
    conn.commit()
    conn.close()


# Eliminar a usuarios de la base de datos por ID.
def eliminar_usuario_bd(id_usuario):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Usuarios WHERE id_usuario = ?', (id_usuario,))
    conn.commit()
    conn.close()


# Calcular el costo de un producto.
def calcular_costo_produccion(id_producto):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()

    # Obtener materiales usados en el producto
    cursor.execute('''
        SELECT m.costo_unitario, dp.cantidad
        FROM detalle_producto dp
        JOIN Materiales m ON dp.id_material = m.id_material
        WHERE dp.id_producto = ?
    ''', (id_producto,))
    materiales = cursor.fetchall()

    # Sumar el costo total
    costo_total = sum(material[0] * material[1] for material in materiales)

    conn.close()
    return costo_total


def actualizar_costo_producto(nuevo_costo, id_producto): # Acualizar aqui los datos
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute(
            "UPDATE Productos SET costo_producto = ? WHERE id_producto = ?",
            (nuevo_costo, id_producto))
    conn.commit()
    conn.close()


# Actualizar los costos de producción.
def datos_costo_d_producto_actualizar(codigo_producto):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, costo_producto, precio_venta FROM Productos WHERE codigo = ?",
            (codigo_producto,))
    producto = cursor.fetchone()

    if not producto:
        messagebox.showerror("Error", f"No se encontró el producto seleccionado con código {codigo_producto}")
    return producto


# Actualizar el precio_venta en la base de datos
def actualizar_precio_venta(precio, id_producto):
        conn = sqlite3.connect('ikigai_inventario.db')
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE Productos SET precio_venta = ? WHERE id_producto = ?",
            (precio, id_producto)
        )
        conn.commit()
        conn.close()
        

# Modulo de simulacion de precios.
def simular_escenario(id_producto, nuevo_precio=None, nuevo_costo=None, nuevo_margen=None):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()

    # Obtener datos actuales
    cursor.execute('SELECT costo_produccion, precio_venta FROM Producto WHERE id_producto = ?', (id_producto,))
    costo_actual, precio_actual = cursor.fetchone()

    # Aplicar cambios simulados
    costo_simulado = nuevo_costo if nuevo_costo is not None else costo_actual
    precio_simulado = nuevo_precio if nuevo_precio is not None else precio_actual
    if nuevo_margen is not None:
        precio_simulado = costo_simulado * (1 + nuevo_margen/100)

    # Calcular ganancia simulada
    ganancia_simulada = (precio_simulado - costo_simulado)
    margen_simulado = (ganancia_simulada / costo_simulado) * 100

    conn.close()
    return {
        "costo_simulado": costo_simulado,
        "precio_simulado": precio_simulado,
        "ganancia_simulada": ganancia_simulada,
        "margen_simulado": margen_simulado
    }
    
    
# Verificar cantidad de producto para la venta.
def verificar_stock_suficiente(id_producto, cantidad_solicitada):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT cantidad FROM Productos WHERE id_producto = ?", (id_producto,))
    stock_actual = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return stock_actual >= cantidad_solicitada


# Restar la venta de un producto en la base de datos.
def actualizar_stock_después_venta(id_producto, cantidad_vendida):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()

    # Restar la cantidad vendida del stock actual
    cursor.execute("""
        UPDATE Productos
        SET cantidad = cantidad - ?
        WHERE id_producto = ?
    """, (cantidad_vendida, id_producto))
    conn.commit()
    conn.close()
    

# Agregar nuevo Cliente.
def nuevo_cliente(nombre, direccion, casa_num, zona_postal, identificacion_fiscal, email, telefono):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Clientes (nombre, direccion, casa_num, zona_postal, identificacion_fiscal, email, telefono)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nombre, direccion, casa_num, zona_postal, identificacion_fiscal, email, telefono))
    conn.commit()
    conn.close()


# Cargar los clientes para factura.
def cargador_clientes():
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_cliente, nombre FROM Clientes")
    clientes = cursor.fetchall()
    conn.commit()
    conn.close()
    return clientes


# Cargar productos disponibles para factura.
def cargador_productos():
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id_producto, codigo, tipo, precio_venta, cantidad FROM Productos WHERE cantidad > 0")
    productos = cursor.fetchall()
    conn.commit()
    conn.close()
    return productos


# Validar stock del producto.
def validar_stock_del_producto(id_producto):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT cantidad FROM Productos WHERE id_producto = ?", (id_producto,))
    stock_actual = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return stock_actual


# Obtener detalle del producto para venta.
def detalle_producto_venta(id_producto):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT codigo, precio_venta FROM Productos WHERE id_producto = ?", (id_producto,))
    nombre, precio_unitario = cursor.fetchone()
    conn.commit()
    conn.close()
    return nombre, precio_unitario


# Insertar la venta en la base de datos "FACTURA"
def guarda_venta_bd(id_venta, id_cliente, fecha_actual, tipo_documento, subtotal, descuento, impuesto, total):
    
    #fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Ventas (id_venta, id_cliente, fecha, tipo_documento, subtotal, descuento, impuesto, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (id_venta, id_cliente, fecha_actual, tipo_documento, subtotal, descuento, impuesto, total))
    id_venta = cursor.lastrowid
    conn.commit()
    conn.close()
    return id_venta


# Insertar datos en detalle factura.
def agregar_detalle_factura(id_venta, id_producto, cantidad, precio_unitario, subtotal):
    print("DETALLE FACTURA: ", id_venta, id_producto,cantidad, precio_unitario, subtotal)
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO Detalle_Venta (id_venta, id_producto, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (id_venta, id_producto, cantidad, precio_unitario, subtotal,))
    conn.commit()
    conn.close()
    

def guardar_nota_entrega(id_cliente, fecha, subtotal, descuento, impuesto, total):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO NotasEntrega (id_cliente, fecha, subtotal, descuento, impuesto, total)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (id_cliente, fecha, subtotal, descuento, impuesto, total))
    id_nota_entrega = cursor.lastrowid  # Obtener el ID de la nota de entrega generada
    conn.commit()
    conn.close()
    return id_nota_entrega


def agregar_detalle_nota_entrega(nota_entrega, id_producto, cantidad, precio_unitario, subtotal):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
            INSERT INTO DetalleNotaEntrega (id_nota_entrega, id_producto, cantidad, precio_unitario, subtotal)
            VALUES (?, ?, ?, ?, ?)
        """, (nota_entrega, id_producto, cantidad, precio_unitario, subtotal))
    conn.commit()
    conn.close()
    

# Actualiza el stock del producto vendido.
def actualizar_stock_producto_venta(cantidad, id_producto):
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
            UPDATE Productos
            SET cantidad = cantidad - ?
            WHERE id_producto = ?
        """, (cantidad, id_producto))
    conn.commit()
    conn.close()
 
# Consulta el historial de costos en la base de datos
def datos_imprimir_historial_costo(): 
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, hc.fecha, hc.costo_anterior, hc.costo_nuevo, hc.motivo
        FROM Historial_Costos hc
        JOIN Productos p ON hc.id_producto = p.id_producto
    """)
    historial = cursor.fetchall()
    conn.close()
    return historial
   
   
# Consulta el historial de Ganancias en la base de datos
def datos_imprimir_historial_ganancia():
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.nombre, hg.mes, hg.ganancia_total, hg.margen_promedio
        FROM Historial_Ganancias hg
        JOIN Productos p ON hg.id_producto = p.id_producto
    """)
    historial = cursor.fetchall()
    conn.close()
    return historial


# Eliminar Proveedores de la base de datos
def eliminar_proveedor_bd(nombre_proveedor):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Proveedores WHERE nombre = ?', (nombre_proveedor,))
    conn.commit()
    conn.close()
    
# Eliminar materiales de la base de datos
def eliminar_material_bd(nombre_material):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Materiales WHERE nombre = ?', (nombre_material,))
    conn.commit()
    conn.close()
    
    
# Eliminar Productos.
def eliminar_producto_bd(codigo_producto):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Productos WHERE codigo = ?', (codigo_producto,))
    conn.commit()
    conn.close()
    
# Obtener los lotes 
def obtener_lotes():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT id_lote, fecha_creacion, descripcion, cantidad_unidades FROM Lotes")
    lotes = cursor.fetchall()
    conn.close()
    return lotes

# Registrar el nuevo lote
def registrar_producto_en_lote(id_lote, id_producto, unidades_lote):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Lote_Productos (id_lote, id_producto, cantidad_asignada) VALUES (?, ?, ?)",
        (id_lote, id_producto, unidades_lote)
    )
    conn.commit()
    conn.close()
    
# Obtener lotes y sus productos.
def obtener_lotes_con_productos():
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            l.id_lote,
            l.descripcion,
            l.cantidad_unidades,
            GROUP_CONCAT(p.codigo || ' (' || lp.cantidad_asignada || ')', ', ') as productos
        FROM Lotes l
        LEFT JOIN Lote_Productos lp ON l.id_lote = lp.id_lote
        LEFT JOIN Productos p ON lp.id_producto = p.id_producto
        GROUP BY l.id_lote
    """)
    lotes = cursor.fetchall()
    conn.close()
    return lotes


def obtener_costo_actual_lote(id_lote):
    conn = sqlite3.connect('ikigai_inventario.db')
    cursor = conn.cursor()
    cursor.execute("SELECT costo_lote FROM Lotes WHERE id_lote = ?", (id_lote,))
    costo_actual = cursor.fetchone()
    conn.close()
    return costo_actual[0] if costo_actual else 0.0


import sqlite3

def limpiar_base_datos():
    conn = sqlite3.connect("ikigai_inventario.db")
    cursor = conn.cursor()

    # Desactivar las restricciones de claves foráneas
    cursor.execute("PRAGMA foreign_keys = OFF;")

    # Eliminar datos de las tablas en el orden correcto
    # Primero, elimina datos de tablas que tienen claves foráneas
    cursor.execute("DELETE FROM Detalle_Venta;")
    cursor.execute("DELETE FROM Ventas;")
    cursor.execute("DELETE FROM DetalleNotaEntrega;")
    cursor.execute("DELETE FROM NotasEntrega;")
    cursor.execute("DELETE FROM Clientes;")
    cursor.execute("DELETE FROM Productos;")
    cursor.execute("DELETE FROM Detalle_Producto;")
    cursor.execute("DELETE FROM Historial_Costos;")
    cursor.execute("DELETE FROM Historial_Ganancias;")
    # Añade aquí más tablas según sea necesario

    # Volver a activar las restricciones de claves foráneas
    cursor.execute("PRAGMA foreign_keys = ON;")

    conn.commit()
    conn.close()
    print("borrado")


if __name__ == "__main__":
    init_db()
    #verificar_campo_en_bd()
    #agregar_campo_()
    #verificar_datos()
    #limpiar_base_datos()