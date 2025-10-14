# utils/config.py
import os
import json
from pathlib import Path

class Config:
    def __init__(self, config_file="config.json"):
        self.config_file = Path(__file__).parent.parent / config_file
        self.settings = self._load_config()
    
    def _load_config(self):
        """Carrega configurações do arquivo JSON"""
        default_config = {
            "database": {
                "path": "db/finance.db",
                "type": "sqlite"
            },
            "logging": {
                "level": "INFO",
                "file": "logs/app.log"
            },
            "gui": {
                "theme": "dark",
                "language": "pt-BR"
            }
        }
        
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return {**default_config, **json.load(f)}
        return default_config
    
    def get(self, key, default=None):
        """Obtém valor da configuração"""
        keys = key.split('.')
        value = self.settings
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default