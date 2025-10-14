import logging
import os
from datetime import datetime

def setup_logger():
    """Configurar sistema de logging"""
    # Criar diretório de logs se não existir
    os.makedirs('logs', exist_ok=True)
    
    # Configurar formato do log
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configurar logger principal
    logger = logging.getLogger('barcakpert')
    logger.setLevel(logging.INFO)
    
    # Handler para arquivo
    log_file = f'logs/barcakpert_{datetime.now().strftime("%Y%m%d")}.log'
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    
    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(log_format)
    console_handler.setFormatter(console_formatter)
    
    # Adicionar handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger