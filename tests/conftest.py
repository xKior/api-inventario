import pytest
from inventario.app import crear_app
from inventario.models import db

@pytest.fixture(scope='function')
def app():
    """Fixture de aplicación Flask para testing"""
    config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    
    app = crear_app(config)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='function')
def client(app):
    """Cliente de pruebas Flask"""
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    """CLI runner para testing"""
    return app.test_cli_runner()

@pytest.fixture
def sample_producto(app):
    """Fixture para crear un producto de ejemplo"""
    from inventario.models import Producto
    with app.app_context():
        producto = Producto(nombre="Producto Test", precio=100.0, stock=10)
        db.session.add(producto)
        db.session.commit()
        # Refrescar para obtener el ID
        db.session.refresh(producto)
        producto_id = producto.id
        yield producto_id