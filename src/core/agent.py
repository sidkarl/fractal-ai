"""Base Agent class for all agents in the system."""
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
import time
import concurrent.futures
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
            name: Agent's name, for example backend_dev_001
            role: Agent's role, for example Backend Developer
            model_provider: LLM provider, openai or anthropic
            model_name: Specific model to use
        """
        self.name = name
        self.role = role
        self.model: BaseModel = ModelFactory.create(model_provider, model_name)

    def execute(self, task: Task, depth: int = 0) -> Result:
        """Execute a task at given recursion depth.

        Args:
            task: Task to execute
            depth: Current recursion depth, 0 means top level

        Returns:
            Result object with output
        """
        start_time = time.time()

        print(f"{'  ' * depth}{self.role} starting: {task.description[:50]}...")

        if depth >= MAX_RECURSION_DEPTH:
            print(f"{'  ' * depth}Max depth reached, executing directly")
            content = self._execute_directly(task)
            sub_results = []
        else:
            if self._should_delegate(task, depth):
                print(f"{'  ' * depth}Delegating to sub-agents...")
                content, sub_results = self._execute_with_delegation(task, depth)
            else:
                print(f"{'  ' * depth}Executing directly")
                content = self._execute_directly(task)
                sub_results = []

        execution_time = time.time() - start_time

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

        print(f"{'  ' * depth}{self.role} complete (${total_cost:.4f}, {execution_time:.1f}s)")

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
        return len(task.description) > 100 and depth < MAX_RECURSION_DEPTH

    def get_sub_agents(self, task: Task, depth: int) -> List['Agent']:
        """Define which sub-agents to spawn for this task.

        Override this in subclasses to define delegation strategy.
        Default returns an empty list, meaning no delegation possible
        unless a subclass provides sub-agents.

        Args:
            task: Task being delegated
            depth: Current recursion depth

        Returns:
            List of Agent instances to run in parallel
        """
        return []

    def _execute_with_delegation(self, task: Task, depth: int) -> Tuple[str, List[Result]]:
        """Execute task by delegating to sub-agents, running them in parallel.

        Args:
            task: Task to delegate
            depth: Current recursion depth

        Returns:
            Tuple of synthesized_content and list_of_sub_results
        """
        sub_agents = self.get_sub_agents(task, depth)

        if not sub_agents:
            # No sub-agents defined, fall back to direct execution
            content = self._execute_directly(task)
            return content, []

        sub_results: List[Result] = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=len(sub_agents)) as executor:
            futures = {
                executor.submit(agent.execute, task, depth + 1): agent
                for agent in sub_agents
            }
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                sub_results.append(result)

        content = self._synthesize(task, sub_results)

        return content, sub_results

    def _synthesize(self, task: Task, sub_results: List[Result]) -> str:
        """Combine sub-agent outputs into a single coherent result.

        Default implementation concatenates outputs with labels.
        Override in subclasses for smarter synthesis, for example
        using the LLM itself to merge and reconcile outputs.

        Args:
            task: Original task
            sub_results: Results from all sub-agents

        Returns:
            Synthesized content string
        """
        sections = []
        for result in sub_results:
            role = result.metadata.get("role", result.agent_name)
            sections.append(f"--- {role} ---\n{result.content}\n")

        return "\n".join(sections)

    @abstractmethod
    def _execute_directly(self, task: Task) -> str:
        """Execute the task directly using the LLM.

        This is where the actual work happens.
        Must be implemented by all subclasses.

        Args:
            task: Task to execute

        Returns:
            The output content, code, text, or analysis
        """
        pass

    def _create_prompt(self, task: Task) -> str:
        """Create a prompt for the LLM based on the task.

        Override in subclasses for role specific prompting.

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

        Override in subclasses for role specific instructions.

        Returns:
            System prompt string
        """
        return f"You are a {self.role}. Be concise, accurate, and professional."