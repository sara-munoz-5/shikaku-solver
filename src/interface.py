import tkinter as tk
from tkinter import filedialog, messagebox
import sys
import os

from solver import obtener_pistas, generar_candidatos
from tablero import (
    crear_region,
    validar_area_coincide,
    cargar_tablero_desde_json,
    validar_todas_las_regiones,
    tablero_completamente_cubierto,
    hay_solapamiento,
)
#  CONSTANTES VISUALES
CELDA = 80
PALETA = [
    "#E1F5EE", "#EEEDFE", "#FAEEDA", "#E6F1FB",
    "#FBEAF0", "#EAF3DE", "#FAECE7", "#E8E8E8",
]
PALETA_BORDE = [
    "#0F6E56", "#534AB7", "#854F0B", "#185FA5",
    "#993556", "#3B6D11", "#993C1D", "#888780",
]


#  CLASE PRINCIPAL
class ShikakuApp:
    def __init__(self, root, ruta_tablero):
        self.root = root
        self.root.title("Shikaku")
        self.root.resizable(False, False)
        self.root.configure(bg="#F5F5F2")

        self.tablero   = None
        self.regiones  = []
        self.celda_inicio = None   # primera celda seleccionada por el usuario

        # ── Canvas ────────────────────────────
        self.canvas = tk.Canvas(root, bg="white", highlightthickness=0)
        self.canvas.pack(padx=20, pady=(20, 8))

        # Eventos del mouse
        self.canvas.bind("<Button-1>", self.on_click)

        # ── Botones ───────────────────────────
        frame_btn = tk.Frame(root, bg="#F5F5F2")
        frame_btn.pack(padx=20, pady=(0, 8))

        estilo = dict(font=("Arial", 11), relief="flat", bd=0,
                      padx=14, pady=7, cursor="hand2")

        tk.Button(frame_btn, text="Resolver",
                  bg="#1D9E75", fg="white", activebackground="#0F6E56",
                  command=self.accion_resolver, **estilo
                  ).grid(row=0, column=0, padx=4)

        tk.Button(frame_btn, text="Validar",
                  bg="#E8E8E4", fg="#333", activebackground="#D0D0CC",
                  command=self.accion_validar, **estilo
                  ).grid(row=0, column=1, padx=4)

        tk.Button(frame_btn, text="Nuevo tablero",
                  bg="#E8E8E4", fg="#333", activebackground="#D0D0CC",
                  command=self.accion_nuevo_tablero, **estilo
                  ).grid(row=0, column=2, padx=4)

        tk.Button(frame_btn, text="Reiniciar",
                  bg="#E8E8E4", fg="#333", activebackground="#D0D0CC",
                  command=self.accion_reiniciar, **estilo
                  ).grid(row=0, column=3, padx=4)

        # ── Mensaje de estado ─────────────────
        self.label_msg = tk.Label(root, text="", font=("Arial", 11),
                                  bg="#F5F5F2", fg="#555", anchor="w")
        self.label_msg.pack(fill="x", padx=20, pady=(0, 16))

        self._cargar_tablero(ruta_tablero)

    # ── Carga ─────────────────────────────────
    def _cargar_tablero(self, ruta):
        tablero = cargar_tablero_desde_json(ruta)
        if not tablero:
            messagebox.showerror("Error", f"No se pudo cargar:\n{ruta}")
            return
        self.tablero      = tablero
        self.regiones     = []
        self.celda_inicio = None
        self.canvas.config(
            width=len(tablero[0]) * CELDA,
            height=len(tablero)   * CELDA,
        )
        self.dibujar()
        self._set_mensaje("Haz clic en dos celdas para formar un rectángulo.", "#555")

    # ── Interacción del mouse ─────────────────
    def on_click(self, event):
        """
        Primer clic  → marca la celda de inicio (resaltada en azul).
        Segundo clic → intenta crear un rectángulo entre inicio y fin.
        """
        c = event.x // CELDA
        f = event.y // CELDA

        # Verificar que el clic está dentro del tablero
        if f >= len(self.tablero) or c >= len(self.tablero[0]):
            return

        if self.celda_inicio is None:
            # Primer clic: guardar celda de inicio
            self.celda_inicio = (f, c)
            self._set_mensaje(
                f"Inicio: ({f},{c}) — ahora clic en la celda final.", "#185FA5"
            )
            self.dibujar()
            self._resaltar_celda(f, c)
        else:
            # Segundo clic: intentar crear la región
            f0, c0 = self.celda_inicio
            f1, c1 = f, c

            # Normalizar para que inicio < fin siempre
            fi, ff = min(f0, f1), max(f0, f1)
            ci, cf = min(c0, c1), max(c0, c1)

            # Buscar qué pista queda dentro del rectángulo
            pista_valor = self._obtener_pista_en_region(fi, ff, ci, cf)

            if pista_valor is None:
                self._set_mensaje("El rectángulo no contiene ninguna pista.", "#CC3333")
            else:
                # Usar crear_region de tablero.py — area = valor de la pista
                nueva_region = crear_region(fi, ff, ci, cf, pista_valor)

                if not validar_area_coincide(nueva_region):
                    area_real = (ff - fi + 1) * (cf - ci + 1)
                    self._set_mensaje(
                        f"El área del rectángulo ({area_real}) no coincide con la pista ({pista_valor}).",
                        "#CC3333"
                    )
                elif any(hay_solapamiento(nueva_region, r) for r in self.regiones):
                    self._set_mensaje("Esa región solapa con otra. Intenta de nuevo.", "#CC3333")
                else:
                    self.regiones.append(nueva_region)
                    self._set_mensaje(
                        f"Región agregada — área {pista_valor}.", "#1D9E75"
                    )

            self.celda_inicio = None
            self.dibujar()

    def _obtener_pista_en_region(self, fi, ff, ci, cf):
        """
        Busca si hay exactamente una pista dentro del rectángulo.
        Devuelve su valor, o None si no hay ninguna.
        """
        pistas_encontradas = []
        for f in range(fi, ff + 1):
            for c in range(ci, cf + 1):
                if self.tablero[f][c] != 0:
                    pistas_encontradas.append(self.tablero[f][c])
        if len(pistas_encontradas) == 1:
            return pistas_encontradas[0]
        return None

    def _resaltar_celda(self, f, c):
        """Dibuja un borde azul sobre la celda de inicio seleccionada."""
        x0 = c * CELDA + 2
        y0 = f * CELDA + 2
        x1 = (c + 1) * CELDA - 2
        y1 = (f + 1) * CELDA - 2
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="#185FA5", width=3)

    # ── Dibujo ────────────────────────────────
    def dibujar(self):
        self.canvas.delete("all")
        self._dibujar_regiones()
        self._dibujar_grid()
        self._dibujar_pistas()

    def _dibujar_regiones(self):
        for idx, region in enumerate(self.regiones):
            color       = PALETA[idx % len(PALETA)]
            color_borde = PALETA_BORDE[idx % len(PALETA_BORDE)]
            x0 = region["columna_inicio"] * CELDA
            y0 = region["fila_inicio"]    * CELDA
            x1 = (region["columna_fin"]   + 1) * CELDA
            y1 = (region["fila_fin"]       + 1) * CELDA
            self.canvas.create_rectangle(x0, y0, x1, y1,
                                         fill=color, outline=color_borde, width=3)

    def _dibujar_grid(self):
        filas    = len(self.tablero)
        columnas = len(self.tablero[0])
        for f in range(filas + 1):
            self.canvas.create_line(0, f * CELDA, columnas * CELDA, f * CELDA,
                                    fill="#C8C8C4", width=1)
        for c in range(columnas + 1):
            self.canvas.create_line(c * CELDA, 0, c * CELDA, filas * CELDA,
                                    fill="#C8C8C4", width=1)
        self.canvas.create_rectangle(0, 0, columnas * CELDA, filas * CELDA,
                                     outline="#1E1E1E", width=2)

    def _dibujar_pistas(self):
        for f in range(len(self.tablero)):
            for c in range(len(self.tablero[0])):
                valor = self.tablero[f][c]
                if valor != 0:
                    self.canvas.create_text(
                        c * CELDA + CELDA // 2,
                        f * CELDA + CELDA // 2,
                        text=str(valor),
                        font=("Arial", 22, "bold"),
                        fill="#1A1A1A",
                    )

    # ── Mensaje ───────────────────────────────
    def _set_mensaje(self, texto, color="#555"):
        self.label_msg.config(text=texto, fg=color)

    # ── Acciones ──────────────────────────────
    def accion_resolver(self):
        self._set_mensaje("Resolviendo...", "#555")
        self.root.update()
        solucion = resolver(self.tablero)
        if solucion:
            self.regiones = solucion
            self.celda_inicio = None
            self.dibujar()
            self._set_mensaje("Solución encontrada.", "#1D9E75")
        else:
            self._set_mensaje("No se encontró solución.", "#CC3333")

    def accion_validar(self):
        if not self.regiones:
            self._set_mensaje("No hay regiones para validar.", "#555")
            return
        sin_solapamiento = validar_todas_las_regiones(self.regiones)
        cubierto = tablero_completamente_cubierto(
            self.regiones, len(self.tablero), len(self.tablero[0])
        )
        if sin_solapamiento and cubierto:
            self._set_mensaje("¡Correcto! El tablero está resuelto.", "#1D9E75")
        elif not sin_solapamiento:
            self._set_mensaje("Error: hay regiones solapadas.", "#CC3333")
        else:
            self._set_mensaje("Incompleto: quedan celdas sin cubrir.", "#CC3333")

    def accion_nuevo_tablero(self):
        self.root.focus_force()
        ruta = filedialog.askopenfilename(
            parent=self.root,
            title="Seleccionar tablero",
            filetypes=[("JSON", "*.json"), ("Todos", "*.*")],
        )
        if ruta:
            self._cargar_tablero(ruta)

    def accion_reiniciar(self):
        # Limpia todo sin preguntar nada
        self.regiones     = []
        self.celda_inicio = None
        self.dibujar()
        self._set_mensaje("Tablero reiniciado.", "#555")


#  ENTRADA
if __name__ == "__main__":
    ruta = "../data/tablero.json"
    root = tk.Tk()
    app  = ShikakuApp(root, ruta)
    root.mainloop()