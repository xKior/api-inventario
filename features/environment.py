from inventario.app import crear_app
from inventario.models import db

def before_all(context):
    """Configuración inicial antes de todas las pruebas"""
    config = {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    }
    context.app = crear_app(config)
    context.client = context.app.test_client()

def before_scenario(context, scenario):
    """Configuración antes de cada escenario"""
    with context.app.app_context():
        db.create_all()

def after_scenario(context, scenario):
    """Limpieza después de cada escenario"""
    with context.app.app_context():
        db.session.remove()
        db.drop_all()