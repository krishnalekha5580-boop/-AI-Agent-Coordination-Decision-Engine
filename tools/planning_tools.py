def format_team_for_matching(team: list) -> str:
    """Format team roster into a readable string for the LLM to reference when assigning tasks."""
    lines = []
    for member in team:
        skills_str = ", ".join(member.get("skills", []))
        lines.append(f"- {member['name']}: skills = [{skills_str}]")
    return "\n".join(lines)