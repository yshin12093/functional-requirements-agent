"""
Anthropic LLM provider implementation.
"""

from typing import List, Dict, Any, Optional
from llm_interface import LLMInterface


class AnthropicProvider(LLMInterface):
    """Implementation of LLMInterface for Anthropic (Claude)"""
    
    def __init__(self, model: str = "claude-3-sonnet-20240229", api_key: Optional[str] = None, **kwargs):
        """
        Initialize the Anthropic provider.
        
        Args:
            model: Name of the model to use (default: claude-3-sonnet-20240229)
            api_key: Anthropic API key (if None, will use ANTHROPIC_API_KEY env var)
            **kwargs: Additional arguments to pass to Anthropic
        """
        self.model = model
        self.api_key = api_key
        self.kwargs = kwargs
        
        # Import here to avoid requiring anthropic package if not used
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
        except ImportError:
            self.client = None
            print("Anthropic package not installed. Please install it with: pip install anthropic")
    
    def chat(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a chat request to Anthropic.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            system_prompt: Optional system prompt to override default
            
        Returns:
            Dictionary containing the response and metadata
        """
        if self.client is None:
            raise ImportError("Anthropic package not installed. Please install it with: pip install anthropic")
        
        # Convert messages to Anthropic format
        anthropic_messages = []
        for msg in messages:
            role = msg["role"]
            # Anthropic uses "user" and "assistant" roles
            if role == "system":
                # Skip system messages as they'll be handled separately
                continue
            elif role == "user":
                anthropic_messages.append({"role": "user", "content": msg["content"]})
            elif role == "assistant":
                anthropic_messages.append({"role": "assistant", "content": msg["content"]})
        
        # Send request to Anthropic
        response = self.client.messages.create(
            model=self.model,
            messages=anthropic_messages,
            system=system_prompt,  # Anthropic handles system prompt differently
            **self.kwargs
        )
        
        # Format response to match the expected structure
        return {
            "message": {
                "role": "assistant",
                "content": response.content[0].text
            },
            "model": self.model,
            "provider": "anthropic",
            "id": response.id
        }
    
    def get_name(self) -> str:
        """
        Get the name of the LLM provider.
        
        Returns:
            Name of the LLM provider
        """
        return "Anthropic"
    
    def get_model_name(self) -> str:
        """
        Get the name of the specific model being used.
        
        Returns:
            Name of the model
        """
        return self.model
