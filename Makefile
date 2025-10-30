.PHONY: install test coverage behave locust clean run all

# Instalar dependencias
install:
	poetry install

# Ejecutar todas las pruebas
test:
	poetry run pytest -v

# Ejecutar pruebas con cobertura
coverage:
	poetry run pytest --cov=inventario --cov-report=html --cov-report=term-missing
	@echo "\n✅ Reporte de cobertura generado en htmlcov/index.html"

# Ejecutar pruebas BDD con Behave
behave:
	poetry run behave --format=pretty
	poetry run behave --format=html --outfile=behave-report.html
	@echo "\n✅ Reporte Behave generado en behave-report.html"

# Ejecutar servidor para pruebas de carga
run:
	poetry run python -m inventario.app

# Ejecutar Locust (interfaz web)
locust:
	@echo "🚀 Iniciando Locust en http://localhost:8089"
	@echo "📝 Configuración sugerida:"
	@echo "   - Usuarios: 50"
	@echo "   - Spawn rate: 2 usuarios/segundo"
	@echo "   - Host: http://localhost:5000"
	@echo "   - Duración: 5 minutos (300 segundos)"
	poetry run locust -f locustfile.py --host=http://localhost:5000

# Ejecutar Locust en modo headless (sin interfaz)
locust-headless:
	poetry run locust -f locustfile.py --host=http://localhost:5000 \
		--users 50 --spawn-rate 2 --run-time 300s --headless \
		--html=locust-report.html
	@echo "\n✅ Reporte Locust generado en locust-report.html"

# Limpiar archivos generados
clean:
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .coverage
	rm -f behave-report.html
	rm -f locust-report.html
	rm -f inventario.db
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Ejecutar pipeline completo
all: clean install coverage behave
	@echo "\n🎉 ¡Pipeline completo ejecutado exitosamente!"
	@echo "📊 Revisa los reportes:"
	@echo "   - Coverage: htmlcov/index.html"
	@echo "   - Behave: behave-report.html"
	@echo "\n⚠️  Para pruebas de carga, ejecuta en otra terminal:"
	@echo "   make run     # Inicia el servidor"
	@echo "   make locust  # Inicia Locust"

# Verificar requisitos mínimos
check:
	@echo "🔍 Verificando instalación..."
	@poetry --version || echo "❌ Poetry no instalado"
	@python --version || echo "❌ Python no instalado"
	@echo "✅ Verificación completa"

# Generar requirements.txt para compatibilidad
requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
	@echo "✅ requirements.txt generado"