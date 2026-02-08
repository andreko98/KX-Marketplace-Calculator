import tkinter as tk
from tkinter import ttk

from components.products.edit.edit_product_modal import EditProductModal
from components.products.new.new_product_modal import NewProductModal
from db.service.product_service import get_products, insert_product, update_product

class ProductListComponent(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        table_frame = tk.Frame(self)
        table_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        columns = ("SKU", "Tipo", "Descrição", "Un/Caixa", "Custo")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        self.tree.pack(expand=True, fill="both")
        
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        button_frame = tk.Frame(self)
        button_frame.grid(row=1, column=0, sticky="w", padx=10, pady=10)

        self.add_btn = ttk.Button(button_frame, text="Novo Produto", command=self.open_add_modal)
        self.add_btn.pack(side="left", padx=(0, 5))

        self.edit_btn = ttk.Button(button_frame, text="Editar", command=self.open_edit_modal)
        self.edit_btn.pack(side="left")
        self.edit_btn.pack_forget()

        self.load_products()

    def load_products(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        products = get_products()
        if not products:
            self.tree.insert("", tk.END, values=("---", "---", "Nenhum produto", "---", "---"))
        else:
            for p in products:
                self.tree.insert("", tk.END, values=(p["SKU"], p["Type"], p["Description"], p["UnitPerBox"], p["BuyPrice"]))

    def open_add_modal(self):
        NewProductModal(self, self.add_product)

    def add_product(self, product):
        insert_product(product)
        self.load_products()
        
    def on_select(self, event):
        selected = self.tree.selection()
        if len(selected) == 1:
            self.edit_btn.pack(side="left")
        else:
            self.edit_btn.pack_forget()
            
    def open_edit_modal(self):
        selected = self.tree.selection()
        if len(selected) != 1:
            return

        item = self.tree.item(selected[0], "values")
        product = {
            "SKU": item[0],
            "Type": item[1],
            "Description": item[2],
            "UnitPerBox": item[3],
            "BuyPrice": item[4]
        }
        EditProductModal(self, product, self.update_product)
        
    def update_product(self, product):
        update_product(product)
        self.load_products()