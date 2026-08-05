from fastapi import FastAPI, HTTPException
from db.session import init_db
from db.repository import (
    create_project, list_projects, get_tasks, get_team_members,
    get_latest_budget_entry, get_recent_findings
)
from orchestrator.orchestrator import orchestrate

init_db()

app = FastAPI(title="AI Agent Coordination & Decision Engine API")


@app.get("/")
def root():
    return {"status": "running", "service": "AI Agent Coordination & Decision Engine"}


@app.get("/projects")
def get_projects():
    return list_projects()


@app.post("/projects/{project_id}/analyze")
def analyze_project(project_id: int):
    tasks = get_tasks(project_id)
    if not tasks:
        raise HTTPException(status_code=404, detail="No tasks found for this project")

    team = get_team_members(project_id)
    budget = get_latest_budget_entry(project_id)

    project_data = {"tasks": tasks, "team": team}
    if budget:
        project_data["budget"] = budget

    results, conflicts = orchestrate(project_data, project_id)
    return {"findings": results, "conflicts": conflicts}


@app.get("/projects/{project_id}/history")
def project_history(project_id: int, limit: int = 20):
    return get_recent_findings(project_id, limit=limit)