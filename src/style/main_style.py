import tkinter as tk
from tkinter import ttk

DEFAULT_FONT = ("Segoe UI", 12)
DEFAULT_FONT_BOLD = ("Segoe UI", 12, "bold")

def setup_style(root):
    style = ttk.Style(root)
    style.theme_use("clam")

    # Fonte padrão para todos os widgets ttk
    style.configure(".", font=DEFAULT_FONT)

    # Botões
    style.configure("TButton", font=DEFAULT_FONT_BOLD)

    # Labels
    style.configure("TLabel", font=DEFAULT_FONT)

    # Entradas
    style.configure("TEntry", font=DEFAULT_FONT)

    # Treeview (tabela)
    style.configure("Treeview", font=DEFAULT_FONT)
    style.configure("Treeview.Heading", font=DEFAULT_FONT_BOLD)