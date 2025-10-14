import os
from typing import List, Dict, Any, Optional, Callable

class BuscaInterativa:
    """Classe para busca interativa com diferentes critérios e seleção por índice"""
    
    def __init__(self, database):
        self.db = database
    
    def limpar_tela(self):
        """Limpar a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_resultados(self, resultados: List[Dict], titulo: str, colunas: List[str]):
        """Exibir resultados em formato tabular"""
        if not resultados:
            print("Nenhum resultado encontrado.")
            return
        
        print(f"\n{titulo}")
        print("=" * 80)
        
        # Cabeçalho
        header = f"{'IDX':<4}"
        for coluna in colunas:
            header += f" {coluna:<20}"
        print(header)
        print("-" * 80)
        
        # Dados
        for i, item in enumerate(resultados, 1):
            linha = f"{i:<4}"
            for coluna in colunas:
                valor = str(item.get(coluna, 'N/A'))[:20]
                linha += f" {valor:<20}"
            print(linha)
        
        print("-" * 80)
    
    def selecionar_por_indice(self, resultados: List[Dict], mensagem: str = "Escolha o índice") -> Optional[Dict]:
        """Permitir seleção por índice"""
        if not resultados:
            return None
        
        while True:
            try:
                indice = int(input(f"\n{mensagem} (1-{len(resultados)}): "))
                if 1 <= indice <= len(resultados):
                    return resultados[indice - 1]
                else:
                    print(f"Índice inválido! Digite um número entre 1 e {len(resultados)}")
            except ValueError:
                print("Digite um número válido!")
            except KeyboardInterrupt:
                print("\nOperação cancelada.")
                return None
    
    def menu_tipo_busca(self, entidade: str) -> str:
        """Menu para escolher tipo de busca"""
        print(f"\nComo deseja pesquisar {entidade}?")
        print("1. Por Nome")
        print("2. Por Descrição")
        print("3. Por Qualquer Texto")
        print("4. Digitar ID diretamente")
        print("0. Cancelar")
        
        while True:
            opcao = input("\nEscolha uma opção: ")
            if opcao == "1":
                return "nome"
            elif opcao == "2":
                return "descricao"
            elif opcao == "3":
                return "texto"
            elif opcao == "4":
                return "id"
            elif opcao == "0":
                return "cancelar"
            else:
                print("Opção inválida!")
    
    def buscar_categoria(self, titulo: str = "SELECIONAR CATEGORIA") -> Optional[Dict]:
        """Buscar categoria com diferentes critérios"""
        tipo_busca = self.menu_tipo_busca("categoria")
        
        if tipo_busca == "cancelar":
            return None
        
        if tipo_busca == "id":
            try:
                categoria_id = int(input("ID da categoria: "))
                resultado = self.db.executar_consulta(
                    "SELECT * FROM categorias WHERE id = ? AND ativo = 1", 
                    (categoria_id,)
                )
                return resultado[0] if resultado else None
            except ValueError:
                print("ID inválido!")
                return None
        
        # Busca por texto
        termo = input(f"Digite o termo para buscar por {tipo_busca}: ").strip()
        if not termo:
            print("Termo de busca não pode estar vazio!")
            return None
        
        # Construir query baseada no tipo de busca
        if tipo_busca == "nome":
            query = "SELECT * FROM categorias WHERE nome LIKE ? AND ativo = 1 ORDER BY nome"
            params = (f"%{termo}%",)
        elif tipo_busca == "descricao":
            query = "SELECT * FROM categorias WHERE descricao LIKE ? AND ativo = 1 ORDER BY nome"
            params = (f"%{termo}%",)
        else:  # texto
            query = "SELECT * FROM categorias WHERE (nome LIKE ? OR descricao LIKE ?) AND ativo = 1 ORDER BY nome"
            params = (f"%{termo}%", f"%{termo}%")
        
        resultados = self.db.executar_consulta(query, params)
        
        if not resultados:
            print("Nenhuma categoria encontrada!")
            return None
        
        # Converter para lista de dicionários
        categorias = [dict(cat) for cat in resultados]
        
        # Exibir resultados
        self.exibir_resultados(categorias, titulo, ['id', 'nome', 'descricao'])
        
        # Selecionar por índice
        return self.selecionar_por_indice(categorias, "Escolha a categoria")
    
    def buscar_produto(self, titulo: str = "SELECIONAR PRODUTO", com_estoque: bool = False) -> Optional[Dict]:
        """Buscar produto com diferentes critérios"""
        tipo_busca = self.menu_tipo_busca("produto")
        
        if tipo_busca == "cancelar":
            return None
        
        if tipo_busca == "id":
            try:
                produto_id = int(input("ID do produto: "))
                query = "SELECT * FROM produtos WHERE id = ? AND ativo = 1"
                if com_estoque:
                    query += " AND estoque > 0"
                resultado = self.db.executar_consulta(query, (produto_id,))
                return resultado[0] if resultado else None
            except ValueError:
                print("ID inválido!")
                return None
        
        # Busca por texto
        termo = input(f"Digite o termo para buscar por {tipo_busca}: ").strip()
        if not termo:
            print("Termo de busca não pode estar vazio!")
            return None
        
        # Construir query baseada no tipo de busca
        base_query = """
            SELECT p.*, c.nome as categoria_nome 
            FROM produtos p 
            LEFT JOIN categorias c ON p.categoria_id = c.id 
            WHERE p.ativo = 1
        """
        
        if com_estoque:
            base_query += " AND p.estoque > 0"
        
        if tipo_busca == "nome":
            base_query += " AND p.nome LIKE ?"
            params = (f"%{termo}%",)
        elif tipo_busca == "descricao":
            base_query += " AND p.descricao LIKE ?"
            params = (f"%{termo}%",)
        else:  # texto
            base_query += " AND (p.nome LIKE ? OR p.descricao LIKE ? OR p.codigo_barras LIKE ?)"
            params = (f"%{termo}%", f"%{termo}%", f"%{termo}%")
        
        base_query += " ORDER BY p.nome"
        
        resultados = self.db.executar_consulta(base_query, params)
        
        if not resultados:
            print("Nenhum produto encontrado!")
            return None
        
        # Converter para lista de dicionários
        produtos = [dict(prod) for prod in resultados]
        
        # Exibir resultados
        self.exibir_resultados(produtos, titulo, ['id', 'nome', 'categoria_nome', 'preco_venda', 'estoque'])
        
        # Selecionar por índice
        return self.selecionar_por_indice(produtos, "Escolha o produto")
    
    def buscar_cliente(self, titulo: str = "SELECIONAR CLIENTE") -> Optional[Dict]:
        """Buscar cliente com diferentes critérios"""
        tipo_busca = self.menu_tipo_busca("cliente")
        
        if tipo_busca == "cancelar":
            return None
        
        if tipo_busca == "id":
            try:
                cliente_id = int(input("ID do cliente: "))
                resultado = self.db.executar_consulta(
                    "SELECT * FROM clientes WHERE id = ? AND ativo = 1", 
                    (cliente_id,)
                )
                return resultado[0] if resultado else None
            except ValueError:
                print("ID inválido!")
                return None
        
        # Busca por texto
        termo = input(f"Digite o termo para buscar por {tipo_busca}: ").strip()
        if not termo:
            print("Termo de busca não pode estar vazio!")
            return None
        
        # Construir query baseada no tipo de busca
        if tipo_busca == "nome":
            query = "SELECT * FROM clientes WHERE nome LIKE ? AND ativo = 1 ORDER BY nome"
            params = (f"%{termo}%",)
        elif tipo_busca == "descricao":
            query = "SELECT * FROM clientes WHERE (telefone LIKE ? OR email LIKE ? OR endereco LIKE ?) AND ativo = 1 ORDER BY nome"
            params = (f"%{termo}%", f"%{termo}%", f"%{termo}%")
        else:  # texto
            query = "SELECT * FROM clientes WHERE (nome LIKE ? OR telefone LIKE ? OR email LIKE ? OR cpf_cnpj LIKE ?) AND ativo = 1 ORDER BY nome"
            params = (f"%{termo}%", f"%{termo}%", f"%{termo}%", f"%{termo}%")
        
        resultados = self.db.executar_consulta(query, params)
        
        if not resultados:
            print("Nenhum cliente encontrado!")
            return None
        
        # Converter para lista de dicionários
        clientes = [dict(cli) for cli in resultados]
        
        # Exibir resultados
        self.exibir_resultados(clientes, titulo, ['id', 'nome', 'telefone', 'email'])
        
        # Selecionar por índice
        return self.selecionar_por_indice(clientes, "Escolha o cliente")
    
    def buscar_usuario(self, titulo: str = "SELECIONAR USUÁRIO") -> Optional[Dict]:
        """Buscar usuário com diferentes critérios"""
        tipo_busca = self.menu_tipo_busca("usuário")
        
        if tipo_busca == "cancelar":
            return None
        
        if tipo_busca == "id":
            try:
                usuario_id = int(input("ID do usuário: "))
                resultado = self.db.executar_consulta(
                    "SELECT * FROM usuarios WHERE id = ? AND ativo = 1", 
                    (usuario_id,)
                )
                return resultado[0] if resultado else None
            except ValueError:
                print("ID inválido!")
                return None
        
        # Busca por texto
        termo = input(f"Digite o termo para buscar por {tipo_busca}: ").strip()
        if not termo:
            print("Termo de busca não pode estar vazio!")
            return None
        
        # Construir query baseada no tipo de busca
        if tipo_busca == "nome":
            query = "SELECT * FROM usuarios WHERE nome LIKE ? AND ativo = 1 ORDER BY nome"
            params = (f"%{termo}%",)
        elif tipo_busca == "descricao":
            query = "SELECT * FROM usuarios WHERE username LIKE ? AND ativo = 1 ORDER BY nome"
            params = (f"%{termo}%",)
        else:  # texto
            query = "SELECT * FROM usuarios WHERE (nome LIKE ? OR username LIKE ?) AND ativo = 1 ORDER BY nome"
            params = (f"%{termo}%", f"%{termo}%")
        
        resultados = self.db.executar_consulta(query, params)
        
        if not resultados:
            print("Nenhum usuário encontrado!")
            return None
        
        # Converter para lista de dicionários
        usuarios = [dict(usr) for usr in resultados]
        
        # Exibir resultados
        self.exibir_resultados(usuarios, titulo, ['id', 'username', 'nome', 'nivel_permissao'])
        
        # Selecionar por índice
        return self.selecionar_por_indice(usuarios, "Escolha o usuário")
