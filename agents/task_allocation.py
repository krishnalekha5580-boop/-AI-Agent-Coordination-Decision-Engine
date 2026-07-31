import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from tools.allocation_tools import recommend_assignee
from prompts.allocation_prompt import ALLOCATION_SYSTEM_PROMPT

model = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.2)

allocation_agent = create_agent(
    model=model,
    tools=[recommend_assignee],
    system_prompt=ALLOCATION_SYSTEM_PROMPT
)

if __name__ == "__main__":
    response = allocation_agent.invoke({
        "messages": [{"role": "user", "content": "Candidates: Riya (115% utilized), Arjun (75% utilized). Who should take a new task?"}]
    })
    print(response["messages"][-1].content)