# Este archivo convierte la carpeta controllers en un paquete de Python y permite la reexportación de funciones y clases desde los módulos internos.
#Reexporta funciones y clases del módulo controllers para facilitar su acceso desde otros módulos

from.inventario import check_low_stock, check_expired_items, calculate_order_qty # Reexportar funciones del módulo inventario
from. pedidos import generate_suggested_orders, confirm_orders # Reexportar funciones del módulo pedidos

__all__ = [ # Definir los nombres que se exportan al importar el paquete
    "chechk_low_stock", #Reexportar funciones del módulo inventario
    "check_expired_items", # Reexportar funciones del módulo inventario
    "calculate_suggested_orders_qty", # Reexportar funciones del módulo inventario
    "generate_suggested_orders", # Reexportar funciones del módulo pedidos
    "confirm_orders"    # Reexportar funciones del módulo pedidos
]

