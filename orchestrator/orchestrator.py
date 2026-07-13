import sys, os, json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.risk_deadline import risk_agent

def run_risk_agent(project_data):
    findings = []
    for task in project_data["tasks"]:
        prompt = f"Analyze this task using the tools: {task}. Full task list for dependency checks: {project_data['tasks']}"
        response = risk_agent.invoke({"messages": [{"role": "user", "content": prompt}]})
        findings.append({
            "agent": "risk_deadline",
            "task_id": task["id"],
            "output": response["messages"][-1].content
        })
    return findings

def orchestrate(project_data):
    all_findings = []
    all_findings.extend(run_risk_agent(project_data))
    # Future: all_findings.extend(run_resource_agent(project_data))
    # Future: all_findings.extend(run_budget_agent(project_data))
    return all_findings

if __name__ == "__main__":
    with open("data/sample_project.json") as f:
        project_data = json.load(f)

    results = orchestrate(project_data)
    print("=== Orchestrator Report ===")
    for r in results:
        print(f"[{r['agent']}] {r['task_id']}: {r['output']}\n")