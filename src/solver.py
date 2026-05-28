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