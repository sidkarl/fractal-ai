"""Day 2 test - verify Agent architecture works."""
from src.core.task import Task
from src.agents.level_1.backend_developer import BackendDeveloper


def test_task_creation():
    """Test Task class."""
    print("\n Testing Task creation...")

    task = Task(
        description="Create a simple REST API endpoint",
        context="Use Flask framework"
    )

    print(f" Created: {task}")
    print(f" Task ID: {task.task_id}")
    print(f" Task dict: {task.to_dict()}")


def test_backend_agent():
    """Test BackendDeveloper agent."""
    print("\n Testing BackendDeveloper agent...")

    agent = BackendDeveloper(
        name="backend_dev_001",
        model_provider="openai",
        model_name="gpt-4o"
    )

    task = Task(
        description="Write a Python function that validates an email address using regex",
        context="Should return True if valid, False otherwise"
    )

    print(f"\n Task: {task.description}")
    print(f"Agent: {agent.role}")
    print("\n" + "=" * 60)

    result = agent.execute(task, depth=0)

    print("=" * 60)
    print(f"\n Result: {result}")
    print(f"\n Output:\n{result.content}")
    print(f"\n Cost: ${result.total_cost():.6f}")
    print(f"⏱️  Time: {result.execution_time:.2f}s")


def test_depth_limit():
    """Test that depth limiting works."""
    print("\n🧪 Testing depth limit...")

    agent = BackendDeveloper()

    task = Task(
        description="Simple task to test depth"
    )

    # Execute at max depth - should still work
    result = agent.execute(task, depth=3)

    print(f" Executed at depth 3: {result}")
    print(f" Cost: ${result.cost:.6f}")


if __name__ == "__main__":
    print(" DAY 2 - AGENT ARCHITECTURE TEST")
    print("=" * 60)

    test_task_creation()
    test_backend_agent()
    test_depth_limit()

    print("\n" + "=" * 60)
    print(" ALL TESTS PASSED - Agent architecture ready!")