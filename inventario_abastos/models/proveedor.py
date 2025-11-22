from dataclasses import dataclass, asdict # Importar dataclass y asdict para definir modelos de datos
from typing import Optional, Dict, Any # Importar tipos para anotaciones de tipo
from datetime import datetime # Importar datetime para manejar fechas y horas

@dataclass # Define la clase Proveedor como un dataclass
class Proveedor: # Clase que representa un proveedor en el sistema
    id: Optional[int] = None # Identificador del proveedor
    nombre: str = "" # Nombre del proveedor
    telefono: Optional[str] = None # Teléfono del proveedor
    direccion: Optional[str] = None # Dirección del proveedor
    tiempo_estimado_entrega: Optional[int] = None # Tiempo estimado de entrega en días
    fecha_creacion: Optional[datetime] = None # Fecha de creación del proveedor
    fecha_actualizacion: Optional[datetime] = None # Fecha de última actualización del proveedor

    def diccionario(self) -> Dict[str, Any]: # Convierte el objeto Proveedor a un diccionario
        d = asdict(self) # Convierte el dataclass a un diccionario
        d["fecha_creacion"] = self.fecha_creacion.isoformat() if self.fecha_creacion else None # Convierte fecha_creacion a cadena ISO
        d["fecha_actualizacion"] = self.fecha_actualizacion.isoformat() if self.fecha_actualizacion else None # Convierte fecha_actualizacion a cadena ISO
        return d # Devuelve el diccionario
    
    @classmethod # Crea una instancia de Proveedor desde un diccionario
    def desde_diccionario(cls, datos: Dict[str, Any]) -> "Proveedor": # Crea un objeto Proveedor a partir de un diccionario
        def parsear_fecha(v): # Función auxiliar para convertir cadenas a datetime
            try:
                return datetime.fromisoformat(str(v)) if v else None # Convierte fecha desde cadena ISO
            except Exception:
                return None # Asigna None si la conversión falla
        
        return cls( # Devuelve una nueva instancia de Proveedor
            id=datos.get("id"), # Asigna el ID del proveedor
            nombre=str(datos.get("nombre", "") or ""), # Asigna el nombre del proveedor
            telefono=datos.get("telefono"), # Asigna el teléfono del proveedor
            direccion=datos.get("direccion"), # Asigna la dirección del proveedor
            tiempo_estimado_entrega=datos.get("tiempo_estimado_entrega"), # Asigna el tiempo estimado de entrega
            fecha_creacion=parsear_fecha(datos.get("fecha_creacion")), # Asigna la fecha de creación del proveedor
            fecha_actualizacion=parsear_fecha(datos.get("fecha_actualizacion")), # Asigna la fecha de actualización del proveedor
        )
    

