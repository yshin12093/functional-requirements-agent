"""
Configuration settings for the Functional Requirements Agent.
"""

# Default LLM provider configuration
DEFAULT_LLM_PROVIDER = "ollama"  # Options: ollama, openai, anthropic, deepseek
DEFAULT_LLM_MODEL = "llama3"     # Default model for the selected provider

# Provider-specific default models
PROVIDER_DEFAULT_MODELS = {
    "ollama": "llama3",
    "openai": "gpt-4o",
    "anthropic": "claude-3-sonnet-20240229",
    "deepseek": "deepseek-coder"
}

# UI Configuration
UI_TITLE = "Functional Requirements Agent"
UI_WIDTH = 900
UI_HEIGHT = 700

# Application paths
REQUIREMENTS_DATA_DIR = "requirements_data"
EXPORTS_DIR = "exports"
