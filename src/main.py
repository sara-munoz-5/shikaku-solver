from solver import obtener_pistas

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