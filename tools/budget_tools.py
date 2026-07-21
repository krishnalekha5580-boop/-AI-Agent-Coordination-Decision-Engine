def check_budget_status(planned_spend: float, actual_spend: float, pct_time_elapsed: float) -> str:
    """Check if project spend is tracking on budget relative to timeline progress."""
    try:
        pct_spent = (actual_spend / planned_spend) * 100
        if pct_spent > pct_time_elapsed + 10:
            return f"Over budget: {pct_spent:.0f}% spent vs {pct_time_elapsed:.0f}% time elapsed"
        return f"On budget: {pct_spent:.0f}% spent vs {pct_time_elapsed:.0f}% time elapsed"
    except ZeroDivisionError:
        return "Error: planned_spend cannot be zero"