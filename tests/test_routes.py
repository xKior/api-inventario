import pytest
import json

def test_crear_producto_exitoso(client):
    """Prueba crear producto con datos válidos"""
    datos = {
        'nombre': 'Teclado',
        'precio': 75.50,
        'stock': 20
    }
    
    response = client.post('/api/productos',
                          data=json.dumps(datos),
                          content_type='application/json')
    
    assert response.status_code == 201
    data = response.get_json()
    assert data['mensaje'] == 'Producto creado exitosamente'
    assert data['producto']['nombre'] == 'Teclado'

def test_crear_producto_sin_datos(client):
    """Prueba crear producto sin datos JSON"""
    response = client.post('/api/productos', content_type='application/json')
    assert response.status_code == 400

def test_crear_producto_nombre_vacio(client):
    """Prueba crear producto con nombre vacío"""
    datos = {'nombre': '', 'precio': 100, 'stock': 10}
    response = client.post('/api/productos',
                          data=json.dumps(datos),
                          content_type='application/json')
    assert response.status_code == 400

def test_crear_producto_precio_invalido(client):
    """Prueba crear producto con precio negativo"""
    datos = {'nombre': 'Producto', 'precio': -50, 'stock': 10}
    response = client.post('/api/productos',
                          data=json.dumps(datos),
                          content_type='application/json')
    assert response.status_code == 400

def test_listar_productos(client):
    """Prueba listar productos con paginación"""
    # Crear productos de prueba
    for i in range(5):
        datos = {'nombre': f'Producto {i}', 'precio': 10.0 * (i+1), 'stock': i}
        client.post('/api/productos',
                   data=json.dumps(datos),
                   content_type='application/json')
    
    response = client.get('/api/productos?pagina=1&por_pagina=10')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['productos']) == 5
    assert data['total'] == 5

def test_listar_productos_sin_parametros(client):
    """Prueba listar productos sin parámetros (usa defaults)"""
    datos = {'nombre': 'Producto Default', 'precio': 50, 'stock': 5}
    client.post('/api/productos',
               data=json.dumps(datos),
               content_type='application/json')
    
    response = client.get('/api/productos')
    assert response.status_code == 200
    data = response.get_json()
    assert 'productos' in data
    assert data['pagina'] == 1

def test_listar_productos_pagina_invalida(client):
    """Prueba listar con página inválida"""
    response = client.get('/api/productos?pagina=0')
    assert response.status_code == 400

def test_listar_productos_por_pagina_invalido(client):
    """Prueba listar con por_pagina fuera de rango"""
    response = client.get('/api/productos?por_pagina=200')
    assert response.status_code == 400

def test_eliminar_producto_inexistente(client):
    """Prueba eliminar producto que no existe"""
    response = client.delete('/api/productos/9999')
    assert response.status_code == 404

def test_health_check(client):
    """Prueba endpoint de health check"""
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.get_json()['status'] == 'ok'
    
def test_crear_producto_sin_json(client):
    """Prueba crear producto sin cuerpo JSON"""
    response = client.post('/api/productos')
    assert response.status_code == 400
    data = response.get_json()
    assert 'Datos JSON requeridos' in data['error']


def test_actualizar_stock_exitoso(client):
    """Prueba actualizar stock de un producto existente"""
    # Crear producto
    datos = {'nombre': 'Mouse', 'precio': 25, 'stock': 10}
    res = client.post('/api/productos', data=json.dumps(datos), content_type='application/json')
    producto_id = res.get_json()['producto']['id']

    # Actualizar stock
    nuevo_stock = {'stock': 50}
    response = client.put(f'/api/productos/{producto_id}/stock',
                          data=json.dumps(nuevo_stock),
                          content_type='application/json')

    assert response.status_code == 200
    data = response.get_json()
    assert data['mensaje'] == 'Stock actualizado exitosamente'
    assert data['producto']['stock'] == 50


def test_actualizar_stock_invalido(client):
    """Prueba actualizar stock con valor no numérico"""
    datos = {'nombre': 'Pantalla', 'precio': 300, 'stock': 5}
    res = client.post('/api/productos', data=json.dumps(datos), content_type='application/json')
    producto_id = res.get_json()['producto']['id']

    response = client.put(f'/api/productos/{producto_id}/stock',
                          data=json.dumps({'stock': 'abc'}),
                          content_type='application/json')

    assert response.status_code == 400
    assert 'El stock debe ser un número entero' in response.get_json()['error']


def test_actualizar_stock_faltante(client):
    """Prueba actualizar stock sin campo 'stock' en el JSON"""
    datos = {'nombre': 'Tablet', 'precio': 200, 'stock': 15}
    res = client.post('/api/productos', data=json.dumps(datos), content_type='application/json')
    producto_id = res.get_json()['producto']['id']

    response = client.put(f'/api/productos/{producto_id}/stock',
                          data=json.dumps({'cantidad': 99}),
                          content_type='application/json')

    assert response.status_code == 400
    assert 'Campo stock requerido' in response.get_json()['error']


def test_eliminar_producto_exitoso(client):
    """Prueba eliminar producto existente"""
    datos = {'nombre': 'Silla', 'precio': 100, 'stock': 8}
    res = client.post('/api/productos', data=json.dumps(datos), content_type='application/json')
    producto_id = res.get_json()['producto']['id']

    response = client.delete(f'/api/productos/{producto_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['mensaje'] == 'Producto eliminado exitosamente'
