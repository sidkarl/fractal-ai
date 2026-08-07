"""Base Agent class for all agents in the system."""
from abc import ABC, abstractmethod
from typing import Optional, List
import time
from .task import Task
from .result import Result
from ..models.base import BaseModel
from ..models.factory import ModelFactory

# Global configuration
MAX_RECURSION_DEPTH = 3


class Agent(ABC):
    """Abstract base class for all agents.

    All agents in the system inherit from this class.
    Provides depth tracking, model access, and execution framework.
    """

    def __init__(
            self,
            name: str,
            role: str,
            model_provider: str = "openai",
            model_name: str = "gpt-4o"
    ):
        """Initialize agent.

        Args:
            name: Agent's name (e.g., "backend_dev_001")
            role: Agent's role (e.g., "Backend Developer")
            model_provider: LLM provider ("openai" or "anthropic")
            model_name: Specific model to use
        """
        self.name = name
        self.role = role
        self.model: BaseModel = ModelFactory.create(model_provider, model_name)

    def execute(self, task: Task, depth: int = 0) -> Result:
        """Execute a task at given recursion depth.

        Args:
            task: Task to execute
            depth: Current recursion depth (0 = top level)

        Returns:
            Result object with output
        """
        start_time = time.time()

        print(f"{'  ' * depth}🤖 {self.role} starting: {task.description[:50]}...")

        # Check if we've hit max depth
        if depth >= MAX_RECURSION_DEPTH:
            print(f"{'  ' * depth}⚠️  Max depth reached, executing directly")
            content = self._execute_directly(task)
            sub_results = []
        else:
            # Decide whether to delegate or do it ourselves
            if self._should_delegate(task, depth):
                print(f"{'  ' * depth}📋 Delegating to sub-agents...")
                content, sub_results = self._execute_with_delegation(task, depth)
            else:
                print(f"{'  ' * depth}✍️  Executing directly")
                content = self._execute_directly(task)
                sub_results = []

        execution_time = time.time() - start_time

        # Calculate cost (this agent + all sub-agents)
        my_cost = self.model.total_cost
        total_cost = my_cost + sum(r.total_cost() for r in sub_results)

        result = Result(
            content=content,
            agent_name=self.name,
            task_id=task.task_id,
            success=True,
            cost=my_cost,
            execution_time=execution_time,
            sub_results=sub_results,
            metadata={"depth": depth, "role": self.role}
        )

        print(f"{'  ' * depth} {self.role} complete (${total_cost:.4f}, {execution_time:.1f}s)")

        return result

    def _should_delegate(self, task: Task, depth: int) -> bool:
        """Decide if this task should be delegated to sub-agents.

        Override this in subclasses for custom logic.

        Args:
            task: The task to evaluate
            depth: Current recursion depth

        Returns:
            True if should delegate, False if should execute directly
        """
        # Default: simple heuristic based on task description length
        # Complex tasks (long descriptions) should be delegated
        # Override this in specialist agents for smarter decisions
        return len(task.description) > 100 and depth < MAX_RECURSION_DEPTH

    def _execute_with_delegation(self, task: Task, depth: int) -> tuple[str, List[Result]]:
        """Execute task by delegating to sub-agents.

        Override this in subclasses to define delegation strategy.

        Args:
            task: Task to delegate
            depth: Current recursion depth

        Returns:
            Tuple of (synthesized_content, list_of_sub_results)
        """
        # Default implementation: just execute directly
        # Subclasses should override this to spawn sub-agents
        content = self._execute_directly(task)
        return content, []

    @abstractmethod
    def _execute_directly(self, task: Task) -> str:
        """Execute the task directly using the LLM.

        This is where the actual work happens.
        Must be implemented by all subclasses.

        Args:
            task: Task to execute

        Returns:
            The output content (code, text, analysis, etc.)
        """
        pass

    def _create_prompt(self, task: Task) -> str:
        """Create a prompt for the LLM based on the task.

        Override in subclasses for role-specific prompting.

        Args:
            task: Task to create prompt for

        Returns:
            Formatted prompt string
        """
        prompt = f"""You are a {self.role}.

Task: {task.description}
"""
        if task.context:
            prompt += f"\nContext: {task.context}"

        prompt += "\n\nProvide your response:"

        return prompt

    def _get_system_prompt(self) -> str:
        """Get system prompt for this agent's role.

        Override in subclasses for role-specific instructions.

        Returns:
            System prompt string
        """
        return f"You are a {self.role}. Be concise, accurate, and professional."