import tkinter as tk
from tkinter import ttk

from components.products.product_list_component import ProductListComponent

class MainComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        notebook = ttk.Notebook(self)
        notebook.pack(expand=True, fill="both")

        notebook.add(ProductListComponent(notebook), text="Produtos")