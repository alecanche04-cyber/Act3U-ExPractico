
import os # Importa el módulo os para manejar rutas de archivos
import logging # Importa el módulo logging para manejo de logs
import atexit # Importa atexit para registrar funciones al salir
from typing import Any # Importa Any para anotaciones de tipo
from inventario_abastos.controllers.inventario import verificar_bajo_stock, verificar_items_por_caducar # Importa funciones de controladores
from inventario_abastos.database.db import obtener_todos # Importa función para obtener datos de la base de datos

try:
    from flask import Flask # Importa Flask para crear la aplicación web
except Exception: # Maneja la ausencia de Flask
    Flask = None # Asigna None si Flask no está disponible

try:
    from apscheduler.schedulers.background import BackgroundScheduler # Importa el scheduler para tareas en segundo plano
    _HAS_SCHED = True
except Exception:
    _HAS_SCHED = False # Indica que APScheduler no está disponible

LOG = logging.getLogger("inventario_abastos") # Crea un logger para el paquete inventario_abastos
if not LOG.handlers:
    logging.basicConfig(level=logging.INFO) # Configura el logging básico si no hay handlers

# Scheduler global (se inicializa en iniciar_scheduler)
scheduler = None # Variable global para el scheduler

check_low_stock = verificar_bajo_stock # Alias para la función de verificación de bajo stock
check_expiring_items = verificar_items_por_caducar # Alias para la función de verificación de productos por caducar

def send_console(msg, level="info"): # Función para enviar notificaciones a la consola
    print(f"[NOTIFICACIÓN] {msg}") # Imprime el mensaje en la consola

def asegurar_directorio_datos() -> str: # Asegura que el directorio de datos exista y lo devuelve 
    pkg_dir = os.path.dirname(__file__) # Directorio del paquete actual
    data_dir = os.path.join(pkg_dir, "data") # Ruta del directorio de datos
    os.makedirs(data_dir, exist_ok=True) # Crea el directorio si no existe
    LOG.debug(f"Directorio de datos asegurado en: {data_dir}") # Loguea la ruta del directorio de datos
    return data_dir

def crear_app() -> Any:
    if Flask is None:
        LOG.error("Aplicación Flask no disponible.") # Loguea error si Flask no está disponible
        return None
    app = Flask(__name__)
    app.config["JSON_AS_ASCII"] = False # Configura Flask para manejar JSON con UTF-8
    asegurar_directorio_datos() # Asegura que el directorio de datos exista

    try: 
        from inventario_abastos.routes import productos_router, pedidos_router # Importa los routers de productos y pedidos
        if hasattr(productos_router, "db"): # Verifica si el router de productos tiene atributo db
            app.register_blueprint(productos_router.db) # Registra el blueprint de productos
        if hasattr(pedidos_router, "db"): # Verifica si el router de pedidos tiene atributo db
            app.register_blueprint(pedidos_router.db) # Registra el blueprint de pedidos
    except Exception:
        LOG.exception("Error al registrar los routers.") # Loguea cualquier excepción al registrar los routers
    return app

def notificar_y_loguear(title: str, payload) -> None: # Función para notificar y loguear eventos
    mensaje = f"{title}: {payload}" # Construye el mensaje completo
    try:
        send_console(mensaje, level="info") # Envía la notificación a la consola
        LOG.info(mensaje) # Loguea el mensaje como info
    except Exception:
        LOG.exception("Error al enviar notificación") # Loguea cualquier excepción al enviar la notificación

def iniciar_scheduler() -> None: # Función para iniciar el scheduler de tareas en segundo plano
    global scheduler # Declara que se usará la variable global scheduler
    if not _HAS_SCHED:
        LOG.info("APScheduler no está disponible. No se iniciará el scheduler.") # Loguea si APScheduler no está disponible
        return
    scheduler = BackgroundScheduler() # Crea una instancia del scheduler en segundo plano
def producto_bajo_stock():
    productos = obtener_todos("inventario") # Obtiene todos los productos del inventario
    res = producto_bajo_stock(productos) # Verifica productos con bajo stock    
    if res:
        notificar_y_loguear("Productos con bajo stock detectados", res) # Notifica y loguea productos con bajo stock
        return
def productos_por_caducar():
    productos = obtener_todos("inventario") # Obtiene todos los productos del inventario
# Eliminada definición duplicada y lógica de scheduler (ahora en iniciar_scheduler).

    scheduler.start()
    LOG.info("Scheduler iniciado")  # Loguea que el scheduler ha sido iniciado
    atexit.register(lambda: scheduler.shutdown(wait=False)) # Registra el apagado del scheduler al salir

if __name__ == "__main__": # Punto de entrada principal del programa
    app = crear_app() # Crea la aplicación Flask
    iniciar_scheduler() # Inicia el scheduler de tareas en segundo plano
    if app is not None:
        LOG.info("App no creada correctamente.") # Loguea si la app no se creó correctamente
    else:
        LOG.info("App creada correctamente. En http://127.0.0.1:5000") # Loguea que la app se creó correctamente
        app.run(host="127.0.0.1", port=5000, debug=True) # Ejecuta la app Flask en modo debug