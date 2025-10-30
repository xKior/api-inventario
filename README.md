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