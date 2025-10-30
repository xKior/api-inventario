from inventario.models import db, Producto

def init_db(app):
    """Inicializar base de datos"""
    db.init_app(app)
    with app.app_context():
        db.create_all()

def obtener_productos(pagina=1, por_pagina=10):
    """Obtener productos con paginación"""
    return Producto.query.paginate(
        page=pagina,
        per_page=por_pagina,
        error_out=False
    )

def crear_producto(datos):
    """Crear nuevo producto"""
    producto = Producto(
        nombre=datos.get('nombre'),
        precio=datos.get('precio'),
        stock=datos.get('stock', 0)
    )
    
    errores = producto.validar()
    if errores:
        return None, errores
    
    db.session.add(producto)
    db.session.commit()
    return producto, None

def obtener_producto_por_id(producto_id):
    """Obtener producto por ID"""
    return Producto.query.get(producto_id)

def actualizar_stock(producto_id, nuevo_stock):
    """Actualizar stock de producto"""
    producto = Producto.query.get(producto_id)
    if not producto:
        return None, "Producto no encontrado"
    
    if nuevo_stock < 0:
        return None, "El stock no puede ser negativo"
    
    producto.stock = nuevo_stock
    db.session.commit()
    return producto, None

def eliminar_producto(producto_id):
    """Eliminar producto"""
    producto = Producto.query.get(producto_id)
    if not producto:
        return False, "Producto no encontrado"
    
    db.session.delete(producto)
    db.session.commit()
    return True, None