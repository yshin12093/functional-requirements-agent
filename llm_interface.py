"""
LLM Interface for the Functional Requirements Agent.
This module defines the interface for LLM providers and common functionality.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, Union


class LLMInterface(ABC):
    """Abstract base class for LLM providers"""
    
    @abstractmethod
    def chat(self, messages: List[Dict[str, str]], system_prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Send a chat request to the LLM provider.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            system_prompt: Optional system prompt to override default
            
        Returns:
            Dictionary containing the response and any metadata
        """
        pass
    
    @abstractmethod
    def get_name(self) -> str:
        """
        Get the name of the LLM provider.
        
        Returns:
            Name of the LLM provider
        """
        pass
    
    @abstractmethod
    def get_model_name(self) -> str:
        """
        Get the name of the specific model being used.
        
        Returns:
            Name of the model
        """
        pass


class LLMFactory:
    """Factory class to create LLM provider instances"""
    
    @staticmethod
    def create(provider: str, **kwargs) -> LLMInterface:
        """
        Create an instance of the specified LLM provider.
        
        Args:
            provider: Name of the LLM provider (ollama, openai, anthropic, deepseek)
            **kwargs: Additional arguments to pass to the provider constructor
            
        Returns:
            An instance of the specified LLM provider
        
        Raises:
            ValueError: If the specified provider is not supported
        """
        if provider.lower() == "ollama":
            from llm_providers.ollama_provider import OllamaProvider
            return OllamaProvider(**kwargs)
        elif provider.lower() == "openai":
            from llm_providers.openai_provider import OpenAIProvider
            return OpenAIProvider(**kwargs)
        elif provider.lower() == "anthropic":
            from llm_providers.anthropic_provider import AnthropicProvider
            return AnthropicProvider(**kwargs)
        elif provider.lower() == "deepseek":
            from llm_providers.deepseek_provider import DeepseekProvider
            return DeepseekProvider(**kwargs)
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")


def get_default_system_prompt() -> str:
    """
    Get the default system prompt for functional requirements elicitation.
    
    Returns:
        Default system prompt as a string
    """
    return """You are a systems engineering assistant designed to help users define clear, complete, and validated functional requirements.

Your goals are:

Identify key stakeholders and their expectations.

Elicit and clarify system goals, constraints, and operational scenarios.

Translate stakeholder needs into unambiguous, testable functional requirements.

Ensure traceability between stakeholder expectations and technical requirements.

Validate requirements through iterative dialogue until completeness and consistency are achieved.

Begin by asking who the system is for and what it is intended to accomplish. Use structured, conversational questioning. At each step, explain why your questions matter. Adapt your language and depth of inquiry to the user's background and domain. Only conclude when all core functional requirements are well-formed and reviewed.

If you identify a clear functional requirement in the user's message, format it as 'The system shall [action]' and make it specific and testable."""
