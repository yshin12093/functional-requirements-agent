"""
LLM handler for the Functional Requirements Agent.
"""
import config
from llm_interface import LLMFactory

class LLMHandler:
    """Handler for LLM-related functionality"""
    
    def __init__(self):
        """Initialize the LLM handler"""
        self.llm_settings = {
            "provider": config.DEFAULT_LLM_PROVIDER,
            "model": config.DEFAULT_LLM_MODEL,
            "api_key": None
        }
        self.llm = self.create_llm_instance()
    
    def create_llm_instance(self):
        """
        Create an instance of the LLM provider based on current settings
        
        Returns:
            LLM provider instance
        """
        try:
            provider = self.llm_settings["provider"]
            model = self.llm_settings["model"]
            api_key = self.llm_settings["api_key"]
            
            # Create the LLM provider instance
            llm = LLMFactory.create(
                provider=provider,
                model=model,
                api_key=api_key
            )
            
            return llm
        except Exception as e:
            # Fall back to Ollama if there's an error
            print(f"Error creating LLM instance: {e}. Falling back to Ollama.")
            self.llm_settings = {
                "provider": "ollama",
                "model": "llama3",
                "api_key": None
            }
            return LLMFactory.create(provider="ollama", model="llama3")
    
    def update_settings(self, settings):
        """
        Update the LLM settings and recreate the instance
        
        Args:
            settings: Dictionary with provider, model, and api_key
        """
        self.llm_settings = settings
        self.llm = self.create_llm_instance()
    
    def get_llm(self):
        """Get the current LLM instance"""
        return self.llm
    
    def get_settings(self):
        """Get the current LLM settings"""
        return self.llm_settings
    
    def get_status_text(self):
        """Get a status text describing the current LLM configuration"""
        return f"LLM: {self.llm.get_name()} - {self.llm.get_model_name()}"
