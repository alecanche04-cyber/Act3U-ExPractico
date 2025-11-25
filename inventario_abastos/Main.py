
import sys
import os
import logging

# Import adaptativo: intenta nombres en español primero, luego en inglés.
def _safe_import(): # Importa módulos y funciones con nombres en español o inglés
    names = {} # Diccionario para almacenar las referencias importadas
    try:
        from inventario_abastos.controllers.inventario import ( # Importa funciones del controlador de inventario
            verificar_bajo_stock, # Importa funciones del controlador de inventario en español
            verificar_items_por_caducar, # Importa funciones del controlador de inventario en español
            calcular_cantidad_sugerida_orden, # Importa funciones del controlador de inventario en español
        )
        names.update({ # Agrega las funciones importadas al diccionario
            "verificar_bajo_stock": verificar_bajo_stock, # Agrega las funciones importadas al diccionario
            "verificar_items_por_caducar": verificar_items_por_caducar, # Agrega las funciones importadas al diccionario
            "calcular_cantidad_sugerida_orden": calcular_cantidad_sugerida_orden, # Agrega las funciones importadas al diccionario
        })
    except Exception:
        try:
            from inventario_abastos.controllers.inventario import ( # Importa funciones del controlador de inventario en inglés
                check_low_stock,  # Importa funciones del controlador de inventario en inglés
                check_expiring_items,  # Importa funciones del controlador de inventario en inglés
                calculate_suggested_order_qty, # Importa funciones del controlador de inventario en inglés
            )
            names.update({ # Agrega las funciones importadas al diccionario
                "verificar_bajo_stock": check_low_stock, # Agrega las funciones importadas al diccionario
                "verificar_items_por_caducar": check_expiring_items, # Agrega las funciones importadas al diccionario
                "calcular_cantidad_sugerida_orden": calculate_suggested_order_qty, # Agrega las funciones importadas al diccionario
            })
        except Exception:
            pass

    try:
        from inventario_abastos.controllers.pedidos import (
            generar_ordenes_sugeridas, # Importa funciones del controlador de pedidos
            confirmar_orden, # Importa funciones del controlador de pedidos
        )
        names.update({
            "generar_ordenes_sugeridas": generar_ordenes_sugeridas, # Agrega las funciones importadas al diccionario
            "confirmar_orden": confirmar_orden, # Agrega las funciones importadas al diccionario
        })
    except Exception:
        try:
            from inventario_abastos.controllers.pedidos import ( # Importa funciones del controlador de pedidos en inglés
                generate_suggested_orders, # Importa funciones del controlador de pedidos en inglés
                confirm_order, # Importa funciones del controlador de pedidos en inglés
            )
            names.update({
                "generar_ordenes_sugeridas": generate_suggested_orders, # Agrega las funciones importadas al diccionario
                "confirmar_orden": confirm_order, # Agrega las funciones importadas al diccionario
            })
        except Exception:
            pass

    # DB layer: español o inglés
    try:
        from inventario_abastos.database.db import obtener_todos, agregar, actualizar # Importa funciones de la base de datos en español
        names.update({"obtener_todos": obtener_todos, "agregar": agregar, "actualizar": actualizar}) # Agrega las funciones al diccionario
    except Exception:
        try:
            from inventario_abastos.database.db import get_all, add, update # Importa funciones de la base de datos en inglés
            names.update({"obtener_todos": get_all, "agregar": add, "actualizar": update}) # Agrega las funciones al diccionario
        except Exception:
            names.update({"obtener_todos": None, "agregar": None, "actualizar": None}) # Asigna None si no se pueden importar

    # utilidades: limpiar_pantalla, mostrar_titulo, pausar
    try:
        from inventario_abastos.utilidades import limpiar_pantalla, mostrar_titulo, pausar # Importa utilidades en español
        names.update({"limpiar_pantalla": limpiar_pantalla, "mostrar_titulo": mostrar_titulo, "pausar": pausar}) # Agrega las utilidades al diccionario
    except Exception:
        # fallbacks mínimos
        names.update({
            "limpiar_pantalla": lambda: os.system('cls' if os.name == 'nt' else 'clear'), # Limpia la pantalla
            "mostrar_titulo": lambda: print("SISTEMA GENERAL DE INVENTARIO Y PEDIDOS"), # Muestra el título del sistema
            "pausar": lambda: input("Presiona Enter para continuar..."), # Pausa la ejecución hasta que el usuario presione Enter
        })

    return names

_impl = _safe_import() # Diccionario con las implementaciones importadas

LOG = logging.getLogger("inventario_abastos.Main") # Logger específico para este módulo
LOG.setLevel(logging.INFO) # Nivel de logging INFO
if not LOG.handlers:
    ch = logging.StreamHandler() # Crea un handler para la consola
    ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s")) # Formato del log
    LOG.addHandler(ch) # Agrega el handler al logger


def mostrar_menu(): # Muestra el menú principal de opciones
    print("\n" + "-"*50) # Línea separadora
    print("SISTEMA GENERAL DE INVENTARIO Y PEDIDOS") # Título del sistema
    print("-"*50) # Línea separadora
    print("1. Revisar productos con bajo stock") # Opción para revisar productos con bajo stock
    print("2. Revisar productos próximos a caducar") # Opción para revisar productos próximos a caducar
    print("3. Calcular cantidad sugerida para reabastecer") # Opción para calcular cantidad sugerida para reabastecer
    print("4. Generar órdenes sugeridas automáticamente") # Opción para generar órdenes sugeridas automáticamente
    print("5. Registrar una orden manual") # Opción para registrar una orden manual
    print("6. Mostrar todo lo guardado en la base de datos") # Opción para mostrar todo lo guardado en la base de datos
    print("0. Salir del sistema")
    print("-"*50)


def main(): # Función principal que ejecuta el sistema de inventario y pedidos
    limpiar = _impl.get("limpiar_pantalla") # Obtiene la función para limpiar la pantalla
    mostrar_titulo = _impl.get("mostrar_titulo") # Obtiene la función para mostrar el título
    pausar = _impl.get("pausar") # Obtiene la función para pausar la ejecución
    obtener_todos = _impl.get("obtener_todos") # Obtiene la función para obtener todos los registros
    verificar_bajo_stock = _impl.get("verificar_bajo_stock") # Obtiene la función para verificar bajo stock
    verificar_items_por_caducar = _impl.get("verificar_items_por_caducar") # Obtiene la función para verificar items por caducar
    calcular_cantidad_sugerida_orden = _impl.get("calcular_cantidad_sugerida_orden") # Obtiene la función para calcular cantidad sugerida para reabastecer
    generar_ordenes_sugeridas = _impl.get("generar_ordenes_sugeridas") # Obtiene la función para generar órdenes sugeridas automáticamente
    confirmar_orden = _impl.get("confirmar_orden") # Obtiene la función para confirmar una orden
    agregar = _impl.get("agregar") # Obtiene la función para agregar un registro

    while True: # Bucle principal del menú
        limpiar() # Limpia la pantalla
        mostrar_titulo() # Muestra el título
        mostrar_menu() # Muestra el menú
        opcion = input("Seleccione una opción: ").strip() # Solicita al usuario que seleccione una opción

        if opcion == "1": # Opción para revisar productos con bajo stock
            print("\nProductos con bajo stock:") # Muestra los productos con bajo stock
            data = obtener_todos("inventario") if obtener_todos else []     # Obtiene todos los productos del inventario
            if verificar_bajo_stock: # Verifica productos con bajo stock
                print(verificar_bajo_stock(data)) # Muestra los productos con bajo stock
            else:
                print("Función verificar_bajo_stock no disponible.") # Mensaje si la función no está disponible
            pausar()

        elif opcion == "2":
            print("\nProductos próximos a caducar:") # Muestra los productos próximos a caducar
            data = obtener_todos("inventario") if obtener_todos else []     # Obtiene todos los productos del inventario
            if verificar_items_por_caducar: # Verifica productos próximos a caducar
                print(verificar_items_por_caducar(data)) # Muestra los productos próximos a caducar
            else:
                print("Función verificar_items_por_caducar no disponible.") # Mensaje si la función no está disponible
            pausar()

        elif opcion == "3":
            print("\nCálculo de cantidad sugerida:") # Muestra el cálculo de cantidad sugerida para reabastecer
            try:
                stock = int(input("Stock actual: ")) # Solicita el stock actual
                minimo = int(input("Stock mínimo: ")) # Solicita el stock mínimo
                maximo = int(input("Stock máximo: ")) # Solicita el stock máximo
            except ValueError:
                print("Entrada numérica inválida.") # Mensaje si la entrada no es válida
                pausar()
                continue

            if calcular_cantidad_sugerida_orden: # Calcula la cantidad sugerida para reabastecer
                try:
                    sugerido = calcular_cantidad_sugerida_orden(stock, minimo, maximo) # Llama a la función con los parámetros numéricos
                except TypeError:
                    # si la función espera un objeto Producto, llamar de forma segura
                    sugerido = calcular_cantidad_sugerida_orden({"cantidad": stock, "cantidad_minima": minimo}) # Llama a la función con un diccionario simulado
                print(f"Cantidad sugerida: {sugerido}")
            else:
                print("Función calcular_cantidad_sugerida_orden no disponible.") # Mensaje si la función no está disponible
            pausar()

        elif opcion == "4":
            print("\nGenerando órdenes sugeridas...") # Muestra mensaje de generación de órdenes sugeridas
            inventario = obtener_todos("inventario") if obtener_todos else []     # Obtiene todos los productos del inventario
            proveedores = obtener_todos("proveedores") if obtener_todos else []   # Obtiene todos los proveedores
            if generar_ordenes_sugeridas:
                try:
                    ordenes = generar_ordenes_sugeridas(inventario, proveedores) # Genera órdenes sugeridas con inventario y proveedores
                except TypeError:
                    ordenes = generar_ordenes_sugeridas(inventario) # Genera órdenes sugeridas solo con inventario
                print("Órdenes creadas:", ordenes) # Muestra las órdenes creadas
            else:
                print("Función generar_ordenes_sugeridas no disponible.") # Mensaje si la función no está disponible
            pausar()

        elif opcion == "5":
            print("\nRegistrar orden manual") # Muestra mensaje para registrar una orden manual
            producto = input("Producto: ") # Solicita el nombre del producto
            try:
                cantidad = int(input("Cantidad: "))     # Solicita la cantidad del producto
            except ValueError:
                print("Cantidad inválida.") # Mensaje si la cantidad no es válida
                pausar()
                continue
            proveedor = input("Proveedor: ") # Solicita el nombre del proveedor
            if confirmar_orden:
                try:
                    resultado = confirmar_orden(producto, cantidad, proveedor) # Confirma la orden con los parámetros dados
                except TypeError:
                    # intentar variantes: confirmar_orden espera dict o id
                    try:
                        resultado = confirmar_orden({"producto": producto, "cantidad": cantidad, "proveedor": proveedor}) # Llama a la función con un diccionario simulado
                    except Exception as e:
                        resultado = f"Error al confirmar orden: {e}" # Mensaje de error si la confirmación falla
                print(resultado)
            else:
                # si hay función agregar en DB, crear pedido básico
                if agregar:
                    pedido = {"producto": producto, "cantidad": cantidad, "proveedor": proveedor, "estado": "pendiente"} # Crea un diccionario para el pedido
                    saved = agregar("pedidos", pedido) # Agrega el pedido a la base de datos
                    print("Pedido guardado:", saved) # Muestra el pedido guardado
                else:
                    print("No hay función disponible para registrar la orden.") # Mensaje si no hay función para registrar la orden
            pausar()

        elif opcion == "6":
            print("\nContenido de la base de datos:") # Muestra el contenido de la base de datos
            if obtener_todos:
                print("Inventario:", obtener_todos("inventario")) # Muestra el inventario
                print("Proveedores:", obtener_todos("proveedores")) # Muestra los proveedores
                print("Pedidos:", obtener_todos("pedidos")) # Muestra los pedidos
            else:
                print("Capa de persistencia no disponible.") # Mensaje si la capa de persistencia no está disponible
            pausar()

        elif opcion == "0":
            print("Saliendo del sistema...") # Muestra mensaje de salida
            break

        else:
            print("Opción no válida. Intente nuevamente.") # Mensaje para opción no válida
            pausar()


if __name__ == "__main__": # Punto de entrada principal del programa
    main()
