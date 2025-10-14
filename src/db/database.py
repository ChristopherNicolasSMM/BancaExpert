import sqlite3
import os
from datetime import datetime
import logging

class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            # Usar diretório do executável como base para o banco
            base_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(base_dir, 'barcaExpert.db')
        
        self.db_path = db_path
        self.conn = None
        self.logger = logging.getLogger(__name__)
        
    def conectar(self):
        """Conectar ao banco de dados"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            return self.conn
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao conectar ao banco: {e}")
            raise
    
    def inicializar_tabelas(self):
        """Inicializar todas as tabelas do sistema"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            
            # Tabela de usuários
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    nome TEXT NOT NULL,
                    nivel_permissao TEXT NOT NULL DEFAULT 'operador',
                    ativo INTEGER DEFAULT 1,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de categorias de produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS categorias (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    ativo INTEGER DEFAULT 1
                )
            ''')
            
            # Tabela de produtos
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    codigo_barras TEXT UNIQUE,
                    nome TEXT NOT NULL,
                    descricao TEXT,
                    categoria_id INTEGER,
                    preco_custo DECIMAL(10,2) NOT NULL,
                    preco_venda DECIMAL(10,2) NOT NULL,
                    estoque INTEGER DEFAULT 0,
                    estoque_minimo INTEGER DEFAULT 0,
                    ncm TEXT,
                    cest TEXT,
                    cfop TEXT DEFAULT '5102',
                    unidade TEXT DEFAULT 'UN',
                    ativo INTEGER DEFAULT 1,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (categoria_id) REFERENCES categorias (id)
                )
            ''')
            
            # Tabela de clientes
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clientes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    telefone TEXT,
                    email TEXT,
                    endereco TEXT,
                    cpf_cnpj TEXT,
                    limite_credito DECIMAL(10,2) DEFAULT 0,
                    ativo INTEGER DEFAULT 1,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabela de vendas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vendas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER,
                    usuario_id INTEGER NOT NULL,
                    valor_total DECIMAL(10,2) NOT NULL,
                    forma_pagamento TEXT DEFAULT 'dinheiro',
                    status TEXT DEFAULT 'concluida',
                    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                    FOREIGN KEY (usuario_id) REFERENCES usuarios (id)
                )
            ''')
            
            # Tabela de itens da venda
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS venda_itens (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    venda_id INTEGER NOT NULL,
                    produto_id INTEGER NOT NULL,
                    quantidade INTEGER NOT NULL,
                    preco_unitario DECIMAL(10,2) NOT NULL,
                    subtotal DECIMAL(10,2) NOT NULL,
                    FOREIGN KEY (venda_id) REFERENCES vendas (id),
                    FOREIGN KEY (produto_id) REFERENCES produtos (id)
                )
            ''')
            
            # Inserir categorias padrão
            categorias_padrao = [
                ('Revistas', 'Revistas e periódicos'),
                ('Doces', 'Doces, balas e chocolates'),
                ('Refrigerantes', 'Bebidas não alcoólicas'),
                ('Cervejas', 'Bebidas alcoólicas'),
                ('Salgadinhos', 'Salgadinhos e snacks'),
                ('Tabaco', 'Cigarros e derivados'),
                ('Diversos', 'Outros produtos')
            ]
            
            cursor.executemany(
                'INSERT OR IGNORE INTO categorias (nome, descricao) VALUES (?, ?)',
                categorias_padrao
            )
            
            # Inserir usuário admin padrão
            cursor.execute('''
                INSERT OR IGNORE INTO usuarios (username, password_hash, nome, nivel_permissao)
                VALUES ('admin', 'admin123', 'Administrador', 'admin')
            ''')
            
            conn.commit()
            self.logger.info("Tabelas inicializadas com sucesso")
            
        except sqlite3.Error as e:
            self.logger.error(f"Erro ao inicializar tabelas: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def executar_consulta(self, query, params=None):
        """Executar consulta no banco de dados"""
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                conn.commit()
                return cursor.lastrowid
                
        except sqlite3.Error as e:
            self.logger.error(f"Erro na consulta: {e}")
            raise
        finally:
            if conn:
                conn.close()