#---------------------------------------------
# Routes de Pedidos
# Manejo de pedidos manuales y automáticos
#---------------------------------------------

from fastapi import APIRouter
from datetime import date

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"]
)

# Simulación de base de datos para pedidos
pedidos = []


# Obtener todos los pedidos
@router.get("/")
def obtener_pedidos():
    return {"pedidos": pedidos}


# Crear un pedido manualmente
@router.post("/")
def crear_pedido(pedido: dict):
    pedido["id"] = len(pedidos) + 1
    pedido["fecha"] = date.today()

    pedidos.append(pedido)
    return {"mensaje": "Pedido creado exitosamente", "pedido": pedido}


# Crear un pedido automático según el inventario
@router.post("/generar-automatico")
def generar_pedido_automatico():
    # Importar productos desde el router de productos
    from routers.productos_router import productos

    productos_faltantes = [
        {
            "producto": p["nombre"],
            "stock_actual": p["stock"],
            "stock_minimo": p["stock_min"]
        }
        for p in productos if p["stock"] < p["stock_min"]
    ]

    pedido = {
        "id": len(pedidos) + 1,
        "fecha": date.today(),
        "productos_a_reponer": productos_faltantes
    }

    pedidos.append(pedido)

    return {
        "mensaje": "Pedido automático generado correctamente",
        "pedido": pedido
    }
