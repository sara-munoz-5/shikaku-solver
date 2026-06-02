"""
Módulo solucionador de Shikaku usando Backtracking.

Este módulo implementa un algoritmo de fuerza bruta con retroceso (backtracking)
para resolver puzzles de Shikaku. El proceso es:

1. Extraer todas las pistas numéricas del tablero
2. Para cada pista, generar todos los rectángulos candidatos válidos
3. Usar backtracking para encontrar una combinación de rectángulos que:
   - Cubra completamente el tablero
   - No tenga solapamientos
   - Cada rectángulo tenga área igual a su pista

Complejidad: O(n!) en el peor caso, donde n es el número de pistas
"""

def obtener_pistas(tablero):
    """Extrae todas las pistas numéricas del tablero.
    
    Las pistas son celdas con valores mayores a 0. Cada pista indica
    el área que debe cubrir la región que contiene esa celda.
    
    Args:
        tablero: Matriz 2D donde 0 representa celda vacía, >0 es una pista
    
    Returns:
        list: Lista de diccionarios con formato:
              {"fila": int, "columna": int, "valor": int}
    """
    pistas = []

    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            if tablero[fila][columna] != 0:
                pistas.append({
                    "fila": fila,
                    "columna": columna,
                    "valor": tablero[fila][columna]
                })

    return pistas

def contiene_otra_pista(rectangulo, pista_original, tablero):
    """Verifica si un rectángulo contiene pistas adicionales.
    
    En Shikaku, cada región debe contener exactamente una pista.
    Esta función detecta si un rectángulo candidato contiene más de una pista.
    
    Args:
        rectangulo: Diccionario con coordenadas del rectángulo
        pista_original: Diccionario de la pista que genera este rectángulo
        tablero: Matriz del tablero completo
    
    Returns:
        bool: True si hay otras pistas en el rectángulo, False si solo está la original
    """
    fila_inicio = rectangulo["fila_inicio"]
    fila_fin = rectangulo["fila_fin"]
    columna_inicio = rectangulo["columna_inicio"]
    columna_fin = rectangulo["columna_fin"]

    for fila in range(fila_inicio, fila_fin + 1):
        for columna in range(columna_inicio, columna_fin + 1):
            if tablero[fila][columna] != 0:
                if fila != pista_original["fila"] or columna != pista_original["columna"]:
                    return True

    return False


def generar_candidatos(pista, tablero):
    """Genera todos los rectángulos válidos para una pista.
    
    Para cada pista, se generan todos los rectángulos posibles que:
    - Tengan un área igual al valor de la pista
    - Contengan la celda con la pista
    - Estén dentro de los límites del tablero
    - No contengan otras pistas
    
    Args:
        pista: Diccionario con {"fila", "columna", "valor"}
        tablero: Matriz del tablero completo
    
    Returns:
        list: Lista de rectángulos válidos, cada uno es un diccionario con:
              {"fila_inicio", "fila_fin", "columna_inicio", "columna_fin", "area", "pista"}
    """
    candidatos = []

    filas = len(tablero)
    columnas = len(tablero[0])

    valor = pista["valor"]
    fila_pista = pista["fila"]
    columna_pista = pista["columna"]

    # Iterar sobre todos los posibles divisores del área
    for alto in range(1, valor + 1):
        if valor % alto == 0:
            ancho = valor // alto

            # Generar todas las posiciones posibles del rectángulo
            for fila_inicio in range(fila_pista - alto + 1, fila_pista + 1):
                for columna_inicio in range(columna_pista - ancho + 1, columna_pista + 1):

                    fila_fin = fila_inicio + alto - 1
                    columna_fin = columna_inicio + ancho - 1

                    # Verificar que el rectángulo esté dentro del tablero
                    esta_dentro = (
                        fila_inicio >= 0 and
                        columna_inicio >= 0 and
                        fila_fin < filas and
                        columna_fin < columnas
                    )

                    if esta_dentro:
                        rectangulo = {
                            "fila_inicio": fila_inicio,
                            "fila_fin": fila_fin,
                            "columna_inicio": columna_inicio,
                            "columna_fin": columna_fin,
                            "area": valor,
                            "pista": pista
                        }

                        # Verificar que no contenga otras pistas
                        if not contiene_otra_pista(rectangulo, pista, tablero):
                            candidatos.append(rectangulo)

    return candidatos

def revisar_solapamiento(rect1, rect2):
    """Verifica si dos rectángulos se solapan.
    
    Dos rectángulos no se solapan si uno está completamente arriba, abajo,
    a la izquierda o a la derecha del otro.
    
    Args:
        rect1: Primer rectángulo
        rect2: Segundo rectángulo
    
    Returns:
        bool: True si los rectángulos se solapan, False en caso contrario
    """
    return not (
        rect1["fila_fin"] < rect2["fila_inicio"] or 
        rect1["fila_inicio"] > rect2["fila_fin"] or
        rect1["columna_fin"] < rect2["columna_inicio"] or
        rect1["columna_inicio"] > rect2["columna_fin"]
    )

def resolver_shikaku(tablero):
    """Resuelve un puzzle de Shikaku usando backtracking.
    
    Implementa un algoritmo de búsqueda exhaustiva con retroceso que:
    1. Genera candidatos para cada pista
    2. Intenta asignar rectángulos sin que se solapan
    3. Si encuentra una solución válida completa, la retorna
    4. Si no encuentra solución, retorna None
    
    Args:
        tablero: Matriz 2D del puzzle (0 = vacío, >0 = pista)
    
    Returns:
        list: Lista de rectángulos de la solución, o None si no hay solución
    """
    # Extraer todas las pistas del tablero
    pistas = obtener_pistas(tablero)

    # Generar candidatos para cada pista
    candidatos_por_pista = []

    for pista in pistas:
        candidatos = generar_candidatos(pista, tablero)
        # Si no hay candidatos válidos para una pista, no hay solución
        if not candidatos:
            return None 
        candidatos_por_pista.append(candidatos)

    # Lista para ir guardando la solución parcial
    solucion_actual = []

    def backtracking(indice_pista):
        """Función interna recursiva que implementa el backtracking.
        
        Intenta asignar un rectángulo a cada pista sin crear solapamientos.
        
        Args:
            indice_pista: Índice de la pista actual a resolver
        
        Returns:
            bool: True si se encontró una solución completa, False en caso contrario
        """
        # Caso base: todas las pistas han sido asignadas
        if indice_pista == len(pistas):
            return True

        # Probar cada candidato para la pista actual
        for candidato in candidatos_por_pista[indice_pista]:
            choca = False
            
            # Verificar si este candidato se solapa con algún rectángulo ya aceptado
            for rect_aceptado in solucion_actual:
                if revisar_solapamiento(candidato, rect_aceptado):
                    choca = True
                    break

            # Si no hay solapamiento, usar este candidato
            if not choca:
                solucion_actual.append(candidato)

                # Intentar resolver la siguiente pista
                if backtracking(indice_pista + 1):
                    return True
                
                # Si no funcionó, retroceder
                solucion_actual.pop()

        return False

    # Ejecutar el backtracking desde la primera pista
    if backtracking(0):
        return solucion_actual
    return None
