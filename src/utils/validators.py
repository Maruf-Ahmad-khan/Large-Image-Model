# ================================
# src/utils/validators.py
# ================================
"""Input validation utilities."""

import logging
from typing import Optional, List
from PIL import Image
import io

from .exceptions import ValidationError

logger = logging.getLogger(__name__)

class ImageValidator:
    """Image validation utilities."""
    
    def __init__(self, max_size_mb: int = 10, allowed_extensions: List[str] = None):
        self.max_size_mb = max_size_mb
        self.allowed_extensions = allowed_extensions or ['jpg', 'jpeg', 'png', 'webp']
    
    def validate_image(self, uploaded_file) -> bool:
        """Validate uploaded image file."""
        if not uploaded_file:
            return False
        
        # Check file size
        file_size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        if file_size_mb > self.max_size_mb:
            raise ValidationError(f"File size ({file_size_mb:.1f}MB) exceeds limit ({self.max_size_mb}MB)")
        
        # Check file extension
        file_extension = uploaded_file.name.split('.')[-1].lower()
        if file_extension not in self.allowed_extensions:
            raise ValidationError(f"Unsupported file type: {file_extension}")
        
        # Try to open as image
        try:
            image = Image.open(uploaded_file)
            image.verify()
            return True
        except Exception as e:
            raise ValidationError(f"Invalid image file: {e}")