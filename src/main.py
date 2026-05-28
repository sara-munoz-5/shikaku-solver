from solver import obtener_pistas, generar_candidatos

tablero = [
    [0, 0, 4, 0],
    [0, 0, 0, 0],
    [2, 0, 0, 0],
    [0, 0, 0, 2]
]

pistas = obtener_pistas(tablero)

print("Pistas encontradas:")
for pista in pistas:
    print(pista)

print("\nCandidatos por pista:")
for pista in pistas:
    candidatos = generar_candidatos(pista, tablero)

    print(f"\nPista {pista['valor']} en ({pista['fila']}, {pista['columna']}):")
    for candidato in candidatos:
        print(candidato)