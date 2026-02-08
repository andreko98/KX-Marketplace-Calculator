import tkinter as tk

from components.main.main_component import MainComponent
from style.main_style import setup_style

def main():
    root = tk.Tk()
    root.title("KX Calculadora de Preços")

    setup_style(root)
    
    root.state("zoomed")

    root.geometry("400x300")

    app = MainComponent(root)
    app.pack(expand=True, fill="both")

    root.mainloop()

if __name__ == "__main__":
    main()