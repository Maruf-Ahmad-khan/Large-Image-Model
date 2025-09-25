# ================================
# src/ui/app.py
# ================================
"""Main Streamlit application."""

import streamlit as st
import logging
from typing import Dict, Any
from PIL import Image

from ..llm.gemini_client import GeminiClient
from ..utils.validators import ImageValidator
from ..utils.exceptions import ValidationError, ModelError, APIError
from .components import UIComponents

logger = logging.getLogger(__name__)

class StreamlitApp:
    """Main Streamlit application class."""
    
    def __init__(self, config: Dict[str, Any], api_key: str):
        """Initialize the Streamlit app."""
        self.config = config
        self.api_key = api_key
        self.ui = UIComponents()
        
        # Initialize components
        self.gemini_client = GeminiClient(
            api_key=api_key,
            model_name=config['model']['name']
        )
        
        self.image_validator = ImageValidator(
            max_size_mb=config['ui']['max_file_size'],
            allowed_extensions=config['ui']['allowed_extensions']
        )
        
        logger.info("StreamlitApp initialized successfully")
    
    def run(self):
        """Run the Streamlit application."""
        try:
            # Render header
            self.ui.render_header(self.config)
            
            # Create two columns for better layout
            col1, col2 = st.columns([1, 1])
            
            with col1:
                # File upload section
                uploaded_file = self.ui.render_file_uploader(
                    self.config['ui']['max_file_size'],
                    self.config['ui']['allowed_extensions']
                )
                
                # Prompt selection section
                prompt = self.ui.render_prompt_selector(self.config['prompts'])
            
            with col2:
                # Image preview
                if uploaded_file:
                    try:
                        self.image_validator.validate_image(uploaded_file)
                        image = Image.open(uploaded_file)
                        self.ui.render_image_preview(image)
                        
                        # Store image in session state
                        st.session_state.current_image = image
                        
                    except ValidationError as e:
                        self.ui.render_error(str(e))
                        return
                    except Exception as e:
                        self.ui.render_error(f"Failed to process image: {e}")
                        return
            
            # Analysis button and results
            st.divider()
            
            if st.button("🚀 Analyze Image", type="primary", use_container_width=True):
                self._handle_analysis(prompt)
                
        except Exception as e:
            logger.error(f"Application error: {e}")
            self.ui.render_error(f"Application error: {e}")
    
    def _handle_analysis(self, prompt: str):
        """Handle image analysis request."""
        if 'current_image' not in st.session_state:
            self.ui.render_error("Please upload an image first")
            return
        
        if not prompt.strip():
            self.ui.render_error("Please provide a prompt")
            return
        
        try:
            with st.spinner("🔍 Analyzing image..."):
                # Generate response
                response = self.gemini_client.generate_content(
                    prompt=prompt,
                    image=st.session_state.current_image
                )
                
                # Display response
                self.ui.render_response(response)
                self.ui.render_success("Analysis completed successfully!")
                
        except ModelError as e:
            self.ui.render_error(f"Model error: {e}")
        except APIError as e:
            self.ui.render_error(f"API error: {e}")
        except Exception as e:
            logger.error(f"Unexpected error during analysis: {e}")
            self.ui.render_error("An unexpected error occurred. Please try again.")