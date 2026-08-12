from db.session import init_db
from db.repository import create_project_with_description, copy_default_team_to_project, get_team_members
from db.default_team import DEFAULT_TEAM

init_db()

pid = create_project_with_description(
    "Test Description Project",
    "Build a payment gateway integration for an e-commerce checkout flow",
    "2026-08-15", "2026-09-15"
)
print("Created project:", pid)

copy_default_team_to_project(pid, DEFAULT_TEAM)
print("Team seeded")

print(get_team_members(pid))