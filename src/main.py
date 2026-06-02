""".
Módulo principal de la aplicación Shikaku Solver.

Este módulo es el punto de entrada de la aplicación. Inicializa la ventana
principales de Tkinter y carga la interfaz gráfica del solucionador de Shikaku.
"""

import tkinter as tk
from views.interfaz import ShikakuInterfaz

def main():
    """Función principal que inicia la aplicación.
    
    Crea la ventana raíz de Tkinter, instancia la interfaz gráfica
    y comienza el ciclo principal de eventos.
    """
    # Crear la ventana raíz de Tkinter
    root = tk.Tk()

    # Instanciar la interfaz gráfica del solucionador
    app = ShikakuInterfaz(root)

    # Iniciar el ciclo principal de eventos
    root.mainloop()

if __name__ == "__main__":
    main()