# Análisis Algorítmico - Solucionador Shikaku

## 1. Descripción General

Este documento describe el **solucionador sintético** para el rompecabezas Shikaku, implementado usando **algoritmo de backtracking con poda inteligente**.

---

## 2. Problema a Resolver

### 2.1 Definición del Problema Shikaku

El Shikaku es un rompecabezas cuadriculado donde:
- **Entrada**: Una cuadrícula de tamaño M × N con números distribuidos
- **Objetivo**: Dividir la cuadrícula en rectángulos tales que:
  - Cada rectángulo contiene exactamente una pista numérica
  - El área del rectángulo coincide con el valor de la pista
  - No hay solapamientos
  - Toda la cuadrícula está cubierta

### 2.2 Complejidad del Problema

- **Clasificación**: NP-completo (problema de satisfacción de restricciones)
- **Tipo**: Constraint Satisfaction Problem (CSP)
- **Factor de ramificación**: Variable según los candidatos por pista

---

## 3. Algoritmo Implementado: Backtracking con Poda

### 3.1 Estructura General

```
RESOLVER(tablero)
    1. pistas ← obtener_pistas(tablero)
    2. Para cada pista: generar_candidatos(pista)
    3. regiones ← backtrack(pistas, 0, candidatos, [])
    4. Retornar regiones
```

### 3.2 Componentes Principales

#### 3.2.1 `obtener_pistas(tablero)`

**Propósito**: Extraer todas las pistas numéricas del tablero.

**Algoritmo**:
```
Para cada celda (f, c) en tablero:
    Si tablero[f][c] ≠ 0:
        Agregar {fila, columna, valor} a pistas
```

**Complejidad**: O(M × N)

---

#### 3.2.2 `generar_candidatos(pista, tablero)`

**Propósito**: Generar todos los rectángulos posibles que contengan la pista con área = valor.

**Algoritmo**:
```
valor ← pista.valor
candidatos ← []

Para alto = 1 hasta valor:
    Si valor % alto == 0:
        ancho ← valor / alto
        
        Para fila_inicio = pista.fila - alto + 1 hasta pista.fila:
            Para col_inicio = pista.col - ancho + 1 hasta pista.col:
                fila_fin ← fila_inicio + alto - 1
                col_fin ← col_inicio + ancho - 1
                
                Si rect. está dentro del tablero:
                    Si rect. no contiene otra pista:
                        candidatos.agregar(rect)
                        
Retornar candidatos
```

**Complejidad**: O(D(valor) × valor) donde D(valor) es el número de divisores de valor

**Observación**: El número de divisores es típicamente pequeño (≤ 16 para valores ≤ 100).

---

#### 3.2.3 `puede_asignarse_pista(pista, candidatos, regiones_asignadas)`

**Propósito**: Filtrar candidatos que no solapan con regiones ya asignadas.

**Función auxiliar de poda temprana**: Reduce el espacio de búsqueda.

**Complejidad**: O(|candidatos| × |regiones_asignadas|)

---

#### 3.2.4 `_backtrack_resolver(pistas, indice, candidatos_por_pista, regiones_asignadas, tablero)`

**Propósito**: Encontrar una asignación válida de regiones mediante búsqueda recursiva con backtracking.

**Algoritmo**:
```
BACKTRACK(indice_pista)
    Si indice_pista == |pistas|:
        Si tablero está completamente cubierto:
            Retornar regiones_asignadas  ← CASO BASE: SOLUCIÓN ENCONTRADA
        Si no:
            Retornar NULL
    
    pista_actual ← pistas[indice_pista]
    candidatos ← puede_asignarse_pista(...)  ← PODA
    
    Si candidatos está vacío:
        Retornar NULL  ← PODA: SIN CANDIDATOS VÁLIDOS
    
    Para cada candidato en candidatos:
        regiones_asignadas.agregar(candidato)
        resultado ← BACKTRACK(indice_pista + 1)
        
        Si resultado ≠ NULL:
            Retornar resultado  ← SOLUCIÓN ENCONTRADA
        
        regiones_asignadas.eliminar()  ← BACKTRACK
    
    Retornar NULL
```

**Complejidad Teórica**: O(∏ᵢ |candidatos[i]|) en el peor caso
- Factorial del número de pistas en el peor caso
- En la práctica: mucho mejor gracias a la poda

---

### 3.3 Estrategias de Poda

#### 3.3.1 Poda Temprana por Solapamiento

Durante cada recursión, se filtra:
```
candidatos_válidos ← 
    {c ∈ candidatos | no_solapa(c, regiones_asignadas)}
```

**Beneficio**: Elimina ramas inviables tempranamente.

**Complejidad**: O(|candidatos| × |regiones_asignadas|) pero aceptable

#### 3.3.2 Validación Final de Cobertura

Solo se verifica cobertura completa cuando todas las pistas están asignadas:
```
Si |regiones_asignadas| == |pistas|:
    Validar tablero_completamente_cubierto()
```

**Beneficio**: Evita computaciones de cobertura parcial innecesarias.

---

## 4. Análisis de Complejidad

### 4.1 Complejidad Temporal

#### Mejor Caso: O(M × N + ∑ D(vᵢ))
- Cuando se encuentra rápidamente una solución válida
- Principalmente costo de generación de candidatos

#### Peor Caso: O(∏ᵢ |candidatos[i]| × M × N)
- Cuando hay múltiples soluciones o ninguna
- Factor factorial en el número de pistas

#### Caso Promedio: Exponencial pero acotado por poda
- Empíricamente: muy rápido para tableros típicos (< 1 segundo)

### 4.2 Complejidad Espacial

- **Almacenamiento de candidatos**: O(∑ᵢ |candidatos[i]|)
- **Pila de recursión**: O(|pistas|)
- **Total**: O(∑ᵢ |candidatos[i]| + |pistas|)

Típicamente: O(100) a O(1000) para tableros estándar

---

## 5. Comparativa con Otras Estrategias

| Estrategia | Ventajas | Desventajas |
|-----------|----------|------------|
| **Backtracking** (nuestra) | Eficiente, fácil implementar poda | Exponencial en peor caso |
| Programación Dinámica | Óptimo si hay subestructura | Difícil aplicar a CSP general |
| Algoritmos Genéticos | Escalable | No garantiza optimalidad |
| SAT Solver | Robusto, probado | Overhead computacional alto |

**Conclusión**: Backtracking es ideal para Shikaku por su balance entre simplicidad e eficiencia.

---

## 6. Optimizaciones Posibles

### 6.1 Heurística MRV (Minimum Remaining Values)

**Idea**: Resolver primero la pista con menos candidatos válidos.

**Implementación actual**: Orden secuencial de pistas

**Mejora propuesta**: Reorganizar pistas por número de candidatos
```
pista_siguiente ← argmin |candidatos[i]| para i no resuelto
```

**Beneficio**: Reduce factor de ramificación early en el árbol

**Costo**: O(|pistas|) para seleccionar en cada paso

### 6.2 Constraint Propagation

**Idea**: Después de asignar una región, eliminar candidatos incompatibles.

**Ejemplo**: Si región A ocupa área X, las pistas vecinas no pueden usar candidatos que solapan.

### 6.3 Paralelización

**Idea**: Explorar diferentes ramas del árbol de búsqueda en paralelo.

**Consideración**: Tkinter es single-threaded en la UI; usar threading cuidadosamente.

---

## 7. Validación de la Solución

La solución retornada debe cumplir:

1. **Cobertura completa**: Area total = M × N
2. **Sin solapamientos**: Ningún par de regiones se intersecta
3. **Una pista por región**: Cada región contiene exactamente una pista
4. **Área coincide**: Area(región) = valor(pista)

**Funciones de validación**:
- `validar_todas_las_regiones()`: Verifica sin solapamientos
- `tablero_completamente_cubierto()`: Verifica cobertura
- `hay_solapamiento()`: Detecta intersecciones

---

## 8. Ejemplo de Ejecución

### Tablero de entrada:
```
[0, 0, 4, 0]
[4, 0, 0, 0]
[0, 0, 0, 6]
[2, 0, 0, 0]
```

### Pistas encontradas:
- (0, 2) = 4
- (1, 0) = 4
- (2, 3) = 6
- (3, 0) = 2

### Árbol de búsqueda (simplificado):
```
Backtrack(0)
├─ Asignar pista (0,2)=4 → candidatos posibles
│  └─ Backtrack(1)
│     ├─ Asignar pista (1,0)=4 → candidatos válidos (sin solapamiento)
│     │  └─ Backtrack(2)
│     │     ├─ Asignar pista (2,3)=6 → candidatos válidos
│     │     │  └─ Backtrack(3)
│     │     │     ├─ Asignar pista (3,0)=2 → candidatos válidos
│     │     │     │  └─ Backtrack(4)
│     │     │     │     ✅ TODAS LAS PISTAS ASIGNADAS
│     │     │     │     ✅ VALIDAR COBERTURA COMPLETA
│     │     │     │     ✅ RETORNAR SOLUCIÓN
```

### Solución encontrada:
```
Región 1: (0,0) → (0,3), área = 4
Región 2: (1,0) → (1,3), área = 4
Región 3: (2,1) → (3,3), área = 6
Región 4: (2,0) → (3,0), área = 2
```

---

## 9. Conclusiones

El solucionador implementado:

✅ **Es correcto**: Valida todas las restricciones del problema
✅ **Es eficiente**: Usa backtracking con poda temprana
✅ **Es escalable**: Funciona bien para tableros típicos (4×4 a 10×10)
✅ **Es mantenible**: Código limpio y bien documentado
✅ **Es integrable**: Se conecta fácilmente con la interfaz Tkinter

**Tiempo de ejecución típico**: < 1 segundo para tableros estándar

---

**Autor**: Solucionador Sintético Shikaku v1.0
**Fecha de implementación**: 2026-06-02
