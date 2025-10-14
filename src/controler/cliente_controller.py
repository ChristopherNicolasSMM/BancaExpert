import sqlite3
from utils.busca_interativa import BuscaInterativa

class ClienteController:
    def __init__(self, database):
        self.db = database
        self.busca = BuscaInterativa(database)
    
    def listar_clientes(self):
        """Listar todos os clientes"""
        try:
            clientes = self.db.executar_consulta(
                "SELECT * FROM clientes WHERE ativo = 1 ORDER BY nome"
            )
            
            print("\nLISTA DE CLIENTES")
            print("-" * 80)
            print(f"{'ID':<3} {'NOME':<25} {'TELEFONE':<15} {'EMAIL':<25} {'LIMITE':<10}")
            print("-" * 80)
            
            for cliente in clientes:
                print(f"{cliente['id']:<3} {cliente['nome']:<25} {cliente['telefone'] or 'N/A':<15} "
                      f"{cliente['email'] or 'N/A':<25} R$ {cliente['limite_credito']:<8.2f}")
            
            print("-" * 80)
            input("\nPressione Enter para continuar...")
            
        except sqlite3.Error as e:
            print(f"Erro ao listar clientes: {e}")
    
    def cadastrar_cliente(self):
        """Cadastrar novo cliente"""
        try:
            print("\nCADASTRAR NOVO CLIENTE")
            print("-" * 40)
            
            nome = input("Nome: ")
            telefone = input("Telefone: ") or None
            email = input("Email: ") or None
            endereco = input("Endereço: ") or None
            cpf_cnpj = input("CPF/CNPJ: ") or None
            limite_credito = float(input("Limite de crédito: R$ ") or 0)
            
            cliente_id = self.db.executar_consulta('''
                INSERT INTO clientes (nome, telefone, email, endereco, cpf_cnpj, limite_credito)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nome, telefone, email, endereco, cpf_cnpj, limite_credito))
            
            print(f"\nCliente cadastrado com sucesso! ID: {cliente_id}")
            
        except ValueError:
            print("Erro: Limite de crédito deve ser um valor numérico!")
        except sqlite3.Error as e:
            print(f"Erro ao cadastrar cliente: {e}")
        input("Pressione Enter para continuar...")
    
    def editar_cliente(self):
        """Editar cliente existente"""
        try:
            # Usar busca interativa para selecionar cliente
            cliente = self.busca.buscar_cliente("SELECIONAR CLIENTE PARA EDITAR")
            if not cliente:
                print("Cliente não selecionado!")
                return
            
            cliente_id = cliente['id']
            print(f"\nEditando cliente: {cliente['nome']}")
            print("Deixe em branco para manter o valor atual")
            
            nome = input(f"Nome [{cliente['nome']}]: ") or cliente['nome']
            telefone = input(f"Telefone [{cliente['telefone']}]: ") or cliente['telefone']
            email = input(f"Email [{cliente['email']}]: ") or cliente['email']
            endereco = input(f"Endereço [{cliente['endereco']}]: ") or cliente['endereco']
            limite_credito = input(f"Limite crédito [R$ {cliente['limite_credito']}]: ") or cliente['limite_credito']
            
            self.db.executar_consulta('''
                UPDATE clientes 
                SET nome = ?, telefone = ?, email = ?, endereco = ?, limite_credito = ?
                WHERE id = ?
            ''', (nome, telefone, email, endereco, float(limite_credito), cliente_id))
            
            print("Cliente atualizado com sucesso!")
            
        except ValueError:
            print("Erro: Limite de crédito deve ser um valor numérico!")
        except sqlite3.Error as e:
            print(f"Erro ao editar cliente: {e}")
        input("Pressione Enter para continuar...")
    
    def excluir_cliente(self):
        """Excluir cliente (soft delete)"""
        try:
            # Usar busca interativa para selecionar cliente
            cliente = self.busca.buscar_cliente("SELECIONAR CLIENTE PARA EXCLUIR")
            if not cliente:
                print("Cliente não selecionado!")
                return
            
            cliente_id = cliente['id']
            print(f"\nCliente selecionado: {cliente['nome']}")
            
            # Verificar se cliente tem vendas em aberto
            vendas_aberto = self.db.executar_consulta('''
                SELECT COUNT(*) as qtd FROM vendas 
                WHERE cliente_id = ? AND forma_pagamento = 'fiado' AND status = 'concluida'
            ''', (cliente_id,))
            
            if vendas_aberto[0]['qtd'] > 0:
                print("Não é possível excluir cliente com vendas em aberto!")
                return
            
            confirmacao = input("Tem certeza que deseja excluir? (s/n): ")
            if confirmacao.lower() == 's':
                self.db.executar_consulta(
                    "UPDATE clientes SET ativo = 0 WHERE id = ?", 
                    (cliente_id,)
                )
                print("Cliente excluído com sucesso!")
            else:
                print("Operação cancelada.")
                
        except sqlite3.Error as e:
            print(f"Erro ao excluir cliente: {e}")
        input("Pressione Enter para continuar...")
    
    def consultar_limite_credito(self):
        """Consultar limite de crédito e situação do cliente"""
        try:
            # Usar busca interativa para selecionar cliente
            cliente = self.busca.buscar_cliente("SELECIONAR CLIENTE PARA CONSULTAR LIMITE")
            if not cliente:
                print("Cliente não selecionado!")
                return
            
            cliente_id = cliente['id']
            
            # Calcular total em aberto
            total_aberto = self.db.executar_consulta('''
                SELECT COALESCE(SUM(valor_total), 0) as total
                FROM vendas 
                WHERE cliente_id = ? AND forma_pagamento = 'fiado' AND status = 'concluida'
            ''', (cliente_id,))[0]['total']
            
            limite_disponivel = cliente['limite_credito'] - total_aberto
            
            print(f"\nSITUAÇÃO DO CLIENTE: {cliente['nome']}")
            print("=" * 50)
            print(f"Limite de crédito: R$ {cliente['limite_credito']:.2f}")
            print(f"Total em aberto: R$ {total_aberto:.2f}")
            print(f"Limite disponível: R$ {limite_disponivel:.2f}")
            print("=" * 50)
            
            # Listar vendas em aberto
            if total_aberto > 0:
                print("\nVENDAS EM ABERTO:")
                vendas_aberto = self.db.executar_consulta('''
                    SELECT id, data_venda, valor_total 
                    FROM vendas 
                    WHERE cliente_id = ? AND forma_pagamento = 'fiado' AND status = 'concluida'
                    ORDER BY data_venda
                ''', (cliente_id,))
                
                for venda in vendas_aberto:
                    print(f"  Venda {venda['id']} - {venda['data_venda']} - R$ {venda['valor_total']:.2f}")
            
        except sqlite3.Error as e:
            print(f"Erro ao consultar limite: {e}")
        input("\nPressione Enter para continuar...")
    
    def selecionar_cliente_interativo(self):
        """Selecionar cliente de forma interativa para venda"""
        try:
            # Usar busca interativa para selecionar cliente
            cliente = self.busca.buscar_cliente("SELECIONAR CLIENTE PARA VENDA")
            if not cliente:
                print("Nenhum cliente selecionado.")
                return None
            
            return cliente['id']
                    
        except sqlite3.Error as e:
            print(f"Erro ao selecionar cliente: {e}")
            return None