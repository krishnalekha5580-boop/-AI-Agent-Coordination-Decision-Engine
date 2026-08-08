# import streamlit as st
# import os
# import sys

# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# from db.session import init_db
# from db.repository import (
#     create_project, list_projects, get_project_summary,
#     add_team_member, get_team_members, get_team_members_with_db_id, update_team_member, delete_team_member,
#     add_task, get_tasks, get_tasks_with_db_id, update_task, delete_task,
#     add_budget_entry, get_latest_budget_entry,
#     get_recent_findings
# )
# from orchestrator.orchestrator import orchestrate

# init_db()

# st.set_page_config(page_title="AI Project Decision Engine", layout="wide", page_icon="🧭")

# st.markdown("""
# <style>
#     .main-header {
#         background: linear-gradient(90deg, #1e3a5f, #2c5f8a);
#         padding: 1.5rem 2rem;
#         border-radius: 10px;
#         margin-bottom: 1.5rem;
#     }
#     .main-header h1 {
#         color: white;
#         margin: 0;
#         font-size: 1.8rem;
#     }
#     .main-header p {
#         color: #cfe0f0;
#         margin: 0.3rem 0 0 0;
#         font-size: 0.95rem;
#     }
#     div[data-testid="stMetric"] {
#         background-color: #f8f9fb;
#         border: 1px solid #e0e4e8;
#         border-radius: 8px;
#         padding: 12px;
#     }
# </style>
# """, unsafe_allow_html=True)
# # ---------- SIDEBAR: project selector + settings ----------
# st.sidebar.title("AI Decision Engine")

# mock_mode = st.sidebar.checkbox("Use Mock Mode (no API calls, instant)", value=True)
# os.environ["USE_MOCK_AGENT"] = "1" if mock_mode else "0"

# st.sidebar.markdown("---")
# st.sidebar.subheader("Project")

# existing_projects = list_projects()
# project_names = {p["name"]: p["id"] for p in existing_projects}

# action = st.sidebar.radio("Action", ["Open existing", "Create new"], label_visibility="collapsed")
# if action == "Create new":
#     st.session_state.pop("active_project_id", None)
#     st.session_state.pop("active_project_name", None)

#     new_name = st.sidebar.text_input("New project name")
#     if st.sidebar.button("Create Project", type="primary"):
#         if new_name.strip():
#             pid = create_project(new_name.strip())
#             st.session_state["active_project_id"] = pid
#             st.session_state["active_project_name"] = new_name.strip()
#             st.rerun()
#         else:
#             st.sidebar.error("Enter a name")

# elif action == "Open existing":
#     if project_names:
#         selected = st.sidebar.selectbox("Select project", list(project_names.keys()))
#         if st.sidebar.button("Open", type="primary"):
#             st.session_state["active_project_id"] = project_names[selected]
#             st.session_state["active_project_name"] = selected
#             st.rerun()
#     else:
#         st.sidebar.info("No projects yet")

# active_id = st.session_state.get("active_project_id")
# active_name = st.session_state.get("active_project_name")

# if not active_id:
#     st.markdown("""
#     <div class="main-header">
#         <h1>🧭 AI Agent Coordination &amp; Decision Engine</h1>
#         <p>Multi-agent risk, resource, and budget analysis for project managers</p>
#     </div>
#     """, unsafe_allow_html=True)
#     st.info("Create or open a project from the sidebar to get started.")
#     st.stop()

# st.sidebar.markdown("---")
# st.sidebar.success(f"Active: **{active_name}**")

# # ---------- MAIN AREA: page navigation via tabs (no long scroll) ----------
# st.markdown(f"""
# <div class="main-header">
#     <h1>🧭 {active_name}</h1>
#     <p>AI Agent Coordination &amp; Decision Engine</p>
# </div>
# """, unsafe_allow_html=True)
# page = st.sidebar.radio("Go to", ["Overview", "Tasks", "Team", "Budget", "Run Analysis", "History"])

# # ---------- OVERVIEW ----------
# if page == "Overview":
#     summary = get_project_summary(active_id)
#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Tasks", summary["task_count"])
#     col2.metric("Team Members", summary["team_count"])
#     budget_data = get_latest_budget_entry(active_id)
#     budget_status = "Not Set"
#     if budget_data:
#         from tools.budget_tools import check_budget_status
#         result = check_budget_status(budget_data["planned_spend"], budget_data["actual_spend"], budget_data["pct_time_elapsed"])
#         if result.startswith("over_budget"):
#             budget_status = "⚠️ Over Budget"
#         elif result.startswith("at_risk"):
#             budget_status = "🟡 At Risk"
#         else:
#             budget_status = "✅ On Budget"
#     col3.metric("Budget Status", budget_status)
#     col4.metric("Last Analysis", summary["last_analysis"].strftime("%b %d, %H:%M") if summary["last_analysis"] else "Never")

#     # ---------- VALIDATION CHECKS ----------
#     tasks = get_tasks(active_id)
#     team = get_team_members(active_id)
#     team_names = {t["name"] for t in team}
#     task_ids = {t["id"] for t in tasks}

#     warnings = []
#     for task in tasks:
#         if task["assigned_to"] and task["assigned_to"] not in team_names:
#             warnings.append(f"Task {task['id']} is assigned to '{task['assigned_to']}', who is not in the team list.")
#         for dep in task["depends_on"]:
#             if dep not in task_ids:
#                 warnings.append(f"Task {task['id']} depends on '{dep}', which does not exist in this project.")

#     if warnings:
#         st.markdown("---")
#         st.warning("**Data issues found:**")
#         for w in warnings:
#             st.write(f"- {w}")

#     st.markdown("---")
#     st.write("Use the sidebar to manage tasks, team members, budget, and run analysis.")
# # ---------- TASKS ----------
# elif page == "Tasks":
#     st.subheader("Tasks")
#     with st.expander("Add New Task"):
#         with st.form("task_form", clear_on_submit=True):
#             tid = st.text_input("Task ID (e.g. T1)")
#             tname = st.text_input("Task Name")
#             progress = st.slider("Progress %", 0, 100, 0)
#             deadline = st.date_input("Deadline")
#             assigned_to = st.text_input("Assigned To")
#             depends_on_raw = st.text_input("Depends On (comma-separated task IDs)")
#             if st.form_submit_button("Add Task"):
#                 if tid.strip() and tname.strip():
#                     depends_on = [d.strip() for d in depends_on_raw.split(",") if d.strip()]
#                     add_task(active_id, tid.strip(), tname.strip(), progress, str(deadline), depends_on, assigned_to.strip())
#                     st.success(f"Task {tid} added")
#                     st.rerun()
#                 else:
#                     st.error("Task ID and Name required")

#     current_tasks = get_tasks_with_db_id(active_id)
#     if not current_tasks:
#         st.info("No tasks yet. Add one above.")
#     else:
#         for task in current_tasks:
#             with st.container(border=True):
#                 col1, col2 = st.columns([4, 1])
#                 with col1:
#                     st.write(f"**{task['id']} — {task['name']}**")
#                     st.caption(f"Progress: {task['progress_pct']}% | Deadline: {task['planned_end']} | "
#                                f"Assigned: {task['assigned_to'] or '-'} | Depends on: {', '.join(task['depends_on']) or 'none'}")
#                 with col2:
#                     edit_key = f"edit_task_{task['db_id']}"
#                     if st.button("Edit", key=f"btn_{edit_key}"):
#                         st.session_state[edit_key] = not st.session_state.get(edit_key, False)

#                 if st.session_state.get(f"edit_task_{task['db_id']}", False):
#                     with st.form(f"edit_form_{task['db_id']}"):
#                         new_name = st.text_input("Name", value=task["name"])
#                         new_progress = st.slider("Progress %", 0, 100, int(task["progress_pct"]))
#                         new_deadline = st.text_input("Deadline (YYYY-MM-DD)", value=task["planned_end"])
#                         new_assigned = st.text_input("Assigned To", value=task["assigned_to"] or "")
#                         new_depends = st.text_input("Depends On", value=", ".join(task["depends_on"]))
#                         c1, c2 = st.columns(2)
#                         with c1:
#                             if st.form_submit_button("Save Changes"):
#                                 depends_list = [d.strip() for d in new_depends.split(",") if d.strip()]
#                                 update_task(task["db_id"], new_name, new_progress, new_deadline, depends_list, new_assigned)
#                                 st.session_state[f"edit_task_{task['db_id']}"] = False
#                                 st.rerun()
#                         with c2:
#                             if st.form_submit_button("Delete Task", type="secondary"):
#                                 delete_task(task["db_id"])
#                                 st.rerun()
# # ---------- TEAM ----------
# elif page == "Team":
#     st.subheader("Team")
#     with st.expander("Add New Team Member"):
#         with st.form("member_form", clear_on_submit=True):
#             mname = st.text_input("Name")
#             capacity = st.number_input("Weekly Capacity (hrs)", value=40.0)
#             logged = st.number_input("Logged Hours This Week", value=0.0)
#             skills_raw = st.text_input("Skills (comma-separated)")
#             if st.form_submit_button("Add Team Member"):
#                 if mname.strip():
#                     skills = [s.strip() for s in skills_raw.split(",") if s.strip()]
#                     add_team_member(active_id, mname.strip(), capacity, logged, skills)
#                     st.success(f"{mname} added")
#                     st.rerun()
#                 else:
#                     st.error("Name required")

#     current_team = get_team_members_with_db_id(active_id)
#     if not current_team:
#         st.info("No team members yet. Add one above.")
#     else:
#         for member in current_team:
#             with st.container(border=True):
#                 col1, col2 = st.columns([4, 1])
#                 with col1:
#                     pct = (member["logged_hrs_week"] / member["capacity_hrs_week"] * 100) if member["capacity_hrs_week"] else 0
#                     st.write(f"**{member['name']}**")
#                     st.caption(f"{member['logged_hrs_week']}/{member['capacity_hrs_week']} hrs ({pct:.0f}% utilized) | "
#                                f"Skills: {', '.join(member['skills']) or 'none listed'}")
#                 with col2:
#                     edit_key = f"edit_member_{member['db_id']}"
#                     if st.button("Edit", key=f"btn_{edit_key}"):
#                         st.session_state[edit_key] = not st.session_state.get(edit_key, False)

#                 if st.session_state.get(f"edit_member_{member['db_id']}", False):
#                     with st.form(f"edit_member_form_{member['db_id']}"):
#                         new_name = st.text_input("Name", value=member["name"])
#                         new_capacity = st.number_input("Weekly Capacity (hrs)", value=float(member["capacity_hrs_week"]))
#                         new_logged = st.number_input("Logged Hours", value=float(member["logged_hrs_week"]))
#                         new_skills = st.text_input("Skills", value=", ".join(member["skills"]))
#                         c1, c2 = st.columns(2)
#                         with c1:
#                             if st.form_submit_button("Save Changes"):
#                                 skills_list = [s.strip() for s in new_skills.split(",") if s.strip()]
#                                 update_team_member(member["db_id"], new_name, new_capacity, new_logged, skills_list)
#                                 st.session_state[f"edit_member_{member['db_id']}"] = False
#                                 st.rerun()
#                         with c2:
#                             if st.form_submit_button("Delete Member", type="secondary"):
#                                 delete_team_member(member["db_id"])
#                                 st.rerun()
# # ---------- BUDGET ----------
# elif page == "Budget":
#     st.subheader("Budget")
#     current_budget = get_latest_budget_entry(active_id)
#     if current_budget:
#         st.json(current_budget)
#     else:
#         st.info("No budget set yet.")

#     with st.form("budget_form"):
#         planned = st.number_input("Planned Spend ($)", value=current_budget["planned_spend"] if current_budget else 50000.0)
#         actual = st.number_input("Actual Spend ($)", value=current_budget["actual_spend"] if current_budget else 0.0)
#         pct_time = st.slider("% of Timeline Elapsed", 0, 100, int(current_budget["pct_time_elapsed"]) if current_budget else 0)
#         if st.form_submit_button("Save Budget"):
#             add_budget_entry(active_id, planned, actual, pct_time)
#             st.success("Budget saved")
#             st.rerun()

# # ---------- RUN ANALYSIS ----------
# elif page == "Run Analysis":
#     st.subheader("Run Analysis")
#     tasks = get_tasks(active_id)
#     team = get_team_members(active_id)
#     budget = get_latest_budget_entry(active_id)

#     if not tasks:
#         st.warning("Add at least one task first (see Tasks page).")
#     else:
#         if st.button("Run Analysis", type="primary"):
#             project_data = {"tasks": tasks, "team": team}
#             if budget:
#                 project_data["budget"] = budget

#             with st.spinner("Agents analyzing project..."):
#                 results, conflicts = orchestrate(project_data, active_id)

#             st.session_state["last_results"] = results  # moved here, right after results exists

#             st.markdown("### Results")
#             col1, col2, col3 = st.columns(3)
#             with col1:
#                 st.write("**Risk & Deadline**")
#                 for r in results:
#                     if r["agent"] == "risk_deadline":
#                         (st.error if r["finding"] == "high_risk" else st.success)(r["user_response"])
#             with col2:
#                 st.write("**Resource Usage**")
#                 for r in results:
#                     if r["agent"] == "resource_usage":
#                         (st.error if r["finding"] in ("overloaded", "severely_overloaded") else st.success)(r["user_response"])
#             with col3:
#                 st.write("**Budget**")
#                 for r in results:
#                     if r["agent"] == "budget_tracking":
#                         (st.error if r["finding"] == "over_budget" else st.success)(r["user_response"])

#             st.markdown("### Decision Engine: Conflicts & Recommendations")
#             if conflicts:
#                 for c in conflicts:
#                     st.warning(f"**{c['issue']}**")
#                     st.markdown(f"➜ {c['recommendation']}")
#             else:
#                 st.info("No conflicts detected.")

# # ---------- HISTORY ----------
# elif page == "History":
#     st.subheader("Short-Term Memory (this session)")
#     if "last_results" in st.session_state:
#         st.table(st.session_state["last_results"])
#     else:
#         st.info("Run an analysis this session to see short-term memory.")

#     st.subheader("Long-Term Memory (full project history)")
#     history = get_recent_findings(active_id, limit=20)
#     if history:
#         st.table(history)
#     else:
#         st.info("No history yet.")

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
    get_recent_findings, bulk_add_tasks, bulk_add_team_members
)
import json as json_lib
from orchestrator.orchestrator import orchestrate

init_db()

st.set_page_config(page_title="AI Project Decision Engine", layout="wide", page_icon="🧭")

st.markdown("""
<style>
    /* ── Global dark base ── */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: #0d0f1a !important;
        color: #e2e8f0 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    [data-testid="stAppViewContainer"] > .main {
        background-color: #0d0f1a;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111326 0%, #0d0f1a 100%) !important;
        border-right: 1px solid #1e2540 !important;
    }
    [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
    [data-testid="stSidebar"] .stRadio label,
    [data-testid="stSidebar"] .stCheckbox label { color: #94a3b8 !important; font-size: 0.88rem; }
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: #f1f5f9 !important; font-weight: 700; letter-spacing: 0.03em; }
    [data-testid="stSidebar"] hr { border-color: #1e2540 !important; }

    /* ── Main header ── */
    .main-header {
        background: linear-gradient(135deg, #0f172a 0%, #1a1f3c 40%, #0c1a35 100%);
        border: 1px solid #1e3a5f;
        padding: 1.8rem 2.4rem;
        border-radius: 14px;
        margin-bottom: 1.8rem;
        box-shadow: 0 4px 32px rgba(0,180,255,0.08), 0 1px 4px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }
    .main-header::before {
        content: "";
        position: absolute;
        top: -40px; right: -40px;
        width: 200px; height: 200px;
        background: radial-gradient(circle, rgba(0,180,255,0.12) 0%, transparent 70%);
        pointer-events: none;
    }
    .main-header h1 { color: #f8fafc; margin: 0; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.02em; }
    .main-header p  { color: #64b5d6; margin: 0.35rem 0 0 0; font-size: 0.92rem; letter-spacing: 0.01em; }

    /* ── Section header label ── */
    .section-label {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        margin: 1.6rem 0 1rem 0;
    }
    .section-label .icon {
        width: 30px; height: 30px;
        background: linear-gradient(135deg, #0ea5e9, #0284c7);
        border-radius: 7px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.9rem;
        flex-shrink: 0;
    }
    .section-label h3 {
        color: #f1f5f9 !important;
        margin: 0 !important;
        font-size: 1.05rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
        border: none !important;
        padding: 0 !important;
    }

    /* ── Metric cards ── */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, #141726, #1a1f38);
        border: 1px solid #1e2d4a;
        border-radius: 12px;
        padding: 18px 20px;
        box-shadow: 0 2px 16px rgba(0,0,0,0.35);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover {
        border-color: #00b4ff55;
        box-shadow: 0 4px 24px rgba(0,180,255,0.12);
    }
    div[data-testid="stMetric"] label {
        color: #64748b !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.10em !important;
        text-transform: uppercase !important;
    }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: #f1f5f9 !important;
        font-size: 1.6rem !important;
        font-weight: 700 !important;
    }

    /* ── Status badges ── */
    .badge {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        padding: 3px 10px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.04em;
    }
    .badge-green  { background: rgba(74,222,128,0.12); color: #4ade80; border: 1px solid rgba(74,222,128,0.25); }
    .badge-yellow { background: rgba(250,204,21,0.12); color: #fbbf24; border: 1px solid rgba(250,204,21,0.25); }
    .badge-red    { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }
    .badge-blue   { background: rgba(14,165,233,0.12); color: #38bdf8; border: 1px solid rgba(14,165,233,0.25); }
    .badge-gray   { background: rgba(100,116,139,0.12); color: #94a3b8; border: 1px solid rgba(100,116,139,0.25); }

    /* ── Task / member card ── */
    .data-card {
        background: #141726;
        border: 1px solid #1e2d4a;
        border-radius: 12px;
        padding: 16px 20px;
        margin-bottom: 10px;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    .data-card:hover {
        border-color: #1e3d5c;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    .data-card .card-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 6px;
    }
    .data-card .card-meta {
        font-size: 0.78rem;
        color: #475569;
        display: flex;
        flex-wrap: wrap;
        gap: 12px;
        align-items: center;
    }
    .card-meta-item {
        display: flex;
        align-items: center;
        gap: 4px;
    }
    .card-meta-item .label {
        color: #374151;
        text-transform: uppercase;
        font-size: 0.67rem;
        letter-spacing: 0.07em;
        font-weight: 600;
    }
    .card-meta-item .value { color: #94a3b8; }

    /* ── Progress bar custom ── */
    .progress-wrap {
        background: #1a1f38;
        border-radius: 100px;
        height: 6px;
        margin-top: 10px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        border-radius: 100px;
        transition: width 0.4s ease;
    }
    .progress-fill.low    { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }
    .progress-fill.mid    { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .progress-fill.high   { background: linear-gradient(90deg, #10b981, #34d399); }
    .progress-fill.danger { background: linear-gradient(90deg, #ef4444, #f87171); }

    /* ── Utilization bar ── */
    .util-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 8px;
        font-size: 0.78rem;
        color: #475569;
    }
    .util-bar-bg {
        flex: 1;
        background: #1a1f38;
        border-radius: 100px;
        height: 5px;
        overflow: hidden;
    }
    .util-bar-fill {
        height: 100%;
        border-radius: 100px;
    }

    /* ── Analysis result card ── */
    .result-card {
        background: #141726;
        border: 1px solid #1e2d4a;
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }
    .result-card .rc-title {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.10em;
        color: #475569;
        margin-bottom: 12px;
        padding-bottom: 10px;
        border-bottom: 1px solid #1e2d4a;
    }
    .result-card .rc-value {
        font-size: 0.92rem;
        color: #cbd5e1;
        line-height: 1.55;
    }

    /* ── Conflict card ── */
    .conflict-card {
        background: rgba(245,158,11,0.06);
        border: 1px solid rgba(245,158,11,0.25);
        border-left: 3px solid #f59e0b;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 12px;
    }
    .conflict-card .cc-issue { color: #fbbf24; font-weight: 700; font-size: 0.9rem; margin-bottom: 6px; }
    .conflict-card .cc-rec   { color: #94a3b8; font-size: 0.85rem; line-height: 1.5; }

    /* ── Info banner ── */
    .info-banner {
        background: rgba(14,165,233,0.06);
        border: 1px solid rgba(14,165,233,0.2);
        border-radius: 10px;
        padding: 14px 18px;
        color: #7dd3fc;
        font-size: 0.88rem;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* ── Warning banner ── */
    .warn-banner {
        background: rgba(245,158,11,0.07);
        border: 1px solid rgba(245,158,11,0.25);
        border-left: 3px solid #f59e0b;
        border-radius: 10px;
        padding: 12px 16px;
        color: #fbbf24;
        font-size: 0.85rem;
        margin-bottom: 8px;
    }

    /* ── Divider with label ── */
    .divider-label {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 1.6rem 0 1.2rem;
    }
    .divider-label span {
        color: #374151;
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.10em;
        white-space: nowrap;
    }
    .divider-label::before,
    .divider-label::after {
        content: "";
        flex: 1;
        height: 1px;
        background: #1e2d4a;
    }

    /* ── History table ── */
    .history-header {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1px;
        background: #1e2d4a;
        border-radius: 10px 10px 0 0;
        overflow: hidden;
        margin-bottom: 1px;
    }
    .history-header div {
        background: #0f1120;
        padding: 10px 14px;
        font-size: 0.70rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #475569;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        letter-spacing: 0.02em !important;
        padding: 0.45rem 1.1rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(14,165,233,0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #38bdf8, #0ea5e9) !important;
        box-shadow: 0 4px 16px rgba(14,165,233,0.45) !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button[kind="secondary"] {
        background: #1e2540 !important;
        box-shadow: none !important;
        color: #94a3b8 !important;
    }
    .stButton > button[kind="secondary"]:hover {
        background: #272f4a !important;
        color: #e2e8f0 !important;
        transform: none !important;
    }

    /* ── Form submit buttons ── */
    .stFormSubmitButton > button {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(14,165,233,0.3) !important;
    }
    .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #38bdf8, #0ea5e9) !important;
        box-shadow: 0 4px 16px rgba(14,165,233,0.45) !important;
    }

    /* ── Containers ── */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #141726 !important;
        border: 1px solid #1e2d4a !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
        transition: border-color 0.2s ease !important;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: #1e3d5c !important; }

    /* ── Inputs ── */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #141726 !important;
        border: 1px solid #1e2d4a !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
        font-size: 0.9rem !important;
    }
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #0ea5e9 !important;
        box-shadow: 0 0 0 2px rgba(14,165,233,0.2) !important;
    }

    /* ── Selectbox ── */
    .stSelectbox > div > div,
    div[data-baseweb="select"] > div {
        background-color: #141726 !important;
        border-color: #1e2d4a !important;
        color: #e2e8f0 !important;
        border-radius: 8px !important;
    }

    /* ── Slider ── */
    .stSlider [data-baseweb="slider"] div[role="slider"] {
        background-color: #0ea5e9 !important;
        border-color: #0ea5e9 !important;
    }

    /* ── Expander ── */
    details[data-testid="stExpander"] {
        background: #0f1120 !important;
        border: 1px solid #1e2d4a !important;
        border-radius: 10px !important;
        overflow: hidden !important;
    }
    details[data-testid="stExpander"] summary {
        color: #64748b !important;
        font-weight: 700 !important;
        font-size: 0.80rem !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        padding: 0.8rem 1rem !important;
    }
    details[data-testid="stExpander"] summary:hover { color: #e2e8f0 !important; background: #141726 !important; }

    /* ── Form container ── */
    div[data-testid="stForm"] {
        background: #0f1120 !important;
        border: 1px solid #1e2d4a !important;
        border-radius: 10px !important;
        padding: 1rem !important;
    }

    /* ── Native Streamlit alerts (hidden in favor of custom) ── */
    div[data-testid="stAlert"] { border-radius: 10px !important; border-left-width: 4px !important; font-size: 0.88rem !important; }

    /* ── Headings ── */
    h2, h3 { color: #f1f5f9 !important; font-weight: 700 !important; letter-spacing: -0.01em !important; }
    h2 { font-size: 1.15rem !important; border-bottom: 1px solid #1e2d4a; padding-bottom: 0.5rem; margin-bottom: 1rem !important; }

    /* ── Captions ── */
    .stCaptionContainer, small { color: #475569 !important; font-size: 0.82rem !important; }

    /* ── HR ── */
    hr { border-color: #1e2d4a !important; }

    /* ── Native table ── */
    div[data-testid="stTable"] table { background-color: #141726 !important; border-radius: 10px !important; overflow: hidden !important; border: 1px solid #1e2d4a !important; }
    div[data-testid="stTable"] th { background-color: #0f1120 !important; color: #475569 !important; font-size: 0.72rem !important; font-weight: 700 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; border-bottom: 1px solid #1e2d4a !important; padding: 10px 14px !important; }
    div[data-testid="stTable"] td { color: #cbd5e1 !important; border-bottom: 1px solid #1a1f38 !important; padding: 10px 14px !important; font-size: 0.88rem !important; }
    div[data-testid="stTable"] tr:hover td { background: #1a1f38 !important; }

    /* ── JSON ── */
    div[data-testid="stJson"] { background: #0f1120 !important; border: 1px solid #1e2d4a !important; border-radius: 10px !important; }

    /* ── Date input ── */
    .stDateInput > div > div > input { background-color: #141726 !important; border: 1px solid #1e2d4a !important; color: #e2e8f0 !important; border-radius: 8px !important; }

    /* ── Sidebar success ── */
    div[data-testid="stSidebar"] .stSuccess { background: #0c1f1a !important; border: 1px solid #134e2e !important; border-radius: 8px !important; color: #4ade80 !important; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: #0d0f1a; }
    ::-webkit-scrollbar-thumb { background: #1e2d4a; border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: #0ea5e9; }

    /* ── Spinner ── */
    .stSpinner > div { border-top-color: #0ea5e9 !important; }

    /* ── Empty state ── */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        background: #0f1120;
        border: 1px dashed #1e2d4a;
        border-radius: 14px;
        color: #374151;
    }
    .empty-state .es-icon { font-size: 2.5rem; margin-bottom: 12px; }
    .empty-state .es-title { color: #475569; font-size: 0.95rem; font-weight: 600; margin-bottom: 4px; }
    .empty-state .es-sub   { color: #374151; font-size: 0.82rem; }

    /* ── Budget display card ── */
    .budget-stat {
        background: #141726;
        border: 1px solid #1e2d4a;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    .budget-stat .bs-label { font-size: 0.70rem; text-transform: uppercase; letter-spacing: 0.10em; font-weight: 700; color: #475569; }
    .budget-stat .bs-value { font-size: 1.5rem; font-weight: 800; color: #f1f5f9; margin: 6px 0; }
    .budget-stat .bs-sub   { font-size: 0.78rem; color: #64748b; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
st.sidebar.markdown("""
<div style="padding: 8px 0 4px 0;">
  <div style="font-size:0.70rem;text-transform:uppercase;letter-spacing:0.12em;color:#374151;font-weight:700;margin-bottom:6px;">Platform</div>
  <div style="font-size:1.05rem;font-weight:800;color:#f1f5f9;letter-spacing:-0.01em;">AI Decision Engine</div>
</div>
""", unsafe_allow_html=True)

mock_mode = st.sidebar.checkbox("Mock mode (no API calls)", value=True)
os.environ["USE_MOCK_AGENT"] = "1" if mock_mode else "0"

st.sidebar.markdown("---")
st.sidebar.markdown('<div style="font-size:0.70rem;text-transform:uppercase;letter-spacing:0.12em;color:#374151;font-weight:700;margin-bottom:8px;">Projects</div>', unsafe_allow_html=True)

existing_projects = list_projects()
project_names = {p["name"]: p["id"] for p in existing_projects}

action = st.sidebar.radio("Action", ["Open existing", "Create new"], label_visibility="collapsed")
if action == "Create new":
    st.session_state.pop("active_project_id", None)
    st.session_state.pop("active_project_name", None)

    new_name = st.sidebar.text_input("New project name")
    new_start = st.sidebar.date_input("Project start date")
    new_end = st.sidebar.date_input("Project end date")
    if st.sidebar.button("Create Project", type="primary"):
        if new_name.strip():
            pid = create_project(new_name.strip(), str(new_start), str(new_end))
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

active_id   = st.session_state.get("active_project_id")
active_name = st.session_state.get("active_project_name")

if not active_id:
    st.markdown("""
    <div class="main-header">
        <h1>🧭 AI Agent Coordination &amp; Decision Engine</h1>
        <p>Multi-agent risk, resource, and budget analysis for project managers</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="info-banner">
        <span>ℹ️</span>
        <span>Create or open a project from the sidebar to get started.</span>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

st.sidebar.markdown("---")
st.sidebar.success(f"Active: **{active_name}**")

# ──────────────────────────────────────────────────────────────
# MAIN HEADER
# ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="main-header">
    <h1>🧭 {active_name}</h1>
    <p>AI Agent Coordination &amp; Decision Engine</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown('<div style="font-size:0.70rem;text-transform:uppercase;letter-spacing:0.12em;color:#374151;font-weight:700;margin:12px 0 6px 0;">Navigation</div>', unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ["Overview", "Tasks", "Team", "Budget", "Run Analysis", "History"], label_visibility="collapsed")

# ──────────────────────────────────────────────────────────────
# OVERVIEW
# ──────────────────────────────────────────────────────────────
if page == "Overview":
    summary    = get_project_summary(active_id)
    budget_data = get_latest_budget_entry(active_id)

    from db.repository import get_project_dates
    from tools.budget_tools import calculate_pct_time_elapsed, check_budget_status

    dates = get_project_dates(active_id)
    live_pct_time = 0
    if dates and dates["start_date"] and dates["end_date"]:
        live_pct_time = calculate_pct_time_elapsed(dates["start_date"], dates["end_date"])

    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tasks",    summary["task_count"])
    col2.metric("Team Members",   summary["team_count"])

    budget_status = "Not Set"
    if budget_data:
        result = check_budget_status(budget_data["planned_spend"], budget_data["actual_spend"], live_pct_time)
        if result.startswith("over_budget"):
            budget_status = "⚠️ Over Budget"
        elif result.startswith("at_risk"):
            budget_status = "🟡 At Risk"
        else:
            budget_status = "✅ On Budget"
    col3.metric("Budget Status",  budget_status)
    col4.metric("Last Analysis",  summary["last_analysis"].strftime("%b %d, %H:%M") if summary["last_analysis"] else "Never")

    # Budget visual strip
    if budget_data:
        st.markdown('<div class="divider-label"><span>Budget Snapshot</span></div>', unsafe_allow_html=True)
        b1, b2, b3 = st.columns(3)
        with b1:
            st.markdown(f"""
            <div class="budget-stat">
                <div class="bs-label">Planned Spend</div>
                <div class="bs-value">₹{budget_data['planned_spend']:,.0f}</div>
                <div class="bs-sub">Total budget</div>
            </div>""", unsafe_allow_html=True)
        with b2:
            st.markdown(f"""
            <div class="budget-stat">
                <div class="bs-label">Actual Spend</div>
                <div class="bs-value">₹{budget_data['actual_spend']:,.0f}</div>
                <div class="bs-sub">Spent to date</div>
            </div>""", unsafe_allow_html=True)
        with b3:
            spend_pct = (budget_data['actual_spend'] / budget_data['planned_spend'] * 100) if budget_data['planned_spend'] else 0
            color = "#ef4444" if spend_pct > live_pct_time + 10 else "#f59e0b" if spend_pct > live_pct_time else "#10b981"
            st.markdown(f"""
            <div class="budget-stat">
                <div class="bs-label">Timeline Elapsed</div>
                <div class="bs-value" style="color:{color};">{live_pct_time:.1f}%</div>
                <div class="bs-sub">{spend_pct:.1f}% of budget used</div>
            </div>""", unsafe_allow_html=True)

    # Validation warnings
    tasks     = get_tasks(active_id)
    team      = get_team_members(active_id)
    team_names = {t["name"] for t in team}
    task_ids   = {t["id"] for t in tasks}

    warnings = []
    for task in tasks:
        if task["assigned_to"] and task["assigned_to"] not in team_names:
            warnings.append(f"Task <b>{task['id']}</b> is assigned to <b>'{task['assigned_to']}'</b> — not found in the team roster.")
        for dep in task["depends_on"]:
            if dep not in task_ids:
                warnings.append(f"Task <b>{task['id']}</b> depends on <b>'{dep}'</b> — this task does not exist.")

    if warnings:
        st.markdown('<div class="divider-label"><span>Data Issues</span></div>', unsafe_allow_html=True)
        for w in warnings:
            st.markdown(f'<div class="warn-banner">⚠ {w}</div>', unsafe_allow_html=True)

    st.markdown('<div class="divider-label"><span>Getting Started</span></div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-banner">
        <span>💡</span>
        <span>Use the sidebar to manage tasks, team members, budget, and run AI analysis.</span>
    </div>
    """, unsafe_allow_html=True)
# ──────────────────────────────────────────────────────────────
# TASKS
# ──────────────────────────────────────────────────────────────
elif page == "Tasks":
    st.markdown('<div class="section-label"><div class="icon">📋</div><h3>Task Management</h3></div>', unsafe_allow_html=True)

    with st.expander("＋  Add New Task"):
        with st.form("task_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                tid  = st.text_input("Task ID", placeholder="e.g. T1")
                tname = st.text_input("Task Name", placeholder="e.g. Design wireframes")
            with c2:
                deadline    = st.date_input("Deadline")
                assigned_to = st.text_input("Assigned To", placeholder="Team member name")
            progress       = st.slider("Progress %", 0, 100, 0)
            depends_on_raw = st.text_input("Depends On", placeholder="Comma-separated task IDs, e.g. T1, T2")
            if st.form_submit_button("Add Task"):
                if tid.strip() and tname.strip():
                    depends_on = [d.strip() for d in depends_on_raw.split(",") if d.strip()]
                    add_task(active_id, tid.strip(), tname.strip(), progress, str(deadline), depends_on, assigned_to.strip())
                    st.success(f"Task **{tid}** added successfully.")
                    st.rerun()
                else:
                    st.error("Task ID and Name are required.")

    with st.expander("📥  Bulk Import Tasks (upload JSON)"):
        st.caption('Upload a JSON file: a list of objects like '
                   '{"id": "T1", "name": "...", "progress_pct": 0, "planned_end": "YYYY-MM-DD", "depends_on": [], "assigned_to": "..."}')
        uploaded = st.file_uploader("Choose a JSON file", type=["json"], key="task_upload")
        if uploaded:
            try:
                data = json_lib.load(uploaded)
                task_list = data.get("tasks", data) if isinstance(data, dict) else data
                st.write(f"Found {len(task_list)} task(s) in file. Preview:")
                st.json(task_list[:3])
                if st.button("Import These Tasks"):
                    count = bulk_add_tasks(active_id, task_list)
                    st.success(f"Imported {count} tasks")
                    st.rerun()
            except Exception as e:
                st.error(f"Could not parse file: {e}")

    current_tasks = get_tasks_with_db_id(active_id)
    st.markdown('<div class="divider-label"><span>All Tasks</span></div>', unsafe_allow_html=True)

    if not current_tasks:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">📭</div>
            <div class="es-title">No tasks yet</div>
            <div class="es-sub">Expand the panel above to add your first task.</div>
        </div>""", unsafe_allow_html=True)
    else:
        for task in current_tasks:
            pct = int(task['progress_pct'])
            if pct >= 80:   bar_cls = "high"
            elif pct >= 40: bar_cls = "mid"
            else:           bar_cls = "low"

            dep_str    = ", ".join(task['depends_on']) if task['depends_on'] else "—"
            assign_str = task['assigned_to'] or "—"

            with st.container(border=True):
                left, right = st.columns([5, 1])
                with left:
                    st.markdown(f"""
                    <div class="card-title">{task['id']} &nbsp;·&nbsp; {task['name']}</div>
                    <div class="card-meta">
                        <div class="card-meta-item"><span class="label">Deadline</span><span class="value">{task['planned_end']}</span></div>
                        <div class="card-meta-item"><span class="label">Assigned</span><span class="value">{assign_str}</span></div>
                        <div class="card-meta-item"><span class="label">Depends on</span><span class="value">{dep_str}</span></div>
                        <div class="card-meta-item"><span class="label">Progress</span><span class="value">{pct}%</span></div>
                    </div>
                    <div class="progress-wrap"><div class="progress-fill {bar_cls}" style="width:{pct}%;"></div></div>
                    """, unsafe_allow_html=True)
                with right:
                    edit_key = f"edit_task_{task['db_id']}"
                    if st.button("Edit", key=f"btn_{edit_key}"):
                        st.session_state[edit_key] = not st.session_state.get(edit_key, False)

                if st.session_state.get(f"edit_task_{task['db_id']}", False):
                    with st.form(f"edit_form_{task['db_id']}"):
                        e1, e2 = st.columns(2)
                        with e1:
                            new_name     = st.text_input("Name",     value=task["name"])
                            new_deadline = st.text_input("Deadline (YYYY-MM-DD)", value=task["planned_end"])
                        with e2:
                            new_assigned = st.text_input("Assigned To", value=task["assigned_to"] or "")
                            new_depends  = st.text_input("Depends On",  value=", ".join(task["depends_on"]))
                        new_progress = st.slider("Progress %", 0, 100, int(task["progress_pct"]))
                        s1, s2 = st.columns(2)
                        with s1:
                            if st.form_submit_button("Save Changes"):
                                depends_list = [d.strip() for d in new_depends.split(",") if d.strip()]
                                update_task(task["db_id"], new_name, new_progress, new_deadline, depends_list, new_assigned)
                                st.session_state[f"edit_task_{task['db_id']}"] = False
                                st.rerun()
                        with s2:
                            if st.form_submit_button("Delete Task", type="secondary"):
                                delete_task(task["db_id"])
                                st.rerun()
# ──────────────────────────────────────────────────────────────
# TEAM
# ──────────────────────────────────────────────────────────────
elif page == "Team":
    st.markdown('<div class="section-label"><div class="icon">👥</div><h3>Team Roster</h3></div>', unsafe_allow_html=True)

    with st.expander("＋  Add New Team Member"):
        with st.form("member_form", clear_on_submit=True):
            c1, c2 = st.columns(2)
            with c1:
                mname    = st.text_input("Full Name", placeholder="e.g. Alice Johnson")
                capacity = st.number_input("Weekly Capacity (hrs)", value=40.0)
            with c2:
                logged     = st.number_input("Logged Hours This Week", value=0.0)
                skills_raw = st.text_input("Skills", placeholder="e.g. Python, Design, DevOps")
            if st.form_submit_button("Add Team Member"):
                if mname.strip():
                    skills = [s.strip() for s in skills_raw.split(",") if s.strip()]
                    add_team_member(active_id, mname.strip(), capacity, logged, skills)
                    st.success(f"**{mname}** added to the team.")
                    st.rerun()
                else:
                    st.error("Name is required.")
    with st.expander("Bulk Import Team (upload JSON)"):
        st.caption('Upload a JSON file: a list of objects like '
                   '{"name": "...", "capacity_hrs_week": 40, "logged_hrs_week": 0, "skills": []}')
        uploaded = st.file_uploader("Choose a JSON file", type=["json"], key="team_upload")
        if uploaded:
            try:
                data = json_lib.load(uploaded)
                member_list = data.get("team", data) if isinstance(data, dict) else data
                st.write(f"Found {len(member_list)} member(s) in file. Preview:")
                st.json(member_list[:3])
                if st.button("Import These Team Members"):
                    count = bulk_add_team_members(active_id, member_list)
                    st.success(f"Imported {count} team members")
                    st.rerun()
            except Exception as e:
                st.error(f"Could not parse file: {e}")

    current_team = get_team_members_with_db_id(active_id)
    st.markdown('<div class="divider-label"><span>Team Members</span></div>', unsafe_allow_html=True)

    if not current_team:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">🧑‍💼</div>
            <div class="es-title">No team members yet</div>
            <div class="es-sub">Expand the panel above to add your first team member.</div>
        </div>""", unsafe_allow_html=True)
    else:
        for member in current_team:
            cap  = member["capacity_hrs_week"] or 1
            log  = member["logged_hrs_week"]
            pct  = min((log / cap * 100), 100)
            if pct >= 90:   util_color, util_label = "#ef4444", "Overloaded"
            elif pct >= 70: util_color, util_label = "#f59e0b", "High"
            elif pct >= 40: util_color, util_label = "#0ea5e9", "Moderate"
            else:            util_color, util_label = "#10b981", "Available"

            skills_str = ", ".join(member["skills"]) if member["skills"] else "—"

            with st.container(border=True):
                left, right = st.columns([5, 1])
                with left:
                    st.markdown(f"""
                    <div class="card-title">{member['name']}
                        <span class="badge badge-blue" style="margin-left:10px;font-size:0.68rem;">{util_label}</span>
                    </div>
                    <div class="card-meta" style="margin-top:4px;">
                        <div class="card-meta-item"><span class="label">Logged</span><span class="value">{log} / {cap} hrs</span></div>
                        <div class="card-meta-item"><span class="label">Utilization</span><span class="value">{pct:.0f}%</span></div>
                        <div class="card-meta-item"><span class="label">Skills</span><span class="value">{skills_str}</span></div>
                    </div>
                    <div class="util-row">
                        <div class="util-bar-bg"><div class="util-bar-fill" style="width:{pct}%;background:{util_color};"></div></div>
                        <span style="color:{util_color};font-weight:700;min-width:36px;">{pct:.0f}%</span>
                    </div>
                    """, unsafe_allow_html=True)
                with right:
                    edit_key = f"edit_member_{member['db_id']}"
                    if st.button("Edit", key=f"btn_{edit_key}"):
                        st.session_state[edit_key] = not st.session_state.get(edit_key, False)

                if st.session_state.get(f"edit_member_{member['db_id']}", False):
                    with st.form(f"edit_member_form_{member['db_id']}"):
                        e1, e2 = st.columns(2)
                        with e1:
                            new_name     = st.text_input("Name",             value=member["name"])
                            new_capacity = st.number_input("Weekly Capacity (hrs)", value=float(member["capacity_hrs_week"]))
                        with e2:
                            new_logged = st.number_input("Logged Hours", value=float(member["logged_hrs_week"]))
                            new_skills = st.text_input("Skills",         value=", ".join(member["skills"]))
                        s1, s2 = st.columns(2)
                        with s1:
                            if st.form_submit_button("Save Changes"):
                                skills_list = [s.strip() for s in new_skills.split(",") if s.strip()]
                                update_team_member(member["db_id"], new_name, new_capacity, new_logged, skills_list)
                                st.session_state[f"edit_member_{member['db_id']}"] = False
                                st.rerun()
                        with s2:
                            if st.form_submit_button("Delete Member", type="secondary"):
                                delete_team_member(member["db_id"])
                                st.rerun()

# ──────────────────────────────────────────────────────────────
# BUDGET
# ──────────────────────────────────────────────────────────────
elif page == "Budget":
    st.subheader("Budget")

    from db.repository import get_project_dates, update_project_dates
    from tools.budget_tools import calculate_pct_time_elapsed

    dates = get_project_dates(active_id)
    if dates and dates["start_date"] and dates["end_date"]:
        pct_time = calculate_pct_time_elapsed(dates["start_date"], dates["end_date"])
        st.info(f"Timeline: {dates['start_date']} to {dates['end_date']} — **{pct_time:.1f}%** elapsed (calculated automatically)")
    else:
        st.warning("This project has no start/end date set. Timeline % cannot be calculated automatically.")
        pct_time = 0.0

    with st.expander("Edit Project Timeline (e.g. if deadline is extended)"):
        with st.form("edit_dates_form"):
            import datetime
            current_start = datetime.date.fromisoformat(dates["start_date"]) if dates and dates["start_date"] else datetime.date.today()
            current_end = datetime.date.fromisoformat(dates["end_date"]) if dates and dates["end_date"] else datetime.date.today()

            new_start = st.date_input("Start Date", value=current_start)
            new_end = st.date_input("End Date", value=current_end)
            if st.form_submit_button("Update Timeline"):
                if new_end > new_start:
                    update_project_dates(active_id, str(new_start), str(new_end))
                    st.success("Project timeline updated")
                    st.rerun()
                else:
                    st.error("End date must be after start date")

    current_budget = get_latest_budget_entry(active_id)
    if current_budget:
        st.json(current_budget)
    else:
        st.info("No budget set yet.")

    with st.form("budget_form"):
        planned = st.number_input("Planned Spend ($)", value=current_budget["planned_spend"] if current_budget else 50000.0)
        actual = st.number_input("Actual Spend ($)", value=current_budget["actual_spend"] if current_budget else 0.0)
        st.caption(f"Timeline elapsed: {pct_time:.1f}% (auto-calculated from project dates)")
        if st.form_submit_button("Save Budget"):
            add_budget_entry(active_id, planned, actual, pct_time)
            st.success("Budget saved")
            st.rerun()
# ──────────────────────────────────────────────────────────────
# RUN ANALYSIS
# ──────────────────────────────────────────────────────────────
elif page == "Run Analysis":
    st.markdown('<div class="section-label"><div class="icon">🤖</div><h3>AI Agent Analysis</h3></div>', unsafe_allow_html=True)

    tasks  = get_tasks(active_id)
    team   = get_team_members(active_id)
    budget = get_latest_budget_entry(active_id)

    # Always use the LIVE, auto-calculated timeline percentage instead of
    # whatever was last saved in the budget entry — avoids stale data.
    from db.repository import get_project_dates
    from tools.budget_tools import calculate_pct_time_elapsed

    dates = get_project_dates(active_id)
    if budget and dates and dates["start_date"] and dates["end_date"]:
        budget["pct_time_elapsed"] = calculate_pct_time_elapsed(dates["start_date"], dates["end_date"])

    if not tasks:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">📋</div>
            <div class="es-title">No tasks to analyze</div>
            <div class="es-sub">Add at least one task on the Tasks page before running analysis.</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="info-banner" style="margin-bottom:1.2rem;">
            <span>🔍</span>
            <span>Ready to analyze <b>{len(tasks)} task(s)</b> across <b>{len(team)} team member(s)</b>. Click below to run all agents.</span>
        </div>""", unsafe_allow_html=True)

        if st.button("▶  Run Analysis", type="primary"):
            project_data = {"tasks": tasks, "team": team}
            if budget:
                project_data["budget"] = budget

            with st.spinner("Agents analyzing project..."):
                results, conflicts = orchestrate(project_data, active_id)
            st.session_state["last_results"] = results

            st.markdown('<div class="divider-label"><span>Agent Results</span></div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)

            with col1:
                st.markdown('<div class="result-card"><div class="rc-title">⚠ Risk &amp; Deadline</div>', unsafe_allow_html=True)
                for r in results:
                    if r["agent"] == "risk_deadline":
                        is_bad = r["finding"] == "high_risk"
                        color  = "#f87171" if is_bad else "#4ade80"
                        icon   = "🔴" if is_bad else "🟢"
                        st.markdown(f'<div class="rc-value" style="color:{color};">{icon} {r["user_response"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                st.markdown('<div class="result-card"><div class="rc-title">👤 Resource Usage</div>', unsafe_allow_html=True)
                for r in results:
                    if r["agent"] == "resource_usage":
                        is_bad = r["finding"] in ("overloaded", "severely_overloaded")
                        color  = "#f87171" if is_bad else "#4ade80"
                        icon   = "🔴" if is_bad else "🟢"
                        st.markdown(f'<div class="rc-value" style="color:{color};">{icon} {r["user_response"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col3:
                st.markdown('<div class="result-card"><div class="rc-title">💰 Budget</div>', unsafe_allow_html=True)
                for r in results:
                    if r["agent"] == "budget_tracking":
                        is_bad = r["finding"] == "over_budget"
                        color  = "#f87171" if is_bad else "#4ade80"
                        icon   = "🔴" if is_bad else "🟢"
                        st.markdown(f'<div class="rc-value" style="color:{color};">{icon} {r["user_response"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            col4, col5 = st.columns(2)

            with col4:
                st.markdown('<div class="result-card"><div class="rc-title">🏃 Scrum Master</div>', unsafe_allow_html=True)
                for r in results:
                    if r["agent"] == "scrum_master":
                        is_bad = r["finding"] == "impediments_found"
                        color  = "#f87171" if is_bad else "#4ade80"
                        icon   = "🔴" if is_bad else "🟢"
                        st.markdown(f'<div class="rc-value" style="color:{color};">{icon} {r["user_response"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col5:
                st.markdown('<div class="result-card"><div class="rc-title">⚖ Project Distribution</div>', unsafe_allow_html=True)
                for r in results:
                    if r["agent"] == "project_distribution":
                        is_bad = r["finding"] == "imbalanced"
                        color  = "#f87171" if is_bad else "#4ade80"
                        icon   = "🔴" if is_bad else "🟢"
                        st.markdown(f'<div class="rc-value" style="color:{color};">{icon} {r["user_response"]}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown('<div class="divider-label"><span>Decision Engine · Conflicts &amp; Recommendations</span></div>', unsafe_allow_html=True)
            if conflicts:
                for c in conflicts:
                    st.markdown(f"""
                    <div class="conflict-card">
                        <div class="cc-issue">⚡ {c['issue']}</div>
                        <div class="cc-rec">➜ {c['recommendation']}</div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="info-banner">
                    <span>✅</span>
                    <span>No conflicts detected — all agents report healthy project status.</span>
                </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# HISTORY
# ──────────────────────────────────────────────────────────────
elif page == "History":
    st.markdown('<div class="section-label"><div class="icon">🕑</div><h3>Analysis History</h3></div>', unsafe_allow_html=True)

    st.markdown('<div class="divider-label"><span>Short-Term Memory · This Session</span></div>', unsafe_allow_html=True)
    if "last_results" in st.session_state:
        st.table(st.session_state["last_results"])
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">🧠</div>
            <div class="es-title">No session data yet</div>
            <div class="es-sub">Run an analysis to populate short-term memory.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider-label"><span>Long-Term Memory · Full Project History</span></div>', unsafe_allow_html=True)
    history = get_recent_findings(active_id, limit=20)
    if history:
        st.table(history)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">📂</div>
            <div class="es-title">No history yet</div>
            <div class="es-sub">Previous analysis runs will appear here.</div>
        </div>""", unsafe_allow_html=True)

