"""
Módulo de gestión del tablero de Shikaku.

Este módulo proporciona funciones para:
- Crear y manipular regiones del tablero
- Validar regiones (área, solapamiento, cobertura)
- Cargar tableros desde archivos JSON

Una región es un rectángulo que debe cubrirse con un área igual a la pista numérica.
"""

import json
import os

def crear_region(fila_inicio, fila_fin, columna_inicio, columna_fin, pista_valor):
    """Crea una estructura de diccionario que representa una región del tablero.
    
    Args:
        fila_inicio: Índice de la fila inicial del rectángulo
        fila_fin: Índice de la fila final del rectángulo
        columna_inicio: Índice de la columna inicial del rectángulo
        columna_fin: Índice de la columna final del rectángulo
        pista_valor: El valor de la pista (área esperada de la región)
    
    Returns:
        dict: Diccionario con las coordenadas y área de la región
    """
    return {
        "fila_inicio": fila_inicio,
        "fila_fin": fila_fin,
        "columna_inicio": columna_inicio,
        "columna_fin": columna_fin,
        "area": pista_valor
    }

def calcular_area_region(region):
    """Calcula el área total de una región rectangular por sus coordenadas.
    
    Args:
        region: Diccionario con coordenadas (fila_inicio, fila_fin, columna_inicio, columna_fin)
    
    Returns:
        int: El área total de la región (alto × ancho)
    """
    alto = (region["fila_fin"] - region["fila_inicio"]) + 1
    ancho = (region["columna_fin"] - region["columna_inicio"]) + 1
    return ancho * alto

# ==================== VALIDACIONES REQUERIDAS ====================
# Estas funciones verifican que las regiones cumplan con las reglas del Shikaku

def validar_area_coincide(region):
    """Valida que el área de una región sea igual a su pista.
    
    En Shikaku, cada región debe tener un área exacta igual al número de su pista.
    
    Args:
        region: Diccionario con coordenadas y área esperada
    
    Returns:
        bool: True si el área coincide con la pista, False en caso contrario
    """
    return calcular_area_region(region) == region["area"]

def hay_solapamiento(region1, region2):
    """Detecta si dos regiones rectangulares se solapan.
    
    Comprueba todas las direcciones posibles (arriba, abajo, izquierda, derecha).
    Si las regiones no se tocan en ninguna dirección, no hay solapamiento.
    
    Args:
        region1: Primera región
        region2: Segunda región
    
    Returns:
        bool: True si las regiones se solapan, False si no hay solapamiento
    """
    esta_arriba = region1["fila_fin"] < region2["fila_inicio"] 
    esta_abajo = region1["fila_inicio"] > region2["fila_fin"]
    esta_izquierda = region1["columna_fin"] < region2["columna_inicio"]
    esta_derecha = region1["columna_inicio"] > region2["columna_fin"] 

    if esta_arriba or esta_abajo or esta_derecha or esta_izquierda:
        return False
    
    return True

def validar_todas_las_regiones(regiones):
    """Valida que no haya solapamiento entre ninguna par de regiones.
    
    Comprueba todas las combinaciones posibles de regiones para detectar
    si algún par de ellas se solapa.
    
    Args:
        regiones: Lista de regiones a validar
    
    Returns:
        bool: True si todas las regiones son válidas (sin solapamientos), False si hay solapamiento
    """
    for i in range(len(regiones)):
        for j in range(i + 1, len(regiones)):
            if hay_solapamiento(regiones[i], regiones[j]):
                return False
    return True

def tablero_completamente_cubierto(regiones, filas, columnas):
    """Verifica que todas las celdas del tablero estén cubierta por regiones.
    
    En Shikaku, la solución es válida solo si todas las celdas del tablero
    están cubierta por exactamente una región sin dejar espacios vacíos.
    
    Args:
        regiones: Lista de regiones dibujadas
        filas: Número de filas del tablero
        columnas: Número de columnas del tablero
    
    Returns:
        bool: True si el tablero está completamente cubierto, False en caso contrario
    """
    area_total_tablero = filas * columnas
    area_cubierta = sum(calcular_area_region(r) for r in regiones)

    return area_cubierta == area_total_tablero

# ==================== MANEJO Y LECTURA DE TABLEROS ====================
# Funciones para cargar y manipular tableros desde archivos JSON

def cargar_tablero_desde_json(ruta_archivo):
    """Carga un tablero de Shikaku desde un archivo JSON.
    
    La función busca el archivo JSON en una ruta relativa al módulo actual.
    El archivo debe contener una clave "tablero" con la matriz de números.
    
    Args:
        ruta_archivo: Ruta relativa del archivo JSON a cargar
    
    Returns:
        list: Matriz 2D del tablero, o None si hay error de lectura
    
    Estructura esperada del JSON:
        {
            "tablero": [
                [2, 0, 4, 0],
                [0, 0, 0, 0],
                [3, 0, 2, 0],
                [0, 0, 0, 0]
            ]
        }
    """
    # Obtener el directorio actual del módulo
    directorio_actual = os.path.dirname(os.path.abspath(__file__))

    # Construir la ruta absoluta del archivo
    ruta_absoluta = os.path.normpath(os.path.join(directorio_actual, ruta_archivo))

    try:
        # Abrir y cargar el archivo JSON
        with open(ruta_absoluta, 'r') as archivo:
            datos = json.load(archivo)
            return datos["tablero"]
    except FileNotFoundError:
        # Mostrar error si el archivo no se encuentra
        print(f"Error: El archivo {ruta_archivo} no existe.")
        return None
