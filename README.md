# Inventario Abastos — Documentación Completa

## 1. Propósito General

Sistema web para gestionar el inventario de una tienda de abarrotes, automatizando:
- **Registro de productos** con stock y fechas de caducidad
- **Gestión de proveedores** para reabastecimiento
- **Generación automática de pedidos** cuando el stock es bajo
- **Alertas automáticas** por correo/consola cuando hay faltantes o próximas caducidades

**Problema que resuelve:**
- Evita revisión manual del inventario
- Previene faltantes (pérdida de ventas)
- Evita exceso de stock (pérdida por caducidad)
- Genera pedidos automáticamente según niveles de stock


## 2. Estructura de Carpetas Actual

```
inventario_abastos/
├── app.py                    # Punto de entrada
├── config.py                 # Configuración
├── database.py/
│   └── db.py                 # SQLAlchemy + helpers
├── models/
│   ├── __init__.py
│   ├── producto.py
│   ├── proveedor.py
│   ├── pedido.py
│   ├── pedido_item.py
│   └── lote.py
├── routes/
│   ├── __init__.py
│   ├── producto_routes.py
│   └── pedido_routes.py
├── controllers/
│   ├── __init__.py
│   ├── inventario.py         # Lógica de stock/caducidad
│   └── pedidos.py            # Lógica de pedidos
├── services/
│   ├── __init__.py
│   ├── alertas.py            # Crear alertas
│   └── notificaciones.py      # Enviar notificaciones
└── utilidades/
    └── helpers.py            # Funciones reutilizables
```
