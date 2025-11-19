# Inventario Abastos — README

Resumen breve
---------------
Aplicación para gestionar inventario, proveedores y pedidos en una tienda de abarrotes. Facilita la detección de productos con bajo stock, control de caducidades y la generación de pedidos sugeridos a proveedores.

Estado del código
------------------
En el repositorio hay la estructura básica (módulos y archivos), algunos archivos están como plantillas y requieren implementación de lógica (models, controllers, routes, services). Este README explica qué hace cada archivo y cómo empezar.

## Estructura y propósito de archivos

```
inventario_abastos/
- app.py                    : Punto de entrada. Debe crear la app Flask, cargar configuración, inicializar la BD y registrar rutas y jobs.
- config.py                 : Variables de configuración (URI de BD, secretos, configuración de correo).
- database.py/db.py         : Inicialización de SQLAlchemy y helpers init_db(app)/drop_all_tables(app).

models/
- __init__.py               : Importa y expone los modelos (actualmente vacío; debería exportar Producto, Proveedor, etc.).
- producto.py               : Modelo Producto (nombre, codigo, cantidad, cantidad_minima, precio_unitario, id_proveedor).
- proveedor.py              : Modelo Proveedor (nombre, contacto, lead_time_days).

routes/
- producto_routes.py        : Endpoints CRUD para productos.
- pedido_routes.py          : Endpoints para pedidos (crear/confirmar/listar sugeridos).

controllers/
- inventario.py             : Lógica para revisar stock y caducidades (jobs programados).
- pedidos.py                : Generar pedidos sugeridos, confirmar pedidos.

services/
- alertas.py                : Funciones para crear/registrar alertas internas (bajo stock, caducidad).
- notificaciones.py         : Funciones para enviar notificaciones (SMTP o impresión en consola).

utilidades/
- helpers.py                : Utilidades y funciones auxiliares.
```

## Cómo ejecutar (rápido)

1. Crear y activar entorno virtual (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Instalar dependencias mínimas:

```powershell
pip install flask flask-sqlalchemy apscheduler python-dotenv
```

3. Ejecutar la aplicación (desde la carpeta del proyecto):

```powershell
cd inventario_abastos
python app.py
```

4. Verificar en el navegador: `http://127.0.0.1:5000/` (si `app.py` expone ruta de bienvenida).

## Notas importantes

- Muchos archivos están creados pero vacíos (models, controllers, routes, services). Debes implementar los modelos y la lógica de cada módulo para que la aplicación funcione.
- `app.py` es el entrypoint: desde allí se carga todo. Si no existe, crea una `create_app()` que inicialice `db` y registre blueprints.

## Endpoints recomendados (sugerencia)

- `GET /api/productos` — listar productos
- `POST /api/productos` — crear producto
- `PUT /api/productos/<id>` — actualizar producto
- `GET /api/pedidos/sugeridos` — ver pedidos sugeridos por el sistema
- `POST /api/pedidos` — confirmar un pedido

## Siguientes pasos sugeridos

1. Implementar modelos (`models/producto.py`, `models/proveedor.py`).
2. Implementar routes CRUD y registrarlas en `app.py`.
3. Implementar `controllers/inventario.py` con `check_low_stock()` y `check_expiring_items()`.
4. Añadir un job con `APScheduler` en `app.py` para ejecutar esas comprobaciones periódicamente.
5. Implementar `services/notificaciones.py` para enviar correos o SMS (opcional).

---

Si quieres, implemento ahora uno de los siguientes: modelos + `app.py` mínimo, rutas CRUD básicas, o un job POC con `APScheduler` que muestre alertas en consola.
