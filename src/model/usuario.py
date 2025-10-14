from dataclasses import dataclass
from typing import Optional
from enum import Enum

class NivelPermissao(Enum):
    ADMIN = "admin"
    OPERADOR = "operador"
    VENDEDOR = "vendedor"

@dataclass
class Usuario:
    id: Optional[int] = None
    username: str = ""
    password_hash: str = ""
    nome: str = ""
    nivel_permissao: NivelPermissao = NivelPermissao.OPERADOR
    ativo: bool = True
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password_hash': self.password_hash,
            'nome': self.nome,
            'nivel_permissao': self.nivel_permissao.value,
            'ativo': self.ativo
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get('id'),
            username=data.get('username', ''),
            password_hash=data.get('password_hash', ''),
            nome=data.get('nome', ''),
            nivel_permissao=NivelPermissao(data.get('nivel_permissao', 'operador')),
            ativo=bool(data.get('ativo', True))
        )
    
    def tem_permissao_admin(self):
        return self.nivel_permissao == NivelPermissao.ADMIN
    
    def tem_permissao_vendas(self):
        return self.nivel_permissao in [NivelPermissao.ADMIN, NivelPermissao.VENDEDOR, NivelPermissao.OPERADOR]
