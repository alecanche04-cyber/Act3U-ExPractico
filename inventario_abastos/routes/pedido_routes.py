#---------------------------------------------
# Routes de Pedidos
# Manejo de pedidos manuales y automáticos
#---------------------------------------------
# pedidos_router.py
from fastapi import APIRouter
from datetime import date

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

# Simulación de base de datos de pedidos
PEDIDOS = []

@router.get("/")
def obtener_pedidos():
    return {
        "total": len(PEDIDOS),
        "pedidos": PEDIDOS
    }

@router.post("/")
def crear_pedido(pedido: dict):
    nuevo_id = len(PEDIDOS) + 1
    pedido["id"] = nuevo_id
    pedido["fecha"] = date.today()
    PEDIDOS.append(pedido)

    return {
        "mensaje": "Pedido creado correctamente",
        "pedido": pedido
    }
@router.get("/{pedido_id}")
def obtener_pedido_por_id(pedido_id: int):
    pedido = next((p for p in PEDIDOS if p["id"] == pedido_id), None)
    if not pedido:
        return {"error": "Pedido no encontrado"}
    return pedido


@router.put("/{pedido_id}")
def actualizar_pedido(pedido_id: int, datos: dict):
    for p in PEDIDOS:
        if p["id"] == pedido_id:
            p.update(datos)
            return {
                "mensaje": "Pedido actualizado",
                "pedido": p
            }
    return {"error": "Pedido no encontrado"}


@router.delete("/{pedido_id}")
def eliminar_pedido(pedido_id: int):
    global PEDIDOS
    PEDIDOS = [p for p in PEDIDOS if p["id"] != pedido_id]
    return {"mensaje": "Pedido eliminado correctamente"}
