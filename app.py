import streamlit as st
import json
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from orchestrator.orchestrator import orchestrate

st.set_page_config(page_title="AI Project Decision Engine", layout="wide")

st.title("AI Agent Coordination & Decision Engine")
st.caption("Multi-agent system for project risk and resource analysis")

# ---------- MODE TOGGLE ----------
mock_mode = st.sidebar.checkbox("Use Mock Mode (no API calls, instant)", value=True)
os.environ["USE_MOCK_AGENT"] = "1" if mock_mode else "0"

st.sidebar.markdown("---")
st.sidebar.write("Mock Mode is recommended for fast, quota-free testing. Turn it off to use the real LLM.")

# ---------- DATA INPUT METHOD ----------
st.header("1. Project Data")
input_method = st.radio("How do you want to provide data?", ["Upload JSON file", "Use sample data", "Enter manually"])

project_data = None

if input_method == "Upload JSON file":
    uploaded_file = st.file_uploader("Upload project JSON", type=["json"])
    if uploaded_file:
        project_data = json.load(uploaded_file)

elif input_method == "Use sample data":
    sample_choice = st.selectbox("Choose sample dataset", ["sample_project.json", "sample_project_2.json"])
    try:
        with open(f"data/{sample_choice}") as f:
            project_data = json.load(f)
    except FileNotFoundError:
        st.error(f"data/{sample_choice} not found")

elif input_method == "Enter manually":
    st.subheader("Tasks")
    num_tasks = st.number_input("Number of tasks", min_value=1, max_value=10, value=2)
    tasks = []
    for i in range(num_tasks):
        with st.expander(f"Task {i+1}"):
            tid = st.text_input(f"Task ID", value=f"T{i+1}", key=f"tid{i}")
            name = st.text_input(f"Task Name", key=f"tname{i}")
            progress = st.slider(f"Progress %", 0, 100, 50, key=f"tprog{i}")
            deadline = st.date_input(f"Deadline", key=f"tdead{i}")
            assigned_to = st.text_input(f"Assigned To", key=f"tassign{i}")
            depends_on = st.text_input(f"Depends On (comma-separated task IDs, or leave blank)", key=f"tdep{i}")
            tasks.append({
                "id": tid,
                "name": name,
                "progress_pct": progress,
                "planned_end": str(deadline),
                "assigned_to": assigned_to,
                "depends_on": [d.strip() for d in depends_on.split(",") if d.strip()]
            })

    st.subheader("Team")
    num_members = st.number_input("Number of team members", min_value=1, max_value=10, value=1)
    team = []
    for i in range(num_members):
        with st.expander(f"Team Member {i+1}"):
            mname = st.text_input(f"Name", key=f"mname{i}")
            capacity = st.number_input(f"Weekly Capacity (hrs)", value=40, key=f"mcap{i}")
            logged = st.number_input(f"Logged Hours", value=30, key=f"mlog{i}")
            team.append({"name": mname, "capacity_hrs_week": capacity, "logged_hrs_week": logged})

    st.subheader("Budget")
    planned = st.number_input("Planned Spend ($)", value=50000)
    actual = st.number_input("Actual Spend ($)", value=41000)
    pct_time = st.slider("% of Timeline Elapsed", 0, 100, 85)
    budget = {"planned_spend": planned, "actual_spend": actual, "pct_time_elapsed": pct_time}

    project_data = {"tasks": tasks, "team": team, "budget": budget}

# ---------- RUN ANALYSIS ----------
st.header("2. Run Analysis")

if project_data and st.button("Run Analysis", type="primary"):
    with st.spinner("Agents analyzing project..."):
        results, conflicts = orchestrate(project_data)

    st.header("3. Results")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Risk & Deadline Findings")
        for r in results:
            if r["agent"] == "risk_deadline":
                if r["finding"] == "high_risk":
                    st.error(r["user_response"])
                else:
                    st.success(r["user_response"])

    with col2:
        st.subheader("Resource Usage Findings")
        for r in results:
            if r["agent"] == "resource_usage":
                if r["finding"] == "overloaded":
                    st.error(r["user_response"])
                else:
                    st.success(r["user_response"])

    with col3:
        st.subheader("Budget Findings")
        for r in results:
            if r["agent"] == "budget_tracking":
                if r["finding"] == "over_budget":
                    st.error(r["user_response"])
                else:
                    st.success(r["user_response"])

    st.subheader("Decision Engine: Conflicts & Recommendations")
    if conflicts:
        for c in conflicts:
            st.warning(f"**{c['issue']}**")
            st.markdown(f"➜ {c['recommendation']}")
            st.divider()
    else:
        st.info("No conflicts detected.")

    with st.expander("Raw findings (debug view)"):
        st.json(results)

elif not project_data:
    st.info("Provide project data above to run analysis.")