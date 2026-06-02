#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar el funcionamiento del solucionador sintético.
"""

from tablero import cargar_tablero_desde_json, validar_todas_las_regiones, tablero_completamente_cubierto
from solver import resolver, obtener_pistas


def probar_solucionador():
    """Prueba el solucionador con el tablero de prueba."""
    
    ruta = "../data/tablero.json"
    tablero = cargar_tablero_desde_json(ruta)
    
    if not tablero:
        print("❌ No se pudo cargar el tablero.")
        return
    
    print("=" * 70)
    print("PRUEBA DEL SOLUCIONADOR SINTÉTICO - SHIKAKU")
    print("=" * 70)
    
    filas = len(tablero)
    columnas = len(tablero[0])
    print(f"\n📊 Tablero cargado: {filas} x {columnas}")
    
    print("\n📍 Pistas encontradas:")
    pistas = obtener_pistas(tablero)
    for p in pistas:
        print(f"   - Valor {p['valor']} en ({p['fila']}, {p['columna']})")
    
    print(f"\n🔍 Resolviendo...")
    solucion = resolver(tablero)
    
    if solucion is None:
        print("❌ No se encontró solución.")
        return
    
    print(f"✅ ¡Solución encontrada!")
    print(f"\n📋 Regiones de la solución ({len(solucion)} regiones):")
    
    for i, region in enumerate(solucion, 1):
        area = (region["fila_fin"] - region["fila_inicio"] + 1) * \
               (region["columna_fin"] - region["columna_inicio"] + 1)
        print(f"   {i}. Área: {area} | ({region['fila_inicio']},{region['columna_inicio']}) "
              f"→ ({region['fila_fin']},{region['columna_fin']})")
    
    # Validaciones finales
    print(f"\n✓ Validando solución...")
    sin_solapamiento = validar_todas_las_regiones(solucion)
    cubierto = tablero_completamente_cubierto(solucion, filas, columnas)
    
    if sin_solapamiento and cubierto:
        print("✅ ¡La solución es CORRECTA!")
        print("   - Sin solapamientos ✓")
        print("   - Tablero completamente cubierto ✓")
    else:
        print("❌ La solución tiene problemas:")
        if not sin_solapamiento:
            print("   - ERROR: Hay regiones solapadas")
        if not cubierto:
            print("   - ERROR: El tablero no está completamente cubierto")
    
    print("\n" + "=" * 70)


if __name__ == "__main__":
    probar_solucionador()
