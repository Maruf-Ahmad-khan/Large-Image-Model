# ================================
# src/ui/components.py
# ================================
"""Reusable UI components."""

import streamlit as st
from typing import Dict, Any, Optional
from PIL import Image

class UIComponents:
    """Reusable UI components for Streamlit."""
    
    @staticmethod
    def render_header(config: Dict[str, Any]):
        """Render application header."""
        st.set_page_config(
            page_title=config['app']['title'],
            page_icon=config['app']['page_icon'],
            layout=config['app']['layout']
        )
        
        st.title(config['app']['title'])
        st.markdown(f"*{config['app']['description']}*")
        st.divider()
    
    @staticmethod
    def render_file_uploader(max_size_mb: int, allowed_extensions: list) -> Optional[Any]:
        """Render file uploader with validation info."""
        st.subheader("📁 Upload Image")
        
        with st.expander("ℹ️ Upload Guidelines", expanded=False):
            st.markdown(f"""
            - **Max file size:** {max_size_mb}MB
            - **Supported formats:** {', '.join(allowed_extensions).upper()}
            - **Recommended:** Clear, high-quality images for best results
            """)
        
        return st.file_uploader(
            "Choose an image file",
            type=allowed_extensions,
            help=f"Upload an image file (max {max_size_mb}MB)"
        )
    
    @staticmethod
    def render_prompt_selector(prompts: Dict[str, str]) -> str:
        """Render prompt selection interface."""
        st.subheader("💭 Analysis Type")
        
        prompt_options = {
            "Custom": "custom",
            "General Analysis": "analyze",
            "Detailed Description": "describe",
            "Technical Analysis": "technical",
            "Creative Description": "creative"
        }
        
        selected_type = st.selectbox(
            "Choose analysis type:",
            options=list(prompt_options.keys()),
            help="Select the type of analysis you want"
        )
        
        if selected_type == "Custom":
            return st.text_area(
                "Enter your custom prompt:",
                value=prompts.get('default', ''),
                height=100,
                help="Describe what you want to know about the image"
            )
        else:
            prompt_key = prompt_options[selected_type]
            return prompts.get(prompt_key, prompts['default'])
    
    @staticmethod
    def render_image_preview(image: Image.Image, title: str = "Uploaded Image"):
        """Render image preview."""
        st.subheader(f"🖼️ {title}")
        st.image(image, use_column_width=True, caption=f"{title} - {image.size[0]}x{image.size[1]} pixels")
    
    @staticmethod
    def render_response(response_text: str):
        """Render AI response."""
        st.subheader("🤖 AI Analysis")
        st.markdown(response_text)
    
    @staticmethod
    def render_error(error_message: str):
        """Render error message."""
        st.error(f"❌ {error_message}")
    
    @staticmethod
    def render_success(message: str):
        """Render success message."""
        st.success(f"✅ {message}")