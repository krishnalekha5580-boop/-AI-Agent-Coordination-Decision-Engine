# AI Agent Coordination & Decision Engine

A multi-agent system for project management, where specialized AI agents independently analyze different aspects of a project, and a central Decision Engine cross-references their findings to detect conflicts and produce actionable recommendations.

## Agents Built

### 1. Risk & Deadline Agent (`agents/risk_deadline.py`)
Analyzes a task's timeline and dependencies to determine if it's `high_risk` or `on_track`.

**Tools used:**
- `calculate_days_remaining` — days left until deadline
- `check_dependency_status` — checks if dependency tasks are behind schedule
- `assess_progress_risk` — evaluates progress made vs. time remaining

**Prompt template:** `prompts/risk_deadline_prompt.py`

### 2. Resource Usage Agent (`agents/resource_usage.py`)
Analyzes a team member's workload to flag overload.

**Tools used:**
- `calculate_utilization` — logged hours vs. capacity, flags overload above 100%

## Decision Engine — Conflict Resolution

The orchestrator's `resolve_conflicts()` function is the core coordination logic. It:
1. Links tasks to their assignees (`assigned_to` field in task data)
2. Checks if a high-risk task's assignee is also flagged as overloaded
3. Generates a specific, reasoned recommendation (e.g., reassign the task rather than overload the person further)

This demonstrates genuine multi-agent coordination — two independently-running agents whose findings are cross-referenced by a central decision layer, rather than simply listed side by side.

## Reliability Engineering

- **Deterministic verdicts:** Instead of trusting the LLM's final text summary (which was observed to occasionally hallucinate numbers or contradict its own tool outputs), the system extracts raw tool outputs directly from the agent's message trace and computes the final `finding` in Python — deterministic and bug-proof against LLM inconsistency.
- **Mock mode:** Set `USE_MOCK_AGENT=1` to run the entire pipeline (planning, tools, decision engine, memory, output) without calling the LLM at all — useful for fast, quota-free testing and demos.
- **Error handling:** Tools handle invalid input (bad dates, zero-division) gracefully via try/except instead of crashing.
- **Retry logic:** `max_retries=3` on the LLM client to recover from temporary API server issues.

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Set up your .env file with GOOGLE_API_KEY

# Run in mock mode (no API calls, instant, free)
set USE_MOCK_AGENT=1
python orchestrator/orchestrator.py

# Run with real LLM calls
python orchestrator/orchestrator.py

# Run isolated test cases for the Risk agent
python test_agents.py
```

## Sample Output

Tech Stack
Python 3.12
LangChain
Google Gemini API (via langchain-google-genai)

**Upcoming**
Budget Tracking Agent
Task Allocation Agent
Central Decision Engine (conflict resolution across agents
