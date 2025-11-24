#---------------------------------------------
# Módulo de Pedidos
# Manejo de pedidos manuales y automáticos
#---------------------------------------------
from datetime import date

# Simulación de base de datos de pedidos
PEDIDOS = []

def obtener_pedidos():
    return {
        "total": len(PEDIDOS),
        "pedidos": PEDIDOS
    }


def crear_pedido(pedido: dict):
    nuevo_id = len(PEDIDOS) + 1
    pedido["id"] = nuevo_id
    pedido["fecha"] = date.today()
    PEDIDOS.append(pedido)

    return {
        "mensaje": "Pedido creado correctamente",
        "pedido": pedido
    }


def obtener_pedido_por_id(pedido_id: int):
    pedido = next((p for p in PEDIDOS if p["id"] == pedido_id), None)
    if not pedido:
        return {"error": "Pedido no encontrado"}
    return pedido


def actualizar_pedido(pedido_id: int, datos: dict):
    for p in PEDIDOS:
        if p["id"] == pedido_id:
            p.update(datos)
            return {
                "mensaje": "Pedido actualizado",
                "pedido": p
            }
    return {"error": "Pedido no encontrado"}


def eliminar_pedido(pedido_id: int):
    global PEDIDOS
    PEDIDOS = [p for p in PEDIDOS if p["id"] != pedido_id]
    return {"mensaje": "Pedido eliminado correctamente"}

