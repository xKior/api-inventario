from flask import Blueprint, request, jsonify
from inventario.database import (
    obtener_productos, crear_producto, obtener_producto_por_id,
    actualizar_stock, eliminar_producto
)

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/productos', methods=['POST'])
def crear_producto_endpoint():
    """POST /api/productos - Crear producto"""
    datos = request.get_json()
    
    if not datos:
        return jsonify({'error': 'Datos JSON requeridos'}), 400
    
    producto, errores = crear_producto(datos)
    
    if errores:
        return jsonify({'error': 'Validación fallida', 'detalles': errores}), 400
    
    return jsonify({
        'mensaje': 'Producto creado exitosamente',
        'producto': producto.to_dict()
    }), 201

@api.route('/productos', methods=['GET'])
def listar_productos():
    """GET /api/productos - Listar productos con paginación"""
    pagina = request.args.get('pagina', 1, type=int)
    por_pagina = request.args.get('por_pagina', 10, type=int)
    
    if pagina < 1:
        return jsonify({'error': 'La página debe ser mayor a 0'}), 400
    
    if por_pagina < 1 or por_pagina > 100:
        return jsonify({'error': 'por_pagina debe estar entre 1 y 100'}), 400
    
    paginacion = obtener_productos(pagina, por_pagina)
    
    return jsonify({
        'productos': [p.to_dict() for p in paginacion.items],
        'total': paginacion.total,
        'pagina': paginacion.page,
        'por_pagina': paginacion.per_page,
        'total_paginas': paginacion.pages
    }), 200

@api.route('/productos/<int:producto_id>/stock', methods=['PUT'])
def actualizar_stock_endpoint(producto_id):
    """PUT /api/productos/{id}/stock - Actualizar stock"""
    datos = request.get_json()
    
    if not datos or 'stock' not in datos:
        return jsonify({'error': 'Campo stock requerido'}), 400
    
    nuevo_stock = datos.get('stock')
    
    try:
        nuevo_stock = int(nuevo_stock)
    except (ValueError, TypeError):
        return jsonify({'error': 'El stock debe ser un número entero'}), 400
    
    producto, error = actualizar_stock(producto_id, nuevo_stock)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify({
        'mensaje': 'Stock actualizado exitosamente',
        'producto': producto.to_dict()
    }), 200

@api.route('/productos/<int:producto_id>', methods=['DELETE'])
def eliminar_producto_endpoint(producto_id):
    """DELETE /api/productos/{id} - Eliminar producto"""
    exitoso, error = eliminar_producto(producto_id)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify({'mensaje': 'Producto eliminado exitosamente'}), 200

@api.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check para pruebas"""
    return jsonify({'status': 'ok'}), 200