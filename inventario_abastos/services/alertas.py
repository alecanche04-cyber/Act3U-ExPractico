# services/alertas.py

from datetime import datetime
from utilidades.helpers import obtener_todos_los_productos, obtener_info_proveedor, formatear_fecha
from utilidades.config import UMBRALES_STOCK_MINIMO, STOCK_MINIMO_GENERICO, DIAS_ALERTA_CADUCIDAD

# SERVICIOS DE GESTIÓN DE ALERTAS (STOCK Y CADUCIDAD)

def obtener_umbral_stock(producto_id):
    """
    Devuelve el umbral de stock mínimo específico para un producto,
    o el genérico si no se encuentra en la configuración.
    :param producto_id: ID del producto.
    :return: Cantidad mínima de stock.
    """
    # Utiliza .get() para obtener el valor o el genérico por defecto.
    return UMBRALES_STOCK_MINIMO.get(producto_id, STOCK_MINIMO_GENERICO)


def revisar_inventario_stock():
    """
    Revisa el stock actual de todos los productos y genera una lista
    de alertas de stock bajo (necesidad de reponer un producto - punto 1).
    :return: Lista de productos con stock bajo.
    """
    productos = obtener_todos_los_productos()
    alertas_stock = []

    print("-> [ALERTA] Revisando niveles de stock...")

    for prod in productos:
        # Obtiene el umbral específico para el producto
        umbral_minimo = obtener_umbral_stock(prod["id"])

        if prod["stock_actual"] <= umbral_minimo:
            # Producto por debajo o en el umbral de seguridad
            alerta = {
                "tipo": "STOCK_BAJO",
                "producto_id": prod["id"],
                "nombre": prod["nombre"],
                "stock_actual": prod["stock_actual"],
                "umbral_minimo": umbral_minimo,
                "proveedor": obtener_info_proveedor(prod["proveedor_id"])
            }
            alertas_stock.append(alerta)
            print(f"   [!] ALERTA STOCK BAJO: {prod['nombre']} ({prod['stock_actual']} uds.)")

    return alertas_stock


def revisar_inventario_caducidad():
    """
    Revisa las fechas de caducidad y genera una lista de alertas
    para productos con vencimiento cercano.
    :return: Lista de productos con caducidad próxima.
    """
    productos = obtener_todos_los_productos()
    alertas_caducidad = []
    fecha_limite = datetime.now() + timedelta(days=DIAS_ALERTA_CADUCIDAD)

    print(f"-> [ALERTA] Revisando caducidades (en los próximos {DIAS_ALERTA_CADUCIDAD} días)...")

    for prod in productos:
        # Compara la fecha de caducidad con la fecha límite de alerta
        if prod["fecha_caducidad"] <= fecha_limite:
            # Producto con fecha de caducidad cercana
            dias_restantes = (prod["fecha_caducidad"] - datetime.now()).days

            alerta = {
                "tipo": "CADUCIDAD_PROXIMA",
                "producto_id": prod["id"],
                "nombre": prod["nombre"],
                "stock_actual": prod["stock_actual"],
                "fecha_caducidad": formatear_fecha(prod["fecha_caducidad"]),
                "dias_restantes": dias_restantes,
            }
            alertas_caducidad.append(alerta)
            print(f"   [!] ALERTA CADUCIDAD: {prod['nombre']} ({dias_restantes} días rest.)")

    return alertas_caducidad


def generar_resumen_pedidos(alertas_stock_bajo):
    """
    Agrupa las alertas de stock bajo por proveedor y genera un resumen
    para el pedido (simulando la eliminación de la 'hoja de papel' - punto 2).
    :param alertas_stock_bajo: Lista de diccionarios de alertas de stock.
    :return: Diccionario agrupado por proveedor.
    """
    pedidos_por_proveedor = {}
    print("-> [PEDIDOS] Generando resumen de pedidos por proveedor...")

    for alerta in alertas_stock_bajo:
        prov_id = alerta["proveedor"]["id"] if alerta.get("proveedor") else "SIN_PROVEEDOR"
        prov_nombre = alerta["proveedor"]["nombre"] if alerta.get("proveedor") else "SIN PROVEEDOR ASIGNADO"

        if prov_id not in pedidos_por_proveedor:
            pedidos_por_proveedor[prov_id] = {
                "nombre": prov_nombre,
                "contacto": alerta["proveedor"]["contacto"] if alerta.get("proveedor") else "N/A",
                "productos": []
            }

        # Cálculo simple: pedir 10 unidades más que el stock mínimo,
        # o 10 unidades si es stock bajo por debajo de 5.
        cantidad_a_pedir = alerta["umbral_minimo"] + 10

        pedidos_por_proveedor[prov_id]["productos"].append({
            "nombre": alerta["nombre"],
            "stock_actual": alerta["stock_actual"],
            "stock_minimo": alerta["umbral_minimo"],
            "cantidad_a_pedir": cantidad_a_pedir
        })
        print(f"   [*] Agregar a pedido de {prov_nombre}: {alerta['nombre']} (pedir {cantidad_a_pedir})")


    return pedidos_por_proveedor