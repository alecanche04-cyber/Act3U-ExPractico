# Inventario Abastos — Documentación y Arquitectura

Este README describe la arquitectura del proyecto, la función de cada archivo existente y, cuando corresponde, la función y salida esperada de los métodos implementados.

--------------------------------

inventario_abastos/
│
├── controllers/
│   ├── __init__.py
│   ├── inventario.py
│   ├── pedidos.py
│
├── models/
│   ├── __init__.py
│   ├── lote.py
│   ├── producto.py
│   ├── proveedor.py
│
├── routes/
│   ├── __init__.py
│   ├── producto_routes.py
│   ├── pedido_routes.py
│
├── services/
│   ├── __init__.py
│   ├── alertas.py
│   ├── notificaciones.py
│
├── utilidades/
│   ├──helpers.py
│
└── database/
│     └── db.py
│
├── config.py
└── Main.py

----------------------------------------------------------------------------------------

# Inventario Abastos — Resumen, arquitectura y uso rápido

## 1. Propósito
Aplicación para una tienda de abarrotes que automatiza:  
- Detección de productos con **stock bajo**.  
- Detección de **lotes próximos a caducar**.  
- Generación de **pedidos sugeridos a proveedores**.  
- Envío de **notificaciones** (por consola o correo) para tomar acciones preventivas.  

----------------------------------------------------------------------------------------

## 2. Problema que resuelve
- Evita llevar el control del inventario de forma manual y los errores por cálculos “a ojo”.  
- Centraliza la creación de pedidos y sugiere cantidades correctas.  
- Envía alertas para prevenir faltantes y pérdidas por caducidad.  

----------------------------------------------------------------------------------------

## 3. Cómo funciona (resumen)
- Tareas periódicas (planificador/scheduler) ejecutan comprobaciones:  
  - **verificar_bajo_stock()**: - muestra una lista de productos cuya cantidad es menor o igual a la cantidad mínima permitida.
  -**verificar_items_por_caducar(dias)**:- muestra una lista de lotes cuya fecha de caducidad es menor o igual a hoy + días.
  _**calcular_cantidad_sugerida_orde()**:Calcula cantidad sugerida para reponer un producto.
  
	# Regla simple (configurable):
  - **generar_ordenes_sugeridas()**: agrupa productos bajos por proveedor y propone cantidades.  
- **Persistencia**: archivos JSON en `data/` (capa `database/db.py` con funciones add/get_all/update/delete).  
- **Modelos**: dataclasses con métodos `to_dict` y `from_dict` para `Producto`, `Lote`, `Proveedor`.  
- **API / rutas**: en `routes/` se exponen endpoints CRUD para productos y pedidos.  
- **Servicios**: `services/alertas.py` y `services/notificaciones.py` construyen y envían alertas.  

----------------------------------------------------------------------------------------

## 4. Estructura de carpetas
- **controllers/**  
  - `inventario.py` — comprobaciones y cálculos (stock bajo, caducidad, cantidad sugerida).  
  - `pedidos.py` — generar sugerencias, crear/guardar/confirmar pedidos.  
- **models/**  
  - `producto.py` — dataclass Producto (to_dict/from_dict, actualizar stock, necesita reorden).  
  - `lote.py` — dataclass Lote (to_dict/from_dict, parsear fecha).  
  - `proveedor.py` — dataclass Proveedor (to_dict/from_dict).  
- **routes/**  
  - `producto_routes.py` — CRUD de productos.  
  - `pedido_routes.py` — endpoints de pedidos.  
- **services/**  
  - `alertas.py` — reglas para construir alertas.  
  - `notificaciones.py` — envío de alertas (consola/SMTP/Twilio opcional).  
- **utilidades/**  
  - `config.py` — variables y parámetros (DATA_DIR, tablas JSON, scheduler).  
  - `app.py` — punto de arranque, registra blueprints y scheduler.  
- **database/**  
  - `db.py` — capa JSON: get_all/add/update/delete.  

----------------------------------------------------------------------------------------

## 5. Métodos clave y salida esperada

- **verificar_stock_bajo()**  
  → Devuelve una lista de diccionarios con:  
  `{id, nombre, codigo, cantidad, cantidad_minima, id_proveedor}`  
- **verificar_productos_por_caducar(dias=7)**  
  → Devuelve una lista de diccionarios con:  
  `{id_lote, id_producto, nombre_producto, cantidad_lote, fecha_caducidad}`  

- **calcular_cantidad_sugerida(producto, factor=2)**  
  → Devuelve un número sugerido a pedir.  

- **generar_ordenes_sugeridas(productos_bajos, factor=2)**  
  → Devuelve un diccionario con:  
  `{id_proveedor, lista_productos_sugeridos}`  

- **crear_diccionario_orden(id_proveedor, items, numero_pedido=None)**  
  → Devuelve un diccionario con el pedido:  
  `{fecha, items, total}`  

- **guardar_orden(orden_dict)**  
  → Devuelve la orden guardada con su `id`.  

- **confirmar_orden(id_orden)**  
  → Devuelve la orden confirmada o `None`.  

----------------------------------------------------------------------------------------

En resumen: este proyecto es un **sistema de inventario para abarrotes** que automatiza el control de stock, caducidad y pedidos, usando archivos JSON como base de datos y enviando alertas por consola o correo.  


