# ================================
# src/utils/logger.py
# ================================
"""Logging configuration."""

import logging
import logging.config
from pathlib import Path

def setup_logging(config_path: str = "config/logging_config.yaml"):
    """Setup logging configuration."""
    # Create logs directory if it doesn't exist
    Path("logs").mkdir(exist_ok=True)
    
    try:
        from .config_loader import ConfigLoader
        log_config = ConfigLoader.load_config(config_path)
        logging.config.dictConfig(log_config)
    except Exception:
        # Fallback to basic logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
