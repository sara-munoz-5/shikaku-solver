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