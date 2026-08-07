from tools.distribution_tools import analyze_workload_distribution

team = [
    {"name": "Riya", "capacity_hrs_week": 40, "logged_hrs_week": 46},
    {"name": "Arjun", "capacity_hrs_week": 40, "logged_hrs_week": 15},
]
print(analyze_workload_distribution(team))