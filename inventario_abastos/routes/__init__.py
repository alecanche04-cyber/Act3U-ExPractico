# __init__.py
# Permite importar los routers desde la carpeta "routes".

from .productos_router import router as productos_router
from .pedidos_router import router as pedidos_router

__all__ = ["productos_router", "pedidos_router"]
