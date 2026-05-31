import tkinter as tk 
from tkinter import messagebox, filedialog
import os 
from tablero import cargar_tablero_desde_json, validar_area_coincide, tablero_completamente_cubierto

class ShikakuInterfaz: 
    def __init__(self, root):
        self.root = root
        self.root.title("Shikaku Solver")
        self.root.geometry("600x700")
        self.root.configure(bg="#F3F4F6")

        self.tablero_datos = None
        self.filas = 0 
        self.columnas = 0 
        self.celdas_botones = {}
        self.regiones_usuario = [] #para guardar las regiones del usuario 

        #variables para arrastrar el mouse
        self.fila_inicio = None
        self.columna_inicio = None

        #paleta para los rectangulos 
        self.colores = ["#A7F3D0", "#FED7AA", "#FBCFE8", "#C7D2FE", "#FDE68A", "#BFDBFE"]
        self.color_actual_idx = 0

        #layout
        self.panel_superior = tk.Frame(root , bg="#F3F4F6", pady=10)
        self.panel_superior.pack(side=tk.TOP, fill=tk.X)

        self.panel_tablero = tk.Frame(root, bg="#DEE2E6", bd=2, relief=tk.SOLID)
        self.panel_tablero.pack(expand=True, pady=20)

        self.panel_inferior = tk.Frame(root, bg="#F3F4F6", pady=15)
        self.panel_inferior.pack(side=tk.BOTTOM, fill=tk.X)

        #crear botones
        self.btn_cargar = tk.Button(self.panel_superior, text="Cargar Juego", font=("Arial", 11, "bold"), bg="#3B82F6", fg="white", padx=10, command=self.cargar_nuevo_juego)
        self.btn_cargar.pack(side=tk.LEFT, padx=10)

        self.btn_reiniciar = tk.Button(self.panel_superior, text="Reiniciar", font=("Arial", 11), bg="#9CA3AF", fg="white", padx=10, command=self.reiniciar_tablero)
        self.btn_reiniciar.pack(side=tk.LEFT, padx=10)

        self.btn_validar = tk.Button(self.panel_inferior, text="Validar", font=("Arial", 12, "bold"), bg="#10B981", fg="white", width=12, pady=5, command=self.validar_jugada)
        self.btn_validar.pack(side=tk.LEFT, expand=True)

        self.btn_resolver = tk.Button(self.panel_inferior, text="Resolver", font=("Arial", 12, "bold"), bg="#8B5CF6", fg="white", width=12, pady=5, command=self.resolver_automatico)
        self.btn_resolver.pack(side=tk.RIGHT, expand=True)

        #Cargar por default el tablero
        self.inicializar_con_ruta_defecto()

    def inicializar_con_ruta_defecto(self):
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_defecto = os.path.normpath(os.path.join(dir_actual, "../data/tablero.json"))
        if os.path.exists(ruta_defecto):
            self.construir_tablero_visual(ruta_defecto)
    
    def construir_tablero_visual(self, ruta_json):

        #limpiar tablero
        for widget in self.panel_tablero.winfo_children():
            widget.destroy()
        self.celdas_botones.clear()
        self.regiones_usuario.clear()

        #cargar matriz
        self.tablero_datos = cargar_tablero_desde_json(ruta_json)
        if not self.tablero_datos:
            messagebox.showerror("Error", "No se pudo cargar el archivo JSON.")
            return
        
        self.filas = len(self.tablero_datos)
        self.columnas = len(self.tablero_datos[0])

        #crear cuadricula
        for r in range (self.filas):
            for c in range(self.columnas):
                valor = self.tablero_datos[r][c]
                texto = str(valor) if valor > 0 else " "

                #crear celda visual
                celda = tk.Label(
                    self.panel_tablero, text=texto, font=("Arial", 16, "bold"),
                    width=4, height=2, bg="white", relief=tk.RAISED, bd=1, anchor="center"
                )
                celda.grid(row=r, column=c, padx=1, pady=1)

                self.celdas_botones[(r, c)] = celda

                #eventos del mouse
                celda.bind("<Button-1>", lambda event, fila=r, col=c: self.gestionar_clic(fila, col))
    
    def gestionar_clic(self, fila, col):
        if self.fila_inicio is None or self.columna_inicio is None:
            self.fila_inicio = fila
            self.columna_inicio = col
            self.celdas_botones[(fila, col)].config(bg="#E0E7FF")
            return

        fila_fin = fila 
        col_fin = col

        r_min, r_max = min(self.fila_inicio, fila_fin), max(self.fila_inicio, fila_fin)
        c_min, c_max = min(self.columna_inicio, col_fin), max(self.columna_inicio, col_fin)

        color = self.colores[self.color_actual_idx]
        self.color_actual_idx = (self.color_actual_idx + 1) % len(self.colores)

        # Pintar todas las celdas que entran en el rango matemático del rectángulo
        for r in range(r_min, r_max + 1):
            for c in range(c_min, c_max + 1):
                self.celdas_botones[(r, c)].config(bg=color)

        # Buscar si hay una pista numérica dentro del rectángulo dibujado
        pista_valor = 0
        for r in range(r_min, r_max + 1):
            for c in range(c_min, c_max + 1):
                if self.tablero_datos[r][c] > 0:
                    pista_valor = self.tablero_datos[r][c]

        # Guardar la región para enviársela a tus reglas de tablero.py
        nueva_region = {
            "fila_inicio": r_min,
            "fila_fin": r_max,
            "columna_inicio": c_min,
            "columna_fin": c_max,
            "area": pista_valor
        }
        self.regiones_usuario.append(nueva_region)

        # Resetear las variables para que el usuario pueda dibujar el siguiente rectángulo
        self.fila_inicio = None
        self.columna_inicio = None

    def reiniciar_tablero(self):
        self.regiones_usuario.clear()
        for (r, c) , celda in self.celdas_botones.items():
            celda.config(bg="white")
        messagebox.showinfo("Reiniciar", "El tablero ha sido limpiado")

    def cargar_nuevo_juego(self):
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Shikaku JSON",
            filetypes=[("Archivos JSON", "*.json")]
        )
        if ruta_archivo:
            self.construir_tablero_visual(ruta_archivo)
    
    def validar_jugada(self):
        if not self.regiones_usuario:
            messagebox.showwarning("Validación", "¡No has dibujado ninguna región todavía!")
            return

        todas_validas = all(validar_area_coincide(r) for r in self.regiones_usuario)

        cubierto = tablero_completamente_cubierto(self.regiones_usuario, self.filas, self.columnas)

        if todas_validas and cubierto:
            messagebox.showinfo("¡FELICITACIONES!", "¡El rompecabezas está perfectamente resuelto!")
        elif not todas_validas:
            messagebox.showerror("ERROR DE VALIDACIÓN", "Algunas regiones no coinciden en tamaño matemático con el número de su pista interna.")
        else: 
            messagebox.warning("JUEGO INCOMPLETO", "Las regiones son válidas pero aún quedan espacios vacíos o celdas sin cubrir en la cuadrícula.")

    def resolver_automatico(self):
        messagebox.showinfo("Solver Inteligente", "¡Aquí se conectará tu algoritmo de Backtracking de Análisis de Algoritmos para solucionar el tablero por pasos en la pantalla!")