# __init__.py
# Permite importar los routers desde la carpeta "routes".

from .producto_routes import router as productos_router
from .pedido_routes import router as pedidos_router

__all__ = ["productos_router", "pedidos_router"]
