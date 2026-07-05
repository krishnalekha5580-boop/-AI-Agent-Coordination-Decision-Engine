from datetime import datetime
from typing import List, Dict, Any

def calculate_days_remaining(planned_end: str) -> int:
    """Calculate days left until a task's planned end date. Format: YYYY-MM-DD"""
    end = datetime.strptime(planned_end, "%Y-%m-%d")
    return (end - datetime.now()).days

def check_dependency_status(task_id: str, all_tasks:  List[Dict[str, Any]]) -> str:
    """Check if a task's dependencies are behind schedule."""
    task = next(t for t in all_tasks if t["id"] == task_id)
    for dep_id in task.get("depends_on", []):
        dep = next(t for t in all_tasks if t["id"] == dep_id)
        if dep["progress_pct"] < 70:
            return f"Dependency {dep_id} is behind schedule"
    return "No dependency issues"