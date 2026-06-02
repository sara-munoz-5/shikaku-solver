def obtener_pistas(tablero):
    """
    Recorre el tablero y obtiene todas las pistas numéricas.
    Cada pista representa una celda con un número mayor que 0.
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


def hay_solapamiento_con_lista(region, regiones):
    """
    Verifica si una región solapa con alguna región en la lista.
    """
    for r in regiones:
        # Dos rectángulos NO solapan si:
        # - uno está completamente arriba del otro
        # - uno está completamente abajo del otro
        # - uno está completamente a la izquierda del otro
        # - uno está completamente a la derecha del otro
        
        esta_arriba = region["fila_fin"] < r["fila_inicio"]
        esta_abajo = region["fila_inicio"] > r["fila_fin"]
        esta_izquierda = region["columna_fin"] < r["columna_inicio"]
        esta_derecha = region["columna_inicio"] > r["columna_fin"]
        
        if not (esta_arriba or esta_abajo or esta_izquierda or esta_derecha):
            return True
    
    return False


def puede_asignarse_pista(pista, candidatos, regiones_asignadas):
    """
    Filtra los candidatos de una pista que no solapan con las regiones ya asignadas.
    Retorna solo los candidatos válidos.
    """
    candidatos_validos = []
    for candidato in candidatos:
        if not hay_solapamiento_con_lista(candidato, regiones_asignadas):
            candidatos_validos.append(candidato)
    return candidatos_validos
def contiene_otra_pista(rectangulo, pista_original, tablero):
    """
    Verifica si un rectángulo contiene una pista diferente
    a la pista que está intentando resolver.
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
    """
    Genera todos los rectángulos posibles para una pista.
    Cada rectángulo debe:
    - tener un área igual al valor de la pista,
    - contener la celda de la pista,
    - estar dentro del tablero,
    - no contener otra pista.
    """
    candidatos = []

    filas = len(tablero)
    columnas = len(tablero[0])

    valor = pista["valor"]
    fila_pista = pista["fila"]
    columna_pista = pista["columna"]

    for alto in range(1, valor + 1):
        if valor % alto == 0:
            ancho = valor // alto

            for fila_inicio in range(fila_pista - alto + 1, fila_pista + 1):
                for columna_inicio in range(columna_pista - ancho + 1, columna_pista + 1):

                    fila_fin = fila_inicio + alto - 1
                    columna_fin = columna_inicio + ancho - 1

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

                        if not contiene_otra_pista(rectangulo, pista, tablero):
                            candidatos.append(rectangulo)

    return candidatos


# ════════════════════════════════════════════════════════════════════════════════════════════
# SOLUCIONADOR SINTÉTICO - BACKTRACKING CON HEURÍSTICAS
# ════════════════════════════════════════════════════════════════════════════════════════════

def _backtrack_resolver(pistas, indice_pista, candidatos_por_pista, regiones_asignadas, tablero):
    """
    Algoritmo recursivo de backtracking para resolver el Shikaku.
    
    Args:
        pistas: lista de todas las pistas del tablero
        indice_pista: índice de la pista actual a resolver
        candidatos_por_pista: diccionario con candidatos válidos por índice de pista
        regiones_asignadas: lista de regiones ya asignadas (construcción incremental)
        tablero: el tablero original (para validaciones)
    
    Returns:
        Lista de regiones si encuentra solución, None si no la encuentra
    """
    
    # CASO BASE: todas las pistas han sido asignadas
    if indice_pista == len(pistas):
        # Verificar que el tablero esté completamente cubierto
        from tablero import tablero_completamente_cubierto
        filas = len(tablero)
        columnas = len(tablero[0])
        
        if tablero_completamente_cubierto(regiones_asignadas, filas, columnas):
            return regiones_asignadas[:]  # Retornar copia de la solución
        else:
            return None
    
    # CASO RECURSIVO: intentar asignar la pista actual
    pista_actual = pistas[indice_pista]
    candidatos_totales = candidatos_por_pista[indice_pista]
    
    # Si no hay candidatos válidos para esta pista, es un camino sin salida
    if not candidatos_totales:
        return None
    
    # Filtrar candidatos que no solapan con regiones ya asignadas
    candidatos_validos = puede_asignarse_pista(pista_actual, candidatos_totales, regiones_asignadas)
    
    # Si después de filtrar no quedan candidatos, backtrack
    if not candidatos_validos:
        return None
    
    # Intentar cada candidato válido para esta pista
    for candidato in candidatos_validos:
        # Asignar el candidato
        regiones_asignadas.append(candidato)
        
        # Avanzar a la siguiente pista
        resultado = _backtrack_resolver(
            pistas, 
            indice_pista + 1, 
            candidatos_por_pista, 
            regiones_asignadas, 
            tablero
        )
        
        # Si encontramos solución, retornarla
        if resultado is not None:
            return resultado
        
        # Si no funcionó, deshacer la asignación (backtrack)
        regiones_asignadas.pop()
    
    # Si ningún candidato funcionó, retornar None
    return None


def _seleccionar_proxima_pista_mrv(pistas, candidatos_por_pista, pistas_resueltas):
    """
    Heurística MRV (Minimum Remaining Values):
    Selecciona la siguiente pista a resolver basándose en cuál tiene menos candidatos válidos.
    Esto reduce el factor de ramificación del árbol de búsqueda.
    
    Args:
        pistas: lista de todas las pistas
        candidatos_por_pista: diccionario con candidatos por índice
        pistas_resueltas: conjunto de índices de pistas ya resueltas
    
    Returns:
        Índice de la próxima pista a resolver, o -1 si todas están resueltas
    """
    min_candidatos = float('inf')
    proxima_pista = -1
    
    for i in range(len(pistas)):
        if i not in pistas_resueltas:
            num_candidatos = len(candidatos_por_pista[i])
            if num_candidatos < min_candidatos:
                min_candidatos = num_candidatos
                proxima_pista = i
    
    return proxima_pista


def resolver(tablero):
    """
    Resuelve un rompecabezas Shikaku usando backtracking con heurísticas.
    
    Estrategia:
    1. Extrae todas las pistas del tablero
    2. Genera todos los candidatos posibles para cada pista
    3. Usa backtracking con poda para encontrar la combinación válida
    4. Valida que no haya solapamientos y que se cubra todo el tablero
    
    Args:
        tablero: matriz 2D donde 0 = celda vacía, n > 0 = pista numérica
    
    Returns:
        Lista de regiones (diccionarios con fila_inicio, fila_fin, columna_inicio, columna_fin, area)
        que resuelven el puzzle, o None si no hay solución.
    """
    
    # Paso 1: Obtener todas las pistas
    pistas = obtener_pistas(tablero)
    
    if not pistas:
        return []
    
    # Paso 2: Generar candidatos para cada pista
    candidatos_por_pista = {}
    for i, pista in enumerate(pistas):
        candidatos = generar_candidatos(pista, tablero)
        candidatos_por_pista[i] = candidatos
        
        # Si alguna pista no tiene candidatos, no hay solución
        if not candidatos:
            return None
    
    # Paso 3: Aplicar backtracking
    regiones_asignadas = []
    solucion = _backtrack_resolver(
        pistas,
        0,
        candidatos_por_pista,
        regiones_asignadas,
        tablero
    )
    
    return solucion
