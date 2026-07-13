# AI Agent Coordination & Decision Engine

## Project Overview
A multi-agent system for project management, where specialized AI agents analyze different aspects of a project and a central decision engine coordinates their findings into prioritized, explained recommendations.

## Milestone 1: Risk & Deadline Agent
Built using LangChain's `create_agent` with Google Gemini (`gemini-2.5-flash-lite`).

The agent analyzes tasks using two tools:
- `calculate_days_remaining` — checks time left until deadline
- `check_dependency_status` — checks if a task's dependencies are behind schedule

### How to run
pip install -r requirements.txt
python agents/risk_deadline.py

## Orchestrator (Basic)
Located in `orchestrator/orchestrator.py`. Coordinates agent execution — currently runs the Risk & Deadline agent across all tasks and compiles a combined report. Structured to add more agents (Resource Usage, Budget Tracking, Task Allocation) as they're built.

### How to run
```
python orchestrator/orchestrator.py
```

### Sample output
The agent correctly identifies a task as `high_risk` when its dependency task is behind schedule, and `on_track` otherwise — with a confidence score and reasoning for each.

## Tech Stack
- Python 3.12
- LangChain
- Google Gemini API (via `langchain-google-genai`)

## Upcoming
- Resource Usage Agent
- Budget Tracking Agent
- Task Allocation Agent
- Central Decision Engine (conflict resolution across agents)
