"""
OpenAI LLM provider implementation.
"""

from typing import List, Dict, Any, Optional
from llm_interface import LLMInterface


class OpenAIProvider(LLMInterface):
    """Implementation of LLMInterface for OpenAI"""
    
    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None, **kwargs):
        """
        Initialize the OpenAI provider.
        
        Args:
            model: Name of the model to use (default: gpt-4o)
            api_key: OpenAI API key (if None, will use OPENAI_API_KEY env var)
            **kwargs: Additional arguments to pass to OpenAI
        """
        self.model = model
        self.api_key = api_key
        self.kwargs = kwargs
        
        # Import here to avoid requiring openai package if not used
        try:
            import openai
            self.client = openai.OpenAI(api_key=api_key)
        except ImportError:
            self.client = None
            print("OpenAI package not installed. Please install it with: pip install openai")
    
    def chat(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a chat request to OpenAI.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            system_prompt: Optional system prompt to override default
            
        Returns:
            Dictionary containing the response and metadata
        """
        if self.client is None:
            raise ImportError("OpenAI package not installed. Please install it with: pip install openai")
        
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
        
        # Send request to OpenAI
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
            "provider": "openai",
            "created_at": response.created,
            "id": response.id
        }
    
    def get_name(self) -> str:
        """
        Get the name of the LLM provider.
        
        Returns:
            Name of the LLM provider
        """
        return "OpenAI"
    
    def get_model_name(self) -> str:
        """
        Get the name of the specific model being used.
        
        Returns:
            Name of the model
        """
        return self.model
