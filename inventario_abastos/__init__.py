
__version__ = "1.0.0" # Versión del paquete inventario_abastos

from . import controllers, models, services, database, utilidades, routes # Importa submódulos del paquete

__all__ = [ # Define los nombres que se exportan al importar el paquete
    "__version__", # Versión del paquete
    "controllers", # Controladores del paquete
    "models", # Modelo de datos
    "routes", # Rutas del paquete
    "services", # Servicios del paquete
    "database", # Base de datos del paquete
    "utilidades", # Utilidades del paquete
]