# -----------------------------------------------------
# Ejecutar inventario y pedidos
# -----------------------------------------------------
from inventario_abastos.controllers.inventario import ( # Importar funciones del módulo inventario
    verificar_bajo_stock,  # Función para verificar productos con bajo stock
    verificar_items_por_caducar,  # Función para verificar productos próximos a caducar
    calcular_cantidad_sugerida_orden  # Función para calcular cantidad sugerida para reabastecer
)
from inventario_abastos.controllers.pedidos import ( # Importar funciones del módulo pedidos
    generar_ordenes_sugeridas,  # Función para generar órdenes sugeridas automáticamente
    confirmar_orden  # Función para confirmar una orden manual
) 
from inventario_abastos.database.db import obtener_todos, agregar, actualizar # Importar funciones de la base de datos
from inventario_abastos. utilidades import limpiar_pantalla, mostrar_titulo, pausar # Importar utilidades de la aplicación
import sys # Importar módulo sys para manipulación del sistema
import os # Importar módulo os para manejo de rutas de archivos
sys.path.append(os.path.dirname(os.path.abspath(__file__))) # Asegura que el directorio actual esté en el path


    
def mostrar_menu(): # Muestra el menú principal de opciones
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


def main(): # Función principal para ejecutar el sistema de inventario y pedidos
    while True:
        limpiar_pantalla() # Limpia la pantalla de la consola
        mostrar_titulo() # Muestra el título decorativo
    
        mostrar_menu()
        opcion = input("Seleccione una opción: ") # Solicita al usuario seleccionar una opción del menú

        if opcion == "1":
            print("\nProductos con bajo stock:") # Muestra productos con bajo stock
            productos = obtener_todos("inventario") # Obtiene todos los productos del inventario
            print(verificar_bajo_stock(productos)) # Verifica y muestra productos con bajo stock

        elif opcion == "2":
            print("\nProductos próximos a caducar:") # Muestra productos próximos a caducar
            productos = obtener_todos("inventario") # Obtiene todos los productos del inventario
            print(verificar_items_por_caducar(productos)) # Verifica y muestra productos próximos a caducar

        elif opcion == "3":
            print("\nCálculo de cantidad sugerida:") # Calcula cantidad sugerida para reabastecer un producto
            stock = int(input("Stock actual: ")) # Solicita al usuario ingresar el stock actual
            minimo = int(input("Stock mínimo: ")) # Solicita al usuario ingresar el stock mínimo
            maximo = int(input("Stock máximo: ")) # Solicita al usuario ingresar el stock máximo
            sugerido = calcular_cantidad_sugerida_orden(stock, minimo, maximo) # Calcula la cantidad sugerida para reabastecer
            print(f"Cantidad sugerida: {sugerido}") # Muestra la cantidad sugerida para reabastecer

        elif opcion == "4":
            print("\nGenerando órdenes sugeridas...") # Genera órdenes sugeridas automáticamente
            inventario = obtener_todos("inventario") # Obtiene todos los productos del inventario
            proveedores = obtener_todos("proveedores") # Obtiene todos los proveedores
            ordenes = generar_ordenes_sugeridas(inventario, proveedores) # Genera órdenes sugeridas basadas en inventario y proveedores
            print("Órdenes creadas:", ordenes) # Muestra las órdenes creadas
        elif opcion == "5":
            print("\nRegistrar orden manual") # Registra una orden manualmente
            producto = input("Producto: ") # Solicita al usuario ingresar el nombre del producto
            cantidad = int(input("Cantidad: ")) # Solicita al usuario ingresar la cantidad
            proveedor = input("Proveedor: ") # Solicita al usuario ingresar el nombre del proveedor
            resultado = confirmar_orden(producto, cantidad, proveedor) # Confirma la orden con los datos ingresados
            print(resultado) # Muestra el resultado de la confirmación de la orden

        elif opcion == "6":
            print("\nContenido de la base de datos:") # Muestra todo lo guardado en la base de datos
            print("Inventario:", obtener_todos("inventario")) # Muestra el inventario
            print("Proveedores:", obtener_todos("proveedores")) # Muestra los proveedores
            print("Pedidos:", obtener_todos("pedidos")) # Muestra los pedidos

        elif opcion == "0":
            print("Saliendo del sistema...") # Sale del sistema
            sys.exit()

        else:
            print("Opción no válida. Intente nuevamente.") # Maneja opciones no válidas

if __name__ == "__main__": # Ejecuta la función
    main()  # Ejecuta la función principal del sistema de inventario y pedidos
    pausar() # Pausa la ejecución hasta que el usuario presione Enter