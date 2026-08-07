"""Task representation for agent execution."""
from typing import Optional, Dict, Any
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Task:
    """Represents a task for an agent to execute.

    Attributes:
        description: What needs to be done
        context: Additional information/requirements
        task_id: Unique identifier
        created_at: When task was created
        metadata: Additional task-specific data
    """
    description: str
    context: Optional[str] = None
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        return f"Task({self.task_id[:8]}...): {self.description[:50]}"

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "task_id": self.task_id,
            "description": self.description,
            "context": self.context,
            "created_at": self.created_at.isoformat(),
            "metadata": self.metadata
        }