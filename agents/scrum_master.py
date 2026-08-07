import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools.scrum_tools import check_sprint_progress, flag_impediments
from prompts.scrum_prompt import SCRUM_MASTER_SYSTEM_PROMPT

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

scrum_master_agent = create_agent(
    model=model,
    tools=[check_sprint_progress, flag_impediments],
    system_prompt=SCRUM_MASTER_SYSTEM_PROMPT
)

if __name__ == "__main__":
    tasks = [
        {"id": "T1", "progress_pct": 100, "planned_end": "2026-08-01"},
        {"id": "T2", "progress_pct": 40, "planned_end": "2026-08-10"},
        {"id": "T3", "progress_pct": 0, "planned_end": "2026-08-07"},
    ]
    response = scrum_master_agent.invoke({
        "messages": [{"role": "user", "content": f"Evaluate this sprint's tasks: {tasks}"}]
    })
    print(response["messages"][-1].content)