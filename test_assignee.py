import logging

# Suppress internal log output so only the recommendation messages are printed.
# Set level=logging.WARNING (or remove this line) if you want to see the logs too.
logging.disable(logging.CRITICAL)

from tools.allocation_tools import recommend_assignee

candidates = [
    {'name': 'Riya', 'utilization_pct': 115, 'skills': ['backend', 'python']},
    {'name': 'Arjun', 'utilization_pct': 75, 'skills': ['frontend', 'design']},
]

tests = [
    ("required_skill='backend'", {'required_skill': 'backend'}),
    ("required_skill='frontend'", {'required_skill': 'frontend'}),
    ("no skill filter", {}),
]

for label, kwargs in tests:
    result = recommend_assignee(candidates, **kwargs)
    print(f"\n[{label}]")
    print(f"  message      : {result.message}")
    print(f"  name         : {result.name}")
    print(f"  utilization  : {result.utilization_pct}")
    print(f"  skill_match  : {result.skill_match}")
    print(f"  overloaded   : {result.overloaded}")
    print(f"  error        : {result.error}")


