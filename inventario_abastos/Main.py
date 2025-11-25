# -----------------------------------------------------
# Ejecutar inventario y pedidos
# -----------------------------------------------------

from controllers.inventario import (
    verificar_bajo_stock,
    verificar_items_por_caducar,
    calcular_cantidad_sugerida_orden
)

from controllers.pedidos import (
    generar_ordenes_sugeridas,
    confirmar_orden
)

from database.db import agregar, actualizar, obtener_todos
from models.proveedor import Proveedor
from models.inventario import Producto

import sys


def mostrar_menu():
    print("\n" + "-"*50)
    print("SISTEMA GENERAL DE INVENTARIO Y PEDIDOS")
    print("-"*50)
    print("1. Revisar productos con bajo stock")
    print("2. Revisar productos próximos a caducar")
    print("3. Calcular cantidad sugerida para reabastecer")
    print("4. Generar órdenes sugeridas automáticamente")
    print("5. Registrar una orden manual")
    print("6. Mostrar todo lo guardado en la base de datos")
    print("0. Salir del sistema")
    print("-"*50)


def main():
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            print("\nProductos con bajo stock:")
            productos = obtener_todos("inventario")
            print(verificar_bajo_stock(productos))

        elif opcion == "2":
            print("\nProductos próximos a caducar:")
            productos = obtener_todos("inventario")
            print(verificar_items_por_caducar(productos))

        elif opcion == "3":
            print("\nCálculo de cantidad sugerida:")
            stock = int(input("Stock actual: "))
            minimo = int(input("Stock mínimo: "))
            maximo = int(input("Stock máximo: "))
            sugerido = calcular_cantidad_sugerida_orden(stock, minimo, maximo)
            print(f"Cantidad sugerida: {sugerido}")

        elif opcion == "4":
            print("\nGenerando órdenes sugeridas...")
            inventario = obtener_todos("inventario")
            proveedores = obtener_todos("proveedores")
            ordenes = generar_ordenes_sugeridas(inventario, proveedores)
            print("Órdenes creadas:", ordenes)

        elif opcion == "5":
            print("\nRegistrar orden manual")
            producto = input("Producto: ")
            cantidad = int(input("Cantidad: "))
            proveedor = input("Proveedor: ")
            resultado = confirmar_orden(producto, cantidad, proveedor)
            print(resultado)

        elif opcion == "6":
            print("\nContenido de la base de datos:")
            print("Inventario:", obtener_todos("inventario"))
            print("Proveedores:", obtener_todos("proveedores"))
            print("Pedidos:", obtener_todos("pedidos"))

        elif opcion == "0":
            print("Saliendo del sistema...")
            sys.exit()

        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()
