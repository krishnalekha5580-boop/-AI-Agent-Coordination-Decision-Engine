import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.session import init_db
from db.repository import (
    create_project, list_projects, get_project_summary,
    add_team_member, get_team_members, get_team_members_with_db_id, update_team_member, delete_team_member,
    add_task, get_tasks, get_tasks_with_db_id, update_task, delete_task,
    add_budget_entry, get_latest_budget_entry,
    get_recent_findings
)
from orchestrator.orchestrator import orchestrate

init_db()

st.set_page_config(page_title="AI Project Decision Engine", layout="wide", page_icon="🧭")

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1e3a5f, #2c5f8a);
        padding: 1.5rem 2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 1.8rem;
    }
    .main-header p {
        color: #cfe0f0;
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }
    div[data-testid="stMetric"] {
        background-color: #f8f9fb;
        border: 1px solid #e0e4e8;
        border-radius: 8px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)
# ---------- SIDEBAR: project selector + settings ----------
st.sidebar.title("AI Decision Engine")

mock_mode = st.sidebar.checkbox("Use Mock Mode (no API calls, instant)", value=True)
os.environ["USE_MOCK_AGENT"] = "1" if mock_mode else "0"

st.sidebar.markdown("---")
st.sidebar.subheader("Project")

existing_projects = list_projects()
project_names = {p["name"]: p["id"] for p in existing_projects}

action = st.sidebar.radio("Action", ["Open existing", "Create new"], label_visibility="collapsed")
if action == "Create new":
    st.session_state.pop("active_project_id", None)
    st.session_state.pop("active_project_name", None)

    new_name = st.sidebar.text_input("New project name")
    if st.sidebar.button("Create Project", type="primary"):
        if new_name.strip():
            pid = create_project(new_name.strip())
            st.session_state["active_project_id"] = pid
            st.session_state["active_project_name"] = new_name.strip()
            st.rerun()
        else:
            st.sidebar.error("Enter a name")

elif action == "Open existing":
    if project_names:
        selected = st.sidebar.selectbox("Select project", list(project_names.keys()))
        if st.sidebar.button("Open", type="primary"):
            st.session_state["active_project_id"] = project_names[selected]
            st.session_state["active_project_name"] = selected
            st.rerun()
    else:
        st.sidebar.info("No projects yet")

active_id = st.session_state.get("active_project_id")
active_name = st.session_state.get("active_project_name")

if not active_id:
    st.markdown("""
    <div class="main-header">
        <h1>🧭 AI Agent Coordination &amp; Decision Engine</h1>
        <p>Multi-agent risk, resource, and budget analysis for project managers</p>
    </div>
    """, unsafe_allow_html=True)
    st.info("Create or open a project from the sidebar to get started.")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.success(f"Active: **{active_name}**")

# ---------- MAIN AREA: page navigation via tabs (no long scroll) ----------
st.markdown(f"""
<div class="main-header">
    <h1>🧭 {active_name}</h1>
    <p>AI Agent Coordination &amp; Decision Engine</p>
</div>
""", unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ["Overview", "Tasks", "Team", "Budget", "Run Analysis", "History"])

# ---------- OVERVIEW ----------
if page == "Overview":
    summary = get_project_summary(active_id)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tasks", summary["task_count"])
    col2.metric("Team Members", summary["team_count"])
    budget_data = get_latest_budget_entry(active_id)
    budget_status = "Not Set"
    if budget_data:
        from tools.budget_tools import check_budget_status
        result = check_budget_status(budget_data["planned_spend"], budget_data["actual_spend"], budget_data["pct_time_elapsed"])
        if result.startswith("over_budget"):
            budget_status = "⚠️ Over Budget"
        elif result.startswith("at_risk"):
            budget_status = "🟡 At Risk"
        else:
            budget_status = "✅ On Budget"
    col3.metric("Budget Status", budget_status)
    col4.metric("Last Analysis", summary["last_analysis"].strftime("%b %d, %H:%M") if summary["last_analysis"] else "Never")

    # ---------- VALIDATION CHECKS ----------
    tasks = get_tasks(active_id)
    team = get_team_members(active_id)
    team_names = {t["name"] for t in team}
    task_ids = {t["id"] for t in tasks}

    warnings = []
    for task in tasks:
        if task["assigned_to"] and task["assigned_to"] not in team_names:
            warnings.append(f"Task {task['id']} is assigned to '{task['assigned_to']}', who is not in the team list.")
        for dep in task["depends_on"]:
            if dep not in task_ids:
                warnings.append(f"Task {task['id']} depends on '{dep}', which does not exist in this project.")

    if warnings:
        st.markdown("---")
        st.warning("**Data issues found:**")
        for w in warnings:
            st.write(f"- {w}")

    st.markdown("---")
    st.write("Use the sidebar to manage tasks, team members, budget, and run analysis.")
# ---------- TASKS ----------
elif page == "Tasks":
    st.subheader("Tasks")
    with st.expander("Add New Task"):
        with st.form("task_form", clear_on_submit=True):
            tid = st.text_input("Task ID (e.g. T1)")
            tname = st.text_input("Task Name")
            progress = st.slider("Progress %", 0, 100, 0)
            deadline = st.date_input("Deadline")
            assigned_to = st.text_input("Assigned To")
            depends_on_raw = st.text_input("Depends On (comma-separated task IDs)")
            if st.form_submit_button("Add Task"):
                if tid.strip() and tname.strip():
                    depends_on = [d.strip() for d in depends_on_raw.split(",") if d.strip()]
                    add_task(active_id, tid.strip(), tname.strip(), progress, str(deadline), depends_on, assigned_to.strip())
                    st.success(f"Task {tid} added")
                    st.rerun()
                else:
                    st.error("Task ID and Name required")

    current_tasks = get_tasks_with_db_id(active_id)
    if not current_tasks:
        st.info("No tasks yet. Add one above.")
    else:
        for task in current_tasks:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.write(f"**{task['id']} — {task['name']}**")
                    st.caption(f"Progress: {task['progress_pct']}% | Deadline: {task['planned_end']} | "
                               f"Assigned: {task['assigned_to'] or '-'} | Depends on: {', '.join(task['depends_on']) or 'none'}")
                with col2:
                    edit_key = f"edit_task_{task['db_id']}"
                    if st.button("Edit", key=f"btn_{edit_key}"):
                        st.session_state[edit_key] = not st.session_state.get(edit_key, False)

                if st.session_state.get(f"edit_task_{task['db_id']}", False):
                    with st.form(f"edit_form_{task['db_id']}"):
                        new_name = st.text_input("Name", value=task["name"])
                        new_progress = st.slider("Progress %", 0, 100, int(task["progress_pct"]))
                        new_deadline = st.text_input("Deadline (YYYY-MM-DD)", value=task["planned_end"])
                        new_assigned = st.text_input("Assigned To", value=task["assigned_to"] or "")
                        new_depends = st.text_input("Depends On", value=", ".join(task["depends_on"]))
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.form_submit_button("Save Changes"):
                                depends_list = [d.strip() for d in new_depends.split(",") if d.strip()]
                                update_task(task["db_id"], new_name, new_progress, new_deadline, depends_list, new_assigned)
                                st.session_state[f"edit_task_{task['db_id']}"] = False
                                st.rerun()
                        with c2:
                            if st.form_submit_button("Delete Task", type="secondary"):
                                delete_task(task["db_id"])
                                st.rerun()
# ---------- TEAM ----------
elif page == "Team":
    st.subheader("Team")
    with st.expander("Add New Team Member"):
        with st.form("member_form", clear_on_submit=True):
            mname = st.text_input("Name")
            capacity = st.number_input("Weekly Capacity (hrs)", value=40.0)
            logged = st.number_input("Logged Hours This Week", value=0.0)
            skills_raw = st.text_input("Skills (comma-separated)")
            if st.form_submit_button("Add Team Member"):
                if mname.strip():
                    skills = [s.strip() for s in skills_raw.split(",") if s.strip()]
                    add_team_member(active_id, mname.strip(), capacity, logged, skills)
                    st.success(f"{mname} added")
                    st.rerun()
                else:
                    st.error("Name required")

    current_team = get_team_members_with_db_id(active_id)
    if not current_team:
        st.info("No team members yet. Add one above.")
    else:
        for member in current_team:
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    pct = (member["logged_hrs_week"] / member["capacity_hrs_week"] * 100) if member["capacity_hrs_week"] else 0
                    st.write(f"**{member['name']}**")
                    st.caption(f"{member['logged_hrs_week']}/{member['capacity_hrs_week']} hrs ({pct:.0f}% utilized) | "
                               f"Skills: {', '.join(member['skills']) or 'none listed'}")
                with col2:
                    edit_key = f"edit_member_{member['db_id']}"
                    if st.button("Edit", key=f"btn_{edit_key}"):
                        st.session_state[edit_key] = not st.session_state.get(edit_key, False)

                if st.session_state.get(f"edit_member_{member['db_id']}", False):
                    with st.form(f"edit_member_form_{member['db_id']}"):
                        new_name = st.text_input("Name", value=member["name"])
                        new_capacity = st.number_input("Weekly Capacity (hrs)", value=float(member["capacity_hrs_week"]))
                        new_logged = st.number_input("Logged Hours", value=float(member["logged_hrs_week"]))
                        new_skills = st.text_input("Skills", value=", ".join(member["skills"]))
                        c1, c2 = st.columns(2)
                        with c1:
                            if st.form_submit_button("Save Changes"):
                                skills_list = [s.strip() for s in new_skills.split(",") if s.strip()]
                                update_team_member(member["db_id"], new_name, new_capacity, new_logged, skills_list)
                                st.session_state[f"edit_member_{member['db_id']}"] = False
                                st.rerun()
                        with c2:
                            if st.form_submit_button("Delete Member", type="secondary"):
                                delete_team_member(member["db_id"])
                                st.rerun()
# ---------- BUDGET ----------
elif page == "Budget":
    st.subheader("Budget")
    current_budget = get_latest_budget_entry(active_id)
    if current_budget:
        st.json(current_budget)
    else:
        st.info("No budget set yet.")

    with st.form("budget_form"):
        planned = st.number_input("Planned Spend ($)", value=current_budget["planned_spend"] if current_budget else 50000.0)
        actual = st.number_input("Actual Spend ($)", value=current_budget["actual_spend"] if current_budget else 0.0)
        pct_time = st.slider("% of Timeline Elapsed", 0, 100, int(current_budget["pct_time_elapsed"]) if current_budget else 0)
        if st.form_submit_button("Save Budget"):
            add_budget_entry(active_id, planned, actual, pct_time)
            st.success("Budget saved")
            st.rerun()

# ---------- RUN ANALYSIS ----------
elif page == "Run Analysis":
    st.subheader("Run Analysis")
    tasks = get_tasks(active_id)
    team = get_team_members(active_id)
    budget = get_latest_budget_entry(active_id)

    if not tasks:
        st.warning("Add at least one task first (see Tasks page).")
    else:
        if st.button("Run Analysis", type="primary"):
            project_data = {"tasks": tasks, "team": team}
            if budget:
                project_data["budget"] = budget

            with st.spinner("Agents analyzing project..."):
                results, conflicts = orchestrate(project_data, active_id)

            st.session_state["last_results"] = results  # moved here, right after results exists

            st.markdown("### Results")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write("**Risk & Deadline**")
                for r in results:
                    if r["agent"] == "risk_deadline":
                        (st.error if r["finding"] == "high_risk" else st.success)(r["user_response"])
            with col2:
                st.write("**Resource Usage**")
                for r in results:
                    if r["agent"] == "resource_usage":
                        (st.error if r["finding"] in ("overloaded", "severely_overloaded") else st.success)(r["user_response"])
            with col3:
                st.write("**Budget**")
                for r in results:
                    if r["agent"] == "budget_tracking":
                        (st.error if r["finding"] == "over_budget" else st.success)(r["user_response"])

            st.markdown("### Decision Engine: Conflicts & Recommendations")
            if conflicts:
                for c in conflicts:
                    st.warning(f"**{c['issue']}**")
                    st.markdown(f"➜ {c['recommendation']}")
            else:
                st.info("No conflicts detected.")

# ---------- HISTORY ----------
elif page == "History":
    st.subheader("Short-Term Memory (this session)")
    if "last_results" in st.session_state:
        st.table(st.session_state["last_results"])
    else:
        st.info("Run an analysis this session to see short-term memory.")

    st.subheader("Long-Term Memory (full project history)")
    history = get_recent_findings(active_id, limit=20)
    if history:
        st.table(history)
    else:
        st.info("No history yet.")