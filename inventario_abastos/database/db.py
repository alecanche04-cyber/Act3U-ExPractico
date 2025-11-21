import json # Para manejar datos en formato JSON
import os # Para operaciones del sistema operativo
import tempfile # Para crear archivos temporales
from threading import Lock # Para manejar concurrencia en hilos
from typing import Any, Dict, List, Optional # Para anotaciones de tipos

DATA_DIR = os.path.join(os.path.dirname(__file__), "..." "data") # Directorio donde se almacenan los datos
os.makedirs(DATA_DIR, exist_ok=True) # Asegura que el directorio de datos exista

_lock = Lock() # Lock para manejar acceso concurrente a la base de datos

def ruta(tabla: str) -> str: # Obtiene la ruta del archivo JSON para una tabla dada
    return os.path.join(DATA_DIR, f"{tabla}.json") # Construye la ruta del archivo JSON

def cargar(tabla: str) -> List[Dict[str, Any]]: # Carga los datos de una tabla desde su archivo JSON
    ruta_archivo = ruta(tabla) # Obtiene la ruta del archivo JSON

    if not os.path.exists(ruta_archivo): # Si el archivo no existe
        return [] # Devuelve una lista vacía
    
    with open(ruta_archivo, "r", encoding="utf-8") as f: # Abre el archivo para lectura
        return json.load(f) # Carga y devuelve los datos JSON

def guardar(tabla: str, datos: List[Dict[str, Any]]) -> None: # Guarda los datos de una tabla en su archivo JSON
    ruta_archivo = ruta(tabla) # Obtiene la ruta del archivo JSON
    fd, tmp = tempfile.mkstemp(dir=DATA_DIR) # Crea un archivo temporal en el directorio de datos

    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f: # Abre el archivo temporal para escritura
            json.dump(datos, f, indent=4, ensure_ascii=False) # Escribe los datos JSON en el archivo temporal
        os.replace(tmp, ruta_archivo) # Reemplaza el archivo original con el temporal
    finally:
        if os.path.exists(tmp): # Si el archivo temporal aún existe
            os.remove(tmp) # Lo elimina

def obtener_todos(tabla: str) -> List[Dict[str, Any]]: # Obtiene todos los registros de una tabla
        return cargar(tabla) # Carga y devuelve los datos de la tabla

def obtener_por_id(tabla: str, id_valor: Any, campo_id: str = "id") -> Optional[Dict[str, Any]]: # Obtiene un registro por su ID
    for it in cargar(tabla): # Recorre los registros de la tabla
        if it.get(campo_id) == id_valor: # Si el ID coincide
            return it # Devuelve el registro encontrado
    return None # Devuelve None si no se encuentra el registro

def siguiente_id(elementos: List[Dict[str, Any]])-> int: # Obtiene el siguiente ID disponible en una lista de registros
    if not elementos: # Si la lista está vacía
        return 1 # Devuelve 1 como el primer ID
    return max(int(i.get("id", 0)) for i in elementos) + 1 # Devuelve el siguiente ID disponible

def agregar(tabla: str, obj: Dict[str, Any]) -> Dict[str, Any]: # Agrega un nuevo registro a una tabla
    elementos = cargar(tabla) # Carga los registros existentes de la tabla
    if "id" not in obj or obj["id"] is None: # Si el objeto no tiene ID
        obj["id"] = siguiente_id(elementos) # Asigna el siguiente ID disponible
    elementos.append(obj) # Agrega el nuevo registro a la lista
    guardar(tabla, elementos) # Guarda la lista actualizada en el archivo JSON
    return obj # Devuelve el registro agregado

def actualizar(tabla: str, id_valor: Any, cambios: Dict[str, Any], campo_id: str = "id") -> Optional[Dict[str, Any]]: # Actualiza un registro existente en una tabla
    elementos = cargar(tabla) # Carga los registros existentes de la tabla
    for i, it in enumerate(elementos): # Recorre los registros con su índice
        if it.get(campo_id) == id_valor: # Si el ID coincide
            elementos[i] = {**it, **cambios, campo_id: id_valor} # Actualiza el registro con los cambios
            guardar(tabla, elementos) # Guarda la lista actualizada en el archivo JSON
            return elementos[i] # Devuelve el registro actualizado
    return None # Devuelve None si no se encuentra el registro

def eliminar(tabla: str, id_valor: Any, campo_id: str = "id") -> bool: # Elimina un registro de una tabla por su ID
    elementos = cargar(tabla) # Carga los registros existentes de la tabla
    nuevos = [it for it in elementos if it.get(campo_id) != id_valor] # Filtra los registros para eliminar el especificado
    if len(nuevos) == len(elementos): # Si no se eliminó ningún registro
        return False # Devuelve False
    guardar(tabla, nuevos) # Guarda la lista actualizada en el archivo JSON
    return True # Devuelve True indicando que se eliminó el registro
