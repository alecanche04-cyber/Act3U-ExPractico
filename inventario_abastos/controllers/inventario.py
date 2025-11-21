
from datetime import datetime, timedelta # Permite trabajar con fechas y calcular rangos  de tiempo 
from typing import List, Dict # Permite usar tipos de tados como listas y diccionarios
import logging # Permite registrar eventos y errores en el sistema

# Importa modelos de base de datos
from ..models.producto import Producto # Importa el modelo Producto
from ..models.lote import Lote # Importa el modelo Lote
from ..models.proveedor import proveedor # Importa el modelo Proveedor
from ..database.db import db  # Importa la instancia de la base de datos

logger = logging.getLogger(__name__) # Crea un registrador para guardar mensajes de error o informacion util


def verificar_bajo_stock(): #Buscar productos con stock menor o igual a lo permitido

	productos = Producto.query.filter(Producto.cantidad <= Producto.cantidad_minima).all() # Obtiene productos con stock bajo
	salida: List[Dict] = [] # Lista para almacenar resultados
	for p in productos: # Recorre sobre productos con stock bajo
		try:
			if hasattr(p, "to_dict"): # Si el producto tiene metodo to_dict, usarlo
				salida.append(p.to_dict()) # Agrega diccionario del producto a la salida
			else:
				salida.append({ # Serializa manualmente los campos del producto
					"id": p.id, # Identificador del producto
					"nombre": getattr(p, "nombre", None), # Nombre del producto
					"codigo": getattr(p, "codigo", None), # Código del producto
					"cantidad": getattr(p, "cantidad", None), # Cantidad disponible
					"cantidad_minima": getattr(p, "cantidad_minima", None), # Cantidad mínima permitida
					"id_proveedor": getattr(p, "id_proveedor", None), # Identificador del proveedor
				})
		except Exception as e: # Manejo de errores durante la serialización
			logger.exception("Error al serializar producto %s: %s", getattr(p, "id", None), e) # Registra el error con detalles del producto
	return salida


def verificar_items_por_caducar(dias: int = 7) -> List[Dict]: # Buscar lotes cuya fecha de caducidad está dentro de los próximos `days` días

	limite = datetime.utcnow() + timedelta(days=dias) # Calcula la fecha límite para la caducidad
	lotes = Lote.query.filter(Lote.fecha_caducidad != None, Lote.fecha_caducidad <= limite).all() # Consulta lotes que caducan antes del límite
	salida: List[Dict] = [] # Lista para almacenar resultados
	for l in lotes: # Recorre lotes encontrados
		producto = None # Inicializa variable para el producto asociado
		try:
			producto = Producto.query.get(l.id_producto) # Obtiene el producto asociado al lote
		except Exception: # Manejo de errores al obtener el producto
			producto = None # En caso de error, asigna None

		salida.append({ # Agrega información del lote y producto a la salida
			"id_lote": getattr(l, "id", None), # Identificador del lote
			"id_producto": getattr(l, "id_producto", None), # Identificador del producto
			"producto_nombre": getattr(producto, "nombre", None) if producto else None, # Nombre del producto
			"cantidad_lote": getattr(l, "cantidad", None), # Cantidad en el lote
			"fecha_caducidad": getattr(l, "fecha_caducidad", None), # Fecha de caducidad del lote
		})
	return salida # Devuelve la lista de lotes próximos a caducar


def calcular_cantidad_sugerida_orden(producto: Producto, factor: int = 2) -> int: # Calcular cantidad sugerida para reponer un producto
	# Regla simple (configurable):
	# objetivo = cantidad_minima * factor
	# sugerida = max(objetivo - cantidad_actual, cantidad_minima)

	# Devuelve un entero >= 0.

	try:
		cantidad_actual = int(getattr(producto, "cantidad", 0) or 0) # Obtiene la cantidad actual del producto
		cantidad_minima = int(getattr(producto, "cantidad_minima", 1) or 1) # Obtiene la cantidad mínima permitida
	except Exception:
		logger.exception("Error leyendo campos numéricos del producto %s", getattr(producto, "id", None)) # Registra error al leer campos numéricos
		return 0 # En caso de error, devuelve 0

	objetivo = cantidad_minima * max(1, int(factor)) # Calcula el objetivo de stock basado en el factor
	sugerida = max(objetivo - cantidad_actual, cantidad_minima) # Calcula la cantidad sugerida para ordenar
	return int(sugerida) # Devuelve la cantidad sugerida como entero

