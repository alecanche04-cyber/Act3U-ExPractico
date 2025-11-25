# services/_init_.py

# Este archivo convierte el directorio 'services' en un paquete Python.

from .alertas import alertas # Importa el módulo de alertas
from .notificaciones import notificaciones # Importa el módulo de notificaciones

__all__ = [  # Define los nombres que se exportan al importar el paquete
    "alertas", # Importa el módulo de alertas
    "notificaciones", # Importa el módulo de notificaciones
]
