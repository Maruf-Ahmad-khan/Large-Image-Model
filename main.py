
# ================================
# main.py (Root level)
# ================================
"""Main application entry point."""

import os
import sys
from pathlib import Path
import streamlit as st
from dotenv import load_dotenv

# Add src to Python path
sys.path.append(str(Path(__file__).parent / "src"))

from src.utils.config_loader import ConfigLoader
from src.utils.logger import setup_logging
from src.utils.exceptions import ConfigurationError
from src.ui.app import StreamlitApp

def main():
    """Main application function."""
    try:
        # Load .env file first
        env_loaded = load_dotenv()
        
        # Setup logging
        setup_logging()
        
        # Load configuration
        model_config = ConfigLoader.load_config("config/model_config.yaml")
        prompt_config = ConfigLoader.load_config("config/prompt_templates.yaml")
        env_vars = ConfigLoader.load_env_variables()
        
        # Combine configurations
        config = {**model_config, **prompt_config}
        
        # Debug information
        if not env_loaded:
            st.warning("⚠️ .env file not found or not loaded properly")
        
        # Validate API key
        api_key = env_vars.get('google_api_key')
        if not api_key:
            st.error("❌ GOOGLE_API_KEY not found in environment variables")
            
            # Provide debugging information
            st.info("🔍 **Debugging Information:**")
            st.markdown(f"""
            - **.env file loaded:** {'✅ Yes' if env_loaded else '❌ No'}
            - **Current working directory:** `{os.getcwd()}`
            - **.env file exists:** {'✅ Yes' if Path('.env').exists() else '❌ No'}
            - **GOOGLE_API_KEY in environment:** {'✅ Yes' if 'GOOGLE_API_KEY' in os.environ else '❌ No'}
            """)
            
            st.markdown("""
            ### 📝 **Setup Instructions:**
            
            1. **Create a `.env` file** in the project root directory
            2. **Add your Google API key:**
               ```
               GOOGLE_API_KEY=your_actual_api_key_here
               ```
            3. **Make sure the .env file is in the same directory as main.py**
            4. **Restart the application**
            
            ### 🔑 **Get your API key from:**
            - [Google AI Studio](https://aistudio.google.com/app/apikey)
            """)
            return
        
        # Initialize and run app
        app = StreamlitApp(config, api_key)
        app.run()
        
    except FileNotFoundError as e:
        st.error(f"❌ Configuration file not found: {e}")
        st.info("Make sure all configuration files are in the `config/` directory")
    except ConfigurationError as e:
        st.error(f"❌ Configuration error: {e}")
    except Exception as e:
        st.error(f"❌ Application startup failed: {e}")
        st.exception(e)  # Show full traceback in debug mode

if __name__ == "__main__":
    main()