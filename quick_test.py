from db.session import init_db
from db.repository import (
    create_project, get_or_create_person, assign_person_to_project,
    get_project_team_v2, get_all_people
)

init_db()

# Create two projects
pid_a = create_project("Project A - Test")
pid_b = create_project("Project B - Test")

# Create Sana once, globally
sana_id = get_or_create_person("Sana", capacity_hrs_week=40, skills=["DevOps", "Cloud"])

# Assign her to Project A with heavy hours (overloaded there)
assign_person_to_project(sana_id, pid_a, logged_hrs_week=35)

# Assign her to Project B too, with more hours
assign_person_to_project(sana_id, pid_b, logged_hrs_week=15)

print("Project A team:", get_project_team_v2(pid_a))
print("\nProject B team:", get_project_team_v2(pid_b))
print("\nAll people (global view):", get_all_people())