```markdown
# 🏪 API de Inventario - Proyecto Completo con Testing

Sistema completo de API REST para gestión de inventario con suite integral de pruebas: unitarias, BDD y carga.

## 🚀 Inicio Rápido

### Prerrequisitos

```bash
# Verificar instalaciones
poetry --version  # Poetry 1.6+
python --version  # Python 3.9+
```

### Instalación

```bash
# Clonar y configurar
git clone 
cd api-inventario

# Instalar dependencias
poetry install

# O usar make
make install
```

### Ejecutar API

```bash
# Método 1: Con Poetry
poetry run python -m inventario.app

# Método 2: Con Make
make run

# La API estará disponible en http://localhost:5000
```

## 📡 Endpoints Disponibles

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/productos` | Crear producto |
| GET | `/api/productos` | Listar productos (paginado) |
| PUT | `/api/productos/{id}/stock` | Actualizar stock |
| DELETE | `/api/productos/{id}` | Eliminar producto |
| GET | `/api/health` | Health check |

### Ejemplos de Uso

```bash
# Crear producto
curl -X POST http://localhost:5000/api/productos \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Laptop","precio":1200,"stock":5}'

# Listar productos
curl http://localhost:5000/api/productos?pagina=1&por_pagina=10

# Actualizar stock
curl -X PUT http://localhost:5000/api/productos/1/stock \
  -H "Content-Type: application/json" \
  -d '{"stock":20}'

# Eliminar producto
curl -X DELETE http://localhost:5000/api/productos/1
```

### Anexos de cobertura test
<img width="601" height="301" alt="image" src="https://github.com/user-attachments/assets/c4558ace-f50c-4f76-92e3-38a22aaeac3c" />

### Anexos de cobertura Behave Test Report
<img width="1850" height="964" alt="image" src="https://github.com/user-attachments/assets/eb16364b-7642-46d5-a044-09cf2c489df5" />

### Anexos de Locust
<img width="1845" height="806" alt="image" src="https://github.com/user-attachments/assets/34f0cd3b-2034-4e26-91a5-d5d532cb5434" />


1. Arquitectura del Sistema
1.1 Arquitectura General
El sistema implementa una arquitectura de 3 capas siguiendo principios de diseño SOLID y separación de responsabilidades:
┌─────────────────────────────────────────┐
│         Capa de Presentación            │
│    (Flask Routes - API REST)            │
├─────────────────────────────────────────┤
│         Capa de Lógica de Negocio       │
│    (Database Layer - Validaciones)      │
├─────────────────────────────────────────┤
│         Capa de Persistencia            │
│    (SQLAlchemy - SQLite)                │
└─────────────────────────────────────────┘
1.2 Arquitectura Flask
1.2.1 Patrón Application Factory
pythondef crear_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
    
    if config:
        app.config.update(config)
    
    # Inicializar extensiones
    CORS(app)
    init_db(app)
    
    # Registrar blueprints
    app.register_blueprint(api)
    
    return app
Ventajas:

Testing simplificado con configuraciones diferentes
Múltiples instancias de la app (desarrollo, producción, testing)
Inyección de dependencias facilitada

1.2.2 Blueprints y Modularización
pythonapi = Blueprint('api', __name__, url_prefix='/api')

@api.route('/productos', methods=['POST'])
def crear_producto_endpoint():
    # Lógica del endpoint
Beneficios:

Organización modular del código
Reutilización de rutas
Escalabilidad para microservicios

1.2.3 Capa de Datos (Repository Pattern)
python# database.py - Abstracción de operaciones CRUD
def crear_producto(datos):
    producto = Producto(**datos)
    errores = producto.validar()
    if errores:
        return None, errores
    db.session.add(producto)
    db.session.commit()
    return producto, None
Ventajas:

Desacoplamiento de la lógica de persistencia
Testing simplificado con mocks
Cambio de ORM sin afectar lógica de negocio

1.3 Modelo de Datos
sqlCREATE TABLE productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    precio FLOAT NOT NULL CHECK(precio >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK(stock >= 0),
    fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP
);
Validaciones implementadas:

Nombre obligatorio y no vacío
Precio no negativo
Stock no negativo
Timestamps automáticos

1.4 Flujo de Datos
Cliente HTTP
    ↓
Flask Route (routes.py)
    ↓
Validación de entrada
    ↓
Database Layer (database.py)
    ↓
Modelo SQLAlchemy (models.py)
    ↓
Base de datos SQLite
    ↓
Respuesta JSON

2. Pipeline CI/CD
2.1 Configuración de GitHub Actions
yaml# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH
    
    - name: Install Dependencies
      run: poetry install
    
    - name: Run Tests
      run: poetry run pytest --cov=inventario --cov-report=xml
    
    - name: Upload Coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
    
    - name: Run BDD Tests
      run: poetry run behave
    
    - name: Security Scan
      run: poetry run bandit -r inventario/
    
    - name: Code Quality
      run: poetry run flake8 inventario/ --max-line-length=120

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: Deploy to Production
      run: echo "Deploying to production server"
2.2 Etapas del Pipeline

Build: Instalación de dependencias con Poetry
Test: Ejecución de pruebas unitarias y BDD
Quality: Análisis de cobertura y calidad de código
Security: Escaneo de vulnerabilidades con Bandit
Deploy: Despliegue automático a producción

2.3 Estrategia de Branching
main (producción)
  ↑
develop (desarrollo)
  ↑
feature/xxx (funcionalidades)
Reglas:

main: Solo código probado y aprobado
PR requiere: Tests pasando + Cobertura >85% + Code review
Deploy automático solo desde main

2.4 Ambientes
AmbienteBranchDatabaseURLDesarrollodevelopSQLite (local)localhost:5000StagingstagingPostgreSQLstaging.api.comProducciónmainPostgreSQLapi.inventario.com
