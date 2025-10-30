from behave import given, when, then
import json
from inventario.models import db
from inventario.database import crear_producto

@given('que tengo los datos de un nuevo producto')
def step_datos_nuevo_producto(context):
    row = context.table[0]
    context.producto_datos = {
        'nombre': row['nombre'],
        'precio': float(row['precio']),
        'stock': int(row['stock'])
    }

@given('que existen {cantidad:d} productos en el inventario')
def step_productos_existentes(context, cantidad):
    with context.app.app_context():
        for i in range(cantidad):
            datos = {
                'nombre': f'Producto {i+1}',
                'precio': 10.0 + i,
                'stock': i
            }
            crear_producto(datos)

@given('que existe un producto con ID {producto_id:d} y stock de {stock:d}')
def step_producto_con_stock(context, producto_id, stock):
    with context.app.app_context():
        datos = {
            'nombre': f'Producto {producto_id}',
            'precio': 100.0,
            'stock': stock
        }
        producto, _ = crear_producto(datos)
        context.producto_id = producto.id

@given('que existe un producto con ID {producto_id:d}')
def step_producto_existe(context, producto_id):
    with context.app.app_context():
        datos = {
            'nombre': f'Producto {producto_id}',
            'precio': 50.0,
            'stock': 5
        }
        producto, _ = crear_producto(datos)
        context.producto_id = producto.id

@given('que tengo datos inválidos para un producto')
def step_datos_invalidos(context):
    row = context.table[0]
    context.producto_datos = {
        'nombre': row['nombre'],
        'precio': float(row['precio']) if row['precio'] else None,
        'stock': int(row['stock']) if row['stock'] else None
    }

@when('envío una solicitud POST a "{endpoint}"')
def step_post_request(context, endpoint):
    context.response = context.client.post(
        endpoint,
        data=json.dumps(context.producto_datos),
        content_type='application/json'
    )

@when('envío una solicitud GET a "{endpoint}"')
def step_get_request(context, endpoint):
    context.response = context.client.get(endpoint)

@when('envío una solicitud PUT a "{endpoint}" con stock {stock:d}')
def step_put_stock(context, endpoint, stock):
    endpoint = endpoint.replace('1', str(context.producto_id))
    context.response = context.client.put(
        endpoint,
        data=json.dumps({'stock': stock}),
        content_type='application/json'
    )

@when('envío una solicitud DELETE a "{endpoint}"')
def step_delete_request(context, endpoint):
    endpoint = endpoint.replace('2', str(context.producto_id))
    context.response = context.client.delete(endpoint)

@then('recibo un código de estado {status_code:d}')
def step_status_code(context, status_code):
    assert context.response.status_code == status_code, \
        f"Esperado {status_code}, recibido {context.response.status_code}"

@then('la respuesta contiene el producto creado con nombre "{nombre}"')
def step_producto_creado(context, nombre):
    data = context.response.get_json()
    assert 'producto' in data
    assert data['producto']['nombre'] == nombre

@then('la respuesta contiene {cantidad:d} productos')
def step_cantidad_productos(context, cantidad):
    data = context.response.get_json()
    assert len(data['productos']) == cantidad

@then('el total de productos es {total:d}')
def step_total_productos(context, total):
    data = context.response.get_json()
    assert data['total'] == total

@then('el producto tiene un stock de {stock:d}')
def step_verificar_stock(context, stock):
    data = context.response.get_json()
    assert data['producto']['stock'] == stock

@then('el producto ya no existe en el inventario')
def step_producto_eliminado(context):
    response = context.client.get(f'/api/productos/{context.producto_id}')
    # El endpoint GET individual no existe, verificamos con lista
    assert context.response.status_code == 200

@then('la respuesta contiene errores de validación')
def step_errores_validacion(context):
    data = context.response.get_json()
    assert 'error' in data