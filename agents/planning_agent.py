import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
from langchain_groq import ChatGroq
from tools.planning_tools import format_team_for_matching
from prompts.planning_prompt import PLANNING_SYSTEM_PROMPT

# model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)
model = ChatGroq(model="openai/gpt-oss-120b", temperature=0.3)
def generate_task_breakdown(description: str, team: list) -> list:
    """Given a project description and team, return a list of proposed tasks with assignments."""
    team_str = format_team_for_matching(team)
    prompt = (
        f"Project description: {description}\n\n"
        f"Available team members:\n{team_str}\n\n"
        f"Break this into tasks and assign each to the best-matching team member."
    )

    response = model.invoke([
        {"role": "system", "content": PLANNING_SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ])

    content = response.content.strip()
    # Strip markdown code fences if the model added them despite instructions
    if content.startswith("```"):
        content = content.split("```")[1]
        if content.startswith("json"):
            content = content[4:]
        content = content.strip()

    try:
        tasks = json.loads(content)
        return tasks
    except json.JSONDecodeError:
        return []


if __name__ == "__main__":
    from db.default_team import DEFAULT_TEAM

    description = "Build a payment gateway integration for an e-commerce checkout flow, including frontend cart UI and backend webhook handling."
    tasks = generate_task_breakdown(description, DEFAULT_TEAM)

    print(f"Generated {len(tasks)} tasks:")
    for t in tasks:
        print(f"  {t.get('id')} - {t.get('name')} → {t.get('assigned_to')} (skill: {t.get('required_skill')})")