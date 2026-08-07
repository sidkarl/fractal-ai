"""Project Coordinator agent that delegates to specialist agents."""
from typing import List
from ...core.agent import Agent
from ...core.task import Task
from .backend_developer import BackendDeveloper
from .security_expert import SecurityExpert


class ProjectCoordinator(Agent):
    """Coordinates work across multiple specialist agents."""

    def __init__(
        self,
        name: str = "project_coordinator",
        model_provider: str = "openai",
        model_name: str = "gpt-4o"
    ):
        super().__init__(
            name=name,
            role="Project Coordinator",
            model_provider=model_provider,
            model_name=model_name
        )

    def _should_delegate(self, task: Task, depth: int) -> bool:
        """Coordinator always delegates if depth allows it."""
        return depth < 3

    def get_sub_agents(self, task: Task, depth: int) -> List[Agent]:
        """Spawn a backend developer and a security expert for this task."""
        return [
            BackendDeveloper(name=f"backend_dev_d{depth}", model_provider="openai", model_name="gpt-4o"),
            SecurityExpert(name=f"security_expert_d{depth}", model_provider="openai", model_name="gpt-4o"),
        ]

    def _execute_directly(self, task: Task) -> str:
        """Fallback direct execution if delegation is skipped."""
        prompt = self._create_prompt(task)
        system_prompt = self._get_system_prompt()

        response = self.model.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1500
        )

        return response

    def _get_system_prompt(self) -> str:
        return "You are a Project Coordinator who manages engineering tasks."