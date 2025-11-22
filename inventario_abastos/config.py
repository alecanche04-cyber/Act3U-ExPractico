import os # Importa el módulo os para manejar rutas de archivos
from pathlib import Path  # Importa Path para manejar rutas de archivos de manera más conveniente

BASE_DIR = Path(__file__).resolve().parent  # Directorio base del proyecto
DATA_DIR = os.environ.get("DATA_DIR", str(BASE_DIR / "data"))  # Directorio de datos, puede ser configurado mediante variable de entorno
DEBUG = os.environ.get("DEBUG", "1") == "1"  # Modo de depuración, activado por defecto
SECRET_KEY = os.environ.get("SECRET_KEY", "cambiame_ahora")  # Clave secreta para la aplicación

TABLAS_JSON = { # Nombres de tablas JSON para almacenar datos
    "productos":"productos", # Tabla de productos
    "proveedores":"proveedores", # Tabla de proveedores
    "pedidos":"pedidos", # Tabla de pedidos
    "lotes":"lotes", # Tabla de lotes
} 

PLANIFICADOR = {
    "dias_revision_caducidad": int(os.environ.get("DIAS_REVISION_CADUCIDAD", "7")), # Días para revisar caducidad de productos
    "cron_revisar_stock_bajo": os.environ.get("CRON_STOCK_BAJO", "0 8 ** LUN"), # Cron para revisar stock bajo (lunes a las 8 AM)
}

SMTP = { # Configuración del servidor SMTP para envío de correos
    "servidor": os.environ.get("SMTP_SERVIDOR", ""), # Dirección del servidor de correo 
    "puerto": int(os.environ.get("SMTP_PUERTO", "587") or 587), # Puerto de conexión 
    "usuario": os.environ.get("SMTP_USUARIO", ""), # Usuario para autenticación
    "contrasena": os.environ.get("SMTP_CONTRASENA", ""), # Contraseña usuario 
    "remitente": os.environ.get("SMTP_REMITENTE", "alecanche04@gmail.com"), # Dirección de corre de quien envía los correos
}