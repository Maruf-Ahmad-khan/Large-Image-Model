# ================================
# src/llm/gemini_client.py
# ================================
"""Gemini LLM client implementation."""

import logging
from typing import Optional
from PIL import Image
import google.generativeai as genai

from .base import BaseLLMClient
from ..utils.exceptions import ModelError, APIError

logger = logging.getLogger(__name__)

class GeminiClient(BaseLLMClient):
    """Google Gemini AI client implementation."""
    
    def __init__(self, api_key: str, model_name: str = "gemini-1.5-flash", **kwargs):
        """Initialize Gemini client."""
        self.api_key = api_key
        self.model_name = model_name
        self.config = kwargs
        
        try:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel(model_name)
            logger.info(f"Gemini client initialized with model: {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Gemini client: {e}")
            raise APIError(f"Gemini initialization failed: {e}")
    
    def generate_content(self, prompt: str, image: Optional[Image.Image] = None) -> str:
        """Generate content using Gemini model."""
        try:
            if image and prompt:
                response = self.model.generate_content([prompt, image])
            elif image:
                response = self.model.generate_content(image)
            else:
                response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                raise ModelError("Empty response from Gemini model")
            
            logger.info("Successfully generated content from Gemini")
            return response.text
            
        except Exception as e:
            logger.error(f"Content generation failed: {e}")
            raise ModelError(f"Failed to generate content: {e}")
    
    def is_healthy(self) -> bool:
        """Check if Gemini client is healthy."""
        try:
            # Simple health check with minimal content generation
            test_response = self.model.generate_content("Hello")
            return bool(test_response and test_response.text)
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False
