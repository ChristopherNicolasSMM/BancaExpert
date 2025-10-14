# Barcakpert - Sistema de Gerenciamento para Banca de Jornal

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Desenvolvimento-yellow.svg)

Sistema em console para gerenciamento completo de banca de jornal, incluindo cadastro de produtos, vendas, clientes, controle de estoque e relatórios.

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Módulos](#módulos)
- [Banco de Dados](#banco-de-dados)
- [Importação/Exportação](#importaçãoexportação)
- [Desenvolvimento](#desenvolvimento)
- [Licença](#licença)

## 🎯 Visão Geral

O Barcakpert é um sistema completo desenvolvido em Python para gerenciamento de bancas de jornal. Oferece controle de produtos, vendas, clientes, estoque e relatórios, com interface em console intuitiva e funcionalidades fiscais integradas.

## ✨ Funcionalidades

### 🏪 Gestão de Produtos
- Cadastro completo com dados fiscais (NCM, CEST, CFOP)
- Controle de estoque e alertas de estoque mínimo
- Categorização de produtos (revistas, doces, bebidas, etc.)
- Código de barras e múltiplas unidades de medida

### 💰 Sistema de Vendas
- Vendas rápidas com ou sem cliente
- Múltiplas formas de pagamento (dinheiro, cartão, PIX, fiado)
- Carrinho de compras interativo
- Controle de vendas em aberto (fiado)

### 👥 Gestão de Clientes
- Cadastro completo com dados de contato
- Sistema de limite de crédito
- Controle de vendas fiado
- Opção de operar sem cadastro de clientes

### 📊 Relatórios e Análises
- Relatório de vendas por período
- Controle de estoque e produtos em falta
- Situação financeira de clientes
- Exportação para Excel

### 🔄 Importação/Exportação
- Importação em lote via planilha Excel
- Modelo de planilha para download
- Exportação de produtos e vendas
- Backup de dados

### 🔐 Segurança e Permissões
- Sistema de usuários e níveis de acesso
- Controle de permissões por módulo
- Logs de atividades
- Dados sensíveis protegidos

## 🗂️ Estrutura do Projeto

```
Barcakpert/
├── src/
│   ├── __init__.py
│   ├── api/                 # Futura API REST
│   ├── cli/                 # Interface em console
│   │   └── menu_principal.py
│   ├── controller/          # Lógica de negócio
│   │   ├── produto_controller.py
│   │   ├── venda_controller.py
│   │   ├── cliente_controller.py
│   │   ├── import_export_controller.py
│   │   └── usuario_controller.py
│   ├── db/                  # Camada de dados
│   │   └── database.py
│   ├── debug/               # Ferramentas de debug
│   ├── gui/                 # Futura interface gráfica
│   ├── log/                 # Sistema de logging
│   │   └── logger.py
│   ├── logs/                # Arquivos de log
│   ├── model/               # Modelos de dados
│   ├── relatorios/          # Geração de relatórios
│   └── utils/               # Utilitários
├── export/                  # Arquivos exportados
├── backups/                 # Backup do banco
├── .env                     # Variáveis de ambiente
└── main.py                  # Arquivo principal
```

## 🚀 Instalação

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. **Clone ou baixe o projeto**
   ```bash
   git clone <url-do-repositorio>
   cd Barcakpert
   ```

2. **Instale as dependências**
   ```bash
   pip install pandas openpyxl python-dotenv
   ```

3. **Configure o ambiente** (opcional)
   - Edite o arquivo `.env` conforme necessário

4. **Execute o sistema**
   ```bash
   python main.py
   ```

## ⚙️ Configuração

### Arquivo .env
```env
# Configurações do Banco de Dados
DB_PATH=./barcakpert.db
DB_BACKUP_PATH=./backups/

# Configurações do Sistema
MODO_CLIENTE=sim              # Ativar sistema de clientes
PERMISSOES_STRICT=nao         # Controle rigoroso de permissões
LOG_LEVEL=INFO               # Nível de logging

# Configurações Fiscais
NCM_PADRAO_REVISTAS=49019900
NCM_PADRAO_DOCES=17049000
NCM_PADRAO_BEBIDAS=22021000
```

### Configurações Principais

- **MODO_CLIENTE**: Define se o sistema de clientes está ativo (`sim`/`nao`)
- **DB_PATH**: Caminho do arquivo do banco de dados SQLite
- **LOG_LEVEL**: Nível de detalhe dos logs (DEBUG, INFO, WARNING, ERROR)

## 💻 Uso

### Primeiro Acesso
1. Execute `python main.py`
2. Use as credenciais padrão:
   - **Usuário**: `admin`
   - **Senha**: `admin123`

### Menu Principal
```
SISTEMA BANCAKPERT - BANCA DE JORNAL
============================================================

MENU PRINCIPAL
1. Cadastro de Produtos
2. Vendas
3. Clientes
4. Relatórios
5. Importar/Exportar
6. Usuários e Permissões
0. Sair
```

### Fluxo de Trabalho Típico

1. **Cadastrar Produtos**: Menu 1 → Cadastrar Produto
2. **Realizar Venda**: Menu 2 → Nova Venda
3. **Consultar Estoque**: Menu 1 → Consultar Estoque
4. **Emitir Relatório**: Menu 4 → Relatório de Vendas

## 🧩 Módulos

### 1. Gestão de Produtos
- Cadastro com dados completos
- Controle de estoque em tempo real
- Categorização automática
- Alertas de reposição

### 2. Sistema de Vendas
- Interface de venda rápida
- Suporte a múltiplos pagamentos
- Carrinho com edição em tempo real
- Histórico completo

### 3. Gestão de Clientes
- Cadastro opcional
- Controle de limite de crédito
- Histórico de compras
- Situação financeira

### 4. Relatórios
- Vendas por período
- Produtos mais vendidos
- Estoque crítico
- Performance financeira

### 5. Importação/Exportação
- Planilhas Excel
- Modelos pré-formatados
- Backup de segurança
- Migração de dados

## 🗃️ Banco de Dados

### Tabelas Principais

- **produtos**: Cadastro completo de produtos
- **categorias**: Categorias de produtos
- **clientes**: Dados dos clientes
- **vendas**: Registro de vendas
- **venda_itens**: Itens de cada venda
- **usuarios**: Usuários do sistema

### Estrutura de Produtos
```sql
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY,
    codigo_barras TEXT,
    nome TEXT NOT NULL,
    descricao TEXT,
    categoria_id INTEGER,
    preco_custo DECIMAL(10,2),
    preco_venda DECIMAL(10,2),
    estoque INTEGER,
    estoque_minimo INTEGER,
    ncm TEXT,           -- Nomenclatura Comum do Mercosul
    cest TEXT,          -- Código Especificador da Substituição Tributária
    cfop TEXT,          -- Código Fiscal de Operações e Prestações
    unidade TEXT,
    ativo INTEGER
);
```

## 📤 Importação/Exportação

### Modelo de Planilha
Baixe o modelo em: `Menu 5 → Baixar modelo de planilha`

**Colunas obrigatórias:**
- nome
- preco_custo
- preco_venda  
- estoque

**Colunas opcionais:**
- descricao, categoria_id, codigo_barras, ncm, cest, unidade

### Formatos Suportados
- ✅ Excel (.xlsx)
- ✅ CSV (via Excel)
- ✅ Planilhas Google Sheets (exportação para Excel)

## 🛠️ Desenvolvimento

### Adicionando Novas Funcionalidades

1. **Novo Controller**
   ```python
   class NovoController:
       def __init__(self, database):
           self.db = database
   ```

2. **Integração com Menu**
   ```python
   # Em menu_principal.py
   def menu_novo(self):
       controller = NovoController(self.db)
       # Lógica do menu
   ```

### Logs e Debug
- Logs salvos em `logs/barcakpert_YYYYMMDD.log`
- Nível configurável via `.env`
- Timestamp e detalhes completos

### Backup
- Backup automático do banco
- Local: `backups/` 
- Recomendado backup externo periódico

## 📞 Suporte

### Problemas Comuns

1. **Erro de dependências**
   ```bash
   pip install --upgrade pandas openpyxl python-dotenv
   ```

2. **Arquivo de banco corrompido**
   - Use backup automático
   - Reinicie o sistema para recriação

3. **Problemas de permissão**
   - Verifique permissões de escrita nas pastas
   - Execute como administrador se necessário

### Logs de Erro
Consulte `logs/barcakpert_YYYYMMDD.log` para detalhes de erros.

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🔄 Changelog

### v1.0.0
- ✅ Sistema básico completo
- ✅ Gestão de produtos e vendas
- ✅ Controle de clientes
- ✅ Importação/Exportação Excel
- ✅ Sistema de usuários

### Próximas Versões
- [ ] Interface web
- [ ] API REST
- [ ] Aplicativo móvel
- [ ] Integração com impressoras térmicas
- [ ] Nota fiscal eletrônica (NFe)

## 👥 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

---

**Barcakpert** - Tornando a gestão da sua banca mais simples e eficiente! 🗞️✨