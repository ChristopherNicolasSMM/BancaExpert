import sqlite3
import os
from datetime import datetime
from utils.busca_interativa import BuscaInterativa
from utils.tui import read_key, print_footer_hotkeys, prompt_text, clear_screen, print_header, print_title, print_table
import os

class VendaController:
    def __init__(self, database, usuario_id, usuario_logado=None):
        self.db = database
        self.usuario_id = usuario_id
        self.usuario_logado = usuario_logado
        self.carrinho = []
        self.busca = BuscaInterativa(database)
    
    def nova_venda(self):
        """Processar nova venda"""
        try:
            self.carrinho = []
            cliente_id = None
            
            # Verificar se sistema de clientes está ativo
            modo_cliente = os.getenv('MODO_CLIENTE', 'sim').lower()
            
            if modo_cliente == 'sim':
                usar_cliente = input("Vincular a cliente? (s/n): ").lower()
                if usar_cliente == 's':
                    cliente_id = self.selecionar_cliente()
            
            # Adicionar itens ao carrinho com hotkeys
            while True:
                clear_screen()
                enabled_colors = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
                header_color = os.getenv('ANSI_HEADER_COLOR', 'yellow')
                print_header(self.usuario_logado['nome'] if self.usuario_logado else None, enabled_colors, header_color)
                self.exibir_carrinho()
                print("\nComandos: 1-Adicionar  2-Remover  3-Finalizar  0-Cancelar")
                print_footer_hotkeys([
                    ("F1", "Pesquisar"), ("F2", "Nome"), ("F3", "Remover"), ("F4", "Finalizar"),
                    ("F5", "Cliente"), ("F6", "Histórico"), ("F7", "Aberto"), ("F12", "Cancelar")
                ], enabled_colors, os.getenv('ANSI_FOOTER_COLOR', 'cyan'))
                print("Pressione uma tecla de atalho ou digite a opção e ENTER:")

                key = read_key()
                opcao = None
                if key in {"1", "2", "3", "0"}:
                    opcao = key
                elif key == "F1":
                    # Pesquisa geral
                    self.adicionar_produto_carrinho()
                    continue
                elif key == "F2":
                    # Pesquisa forçada por nome
                    self.adicionar_produto_carrinho(tipo_forcado="nome")
                    continue
                elif key == "F3":
                    self.remover_produto_carrinho()
                    continue
                elif key == "F4":
                    self.finalizar_venda(cliente_id)
                    break
                elif key == "F5":
                    cliente_id = self.selecionar_cliente()
                    continue
                elif key == "F6":
                    self.historico_vendas()
                    continue
                elif key == "F7":
                    self.vendas_aberto()
                    continue
                elif key == "F12" or key == "ESC":
                    print("Venda cancelada!")
                    break
                else:
                    opcao = prompt_text("\nEscolha uma opção: ")

                if opcao == "1":
                    self.adicionar_produto_carrinho()
                elif opcao == "2":
                    self.remover_produto_carrinho()
                elif opcao == "3":
                    self.finalizar_venda(cliente_id)
                    break
                elif opcao == "0":
                    print("Venda cancelada!")
                    break
                else:
                    print("Opção inválida!")
                    
        except Exception as e:
            print(f"Erro ao processar venda: {e}")
        input("Pressione Enter para continuar...")
    
    def adicionar_produto_carrinho(self, tipo_forcado=None):
        """Adicionar produto ao carrinho. tipo_forcado permite forçar o modo de busca (ex.: 'nome')."""
        try:
            # Usar busca interativa para selecionar produto
            produto = self.busca.buscar_produto("SELECIONAR PRODUTO PARA VENDA", com_estoque=True, tipo_forcado=tipo_forcado)
            if not produto:
                print("Produto não selecionado!")
                return
            print(f"Produto: {produto['nome']} | Preço: R$ {produto['preco_venda']:.2f} | Estoque: {produto['estoque']}")
            
            quantidade = int(prompt_text("Quantidade: "))
            
            if quantidade > produto['estoque']:
                print("Quantidade indisponível em estoque!")
                return
            
            # Verificar se produto já está no carrinho
            for item in self.carrinho:
                if item['produto_id'] == produto['id']:
                    item['quantidade'] += quantidade
                    item['subtotal'] = item['quantidade'] * item['preco_unitario']
                    break
            else:
                self.carrinho.append({
                    'produto_id': produto['id'],
                    'nome': produto['nome'],
                    'quantidade': quantidade,
                    'preco_unitario': produto['preco_venda'],
                    'subtotal': quantidade * produto['preco_venda']
                })
            
            print("Produto adicionado ao carrinho!")
            
        except ValueError:
            print("Quantidade deve ser um número inteiro!")
        except sqlite3.Error as e:
            print(f"Erro ao adicionar produto: {e}")
    
    def remover_produto_carrinho(self):
        """Remover produto do carrinho"""
        if not self.carrinho:
            print("Carrinho vazio!")
            return
        
        self.exibir_carrinho()
        try:
            index = int(input("\nNúmero do item a remover: ")) - 1
            
            if 0 <= index < len(self.carrinho):
                produto = self.carrinho.pop(index)
                print(f"Produto {produto['nome']} removido do carrinho!")
            else:
                print("Item inválido!")
                
        except ValueError:
            print("Número inválido!")
    
    def exibir_carrinho(self):
        """Exibir carrinho atual"""
        print("\n" + "=" * 60)
        print("CARRINHO DE COMPRAS")
        print("=" * 60)
        
        if not self.carrinho:
            print("Carrinho vazio")
            return
        
        total = 0
        for i, item in enumerate(self.carrinho, 1):
            print(f"{i}. {item['nome']} | {item['quantidade']} x R$ {item['preco_unitario']:.2f} = R$ {item['subtotal']:.2f}")
            total += item['subtotal']
        
        print("-" * 60)
        print(f"TOTAL: R$ {total:.2f}")
        print("=" * 60)
    
    def finalizar_venda(self, cliente_id):
        """Finalizar venda e salvar no banco"""
        if not self.carrinho:
            print("Carrinho vazio!")
            return
        
        try:
            total = sum(item['subtotal'] for item in self.carrinho)
            
            print(f"\nTotal da venda: R$ {total:.2f}")
            print("\nFormas de pagamento:")
            print("1. Dinheiro")
            print("2. Cartão de crédito")
            print("3. Cartão de débito")
            print("4. Pix")
            print("5. Fiado (conta)")
            
            forma_pagamento_opcoes = {
                '1': 'dinheiro',
                '2': 'credito',
                '3': 'debito',
                '4': 'pix',
                '5': 'fiado'
            }
            
            opcao_pagamento = input("\nForma de pagamento: ")
            forma_pagamento = forma_pagamento_opcoes.get(opcao_pagamento, 'dinheiro')
            
            # Inserir venda
            venda_id = self.db.executar_consulta('''
                INSERT INTO vendas (cliente_id, usuario_id, valor_total, forma_pagamento)
                VALUES (?, ?, ?, ?)
            ''', (cliente_id, self.usuario_id, total, forma_pagamento))
            
            # Inserir itens da venda e atualizar estoque
            for item in self.carrinho:
                self.db.executar_consulta('''
                    INSERT INTO venda_itens (venda_id, produto_id, quantidade, preco_unitario, subtotal)
                    VALUES (?, ?, ?, ?, ?)
                ''', (venda_id, item['produto_id'], item['quantidade'], item['preco_unitario'], item['subtotal']))
                
                # Atualizar estoque
                self.db.executar_consulta('''
                    UPDATE produtos 
                    SET estoque = estoque - ? 
                    WHERE id = ?
                ''', (item['quantidade'], item['produto_id']))
            
            print(f"\nVenda finalizada com sucesso! Nº {venda_id}")
            self.carrinho = []
            
        except sqlite3.Error as e:
            print(f"Erro ao finalizar venda: {e}")
    
    def selecionar_cliente(self):
        """Selecionar cliente para venda"""
        try:
            from controler.cliente_controller import ClienteController
            cliente_controller = ClienteController(self.db)
            return cliente_controller.selecionar_cliente_interativo()
        except Exception as e:
            print(f"Erro ao selecionar cliente: {e}")
            return None
    
    def historico_vendas(self):
        """Exibir histórico de vendas"""
        try:
            vendas = self.db.executar_consulta('''
                SELECT v.*, c.nome as cliente_nome, u.nome as usuario_nome
                FROM vendas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                LEFT JOIN usuarios u ON v.usuario_id = u.id
                ORDER BY v.data_venda DESC
                LIMIT 50
            ''')
            
            import os
            ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
            header_color = os.getenv('ANSI_HEADER_COLOR', 'yellow')
            print_title("HISTÓRICO DE VENDAS (Últimas 50)", ansi_enabled, header_color)
            headers = [("Nº", 4), ("DATA", 16), ("CLIENTE", 20), ("VALOR", 10), ("PAGAMENTO", 12), ("VENDEDOR", 15)]
            rows = []
            for venda in vendas:
                data = datetime.strptime(venda['data_venda'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y %H:%M')
                cliente = venda['cliente_nome'] or '---'
                rows.append([
                    str(venda['id']), data, cliente, f"R$ {venda['valor_total']:.2f}", venda['forma_pagamento'], venda['usuario_nome']
                ])
            print_table(headers, rows, ansi_enabled, header_color, zebra=True)
            
        except sqlite3.Error as e:
            print(f"Erro ao consultar histórico: {e}")
        input("\nPressione Enter para continuar...")
    
    def vendas_aberto(self):
        """Vendas em aberto (fiado)"""
        try:
            vendas_aberto = self.db.executar_consulta('''
                SELECT v.*, c.nome as cliente_nome, c.telefone
                FROM vendas v
                JOIN clientes c ON v.cliente_id = c.id
                WHERE v.forma_pagamento = 'fiado' AND v.status = 'concluida'
                ORDER BY v.data_venda
            ''')
            
            import os
            ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
            header_color = os.getenv('ANSI_HEADER_COLOR', 'yellow')
            print_title("VENDAS EM ABERTO (FIADO)", ansi_enabled, header_color)
            if not vendas_aberto:
                print("Nenhuma venda em aberto.")
                return
            headers = [("Nº", 6), ("CLIENTE", 20), ("DATA", 10), ("VALOR", 10), ("TEL", 14)]
            rows = []
            total_aberto = 0
            for venda in vendas_aberto:
                data = datetime.strptime(venda['data_venda'], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%y')
                rows.append([
                    str(venda['id']), venda['cliente_nome'], data, f"R$ {venda['valor_total']:.2f}", venda['telefone']
                ])
                total_aberto += venda['valor_total']
            print_table(headers, rows, ansi_enabled, header_color, zebra=True)
            print(f"\nTOTAL EM ABERTO: R$ {total_aberto:.2f}")
            
        except sqlite3.Error as e:
            print(f"Erro ao consultar vendas em aberto: {e}")
        input("\nPressione Enter para continuar...")