# utilidades

from datetime import date
import random

# Genera un ID tomando la cantidad de elementos dentro de una lista.
# Es suficiente para este proyecto de inventario.
def generar_id(lista):
    return len(lista) + 1


# Estructura estándar para todas las respuestas que devuelven los endpoints.
def formatear_respuesta(mensaje: str, datos: dict = None):
    return {
        "mensaje": mensaje,
        "datos": datos
    }


# Calcula cuántos días faltan para que un producto caduque.
def dias_para_caducar(caducidad: date):
    hoy = date.today()
    return (caducidad - hoy).days


# Revisa si el stock está igual o por debajo del mínimo permitido.
def validar_stock(stock: int, minimo: int):
    return stock <= minimo


# Genera un código corto para productos o pedidos, fácil de leer.
def generar_codigo_random():
    return "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=4))


def limpiar_pantalla():
    #Limpia la pantalla de la consola como si fuera una nueva 
    import os
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/Mac
        os.system('clear')

def mostrar_titulo(): #Muestra un título decorativo en la consola

    print("╔" + "═" * 38 + "╗")
    print("║     INVENTARIO DE ABASTO                 ║")
    print("║              ¡Bienvenido!                ║")
    print("╚" + "═" * 38 + "╝")
    


def pausar():

#Pausa la ejecución hasta que el usuario presione Enter
    #input(): se usara para mostara un mensasje y esperar a que el usuario presione Enter

    input("\n---Presiona Enter para continuar---")

