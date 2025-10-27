"""Base model interface for LLM providers."""
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any


class BaseModel(ABC):
    """Abstract base class for all LLM providers."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.total_cost = 0.0
        self.total_calls = 0

    @abstractmethod
    def generate(
            self,
            prompt: str,
            system_prompt: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: int = 2000
    ) -> str:
        """Generate text from the model."""
        pass

    @abstractmethod
    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for a generation."""
        pass

    def get_stats(self) -> Dict[str, Any]:
        """Get usage statistics."""
        return {
            "model": self.model_name,
            "total_calls": self.total_calls,
            "total_cost": self.total_cost
        }