Fractal AI

Recursive multi-agent framework with unbounded breadth and bounded depth. Agents dynamically spawn specialized sub-agents to decompose complex tasks, while a hard recursion cap prevents exponential compute blowup.

Motivation

Current multi-agent systems fall into two failure modes:

Fixed teams - cannot adapt when task structure is unknown at design time.
Unbounded spawning - cost explodes exponentially with task complexity.

Fractal AI resolves this by decoupling the two axes: as many specialists as needed at each level, but no more than 3–4 levels deep. This makes recursive decomposition tractable without sacrificing adaptability.

Features
Model-agnostic core (OpenAI GPT-4o, Anthropic Claude Sonnet)
Integrated per-call cost tracking
Pluggable resource control strategies
Extensible Task / Result / Agent base classes
Experiment harness for systematic evaluation
Architecture
                    Root Agent (depth 0)
                   /        |         \
           Sub-Agent    Sub-Agent    Sub-Agent    (depth 1)
            /    \         |           /  \
          ...    ...      ...        ...  ...    (depth 2)
                                                 (depth ≤ 3–4, hard cap)

Core abstractions:

Task - unit of work; carries context, budget, depth counter.
Agent - decides whether to solve directly or decompose into sub-tasks.
Result - structured output; propagated up the tree and aggregated.
Resource Control Strategies

Five strategies are implemented and evaluated:

Fixed depth budget - hard cap on recursion levels.
Token/cost budget - top-down budget allocation; children inherit fractions of parent's remaining budget.
Confidence-gated recursion - agents only spawn sub-agents when self-assessed confidence falls below threshold.
Complexity-based allocation - upfront classifier estimates task complexity, allocates depth/breadth accordingly.
Adaptive/learned controller - meta-policy decides spawn/recurse/terminate per call.

Confirm strategy names against your design docs before publishing.

Installation
bash
git clone https://github.com/<USER>/<REPO>.git
cd <REPO>
python -m venv .venv
.venv\Scripts\activate      # Windows
pip install -r requirements.txt

Environment variables:

OPENAI_API_KEY=...
ANTHROPIC_API_KEY=...
Quick Start
python
from fractal_ai import Agent, Task

task = Task(description="Analyze the tradeoffs between X and Y")
agent = Agent(model="claude-sonnet", strategy="confidence_gated", max_depth=3)
result = agent.run(task)

print(result.output)
print(result.cost_summary())
Evaluation

Benchmark suite covers ~20 tasks across varying complexity, run under all five strategies (~100 scenarios total). Metrics:

Total cost (tokens, USD)
Quality (task-specific rubric + LLM-as-judge)
Depth / breadth statistics
Failure modes

See experiments/ for scripts and results/ for logs.

Research

This repository accompanies an academic evaluation of cost-quality tradeoffs in recursive multi-agent systems. Target venues: arXiv, AAMAS, ICML, NeurIPS.

Citation:

@misc{fractal_ai,
  title  = {Fractal AI: Bounded-Depth Recursive Multi-Agent Systems},
  author = {<AUTHOR>},
  year   = {2026},
  note   = {In preparation}
}
Roadmap
 Core framework, model-agnostic execution
 Cost tracking
 Task / Result / Agent base classes finalized
 Five resource control strategies implemented
 Full experimental sweep (100 scenarios)
 arXiv preprint
 Conference submission
