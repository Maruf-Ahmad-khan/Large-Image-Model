# # ================================
# # src/utils/logger.py
# # ================================
# """Logging configuration."""

# import logging
# import logging.config
# from pathlib import Path

# def setup_logging(config_path: str = "config/logging_config.yaml"):
#     """Setup logging configuration."""
#     # Create logs directory if it doesn't exist
#     Path("logs").mkdir(exist_ok=True)
    
#     try:
#         from .config_loader import ConfigLoader
#         log_config = ConfigLoader.load_config(config_path)
#         logging.config.dictConfig(log_config)
#     except Exception:
#         # Fallback to basic logging
#         logging.basicConfig(
#             level=logging.INFO,
#             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#         )

# src/utils/logger.py
"""Advanced logging configuration with rotation and structured formatting."""

import logging
import logging.config
import logging.handlers
from pathlib import Path
import sys
import json
from datetime import datetime
from typing import Dict, Any, Optional

class JSONFormatter(logging.Formatter):
    """Custom JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry, ensure_ascii=False)

class LoggerSetup:
    """Logger configuration and setup class."""
    
    def __init__(self):
        self.logs_dir = Path("logs")
        self.setup_directories()
    
    def setup_directories(self) -> None:
        """Create necessary directories."""
        self.logs_dir.mkdir(exist_ok=True)
    
    def get_logging_config(self) -> Dict[str, Any]:
        """Get comprehensive logging configuration."""
        
        return {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'standard': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
                },
                'json': {
                    '()': JSONFormatter,
                },
                'detailed': {
                    'format': '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(funcName)s - %(message)s'
                }
            },
            'handlers': {
                'app_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'filename': str(self.logs_dir / 'app.log'),
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'encoding': 'utf-8',
                },
                'error_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'ERROR',
                    'formatter': 'detailed',
                    'filename': str(self.logs_dir / 'errors.log'),
                    'maxBytes': 10485760,  # 10MB
                    'backupCount': 5,
                    'encoding': 'utf-8',
                },
                'console': {
                    'class': 'logging.StreamHandler',
                    'level': 'INFO',
                    'formatter': 'standard',
                    'stream': sys.stdout,
                },
                'json_file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'level': 'DEBUG',
                    'formatter': 'json',
                    'filename': str(self.logs_dir / 'structured.log'),
                    'maxBytes': 10485760,
                    'backupCount': 3,
                    'encoding': 'utf-8',
                }
            },
            'loggers': {
                'src': {
                    'level': 'DEBUG',
                    'handlers': ['app_file', 'console', 'json_file'],
                    'propagate': False
                },
                'src.ui': {
                    'level': 'INFO',
                    'handlers': ['app_file', 'console', 'error_file'],
                    'propagate': False
                },
                'src.llm': {
                    'level': 'DEBUG',
                    'handlers': ['app_file', 'console', 'json_file'],
                    'propagate': False
                },
                'src.utils': {
                    'level': 'DEBUG',
                    'handlers': ['app_file', 'console', 'json_file'],
                    'propagate': False
                }
            },
            'root': {
                'level': 'INFO',
                'handlers': ['console', 'app_file']
            }
        }
    
    def setup_logging(self) -> None:
        """Setup logging configuration."""
        try:
            logging_config = self.get_logging_config()
            logging.config.dictConfig(logging_config)
            
            # Test logging
            logger = logging.getLogger(__name__)
            logger.info("Logging system initialized successfully")
            logger.info(f"Log files location: {self.logs_dir.absolute()}")
            
        except Exception as e:
            # Emergency fallback
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('logs/emergency.log'),
                    logging.StreamHandler()
                ]
            )
            logging.getLogger("emergency").error(f"Failed to setup logging: {e}")

# Global logger setup instance
_logger_setup = LoggerSetup()

def setup_logging() -> None:
    """Public interface to setup logging."""
    _logger_setup.setup_logging()

def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance with the given name."""
    return logging.getLogger(name)

# Initialize logging when module is imported
setup_logging()
