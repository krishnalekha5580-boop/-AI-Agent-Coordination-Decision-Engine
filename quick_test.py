from db.session import init_db
from db.repository import get_tasks, get_team_members, get_latest_budget_entry
from orchestrator.orchestrator import orchestrate
import os

os.environ["USE_MOCK_AGENT"] = "1"
init_db()

pid = 4
tasks = get_tasks(pid)
team = get_team_members(pid)
budget = get_latest_budget_entry(pid)

project_data = {"tasks": tasks, "team": team}
if budget:
    project_data["budget"] = budget

results, conflicts = orchestrate(project_data, pid)

for r in results:
    if r["agent"] == "risk_deadline":
        print(r["task_id"], "->", r["finding"])
        print("   ", r["raw_tool_outputs"])