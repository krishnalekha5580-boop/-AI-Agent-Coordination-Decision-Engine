def check_budget_status(planned_spend: float, actual_spend: float, pct_time_elapsed: float) -> str:
    """Check current budget status and project whether spend will exceed budget by project end."""
    try:
        if pct_time_elapsed <= 0:
            return "Error: pct_time_elapsed must be greater than 0 to project burn rate"

        pct_spent = (actual_spend / planned_spend) * 100
        burn_rate = pct_spent / pct_time_elapsed  # >1 means spending faster than time is passing
        projected_final_pct = burn_rate * 100  # if this rate continues to 100% time elapsed

        if projected_final_pct > 115:
            status = "over_budget"
            detail = f"projected to reach {projected_final_pct:.0f}% of budget by project end at current burn rate"
        elif projected_final_pct > 100:
            status = "at_risk"
            detail = f"projected to reach {projected_final_pct:.0f}% of budget by project end - monitor closely"
        else:
            status = "on_budget"
            detail = f"projected to finish at {projected_final_pct:.0f}% of budget if current rate continues"

        return f"{status}: {pct_spent:.0f}% spent vs {pct_time_elapsed:.0f}% time elapsed - {detail}"
    except ZeroDivisionError:
        return "Error: planned_spend cannot be zero"

def check_threshold_alerts(pct_spent: float) -> str:
    """Check if spending has crossed key alert thresholds."""
    if pct_spent >= 100:
        return "ALERT: Budget fully consumed (100%+) - immediate action required"
    elif pct_spent >= 90:
        return "ALERT: 90% of budget consumed - critical review needed"
    elif pct_spent >= 80:
        return "WARNING: 80% of budget consumed - monitor closely"
    else:
        return f"No threshold alert - {pct_spent:.0f}% consumed"