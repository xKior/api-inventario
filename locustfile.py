from locust import HttpUser, task, between
import json
import random

class InventarioUser(HttpUser):
    """Usuario simulado para pruebas de carga"""
    wait_time = between(1, 3)
    
    def on_start(self):
        """Método ejecutado al inicio para cada usuario"""
        # Verificar que la API está disponible
        response = self.client.get("/api/health")
        if response.status_code != 200:
            print("ERROR: API no disponible")
    
    @task(5)
    def listar_productos(self):
        """Tarea: Listar productos (peso 5)"""
        pagina = random.randint(1, 5)
        with self.client.get(
            f"/api/productos?pagina={pagina}&por_pagina=10",
            catch_response=True,
            name="/api/productos [GET]"
        ) as response:
            if response.status_code == 200:
                data = response.json()
                if 'productos' in data:
                    response.success()
                else:
                    response.failure("No se encontró 'productos' en respuesta")
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(3)
    def crear_producto(self):
        """Tarea: Crear producto (peso 3)"""
        producto_id = random.randint(1000, 9999)
        datos = {
            'nombre': f'Producto Test {producto_id}',
            'precio': round(random.uniform(10.0, 1000.0), 2),
            'stock': random.randint(1, 100)
        }
        
        with self.client.post(
            "/api/productos",
            json=datos,
            catch_response=True,
            name="/api/productos [POST]"
        ) as response:
            if response.status_code == 201:
                data = response.json()
                if 'producto' in data and 'id' in data['producto']:
                    # Guardar ID para otras operaciones
                    self.producto_id = data['producto']['id']
                    response.success()
                else:
                    response.failure("Respuesta inválida")
            else:
                response.failure(f"Status code: {response.status_code}")
    
    @task(2)
    def actualizar_stock(self):
        """Tarea: Actualizar stock (peso 2)"""
        # Primero crear un producto para actualizar
        datos = {
            'nombre': f'Producto Stock {random.randint(1, 999)}',
            'precio': 50.0,
            'stock': 10
        }
        
        response = self.client.post("/api/productos", json=datos)
        
        if response.status_code == 201:
            producto_id = response.json()['producto']['id']
            nuevo_stock = random.randint(0, 200)
            
            with self.client.put(
                f"/api/productos/{producto_id}/stock",
                json={'stock': nuevo_stock},
                catch_response=True,
                name="/api/productos/{id}/stock [PUT]"
            ) as update_response:
                if update_response.status_code == 200:
                    update_response.success()
                else:
                    update_response.failure(f"Status: {update_response.status_code}")
    
    @task(1)
    def eliminar_producto(self):
        """Tarea: Eliminar producto (peso 1)"""
        # Primero crear un producto para eliminar
        datos = {
            'nombre': f'Producto Temp {random.randint(1, 999)}',
            'precio': 25.0,
            'stock': 5
        }
        
        response = self.client.post("/api/productos", json=datos)
        
        if response.status_code == 201:
            producto_id = response.json()['producto']['id']
            
            with self.client.delete(
                f"/api/productos/{producto_id}",
                catch_response=True,
                name="/api/productos/{id} [DELETE]"
            ) as delete_response:
                if delete_response.status_code == 200:
                    delete_response.success()
                else:
                    delete_response.failure(f"Status: {delete_response.status_code}")
    
    @task(1)
    def health_check(self):
        """Tarea: Health check (peso 1)"""
        with self.client.get(
            "/api/health",
            catch_response=True,
            name="/api/health [GET]"
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Status code: {response.status_code}")