"""
Deepseek LLM provider implementation.
"""

from typing import List, Dict, Any, Optional
from llm_interface import LLMInterface


class DeepseekProvider(LLMInterface):
    """Implementation of LLMInterface for Deepseek"""
    
    def __init__(self, model: str = "deepseek-coder", api_key: Optional[str] = None, **kwargs):
        """
        Initialize the Deepseek provider.
        
        Args:
            model: Name of the model to use (default: deepseek-coder)
            api_key: Deepseek API key (if None, will use DEEPSEEK_API_KEY env var)
            **kwargs: Additional arguments to pass to Deepseek
        """
        self.model = model
        self.api_key = api_key
        self.kwargs = kwargs
        
        # Import here to avoid requiring deepseek package if not used
        try:
            import deepseek
            self.client = deepseek.DeepseekAI(api_key=api_key)
        except ImportError:
            self.client = None
            print("Deepseek package not installed. Please install it with: pip install deepseek-ai")
    
    def chat(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a chat request to Deepseek.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            system_prompt: Optional system prompt to override default
            
        Returns:
            Dictionary containing the response and metadata
        """
        if self.client is None:
            raise ImportError("Deepseek package not installed. Please install it with: pip install deepseek-ai")
        
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
        
        # Send request to Deepseek
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            **self.kwargs
        )
        
        # Format response to match the expected structure
        return {
            "message": {
                "role": "assistant",
                "content": response.choices[0].message.content
            },
            "model": self.model,
            "provider": "deepseek",
            "id": response.id
        }
    
    def get_name(self) -> str:
        """
        Get the name of the LLM provider.
        
        Returns:
            Name of the LLM provider
        """
        return "Deepseek"
    
    def get_model_name(self) -> str:
        """
        Get the name of the specific model being used.
        
        Returns:
            Name of the model
        """
        return self.model
