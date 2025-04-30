"""
Ollama LLM provider implementation.
"""

import ollama
from typing import List, Dict, Any, Optional
from llm_interface import LLMInterface


class OllamaProvider(LLMInterface):
    """Implementation of LLMInterface for Ollama"""
    
    def __init__(self, model: str = "llama3", api_key: Optional[str] = None, **kwargs):
        """
        Initialize the Ollama provider.
        
        Args:
            model: Name of the model to use (default: llama3)
            api_key: Not used for Ollama but included for interface consistency
            **kwargs: Additional arguments to pass to Ollama
        """
        self.model = model
        # Filter out api_key from kwargs since Ollama doesn't use it
        self.kwargs = {k: v for k, v in kwargs.items() if k != 'api_key'}
    
    def chat(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a chat request to Ollama.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            system_prompt: Optional system prompt to override default
            
        Returns:
            Dictionary containing the response and metadata
        """
        # If system prompt is provided, add or replace the system message
        if system_prompt:
            # Check if there's already a system message
            has_system = False
            for i, msg in enumerate(messages):
                if msg.get("role") == "system":
                    messages[i]["content"] = system_prompt
                    has_system = True
                    break
            
            # If no system message, add it at the beginning
            if not has_system:
                messages.insert(0, {"role": "system", "content": system_prompt})
        
        # Send request to Ollama
        # Only pass supported parameters to avoid errors
        ollama_params = {}
        if self.kwargs:
            # Filter for only supported parameters
            supported_params = ['format', 'options', 'keep_alive', 'stream']
            for param in supported_params:
                if param in self.kwargs:
                    ollama_params[param] = self.kwargs[param]
        
        response = ollama.chat(model=self.model, messages=messages, **ollama_params)
        
        return response
    
    def get_name(self) -> str:
        """
        Get the name of the LLM provider.
        
        Returns:
            Name of the LLM provider
        """
        return "Ollama"
    
    def get_model_name(self) -> str:
        """
        Get the name of the specific model being used.
        
        Returns:
            Name of the model
        """
        return self.model
