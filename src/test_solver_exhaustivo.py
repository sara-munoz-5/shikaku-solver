#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de pruebas exhaustivas para el solucionador Shikaku.
Prueba múltiples casos y valida la robustez del algoritmo.
"""

from tablero import (
    cargar_tablero_desde_json, 
    validar_todas_las_regiones, 
    tablero_completamente_cubierto,
    crear_region
)
from solver import resolver, obtener_pistas


def validar_solucion(solucion, tablero, nombre_caso):
    """
    Valida una solución completamente.
    
    Returns:
        (es_valida, mensajes)
    """
    if solucion is None:
        return False, ["No se encontró solución"]
    
    mensajes = []
    es_valida = True
    filas = len(tablero)
    columnas = len(tablero[0])
    
    # Validar sin solapamientos
    if not validar_todas_las_regiones(solucion):
        mensajes.append("❌ ERROR: Hay regiones solapadas")
        es_valida = False
    else:
        mensajes.append("✅ Sin solapamientos")
    
    # Validar cobertura completa
    if not tablero_completamente_cubierto(solucion, filas, columnas):
        mensajes.append("❌ ERROR: El tablero no está completamente cubierto")
        es_valida = False
    else:
        mensajes.append("✅ Tablero completamente cubierto")
    
    # Validar número de regiones
    pistas = obtener_pistas(tablero)
    if len(solucion) != len(pistas):
        mensajes.append(f"❌ ERROR: {len(solucion)} regiones, pero {len(pistas)} pistas")
        es_valida = False
    else:
        mensajes.append(f"✅ Número de regiones correcto ({len(solucion)})")
    
    return es_valida, mensajes


def caso_prueba_1():
    """Caso 1: Tablero simple 4x4 (dado en el enunciado)"""
    print("\n" + "="*70)
    print("CASO 1: Tablero Simple 4x4")
    print("="*70)
    
    ruta = "../data/tablero.json"
    tablero = cargar_tablero_desde_json(ruta)
    
    if not tablero:
        print("❌ Error cargando tablero")
        return False
    
    print("📊 Tablero:")
    for fila in tablero:
        print("   ", fila)
    
    solucion = resolver(tablero)
    es_valida, mensajes = validar_solucion(solucion, tablero, "Caso 1")
    
    print("\n📋 Resultado:")
    for msg in mensajes:
        print("   " + msg)
    
    if solucion:
        print("\n📐 Regiones encontradas:")
        for i, r in enumerate(solucion, 1):
            area = (r["fila_fin"] - r["fila_inicio"] + 1) * \
                   (r["columna_fin"] - r["columna_inicio"] + 1)
            print(f"   {i}. Área {area} en ({r['fila_inicio']},{r['columna_inicio']}) → "
                  f"({r['fila_fin']},{r['columna_fin']})")
    
    return es_valida


def caso_prueba_2():
    """Caso 2: Variación del tablero 4x4"""
    print("\n" + "="*70)
    print("CASO 2: Variación del Tablero 4x4")
    print("="*70)
    
    # Tablero similar al caso 1 pero con números diferentes
    tablero = [
        [0, 0, 6, 0],
        [2, 0, 0, 0],
        [0, 0, 0, 4],
        [0, 0, 4, 0]
    ]
    
    print("📊 Tablero:")
    for fila in tablero:
        print("   ", fila)
    
    solucion = resolver(tablero)
    es_valida, mensajes = validar_solucion(solucion, tablero, "Caso 2")
    
    print("\n📋 Resultado:")
    for msg in mensajes:
        print("   " + msg)
    
    if solucion:
        print("\n📐 Regiones encontradas:")
        for i, r in enumerate(solucion, 1):
            area = (r["fila_fin"] - r["fila_inicio"] + 1) * \
                   (r["columna_fin"] - r["columna_inicio"] + 1)
            print(f"   {i}. Área {area} en ({r['fila_inicio']},{r['columna_inicio']}) → "
                  f"({r['fila_fin']},{r['columna_fin']})")
    
    return es_valida


def caso_prueba_3():
    """Caso 3: Tablero 2x2 (mínimo)"""
    print("\n" + "="*70)
    print("CASO 3: Tablero Mínimo 2x2")
    print("="*70)
    
    tablero = [
        [2, 2],
        [0, 0]
    ]
    
    print("📊 Tablero:")
    for fila in tablero:
        print("   ", fila)
    
    solucion = resolver(tablero)
    es_valida, mensajes = validar_solucion(solucion, tablero, "Caso 3")
    
    print("\n📋 Resultado:")
    for msg in mensajes:
        print("   " + msg)
    
    if solucion:
        print("\n📐 Regiones encontradas:")
        for i, r in enumerate(solucion, 1):
            area = (r["fila_fin"] - r["fila_inicio"] + 1) * \
                   (r["columna_fin"] - r["columna_inicio"] + 1)
            print(f"   {i}. Área {area} en ({r['fila_inicio']},{r['columna_inicio']}) → "
                  f"({r['fila_fin']},{r['columna_fin']})")
    
    return es_valida


def caso_prueba_4():
    """Caso 4: Tablero simétrico 4x4"""
    print("\n" + "="*70)
    print("CASO 4: Tablero Simétrico 4x4")
    print("="*70)
    
    # Tablero con distribución simétrica (4 cuadrantes)
    tablero = [
        [4, 0, 0, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [4, 0, 0, 4]
    ]
    
    print("📊 Tablero:")
    for fila in tablero:
        print("   ", fila)
    
    print("📝 Nota: Distribución simétrica en 4 cuadrantes")
    
    solucion = resolver(tablero)
    es_valida, mensajes = validar_solucion(solucion, tablero, "Caso 4")
    
    print("\n📋 Resultado:")
    for msg in mensajes:
        print("   " + msg)
    
    if solucion:
        print("\n📐 Regiones encontradas:")
        for i, r in enumerate(solucion, 1):
            area = (r["fila_fin"] - r["fila_inicio"] + 1) * \
                   (r["columna_fin"] - r["columna_inicio"] + 1)
            print(f"   {i}. Área {area} en ({r['fila_inicio']},{r['columna_inicio']}) → "
                  f"({r['fila_fin']},{r['columna_fin']})")
    
    return es_valida


def main():
    """Ejecuta todas las pruebas."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "PRUEBAS EXHAUSTIVAS DEL SOLUCIONADOR" + " "*17 + "║")
    print("╚" + "="*68 + "╝")
    
    resultados = []
    
    resultados.append(("Caso 1: 4x4 Simple", caso_prueba_1()))
    resultados.append(("Caso 2: 3x3 Personalizado", caso_prueba_2()))
    resultados.append(("Caso 3: 2x2 Mínimo", caso_prueba_3()))
    resultados.append(("Caso 4: Números Primos", caso_prueba_4()))
    
    # Resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE PRUEBAS")
    print("="*70)
    
    total = len(resultados)
    exitosas = sum(1 for _, result in resultados if result)
    
    for nombre, resultado in resultados:
        estado = "✅ PASS" if resultado else "❌ FAIL"
        print(f"{estado}  {nombre}")
    
    print("\n" + "-"*70)
    print(f"Total: {exitosas}/{total} pruebas exitosas")
    
    if exitosas == total:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
    else:
        print(f"⚠️  {total - exitosas} prueba(s) fallaron")
    
    print("="*70 + "\n")
    
    return exitosas == total


if __name__ == "__main__":
    import sys
    exito = main()
    sys.exit(0 if exito else 1)
