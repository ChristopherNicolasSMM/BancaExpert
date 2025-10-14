# log/logger.py
import logging
import sys
from pathlib import Path

def setup_logging(config):
    """Configura sistema de logging"""
    log_level = config.get('logging.level', 'INFO')
    log_file = config.get('logging.file', 'logs/app.log')
    
    # Cria diretório de logs se não existir
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    return logging.getLogger(__name__)