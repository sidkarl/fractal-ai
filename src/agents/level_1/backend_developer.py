"""Backend Developer specialist agent."""
from ...core.agent import Agent
from ...core.task import Task


class BackendDeveloper(Agent):
    """Specialist agent for backend development tasks."""

    def __init__(
            self,
            name: str = "backend_dev",
            model_provider: str = "openai",
            model_name: str = "gpt-4o"
    ):
        super().__init__(
            name=name,
            role="Backend Developer",
            model_provider=model_provider,
            model_name=model_name
        )

    def _execute_directly(self, task: Task) -> str:
        """Execute backend development task."""
        prompt = self._create_prompt(task)
        system_prompt = self._get_system_prompt()

        response = self.model.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=2000
        )

        return response

    def _get_system_prompt(self) -> str:
        """System prompt for backend developer."""
        return """You are an expert Backend Developer specializing in Python, Node.js, and API development.

When given a task:
- Write clean, production-ready code
- Include error handling
- Add comments for complex logic
- Follow best practices
- Be concise but complete

Output only the code, no explanations unless asked."""

    def _create_prompt(self, task: Task) -> str:
        """Create backend-specific prompt."""
        prompt = f"""Task: {task.description}
"""
        if task.context:
            prompt += f"\nAdditional Context: {task.context}"

        prompt += "\n\nProvide the implementation:"

        return prompt