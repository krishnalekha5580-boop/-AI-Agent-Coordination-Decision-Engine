def calculate_utilization(logged_hrs: float, capacity_hrs: float) -> str:
    """Calculate team member utilization percentage with severity level."""
    try:
        pct = (logged_hrs / capacity_hrs) * 100
        if pct > 130:
            status = "severely_overloaded"
        elif pct > 100:
            status = "overloaded"
        elif pct > 85:
            status = "near_capacity"
        else:
            status = "available"
        return f"{pct:.0f}% utilized - {status}"
    except ZeroDivisionError:
        return "Error: capacity_hrs cannot be zero"