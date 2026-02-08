import tkinter as tk
from tkinter import ttk, messagebox

from style.main_style import DEFAULT_FONT

class EditProductModal(tk.Toplevel):
    def __init__(self, parent, product_data, on_submit):
        super().__init__(parent)
        self.title("Editar Produto")
        self.transient(parent)
        self.grab_set()

        width, height = 500, 450
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        self.entries = {}
        fields = ["SKU", "Tipo", "Descrição", "Un/Caixa", "Custo"]

        self.grid_columnconfigure(0, weight=1)

        for i, field in enumerate(fields):
            label = ttk.Label(self, text=field)
            label.grid(row=i*2, column=0, padx=10, pady=(10, 0), sticky="w")

            entry = ttk.Entry(self, font=DEFAULT_FONT)
            entry.grid(row=i*2+1, column=0, padx=10, pady=(0, 10), sticky="ew")

            if field == "Un/Caixa":
                vcmd = (self.register(self._validate_int), "%P")
                entry.config(validate="key", validatecommand=vcmd)
            elif field == "Custo":
                vcmd = (self.register(self._validate_decimal), "%P")
                entry.config(validate="key", validatecommand=vcmd)

            self.entries[field] = entry

        self._fill_entries(product_data)

        save_btn = ttk.Button(self, text="Salvar", command=self._save)
        save_btn.grid(row=len(fields)*2, column=0, padx=10, pady=20, sticky="e")

        self.on_submit = on_submit

        self.entries["SKU"].focus_set()
        
        self.bind("<Return>", lambda event: self._save())

    def _fill_entries(self, product_data):
        self.entries["SKU"].insert(0, product_data.get("SKU", ""))
        self.entries["Tipo"].insert(0, product_data.get("Type", ""))
        self.entries["Descrição"].insert(0, product_data.get("Description", ""))
        self.entries["Un/Caixa"].insert(0, str(product_data.get("UnitPerBox", "")))
        self.entries["Custo"].insert(0, str(product_data.get("BuyPrice", "")))

    def _validate_int(self, value):
        return value == "" or value.isdigit()

    def _validate_decimal(self, value):
        if value == "":
            return True
        try:
            float(value.replace(",", "."))
            return True
        except ValueError:
            return False

    def _save(self):
        errors = False 

        for field, entry in self.entries.items():
            entry.configure(background="white")  

        for field, entry in self.entries.items():
            value = entry.get().strip()
            if value == "":
                entry.configure(background="#ffcccc")
                errors = True
     
        if errors:
            messagebox.showerror("Erro", "Preencha todos os campos antes de salvar.")
            return

        product = {
            "SKU": self.entries["SKU"].get(),
            "Type": self.entries["Tipo"].get(),
            "Description": self.entries["Descrição"].get(),
            "UnitPerBox": self.entries["Un/Caixa"].get(),
            "BuyPrice": self.entries["Custo"].get()
        }

        try:
            product["UnitPerBox"] = int(product["UnitPerBox"])
        except ValueError:
            self.entries["Un/Caixa"].configure(background="#ffcccc")
            messagebox.showerror("Erro", "Un/Caixa deve ser um número inteiro.")
            return

        try:
            product["BuyPrice"] = product["BuyPrice"].replace(",", ".")
            product["BuyPrice"] = float(product["BuyPrice"])
        except ValueError:
            self.entries["Custo"].configure(background="#ffcccc")
            messagebox.showerror("Erro", "Custo deve ser um número decimal válido.")
            return

        self.on_submit(product)
        self.destroy()