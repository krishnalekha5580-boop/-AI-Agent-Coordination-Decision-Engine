from typing import List, Dict, Any

def analyze_workload_distribution(team: List[Dict[str, Any]]) -> str:
    """
    Analyze how evenly work is distributed across the team.
    Flags if workload is concentrated on too few people while others are underused.
    """
    try:
        if not team:
            return "No team members to analyze"

        utilizations = []
        for member in team:
            capacity = member.get("capacity_hrs_week", 40)
            logged = member.get("logged_hrs_week", 0)
            pct = (logged / capacity * 100) if capacity else 0
            utilizations.append((member.get("name", "unknown"), pct))

        overloaded = [n for n, p in utilizations if p > 100]
        underused = [n for n, p in utilizations if p < 60]

        if overloaded and underused:
            return (f"Imbalanced distribution: {', '.join(overloaded)} overloaded while "
                    f"{', '.join(underused)} underutilized - rebalancing recommended")
        elif overloaded:
            return f"Overloaded: {', '.join(overloaded)} - but no clearly available team members to redistribute to"
        elif underused:
            return f"Underutilized: {', '.join(underused)} - team has spare capacity"
        else:
            return "Workload is reasonably balanced across the team"
    except Exception as e:
        return f"Error analyzing workload distribution: {str(e)}"