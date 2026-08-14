from db.default_team import DEFAULT_TEAM
from orchestrator.orchestrator import get_reassignment_suggestion

project_data = {
    "tasks": [{"id": "T1", "required_skill": "Backend"}],
    "team": DEFAULT_TEAM
}

# Simulate Priya being overloaded, task needs Backend skill
result = get_reassignment_suggestion(project_data, exclude_person="Priya", required_skill="Backend")
print(result)
result2 = get_reassignment_suggestion(project_data, exclude_person="Arjun", required_skill="Frontend")
print(result2)
result3 = get_reassignment_suggestion(
    {"tasks": [{"id": "T1", "required_skill": "QA"}], "team": DEFAULT_TEAM},
    exclude_person="Priya",
    required_skill="QA"
)
print(result3)