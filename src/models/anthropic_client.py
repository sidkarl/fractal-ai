"""Anthropic Claude API client implementation."""
import os
from typing import Optional
from anthropic import Anthropic
from dotenv import load_dotenv
from .base import BaseModel

load_dotenv()


class AnthropicModel(BaseModel):
    """Anthropic Claude model client."""

    # Pricing per 1M tokens (as of Jan 2025)
    PRICING = {
        "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
        "claude-sonnet-4": {"input": 3.00, "output": 15.00},
        "claude-opus-4": {"input": 15.00, "output": 75.00},
        "claude-haiku-4": {"input": 0.80, "output": 4.00},
    }

    def __init__(self, model_name: str = "claude-sonnet-4-20250514"):
        super().__init__(model_name)
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        self.client = Anthropic(api_key=api_key)

    def generate(
            self,
            prompt: str,
            system_prompt: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: int = 2000
    ) -> str:
        """Generate text using Anthropic API."""
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt if system_prompt else "",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )

            # Track usage
            self.total_calls += 1
            usage = response.usage
            cost = self.estimate_cost(usage.input_tokens, usage.output_tokens)
            self.total_cost += cost

            return response.content[0].text

        except Exception as e:
            raise Exception(f"Anthropic API error: {str(e)}")

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost based on token usage."""
        pricing = self.PRICING.get(self.model_name, self.PRICING["claude-sonnet-4-20250514"])
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost