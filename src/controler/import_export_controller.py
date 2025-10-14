import os
import pandas as pd
from datetime import datetime

class ImportExportController:
    def __init__(self, database):
        self.db = database
    
    def menu_importar_exportar(self):
        """Menu de importação/exportação"""
        while True:
            print("\nIMPORTAR/EXPORTAR DADOS")
            print("1. Baixar modelo de planilha")
            print("2. Importar produtos via Excel")
            print("3. Exportar produtos para Excel")
            print("4. Exportar relatório de vendas")
            print("0. Voltar")
            
            opcao = input("\nEscolha uma opção: ")
            
            if opcao == "1":
                self.baixar_modelo_planilha()
            elif opcao == "2":
                self.importar_produtos_excel()
            elif opcao == "3":
                self.exportar_produtos_excel()
            elif opcao == "4":
                self.exportar_relatorio_vendas()
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
    
    def baixar_modelo_planilha(self):
        """Criar planilha modelo para importação"""
        try:
            # Criar DataFrame com colunas do modelo
            modelo_data = {
                'nome': ['Exemplo Revista', 'Exemplo Doce'],
                'descricao': ['Revista mensal', 'Chocolate 100g'],
                'categoria_id': [1, 2],
                'preco_custo': [5.00, 1.50],
                'preco_venda': [8.00, 3.00],
                'estoque': [50, 100],
                'estoque_minimo': [10, 20],
                'codigo_barras': ['1234567890123', '9876543210987'],
                'ncm': ['49019900', '17049000'],
                'cest': ['', ''],
                'unidade': ['UN', 'UN']
            }
            
            df = pd.DataFrame(modelo_data)
            
            # Criar diretório se não existir
            os.makedirs('export', exist_ok=True)
            
            # Salvar arquivo
            caminho = 'export/modelo_importacao_produtos.xlsx'
            df.to_excel(caminho, index=False, sheet_name='Produtos')
            
            print(f"Modelo baixado com sucesso: {caminho}")
            print("\nINSTRUÇÕES:")
            print("- Preencha os dados na planilha mantendo o formato")
            print("- A coluna 'categoria_id' deve conter IDs válidos das categorias")
            print("- Salve o arquivo e use a opção 'Importar produtos via Excel'")
            
        except Exception as e:
            print(f"Erro ao criar modelo: {e}")
        input("\nPressione Enter para continuar...")
    
    def importar_produtos_excel(self):
        """Importar produtos de arquivo Excel"""
        try:
            caminho = input("\nCaminho do arquivo Excel: ")
            
            if not os.path.exists(caminho):
                print("Arquivo não encontrado!")
                return
            
            # Ler arquivo Excel
            df = pd.read_excel(caminho)
            
            # Validar colunas obrigatórias
            colunas_obrigatorias = ['nome', 'preco_custo', 'preco_venda', 'estoque']
            for coluna in colunas_obrigatorias:
                if coluna not in df.columns:
                    print(f"Coluna obrigatória '{coluna}' não encontrada!")
                    return
            
            print(f"\nEncontrados {len(df)} produtos para importar")
            print("Iniciando importação...")
            
            sucesso = 0
            erros = 0
            
            for index, row in df.iterrows():
                try:
                    # Preparar dados
                    dados = {
                        'nome': str(row['nome']),
                        'descricao': str(row.get('descricao', '')),
                        'categoria_id': int(row.get('categoria_id', 7)),  # Default: Diversos
                        'preco_custo': float(row['preco_custo']),
                        'preco_venda': float(row['preco_venda']),
                        'estoque': int(row['estoque']),
                        'estoque_minimo': int(row.get('estoque_minimo', 0)),
                        'codigo_barras': str(row.get('codigo_barras', '')) or None,
                        'ncm': str(row.get('ncm', '')) or None,
                        'cest': str(row.get('cest', '')) or None,
                        'unidade': str(row.get('unidade', 'UN'))
                    }
                    
                    # Inserir no banco
                    self.db.executar_consulta('''
                        INSERT INTO produtos (
                            nome, descricao, categoria_id, preco_custo, preco_venda,
                            estoque, estoque_minimo, codigo_barras, ncm, cest, unidade
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', tuple(dados.values()))
                    
                    sucesso += 1
                    
                except Exception as e:
                    print(f"Erro na linha {index + 2}: {e}")
                    erros += 1
            
            print(f"\nImportação concluída!")
            print(f"Sucesso: {sucesso} | Erros: {erros}")
            
        except Exception as e:
            print(f"Erro na importação: {e}")
        input("\nPressione Enter para continuar...")
    
    def exportar_produtos_excel(self):
        """Exportar produtos para Excel"""
        try:
            # Buscar produtos
            produtos = self.db.executar_consulta('''
                SELECT p.*, c.nome as categoria_nome
                FROM produtos p 
                LEFT JOIN categorias c ON p.categoria_id = c.id 
                WHERE p.ativo = 1
                ORDER BY p.nome
            ''')
            
            # Converter para DataFrame
            dados = []
            for produto in produtos:
                dados.append({
                    'id': produto['id'],
                    'nome': produto['nome'],
                    'descricao': produto['descricao'],
                    'categoria': produto['categoria_nome'],
                    'preco_custo': produto['preco_custo'],
                    'preco_venda': produto['preco_venda'],
                    'estoque': produto['estoque'],
                    'estoque_minimo': produto['estoque_minimo'],
                    'codigo_barras': produto['codigo_barras'],
                    'ncm': produto['ncm'],
                    'cest': produto['cest'],
                    'unidade': produto['unidade']
                })
            
            df = pd.DataFrame(dados)
            
            # Criar diretório se não existir
            os.makedirs('export', exist_ok=True)
            
            # Salvar arquivo
            data_hora = datetime.now().strftime('%Y%m%d_%H%M%S')
            caminho = f'export/produtos_exportados_{data_hora}.xlsx'
            df.to_excel(caminho, index=False)
            
            print(f"Produtos exportados com sucesso: {caminho}")
            print(f"Total de produtos exportados: {len(produtos)}")
            
        except Exception as e:
            print(f"Erro ao exportar produtos: {e}")
        input("\nPressione Enter para continuar...")
    
    def exportar_relatorio_vendas(self):
        """Exportar relatório de vendas para Excel"""
        try:
            # Buscar vendas
            vendas = self.db.executar_consulta('''
                SELECT v.*, c.nome as cliente_nome, u.nome as usuario_nome
                FROM vendas v
                LEFT JOIN clientes c ON v.cliente_id = c.id
                LEFT JOIN usuarios u ON v.usuario_id = u.id
                ORDER BY v.data_venda DESC
            ''')
            
            # Converter para DataFrame
            dados = []
            for venda in vendas:
                dados.append({
                    'id': venda['id'],
                    'data_venda': venda['data_venda'],
                    'cliente': venda['cliente_nome'] or 'Não informado',
                    'vendedor': venda['usuario_nome'],
                    'valor_total': venda['valor_total'],
                    'forma_pagamento': venda['forma_pagamento'],
                    'status': venda['status']
                })
            
            df = pd.DataFrame(dados)
            
            # Criar diretório se não existir
            os.makedirs('export', exist_ok=True)
            
            # Salvar arquivo
            data_hora = datetime.now().strftime('%Y%m%d_%H%M%S')
            caminho = f'export/relatorio_vendas_{data_hora}.xlsx'
            df.to_excel(caminho, index=False)
            
            print(f"Relatório de vendas exportado: {caminho}")
            print(f"Total de vendas no relatório: {len(vendas)}")
            
        except Exception as e:
            print(f"Erro ao exportar relatório: {e}")
        input("\nPressione Enter para continuar...")