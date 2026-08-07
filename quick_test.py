from tools.scrum_tools import check_sprint_progress, flag_impediments

tasks = [
    {"id": "T1", "progress_pct": 100, "planned_end": "2026-08-01"},
    {"id": "T2", "progress_pct": 40, "planned_end": "2026-08-10"},
    {"id": "T3", "progress_pct": 0, "planned_end": "2026-08-07"},
]

print(check_sprint_progress(tasks))
print(flag_impediments(tasks))