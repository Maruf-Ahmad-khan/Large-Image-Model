# ================================
# src/llm/base.py
# ================================
"""Base LLM client abstract class."""

from abc import ABC, abstractmethod
from typing import Any, Optional
from PIL import Image

class BaseLLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def generate_content(self, prompt: str, image: Optional[Image.Image] = None) -> str:
        """Generate content based on prompt and optional image."""
        pass
    
    @abstractmethod
    def is_healthy(self) -> bool:
        """Check if the client is healthy and ready to serve requests."""
        pass