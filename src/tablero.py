import json
import os

def crear_region(fila_inicio, fila_fin, columna_inicio, columna_fin, pista_valor):
    return {
        "fila_inicio": fila_inicio,
        "fila_fin": fila_fin,
        "columna_inicio": columna_inicio,
        "columna_fin": columna_fin,
        "area": pista_valor
    }

def calcular_area_region(region):
    alto = (region["fila_fin"] - region["fila_inicio"]) + 1
    ancho = (region["columna_fin"] - region["columna_inicio"]) + 1
    return ancho * alto

#VALIDACIONES REQUERIDAS

def validar_area_coincide(region):
    return calcular_area_region(region) == region ["area"]

def hay_solapamiento(region1, region2):
    esta_arriba = region1["fila_fin"] < region2["fila_inicio"] 
    esta_abajo = region1["fila_inicio"] > region2["fila_fin"]
    esta_ezquierda = region1["columna_fin"] < region2["columna_inicio"]
    esta_derecha = region1["columna_inicio"] > region2["columna_fin"] 

    if esta_arriba or esta_abajo or esta_derecha or esta_ezquierda:
        return False
    
    return True

def validar_todas_las_regiones(regiones):
    for i in range(len(regiones)):
        for j in range(i + 1, len(regiones)):
            if hay_solapamiento(regiones[i], regiones[j]):
                return False
    return True

def tablero_completamente_cubierto(regiones, filas, columnas):
    area_total_tablero = filas * columnas
    area_cubierta = sum(calcular_area_region(r) for r in regiones)

    return area_cubierta == area_total_tablero

#MANEJO Y LECTURA DE TABLEROS 

def cargar_tablero_desde_json(ruta_archivo):

    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    ruta_absoluta = os.path.normpath(os.path.join(directorio_actual, ruta_archivo))

    try:
        with open(ruta_absoluta, 'r') as archivo:
            datos = json.load(archivo)
            return datos["tablero"]
    except FileNotFoundError:
        print(f"Error: El archivo {ruta_archivo} no existe.")
        return None    