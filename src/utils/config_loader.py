# ================================
# src/utils/config_loader.py
# ================================
"""Configuration loading utilities."""

import yaml
import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

class ConfigLoader:
    """Configuration loader for YAML files."""
    
    @staticmethod
    def load_config(config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        config_file = Path(config_path)
        if not config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_file, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    
    @staticmethod
    def load_env_variables() -> Dict[str, str]:
        """Load environment variables from .env file."""
        # Load .env file
        load_dotenv()
        
        return {
            'google_api_key': os.getenv('GOOGLE_API_KEY'),
            'environment': os.getenv('ENVIRONMENT', 'development'),
        }
