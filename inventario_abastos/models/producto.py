from dataclasses import dataclass, asdict # Importar dataclass y asdict para definir modelos de datos
from datetime import datetime # Importar datetime para manejar fechas y horas
from typing import  Dict, Optional, Any # Importar tipos para anotaciones de tipo

def entero(valor, Any, defecto: int = 0) -> int: # Convierte un valor a entero, usando un valor por defecto si falla
    try:
        return int(valor) # Intenta convertir el valor a entero
    except Exception:
        return defecto # Devuelve el valor por defecto si la conversión falla
    
def flotante(valor: Any, defecto: float = 0.0) -> float: # Convierte un valor a flotante, usando un valor por defecto si falla
    try:
        return float(valor) # Intenta convertir el valor a flotante
    except Exception:
        return defecto # Devuelve el valor por defecto si la conversión falla

@dataclass # Define la clase Producto como un dataclass
class Producto: # Clase que representa un producto en inventario
    id: Optional[int] = None # Identificador del producto
    nombre: str = "" # Nombre del producto
    codigo: Optional[str] = None # Código del producto
    cantidad: int = 0 # Cantidad disponible del producto
    cantidad_minima: int = 1 # Cantidad mínima permitida del producto
    precio_unitario: float = 0.0 # Precio unitario del producto
    id_proveedor: Optional[int] = None # Identificador del proveedor del producto
    fecha_creacion: Optional[datetime] = None # Fecha de creación del producto
    fecha_actualizacion: Optional[datetime] = None # Fecha de última actualización del producto

    def diccionario(self) -> Dict[str, Any]: # Convierte el objeto Producto a un diccionario
        d = asdict(self) # Convierte el dataclass a un diccionario
        d["fecha_creacion"] = self.fecha_creacion.isoformat() if self.fecha_creacion else None # Convierte fecha_creacion a cadena ISO
        d["fecha_actualizacion"] = self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None # Convierte fecha_actualizacion a cadena ISO
        return d # Devuelve el diccionario
    
    @classmethod # Crea una instancia de Producto desde un diccionario
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Producto": # Crea un objeto Producto a partir de un diccionario
        fc = datos.get("fecha_creacion") # Obtiene la fecha de creación del diccionario
        fa = datos.get("fecha_actualizacion") # Obtiene la fecha de actualización del dic

        try:
            fecha_creacion = datetime.fromisoformat(str(fc)) if fc else None # Convierte fecha_creacion desde cadena ISO
        except Exception:
            fecha_creacion = None # Asigna None si la conversión falla
        try:
            fecha_actualizacion = datetime.fromisoformat(str(fa)) if fa else None # Convierte fecha_actualizacion desde cadena ISO
        except Exception:
            fecha_actualizacion = None # Asigna None si la conversión falla

        return cls( # Devuelve una nueva instancia de Producto
            id=datos.get("id"), # Asigna el ID del producto
            nombre=str(datos.get("nombre", "") or ""), # Asigna el nombre del producto
            codigo=datos.get("codigo"), # Asigna el código del producto
            cantidad=entero(datos.get("cantidad", 0), Any, 0), # Asigna la cantidad del producto
            cantidad_minima=entero(datos.get("cantidad_minima", 1), Any, 1), # Asigna la cantidad mínima del producto
            precio_unitario=flotante(datos.get("precio_unitario", 0.0), 0.0), # Asigna el precio unitario del producto
            id_proveedor=datos.get("id_proveedor"), # Asigna el ID del proveedor del producto
            fecha_creacion=fecha_creacion, # Asigna la fecha de creación del producto
            fecha_actualizacion=fecha_actualizacion, # Asigna la fecha de actualización del producto
        )
    def actualizar_stock(self, delta: int) -> None: # Actualiza la cantidad de stock del producto
        self.cantidad = max(0, int(self.cantidad) + int(delta)) # Ajusta la cantidad asegurando que no sea negativa
        self.fecha_actualizacion = datetime.utcnow() # Actualiza la fecha de última actualización a la fecha y hora actual
    
    def necesita_rebastecer(self) -> bool: # Verifica si el producto necesita ser reabastecido
        return int(self.cantidad) <= int(self.cantidad_minima) # Devuelve True si la cantidad es menor o igual a la cantidad mínima 