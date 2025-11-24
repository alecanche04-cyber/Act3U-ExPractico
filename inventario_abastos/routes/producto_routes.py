# Productos en el invantario
from datetime import date, timedelta

# --------------------------------------------------
# PRODUCTOS 
# --------------------------------------------------
PRODUCTOS = [
    # --------- PANADERÍA Y TORTILLERÍA ---------
    {"id": 1,  "nombre": "Pan dulce", "categoria": "Panadería", "stock": 12, "stock_min": 6,
    "precio": 12.00, "caducidad": date(2025, 10, 25)},

    {"id": 2,  "nombre": "Tortillas de maíz", "categoria": "Panadería", "stock": 10, "stock_min": 5,
    "precio": 20.00, "caducidad": date(2025, 11, 2)},

    {"id": 3,  "nombre": "Pan blanco Bimbo", "categoria": "Panadería", "stock": 10, "stock_min": 5,
    "precio": 38.00, "caducidad": date(2025, 10, 26)},

    # --------- BOTANAS ---------
    {"id": 4,  "nombre": "Sabritas clásicas", "categoria": "Botanas", "stock": 11, "stock_min": 5,
    "precio": 18.00, "caducidad": date(2025, 12, 18)},

    {"id": 5,  "nombre": "Doritos nacho", "categoria": "Botanas", "stock": 7, "stock_min": 5,
    "precio": 17.50, "caducidad": date(2026, 3, 3)},

    {"id": 6,  "nombre": "Cheetos flaming hot", "categoria": "Botanas", "stock": 6, "stock_min": 4,
    "precio": 16.00, "caducidad": date(2025, 10, 28)},

    # --------- BEBIDAS ---------
    {"id": 7, "nombre": "Refresco Coca-Cola 600ml", "categoria": "Bebidas", "stock": 15, "stock_min": 8,
    "precio": 22.00, "caducidad": date(2026, 5, 1)},

    {"id": 8, "nombre": "Refresco Pepsi 600ml", "categoria": "Bebidas", "stock": 9, "stock_min": 6,
        "precio": 20.00, "caducidad": date(2026, 4, 20)},

    {"id": 9, "nombre": "Agua Bonafont 1L", "categoria": "Bebidas", "stock": 9, "stock_min": 5,
    "precio": 14.00, "caducidad": date(2026, 5, 12)},

    {"id": 10, "nombre": "Jugo del Valle 500ml", "categoria": "Bebidas", "stock": 12, "stock_min": 5,
    "precio": 18.50, "caducidad": date(2025, 11, 15)},

    # --------- LÁCTEOS ---------
    {"id": 11, "nombre": "Leche entera 1L", "categoria": "Lácteos", "stock": 8, "stock_min": 6,
    "precio": 25.00, "caducidad": date(2025, 11, 5)},

    {"id": 12, "nombre": "Leche deslactosada 1L", "categoria": "Lácteos", "stock": 10, "stock_min": 6,
    "precio": 27.00, "caducidad": date(2025, 11, 7)},

    {"id": 13, "nombre": "Huevos 12p", "categoria": "Lácteos", "stock": 7, "stock_min": 8,
    "precio": 40.00, "caducidad": date(2025, 10, 23)},

    # --------- ABARROTES SECOS ---------
    {"id": 14, "nombre": "Arroz 1kg", "categoria": "Abarrotes", "stock": 14, "stock_min": 6,
    "precio": 28.00, "caducidad": date(2026, 12, 31)},

    {"id": 15, "nombre": "Frijol 1kg", "categoria": "Abarrotes", "stock": 9, "stock_min": 6,
    "precio": 32.00, "caducidad": date(2026, 11, 19)},

    {"id": 16, "nombre": "Azúcar 1kg", "categoria": "Abarrotes", "stock": 15, "stock_min": 6,
    "precio": 25.00, "caducidad": date(2026, 9, 5)},

    {"id": 17, "nombre": "Sal 1kg", "categoria": "Abarrotes", "stock": 6, "stock_min": 3,
    "precio": 12.00, "caducidad": date(2026, 10, 30)},

    {"id": 18, "nombre": "Atún en agua", "categoria": "Abarrotes", "stock": 10, "stock_min": 5,
    "precio": 18.00, "caducidad": date(2026, 8, 15)},

    {"id": 19, "nombre": "Atún en aceite", "categoria": "Abarrotes", "stock": 12, "stock_min": 5,
    "precio": 19.50, "caducidad": date(2026, 7, 12)},

    {"id": 20, "nombre": "Café soluble", "categoria": "Abarrotes", "stock": 5, "stock_min": 3,
    "precio": 48.00, "caducidad": date(2026, 3, 22)},

    # --------- LIMPIEZA ---------
    {"id": 21, "nombre": "Detergente en polvo 1kg", "categoria": "Limpieza", "stock": 8, "stock_min": 3,
    "precio": 35.00, "caducidad": date(2026, 12, 20)},

    {"id": 22, "nombre": "Cloro 1L", "categoria": "Limpieza", "stock": 11, "stock_min": 4,
    "precio": 18.00, "caducidad": date(2026, 11, 1)},
]

def obtener_productos():
    return {"total": len(PRODUCTOS), "productos": PRODUCTOS}


def obtener_producto(producto_id: int):
    producto = next((p for p in PRODUCTOS if p["id"] == producto_id), None)
    if not producto:
        return {"error": "Producto no encontrado"}
    return producto


def agregar_producto(producto: dict):
    producto["id"] = len(PRODUCTOS) + 1
    PRODUCTOS.append(producto)
    return {"mensaje": "Producto agregado", "producto": producto}


def actualizar_producto(producto_id: int, datos: dict):
    for p in PRODUCTOS:
        if p["id"] == producto_id:
            p.update(datos)
            return {"mensaje": "Producto actualizado", "producto": p}
    return {"error": "Producto no encontrado"}


def borrar_producto(producto_id: int):
    global PRODUCTOS
    PRODUCTOS = [p for p in PRODUCTOS if p["id"] != producto_id]
    return {"mensaje": "Producto eliminado"}


# --------------------------------------------------
# ALERTAS AUTOMÁTICAS
# --------------------------------------------------

def productos_stock_bajo():
    bajos = [p for p in PRODUCTOS if p["stock"] <= p["stock_min"]]
    return {"total": len(bajos), "stock_bajo": bajos}


def proximos_a_caducar():
    hoy = date.today()
    limite = hoy + timedelta(days=10)
    proximos = [p for p in PRODUCTOS if p["caducidad"] <= limite]
    return {"total": len(proximos), "proximos_a_caducar": proximos}


def productos_vencidos():
    hoy = date.today()
    vencidos = [p for p in PRODUCTOS if p["caducidad"] < hoy]
    return {"total": len(vencidos), "vencidos": vencidos}
