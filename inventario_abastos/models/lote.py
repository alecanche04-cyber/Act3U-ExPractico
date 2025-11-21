from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any

def analizar_fecha(valor: Any) -> Optional[datetime]: # Analiza un valor y lo convierte a datetime si es posible
    if valor is None: # Si el valor es None
        return None # Devuelve None
    if isinstance(valor, datetime): # Si el valor ya es un datetime
        return valor # Devuelve el valor tal cual
    try: 
        return datetime.fromisoformat(str(valor)) # Intenta convertir el valor desde una cadena ISO
    except Exception:
        return None # Devuelve None si la conversión falla
    
@dataclass # Define la clase Lote como un dataclass
class Lote: # Clase que representa un lote de productos en inventario
    id: Optional[int] = None # Identificador del lote
    id_producto: Optional[int] = None # Identificador del producto asociado al lote
    cantidad: int = 0 # Cantidad de productos en el lote
    fecha_caducidad: Optional[datetime] = None # Fecha de caducidad del lote
    fecha_ingreso: Optional[datetime] = None # Fecha de ingreso del lote al inventario
    codigo_lote: Optional[str] = None # Código identificador del lote

    def diccionario(self) -> Dict[str, Any]: # Convierte el objeto Lote a un diccionario
        d = asdict(self) # Convierte el dataclass a un diccionario
        d["fecha_caducidad"] = self.fecha_caducidad.isoformat() if self.fecha_caducidad else None # Convierte fecha_caducidad a cadena ISO
        d["fecha_ingreso"] = self.fecha_ingreso.isoformat() if self.fecha_ingreso else None # Convierte fecha_ingreso a cadena ISO
        return d # Devuelve el diccionario
    
    @classmethod # Crea una instancia de Lote desde un diccionario
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Lote": # Crea un objeto Lote a partir de un diccionario
        return cls( # Devuelve una nueva instancia de Lote
            id=datos.get("id"), # Asigna el ID del lote
            id_producto=datos.get("id_producto"), # Asigna el ID del producto
            cantidad=int(datos.get("cantidad", 0) or 0), # Asigna la cantidad del lote
            fecha_caducidad=analizar_fecha(datos.get("fecha_caducidad")), # Asigna la fecha de caducidad
            fecha_ingreso=analizar_fecha(datos.get("fecha_ingreso")), # Asigna la fecha de ingreso
            codigo_lote=datos.get("codigo_lote"), # Asigna el código del lote
        )
    