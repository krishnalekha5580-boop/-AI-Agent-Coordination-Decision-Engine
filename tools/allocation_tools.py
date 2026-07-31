def recommend_assignee(candidates: list) -> str:
    """
    Given a list of candidates (each a dict with 'name' and 'utilization_pct'),
    recommend the one with the most available capacity.
    """
    try:
        if not candidates:
            return "No candidates provided"
        best = min(candidates, key=lambda c: c["utilization_pct"])
        return f"Recommend {best['name']} (currently {best['utilization_pct']}% utilized, most available capacity)"
    except (KeyError, TypeError):
        return "Error: candidates must include 'name' and 'utilization_pct'"