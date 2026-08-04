# AI Agent Coordination & Decision Engine

A multi-agent system for project management, where specialized AI agents independently analyze different aspects of a project, and a central Decision Engine cross-references their findings to detect conflicts and produce specific, actionable recommendations.

## Architecture (mapped to agent framework)

| Component | Where it lives |
|---|---|
| **User / Input** | `data/*.json` — task, team, and budget data; or entered live via the Streamlit frontend |
| **LLM (Brain)** | Groq (Llama 3.3 70B) via `langchain-groq`; Gemini also supported via `langchain-google-genai` |
| **Planning Module** | `plan_analysis_steps()` in `orchestrator.py` — decides which tools a task needs before analysis runs |
| **Tool Calling** | `tools/risk_tools.py`, `tools/resource_tools.py`, `tools/budget_tools.py`, `tools/allocation_tools.py` |
| **Memory** | `store_finding()` / `get_recent_findings()` in `orchestrator.py` |
| **Decision Engine** | `resolve_conflicts()` in `orchestrator.py` — cross-references all agent findings and generates specific recommendations |
| **Output** | `format_user_response()` and the Streamlit frontend (`app.py`) |

## Agents Built (4 of 4 planned)

### 1. Risk & Deadline Agent (`agents/risk_deadline.py`)
Analyzes a task's timeline and dependencies to determine if it's `high_risk` or `on_track`.
**Tools:** `calculate_days_remaining`, `check_dependency_status`, `assess_progress_risk`

### 2. Resource Usage Agent (`agents/resource_usage.py`)
Analyzes a team member's workload to flag overload.
**Tools:** `calculate_utilization`

### 3. Budget Tracking Agent (`agents/budget_tracking.py`)
Analyzes project spend against timeline progress to flag overspending.
**Tools:** `check_budget_status` — compares % of budget spent against % of timeline elapsed, flagging `over_budget` if spend outpaces progress by more than a set threshold.

### 4. Task Allocation Agent (`agents/task_allocation.py`)
Given a set of candidate team members and their current utilization, recommends who has the most available capacity to take on a task.
**Tools:** `recommend_assignee` — selects the least-utilized candidate from a list.

All four agents share the same pattern: LangChain's `create_agent()`, a dedicated prompt template in `prompts/`, custom tools with error handling, and a mock-mode fallback for quota-free testing.

## Decision Engine — Multi-Factor Conflict Resolution

The orchestrator's `resolve_conflicts()` function is the core coordination logic. For every high-risk task, it checks:
1. **Is the assignee also overloaded?** (cross-references Risk + Resource findings via the task's `assigned_to` field)
2. **Is the project also over budget?** (factors in Budget findings)
3. **If reassignment is warranted, who should take it over?** — calls the Task Allocation agent (`get_reassignment_suggestion()`) to name a specific, less-utilized replacement, rather than just flagging "reassign this."

This produces recommendations like:
> *"Task T1 is high-risk, but Riya is already overloaded (115% utilized). Recommend reassigning task T1 away from Riya. Recommend Arjun (currently 75% utilized, most available capacity)."*

Verified against two datasets to confirm the logic is genuinely conditional, not hardcoded:
- A task assigned to an overloaded person → correctly flags a conflict with a named replacement
- A task assigned to a person who is *not* overloaded → correctly reports no conflict, even though the task itself is high-risk

## Frontend

A Streamlit web interface (`app.py`) provides an interactive way to run the whole system without touching code or the terminal:
- **Three data input options:** upload a JSON file, use existing sample datasets, or enter tasks/team/budget manually through a form
- **Mock mode toggle** in the sidebar — run instantly with zero API calls, or switch to live LLM calls
- **Results view:** three color-coded columns (Risk, Resource, Budget findings), followed by the Decision Engine's conflict recommendations

Run with:
```bash
streamlit run app.py
```

## Reliability Engineering

- **Deterministic verdicts:** the system extracts raw tool outputs directly from each agent's message trace and computes the final `finding` in Python — rather than trusting the LLM's final text summary, which was observed to occasionally hallucinate values or contradict its own tool outputs.
- **Mock mode:** set `USE_MOCK_AGENT=1` to run the entire pipeline (all four agents, planning, decision engine, memory, output) with zero LLM calls — used for fast, quota-free testing and reliable demos.
- **Dual LLM providers:** built on Gemini initially; added Groq as a second, independent provider after repeatedly hitting Gemini's free-tier daily quota (20 requests/day) during iterative testing. This means testing/demoing isn't dependent on a single provider's availability.
- **Error handling:** all tools handle invalid input (bad dates, zero-division, missing task IDs) gracefully via try/except instead of crashing.
- **Retry logic:** `max_retries` configured on LLM clients to recover from temporary server issues.

## How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Set up .env with GOOGLE_API_KEY and/or GROQ_API_KEY

# Run the Streamlit frontend
streamlit run app.py

# Or run the orchestrator directly from the terminal
set USE_MOCK_AGENT=1
python orchestrator/orchestrator.py

# Run isolated test cases for the Risk agent
python test_agents.py

```

## Sample Output
[risk_deadline] T1 -> high_risk
[resource_usage] Riya -> overloaded (115% utilized)
[budget_tracking] Overall Project -> on_budget

=== Decision Engine: Conflicts & Recommendations ===
Task T1 is high-risk, but Riya is already overloaded (115% utilized - overloaded)
-> Recommend reassigning task T1 away from Riya. Recommend Arjun (currently 75% utilized, most available capacity)


## Tech Stack
- Python 3.12
- LangChain (`create_agent`)
- Groq (Llama 3.3 70B) and Google Gemini
- Streamlit

## Project Structure

pm-decision-engine/
├── agents/
│ ├── risk_deadline.py
│ ├── resource_usage.py
│ ├── budget_tracking.py
│ └── task_allocation.py
├── tools/
│ ├── risk_tools.py
│ ├── resource_tools.py
│ ├── budget_tools.py
│ └── allocation_tools.py
├── prompts/
│ ├── risk_deadline_prompt.py
│ ├── budget_prompt.py
│ └── allocation_prompt.py
├── orchestrator/
│ └── orchestrator.py
├── data/
│ ├── sample_project.json
│ └── sample_project_2.json
├── app.py
├── test_agents.py
├── requirements.txt
└── README.md


## Upcoming
- Persistent memory (currently resets each run - next step is writing findings to a file or lightweight database)
- REST API layer (FastAPI) to satisfy the "Enterprise API Layer" outcome
- Multi-project support
- Real external integrations (Jira, Slack, Calendar) instead of local/manual data entry
