import os
import sys
from datetime import datetime
from utils.tui import read_key, print_footer_hotkeys, prompt_text, clear_screen, print_header
from dotenv import load_dotenv, set_key
import os

class MenuPrincipal:
    def __init__(self, database):
        self.db = database
        self.usuario_logado = None
        
    def limpar_tela(self):
        """Limpar a tela do terminal"""
        clear_screen()
    
    def exibir_cabecalho(self):
        """Exibir cabeçalho do sistema"""
        user_name = self.usuario_logado['nome'] if self.usuario_logado else None
        enabled_colors = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
        header_color = os.getenv('ANSI_HEADER_COLOR', 'yellow')
        print_header(user_name, enabled_colors, header_color)
    
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
            # Salvar sessão no .env
            try:
                env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env')
                env_path = os.path.abspath(env_path)
                set_key(env_path, 'SESSION_USER', str(self.usuario_logado.get('nome', '')))
                set_key(env_path, 'SESSION_USER_ID', str(self.usuario_logado.get('id', '')))
                set_key(env_path, 'SESSION_USER_LEVEL', str(self.usuario_logado.get('nivel_permissao', 'user')))
                # habilitar auto-login se configurado
                if os.getenv('AUTO_LOGIN_DEFAULT', 'nao').lower() == 'sim':
                    set_key(env_path, 'AUTO_LOGIN', 'sim')
            except Exception:
                pass
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
            print("7. Configurações")
            print("0. Sair")
            print()
            ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
            footer_color = os.getenv('ANSI_FOOTER_COLOR', 'cyan')
            print_footer_hotkeys([
                ("F1", "Pesquisar"), ("F2", "Por Nome"), ("F5", "Clientes"), ("F6", "Relatórios"),
                ("F7", "Import/Export"), ("F8", "Usuários"), ("F12", "Sair")
            ], ansi_enabled, footer_color)
            print("Use atalhos ou digite a opção e ENTER:")
            key = read_key()
            if key in {"1","2","3","4","5","6","7","0"}:
                opcao = key
            elif key == "F12":
                opcao = "0"
            elif key == "F5":
                opcao = "3"
            elif key == "F6":
                opcao = "4"
            elif key == "F7":
                opcao = "5"
            elif key == "F8":
                opcao = "6"
            elif key == "F9":
                opcao = "7"
            else:
                opcao = prompt_text("Escolha uma opção: ")
            
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
            elif opcao == "7":
                self.menu_configuracoes()
            elif opcao == "0":
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")
    
    def menu_produtos(self):
        """Menu de gerenciamento de produtos"""
        from controler.produto_controller import ProdutoController
        
        controller = ProdutoController(self.db, usuario_logado=self.usuario_logado)
        
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
            ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
            footer_color = os.getenv('ANSI_FOOTER_COLOR', 'cyan')
            print_footer_hotkeys([
                ("F1", "Buscar"), ("F2", "Por Nome"), ("F3", "Editar"), ("F4", "Excluir"),
                ("F5", "Estoque"), ("F12", "Voltar")
            ], ansi_enabled, footer_color)
            key = read_key()
            if key in {"1","2","3","4","5","0"}:
                opcao = key
            elif key == "F12":
                opcao = "0"
            elif key == "F5":
                opcao = "5"
            else:
                opcao = prompt_text("Escolha uma opção: ")
            
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
        from controler.venda_controller import VendaController
        
        controller = VendaController(self.db, self.usuario_logado['id'], usuario_logado=self.usuario_logado)
        
        while True:
            self.limpar_tela()
            self.exibir_cabecalho()
            
            print("MENU VENDAS")
            print("1. Nova Venda")
            print("2. Histórico de Vendas")
            print("3. Vendas em Aberto")
            print("0. Voltar")
            print()
            ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
            footer_color = os.getenv('ANSI_FOOTER_COLOR', 'cyan')
            print_footer_hotkeys([
                ("F1", "Nova"), ("F6", "Histórico"), ("F7", "Em Aberto"), ("F12", "Voltar")
            ], ansi_enabled, footer_color)
            key = read_key()
            if key in {"1","2","3","0"}:
                opcao = key
            elif key == "F1":
                opcao = "1"
            elif key == "F6":
                opcao = "2"
            elif key == "F7":
                opcao = "3"
            elif key == "F12":
                opcao = "0"
            else:
                opcao = prompt_text("Escolha uma opção: ")
            
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
        from controler.cliente_controller import ClienteController
        
        controller = ClienteController(self.db, usuario_logado=self.usuario_logado)
        
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
            ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
            footer_color = os.getenv('ANSI_FOOTER_COLOR', 'cyan')
            print_footer_hotkeys([
                ("F1", "Listar"), ("F2", "Cadastrar"), ("F3", "Editar"), ("F4", "Excluir"), ("F5", "Limite"), ("F12", "Voltar")
            ], ansi_enabled, footer_color)
            key = read_key()
            if key in {"1","2","3","4","5","0"}:
                opcao = key
            elif key == "F12":
                opcao = "0"
            elif key == "F5":
                opcao = "5"
            else:
                opcao = prompt_text("Escolha uma opção: ")
            
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
        self.limpar_tela()
        self.exibir_cabecalho()
        print("\nMÓDULO DE RELATÓRIOS")
        print("Em desenvolvimento...")
        ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
        footer_color = os.getenv('ANSI_FOOTER_COLOR', 'cyan')
        print_footer_hotkeys([("F12","Voltar")], ansi_enabled, footer_color)
        input("Pressione Enter para continuar...")
    
    def menu_importar_exportar(self):
        """Menu de importação/exportação"""
        from controler.import_export_controller import ImportExportController
        
        controller = ImportExportController(self.db)
        controller.menu_importar_exportar()

    def menu_configuracoes(self):
        """Menu de configurações (cores ANSI e sessão)"""
        from dotenv import set_key
        self.limpar_tela()
        self.exibir_cabecalho()
        ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower()
        header_color = os.getenv('ANSI_HEADER_COLOR', 'yellow')
        footer_color = os.getenv('ANSI_FOOTER_COLOR', 'cyan')
        auto_login = os.getenv('AUTO_LOGIN', 'nao').lower()
        print("CONFIGURAÇÕES")
        print("-" * 60)
        print(f"1. ANSI Enabled (sim/nao): {ansi_enabled}")
        print(f"2. ANSI Header Color: {header_color}")
        print(f"3. ANSI Footer Color: {footer_color}")
        print(f"4. Auto Login (sim/nao): {auto_login}")
        print("0. Voltar")
        print()
        print_footer_hotkeys([("F12","Voltar")])
        opcao = input("Escolha uma opção: ")
        env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))
        if opcao == '1':
            val = input("sim/nao: ").strip().lower() or ansi_enabled
            set_key(env_path, 'ANSI_ENABLED', 'sim' if val == 'sim' else 'nao')
        elif opcao == '2':
            val = input("Cor (yellow, cyan, blue, green, red, magenta, white): ").strip().lower() or header_color
            set_key(env_path, 'ANSI_HEADER_COLOR', val)
        elif opcao == '3':
            val = input("Cor (yellow, cyan, blue, green, red, magenta, white): ").strip().lower() or footer_color
            set_key(env_path, 'ANSI_FOOTER_COLOR', val)
        elif opcao == '4':
            val = input("sim/nao: ").strip().lower() or auto_login
            set_key(env_path, 'AUTO_LOGIN', 'sim' if val == 'sim' else 'nao')
        else:
            return
        input("\nConfiguração salva. Pressione Enter para continuar...")
    
    def menu_usuarios(self):
        """Menu de usuários"""
        if self.usuario_logado['nivel_permissao'] != 'admin':
            print("Acesso negado! Apenas administradores podem acessar este módulo.")
            input("Pressione Enter para continuar...")
            return
            
        self.limpar_tela()
        self.exibir_cabecalho()
        print("\nMÓDULO DE USUÁRIOS")
        print("Em desenvolvimento...")
        ansi_enabled = os.getenv('ANSI_ENABLED', 'nao').lower() == 'sim'
        footer_color = os.getenv('ANSI_FOOTER_COLOR', 'cyan')
        print_footer_hotkeys([("F12","Voltar")], ansi_enabled, footer_color)
        input("Pressione Enter para continuar...")
    
    def executar(self):
        """Executar o sistema"""
        load_dotenv()
        auto_login = os.getenv('AUTO_LOGIN', 'nao').lower() == 'sim'
        if auto_login and os.getenv('SESSION_USER') and os.getenv('SESSION_USER_ID'):
            self.usuario_logado = {
                'nome': os.getenv('SESSION_USER'),
                'id': int(os.getenv('SESSION_USER_ID') or 0),
                'nivel_permissao': os.getenv('SESSION_USER_LEVEL') or 'user'
            }
            self.menu_principal()
            return
        if self.login():
            self.menu_principal()