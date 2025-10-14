#!/usr/bin/env python3
"""
Sistema de Gerenciamento para Banca de Jornal - BarcaExpert
Sistema em console para cadastro de produtos e clientes
"""

import os
import sys
from cli.menu_principal import MenuPrincipal
from db.database import Database
from log.logger import setup_logger

def main():
    """Função principal do sistema"""
    try:
        # Configurar logger
        logger = setup_logger()
        logger.info("Iniciando sistema BarcaExpert")
        
        # Inicializar banco de dados
        db = Database()
        db.inicializar_tabelas()
        
        # Iniciar menu principal
        menu = MenuPrincipal(db)
        menu.executar()
        
    except KeyboardInterrupt:
        print("\n\nSistema encerrado pelo usuário")
        sys.exit(0)
    except Exception as e:
        print(f"Erro ao iniciar sistema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()