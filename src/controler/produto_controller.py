import sqlite3
from datetime import datetime
from utils.busca_interativa import BuscaInterativa

class ProdutoController:
    def __init__(self, database):
        self.db = database
        self.busca = BuscaInterativa(database)
    
    def listar_produtos(self):
        """Listar todos os produtos"""
        try:
            produtos = self.db.executar_consulta('''
                SELECT p.*, c.nome as categoria_nome 
                FROM produtos p 
                LEFT JOIN categorias c ON p.categoria_id = c.id 
                WHERE p.ativo = 1
                ORDER BY p.nome
            ''')
            
            print("\nLISTA DE PRODUTOS")
            print("-" * 100)
            print(f"{'ID':<3} {'NOME':<20} {'CATEGORIA':<15} {'PREÇO':<10} {'ESTOQUE':<8} {'NCM':<12}")
            print("-" * 100)
            
            for produto in produtos:
                print(f"{produto['id']:<3} {produto['nome']:<20} {produto['categoria_nome']:<15} "
                      f"R$ {produto['preco_venda']:<8.2f} {produto['estoque']:<8} {produto['ncm'] or 'N/A':<12}")
            
            print("-" * 100)
            input("\nPressione Enter para continuar...")
            
        except sqlite3.Error as e:
            print(f"Erro ao listar produtos: {e}")
    
    def cadastrar_produto(self):
        """Cadastrar novo produto"""
        try:
            print("\nCADASTRAR NOVO PRODUTO")
            print("-" * 40)
            
            nome = input("Nome do produto: ")
            descricao = input("Descrição: ")
            
            # Usar busca interativa para categoria
            categoria = self.busca.buscar_categoria("SELECIONAR CATEGORIA PARA O PRODUTO")
            if not categoria:
                print("Categoria é obrigatória!")
                return
            categoria_id = categoria['id']
            
            preco_custo = float(input("Preço de custo: R$ "))
            preco_venda = float(input("Preço de venda: R$ "))
            estoque = int(input("Estoque inicial: "))
            estoque_minimo = int(input("Estoque mínimo: "))
            codigo_barras = input("Código de barras (opcional): ") or None
            ncm = input("NCM (opcional): ") or None
            cest = input("CEST (opcional): ") or None
            unidade = input("Unidade (UN, PCT, etc): ") or "UN"
            
            produto_id = self.db.executar_consulta('''
                INSERT INTO produtos (
                    nome, descricao, categoria_id, preco_custo, preco_venda, 
                    estoque, estoque_minimo, codigo_barras, ncm, cest, unidade
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nome, descricao, categoria_id, preco_custo, preco_venda, 
                  estoque, estoque_minimo, codigo_barras, ncm, cest, unidade))
            
            print(f"\nProduto cadastrado com sucesso! ID: {produto_id}")
            input("Pressione Enter para continuar...")
            
        except ValueError:
            print("Erro: Valores numéricos inválidos!")
        except sqlite3.Error as e:
            print(f"Erro ao cadastrar produto: {e}")
        input("Pressione Enter para continuar...")
    
    def editar_produto(self):
        """Editar produto existente"""
        try:
            # Usar busca interativa para selecionar produto
            produto = self.busca.buscar_produto("SELECIONAR PRODUTO PARA EDITAR")
            if not produto:
                print("Produto não selecionado!")
                return
            
            produto_id = produto['id']
            print(f"\nEditando produto: {produto['nome']}")
            print("Deixe em branco para manter o valor atual")
            
            nome = input(f"Nome [{produto['nome']}]: ") or produto['nome']
            descricao = input(f"Descrição [{produto['descricao']}]: ") or produto['descricao']
            preco_custo = input(f"Preço custo [R$ {produto['preco_custo']}]: ") or produto['preco_custo']
            preco_venda = input(f"Preço venda [R$ {produto['preco_venda']}]: ") or produto['preco_venda']
            estoque = input(f"Estoque [{produto['estoque']}]: ") or produto['estoque']
            ncm = input(f"NCM [{produto['ncm']}]: ") or produto['ncm']
            
            self.db.executar_consulta('''
                UPDATE produtos 
                SET nome = ?, descricao = ?, preco_custo = ?, preco_venda = ?, 
                    estoque = ?, ncm = ?, data_atualizacao = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (nome, descricao, float(preco_custo), float(preco_venda), 
                  int(estoque), ncm, produto_id))
            
            print("Produto atualizado com sucesso!")
            
        except ValueError:
            print("Erro: Valores numéricos inválidos!")
        except sqlite3.Error as e:
            print(f"Erro ao editar produto: {e}")
        input("Pressione Enter para continuar...")
    
    def excluir_produto(self):
        """Excluir produto (soft delete)"""
        try:
            # Usar busca interativa para selecionar produto
            produto = self.busca.buscar_produto("SELECIONAR PRODUTO PARA EXCLUIR")
            if not produto:
                print("Produto não selecionado!")
                return
            
            produto_id = produto['id']
            print(f"\nProduto selecionado: {produto['nome']}")
            
            confirmacao = input("Tem certeza que deseja excluir? (s/n): ")
            if confirmacao.lower() == 's':
                self.db.executar_consulta(
                    "UPDATE produtos SET ativo = 0 WHERE id = ?", 
                    (produto_id,)
                )
                print("Produto excluído com sucesso!")
            else:
                print("Operação cancelada.")
                
        except sqlite3.Error as e:
            print(f"Erro ao excluir produto: {e}")
        input("Pressione Enter para continuar...")
    
    def consultar_estoque(self):
        """Consultar situação do estoque"""
        try:
            # Produtos com estoque baixo
            estoque_baixo = self.db.executar_consulta('''
                SELECT p.*, c.nome as categoria_nome
                FROM produtos p 
                LEFT JOIN categorias c ON p.categoria_id = c.id
                WHERE p.estoque <= p.estoque_minimo AND p.ativo = 1
                ORDER BY p.estoque ASC
            ''')
            
            print("\nPRODUTOS COM ESTOQUE BAIXO")
            print("-" * 80)
            
            if estoque_baixo:
                for produto in estoque_baixo:
                    print(f"{produto['nome']} - Estoque: {produto['estoque']} "
                          f"(Mínimo: {produto['estoque_minimo']})")
            else:
                print("Nenhum produto com estoque baixo.")
            
            print("\n" + "=" * 80)
            
            # Estoque por categoria
            estoque_categoria = self.db.executar_consulta('''
                SELECT c.nome, COUNT(p.id) as qtd_produtos, SUM(p.estoque) as total_estoque
                FROM categorias c
                LEFT JOIN produtos p ON c.id = p.categoria_id AND p.ativo = 1
                WHERE c.ativo = 1
                GROUP BY c.id, c.nome
            ''')
            
            print("\nESTOQUE POR CATEGORIA")
            print("-" * 50)
            for cat in estoque_categoria:
                print(f"{cat['nome']:<15} {cat['qtd_produtos']:<3} produtos | "
                      f"Estoque total: {cat['total_estoque'] or 0}")
            
        except sqlite3.Error as e:
            print(f"Erro ao consultar estoque: {e}")
        input("\nPressione Enter para continuar...")