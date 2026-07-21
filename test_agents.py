import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from agents.risk_deadline import risk_agent

test_cases = [
    {"task": {"id": "T1", "progress_pct": 90, "planned_end": "2026-08-01", "depends_on": []}, "expected": "on_track"},
    {"task": {"id": "T2", "progress_pct": 10, "planned_end": "2026-07-16", "depends_on": []}, "expected": "high_risk"},
]
for case in test_cases:
    prompt = f"Analyze this task: {case['task']}"
    response = risk_agent.invoke({"messages": [{"role": "user", "content": prompt}]})
    print(f"--- Full message trace for {case['task']['id']} ---")
    for m in response["messages"]:
        print(type(m).__name__, ":", getattr(m, "content", None))
    print()