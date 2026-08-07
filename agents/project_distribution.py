import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools.distribution_tools import analyze_workload_distribution
from prompts.distribution_prompt import DISTRIBUTION_SYSTEM_PROMPT

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

distribution_agent = create_agent(
    model=model,
    tools=[analyze_workload_distribution],
    system_prompt=DISTRIBUTION_SYSTEM_PROMPT
)

import json

if __name__ == "__main__":
    team = [
        {"name": "Riya", "capacity_hrs_week": 40, "logged_hrs_week": 46},
        {"name": "Arjun", "capacity_hrs_week": 40, "logged_hrs_week": 15},
    ]
    response = distribution_agent.invoke({
        "messages": [{"role": "user", "content": f"Analyze this team's workload distribution: {json.dumps(team)}"}]
    })
    print(response["messages"][-1].content)