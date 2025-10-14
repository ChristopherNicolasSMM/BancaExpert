from dataclasses import dataclass
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from enum import Enum

class FormaPagamento(Enum):
    DINHEIRO = "dinheiro"
    CREDITO = "credito"
    DEBITO = "debito"
    PIX = "pix"
    FIADO = "fiado"

class StatusVenda(Enum):
    CONCLUIDA = "concluida"
    CANCELADA = "cancelada"
    PENDENTE = "pendente"

@dataclass
class ItemVenda:
    id: Optional[int] = None
    venda_id: Optional[int] = None
    produto_id: int = 0
    quantidade: int = 0
    preco_unitario: Decimal = Decimal('0.00')
    subtotal: Decimal = Decimal('0.00')
    
    def calcular_subtotal(self):
        self.subtotal = self.preco_unitario * self.quantidade
        return self.subtotal

@dataclass
class Venda:
    id: Optional[int] = None
    cliente_id: Optional[int] = None
    usuario_id: int = 0
    valor_total: Decimal = Decimal('0.00')
    forma_pagamento: FormaPagamento = FormaPagamento.DINHEIRO
    status: StatusVenda = StatusVenda.CONCLUIDA
    data_venda: Optional[datetime] = None
    itens: List[ItemVenda] = None
    
    def __post_init__(self):
        if self.itens is None:
            self.itens = []
        if self.data_venda is None:
            self.data_venda = datetime.now()
    
    def calcular_total(self):
        self.valor_total = sum(item.calcular_subtotal() for item in self.itens)
        return self.valor_total
    
    def adicionar_item(self, produto_id: int, quantidade: int, preco_unitario: Decimal):
        item = ItemVenda(
            produto_id=produto_id,
            quantidade=quantidade,
            preco_unitario=preco_unitario
        )
        item.calcular_subtotal()
        self.itens.append(item)
        self.calcular_total()
    
    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'usuario_id': self.usuario_id,
            'valor_total': float(self.valor_total),
            'forma_pagamento': self.forma_pagamento.value,
            'status': self.status.value,
            'data_venda': self.data_venda.isoformat() if self.data_venda else None,
            'itens': [item.__dict__ for item in self.itens]
        }
