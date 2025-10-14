from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class Cliente:
    id: Optional[int] = None
    nome: str = ""
    telefone: Optional[str] = None
    email: Optional[str] = None
    endereco: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    limite_credito: Decimal = Decimal('0.00')
    ativo: bool = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'endereco': self.endereco,
            'cpf_cnpj': self.cpf_cnpj,
            'limite_credito': float(self.limite_credito),
            'ativo': self.ativo
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            nome=data.get('nome', ''),
            telefone=data.get('telefone'),
            email=data.get('email'),
            endereco=data.get('endereco'),
            cpf_cnpj=data.get('cpf_cnpj'),
            limite_credito=Decimal(str(data.get('limite_credito', 0))),
            ativo=bool(data.get('ativo', True))
        )
