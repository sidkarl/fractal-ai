import os

# Directories to create
dirs = [
    "src/core",
    "src/agents/level_1",
    "src/agents/level_2",
    "src/agents/level_3",
    "src/models",
    "src/strategies",
    "src/evaluation",
    "config",
    "experiments/results",
    "tests",
    "docs",
    "paper"
]

# Files to create
files = [
    "src/__init__.py",
    "src/core/__init__.py",
    "src/agents/__init__.py",
    "src/agents/level_1/__init__.py",
    "src/agents/level_2/__init__.py",
    "src/agents/level_3/__init__.py",
    "src/models/__init__.py",
    "src/strategies/__init__.py",
    "src/evaluation/__init__.py",
    "src/core/agent.py",
    "src/core/task.py",
    "src/core/result.py",
    "src/core/coordinator.py",
    "src/models/base.py",
    "src/models/openai_client.py",
    "src/models/anthropic_client.py",
    "src/models/factory.py",
    "config/models.yaml",
    ".env",
    "requirements.txt",
    ".gitignore",
    "README.md"
]

# Create directories
for dir_path in dirs:
    os.makedirs(dir_path, exist_ok=True)
    print(f"✅ Created directory: {dir_path}")

# Create empty files
for file_path in files:
    with open(file_path, 'w') as f:
        pass
    print(f"✅ Created file: {file_path}")

print("\n🎉 Project structure created successfully!")