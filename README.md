# Gemini Vision Assistant

A production-ready AI-powered image analysis application using Google's Gemini model.

## Features

- 🖼️ Image upload and validation
- 🤖 AI-powered image analysis
- 💭 Multiple analysis types (general, technical, creative)
- 🔧 Production-ready architecture
- 📝 Comprehensive logging
- ⚡ Error handling and validation

## Project Structure

```
gemini_vision_project/
├── config/
│   ├── __init__.py
│   ├── model_config.yaml
│   ├── prompt_templates.yaml
│   └── logging_config.yaml
├── src/
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── gemini_client.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── config_loader.py
│   │   ├── exceptions.py
│   │   ├── validators.py
│   │   └── logger.py
│   └── ui/
│       ├── __init__.py
│       ├── components.py
│       └── app.py
├── logs/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

## Setup

1. **Clone/Create the project structure**
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your Google API key: `GOOGLE_API_KEY=your_api_key_here`
4. **Run the application:**
   ```bash
   streamlit run main.py
   ```

## Configuration

- **Model settings:** `config/model_config.yaml`
- **Prompt templates:** `config/prompt_templates.yaml`
- **Logging config:** `config/logging_config.yaml`

## Usage

1. Upload an image (JPG, PNG, WEBP)
2. Select analysis type or enter custom prompt
3. Click "Analyze Image"
4. View AI-generated insights

## Production Features

- Modular architecture with separation of concerns
- Comprehensive error handling and logging
- Input validation and sanitization
- Configuration management
- Type hints and documentation
- Scalable component structure