# model/transaction.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Transaction:
    id: Optional[int] = None
    description: str = ""
    amount: float = 0.0
    type: str = ""  # 'income' or 'expense'
    category: str = ""
    date: str = ""
    created_at: Optional[str] = None
    
    def to_dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'type': self.type,
            'category': self.category,
            'date': self.date
        }