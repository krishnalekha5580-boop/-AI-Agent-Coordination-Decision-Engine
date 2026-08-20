from tools.allocation_tools import recommend_assignee

candidates = [
    {'name': 'A', 'utilization_pct': 70, 'skills': ['backend']},
    {'name': 'B', 'utilization_pct': 40, 'skills': ['frontend']},
]

result = recommend_assignee(candidates, required_skill='backend')
print(result.name)
print(result.message)
print(result.skill_match)
print(result.overloaded)
