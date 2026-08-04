from db.session import init_db
from db.repository import (
    create_project, add_team_member, add_task, add_budget_entry,
    get_team_members, get_tasks, get_latest_budget_entry,
    save_finding, get_recent_findings,
)

init_db()

project_id = create_project("Demo Project")
print(f"Created project with id: {project_id}")

add_team_member(project_id, "Riya", 115, ["backend", "python"])
add_team_member(project_id, "Arjun", 75, ["frontend", "design"])

add_task(project_id, "T1", "Build login API", status="in_progress", assigned_to="Riya", dependencies=[])

add_budget_entry(project_id, spent_pct=60, timeline_pct=40)

save_finding(project_id, "resource_usage", "Riya", "overloaded", {"utilization_pct": 115})

print("\nTeam members:", get_team_members(project_id))
print("\nTasks:", get_tasks(project_id))
print("\nLatest budget:", get_latest_budget_entry(project_id))
print("\nRecent findings:", get_recent_findings(project_id))