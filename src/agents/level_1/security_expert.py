"""Security Expert specialist agent."""
from ...core.agent import Agent
from ...core.task import Task


class SecurityExpert(Agent):
    """Specialist agent for security review tasks."""

    def __init__(
        self,
        name: str = "security_expert",
        model_provider: str = "openai",
        model_name: str = "gpt-4o"
    ):
        super().__init__(
            name=name,
            role="Security Expert",
            model_provider=model_provider,
            model_name=model_name
        )

    def _execute_directly(self, task: Task) -> str:
        """Execute security review task."""
        prompt = self._create_prompt(task)
        system_prompt = self._get_system_prompt()

        response = self.model.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.5,
            max_tokens=1500
        )

        return response

    def _get_system_prompt(self) -> str:
        """System prompt for security expert."""
        return """You are an expert Security Auditor specializing in web application security.

When given code or a task description:
- Identify potential vulnerabilities
- Reference specific attack vectors when relevant, such as SQL injection, XSS, or CSRF
- Suggest concrete mitigations
- Be concise and specific, avoid generic advice

Output a short list of findings, not a full essay."""

    def _create_prompt(self, task: Task) -> str:
        """Create security specific prompt."""
        prompt = f"""Review the following for security issues.

Task or code context: {task.description}
"""
        if task.context:
            prompt += f"\nAdditional Context: {task.context}"

        prompt += "\n\nProvide your security review:"

        return prompt