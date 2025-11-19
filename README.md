# Inventario Abastos — Documentación y Arquitectura

Este README describe la arquitectura del proyecto, la función de cada archivo existente y, cuando corresponde, la función y salida esperada de los métodos implementados.

Estructura (idea base que usas)
--------------------------------
```
inventario_abastos/
│
├── controllers/
│   ├── inventario.py
│   ├── pedidos.py
│
├── models/
│   ├── producto.py
│   ├── proveedor.py
│
├── routes/
│   ├── producto_routes.py
│   ├── pedido_routes.py
│
├── services/
│   ├── alertas.py
│   ├── notificaciones.py
│
├── utilidades/
│   ├── config.py
│   ├── app.py
│
└── database/
    └── db.py
```

Resumen general
----------------
- `app.py` (en `utilidades/`): punto de entrada; crea la app Flask, carga la configuración y registra blueprints y jobs.
- `database/db.py`: instancia y helpers de SQLAlchemy (`db`, `init_db(app)`).
- `models/`: definiciones ORM (Producto, Proveedor, potencialmente Lote y PedidoItem si se añaden).
- `controllers/`: lógica de negocio (comprobaciones, generación de pedidos).
- `routes/`: blueprints con endpoints REST.
- `services/`: funcionalidades auxiliares (alertas, notificaciones por correo/SMS).

Detalles por archivo (función y salida esperada)
------------------------------------------------

1) controllers/inventario.py
----------------------------
Este archivo ya contiene implementaciones. Funciones principales:

- `check_low_stock() -> List[Dict]`
  - Qué hace: consulta productos cuya `cantidad <= cantidad_minima`.
  - Entrada: ninguna (usa modelo `Producto` desde la BD).
  - Salida esperada: lista de diccionarios, cada uno con los campos del producto. Ejemplo:
    ```json
    [
      {"id": 1, "nombre": "Leche", "codigo": "L001", "cantidad": 3, "cantidad_minima": 5, "id_proveedor": 2},
      ...
    ]
    ```
  - Errores comunes: si `Producto` no existe o `db` no está inicializado, la consulta fallará.

- `check_expiring_items(days: int = 7) -> List[Dict]`
  - Qué hace: busca `Lote` con `fecha_caducidad` dentro de los próximos `days` días.
  - Entrada: opcional `days` (por defecto 7).
  - Salida esperada: lista de diccionarios con información del lote y nombre del producto, p.ej:
    ```json
    [
      {"id_lote": 10, "id_producto": 3, "producto_nombre": "Yogurt", "cantidad_lote": 20, "fecha_caducidad": "2025-11-25T00:00:00"},
      ...
    ]
    ```

- `calculate_suggested_order_qty(producto: Producto, factor: int = 2) -> int`
  - Qué hace: calcula una cantidad sugerida para reponer según la regla:
    `objetivo = cantidad_minima * factor` y `sugerida = max(objetivo - cantidad_actual, cantidad_minima)`.
  - Entrada: instancia de `Producto` (de la BD) y `factor` (int).
  - Salida esperada: entero (cantidad sugerida).
  - Ejemplo: producto.cantidad=3, producto.cantidad_minima=5, factor=2 → objetivo=10 → sugerida=10-3=7.

Notas: para que estas funciones funcionen debes tener implementados los modelos `Producto` y `Lote` con los campos usados: `id, nombre, codigo, cantidad, cantidad_minima, id_proveedor` y `id, id_producto, cantidad, fecha_caducidad`.

2) controllers/pedidos.py
-------------------------
Actualmente vacío. Funciones esperadas a implementar:

- `generate_suggested_orders(productos_bajos: List[Producto]) -> Dict[int, List[Dict]]`
  - Qué hace: agrupa productos bajos por `id_proveedor` y calcula `cantidad_sugerida` por producto.
  - Salida esperada: dict donde la clave es `id_proveedor` y el valor es lista de items `{id_producto, cantidad_sugerida}`.

- `confirm_order(pedido_data: Dict) -> Pedido`
  - Qué hace: crea en BD un `Pedido` y sus `PedidoItem` a partir de `pedido_data`.
  - Entrada: `{'id_proveedor': X, 'items': [{'id_producto': Y, 'cantidad': Z}, ...]}`.
  - Salida esperada: objeto `Pedido` creado (o dict serializado) con `id` y estado `pendiente`.

3) models/producto.py
---------------------
Archivo vacío; se espera un modelo SQLAlchemy similar a:

```python
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(50), unique=True)
    cantidad = db.Column(db.Integer, default=0)
    cantidad_minima = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Float)
    id_proveedor = db.Column(db.Integer, db.ForeignKey('proveedores.id'))
    def to_dict(self): ...
```

Salida esperada al serializar (ejemplo):
```json
{"id":1,"nombre":"Leche","codigo":"L001","cantidad":3,"cantidad_minima":5,"precio_unitario":1.50,"id_proveedor":2}
```

4) models/proveedor.py
-----------------------
Se espera un modelo `Proveedor` con campos: `id, nombre, ruc, email, telefono, lead_time_days`.

5) routes/producto_routes.py y routes/pedido_routes.py
---------------------------------------------------
Archivos vacíos; rutas recomendadas:

- `producto_routes.py`:
  - `GET /api/productos` → lista de productos (usar `Producto.query.all()` y serializar con `to_dict()`).
  - `POST /api/productos` → crear producto (recibir JSON y guardarlo).
  - `PUT /api/productos/<id>` → actualizar.
  - `DELETE /api/productos/<id>` → eliminar.

- `pedido_routes.py`:
  - `GET /api/pedidos/sugeridos` → devolver pedidos sugeridos (usar `controllers.generate_suggested_orders`).
  - `POST /api/pedidos` → confirmar pedido (usar `controllers.confirm_order`).

6) services/alertas.py
----------------------
Vacío. Función esperada:
- `crear_alerta_bajo_stock(producto_dict)` → registra alerta en BD o log y devuelve `True`/`False`.

7) services/notificaciones.py
-----------------------------
Vacío. Funciones esperadas:
- `send_email(to, subject, body)` → envía correo; devuelve `True` si se envía.
- `send_sms(to, message)` → opcional con Twilio.

8) utilidades/config.py y utilidades/app.py
-----------------------------------------
- `utilidades/config.py`: variables de configuración (URI de BD, credenciales SMTP, parámetros de scheduler).
- `utilidades/app.py`: wrapper para crear la app Flask si decides mover `create_app()` fuera de la raíz.

9) database/db.py
-----------------
Vacío. Debe contener al menos:

```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
```

Ejecutar la aplicación (pasos rápidos)
------------------------------------
1) Crear y activar entorno virtual (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2) Instalar dependencias básicas:

```powershell
pip install flask flask-sqlalchemy apscheduler python-dotenv
```

3) Ejecutar la app (desde la raíz del repositorio, para que imports relativos funcionen):

```powershell
# Ejecutar como paquete para evitar problemas con imports relativos
python -m inventario_abastos.utilidades.app
```

O, si `utilidades/app.py` define `if __name__ == '__main__': create_app().run()`, puedes:

```powershell
cd inventario_abastos
python utilidades/app.py
```

Notas finales y recomendaciones
-------------------------------
- Mantén consistentes los nombres de clases (ej. `Proveedor`) y de funciones exportadas.
- Añade `__init__.py` vacíos en directorios si usas imports relativos y ejecuta como paquete.
- Implementa primero `models` y `database/db.py` para que las funciones del controlador funcionen.
- Añade logging y pruebas unitarias para `controllers`.

Si quieres, puedo: (elige una)
- A) Crear implementaciones mínimas de `models/producto.py`, `models/proveedor.py` y `database/db.py` para que `controllers/inventario.py` funcione ahora.
- B) Generar los `routes` básicos para productos y pedidos.
- C) Implementar `controllers/pedidos.py` que genere pedidos sugeridos.

Dime cuál prefieres y lo implemento.
