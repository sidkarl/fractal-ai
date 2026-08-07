"""Day 3 test - verify delegation and parallel sub-agent execution."""
from src.core.task import Task
from src.agents.level_1.project_coordinator import ProjectCoordinator


def test_delegation():
    """Test that coordinator delegates to two sub-agents in parallel."""
    print("\nTesting ProjectCoordinator delegation...")

    coordinator = ProjectCoordinator()

    task = Task(
        description="Design a login endpoint that accepts a username and password and returns a session token",
        context="This will be used in a public facing web application"
    )

    print(f"\nTask: {task.description}")
    print(f"Coordinator: {coordinator.role}")
    print("=" * 60)

    result = coordinator.execute(task, depth=0)

    print("=" * 60)
    print(f"\nTop level result: {result}")
    print(f"Number of sub-results: {len(result.sub_results)}")
    print(f"Total cost across all agents: ${result.total_cost():.6f}")
    print(f"\nSynthesized output:\n{result.content}")


if __name__ == "__main__":
    print("DAY 3 - DELEGATION TEST")
    print("=" * 60)

    test_delegation()

    print("\n" + "=" * 60)
    print("TEST COMPLETE")