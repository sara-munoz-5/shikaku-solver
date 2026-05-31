import tkinter as tk
from views.interfaz import ShikakuInterfaz

def main():
    root = tk.Tk()

    app = ShikakuInterfaz(root)

    root.mainloop()

if __name__ == "__main__":
    main()