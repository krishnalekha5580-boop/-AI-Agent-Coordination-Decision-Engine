import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dotenv import load_dotenv
load_dotenv()
from langchain.agents import create_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.resource_tools import calculate_utilization
from prompts.resource_usage_prompt import RESOURCE_USAGE_SYSTEM_PROMPT

model = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.2, max_retries=3)

resource_agent = create_agent(
    model=model,
    tools=[calculate_utilization],
    system_prompt=RESOURCE_USAGE_SYSTEM_PROMPT
)
if __name__ == "__main__":
    response = resource_agent.invoke({
        "messages": [{"role": "user", "content": "Check utilization for Riya: logged 46 hrs, capacity 40 hrs."}]
    })
    print(response["messages"][-1].content)