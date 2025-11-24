# services/notificaciones.py

from utilidades.config import EMAIL_ADMIN, CANAL_NOTIFICACION

# SERVICIOS DE GESTIÓN DE NOTIFICACIONES (EMAIL/MENSAJE)

def enviar_notificacion_stock_bajo(alerta_stock):
    """
    Envía una notificación al administrador sobre un producto con stock bajo.
    :param alerta_stock: Diccionario de la alerta de stock generada en alertas.py.
    """
    prod_nombre = alerta_stock["nombre"]
    stock = alerta_stock["stock_actual"]
    minimo = alerta_stock["umbral_minimo"]

    asunto = f"[ALERTA URGENTE] Stock Bajo: {prod_nombre}"
    cuerpo = f"""
    Estimado(a) Administrador(a),

    El producto "{prod_nombre}" ha caído por debajo del umbral de stock mínimo.
    - Stock Actual: {stock} unidades.
    - Stock Mínimo Requerido: {minimo} unidades.

    Por favor, revise el resumen de pedidos generado y contacte al proveedor.
    """
    _simular_envio(asunto, cuerpo)


def enviar_notificacion_caducidad_proxima(alerta_caducidad):
    """
    Envía una notificación al administrador sobre un producto con caducidad próxima.
    :param alerta_caducidad: Diccionario de la alerta de caducidad.
    """
    prod_nombre = alerta_caducidad["nombre"]
    fecha_cad = alerta_caducidad["fecha_caducidad"]
    dias = alerta_caducidad["dias_restantes"]

    asunto = f"[ALERTA INVENTARIO] Caducidad Próxima: {prod_nombre}"
    cuerpo = f"""
    Estimado(a) Administrador(a),

    El producto "{prod_nombre}" está a punto de caducar.
    - Fecha de Caducidad: {fecha_cad}.
    - Días Restantes: {dias} días.

    Se recomienda aplicar descuentos o tomar medidas antes de que sea una pérdida.
    """
    _simular_envio(asunto, cuerpo)


def enviar_resumen_pedidos(resumen_pedidos):
    """
    Envía el resumen de los pedidos necesarios al administrador para su revisión
    y gestión con los proveedores (eliminando la descentralización).
    :param resumen_pedidos: Diccionario de pedidos agrupados por proveedor.
    """
    asunto = "[REPORTE] Resumen Diario/Semanal de Pedidos a Proveedores"
    cuerpo = "A continuación se detalla el resumen de los productos a pedir:\n\n"

    for prov_id, data in resumen_pedidos.items():
        cuerpo += f"PROVEEDOR: {data['nombre']} (Contacto: {data['contacto']})\n"

        for prod in data["productos"]:
            cuerpo += f"- Producto: {prod['nombre']}\n"
            cuerpo += f"  Stock: {prod['stock_actual']} | Mínimo: {prod['stock_minimo']} | *PEDIR: {prod['cantidad_a_pedir']}*\n"
        cuerpo += "\n"

    _simular_envio(asunto, cuerpo)


def _simular_envio(asunto, cuerpo):
    """
    Función interna para simular el envío de un email o mensaje.
    """
    print(f"\n<<< INICIO SIMULACIÓN ENVÍO DE {CANAL_NOTIFICACION.upper()} >>>")
    print(f"DESTINO: {EMAIL_ADMIN}")
    print(f"ASUNTO: {asunto}")
    print(f"CUERPO: {cuerpo}")
    print(f"<<< FIN SIMULACIÓN ENVÍO >>>\n")

