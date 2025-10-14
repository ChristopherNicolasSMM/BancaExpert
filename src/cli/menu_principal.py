import os
import sys
from datetime import datetime

class MenuPrincipal:
    def __init__(self, database):
        self.db = database
        self.usuario_logado = None
        
    def limpar_tela(self):
        """Limpar a tela do terminal"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_cabecalho(self):
        """Exibir cabeçalho do sistema"""
        print("=" * 60)
        print("           SISTEMA BANCAKPERT - BANCA DE JORNAL")
        print("=" * 60)
        if self.usuario_logado:
            print(f"Usuário: {self.usuario_logado['nome']} | Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        print()
    
    def login(self):
        """Sistema de login"""
        self.limpar_tela()
        print("=== LOGIN ===")
        username = input("Usuário: ")
        password = input("Senha: ")
        
        # Verificar credenciais (simplificado - em produção usar hash)
        usuario = self.db.executar_consulta(
            "SELECT * FROM usuarios WHERE username = ? AND password_hash = ? AND ativo = 1",
            (username, password)
        )
        
        if usuario:
            self.usuario_logado = usuario[0]
            return True
        else:
            print("Credenciais inválidas!")
            input("Pressione Enter para continuar...")
            return False
    
    def menu_principal(self):
        """Menu principal do sistema"""
        while True:
            self.limpar_tela()
            self.exibir_cabecalho()
            
            print("MENU PRINCIPAL")
            print("1. Cadastro de Produtos")
            print("2. Vendas")
            print("3. Clientes")
            print("4. Relatórios")
            print("5. Importar/Exportar")
            print("6. Usuários e Permissões")
            print("0. Sair")
            print()
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                self.menu_produtos()
            elif opcao == "2":
                self.menu_vendas()
            elif opcao == "3":
                self.menu_clientes()
            elif opcao == "4":
                self.menu_relatorios()
            elif opcao == "5":
                self.menu_importar_exportar()
            elif opcao == "6":
                self.menu_usuarios()
            elif opcao == "0":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")
    
    def menu_produtos(self):
        """Menu de gerenciamento de produtos"""
        from src.controller.produto_controller import ProdutoController
        
        controller = ProdutoController(self.db)
        
        while True:
            self.limpar_tela()
            self.exibir_cabecalho()
            
            print("MENU PRODUTOS")
            print("1. Listar Produtos")
            print("2. Cadastrar Produto")
            print("3. Editar Produto")
            print("4. Excluir Produto")
            print("5. Consultar Estoque")
            print("0. Voltar")
            print()
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                controller.listar_produtos()
            elif opcao == "2":
                controller.cadastrar_produto()
            elif opcao == "3":
                controller.editar_produto()
            elif opcao == "4":
                controller.excluir_produto()
            elif opcao == "5":
                controller.consultar_estoque()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")
    
    def menu_vendas(self):
        """Menu de vendas"""
        from src.controller.venda_controller import VendaController
        
        controller = VendaController(self.db, self.usuario_logado['id'])
        
        while True:
            self.limpar_tela()
            self.exibir_cabecalho()
            
            print("MENU VENDAS")
            print("1. Nova Venda")
            print("2. Histórico de Vendas")
            print("3. Vendas em Aberto")
            print("0. Voltar")
            print()
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                controller.nova_venda()
            elif opcao == "2":
                controller.historico_vendas()
            elif opcao == "3":
                controller.vendas_aberto()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")
    
    def menu_clientes(self):
        """Menu de clientes"""
        from src.controller.cliente_controller import ClienteController
        
        controller = ClienteController(self.db)
        
        while True:
            self.limpar_tela()
            self.exibir_cabecalho()
            
            print("MENU CLIENTES")
            print("1. Listar Clientes")
            print("2. Cadastrar Cliente")
            print("3. Editar Cliente")
            print("4. Excluir Cliente")
            print("5. Consultar Limite Crédito")
            print("0. Voltar")
            print()
            
            opcao = input("Escolha uma opção: ")
            
            if opcao == "1":
                controller.listar_clientes()
            elif opcao == "2":
                controller.cadastrar_cliente()
            elif opcao == "3":
                controller.editar_cliente()
            elif opcao == "4":
                controller.excluir_cliente()
            elif opcao == "5":
                controller.consultar_limite_credito()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")
    
    def menu_relatorios(self):
        """Menu de relatórios"""
        from src.controller.relatorio_controller import RelatorioController
        
        controller = RelatorioController(self.db)
        controller.menu_relatorios()
    
    def menu_importar_exportar(self):
        """Menu de importação/exportação"""
        from src.controller.import_export_controller import ImportExportController
        
        controller = ImportExportController(self.db)
        controller.menu_importar_exportar()
    
    def menu_usuarios(self):
        """Menu de usuários"""
        if self.usuario_logado['nivel_permissao'] != 'admin':
            print("Acesso negado! Apenas administradores podem acessar este módulo.")
            input("Pressione Enter para continuar...")
            return
            
        from src.controller.usuario_controller import UsuarioController
        
        controller = UsuarioController(self.db)
        controller.menu_usuarios()
    
    def executar(self):
        """Executar o sistema"""
        if self.login():
            self.menu_principal()