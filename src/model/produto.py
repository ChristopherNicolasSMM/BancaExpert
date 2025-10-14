from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class Produto:
    id: Optional[int] = None
    codigo_barras: Optional[str] = None
    nome: str = ""
    descricao: Optional[str] = None
    categoria_id: Optional[int] = None
    preco_custo: Decimal = Decimal('0.00')
    preco_venda: Decimal = Decimal('0.00')
    estoque: int = 0
    estoque_minimo: int = 0
    ncm: Optional[str] = None
    cest: Optional[str] = None
    cfop: str = "5102"
    unidade: str = "UN"
    ativo: bool = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'codigo_barras': self.codigo_barras,
            'nome': self.nome,
            'descricao': self.descricao,
            'categoria_id': self.categoria_id,
            'preco_custo': float(self.preco_custo),
            'preco_venda': float(self.preco_venda),
            'estoque': self.estoque,
            'estoque_minimo': self.estoque_minimo,
            'ncm': self.ncm,
            'cest': self.cest,
            'cfop': self.cfop,
            'unidade': self.unidade,
            'ativo': self.ativo
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            codigo_barras=data.get('codigo_barras'),
            nome=data.get('nome', ''),
            descricao=data.get('descricao'),
            categoria_id=data.get('categoria_id'),
            preco_custo=Decimal(str(data.get('preco_custo', 0))),
            preco_venda=Decimal(str(data.get('preco_venda', 0))),
            estoque=data.get('estoque', 0),
            estoque_minimo=data.get('estoque_minimo', 0),
            ncm=data.get('ncm'),
            cest=data.get('cest'),
            cfop=data.get('cfop', '5102'),
            unidade=data.get('unidade', 'UN'),
            ativo=bool(data.get('ativo', True))
        )
