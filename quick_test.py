from db.session import init_db
from db.repository import create_project_with_description, copy_default_team_to_project, save_generated_tasks, get_tasks
from db.default_team import DEFAULT_TEAM
from agents.planning_agent import generate_task_breakdown

init_db()

pid = create_project_with_description(
    "AI-Planned E-Commerce Project",
    "Build a payment gateway integration for an e-commerce checkout flow, including frontend cart UI and backend webhook handling.",
    "2026-08-15", "2026-09-15"
)
copy_default_team_to_project(pid, DEFAULT_TEAM)

generated = generate_task_breakdown(
    "Build a payment gateway integration for an e-commerce checkout flow, including frontend cart UI and backend webhook handling.",
    DEFAULT_TEAM
)

count = save_generated_tasks(pid, generated, default_deadline="2026-09-10")
print(f"Saved {count} tasks")
print(get_tasks(pid))