"""
Módulo de interfaz gráfica para el Shikaku Solver.

Proporciona una interfaz interactiva basada en Tkinter donde el usuario puede:
- Cargar puzzles de Shikaku desde archivos JSON
- Dibujar rectángulos por drag-and-drop para resolver el puzzle
- Validar soluciones manualmente
- Usar el solucionador automático basado en backtracking
- Reiniciar el tablero y cargar nuevos juegos
"""

import tkinter as tk 
from tkinter import messagebox, filedialog
import os 
from tablero import cargar_tablero_desde_json, validar_area_coincide, tablero_completamente_cubierto
from solver import resolver_shikaku

class ShikakuInterfaz: 
    def __init__(self, root):
        """Inicializa la interfaz gráfica del Shikaku Solver.
        
        Configura:
        - Ventana principal con título y tamaño
        - Variables de instancia para almacenar el tablero y regiones
        - Paneles de layout (superior, tablero, inferior)
        - Botones de control (Cargar, Reiniciar, Validar, Resolver)
        - Paleta de colores para regiones
        - Carga automática del tablero por defecto
        
        Args:
            root: La ventana principal de Tkinter
        """
        self.root = root
        self.root.title("Shikaku Solver")
        self.root.geometry("600x700")
        self.root.configure(bg="#F3F4F6")

        # Variables para almacenar datos del tablero
        self.tablero_datos = None
        self.filas = 0 
        self.columnas = 0 
        self.celdas_botones = {}
        self.regiones_usuario = []  # Guarda las regiones dibujadas por el usuario

        # Variables para rastrear el arrastre del mouse
        self.fila_inicio = None
        self.columna_inicio = None

        # Paleta de colores para distinguir diferentes regiones
        self.colores = ["#A7F3D0", "#FED7AA", "#FBCFE8", "#C7D2FE", "#FDE68A", "#BFDBFE"]
        self.color_actual_idx = 0

        # Crear los paneles principales del layout
        self.panel_superior = tk.Frame(root, bg="#F3F4F6", pady=10)
        self.panel_superior.pack(side=tk.TOP, fill=tk.X)

        self.panel_tablero = tk.Frame(root, bg="#DEE2E6", bd=2, relief=tk.SOLID)
        self.panel_tablero.pack(expand=True, pady=20)

        self.panel_inferior = tk.Frame(root, bg="#F3F4F6", pady=15)
        self.panel_inferior.pack(side=tk.BOTTOM, fill=tk.X)

        # Crear botones de control
        self.btn_cargar = tk.Button(self.panel_superior, text="Cargar Juego", font=("Arial", 11, "bold"), bg="#3B82F6", fg="white", padx=10, command=self.cargar_nuevo_juego)
        self.btn_cargar.pack(side=tk.LEFT, padx=10)

        self.btn_reiniciar = tk.Button(self.panel_superior, text="Reiniciar", font=("Arial", 11), bg="#9CA3AF", fg="white", padx=10, command=self.reiniciar_tablero)
        self.btn_reiniciar.pack(side=tk.LEFT, padx=10)

        self.btn_validar = tk.Button(self.panel_inferior, text="Validar", font=("Arial", 12, "bold"), bg="#10B981", fg="white", width=12, pady=5, command=self.validar_jugada)
        self.btn_validar.pack(side=tk.LEFT, expand=True)

        self.btn_resolver = tk.Button(self.panel_inferior, text="Resolver", font=("Arial", 12, "bold"), bg="#8B5CF6", fg="white", width=12, pady=5, command=self.resolver_automatico)
        self.btn_resolver.pack(side=tk.RIGHT, expand=True)

        # Cargar el tablero por defecto al iniciar
        self.inicializar_con_ruta_defecto()

    def inicializar_con_ruta_defecto(self):
        """Carga el tablero por defecto desde data/tablero.json.
        
        Si el archivo existe, lo carga automáticamente al iniciar la aplicación.
        Si no existe, la interfaz inicia sin tablero hasta que el usuario cargue uno.
        """
        dir_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_defecto = os.path.normpath(os.path.join(dir_actual, "../data/tablero.json"))
        if os.path.exists(ruta_defecto):
            self.construir_tablero_visual(ruta_defecto)
    
    def construir_tablero_visual(self, ruta_json):
        """Construye la representación visual del tablero a partir de un archivo JSON.
        
        Pasos:
        1. Limpia la interfaz anterior (si existe un tablero)
        2. Carga los datos del JSON
        3. Crea una grilla visual de celdas (Labels de Tkinter)
        4. Vincula eventos de clic a cada celda para permitir interacción
        
        Args:
            ruta_json: Ruta al archivo JSON que contiene el tablero
        """
        # Limpiar widgets anteriores
        for widget in self.panel_tablero.winfo_children():
            widget.destroy()
        self.celdas_botones.clear()
        self.regiones_usuario.clear()

        # Cargar datos del JSON
        self.tablero_datos = cargar_tablero_desde_json(ruta_json)
        if not self.tablero_datos:
            messagebox.showerror("Error", "No se pudo cargar el archivo JSON.")
            return
        
        self.filas = len(self.tablero_datos)
        self.columnas = len(self.tablero_datos[0])

        # Crear grilla visual del tablero
        for r in range(self.filas):
            for c in range(self.columnas):
                valor = self.tablero_datos[r][c]
                # Mostrar el número si es una pista, espacio en blanco si no
                texto = str(valor) if valor > 0 else " "

                # Crear celda visual como Label
                celda = tk.Label(
                    self.panel_tablero, text=texto, font=("Arial", 16, "bold"),
                    width=4, height=2, bg="white", relief=tk.RAISED, bd=1, anchor="center"
                )
                celda.grid(row=r, column=c, padx=1, pady=1)

                self.celdas_botones[(r, c)] = celda

                # Vincular eventos de clic del mouse
                celda.bind("<Button-1>", lambda event, fila=r, col=c: self.gestionar_clic(fila, col))
    
    def gestionar_clic(self, fila, col):
        """Gestiona los clics del mouse para dibujar rectángulos.
        
        Funciona con un sistema de dos clics:
        1. Primer clic: marca la celda inicial (esquina superior izquierda)
        2. Segundo clic: marca la celda final (esquina inferior derecha)
        
        Luego crea un rectángulo pintando todas las celdas entre ambas esquinas
        con un color de la paleta.
        
        Args:
            fila: Índice de fila de la celda donde se hizo clic
            col: Índice de columna de la celda donde se hizo clic
        """
        # Si es el primer clic, guardar la posición inicial
        if self.fila_inicio is None or self.columna_inicio is None:
            self.fila_inicio = fila
            self.columna_inicio = col
            self.celdas_botones[(fila, col)].config(bg="#E0E7FF")  # Destacar celda inicial
            return

        fila_fin = fila 
        col_fin = col

        # Calcular los límites del rectángulo (ignorar el orden de clics)
        r_min, r_max = min(self.fila_inicio, fila_fin), max(self.fila_inicio, fila_fin)
        c_min, c_max = min(self.columna_inicio, col_fin), max(self.columna_inicio, col_fin)

        # Obtener el siguiente color de la paleta
        color = self.colores[self.color_actual_idx]
        self.color_actual_idx = (self.color_actual_idx + 1) % len(self.colores)

        # Pintar todas las celdas dentro del rectángulo
        for r in range(r_min, r_max + 1):
            for c in range(c_min, c_max + 1):
                self.celdas_botones[(r, c)].config(bg=color)

        # Buscar la pista numérica dentro del rectángulo
        pista_valor = 0
        for r in range(r_min, r_max + 1):
            for c in range(c_min, c_max + 1):
                if self.tablero_datos[r][c] > 0:
                    pista_valor = self.tablero_datos[r][c]

        # Crear y guardar la región dibujada
        nueva_region = {
            "fila_inicio": r_min,
            "fila_fin": r_max,
            "columna_inicio": c_min,
            "columna_fin": c_max,
            "area": pista_valor
        }
        self.regiones_usuario.append(nueva_region)

        # Resetear para permitir dibujar el siguiente rectángulo
        self.fila_inicio = None
        self.columna_inicio = None

    def reiniciar_tablero(self):
        """Limpia todas las regiones dibujadas y reinicia el tablero visual.
        
        Borra las regiones del usuario y restaura todas las celdas al color blanco.
        """
        self.regiones_usuario.clear()
        for (r, c), celda in self.celdas_botones.items():
            celda.config(bg="white")
        messagebox.showinfo("Reiniciar", "El tablero ha sido limpiado")

    def cargar_nuevo_juego(self):
        """Abre un diálogo para seleccionar y cargar un nuevo archivo de tablero.
        
        Permite al usuario navegar por el sistema de archivos y seleccionar
        un archivo JSON que contenga un puzzle de Shikaku.
        """
        ruta_archivo = filedialog.askopenfilename(
            title="Seleccionar archivo Shikaku JSON",
            filetypes=[("Archivos JSON", "*.json")]
        )
        if ruta_archivo:
            self.construir_tablero_visual(ruta_archivo)
    
    def validar_jugada(self):
        """Valida la solución del usuario.
        
        Verifica:
        1. Si se han dibujado regiones
        2. Si todas las regiones tienen el área correcta según su pista
        3. Si el tablero está completamente cubierto
        
        Muestra mensajes informativos al usuario sobre el estado de la solución.
        """
        if not self.regiones_usuario:
            messagebox.showwarning("Validación", "¡No has dibujado ninguna región todavía!")
            return

        # Verificar que todas las regiones tengan área correcta
        todas_validas = all(validar_area_coincide(r) for r in self.regiones_usuario)

        # Verificar que el tablero esté completamente cubierto
        cubierto = tablero_completamente_cubierto(self.regiones_usuario, self.filas, self.columnas)

        # Mostrar resultado
        if todas_validas and cubierto:
            messagebox.showinfo("¡FELICITACIONES!", "¡El rompecabezas está perfectamente resuelto!")
        elif not todas_validas:
            messagebox.showerror("ERROR DE VALIDACIÓN", "Algunas regiones no coinciden en tamaño matemático con el número de su pista interna.")
        else: 
            messagebox.showwarning("JUEGO INCOMPLETO", "Las regiones son válidas pero aún quedan espacios vacíos o celdas sin cubrir en la cuadrícula.")

    def resolver_automatico(self):
        """Resuelve el puzzle automáticamente usando el algoritmo backtracking.
        
        Pasos:
        1. Verifica que haya un tablero cargado
        2. Llama al solucionador de Shikaku
        3. Si hay solución, limpia el tablero y dibuja los rectángulos de la solución
        4. Si no hay solución, informa al usuario
        """
        if not self.tablero_datos:
            messagebox.showwarning("Solver", "Primero debes cargar un tablero.")
            return

        # Resolver usando backtracking
        solucion = resolver_shikaku(self.tablero_datos)

        if solucion is None:
            messagebox.showerror("Solver", "Este tablero no tiene una solución matemática válida.")
            return

        # Limpiar el tablero anterior
        self.regiones_usuario.clear()
        for (r, c), celda in self.celdas_botones.items():
            celda.config(bg="white")

        # Dibujar cada rectángulo de la solución con un color diferente
        for rect in solucion:
            color = self.colores[self.color_actual_idx]
            self.color_actual_idx = (self.color_actual_idx + 1) % len(self.colores)

            r_min, r_max = rect["fila_inicio"], rect["fila_fin"]
            c_min, c_max = rect["columna_inicio"], rect["columna_fin"]

            # Pintar las celdas del rectángulo
            for r in range(r_min, r_max + 1):
                for c in range(c_min, c_max + 1):
                    self.celdas_botones[(r, c)].config(bg=color)

            self.regiones_usuario.append(rect)

        messagebox.showinfo("Solver", "¡Tablero resuelto con éxito usando Backtracking!")