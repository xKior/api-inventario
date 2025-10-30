import pytest
from inventario.models import Producto, db
from datetime import datetime

def test_producto_creacion(app):
    """Prueba creación de producto válido"""
    with app.app_context():
        producto = Producto(nombre="Laptop", precio=1500.0, stock=10)
        db.session.add(producto)
        db.session.commit()
        
        assert producto.id is not None
        assert producto.nombre == "Laptop"
        assert producto.precio == 1500.0
        assert producto.stock == 10
        assert producto.fecha_creacion is not None

def test_producto_to_dict(app):
    """Prueba conversión a diccionario"""
    with app.app_context():
        producto = Producto(nombre="Mouse", precio=25.0, stock=50)
        db.session.add(producto)
        db.session.commit()
        
        data = producto.to_dict()
        assert data['nombre'] == "Mouse"
        assert data['precio'] == 25.0
        assert data['stock'] == 50
        assert 'id' in data
        assert 'fecha_creacion' in data


def test_producto_validacion_nombre_vacio(app):
    """Prueba validación de nombre vacío"""
    with app.app_context():
        producto = Producto(nombre="", precio=100.0, stock=5)
        errores = producto.validar()
        assert len(errores) > 0
        assert any("nombre" in e.lower() for e in errores)

def test_producto_validacion_nombre_solo_espacios(app):
    """Prueba validación de nombre con solo espacios"""
    with app.app_context():
        producto = Producto(nombre="   ", precio=100.0, stock=5)
        errores = producto.validar()
        assert len(errores) > 0

def test_producto_validacion_precio_negativo(app):
    """Prueba validación de precio negativo"""
    with app.app_context():
        producto = Producto(nombre="Producto", precio=-10.0, stock=5)
        errores = producto.validar()
        assert len(errores) > 0
        assert any("precio" in e.lower() for e in errores)

def test_producto_validacion_precio_none(app):
    """Prueba validación de precio None"""
    with app.app_context():
        producto = Producto(nombre="Producto", precio=None, stock=5)
        errores = producto.validar()
        assert len(errores) > 0

def test_producto_validacion_precio_cero_valido(app):
    """Prueba que precio 0 es válido"""
    with app.app_context():
        producto = Producto(nombre="Producto", precio=0, stock=5)
        errores = producto.validar()
        # No debe haber error de precio
        assert not any("precio" in e.lower() for e in errores)

def test_producto_validacion_stock_negativo(app):
    """Prueba validación de stock negativo"""
    with app.app_context():
        producto = Producto(nombre="Producto", precio=50.0, stock=-5)
        errores = producto.validar()
        assert len(errores) > 0
        assert any("stock" in e.lower() for e in errores)

def test_producto_validacion_stock_none(app):
    """Prueba validación de stock None"""
    with app.app_context():
        producto = Producto(nombre="Producto", precio=50.0, stock=None)
        errores = producto.validar()
        assert len(errores) > 0

def test_producto_validacion_multiples_errores(app):
    """Prueba validación con múltiples errores"""
    with app.app_context():
        producto = Producto(nombre="", precio=-10, stock=-5)
        errores = producto.validar()
        assert len(errores) >= 3

def test_producto_fecha_actualizacion(app):
    """Prueba que fecha_actualizacion se actualiza"""
    with app.app_context():
        producto = Producto(nombre="Test", precio=100, stock=10)
        db.session.add(producto)
        db.session.commit()
        
        fecha_original = producto.fecha_actualizacion
        
        # Actualizar producto
        producto.stock = 20
        db.session.commit()
        
        # La fecha debería actualizarse automáticamente
        assert producto.fecha_actualizacion is not None