"""
scripts/migrate_json_to_db.py

One-time migration: loads existing data/*.json fixtures into the database
as real projects, so no test data is lost when switching from files to DB.

Usage:
    python scripts/migrate_json_to_db.py
"""

import json
import os
import sys

# allow running this script directly from project root
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.session import init_db
from db.repository import create_project, add_team_member, add_task, add_budget_entry


def migrate_file(filepath: str, project_name: str):
    with open(filepath) as f:
        data = json.load(f)

    project_id = create_project(project_name)
    print(f"Created project '{project_name}' (id={project_id}) from {filepath}")

    for member in data.get("team", []):
        add_team_member(
            project_id=project_id,
            name=member["name"],
            capacity_hrs_week=member["capacity_hrs_week"],
            logged_hrs_week=member["logged_hrs_week"],
            skills=member.get("skills", []),  # not in old JSON yet, defaults to []
        )

    for task in data.get("tasks", []):
        add_task(
            project_id=project_id,
            task_key=task["id"],
            title=task["name"],
            progress_pct=task.get("progress_pct", 0),
            planned_end=task.get("planned_end"),
            depends_on=task.get("depends_on", []),
            assigned_to=task.get("assigned_to"),
        )

    budget = data.get("budget")
    if budget:
        add_budget_entry(
            project_id=project_id,
            planned_spend=budget["planned_spend"],
            actual_spend=budget["actual_spend"],
            pct_time_elapsed=budget["pct_time_elapsed"],
        )

    print(f"  -> {len(data.get('team', []))} team members, "
          f"{len(data.get('tasks', []))} tasks, "
          f"{'1 budget entry' if budget else '0 budget entries'}")


if __name__ == "__main__":
    init_db()

    migrate_file("data/sample_project.json", "Sample Project 1")
    migrate_file("data/sample_project_2.json", "Sample Project 2")

    print("\nMigration complete.")