# Shikaku Solver 🎮

Proyecto de análisis de algoritmos para resolver el rompecabezas Shikaku mediante un **solucionador sintético** e **interfaz gráfica interactiva**.

## 📋 Descripción

**Shikaku** es un rompecabezas lógico de origen japonés inventado por Yoshinao Anpuku en 1989. El objetivo es dividir una cuadrícula en rectángulos donde:
- Cada rectángulo contiene exactamente **una pista numérica**
- El **área del rectángulo = valor de la pista**
- **No hay solapamientos**
- **Toda la cuadrícula está cubierta**

---

## 🏗️ Arquitectura del Proyecto

```
shikaku-solver/
├── src/
│   ├── main.py           # Script de prueba CLI
│   ├── interface.py      # GUI interactiva (Tkinter)
│   ├── solver.py         # ✨ Solucionador sintético (IMPLEMENTADO)
│   ├── tablero.py        # Lógica y validaciones del tablero
│   └── test_solver.py    # Tests unitarios del solver
├── data/
│   └── tablero.json      # Tablero de prueba
├── docs/
│   └── analisis_algoritmico.md  # Análisis técnico detallado
└── README.md             # Este archivo
```

---

## 🚀 Instalación y Ejecución

### Requisitos
- Python 3.7+
- `tkinter` (generalmente viene con Python)

### Instalación
```bash
cd c:\Users\Samuel\vsc\shikaku-solver
```

### 1️⃣ Ejecutar la Interfaz Gráfica
```bash
cd src
python interface.py
```

**Funcionalidades en la GUI**:
- 🖱️ **Hacer clic en dos celdas** para crear un rectángulo
- ✅ **Validar** tu solución manualmente
- 🤖 **Resolver automáticamente** con el solucionador sintético
- 📁 **Cargar nuevo tablero** desde un archivo JSON
- 🔄 **Reiniciar** el tablero actual

### 2️⃣ Probar el Solucionador (Modo CLI)
```bash
cd src
python test_solver.py
```

**Salida esperada**:
```
======================================================================
PRUEBA DEL SOLUCIONADOR SINTÉTICO - SHIKAKU
======================================================================

📊 Tablero cargado: 4 x 4
📍 Pistas encontradas: 4 pistas
🔍 Resolviendo...
✅ ¡Solución encontrada!
✓ Validando solución...
✅ ¡La solución es CORRECTA!
   - Sin solapamientos ✓
   - Tablero completamente cubierto ✓
```

### 3️⃣ Ejecutar el Script Principal
```bash
cd src
python main.py
```

---

## 🧠 Solucionador Sintético

### Algoritmo: Backtracking con Poda Inteligente

El solucionador implementa un **algoritmo de satisfacción de restricciones** usando:

1. **Generación de Candidatos**
   - Para cada pista, genera todos los rectángulos posibles
   - Filtra aquellos que contengan otras pistas

2. **Búsqueda Recursiva (Backtracking)**
   - Intenta asignar cada candidato a su pista
   - Detecta solapamientos tempranamente (poda)
   - Si encuentra solución, la retorna
   - Si falla, retrocede y prueba otra rama

3. **Validación Final**
   - Verifica cobertura completa del tablero
   - Confirma ausencia de solapamientos

### Complejidad

| Aspecto | Valor |
|---------|-------|
| **Mejor caso** | O(M×N + ∑D(vᵢ)) |
| **Peor caso** | O(∏\|candidatos[i]\|) |
| **Caso típico** | < 1 segundo |
| **Espacio** | O(∑\|candidatos[i]\|) |

### Funciones Públicas

```python
from solver import resolver, obtener_pistas, generar_candidatos

# Resolver un tablero completamente
solucion = resolver(tablero)

# Obtener todas las pistas del tablero
pistas = obtener_pistas(tablero)

# Generar candidatos para una pista específica
candidatos = generar_candidatos(pista, tablero)
```

---

## 📊 Formato de Entrada (JSON)

El tablero se especifica en `data/tablero.json`:

```json
{
  "tablero": [
    [0, 0, 4, 0],
    [4, 0, 0, 0],
    [0, 0, 0, 6],
    [2, 0, 0, 0]
  ]
}
```

Donde:
- `0` = celda vacía (sin pista)
- `n > 0` = pista numérica

---

## ✨ Características Implementadas

### Interface (`interface.py`)
- ✅ Visualización interactiva del tablero
- ✅ Input del usuario (click en dos celdas = rectángulo)
- ✅ Validación de soluciones
- ✅ Integración con solucionador sintético
- ✅ Carga de tableros personalizados
- ✅ Reinicio y feedback visual

### Solver (`solver.py`) - **NUEVO**
- ✅ Algoritmo de backtracking robusto
- ✅ Poda temprana de ramas inviables
- ✅ Detección de solapamientos eficiente
- ✅ Validación de soluciones completas
- ✅ Manejo de casos sin solución

### Tablero (`tablero.py`)
- ✅ Gestión de regiones rectangulares
- ✅ Validaciones de área y cobertura
- ✅ Detección de solapamientos
- ✅ Carga de tableros desde JSON

---

## 📖 Documentación Técnica

Para un análisis detallado del algoritmo, complejidad y optimizaciones:

👉 Ver [docs/analisis_algoritmico.md](docs/analisis_algoritmico.md)

Incluye:
- Descripción completa del algoritmo
- Análisis de complejidad temporal y espacial
- Comparativa con otras estrategias
- Optimizaciones posibles
- Ejemplos de ejecución paso a paso

---

## 🧪 Testing

Se incluye un script de prueba para verificar la correctitud del solucionador:

```bash
python test_solver.py
```

**Pruebas realizadas**:
- ✅ Carga correcta del tablero
- ✅ Extracción de pistas
- ✅ Generación de candidatos
- ✅ Resolución completa del puzzle
- ✅ Validación de solución (sin solapamientos, cobertura completa)

---

## 🎓 Proyecto Académico

- **Universidad**: Pontificia Universidad Javeriana
- **Departamento**: Ingeniería de Sistemas
- **Curso**: Análisis de Algoritmos
- **Proyecto**: 2026-10

---

## 📝 Notas de Desarrollo

### Arquitectura Clean
El proyecto sigue principios de software engineering:
- **Separación de responsabilidades**: GUI, lógica de solving, validaciones
- **Modularidad**: Funciones reutilizables y probables
- **Mantenibilidad**: Código documentado y comentado
- **Escalabilidad**: Fácil agregar nuevas características

### Posibles Mejoras Futuras
1. 🧵 Threading para GUI responsivo con puzzles grandes
2. 🎨 Temas visuales personalizables
3. 💾 Historial de movimientos (undo/redo)
4. 🔍 Mostrar estadísticas del solucionador (tiempo, iteraciones)
5. 🎲 Generador de puzzles aleatorios
6. 📊 Editor interactivo de pistas

---

## 👨‍💻 Autores

Implementación del solucionador sintético: Junio 2026

---

## 📄 Licencia

Proyecto académico - Universidad Javeriana

---

**¿Preguntas?** Ver el análisis técnico en `docs/analisis_algoritmico.md` para más detalles.

