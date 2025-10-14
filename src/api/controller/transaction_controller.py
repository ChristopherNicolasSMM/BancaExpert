# api/controller/transaction_controller.py
from db.database import DatabaseManager
from model.transaction import Transaction

class TransactionController:
    def __init__(self, db_manager: DatabaseManager):
        self.db = db_manager
    
    def add_transaction(self, transaction: Transaction) -> bool:
        """Adiciona nova transação"""
        try:
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions 
                    (description, amount, type, category, date)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    transaction.description,
                    transaction.amount,
                    transaction.type,
                    transaction.category,
                    transaction.date
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Erro ao adicionar transação: {e}")
            return False
    
    def get_transactions(self, limit=100):
        """Obtém transações"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT * FROM transactions 
                ORDER BY date DESC 
                LIMIT ?
            ''', (limit,))
            return cursor.fetchall()