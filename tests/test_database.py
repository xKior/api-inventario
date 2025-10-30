import pytest
from inventario.database import (
    crear_producto, obtener_productos, obtener_producto_por_id,
    actualizar_stock, eliminar_producto
)
from inventario.models import db, Producto

def test_crear_producto_database(app):
    """Prueba crear producto en base de datos"""
    with app.app_context():
        datos = {'nombre': 'Auriculares', 'precio': 45.0, 'stock': 12}
        producto, errores = crear_producto(datos)
        
        assert producto is not None
        assert errores is None
        assert producto.nombre == 'Auriculares'

def test_crear_producto_sin_nombre(app):
    """Prueba crear producto sin nombre"""
    with app.app_context():
        datos = {'nombre': None, 'precio': 45.0, 'stock': 12}
        producto, errores = crear_producto(datos)
        
        assert producto is None
        assert errores is not None
        assert len(errores) > 0

def test_crear_producto_datos_invalidos(app):
    """Prueba crear producto con múltiples errores"""
    with app.app_context():
        datos = {'nombre': '', 'precio': -10, 'stock': -5}
        producto, errores = crear_producto(datos)
        
        assert producto is None
        assert len(errores) >= 3

def test_obtener_productos_paginacion(app):
    """Prueba obtener productos con paginación"""
    with app.app_context():
        # Crear 15 productos
        for i in range(15):
            datos = {'nombre': f'Prod {i}', 'precio': 10.0, 'stock': 1}
            crear_producto(datos)
        
        paginacion = obtener_productos(pagina=1, por_pagina=10)
        assert len(paginacion.items) == 10
        assert paginacion.total == 15
        assert paginacion.pages == 2

def test_obtener_productos_segunda_pagina(app):
    """Prueba obtener segunda página"""
    with app.app_context():
        for i in range(15):
            datos = {'nombre': f'Prod {i}', 'precio': 10.0, 'stock': 1}
            crear_producto(datos)
        
        paginacion = obtener_productos(pagina=2, por_pagina=10)
        assert len(paginacion.items) == 5

def test_obtener_producto_por_id_existente(app):
    """Prueba obtener producto por ID existente"""
    with app.app_context():
        datos = {'nombre': 'Cable HDMI', 'precio': 15.0, 'stock': 30}
        producto, _ = crear_producto(datos)
        
        producto_encontrado = obtener_producto_por_id(producto.id)
        assert producto_encontrado is not None
        assert producto_encontrado.nombre == 'Cable HDMI'

def test_obtener_producto_por_id_inexistente(app):
    """Prueba obtener producto por ID inexistente"""
    with app.app_context():
        producto = obtener_producto_por_id(9999)
        assert producto is None

def test_actualizar_stock_database(app):
    """Prueba actualizar stock en base de datos"""
    with app.app_context():
        datos = {'nombre': 'SSD', 'precio': 120.0, 'stock': 8}
        producto, _ = crear_producto(datos)
        
        producto_actualizado, error = actualizar_stock(producto.id, 15)
        assert producto_actualizado is not None
        assert error is None
        assert producto_actualizado.stock == 15

def test_actualizar_stock_a_cero(app):
    """Prueba actualizar stock a cero"""
    with app.app_context():
        datos = {'nombre': 'Producto', 'precio': 50.0, 'stock': 10}
        producto, _ = crear_producto(datos)
        
        producto_actualizado, error = actualizar_stock(producto.id, 0)
        assert producto_actualizado is not None
        assert producto_actualizado.stock == 0

def test_actualizar_stock_producto_inexistente(app):
    """Prueba actualizar stock de producto inexistente"""
    with app.app_context():
        producto, error = actualizar_stock(9999, 10)
        assert producto is None
        assert error == "Producto no encontrado"

def test_actualizar_stock_negativo_error(app):
    """Prueba que stock negativo retorna error"""
    with app.app_context():
        datos = {'nombre': 'Producto', 'precio': 50.0, 'stock': 10}
        producto, _ = crear_producto(datos)
        
        producto_actualizado, error = actualizar_stock(producto.id, -5)
        assert producto_actualizado is None
        assert "negativo" in error.lower()

def test_eliminar_producto_database(app):
    """Prueba eliminar producto de base de datos"""
    with app.app_context():
        datos = {'nombre': 'RAM', 'precio': 80.0, 'stock': 6}
        producto, _ = crear_producto(datos)
        producto_id = producto.id
        
        exitoso, error = eliminar_producto(producto_id)
        assert exitoso is True
        assert error is None
        
        # Verificar que ya no existe
        producto_eliminado = obtener_producto_por_id(producto_id)
        assert producto_eliminado is None

def test_eliminar_producto_inexistente(app):
    """Prueba eliminar producto inexistente"""
    with app.app_context():
        exitoso, error = eliminar_producto(9999)
        assert exitoso is False
        assert error == "Producto no encontrado"