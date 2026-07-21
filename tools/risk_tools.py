from datetime import datetime
from typing import List, Dict, Any

def calculate_days_remaining(planned_end: str) -> int:
    """Calculate days left until a task's planned end date. Format: YYYY-MM-DD. Returns an integer."""
    try:
        from datetime import datetime
        end = datetime.strptime(planned_end, "%Y-%m-%d")
        return (end - datetime.now()).days
    except ValueError:
        return -999  # sentinel for invalid date
def check_dependency_status(task_id: str, all_tasks: List[Dict[str, Any]]) -> str:
    """Check if a task's dependencies are behind schedule."""
    try:
        task = next((t for t in all_tasks if t.get("id") == task_id), None)
        if task is None:
            return "Could not verify dependencies - task not found in provided list"
        for dep_id in task.get("depends_on", []):
            dep = next((t for t in all_tasks if t.get("id") == dep_id), None)
            if dep is None:
                continue
            if dep.get("progress_pct", 100) < 70:
                return f"Dependency {dep_id} is behind schedule"
        return "No dependency issues"
    except Exception as e:
        return f"Error checking dependency status: {str(e)}"
        
def load_project_data(filepath: str = "data/sample_project.json") -> dict:
    """Load project data from the project management system's data source."""
    import json
    with open(filepath) as f:
        return json.load(f)

def assess_progress_risk(progress_pct: float, days_remaining: int) -> str:
    """Assess risk based on how much work is done vs how much time is left."""
    if days_remaining <= 0:
        return "high_risk: deadline has passed or is today"
    if progress_pct < 50 and days_remaining <= 3:
        return "high_risk: low progress with very little time remaining"
    if progress_pct < 70 and days_remaining <= 1:
        return "high_risk: insufficient progress for remaining time"
    return "low_risk: progress is reasonable for time remaining"