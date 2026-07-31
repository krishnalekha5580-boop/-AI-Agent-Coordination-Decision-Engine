import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools.budget_tools import check_budget_status
from prompts.budget_prompt import BUDGET_SYSTEM_PROMPT

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

budget_agent = create_agent(
    model=model,
    tools=[check_budget_status],
    system_prompt=BUDGET_SYSTEM_PROMPT
)

if __name__ == "__main__":
    response = budget_agent.invoke({
        "messages": [{"role": "user", "content": "Check budget: planned_spend=50000, actual_spend=41000, pct_time_elapsed=85."}]
    })
    print(response["messages"][-1].content)