# language: es
Característica: Gestión de Inventario de Productos
  Como usuario de la API
  Quiero gestionar productos en el inventario
  Para mantener un registro actualizado

  Escenario: Crear un producto exitosamente
    Dado que tengo los datos de un nuevo producto
      | nombre    | precio | stock |
      | Laptop HP | 1200   | 5     |
    Cuando envío una solicitud POST a "/api/productos"
    Entonces recibo un código de estado 201
    Y la respuesta contiene el producto creado con nombre "Laptop HP"

  Escenario: Listar productos con paginación
    Dado que existen 15 productos en el inventario
    Cuando envío una solicitud GET a "/api/productos?pagina=1&por_pagina=10"
    Entonces recibo un código de estado 200
    Y la respuesta contiene 10 productos
    Y el total de productos es 15

  Escenario: Actualizar stock de un producto
    Dado que existe un producto con ID 1 y stock de 10
    Cuando envío una solicitud PUT a "/api/productos/1/stock" con stock 25
    Entonces recibo un código de estado 200
    Y el producto tiene un stock de 25

  Escenario: Eliminar un producto existente
    Dado que existe un producto con ID 2
    Cuando envío una solicitud DELETE a "/api/productos/2"
    Entonces recibo un código de estado 200
    Y el producto ya no existe en el inventario

  Escenario: Intentar crear producto con datos inválidos
    Dado que tengo datos inválidos para un producto
      | nombre | precio | stock |
      |        | -50    | -10   |
    Cuando envío una solicitud POST a "/api/productos"
    Entonces recibo un código de estado 400
    Y la respuesta contiene errores de validación