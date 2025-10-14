# gui/main_window.py
import tkinter as tk
from tkinter import ttk, messagebox
from api.controller.transaction_controller import TransactionController

class MainWindow:
    def __init__(self, config, db_manager, logger):
        self.config = config
        self.db = db_manager
        self.logger = logger
        self.transaction_controller = TransactionController(db_manager)
        
    def run(self):
        """Inicia interface gráfica"""
        self.root = tk.Tk()
        self.root.title("Finance/dinian")
        self.root.geometry("800x600")
        
        self._create_widgets()
        self._load_data()
        
        self.root.mainloop()
    
    def _create_widgets(self):
        """Cria widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Botões
        ttk.Button(main_frame, text="Nova Transação", 
                  command=self._new_transaction).grid(row=0, column=0, pady=5)
        
        # Treeview para transações
        columns = ('ID', 'Descrição', 'Valor', 'Tipo', 'Categoria', 'Data')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings')
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def _load_data(self):
        """Carrega dados na treeview"""
        transactions = self.transaction_controller.get_transactions()
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for trans in transactions:
            self.tree.insert('', 'end', values=trans)
    
    def _new_transaction(self):
        """Abre diálogo para nova transação"""
        # Implementar diálogo de nova transação
        print("Nova transação")
        pass