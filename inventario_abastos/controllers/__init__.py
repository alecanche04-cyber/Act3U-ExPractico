#__init__

from .inventario import (
    verificar_bajo_stock,
    verificar_items_por_caducar,
    calcular_cantidad_sugerida_orden
)

from .pedidos import (
    generar_ordenes_sugeridas,
    confirmar_orden
)

__all__ = [
    "verificar_bajo_stock",
    "verificar_items_por_caducar",
    "calcular_cantidad_sugerida_orden",
    "generar_ordenes_sugeridas",
    "confirmar_orden",
]

