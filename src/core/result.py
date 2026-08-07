"""Result representation for agent outputs."""
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Result:
    """Represents the output from an agent.

    Attributes:
        content: The actual output (code, text, analysis, etc.)
        agent_name: Which agent produced this
        task_id: Which task this is for
        result_id: Unique identifier
        success: Whether execution was successful
        cost: Cost in USD for this execution
        metadata: Additional result data
        sub_results: Results from sub-agents (for recursive calls)
    """
    content: str
    agent_name: str
    task_id: str
    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    success: bool = True
    cost: float = 0.0
    execution_time: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    sub_results: List['Result'] = field(default_factory=list)

    def __str__(self) -> str:
        status = "pass" if self.success else "X"
        return f"{status} Result from {self.agent_name} (${self.cost:.4f})"

    def total_cost(self) -> float:
        """Calculate total cost including sub-results."""
        total = self.cost
        for sub_result in self.sub_results:
            total += sub_result.total_cost()
        return total

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "result_id": self.result_id,
            "agent_name": self.agent_name,
            "task_id": self.task_id,
            "success": self.success,
            "cost": self.cost,
            "execution_time": self.execution_time,
            "timestamp": self.timestamp.isoformat(),
            "content_length": len(self.content),
            "sub_results_count": len(self.sub_results),
            "total_cost": self.total_cost()
        }