from .producto import Producto # Importar el modelo Producto
from .lote import Lote # Importar el modelo Lote
from .proveedor import Proveedor # Importar el modelo Proveedor

__all__ = [ # Definir los nombres que se exportan al importar el paquete
    "Producto", # Modelo Producto
    "Lote", # Modelo Lote
    "Proveedor", # Modelo Proveedor
]
