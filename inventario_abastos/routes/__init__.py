#Se importan los routers para que sea mas faciles de usar en este modulo
from .productos_routes import router as productos_router #Router para productos 
from .pedidos_routes import router as pedido_router #Router para pedidos 
__all__ = ["productos_router", "pedido_router"] #all define define lo que sera accesible a la hora de importar el paquete