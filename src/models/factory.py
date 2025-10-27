"""Factory for creating model instances."""
from typing import Dict, Any
from .base import BaseModel
from .openai_client import OpenAIModel
from .anthropic_client import AnthropicModel


class ModelFactory:
    """Factory for creating LLM model instances."""

    @staticmethod
    def create(provider: str, model_name: str) -> BaseModel:
        """Create a model instance.

        Args:
            provider: Provider name ('openai' or 'anthropic')
            model_name: Specific model name

        Returns:
            Model instance
        """
        provider = provider.lower()

        if provider == "openai":
            return OpenAIModel(model_name)
        elif provider == "anthropic":
            return AnthropicModel(model_name)
        else:
            raise ValueError(f"Unknown provider: {provider}")

    @staticmethod
    def create_from_config(config: Dict[str, Any]) -> BaseModel:
        """Create model from configuration dict."""
        return ModelFactory.create(
            provider=config["provider"],
            model_name=config["model"]
        )