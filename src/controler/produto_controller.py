import sqlite3
from datetime import datetime
from utils.busca_interativa import BuscaInterativa
from utils.tui import clear_screen, print_header, print_footer_hotkeys, prompt_text, read_key, print_title, print_table

class ProdutoController:
    def __init__(self, database, usuario_logado=None):
        self.db = database
        self.busca = BuscaInterativa(database)
        self.usuario_logado = usuario_logado
    
    def listar_produtos(self):
        """Listar todos os produtos"""
        try:
            clear_screen()
            print_header(self.usuario_logado['nome'] if self.usuario_logado else None)
            produtos = self.db.executar_consulta('''
                SELECT p.*, c.nome as categoria_nome 
                FROM produtos p 
                LEFT JOIN categorias c ON p.categoria_id = c.id 
                WHERE p.ativo = 1
                ORDER BY p.nome
            ''')
            
            import os
            ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
            header_color = os.getenv('ANSI_HEADER_COLOR', 'yellow')
            print_title("LISTA DE PRODUTOS", ansi_enabled, header_color)
            headers = [("ID", 4), ("NOME", 20), ("CATEGORIA", 15), ("PREÇO", 10), ("ESTOQUE", 8), ("NCM", 12)]
            rows = []
            for produto in produtos:
                rows.append([
                    str(produto['id']),
                    str(produto['nome']),
                    str(produto['categoria_nome']),
                    f"R$ {produto['preco_venda']:.2f}",
                    str(produto['estoque']),
                    (produto['ncm'] or 'N/A')
                ])
            print_table(headers, rows, ansi_enabled, header_color, zebra=True)
            enabled_colors = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
            footer_color = os.getenv('ANSI_FOOTER_COLOR', 'cyan')
            print_footer_hotkeys([("F12","Voltar")], enabled_colors, footer_color)
            input("\nPressione Enter para continuar...")
            
        except sqlite3.Error as e:
            print(f"Erro ao listar produtos: {e}")
    
    def cadastrar_produto(self):
        """Cadastrar novo produto"""
        try:
            clear_screen()
            print_header(self.usuario_logado['nome'] if self.usuario_logado else None)
            import os
            ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
            header_color = os.getenv('ANSI_HEADER_COLOR', 'yellow')
            print_title("CADASTRAR NOVO PRODUTO", ansi_enabled, header_color)
            
            nome = prompt_text("Nome do produto: ")
            descricao = prompt_text("Descrição: ")
            
            # Usar busca interativa para categoria
            categoria = self.busca.buscar_categoria("SELECIONAR CATEGORIA PARA O PRODUTO")
            if not categoria:
                print("Categoria é obrigatória!")
                return
            categoria_id = categoria['id']
            
            preco_custo = float(prompt_text("Preço de custo: R$ "))
            preco_venda = float(prompt_text("Preço de venda: R$ "))
            estoque = int(prompt_text("Estoque inicial: "))
            estoque_minimo = int(prompt_text("Estoque mínimo: "))
            codigo_barras = prompt_text("Código de barras (opcional): ") or None
            ncm = prompt_text("NCM (opcional): ") or None
            cest = prompt_text("CEST (opcional): ") or None
            unidade = prompt_text("Unidade (UN, PCT, etc): ") or "UN"
            
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