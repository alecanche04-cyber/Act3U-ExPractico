
from datetime import datetime # Importa clase datetime para manejo de fechas
from collections import defaultdict # Importa defaultdict para diccionarios con valores por defecto
import logging # Importa módulo de logging para registro de eventos
from typing import List, Dict, Optional # Importa tipos para anotaciones de tipo

from .inventario import check_low_stock, calculate_suggested_order_qty # Importa funciones del módulo inventario

try:
    from ..database.db import add as db_adb, updata as db_update, get_all as db_get_all # Intenta importar funciones de la base de datos JSON
    _HAS_JSON_DB = True
except ImportError:
    _HAS_JSON_DB = False

logger = logging.getLogger(__name__) # Crea un logger para el módulo

def generar_ordenes_sugeridas(productos_bajos: Optional[List[Dict]] = None, factor: int = 2) -> Dict[int, List[Dict]]: # Genera órdenes sugeridas para productos con bajo stock
    
    #Parámetros:
#- productos_bajos: lista opcional de productos (cada uno puede ser dict o modelo).
#Si es None, se llama a check_low_stock().
#- factor: factor usado para calcular cantidad sugerida.

#Salida esperada:
#Diccionario: { id_proveedor: [ { 'id_producto': int, 'nombre': str, 'cantidad_sugerida': int }, ... ], ... }
    
    
    if productos_bajos is None: # Si no se proporcionan productos bajos
        productos_bajos = check_low_stock() # Obtiene productos con bajo stock si no se proporcionan
        grouped = defaultdict(list) # Diccionario para agrupar órdenes por proveedor

    for p in productos_bajos: # Recorre productos con bajo stock
        try:
            if isinstance(p, dict): # Si el producto es un diccionario
                id_producto = p.get("id") # Obtiene el ID del producto
                nombre = p.get("nombre") # Obtiene el nombre del producto
                cantidad = int(p.get("cantidad", 0) or 0) # Obtiene la cantidad actual
                cantidad_minima = int(p.get("cantidad_minima",1) or 1) # Obtiene la cantidad mínima
                id_proveedor = p.get("id_proveedor") # Obtiene el ID del proveedor

                objetivo = cantidad_minima * max(1, int(factor)) # Calcula el objetivo de stock
                cantidad_sugerida = max(objetivo - cantidad, cantidad_minima) # Calcula la cantidad sugerida

            else: # Si el producto es un modelo
                id_producto = getattr(p, "id", None) # Obtiene el ID del producto
                nombre = getattr(p, "nombre", None) # Obtiene el nombre del producto
                id_proveedor = getattr(p, "id_proveedor", None) # Obtiene el ID del proveedor

                try: 
                    cantidad_sugerida = calculate_suggested_order_qty(p, factor = factor) # Calcula la cantidad sugerida usando el modelo
                except Exception:
                    cantidad = int(getattr(p, "cantidad", 0) or 0) # Obtiene la cantidad actual
                    cantidad_minima = int(getattr(p, "cantidad_minima", 1) or 1) # Obtiene la cantidad mínima
                    objetivo = cantidad_minima * max(1, int(factor)) # Calcula el objetivo de stock
                    cantidad_sugerida = max(objetivo - cantidad, cantidad_minima) # Calcula la cantidad sugerida

        except Exception as e: # Manejo de errores durante el procesamiento del producto
            logger.exception("Error al procesar producto para orden sugerida: %s", e) # Registra el error
            continue # Salta al siguiente producto

        grouped[id_proveedor].append({ # Agrega la orden sugerida al grupo del proveedor
            "id_producto": id_producto, # Identificador del producto
            "nombre": nombre, # Nombre del producto
            "cantidad_sugerida": cantidad_sugerida, # Cantidad sugerida para ordenar
        })

    return dict(grouped) # Devuelve el diccionario de órdenes sugeridas agrupadas por proveedor

def crear_orden_dict(id_proveedor: int, items: List[Dict], numero_pedido: Optional[str] = None) -> Dict: # Crea un diccionario que representa una orden de pedido


    fecha = datetime.utcnow().isoformat() # Obtiene la fecha y hora actual en formato ISO
    total = 0.0 # Inicializa el total de la orden
    items_sanitizados = [] # Lista para almacenar los ítems sanitizados
    
    for it in items:
        cantidad = int(it.get("cantidad", 0)) # Obtiene la cantidad del ítem
        precio = float(it.get("precio_unitario",0) or 0) # Obtiene el precio unitario del ítem
        subtotal = cantidad * precio # Calcula el subtotal del ítem
        total += subtotal # Suma el subtotal al total de la orden
        items_sanitizados.append({ # Agrega el ítem sanitizado a la lista
            "id_producto": it.get("id_producto"), # Identificador del producto
            "cantidad": cantidad, # Cantidad del producto
            "precio_unitario": precio, # Precio unitario del producto
            "subtotal": subtotal, # Subtotal del ítem
        })
    pedido = { # Crea el diccionario de la orden de pedido
        "id_proveedor": id_proveedor, # Identificador del proveedor
        "numero_pedido": numero_pedido, # Número del pedido
        "estado": "pendiente", # Estado del pedido
        "fecha_pedido": fecha, # Fecha del pedido
        "items": items_sanitizados, # Lista de ítems en la orden
        "total": total, # Total estimado de la orden
    }
    return pedido # Devuelve el diccionario de la orden de pedido

def guardar_orden(pedido_dict: Dict) -> Dict: # Guarda una orden de pedido en la base de datos JSON si está disponible

    if _HAS_JSON_DB: # Verifica si la base de datos JSON está disponible
        try:
            guardado= db_adb("pedidos", pedido_dict) # Intenta guardar la orden en la base de datos
            logger.info("Orden guardada con id %s", guardado.get("id")) # Registra el ID de la orden guardada
            return guardado # Devuelve el diccionario de la orden guardada
        except Exception as e: # Manejo de errores durante el guardado
            logger.exception("Error al guardar la orden: %s", e) # Registra el error
            raise  # Re-lanza la excepción

    else: # Si la base de datos JSON no está disponible
        logger.error("Base de datos JSON no disponible. No se puede guardar la orden.") # Registra el error
        return pedido_dict # Devuelve el diccionario de la orden sin guardar
    
def confirmar_orden(pedido_id: int) -> Optional[Dict]: # Confirma una orden de pedido existente en la base de datos JSON

    if not _HAS_JSON_DB: # Verifica si la base de datos JSON está disponible
        logger.error("Base de datos JSON no disponible. No se puede confirmar la orden.") # Registra el error
        return None # Devuelve None si la base de datos no está disponible
    
    try: # Intenta confirmar la orden
        pedidos = db_get_all("pedidos") # Obtiene todas las órdenes de pedido
        for p in pedidos: # Recorre las órdenes para encontrar la correspondiente
            if p.get("id") == pedido_id: # Si encuentra la orden con el ID dado
                p["estado"] = "confirmado" # Cambia el estado a confirmado
                actualizado = db_update("pedidos", pedido_id, p) # Actualiza la orden en la base de datos
                logger.info("Orden con id %s confirmada.", pedido_id) # Registra la confirmación
                return actualizado # Devuelve el diccionario de la orden actualizada
            
            logger.error("Orden con id %s no encontrada.", pedido_id) # Registra si no se encuentra la orden
            return None # Devuelve None si no se encuentra la orden
        
    except Exception as e: # Manejo de errores durante la confirmación
        logger.exception("Error al confirmar la orden %s: %s", pedido_id, e) # Registra el error
        return None # Devuelve None en caso de error
    