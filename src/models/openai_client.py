"""OpenAI API client implementation."""
import os
from typing import Optional
from openai import OpenAI
from dotenv import load_dotenv
from .base import BaseModel

load_dotenv()


class OpenAIModel(BaseModel):
    """OpenAI GPT model client."""

    # Pricing per 1M tokens (as of Jan 2025)
    PRICING = {
        "gpt-4o": {"input": 2.50, "output": 10.00},
        "gpt-4o-mini": {"input": 0.15, "output": 0.60},
        "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    }

    def __init__(self, model_name: str = "gpt-4o"):
        super().__init__(model_name)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        self.client = OpenAI(api_key=api_key)

    def generate(
            self,
            prompt: str,
            system_prompt: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: int = 2000
    ) -> str:
        """Generate text using OpenAI API."""
        messages = []

        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})

        messages.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            # Track usage
            self.total_calls += 1
            usage = response.usage
            cost = self.estimate_cost(usage.prompt_tokens, usage.completion_tokens)
            self.total_cost += cost

            return response.choices[0].message.content

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def estimate_cost(self, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost based on token usage."""
        pricing = self.PRICING.get(self.model_name, self.PRICING["gpt-4o"])
        input_cost = (input_tokens / 1_000_000) * pricing["input"]
        output_cost = (output_tokens / 1_000_000) * pricing["output"]
        return input_cost + output_cost