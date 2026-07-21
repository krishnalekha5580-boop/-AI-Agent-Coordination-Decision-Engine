def calculate_utilization(logged_hrs: float, capacity_hrs: float) -> str:
    """Calculate team member utilization percentage and flag overload."""
    try:
        pct = (logged_hrs / capacity_hrs) * 100
        status = "overloaded" if pct > 100 else "available"
        return f"{pct:.0f}% utilized - {status}"
    except ZeroDivisionError:
        return "Error: capacity_hrs cannot be zero"