import sys
import os
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
# from langchain_google_genai import ChatGoogleGenerativeAI
from tools.risk_tools import calculate_days_remaining, check_dependency_status, assess_progress_risk
from prompts.risk_deadline_prompt import RISK_DEADLINE_SYSTEM_PROMPT
from langchain_groq import ChatGroq

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)
# model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.2)

risk_agent = create_agent(
    model=model,
    tools=[calculate_days_remaining, check_dependency_status, assess_progress_risk],
    system_prompt=RISK_DEADLINE_SYSTEM_PROMPT
)

if __name__ == "__main__":
    with open("data/sample_project.json") as f:
        project_data = json.load(f)

    for task in project_data["tasks"]:
        prompt = f"Analyze this task using the tools: {task}. Full task list for dependency checks: {project_data['tasks']}"
        response = risk_agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        print(f"--- {task['id']} ---")
        print(response["messages"][-1].content)
        print()