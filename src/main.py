from solver import obtener_pistas, generar_candidatos
from tablero import cargar_tablero_desde_json, validar_area_coincide, tablero_completamente_cubierto

ruta = "../data/tablero.json"
tablero = cargar_tablero_desde_json(ruta)

if tablero:
    filas = len(tablero)
    columnas = len(tablero[0])

    pistas = obtener_pistas(tablero)

    print("Pistas encontradas:")
    for pista in pistas:
        print(pista)

    print("\nCandidatos por pista:")
    regiones_ejemplo = []

    for pista in pistas:
        candidatos = generar_candidatos(pista, tablero)

        print(f"\nPista {pista['valor']} en ({pista['fila']}, {pista['columna']}):")
        for candidato in candidatos:
            print(candidato)
        
        if candidatos:
            regiones_ejemplo.append(candidatos[0])

    print("\n=========================================")
    print("VALIDACION DE REGLAS INTERNAS")
    print("=========================================")

    todas_validas = all(validar_area_coincide(r) for r in regiones_ejemplo)
    print(f"¿Todas las regiones tienen el tamaño correcto?: {todas_validas}")

    cubierto = tablero_completamente_cubierto(regiones_ejemplo, filas, columnas)
    print(f"¿El tablero está completamente cubierto sin vacíos?: {cubierto}")
else:
    print("No se pudo iniciar el programa porque el tablero no cargó correctamente.")