from flask import Flask
from flask_cors import CORS
from inventario.models import db
from inventario.routes import api
from inventario.database import init_db

def crear_app(config=None):
    """Factory para crear la aplicación Flask"""
    app = Flask(__name__)
    
    # Configuración por defecto
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JSON_AS_ASCII'] = False
    
    # Aplicar configuración personalizada
    if config:
        app.config.update(config)
    
    # Inicializar extensiones
    CORS(app)
    init_db(app)
    
    # Registrar blueprints
    app.register_blueprint(api)
    
    return app

def main():
    """Función principal para ejecutar la aplicación"""
    app = crear_app()
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()