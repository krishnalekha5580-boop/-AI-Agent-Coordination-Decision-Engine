# import streamlit as st
# import os
# import sys

# sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# from db.session import init_db
# from db.repository import (
#     create_user, verify_user,
#     create_project, list_projects, get_project_summary,
#     add_team_member, get_team_members, get_team_members_with_db_id, update_team_member, delete_team_member,
#     add_task, get_tasks, get_tasks_with_db_id, update_task, delete_task,
#     add_budget_entry, get_latest_budget_entry,
#     get_recent_findings, bulk_add_tasks, bulk_add_team_members
# )
# import json as json_lib
# from orchestrator.orchestrator import orchestrate

# init_db()

# st.set_page_config(page_title="AI Project Decision Engine", layout="wide", page_icon="🧭")

# st.markdown("""
# <style>
#     /* ── Global dark base ── */
#     html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
#         background-color: #0d0f1a !important;
#         color: #e2e8f0 !important;
#         font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
#     }
#     [data-testid="stAppViewContainer"] > .main {
#         background-color: #0d0f1a;
#     }

#     /* ── Sidebar ── */
#     [data-testid="stSidebar"] {
#         background: linear-gradient(180deg, #111326 0%, #0d0f1a 100%) !important;
#         border-right: 1px solid #1e2540 !important;
#     }
#     [data-testid="stSidebar"] * { color: #cbd5e1 !important; }
#     [data-testid="stSidebar"] .stRadio label,
#     [data-testid="stSidebar"] .stCheckbox label { color: #94a3b8 !important; font-size: 0.88rem; }
#     [data-testid="stSidebar"] h2,
#     [data-testid="stSidebar"] h3 { color: #f1f5f9 !important; font-weight: 700; letter-spacing: 0.03em; }
#     [data-testid="stSidebar"] hr { border-color: #1e2540 !important; }

#     /* ── Main header ── */
#     .main-header {
#         background: linear-gradient(135deg, #0f172a 0%, #1a1f3c 40%, #0c1a35 100%);
#         border: 1px solid #1e3a5f;
#         padding: 1.8rem 2.4rem;
#         border-radius: 14px;
#         margin-bottom: 1.8rem;
#         box-shadow: 0 4px 32px rgba(0,180,255,0.08), 0 1px 4px rgba(0,0,0,0.5);
#         position: relative;
#         overflow: hidden;
#     }
#     .main-header::before {
#         content: "";
#         position: absolute;
#         top: -40px; right: -40px;
#         width: 200px; height: 200px;
#         background: radial-gradient(circle, rgba(0,180,255,0.12) 0%, transparent 70%);
#         pointer-events: none;
#     }
#     .main-header h1 { color: #f8fafc; margin: 0; font-size: 1.75rem; font-weight: 800; letter-spacing: -0.02em; }
#     .main-header p  { color: #64b5d6; margin: 0.35rem 0 0 0; font-size: 0.92rem; letter-spacing: 0.01em; }

#     /* ── Section header label ── */
#     .section-label {
#         display: flex;
#         align-items: center;
#         gap: 0.6rem;
#         margin: 1.6rem 0 1rem 0;
#     }
#     .section-label .icon {
#         width: 30px; height: 30px;
#         background: linear-gradient(135deg, #0ea5e9, #0284c7);
#         border-radius: 7px;
#         display: flex; align-items: center; justify-content: center;
#         font-size: 0.9rem;
#         flex-shrink: 0;
#     }
#     .section-label h3 {
#         color: #f1f5f9 !important;
#         margin: 0 !important;
#         font-size: 1.05rem !important;
#         font-weight: 700 !important;
#         letter-spacing: -0.01em !important;
#         border: none !important;
#         padding: 0 !important;
#     }

#     /* ── Metric cards ── */
#     div[data-testid="stMetric"] {
#         background: linear-gradient(135deg, #141726, #1a1f38);
#         border: 1px solid #1e2d4a;
#         border-radius: 12px;
#         padding: 18px 20px;
#         box-shadow: 0 2px 16px rgba(0,0,0,0.35);
#         transition: border-color 0.2s ease, box-shadow 0.2s ease;
#     }
#     div[data-testid="stMetric"]:hover {
#         border-color: #00b4ff55;
#         box-shadow: 0 4px 24px rgba(0,180,255,0.12);
#     }
#     div[data-testid="stMetric"] label {
#         color: #64748b !important;
#         font-size: 0.72rem !important;
#         font-weight: 700 !important;
#         letter-spacing: 0.10em !important;
#         text-transform: uppercase !important;
#     }
#     div[data-testid="stMetric"] [data-testid="stMetricValue"] {
#         color: #f1f5f9 !important;
#         font-size: 1.6rem !important;
#         font-weight: 700 !important;
#     }

#     /* ── Status badges ── */
#     .badge {
#         display: inline-flex;
#         align-items: center;
#         gap: 5px;
#         padding: 3px 10px;
#         border-radius: 20px;
#         font-size: 0.75rem;
#         font-weight: 700;
#         letter-spacing: 0.04em;
#     }
#     .badge-green  { background: rgba(74,222,128,0.12); color: #4ade80; border: 1px solid rgba(74,222,128,0.25); }
#     .badge-yellow { background: rgba(250,204,21,0.12); color: #fbbf24; border: 1px solid rgba(250,204,21,0.25); }
#     .badge-red    { background: rgba(248,113,113,0.12); color: #f87171; border: 1px solid rgba(248,113,113,0.25); }
#     .badge-blue   { background: rgba(14,165,233,0.12); color: #38bdf8; border: 1px solid rgba(14,165,233,0.25); }
#     .badge-gray   { background: rgba(100,116,139,0.12); color: #94a3b8; border: 1px solid rgba(100,116,139,0.25); }

#     /* ── Task / member card ── */
#     .data-card {
#         background: #141726;
#         border: 1px solid #1e2d4a;
#         border-radius: 12px;
#         padding: 16px 20px;
#         margin-bottom: 10px;
#         transition: border-color 0.2s ease, box-shadow 0.2s ease;
#     }
#     .data-card:hover {
#         border-color: #1e3d5c;
#         box-shadow: 0 4px 20px rgba(0,0,0,0.3);
#     }
#     .data-card .card-title {
#         font-size: 0.95rem;
#         font-weight: 700;
#         color: #f1f5f9;
#         margin-bottom: 6px;
#     }
#     .data-card .card-meta {
#         font-size: 0.78rem;
#         color: #475569;
#         display: flex;
#         flex-wrap: wrap;
#         gap: 12px;
#         align-items: center;
#     }
#     .card-meta-item {
#         display: flex;
#         align-items: center;
#         gap: 4px;
#     }
#     .card-meta-item .label {
#         color: #374151;
#         text-transform: uppercase;
#         font-size: 0.67rem;
#         letter-spacing: 0.07em;
#         font-weight: 600;
#     }
#     .card-meta-item .value { color: #94a3b8; }

#     /* ── Progress bar custom ── */
#     .progress-wrap {
#         background: #1a1f38;
#         border-radius: 100px;
#         height: 6px;
#         margin-top: 10px;
#         overflow: hidden;
#     }
#     .progress-fill {
#         height: 100%;
#         border-radius: 100px;
#         transition: width 0.4s ease;
#     }
#     .progress-fill.low    { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }
#     .progress-fill.mid    { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
#     .progress-fill.high   { background: linear-gradient(90deg, #10b981, #34d399); }
#     .progress-fill.danger { background: linear-gradient(90deg, #ef4444, #f87171); }

#     /* ── Utilization bar ── */
#     .util-row {
#         display: flex;
#         align-items: center;
#         gap: 10px;
#         margin-top: 8px;
#         font-size: 0.78rem;
#         color: #475569;
#     }
#     .util-bar-bg {
#         flex: 1;
#         background: #1a1f38;
#         border-radius: 100px;
#         height: 5px;
#         overflow: hidden;
#     }
#     .util-bar-fill {
#         height: 100%;
#         border-radius: 100px;
#     }

#     /* ── Analysis result card ── */
#     .result-card {
#         background: #141726;
#         border: 1px solid #1e2d4a;
#         border-radius: 12px;
#         padding: 20px;
#         height: 100%;
#     }
#     .result-card .rc-title {
#         font-size: 0.72rem;
#         font-weight: 700;
#         text-transform: uppercase;
#         letter-spacing: 0.10em;
#         color: #475569;
#         margin-bottom: 12px;
#         padding-bottom: 10px;
#         border-bottom: 1px solid #1e2d4a;
#     }
#     .result-card .rc-value {
#         font-size: 0.92rem;
#         color: #cbd5e1;
#         line-height: 1.55;
#     }

#     /* ── Conflict card ── */
#     .conflict-card {
#         background: rgba(245,158,11,0.06);
#         border: 1px solid rgba(245,158,11,0.25);
#         border-left: 3px solid #f59e0b;
#         border-radius: 10px;
#         padding: 14px 18px;
#         margin-bottom: 12px;
#     }
#     .conflict-card .cc-issue { color: #fbbf24; font-weight: 700; font-size: 0.9rem; margin-bottom: 6px; }
#     .conflict-card .cc-rec   { color: #94a3b8; font-size: 0.85rem; line-height: 1.5; }

#     /* ── Info banner ── */
#     .info-banner {
#         background: rgba(14,165,233,0.06);
#         border: 1px solid rgba(14,165,233,0.2);
#         border-radius: 10px;
#         padding: 14px 18px;
#         color: #7dd3fc;
#         font-size: 0.88rem;
#         display: flex;
#         align-items: center;
#         gap: 10px;
#     }

#     /* ── Warning banner ── */
#     .warn-banner {
#         background: rgba(245,158,11,0.07);
#         border: 1px solid rgba(245,158,11,0.25);
#         border-left: 3px solid #f59e0b;
#         border-radius: 10px;
#         padding: 12px 16px;
#         color: #fbbf24;
#         font-size: 0.85rem;
#         margin-bottom: 8px;
#     }

#     /* ── Divider with label ── */
#     .divider-label {
#         display: flex;
#         align-items: center;
#         gap: 12px;
#         margin: 1.6rem 0 1.2rem;
#     }
#     .divider-label span {
#         color: #374151;
#         font-size: 0.72rem;
#         font-weight: 700;
#         text-transform: uppercase;
#         letter-spacing: 0.10em;
#         white-space: nowrap;
#     }
#     .divider-label::before,
#     .divider-label::after {
#         content: "";
#         flex: 1;
#         height: 1px;
#         background: #1e2d4a;
#     }

#     /* ── History table ── */
#     .history-header {
#         display: grid;
#         grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
#         gap: 1px;
#         background: #1e2d4a;
#         border-radius: 10px 10px 0 0;
#         overflow: hidden;
#         margin-bottom: 1px;
#     }
#     .history-header div {
#         background: #0f1120;
#         padding: 10px 14px;
#         font-size: 0.70rem;
#         font-weight: 700;
#         text-transform: uppercase;
#         letter-spacing: 0.08em;
#         color: #475569;
#     }

#     /* ── Buttons ── */
#     .stButton > button {
#         background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
#         color: #ffffff !important;
#         border: none !important;
#         border-radius: 8px !important;
#         font-weight: 600 !important;
#         font-size: 0.85rem !important;
#         letter-spacing: 0.02em !important;
#         padding: 0.45rem 1.1rem !important;
#         transition: all 0.2s ease !important;
#         box-shadow: 0 2px 8px rgba(14,165,233,0.3) !important;
#     }
#     .stButton > button:hover {
#         background: linear-gradient(135deg, #38bdf8, #0ea5e9) !important;
#         box-shadow: 0 4px 16px rgba(14,165,233,0.45) !important;
#         transform: translateY(-1px) !important;
#     }
#     .stButton > button[kind="secondary"] {
#         background: #1e2540 !important;
#         box-shadow: none !important;
#         color: #94a3b8 !important;
#     }
#     .stButton > button[kind="secondary"]:hover {
#         background: #272f4a !important;
#         color: #e2e8f0 !important;
#         transform: none !important;
#     }

#     /* ── Form submit buttons ── */
#     .stFormSubmitButton > button {
#         background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
#         color: #ffffff !important;
#         border: none !important;
#         border-radius: 8px !important;
#         font-weight: 600 !important;
#         transition: all 0.2s ease !important;
#         box-shadow: 0 2px 8px rgba(14,165,233,0.3) !important;
#     }
#     .stFormSubmitButton > button:hover {
#         background: linear-gradient(135deg, #38bdf8, #0ea5e9) !important;
#         box-shadow: 0 4px 16px rgba(14,165,233,0.45) !important;
#     }

#     /* ── Containers ── */
#     div[data-testid="stVerticalBlockBorderWrapper"] {
#         background: #141726 !important;
#         border: 1px solid #1e2d4a !important;
#         border-radius: 12px !important;
#         box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important;
#         transition: border-color 0.2s ease !important;
#     }
#     div[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: #1e3d5c !important; }

#     /* ── Inputs ── */
#     .stTextInput > div > div > input,
#     .stNumberInput > div > div > input,
#     .stTextArea > div > div > textarea {
#         background-color: #141726 !important;
#         border: 1px solid #1e2d4a !important;
#         color: #e2e8f0 !important;
#         border-radius: 8px !important;
#         font-size: 0.9rem !important;
#     }
#     .stTextInput > div > div > input:focus,
#     .stNumberInput > div > div > input:focus,
#     .stTextArea > div > div > textarea:focus {
#         border-color: #0ea5e9 !important;
#         box-shadow: 0 0 0 2px rgba(14,165,233,0.2) !important;
#     }

#     /* ── Selectbox ── */
#     .stSelectbox > div > div,
#     div[data-baseweb="select"] > div {
#         background-color: #141726 !important;
#         border-color: #1e2d4a !important;
#         color: #e2e8f0 !important;
#         border-radius: 8px !important;
#     }

#     /* ── Slider ── */
#     .stSlider [data-baseweb="slider"] div[role="slider"] {
#         background-color: #0ea5e9 !important;
#         border-color: #0ea5e9 !important;
#     }

#     /* ── Expander ── */
#     details[data-testid="stExpander"] {
#         background: #0f1120 !important;
#         border: 1px solid #1e2d4a !important;
#         border-radius: 10px !important;
#         overflow: hidden !important;
#     }
#     details[data-testid="stExpander"] summary {
#         color: #64748b !important;
#         font-weight: 700 !important;
#         font-size: 0.80rem !important;
#         letter-spacing: 0.08em !important;
#         text-transform: uppercase !important;
#         padding: 0.8rem 1rem !important;
#     }
#     details[data-testid="stExpander"] summary:hover { color: #e2e8f0 !important; background: #141726 !important; }

#     /* ── Form container ── */
#     div[data-testid="stForm"] {
#         background: #0f1120 !important;
#         border: 1px solid #1e2d4a !important;
#         border-radius: 10px !important;
#         padding: 1rem !important;
#     }

#     /* ── Native Streamlit alerts (hidden in favor of custom) ── */
#     div[data-testid="stAlert"] { border-radius: 10px !important; border-left-width: 4px !important; font-size: 0.88rem !important; }

#     /* ── Headings ── */
#     h2, h3 { color: #f1f5f9 !important; font-weight: 700 !important; letter-spacing: -0.01em !important; }
#     h2 { font-size: 1.15rem !important; border-bottom: 1px solid #1e2d4a; padding-bottom: 0.5rem; margin-bottom: 1rem !important; }

#     /* ── Captions ── */
#     .stCaptionContainer, small { color: #475569 !important; font-size: 0.82rem !important; }

#     /* ── HR ── */
#     hr { border-color: #1e2d4a !important; }

#     /* ── Native table ── */
#     div[data-testid="stTable"] table { background-color: #141726 !important; border-radius: 10px !important; overflow: hidden !important; border: 1px solid #1e2d4a !important; }
#     div[data-testid="stTable"] th { background-color: #0f1120 !important; color: #475569 !important; font-size: 0.72rem !important; font-weight: 700 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; border-bottom: 1px solid #1e2d4a !important; padding: 10px 14px !important; }
#     div[data-testid="stTable"] td { color: #cbd5e1 !important; border-bottom: 1px solid #1a1f38 !important; padding: 10px 14px !important; font-size: 0.88rem !important; }
#     div[data-testid="stTable"] tr:hover td { background: #1a1f38 !important; }

#     /* ── JSON ── */
#     div[data-testid="stJson"] { background: #0f1120 !important; border: 1px solid #1e2d4a !important; border-radius: 10px !important; }

#     /* ── Date input ── */
#     .stDateInput > div > div > input { background-color: #141726 !important; border: 1px solid #1e2d4a !important; color: #e2e8f0 !important; border-radius: 8px !important; }

#     /* ── Sidebar success ── */
#     div[data-testid="stSidebar"] .stSuccess { background: #0c1f1a !important; border: 1px solid #134e2e !important; border-radius: 8px !important; color: #4ade80 !important; }

#     /* ── Scrollbar ── */
#     ::-webkit-scrollbar { width: 5px; height: 5px; }
#     ::-webkit-scrollbar-track { background: #0d0f1a; }
#     ::-webkit-scrollbar-thumb { background: #1e2d4a; border-radius: 10px; }
#     ::-webkit-scrollbar-thumb:hover { background: #0ea5e9; }

#     /* ── Spinner ── */
#     .stSpinner > div { border-top-color: #0ea5e9 !important; }

#     /* ── Empty state ── */
#     .empty-state {
#         text-align: center;
#         padding: 3rem 2rem;
#         background: #0f1120;
#         border: 1px dashed #1e2d4a;
#         border-radius: 14px;
#         color: #374151;
#     }
#     .empty-state .es-icon { font-size: 2.5rem; margin-bottom: 12px; }
#     .empty-state .es-title { color: #475569; font-size: 0.95rem; font-weight: 600; margin-bottom: 4px; }
#     .empty-state .es-sub   { color: #374151; font-size: 0.82rem; }

#     /* ── Budget display card ── */
#     .budget-stat {
#         background: #141726;
#         border: 1px solid #1e2d4a;
#         border-radius: 12px;
#         padding: 20px;
#         text-align: center;
#     }
#     .budget-stat .bs-label { font-size: 0.70rem; text-transform: uppercase; letter-spacing: 0.10em; font-weight: 700; color: #475569; }
#     .budget-stat .bs-value { font-size: 1.5rem; font-weight: 800; color: #f1f5f9; margin: 6px 0; }
#     .budget-stat .bs-sub   { font-size: 0.78rem; color: #64748b; }
# </style>
# """, unsafe_allow_html=True)



# # ---------- AUTHENTICATION GATE ----------
# if "user_id" not in st.session_state:
#     st.markdown("""
#     <div style="max-width: 400px; margin: 4rem auto; text-align: center;">
#         <h1>🧭 AI Agent Coordination & Decision Engine</h1>
#         <p style="color: #64748b;">Sign in to continue</p>
#     </div>
#     """, unsafe_allow_html=True)

#     col1, col2, col3 = st.columns([1, 2, 1])
#     with col2:
#         tab1, tab2 = st.tabs(["Log In", "Sign Up"])

#         with tab1:
#             with st.form("login_form"):
#                 login_username = st.text_input("Username")
#                 login_password = st.text_input("Password", type="password")
#                 if st.form_submit_button("Log In", type="primary"):
#                     user_id = verify_user(login_username, login_password)
#                     if user_id:
#                         st.session_state["user_id"] = user_id
#                         st.session_state["username"] = login_username
#                         st.rerun()
#                     else:
#                         st.error("Invalid username or password")

#         with tab2:
#             with st.form("signup_form"):
#                 new_username = st.text_input("Choose a username")
#                 new_password = st.text_input("Choose a password", type="password")
#                 confirm_password = st.text_input("Confirm password", type="password")
#                 if st.form_submit_button("Sign Up", type="primary"):
#                     if not new_username.strip() or not new_password:
#                         st.error("Username and password are required")
#                     elif new_password != confirm_password:
#                         st.error("Passwords do not match")
#                     else:
#                         try:
#                             user_id = create_user(new_username.strip(), new_password)
#                             st.session_state["user_id"] = user_id
#                             st.session_state["username"] = new_username.strip()
#                             st.success("Account created! Redirecting...")
#                             st.rerun()
#                         except ValueError as e:
#                             st.error(str(e))

#     st.stop()  # nothing below this runs until logged in

# # ──────────────────────────────────────────────────────────────
# # SIDEBAR
# # ──────────────────────────────────────────────────────────────
# st.sidebar.markdown(f"👤 Logged in as **{st.session_state.get('username', 'user')}**")
# if st.sidebar.button("Log Out"):
#     st.session_state.pop("user_id", None)
#     st.session_state.pop("username", None)
#     st.session_state.pop("active_project_id", None)
#     st.session_state.pop("active_project_name", None)
#     st.rerun()

# st.sidebar.markdown("""
# <div style="padding: 12px 0 16px 0; border-bottom: 1px solid #1e2d4a; margin-bottom: 12px;">
#   <div style="font-size:1.3rem;font-weight:800;color:#89ceff;letter-spacing:-0.01em;">🛡️ Decision Engine</div>
#   <div style="font-size:0.72rem;color:#475569;text-transform:uppercase;letter-spacing:0.08em;">Enterprise Tier</div>
# </div>
# """, unsafe_allow_html=True)

# mock_mode = st.sidebar.checkbox("Mock mode (no API calls)", value=True)
# os.environ["USE_MOCK_AGENT"] = "1" if mock_mode else "0"

# st.sidebar.markdown("---")
# st.sidebar.markdown('<div style="font-size:0.70rem;text-transform:uppercase;letter-spacing:0.12em;color:#374151;font-weight:700;margin-bottom:8px;">Projects</div>', unsafe_allow_html=True)

# existing_projects = list_projects()
# project_names = {p["name"]: p["id"] for p in existing_projects}

# action = st.sidebar.radio("Action", ["Open existing", "Create new"], label_visibility="collapsed")
# if action == "Create new":
#     st.session_state.pop("active_project_id", None)
#     st.session_state.pop("active_project_name", None)

#     new_name = st.sidebar.text_input("New project name")
#     new_start = st.sidebar.date_input("Project start date")
#     new_end = st.sidebar.date_input("Project end date")
#     if st.sidebar.button("Create Project", type="primary"):
#         if new_name.strip():
#             pid = create_project(new_name.strip(), str(new_start), str(new_end))
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

# active_id   = st.session_state.get("active_project_id")
# active_name = st.session_state.get("active_project_name")

# if not active_id:
#     st.markdown("""
#     <div class="main-header">
#         <h1>🧭 AI Agent Coordination &amp; Decision Engine</h1>
#         <p>Multi-agent risk, resource, and budget analysis for project managers</p>
#     </div>
#     """, unsafe_allow_html=True)
#     st.markdown("""
#     <div class="info-banner">
#         <span>ℹ️</span>
#         <span>Create or open a project from the sidebar to get started.</span>
#     </div>
#     """, unsafe_allow_html=True)
#     st.stop()

# st.sidebar.markdown("---")
# st.sidebar.success(f"Active: **{active_name}**")

# with st.sidebar.expander("⚙️ Project Settings"):
#     with st.form("rename_form"):
#         new_project_name = st.text_input("Rename project", value=active_name)
#         if st.form_submit_button("Rename"):
#             if new_project_name.strip() and new_project_name.strip() != active_name:
#                 from db.repository import rename_project
#                 rename_project(active_id, new_project_name.strip())
#                 st.session_state["active_project_name"] = new_project_name.strip()
#                 st.success("Renamed")
#                 st.rerun()

#     st.markdown("---")
#     st.caption("⚠️ This permanently deletes the project and all its data.")
#     confirm_delete = st.checkbox("I understand this cannot be undone")
#     if st.button("🗑️ Delete This Project", disabled=not confirm_delete):
#         from db.repository import delete_project
#         delete_project(active_id)
#         st.session_state.pop("active_project_id", None)
#         st.session_state.pop("active_project_name", None)
#         st.success("Project deleted")
#         st.rerun()

# # ──────────────────────────────────────────────────────────────
# # MAIN HEADER
# # ──────────────────────────────────────────────────────────────
# st.markdown(f"""
# <div class="main-header">
#     <h1>🧭 {active_name}</h1>
#     <p>AI Agent Coordination &amp; Decision Engine</p>
# </div>
# """, unsafe_allow_html=True)

# st.sidebar.markdown('<div style="font-size:0.70rem;text-transform:uppercase;letter-spacing:0.12em;color:#374151;font-weight:700;margin:12px 0 6px 0;">Navigation</div>', unsafe_allow_html=True)
# page = st.sidebar.radio("Go to", ["Overview", "Tasks", "Team", "Budget", "Run Analysis", "History"], label_visibility="collapsed")

# # ──────────────────────────────────────────────────────────────
# # OVERVIEW
# # ──────────────────────────────────────────────────────────────
# if page == "Overview":
#     summary    = get_project_summary(active_id)
#     budget_data = get_latest_budget_entry(active_id)

#     from db.repository import get_project_dates
#     from tools.budget_tools import calculate_pct_time_elapsed, check_budget_status

#     dates = get_project_dates(active_id)
#     live_pct_time = 0
#     if dates and dates["start_date"] and dates["end_date"]:
#         live_pct_time = calculate_pct_time_elapsed(dates["start_date"], dates["end_date"])

#     # KPI row
#     col1, col2, col3, col4 = st.columns(4)
#     col1.metric("Total Tasks",    summary["task_count"])
#     col2.metric("Team Members",   summary["team_count"])

#     budget_status = "Not Set"
#     if budget_data:
#         result = check_budget_status(budget_data["planned_spend"], budget_data["actual_spend"], live_pct_time)
#         if result.startswith("over_budget"):
#             budget_status = "⚠️ Over Budget"
#         elif result.startswith("at_risk"):
#             budget_status = "🟡 At Risk"
#         else:
#             budget_status = "✅ On Budget"
#     col3.metric("Budget Status",  budget_status)
#     col4.metric("Last Analysis",  summary["last_analysis"].strftime("%b %d, %H:%M") if summary["last_analysis"] else "Never")
#     # ---------- NEW: Stale data warning ----------
#     from db.repository import get_last_data_change

#     last_data_change = get_last_data_change(active_id)
#     last_analysis_time = summary["last_analysis"]

#     if last_data_change and last_analysis_time and last_data_change > last_analysis_time:
#         st.markdown("""
#         <div class="warn-banner">
#             ⚠ Data has changed since your last analysis was run. Results shown elsewhere may be outdated — go to Run Analysis to refresh.
#         </div>
#         """, unsafe_allow_html=True)
#     elif last_data_change and not last_analysis_time:
#         st.markdown("""
#         <div class="warn-banner">
#             ⚠ You have data but haven't run analysis yet. Go to Run Analysis to generate insights.
#         </div>
#         """, unsafe_allow_html=True)
#     # Budget visual strip
#     if budget_data:
#         st.markdown('<div class="divider-label"><span>Budget Snapshot</span></div>', unsafe_allow_html=True)
#         b1, b2, b3 = st.columns(3)
#         with b1:
#             st.markdown(f"""
#             <div class="budget-stat">
#                 <div class="bs-label">Planned Spend</div>
#                 <div class="bs-value">₹{budget_data['planned_spend']:,.0f}</div>
#                 <div class="bs-sub">Total budget</div>
#             </div>""", unsafe_allow_html=True)
#         with b2:
#             st.markdown(f"""
#             <div class="budget-stat">
#                 <div class="bs-label">Actual Spend</div>
#                 <div class="bs-value">₹{budget_data['actual_spend']:,.0f}</div>
#                 <div class="bs-sub">Spent to date</div>
#             </div>""", unsafe_allow_html=True)
#         with b3:
#             spend_pct = (budget_data['actual_spend'] / budget_data['planned_spend'] * 100) if budget_data['planned_spend'] else 0
#             color = "#ef4444" if spend_pct > live_pct_time + 10 else "#f59e0b" if spend_pct > live_pct_time else "#10b981"
#             st.markdown(f"""
#             <div class="budget-stat">
#                 <div class="bs-label">Timeline Elapsed</div>
#                 <div class="bs-value" style="color:{color};">{live_pct_time:.1f}%</div>
#                 <div class="bs-sub">{spend_pct:.1f}% of budget used</div>
#             </div>""", unsafe_allow_html=True)

#     # Validation warnings
#     tasks     = get_tasks(active_id)
#     team      = get_team_members(active_id)
#     team_names = {t["name"] for t in team}
#     task_ids   = {t["id"] for t in tasks}

#     warnings = []
#     for task in tasks:
#         if task["assigned_to"] and task["assigned_to"] not in team_names:
#             warnings.append(f"Task <b>{task['id']}</b> is assigned to <b>'{task['assigned_to']}'</b> — not found in the team roster.")
#         for dep in task["depends_on"]:
#             if dep not in task_ids:
#                 warnings.append(f"Task <b>{task['id']}</b> depends on <b>'{dep}'</b> — this task does not exist.")

#     if warnings:
#         st.markdown('<div class="divider-label"><span>Data Issues</span></div>', unsafe_allow_html=True)
#         for w in warnings:
#             st.markdown(f'<div class="warn-banner">⚠ {w}</div>', unsafe_allow_html=True)

#     st.markdown('<div class="divider-label"><span>Getting Started</span></div>', unsafe_allow_html=True)
#     st.markdown("""
#     <div class="info-banner">
#         <span>💡</span>
#         <span>Use the sidebar to manage tasks, team members, budget, and run AI analysis.</span>
#     </div>
#     """, unsafe_allow_html=True)
# # ──────────────────────────────────────────────────────────────
# # TASKS
# # ──────────────────────────────────────────────────────────────
# elif page == "Tasks":
#     st.markdown('<div class="section-label"><div class="icon">📋</div><h3>Task Management</h3></div>', unsafe_allow_html=True)

#     with st.expander("＋  Add New Task"):
#         with st.form("task_form", clear_on_submit=True):
#             c1, c2 = st.columns(2)
#             with c1:
#                 tid  = st.text_input("Task ID", placeholder="e.g. T1")
#                 tname = st.text_input("Task Name", placeholder="e.g. Design wireframes")
#             with c2:
#                 deadline    = st.date_input("Deadline")
#                 assigned_to = st.text_input("Assigned To", placeholder="Team member name")
#             progress       = st.slider("Progress %", 0, 100, 0)
#             depends_on_raw = st.text_input("Depends On", placeholder="Comma-separated task IDs, e.g. T1, T2")
#             if st.form_submit_button("Add Task"):
#                 if tid.strip() and tname.strip():
#                     depends_on = [d.strip() for d in depends_on_raw.split(",") if d.strip()]
#                     add_task(active_id, tid.strip(), tname.strip(), progress, str(deadline), depends_on, assigned_to.strip())
#                     st.success(f"Task **{tid}** added successfully.")
#                     st.rerun()
#                 else:
#                     st.error("Task ID and Name are required.")

#     with st.expander("📥  Bulk Import Tasks (upload JSON)"):
#         st.caption('Upload a JSON file: a list of objects like '
#                    '{"id": "T1", "name": "...", "progress_pct": 0, "planned_end": "YYYY-MM-DD", "depends_on": [], "assigned_to": "..."}')
#         uploaded = st.file_uploader("Choose a JSON file", type=["json"], key="task_upload")
#         if uploaded:
#             try:
#                 data = json_lib.load(uploaded)
#                 task_list = data.get("tasks", data) if isinstance(data, dict) else data
#                 st.write(f"Found {len(task_list)} task(s) in file. Preview:")
#                 st.json(task_list[:3])
#                 if st.button("Import These Tasks"):
#                     count = bulk_add_tasks(active_id, task_list)
#                     st.success(f"Imported {count} tasks")
#                     st.rerun()
#             except Exception as e:
#                 st.error(f"Could not parse file: {e}")

#     current_tasks = get_tasks_with_db_id(active_id)
#     st.markdown('<div class="divider-label"><span>All Tasks</span></div>', unsafe_allow_html=True)

#     if not current_tasks:
#         st.markdown("""
#         <div class="empty-state">
#             <div class="es-icon">📭</div>
#             <div class="es-title">No tasks yet</div>
#             <div class="es-sub">Expand the panel above to add your first task.</div>
#         </div>""", unsafe_allow_html=True)
#     else:
#         for task in current_tasks:
#             pct = int(task['progress_pct'])
#             if pct >= 80:   bar_cls = "high"
#             elif pct >= 40: bar_cls = "mid"
#             else:           bar_cls = "low"

#             dep_str    = ", ".join(task['depends_on']) if task['depends_on'] else "—"
#             assign_str = task['assigned_to'] or "—"

#             with st.container(border=True):
#                 left, right = st.columns([5, 1])
#                 with left:
#                     st.markdown(f"""
#                     <div class="card-title">{task['id']} &nbsp;·&nbsp; {task['name']}</div>
#                     <div class="card-meta">
#                         <div class="card-meta-item"><span class="label">Deadline</span><span class="value">{task['planned_end']}</span></div>
#                         <div class="card-meta-item"><span class="label">Assigned</span><span class="value">{assign_str}</span></div>
#                         <div class="card-meta-item"><span class="label">Depends on</span><span class="value">{dep_str}</span></div>
#                         <div class="card-meta-item"><span class="label">Progress</span><span class="value">{pct}%</span></div>
#                     </div>
#                     <div class="progress-wrap"><div class="progress-fill {bar_cls}" style="width:{pct}%;"></div></div>
#                     """, unsafe_allow_html=True)
#                 with right:
#                     edit_key = f"edit_task_{task['db_id']}"
#                     if st.button("Edit", key=f"btn_{edit_key}"):
#                         st.session_state[edit_key] = not st.session_state.get(edit_key, False)

#                 if st.session_state.get(f"edit_task_{task['db_id']}", False):
#                     with st.form(f"edit_form_{task['db_id']}"):
#                         e1, e2 = st.columns(2)
#                         with e1:
#                             new_name     = st.text_input("Name",     value=task["name"])
#                             new_deadline = st.text_input("Deadline (YYYY-MM-DD)", value=task["planned_end"])
#                         with e2:
#                             new_assigned = st.text_input("Assigned To", value=task["assigned_to"] or "")
#                             new_depends  = st.text_input("Depends On",  value=", ".join(task["depends_on"]))
#                         new_progress = st.slider("Progress %", 0, 100, int(task["progress_pct"]))
#                         s1, s2 = st.columns(2)
#                         with s1:
#                             if st.form_submit_button("Save Changes"):
#                                 depends_list = [d.strip() for d in new_depends.split(",") if d.strip()]
#                                 update_task(task["db_id"], new_name, new_progress, new_deadline, depends_list, new_assigned)
#                                 st.session_state[f"edit_task_{task['db_id']}"] = False
#                                 st.rerun()
#                         with s2:
#                             if st.form_submit_button("Delete Task", type="secondary"):
#                                 delete_task(task["db_id"])
#                                 st.rerun()
# # ──────────────────────────────────────────────────────────────
# # TEAM
# # ──────────────────────────────────────────────────────────────
# elif page == "Team":
#     st.markdown('<div class="section-label"><div class="icon">👥</div><h3>Team Roster</h3></div>', unsafe_allow_html=True)

#     with st.expander("＋  Add New Team Member"):
#         with st.form("member_form", clear_on_submit=True):
#             c1, c2 = st.columns(2)
#             with c1:
#                 mname    = st.text_input("Full Name", placeholder="e.g. Alice Johnson")
#                 capacity = st.number_input("Weekly Capacity (hrs)", value=40.0)
#             with c2:
#                 logged     = st.number_input("Logged Hours This Week", value=0.0)
#                 skills_raw = st.text_input("Skills", placeholder="e.g. Python, Design, DevOps")
#             if st.form_submit_button("Add Team Member"):
#                 if mname.strip():
#                     skills = [s.strip() for s in skills_raw.split(",") if s.strip()]
#                     add_team_member(active_id, mname.strip(), capacity, logged, skills)
#                     st.success(f"**{mname}** added to the team.")
#                     st.rerun()
#                 else:
#                     st.error("Name is required.")
#     with st.expander("Bulk Import Team (upload JSON)"):
#         st.caption('Upload a JSON file: a list of objects like '
#                    '{"name": "...", "capacity_hrs_week": 40, "logged_hrs_week": 0, "skills": []}')
#         uploaded = st.file_uploader("Choose a JSON file", type=["json"], key="team_upload")
#         if uploaded:
#             try:
#                 data = json_lib.load(uploaded)
#                 member_list = data.get("team", data) if isinstance(data, dict) else data
#                 st.write(f"Found {len(member_list)} member(s) in file. Preview:")
#                 st.json(member_list[:3])
#                 if st.button("Import These Team Members"):
#                     count = bulk_add_team_members(active_id, member_list)
#                     st.success(f"Imported {count} team members")
#                     st.rerun()
#             except Exception as e:
#                 st.error(f"Could not parse file: {e}")

#     current_team = get_team_members_with_db_id(active_id)
#     st.markdown('<div class="divider-label"><span>Team Members</span></div>', unsafe_allow_html=True)

#     if not current_team:
#         st.markdown("""
#         <div class="empty-state">
#             <div class="es-icon">🧑‍💼</div>
#             <div class="es-title">No team members yet</div>
#             <div class="es-sub">Expand the panel above to add your first team member.</div>
#         </div>""", unsafe_allow_html=True)
#     else:
#         for member in current_team:
#             cap  = member["capacity_hrs_week"] or 1
#             log  = member["logged_hrs_week"]
#             pct  = min((log / cap * 100), 100)
#             if pct >= 90:   util_color, util_label = "#ef4444", "Overloaded"
#             elif pct >= 70: util_color, util_label = "#f59e0b", "High"
#             elif pct >= 40: util_color, util_label = "#0ea5e9", "Moderate"
#             else:            util_color, util_label = "#10b981", "Available"

#             skills_str = ", ".join(member["skills"]) if member["skills"] else "—"

#             with st.container(border=True):
#                 left, right = st.columns([5, 1])
#                 with left:
#                     st.markdown(f"""
#                     <div class="card-title">{member['name']}
#                         <span class="badge badge-blue" style="margin-left:10px;font-size:0.68rem;">{util_label}</span>
#                     </div>
#                     <div class="card-meta" style="margin-top:4px;">
#                         <div class="card-meta-item"><span class="label">Logged</span><span class="value">{log} / {cap} hrs</span></div>
#                         <div class="card-meta-item"><span class="label">Utilization</span><span class="value">{pct:.0f}%</span></div>
#                         <div class="card-meta-item"><span class="label">Skills</span><span class="value">{skills_str}</span></div>
#                     </div>
#                     <div class="util-row">
#                         <div class="util-bar-bg"><div class="util-bar-fill" style="width:{pct}%;background:{util_color};"></div></div>
#                         <span style="color:{util_color};font-weight:700;min-width:36px;">{pct:.0f}%</span>
#                     </div>
#                     """, unsafe_allow_html=True)
#                 with right:
#                     edit_key = f"edit_member_{member['db_id']}"
#                     if st.button("Edit", key=f"btn_{edit_key}"):
#                         st.session_state[edit_key] = not st.session_state.get(edit_key, False)

#                 if st.session_state.get(f"edit_member_{member['db_id']}", False):
#                     with st.form(f"edit_member_form_{member['db_id']}"):
#                         e1, e2 = st.columns(2)
#                         with e1:
#                             new_name     = st.text_input("Name",             value=member["name"])
#                             new_capacity = st.number_input("Weekly Capacity (hrs)", value=float(member["capacity_hrs_week"]))
#                         with e2:
#                             new_logged = st.number_input("Logged Hours", value=float(member["logged_hrs_week"]))
#                             new_skills = st.text_input("Skills",         value=", ".join(member["skills"]))
#                         s1, s2 = st.columns(2)
#                         with s1:
#                             if st.form_submit_button("Save Changes"):
#                                 skills_list = [s.strip() for s in new_skills.split(",") if s.strip()]
#                                 update_team_member(member["db_id"], new_name, new_capacity, new_logged, skills_list)
#                                 st.session_state[f"edit_member_{member['db_id']}"] = False
#                                 st.rerun()
#                         with s2:
#                             if st.form_submit_button("Delete Member", type="secondary"):
#                                 delete_team_member(member["db_id"])
#                                 st.rerun()

# # ──────────────────────────────────────────────────────────────
# # BUDGET
# # ──────────────────────────────────────────────────────────────
# elif page == "Budget":
#     st.subheader("Budget")

#     from db.repository import get_project_dates, update_project_dates
#     from tools.budget_tools import calculate_pct_time_elapsed

#     dates = get_project_dates(active_id)
#     if dates and dates["start_date"] and dates["end_date"]:
#         pct_time = calculate_pct_time_elapsed(dates["start_date"], dates["end_date"])
#         st.info(f"Timeline: {dates['start_date']} to {dates['end_date']} — **{pct_time:.1f}%** elapsed (calculated automatically)")
#     else:
#         st.warning("This project has no start/end date set. Timeline % cannot be calculated automatically.")
#         pct_time = 0.0

#     with st.expander("Edit Project Timeline (e.g. if deadline is extended)"):
#         with st.form("edit_dates_form"):
#             import datetime
#             current_start = datetime.date.fromisoformat(dates["start_date"]) if dates and dates["start_date"] else datetime.date.today()
#             current_end = datetime.date.fromisoformat(dates["end_date"]) if dates and dates["end_date"] else datetime.date.today()

#             new_start = st.date_input("Start Date", value=current_start)
#             new_end = st.date_input("End Date", value=current_end)
#             if st.form_submit_button("Update Timeline"):
#                 if new_end > new_start:
#                     update_project_dates(active_id, str(new_start), str(new_end))
#                     st.success("Project timeline updated")
#                     st.rerun()
#                 else:
#                     st.error("End date must be after start date")

#     current_budget = get_latest_budget_entry(active_id)
#     if current_budget:
#         st.json(current_budget)
#     else:
#         st.info("No budget set yet.")

#     with st.form("budget_form"):
#         planned = st.number_input("Planned Spend ($)", value=current_budget["planned_spend"] if current_budget else 50000.0)
#         actual = st.number_input("Actual Spend ($)", value=current_budget["actual_spend"] if current_budget else 0.0)
#         st.caption(f"Timeline elapsed: {pct_time:.1f}% (auto-calculated from project dates)")
#         if st.form_submit_button("Save Budget"):
#             add_budget_entry(active_id, planned, actual, pct_time)
#             st.success("Budget saved")
#             st.rerun()
# # ──────────────────────────────────────────────────────────────
# # RUN ANALYSIS
# # ──────────────────────────────────────────────────────────────
# elif page == "Run Analysis":
#     st.markdown('<div class="section-label"><div class="icon">🤖</div><h3>AI Agent Analysis</h3></div>', unsafe_allow_html=True)

#     tasks  = get_tasks(active_id)
#     team   = get_team_members(active_id)
#     budget = get_latest_budget_entry(active_id)

#     from db.repository import get_last_data_change
#     last_data_change = get_last_data_change(active_id)
#     summary_check = get_project_summary(active_id)
#     if last_data_change and summary_check["last_analysis"] and last_data_change > summary_check["last_analysis"]:
#         st.markdown("""
#         <div class="warn-banner">
#             ⚠ Data has changed since the last analysis. Click "Run Analysis" below to get up-to-date results.
#         </div>
#         """, unsafe_allow_html=True)
#     # Always use the LIVE, auto-calculated timeline percentage instead of
#     # whatever was last saved in the budget entry — avoids stale data.
#     from db.repository import get_project_dates
#     from tools.budget_tools import calculate_pct_time_elapsed

#     dates = get_project_dates(active_id)
#     if budget and dates and dates["start_date"] and dates["end_date"]:
#         budget["pct_time_elapsed"] = calculate_pct_time_elapsed(dates["start_date"], dates["end_date"])

#     if not tasks:
#         st.markdown("""
#         <div class="empty-state">
#             <div class="es-icon">📋</div>
#             <div class="es-title">No tasks to analyze</div>
#             <div class="es-sub">Add at least one task on the Tasks page before running analysis.</div>
#         </div>""", unsafe_allow_html=True)
#     else:
#         st.markdown(f"""
#         <div class="info-banner" style="margin-bottom:1.2rem;">
#             <span>🔍</span>
#             <span>Ready to analyze <b>{len(tasks)} task(s)</b> across <b>{len(team)} team member(s)</b>. Click below to run all agents.</span>
#         </div>""", unsafe_allow_html=True)

#         if st.button("▶  Run Analysis", type="primary"):
#             project_data = {"tasks": tasks, "team": team}
#             if budget:
#                 project_data["budget"] = budget

#             with st.spinner("Agents analyzing project..."):
#                 results, conflicts = orchestrate(project_data, active_id)
#             st.session_state["last_results"] = results

#             st.markdown('<div class="divider-label"><span>Agent Results</span></div>', unsafe_allow_html=True)
#             col1, col2, col3 = st.columns(3)

#             with col1:
#                 st.markdown('<div class="result-card"><div class="rc-title">⚠ Risk &amp; Deadline</div>', unsafe_allow_html=True)
#                 for r in results:
#                     if r["agent"] == "risk_deadline":
#                         is_bad = r["finding"] == "high_risk"
#                         color  = "#f87171" if is_bad else "#4ade80"
#                         icon   = "🔴" if is_bad else "🟢"
#                         st.markdown(f'<div class="rc-value" style="color:{color};">{icon} {r["user_response"]}</div>', unsafe_allow_html=True)
#                 st.markdown('</div>', unsafe_allow_html=True)

#             with col2:
#                 st.markdown('<div class="result-card"><div class="rc-title">👤 Resource Usage</div>', unsafe_allow_html=True)
#                 for r in results:
#                     if r["agent"] == "resource_usage":
#                         is_bad = r["finding"] in ("overloaded", "severely_overloaded")
#                         color  = "#f87171" if is_bad else "#4ade80"
#                         icon   = "🔴" if is_bad else "🟢"
#                         st.markdown(f'<div class="rc-value" style="color:{color};">{icon} {r["user_response"]}</div>', unsafe_allow_html=True)
#                 st.markdown('</div>', unsafe_allow_html=True)

#             with col3:
#                 st.markdown('<div class="result-card"><div class="rc-title">💰 Budget</div>', unsafe_allow_html=True)
#                 for r in results:
#                     if r["agent"] == "budget_tracking":
#                         is_bad = r["finding"] == "over_budget"
#                         color  = "#f87171" if is_bad else "#4ade80"
#                         icon   = "🔴" if is_bad else "🟢"
#                         st.markdown(f'<div class="rc-value" style="color:{color};">{icon} {r["user_response"]}</div>', unsafe_allow_html=True)
#                 st.markdown('</div>', unsafe_allow_html=True)

#             col4, col5 = st.columns(2)

#             with col4:
#                 st.markdown('<div class="result-card"><div class="rc-title">🏃 Scrum Master</div>', unsafe_allow_html=True)
#                 for r in results:
#                     if r["agent"] == "scrum_master":
#                         is_bad = r["finding"] == "impediments_found"
#                         color  = "#f87171" if is_bad else "#4ade80"
#                         icon   = "🔴" if is_bad else "🟢"
#                         st.markdown(f'<div class="rc-value" style="color:{color};">{icon} {r["user_response"]}</div>', unsafe_allow_html=True)
#                 st.markdown('</div>', unsafe_allow_html=True)

#             with col5:
#                 st.markdown('<div class="result-card"><div class="rc-title">⚖ Project Distribution</div>', unsafe_allow_html=True)
#                 for r in results:
#                     if r["agent"] == "project_distribution":
#                         is_bad = r["finding"] == "imbalanced"
#                         color  = "#f87171" if is_bad else "#4ade80"
#                         icon   = "🔴" if is_bad else "🟢"
#                         st.markdown(f'<div class="rc-value" style="color:{color};">{icon} {r["user_response"]}</div>', unsafe_allow_html=True)
#                 st.markdown('</div>', unsafe_allow_html=True)

#             st.markdown('<div class="divider-label"><span>Decision Engine · Conflicts &amp; Recommendations</span></div>', unsafe_allow_html=True)
#             if conflicts:
#                 for c in conflicts:
#                     st.markdown(f"""
#                     <div class="conflict-card">
#                         <div class="cc-issue">⚡ {c['issue']}</div>
#                         <div class="cc-rec">➜ {c['recommendation']}</div>
#                     </div>""", unsafe_allow_html=True)
#             else:
#                 st.markdown("""
#                 <div class="info-banner">
#                     <span>✅</span>
#                     <span>No conflicts detected — all agents report healthy project status.</span>
#                 </div>""", unsafe_allow_html=True)

# # ──────────────────────────────────────────────────────────────
# # HISTORY
# # ──────────────────────────────────────────────────────────────
# elif page == "History":
#     st.markdown('<div class="section-label"><div class="icon">🕑</div><h3>Analysis History</h3></div>', unsafe_allow_html=True)

#     st.markdown('<div class="divider-label"><span>Short-Term Memory · This Session</span></div>', unsafe_allow_html=True)
#     if "last_results" in st.session_state:
#         st.table(st.session_state["last_results"])
#     else:
#         st.markdown("""
#         <div class="empty-state">
#             <div class="es-icon">🧠</div>
#             <div class="es-title">No session data yet</div>
#             <div class="es-sub">Run an analysis to populate short-term memory.</div>
#         </div>""", unsafe_allow_html=True)

#     st.markdown('<div class="divider-label"><span>Long-Term Memory · Full Project History</span></div>', unsafe_allow_html=True)
#     history = get_recent_findings(active_id, limit=20)
#     if history:
#         st.table(history)
#     else:
#         st.markdown("""
#         <div class="empty-state">
#             <div class="es-icon">📂</div>
#             <div class="es-title">No history yet</div>
#             <div class="es-sub">Previous analysis runs will appear here.</div>
#         </div>""", unsafe_allow_html=True) 

import streamlit as st
import os
import sys
import datetime

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.session import init_db
from db.repository import (
    create_user, verify_user, get_security_question, reset_password,
    create_project, list_projects, get_project_summary,
    add_team_member, get_team_members, get_team_members_with_db_id, update_team_member, delete_team_member,
    add_task, get_tasks, get_tasks_with_db_id, update_task, delete_task,
    add_budget_entry, get_latest_budget_entry,
    get_recent_findings, bulk_add_tasks, bulk_add_team_members
)
import json as json_lib
from orchestrator.orchestrator import orchestrate

init_db()

st.set_page_config(page_title="Aegis · AI Decision Engine", layout="wide", page_icon="🛡️")

# ══════════════════════════════════════════════════════════════
# GLOBAL STYLE — "Aegis Core" dark dashboard theme
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
    :root {
        --bg:        #0a0e1a;
        --panel:     #0f1424;
        --card:      #131a2c;
        --card-alt:  #161d33;
        --border:    #1e2740;
        --border-lt: #263252;
        --accent:    #5eb3f5;
        --accent-2:  #38bdf8;
        --text-hi:   #f1f5f9;
        --text-md:   #94a3b8;
        --text-lo:   #56617a;
        --green:     #4ade80;
        --yellow:    #fbbf24;
        --red:       #f87171;
    }

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: var(--bg) !important;
        color: var(--text-hi) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }
    [data-testid="stAppViewContainer"] > .main { background-color: var(--bg); }
    .block-container { padding-top: 5rem !important; max-width: 1400px; }

    /* ── Streamlit's own top toolbar (Deploy / menu bar) ── */
    [data-testid="stHeader"] {
        background: var(--bg) !important;
        border-bottom: 1px solid var(--border) !important;
        height: 3.2rem !important;
    }
    [data-testid="stToolbar"] { right: 1rem !important; }
    [data-testid="stDecoration"] { display: none !important; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: var(--panel) !important;
        border-right: 1px solid var(--border) !important;
    }
    [data-testid="stSidebar"] * { color: var(--text-md) !important; }
    [data-testid="stSidebar"] hr { border-color: var(--border) !important; margin: 0.8rem 0 !important; }

    .brand-block {
        display: flex; align-items: center; gap: 12px;
        padding: 4px 4px 18px 4px;
        border-bottom: 1px solid var(--border);
        margin-bottom: 14px;
    }
    .brand-icon {
        width: 42px; height: 42px; border-radius: 11px;
        background: linear-gradient(135deg, #1a2947, #0f1830);
        border: 1px solid var(--border-lt);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem; flex-shrink: 0;
        box-shadow: 0 0 0 1px rgba(94,179,245,0.08), 0 4px 14px rgba(0,0,0,0.4);
    }
    .brand-name { color: var(--accent) !important; font-size: 1.25rem; font-weight: 800; letter-spacing: -0.01em; line-height: 1.1; }
    .brand-sub  { color: var(--text-lo) !important; font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.10em; font-weight: 700; }

    .nav-label {
        font-size: 0.66rem; text-transform: uppercase; letter-spacing: 0.13em;
        color: var(--text-lo) !important; font-weight: 700; margin: 6px 0 8px 4px;
    }
    [data-testid="stSidebar"] [data-testid="stIconMaterial"] {
        color: var(--accent-2) !important;
        font-size: 1.05rem !important;
        vertical-align: -3px;
    }
    [data-testid="stSidebar"] .stRadio > div { gap: 2px !important; }

    [data-testid="stSidebar"] [data-testid="stRadioOption"] {
        background: transparent;
        border-radius: 9px;
        padding: 9px 12px !important;
        width: 100%;
        transition: background 0.15s ease;
        font-size: 0.88rem !important;
        font-weight: 600 !important;
        color: var(--text-md) !important;
    }

/* Recolor the radio dot from red to blue */
    [data-testid="stSidebar"] [data-testid="stRadioOption"] [aria-hidden="true"],
    [data-testid="stSidebar"] [data-testid="stRadioOption"] [aria-hidden="true"] * {
        background-color: transparent !important;
        border-color: var(--accent-2) !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] [aria-hidden="true"],
    [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] [aria-hidden="true"] * {
        background-color: var(--accent-2) !important;
        border-color: var(--accent-2) !important;
    }
    input[type="radio"] { accent-color: var(--accent-2) !important; }

    [data-testid="stSidebar"] [data-testid="stRadioOption"]:hover {
        background: var(--card) !important;
    }
    [data-testid="stSidebar"] [data-testid="stRadioOption"]:hover p,
    [data-testid="stSidebar"] [data-testid="stRadioOption"]:hover svg {
        color: var(--accent-2) !important;
        fill: var(--accent-2) !important;
    }

    [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] {
        background: var(--card-alt) !important;
        border-left: 3px solid var(--accent);
    }
    [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] p,
    [data-testid="stSidebar"] [data-testid="stRadioOption"][data-selected="true"] svg {
        color: var(--accent-2) !important;
        fill: var(--accent-2) !important;
    }

    .user-chip {
        display: flex; align-items: center; gap: 10px;
        padding: 10px 12px; background: var(--card);
        border: 1px solid var(--border); border-radius: 10px;
        margin-bottom: 10px;
    }
    .user-avatar {
        width: 30px; height: 30px; border-radius: 50%;
        background: linear-gradient(135deg, #38bdf8, #1e6fa8);
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 0.78rem; color: #041322; flex-shrink: 0;
    }
    .user-name { font-size: 0.85rem; color: var(--text-hi) !important; font-weight: 700; }
    .user-role { font-size: 0.68rem; color: var(--text-lo) !important; }

    /* ── Top bar ── */
    .topbar {
        display: flex; align-items: center; justify-content: space-between;
        gap: 20px; margin-bottom: 1.4rem;
    }
    .topbar-title { display: flex; flex-direction: column; }
    .topbar-title .tt-name { font-size: 1.55rem; font-weight: 800; color: var(--text-hi); letter-spacing: -0.02em; }
    .topbar-title .tt-sub  { font-size: 0.82rem; color: var(--text-lo); margin-top: 2px; }
    .topbar-icons { display: flex; align-items: center; gap: 14px; }
    .tb-icon {
        width: 38px; height: 38px; border-radius: 10px;
        background: var(--card); border: 1px solid var(--border);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.0rem; color: var(--text-md);
    }

    /* ── Hero / engine status card ── */
    .hero-card {
        background: linear-gradient(120deg, #101a30 0%, #0d1526 55%, #0a1220 100%);
        border: 1px solid var(--border-lt);
        border-radius: 16px;
        padding: 1.8rem 2.2rem;
        margin-bottom: 1.8rem;
        display: flex; align-items: center; justify-content: space-between;
        gap: 1.5rem; flex-wrap: wrap;
        position: relative; overflow: hidden;
        box-shadow: 0 4px 32px rgba(0,140,255,0.06), 0 1px 4px rgba(0,0,0,0.5);
    }
    .hero-card::before {
        content: ""; position: absolute; top: -60px; right: -60px;
        width: 240px; height: 240px;
        background: radial-gradient(circle, rgba(56,189,248,0.14) 0%, transparent 70%);
        pointer-events: none;
    }
    .hero-left { display: flex; align-items: center; gap: 16px; position: relative; z-index: 1; }
    .hero-icon {
        width: 46px; height: 46px; border-radius: 12px;
        background: linear-gradient(135deg, #0ea5e9, #0284c7);
        display: flex; align-items: center; justify-content: center;
        font-size: 1.3rem; flex-shrink: 0;
        box-shadow: 0 4px 16px rgba(14,165,233,0.35);
    }
    .hero-card h1 { color: var(--text-hi); margin: 0; font-size: 1.4rem; font-weight: 800; letter-spacing: -0.01em; }
    .hero-card p  { color: #7fb8dd; margin: 0.3rem 0 0 0; font-size: 0.9rem; }

    /* ── Section label ── */
    .section-label {
        display: flex; align-items: center; justify-content: space-between;
        margin: 1.6rem 0 1rem 0;
    }
    .section-label .sl-left { display: flex; align-items: center; gap: 10px; }
    .section-label .sl-eyebrow {
        color: var(--text-lo) !important; font-size: 0.70rem; font-weight: 700;
        text-transform: uppercase; letter-spacing: 0.12em;
    }
    .section-label .sl-tag {
        font-size: 0.68rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.08em; color: var(--accent-2); padding: 3px 10px;
        border: 1px solid rgba(56,189,248,0.3); border-radius: 20px;
        background: rgba(56,189,248,0.06);
    }
    .section-label .icon {
        width: 30px; height: 30px; background: linear-gradient(135deg, #0ea5e9, #0284c7);
        border-radius: 8px; display: flex; align-items: center; justify-content: center;
        font-size: 0.9rem; flex-shrink: 0;
    }
    .section-label h3 { color: var(--text-hi) !important; margin: 0 !important; font-size: 1.02rem !important; font-weight: 700 !important; border: none !important; padding: 0 !important; }

    /* ── Metric / stat cards ── */
    div[data-testid="stMetric"] {
        background: linear-gradient(135deg, var(--card), var(--card-alt));
        border: 1px solid var(--border); border-radius: 12px;
        padding: 16px 20px; box-shadow: 0 2px 16px rgba(0,0,0,0.35);
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stMetric"]:hover { border-color: rgba(94,179,245,0.35); box-shadow: 0 4px 24px rgba(0,180,255,0.12); }
    div[data-testid="stMetric"] label { color: var(--text-lo) !important; font-size: 0.70rem !important; font-weight: 700 !important; letter-spacing: 0.10em !important; text-transform: uppercase !important; }
    div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: var(--text-hi) !important; font-size: 1.55rem !important; font-weight: 700 !important; }

    /* ── Panel (telemetry card wrapper) ── */
    .panel {
        background: var(--card); border: 1px solid var(--border);
        border-radius: 12px; padding: 18px 20px; margin-bottom: 16px;
        transition: border-color .2s ease;
    }
    .panel:hover { border-color: var(--border-lt); }
    .panel-head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
    .panel-head .ph-left { display: flex; align-items: center; gap: 8px; font-size: 0.82rem; font-weight: 700; color: var(--text-md); }
    .panel-big { font-size: 2rem; font-weight: 800; color: var(--text-hi); line-height: 1; }
    .panel-sub { font-size: 0.80rem; color: var(--text-lo); margin-top: 6px; }

    /* ── Status badges ── */
    .badge {
        display: inline-flex; align-items: center; gap: 5px;
        padding: 3px 10px; border-radius: 20px;
        font-size: 0.68rem; font-weight: 800; letter-spacing: 0.06em; text-transform: uppercase;
    }
    .badge-green  { background: rgba(74,222,128,0.12);  color: var(--green);  border: 1px solid rgba(74,222,128,0.28); }
    .badge-yellow { background: rgba(250,204,21,0.12);  color: var(--yellow); border: 1px solid rgba(250,204,21,0.28); }
    .badge-red    { background: rgba(248,113,113,0.12); color: var(--red);    border: 1px solid rgba(248,113,113,0.28); }
    .badge-blue   { background: rgba(56,189,248,0.12);  color: var(--accent-2); border: 1px solid rgba(56,189,248,0.28); }
    .badge-gray   { background: rgba(100,116,139,0.12); color: #94a3b8; border: 1px solid rgba(100,116,139,0.28); }

    /* ── Intelligence feed cards ── */
    .feed-card {
        background: var(--card); border: 1px solid var(--border);
        border-left: 3px solid var(--border-lt);
        border-radius: 10px; padding: 16px 18px; margin-bottom: 14px;
    }
    .feed-card.severity-critical { border-left-color: var(--red); }
    .feed-card.severity-warning  { border-left-color: var(--yellow); }
    .feed-card.severity-info     { border-left-color: var(--accent-2); }
    .feed-card.severity-success  { border-left-color: var(--green); }
    .feed-title { font-size: 0.95rem; font-weight: 700; color: var(--text-hi); display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
    .feed-body  { font-size: 0.85rem; color: var(--text-md); line-height: 1.5; }
    .feed-reco {
        background: var(--card-alt); border: 1px solid var(--border);
        border-radius: 8px; padding: 12px 14px; margin-top: 12px;
    }
    .feed-reco .fr-label { font-size: 0.66rem; font-weight: 800; letter-spacing: 0.1em; text-transform: uppercase; color: var(--text-lo); margin-bottom: 6px; }
    .feed-reco .fr-text  { font-size: 0.83rem; color: #cbd5e1; line-height: 1.5; }

    /* ── Data card (tasks) ── */
    .data-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 16px 20px; margin-bottom: 10px; transition: border-color .2s ease, box-shadow .2s ease; }
    .data-card:hover { border-color: var(--border-lt); box-shadow: 0 4px 20px rgba(0,0,0,0.3); }
    .card-title { font-size: 0.95rem; font-weight: 700; color: var(--text-hi); margin-bottom: 6px; }
    .card-meta { font-size: 0.78rem; color: var(--text-lo); display: flex; flex-wrap: wrap; gap: 12px; align-items: center; }
    .card-meta-item { display: flex; align-items: center; gap: 4px; }
    .card-meta-item .label { color: var(--text-lo); text-transform: uppercase; font-size: 0.65rem; letter-spacing: 0.07em; font-weight: 700; }
    .card-meta-item .value { color: var(--text-md); }

    /* ── Progress bar ── */
    .progress-wrap { background: var(--card-alt); border-radius: 100px; height: 6px; margin-top: 10px; overflow: hidden; }
    .progress-fill { height: 100%; border-radius: 100px; }
    .progress-fill.low    { background: linear-gradient(90deg, #0ea5e9, #38bdf8); }
    .progress-fill.mid    { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
    .progress-fill.high   { background: linear-gradient(90deg, #10b981, #34d399); }
    .progress-fill.danger { background: linear-gradient(90deg, #ef4444, #f87171); }

    /* ── Team roster cards ── */
    .member-card { background: var(--card); border: 1px solid var(--border); border-radius: 14px; padding: 20px; margin-bottom: 16px; transition: border-color .2s ease; }
    .member-card:hover { border-color: var(--border-lt); }
    .member-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 10px; margin-bottom: 14px; }
    .member-id { display: flex; align-items: center; gap: 12px; }
    .member-avatar {
        width: 44px; height: 44px; border-radius: 10px;
        background: linear-gradient(135deg, #1c2b4a, #101a30);
        border: 1px solid var(--border-lt);
        display: flex; align-items: center; justify-content: center;
        font-weight: 800; font-size: 0.92rem; color: var(--accent-2); flex-shrink: 0;
    }
    .member-name { font-size: 1.02rem; font-weight: 800; color: var(--text-hi); line-height: 1.2; }
    .member-role { font-size: 0.78rem; color: var(--text-lo); margin-top: 1px; }
    .util-row { display: flex; align-items: center; gap: 10px; margin-top: 4px; font-size: 0.78rem; color: var(--text-lo); }
    .util-label-row { display: flex; justify-content: space-between; font-size: 0.78rem; color: var(--text-lo); margin-bottom: 6px; }
    .util-bar-bg { flex: 1; background: var(--card-alt); border-radius: 100px; height: 5px; overflow: hidden; }
    .util-bar-fill { height: 100%; border-radius: 100px; }
    .skill-tag {
        display: inline-block; font-size: 0.72rem; color: var(--text-md);
        background: var(--card-alt); border: 1px solid var(--border);
        padding: 4px 10px; border-radius: 7px; margin: 10px 6px 0 0;
    }

    /* ── Result card (analysis) ── */
    .result-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; height: 100%; }
    .result-card .rc-title { font-size: 0.70rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.10em; color: var(--text-lo); margin-bottom: 12px; padding-bottom: 10px; border-bottom: 1px solid var(--border); }
    .result-card .rc-value { font-size: 0.90rem; color: #cbd5e1; line-height: 1.55; }

    /* ── Conflict / info / warn banners ── */
    .conflict-card { background: rgba(245,158,11,0.06); border: 1px solid rgba(245,158,11,0.25); border-left: 3px solid #f59e0b; border-radius: 10px; padding: 14px 18px; margin-bottom: 12px; }
    .conflict-card .cc-issue { color: var(--yellow); font-weight: 700; font-size: 0.9rem; margin-bottom: 6px; }
    .conflict-card .cc-rec   { color: var(--text-md); font-size: 0.85rem; line-height: 1.5; }
    .info-banner { background: rgba(56,189,248,0.06); border: 1px solid rgba(56,189,248,0.2); border-radius: 10px; padding: 14px 18px; color: #7dd3fc; font-size: 0.88rem; display: flex; align-items: center; gap: 10px; }
    .warn-banner { background: rgba(245,158,11,0.07); border: 1px solid rgba(245,158,11,0.25); border-left: 3px solid #f59e0b; border-radius: 10px; padding: 12px 16px; color: var(--yellow); font-size: 0.85rem; margin-bottom: 8px; }

    /* ── Divider label ── */
    .divider-label { display: flex; align-items: center; gap: 12px; margin: 1.6rem 0 1.2rem; }
    .divider-label span { color: var(--text-lo); font-size: 0.70rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.10em; white-space: nowrap; }
    .divider-label::before, .divider-label::after { content: ""; flex: 1; height: 1px; background: var(--border); }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #0ea5e9, #0284c7) !important;
        color: #ffffff !important; border: none !important; border-radius: 8px !important;
        font-weight: 700 !important; font-size: 0.85rem !important; letter-spacing: 0.02em !important;
        padding: 0.45rem 1.1rem !important; transition: all .2s ease !important;
        box-shadow: 0 2px 8px rgba(14,165,233,0.3) !important;
    }
    .stButton > button:hover { background: linear-gradient(135deg, #38bdf8, #0ea5e9) !important; box-shadow: 0 4px 16px rgba(14,165,233,0.45) !important; transform: translateY(-1px) !important; }
    .stButton > button[kind="secondary"] { background: var(--card-alt) !important; box-shadow: none !important; color: var(--text-md) !important; border: 1px solid var(--border) !important; }
    .stButton > button[kind="secondary"]:hover { background: #1c2440 !important; color: var(--text-hi) !important; transform: none !important; }
    .stFormSubmitButton > button { background: linear-gradient(135deg, #0ea5e9, #0284c7) !important; color: #fff !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; box-shadow: 0 2px 8px rgba(14,165,233,0.3) !important; }
    .stFormSubmitButton > button:hover { background: linear-gradient(135deg, #38bdf8, #0ea5e9) !important; box-shadow: 0 4px 16px rgba(14,165,233,0.45) !important; }

    /* ── Containers ── */
    div[data-testid="stVerticalBlockBorderWrapper"] { background: var(--card) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; box-shadow: 0 2px 12px rgba(0,0,0,0.3) !important; transition: border-color .2s ease !important; }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover { border-color: var(--border-lt) !important; }

    /* ── Inputs ── */
    .stTextInput > div > div > input, .stNumberInput > div > div > input, .stTextArea > div > div > textarea {
        background-color: var(--card) !important; border: 1px solid var(--border) !important; color: var(--text-hi) !important; border-radius: 8px !important; font-size: 0.9rem !important;
    }
    .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus, .stTextArea > div > div > textarea:focus {
        border-color: var(--accent-2) !important; box-shadow: 0 0 0 2px rgba(56,189,248,0.2) !important;
    }
    .stSelectbox > div > div, div[data-baseweb="select"] > div { background-color: var(--card) !important; border-color: var(--border) !important; color: var(--text-hi) !important; border-radius: 8px !important; }
    .stSlider [data-baseweb="slider"] div[role="slider"] { background-color: var(--accent-2) !important; border-color: var(--accent-2) !important; }
    .stDateInput > div > div > input { background-color: var(--card) !important; border: 1px solid var(--border) !important; color: var(--text-hi) !important; border-radius: 8px !important; }

    /* ── Expander / form ── */
    details[data-testid="stExpander"] { background: var(--panel) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; overflow: hidden !important; }
    details[data-testid="stExpander"] summary { color: var(--text-lo) !important; font-weight: 700 !important; font-size: 0.80rem !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; padding: 0.8rem 1rem !important; }
    details[data-testid="stExpander"] summary:hover { color: var(--text-hi) !important; background: var(--card) !important; }
    div[data-testid="stForm"] { background: var(--panel) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; padding: 1rem !important; }

    div[data-testid="stAlert"] { border-radius: 10px !important; border-left-width: 4px !important; font-size: 0.88rem !important; }
    h2, h3 { color: var(--text-hi) !important; font-weight: 700 !important; letter-spacing: -0.01em !important; }
    h2 { font-size: 1.15rem !important; border-bottom: 1px solid var(--border); padding-bottom: 0.5rem; margin-bottom: 1rem !important; }
    .stCaptionContainer, small { color: var(--text-lo) !important; font-size: 0.82rem !important; }
    hr { border-color: var(--border) !important; }

    div[data-testid="stTable"] table { background-color: var(--card) !important; border-radius: 10px !important; overflow: hidden !important; border: 1px solid var(--border) !important; }
    div[data-testid="stTable"] th { background-color: var(--panel) !important; color: var(--text-lo) !important; font-size: 0.72rem !important; font-weight: 700 !important; letter-spacing: 0.08em !important; text-transform: uppercase !important; border-bottom: 1px solid var(--border) !important; padding: 10px 14px !important; }
    div[data-testid="stTable"] td { color: #cbd5e1 !important; border-bottom: 1px solid var(--card-alt) !important; padding: 10px 14px !important; font-size: 0.88rem !important; }
    div[data-testid="stTable"] tr:hover td { background: var(--card-alt) !important; }
    div[data-testid="stJson"] { background: var(--panel) !important; border: 1px solid var(--border) !important; border-radius: 10px !important; }
    div[data-testid="stSidebar"] .stSuccess { background: #0c1f1a !important; border: 1px solid #134e2e !important; border-radius: 8px !important; color: var(--green) !important; }

    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: var(--bg); }
    ::-webkit-scrollbar-thumb { background: var(--border-lt); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--accent-2); }
    .stSpinner > div { border-top-color: var(--accent-2) !important; }

    .empty-state { text-align: center; padding: 3rem 2rem; background: var(--panel); border: 1px dashed var(--border); border-radius: 14px; color: var(--text-lo); }
    .empty-state .es-icon { font-size: 2.5rem; margin-bottom: 12px; }
    .empty-state .es-title { color: var(--text-md); font-size: 0.95rem; font-weight: 600; margin-bottom: 4px; }
    .empty-state .es-sub   { color: var(--text-lo); font-size: 0.82rem; }

    .budget-stat { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 20px; text-align: center; }
    .budget-stat .bs-label { font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.10em; font-weight: 700; color: var(--text-lo); }
    .budget-stat .bs-value { font-size: 1.5rem; font-weight: 800; color: var(--text-hi); margin: 6px 0; }
    .budget-stat .bs-sub   { font-size: 0.78rem; color: var(--text-md); }
</style>
""", unsafe_allow_html=True)


def initials(name: str) -> str:
    parts = [p for p in name.strip().split(" ") if p]
    if not parts:
        return "?"
    if len(parts) == 1:
        return parts[0][:2].upper()
    return (parts[0][0] + parts[-1][0]).upper()


# ══════════════════════════════════════════════════════════════
# AUTHENTICATION GATE
# ══════════════════════════════════════════════════════════════
if "user_id" not in st.session_state:
    st.markdown("""
    <div style="max-width: 420px; margin: 4rem auto 0 auto; text-align: center;">
        <div class="brand-icon" style="margin: 0 auto 14px auto; width:56px; height:56px; font-size:1.7rem;">🛡️</div>
        <div class="brand-name" style="font-size:1.6rem;">Aegis</div>
        <p style="color: #56617a; margin-top: 6px;">AI Agent Coordination &amp; Decision Engine</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        tab1, tab2, tab3 = st.tabs(["Log In", "Sign Up", "Forgot Password"])

        with tab1:
            with st.form("login_form"):
                login_username = st.text_input("Username")
                login_password = st.text_input("Password", type="password")
                if st.form_submit_button("Log In", type="primary"):
                    user_id = verify_user(login_username, login_password)
                    if user_id:
                        st.session_state["user_id"] = user_id
                        st.session_state["username"] = login_username
                        st.rerun()
                    else:
                        st.error("Invalid username or password")

        with tab2:
            with st.form("signup_form"):
                new_username = st.text_input("Choose a username")
                new_password = st.text_input("Choose a password", type="password")
                confirm_password = st.text_input("Confirm password", type="password")
                security_question = st.selectbox("Security question", [
                    "What is your favorite color?",
                    "What is your pet's name?",
                    "What city were you born in?",
                    "What is your favorite food?"
                ])
                security_answer = st.text_input("Answer")
                if st.form_submit_button("Sign Up", type="primary"):
                    if not new_username.strip() or not new_password:
                        st.error("Username and password are required")
                    elif new_password != confirm_password:
                        st.error("Passwords do not match")
                    elif not security_answer.strip():
                        st.error("Please answer the security question")
                    else:
                        try:
                            user_id = create_user(new_username.strip(), new_password, security_question, security_answer.strip())
                            st.session_state["user_id"] = user_id
                            st.session_state["username"] = new_username.strip()
                            st.success("Account created! Redirecting...")
                            st.rerun()
                        except ValueError as e:
                            st.error(str(e))

        with tab3:
            if "reset_username" not in st.session_state:
                with st.form("find_account_form"):
                    reset_username_input = st.text_input("Enter your username")
                    if st.form_submit_button("Find Account"):
                        question = get_security_question(reset_username_input)
                        if question:
                            st.session_state["reset_username"] = reset_username_input
                            st.session_state["reset_question"] = question
                            st.rerun()
                        else:
                            st.error("Username not found or no security question set")
            else:
                st.info(f"Security question for **{st.session_state['reset_username']}**:")
                st.write(f"*{st.session_state['reset_question']}*")
                with st.form("reset_password_form"):
                    answer = st.text_input("Your answer")
                    new_pw = st.text_input("New password", type="password")
                    confirm_pw = st.text_input("Confirm new password", type="password")
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if st.form_submit_button("Reset Password", type="primary"):
                            if new_pw != confirm_pw:
                                st.error("Passwords do not match")
                            elif not new_pw:
                                st.error("Enter a new password")
                            else:
                                success = reset_password(st.session_state["reset_username"], answer, new_pw)
                                if success:
                                    st.success("Password reset successfully! Please log in.")
                                    st.session_state.pop("reset_username", None)
                                    st.session_state.pop("reset_question", None)
                                else:
                                    st.error("Incorrect answer")
                    with col_b:
                        if st.form_submit_button("Cancel"):
                            st.session_state.pop("reset_username", None)
                            st.session_state.pop("reset_question", None)
                            st.rerun()

    st.stop()

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
username = st.session_state.get("username", "user")
st.sidebar.markdown(f"""
<div class="brand-block">
    <div class="brand-icon">🛡️</div>
    <div>
        <div class="brand-name">Aegis</div>
        <div class="brand-sub">Enterprise Tier</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown(f"""
<div class="user-chip">
    <div class="user-avatar">{initials(username)}</div>
    <div>
        <div class="user-name">{username}</div>
        <div class="user-role">Signed in</div>
    </div>
</div>
""", unsafe_allow_html=True)
 

active_id   = st.session_state.get("active_project_id")
active_name = st.session_state.get("active_project_name")

# ══════════════════════════════════════════════════════════════
# NO PROJECT SELECTED → clean, focused picker (not cluttered sidebar)
# ══════════════════════════════════════════════════════════════
if not active_id:
    st.sidebar.markdown("---")
    st.sidebar.info("Select or create a project to begin.")

    st.markdown("""
    <div class="hero-card">
        <div class="hero-left">
            <div class="hero-icon">🛡️</div>
            <div>
                <h1>Aegis Decision Engine</h1>
                <p>Multi-agent risk, resource, and budget analysis for project managers</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_open, tab_new = st.tabs(["📂  Open Existing Project", "＋  Create New Project"])

    with tab_open:
        existing_projects = list_projects()
        project_names = {p["name"]: p["id"] for p in existing_projects}
        if project_names:
            selected = st.selectbox("Select a project", list(project_names.keys()))
            if st.button("Open Project", type="primary"):
                st.session_state["active_project_id"] = project_names[selected]
                st.session_state["active_project_name"] = selected
                st.rerun()
        else:
            st.info("No projects yet — switch to the 'Create New Project' tab.")

    with tab_new:
        with st.form("create_project_form"):
            new_name = st.text_input("Project name")
            new_description = st.text_area(
                "Project description",
                placeholder="e.g. Build a payment gateway integration for an e-commerce checkout flow, including frontend cart UI and backend webhook handling."
            )
            new_start = st.date_input("Start date")
            new_end = st.date_input("End date")
            use_ai_planning = st.checkbox("🤖 Auto-generate tasks and team assignments from this description", value=True)

            if st.form_submit_button("Create Project", type="primary"):
                if new_name.strip():
                    from db.repository import create_project_with_description, copy_default_team_to_project, save_generated_tasks
                    from db.default_team import DEFAULT_TEAM

                    pid = create_project_with_description(new_name.strip(), new_description.strip(), str(new_start), str(new_end))

                    if use_ai_planning and new_description.strip():
                        from agents.planning_agent import generate_task_breakdown
                        with st.spinner("AI is breaking down your project into tasks..."):
                            generated = generate_task_breakdown(new_description.strip(), DEFAULT_TEAM)
                            if generated:
                                assigned_names = {t.get("assigned_to") for t in generated if t.get("assigned_to")}
                                relevant_team = [m for m in DEFAULT_TEAM if m["name"] in assigned_names]
                                copy_default_team_to_project(pid, relevant_team)
                                save_generated_tasks(pid, generated, default_deadline=str(new_end))
                                st.success(f"Created project and generated {len(generated)} tasks, assigned to {len(relevant_team)} team member(s)")
                            else:
                                st.warning("Project created, but AI task generation didn't return valid results. You can add tasks manually.")
                    # else: no AI planning - project starts with an empty team, added manually

                    st.session_state["active_project_id"] = pid
                    st.session_state["active_project_name"] = new_name.strip()
                    st.rerun()
                else:
                    st.error("Enter a project name")
    st.stop()



# ══════════════════════════════════════════════════════════════
# PROJECT SELECTED → clean active-project card + navigation
# ══════════════════════════════════════════════════════════════
st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div class="panel" style="padding:14px 16px;margin-bottom:10px;">
    <div class="nav-label" style="margin:0 0 4px 0;">Active Project</div>
    <div style="font-size:0.98rem;font-weight:800;color:var(--text-hi);">{active_name}</div>
</div>
""", unsafe_allow_html=True)

if st.sidebar.button("↔ Switch Project", use_container_width=True):
    st.session_state.pop("active_project_id", None)
    st.session_state.pop("active_project_name", None)
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown('<div class="nav-label">Navigation</div>', unsafe_allow_html=True)

NAV_ITEMS = {
    "Overview":     ":material/dashboard: Overview",
    "Tasks":        ":material/task_alt: Tasks",
    "Team":         ":material/group: Team",
    "Budget":       ":material/payments: Budget",
    "Run Analysis": ":material/neurology: AI Engine",
    "History":      ":material/history: History",
}
nav_choice = st.sidebar.radio("Go to", list(NAV_ITEMS.values()), label_visibility="collapsed")
page = [k for k, v in NAV_ITEMS.items() if v == nav_choice][0]
st.sidebar.markdown("---")
st.sidebar.markdown('<div class="nav-label">Quick Action</div>', unsafe_allow_html=True)
mock_mode = st.sidebar.checkbox("Mock mode (no API calls)", value=True)
os.environ["USE_MOCK_AGENT"] = "1" if mock_mode else "0"

st.sidebar.markdown("---")
if st.sidebar.button("Log Out", use_container_width=True):
    st.session_state.pop("user_id", None)
    st.session_state.pop("username", None)
    st.session_state.pop("active_project_id", None)
    st.session_state.pop("active_project_name", None)
    st.rerun()
# ══════════════════════════════════════════════════════════════
# TOP BAR (search + notifications + settings + avatar)
# ══════════════════════════════════════════════════════════════
tb1, tb2, tb3 = st.columns([2.4, 3, 1.4])
with tb1:
    st.markdown(f"""
    <div class="topbar-title">
        <div class="tt-name">{active_name}</div>
        <div class="tt-sub">AI Agent Coordination &amp; Decision Engine</div>
    </div>
    """, unsafe_allow_html=True)
with tb2:
    quick_search = st.text_input("Search", placeholder="🔍  Search tasks, team members…", label_visibility="collapsed")
with tb3:
    icon_col1, icon_col2, icon_col3 = st.columns([1, 1, 1])
    with icon_col1:
        st.markdown('<div class="tb-icon">🔔</div>', unsafe_allow_html=True)
    with icon_col2:
        if st.button("⚙️", key="settings_toggle", help="Project Settings"):
            st.session_state["show_settings"] = not st.session_state.get("show_settings", False)
    with icon_col3:
        st.markdown(f'<div class="user-avatar" style="width:38px;height:38px;">{initials(username)}</div>', unsafe_allow_html=True)

if st.session_state.get("show_settings", False):
    with st.container(border=True):
        st.markdown('<div class="section-label"><div class="sl-left"><div class="icon">⚙️</div><h3>Project Settings</h3></div></div>', unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        with s1:
            with st.form("rename_form"):
                new_project_name = st.text_input("Rename project", value=active_name)
                if st.form_submit_button("Rename Project"):
                    if new_project_name.strip() and new_project_name.strip() != active_name:
                        from db.repository import rename_project
                        rename_project(active_id, new_project_name.strip())
                        st.session_state["active_project_name"] = new_project_name.strip()
                        st.success("Renamed")
                        st.rerun()
        with s2:
            st.caption("⚠️ This permanently deletes the project and all its data.")
            confirm_delete = st.checkbox("I understand this cannot be undone")
            if st.button("🗑️ Delete This Project", disabled=not confirm_delete, type="secondary"):
                from db.repository import delete_project
                delete_project(active_id)
                st.session_state.pop("active_project_id", None)
                st.session_state.pop("active_project_name", None)
                st.session_state.pop("show_settings", None)
                st.success("Project deleted")
                st.rerun()

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# OVERVIEW
# ══════════════════════════════════════════════════════════════
if page == "Overview":
    summary     = get_project_summary(active_id)
    budget_data = get_latest_budget_entry(active_id)

    from db.repository import get_project_dates
    from tools.budget_tools import calculate_pct_time_elapsed, check_budget_status

    dates = get_project_dates(active_id)
    live_pct_time = 0
    if dates and dates["start_date"] and dates["end_date"]:
        live_pct_time = calculate_pct_time_elapsed(dates["start_date"], dates["end_date"])

    budget_status = "Not Set"
    if budget_data:
        result = check_budget_status(budget_data["planned_spend"], budget_data["actual_spend"], live_pct_time)
        if result.startswith("over_budget"):
            budget_status = "⚠️ Over Budget"
        elif result.startswith("at_risk"):
            budget_status = "🟡 At Risk"
        else:
            budget_status = "✅ On Budget"

    # ── Hero: Engine status card ──
    hcol1, hcol2 = st.columns([3, 1])
    with hcol1:
        tasks_for_hero = get_tasks(active_id)
        team_for_hero = get_team_members(active_id)
        st.markdown(f"""
        <div class="hero-card" style="margin-bottom:1.6rem;">
            <div class="hero-left">
                <div class="hero-icon">🧠</div>
                <div>
                    <h1>Cognitive Engine Status</h1>
                    <p>Ready to process {len(tasks_for_hero)} task(s) across {len(team_for_hero)} team member(s).</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with hcol2:
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        if st.button("▶  Execute Analysis", type="primary", use_container_width=True):
            st.session_state["_jump_to_analysis"] = True
            st.info("Head to the AI Engine tab in the sidebar to view full results.")

    # KPI row
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tasks",   summary["task_count"])
    col2.metric("Team Members",  summary["team_count"])
    col3.metric("Budget Status", budget_status)
    col4.metric("Last Analysis", summary["last_analysis"].strftime("%b %d, %H:%M") if summary["last_analysis"] else "Never")

    from db.repository import get_last_data_change
    last_data_change = get_last_data_change(active_id)
    last_analysis_time = summary["last_analysis"]

    if last_data_change and last_analysis_time and last_data_change > last_analysis_time:
        st.markdown("""
        <div class="warn-banner">
            ⚠ Data has changed since your last analysis was run. Results shown elsewhere may be outdated — go to AI Engine to refresh.
        </div>
        """, unsafe_allow_html=True)
    elif last_data_change and not last_analysis_time:
        st.markdown("""
        <div class="warn-banner">
            ⚠ You have data but haven't run analysis yet. Go to AI Engine to generate insights.
        </div>
        """, unsafe_allow_html=True)

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

    # ── Agent telemetry + Intelligence feed (two column layout like reference) ──
    tasks     = get_tasks(active_id)
    team      = get_team_members(active_id)
    team_names = {t["name"] for t in team}
    task_ids   = {t["id"] for t in tasks}

    overloaded = [m for m in team if m["capacity_hrs_week"] and (m["logged_hrs_week"] / m["capacity_hrs_week"]) >= 0.9]
    avg_util = 0
    if team:
        avg_util = sum((m["logged_hrs_week"] / m["capacity_hrs_week"] * 100) if m["capacity_hrs_week"] else 0 for m in team) / len(team)

    warnings = []
    for task in tasks:
        if task["assigned_to"] and task["assigned_to"] not in team_names:
            warnings.append({"issue": f"Task {task['id']} unassigned owner",
                              "body": f"Task <b>{task['id']}</b> is assigned to <b>'{task['assigned_to']}'</b> — not found in the team roster.",
                              "severity": "warning"})
        for dep in task["depends_on"]:
            if dep not in task_ids:
                warnings.append({"issue": f"Task {task['id']} broken dependency",
                                  "body": f"Task <b>{task['id']}</b> depends on <b>'{dep}'</b> — this task does not exist.",
                                  "severity": "critical"})

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown("""
        <div class="section-label">
            <div class="sl-left"><span class="sl-eyebrow">Agent Telemetry</span></div>
            <span class="sl-tag">Live Sync</span>
        </div>
        """, unsafe_allow_html=True)

        tcol1, tcol2 = st.columns(2)
        with tcol1:
            risk_level = "ELEVATED" if warnings else "NOMINAL"
            risk_badge = "badge-red" if warnings else "badge-green"
            st.markdown(f"""
            <div class="panel">
                <div class="panel-head">
                    <div class="ph-left">⚠️ Risk Vector</div>
                    <span class="badge {risk_badge}">{risk_level}</span>
                </div>
                <div class="panel-big">{len(warnings)}</div>
                <div class="panel-sub">Open data issue(s) detected</div>
            </div>
            """, unsafe_allow_html=True)
        with tcol2:
            wl_status = "OPTIMAL" if not overloaded else "AT RISK"
            wl_badge = "badge-blue" if not overloaded else "badge-red"
            st.markdown(f"""
            <div class="panel">
                <div class="panel-head">
                    <div class="ph-left">👥 Workload</div>
                    <span class="badge {wl_badge}">{wl_status}</span>
                </div>
                <div class="panel-big">{avg_util:.0f}%</div>
                <div class="panel-sub">Avg. team utilization &middot; {len(overloaded)} overloaded</div>
            </div>
            """, unsafe_allow_html=True)

        if budget_data:
            spend_pct = (budget_data['actual_spend'] / budget_data['planned_spend'] * 100) if budget_data['planned_spend'] else 0
            under = spend_pct <= live_pct_time
            st.markdown(f"""
            <div class="panel">
                <div class="panel-head"><div class="ph-left">💳 Burn Rate vs Allocation</div></div>
                <div style="display:flex; justify-content:space-between; align-items:baseline;">
                    <div>
                        <span style="color:var(--text-md); font-size:0.85rem;">Spend</span>
                        <span style="color:var(--text-hi); font-weight:700; margin-left:8px;">₹{budget_data['actual_spend']:,.0f} / ₹{budget_data['planned_spend']:,.0f}</span>
                    </div>
                    <div style="color:{'#4ade80' if under else '#f87171'}; font-weight:800;">{spend_pct - live_pct_time:+.1f}%</div>
                </div>
                <div class="progress-wrap"><div class="progress-fill {'low' if under else 'danger'}" style="width:{min(spend_pct,100):.0f}%;"></div></div>
                <div class="panel-sub">{"Under budget pace" if under else "Ahead of timeline pace"}</div>
            </div>
            """, unsafe_allow_html=True)

        pcol1, pcol2 = st.columns(2)
        with pcol1:
            st.markdown(f"""
            <div class="panel">
                <div class="panel-head"><div class="ph-left">🧩 Process Health</div></div>
                <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                    <span style="color:var(--text-md); font-size:0.85rem;">Active Blockers</span>
                    <span class="badge badge-yellow">{len(warnings)}</span>
                </div>
                <div style="display:flex; justify-content:space-between;">
                    <span style="color:var(--text-md); font-size:0.85rem;">Avg Task Progress</span>
                    <span style="color:var(--text-hi); font-weight:700;">{(sum(t['progress_pct'] for t in tasks)/len(tasks)):.0f}%</span>
                </div>
            </div>
            """ if tasks else """
            <div class="panel">
                <div class="panel-head"><div class="ph-left">🧩 Process Health</div></div>
                <div class="panel-sub">No tasks yet.</div>
            </div>
            """, unsafe_allow_html=True)
        with pcol2:
            st.markdown(f"""
            <div class="panel" style="text-align:center;">
                <div class="panel-head" style="justify-content:center;"><div class="ph-left">🔗 Resource Spline</div></div>
                <div class="panel-big" style="font-size:1.1rem;">{len(team)} Node(s)</div>
                <div class="panel-sub">Active team allocation graph</div>
            </div>
            """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="section-label">
            <div class="sl-left"><span class="sl-eyebrow">Intelligence Feed</span></div>
        </div>
        """, unsafe_allow_html=True)

        if warnings:
            for w in warnings:
                sev_cls = "severity-critical" if w["severity"] == "critical" else "severity-warning"
                st.markdown(f"""
                <div class="feed-card {sev_cls}">
                    <div class="feed-title">⚠️ {w['issue']}</div>
                    <div class="feed-body">{w['body']}</div>
                </div>
                """, unsafe_allow_html=True)

        if overloaded:
            names = ", ".join(m["name"] for m in overloaded)
            st.markdown(f"""
            <div class="feed-card severity-warning">
                <div class="feed-title">🧑‍💻 Resource Bottleneck</div>
                <div class="feed-body">{names} {'is' if len(overloaded)==1 else 'are'} at or above 90% capacity this week.</div>
                <div class="feed-reco">
                    <div class="fr-label">AI Recommendation</div>
                    <div class="fr-text">Re-balance tasks toward team members under 70% utilization, or extend the deadline for affected tasks.</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        if budget_data:
            spend_pct = (budget_data['actual_spend'] / budget_data['planned_spend'] * 100) if budget_data['planned_spend'] else 0
            if spend_pct <= live_pct_time:
                st.markdown(f"""
                <div class="feed-card severity-success">
                    <div class="feed-title">✅ Budget Optimization Found</div>
                    <div class="feed-body">Spend is tracking {live_pct_time - spend_pct:.1f} points under the elapsed timeline — comfortable buffer remains.</div>
                    <div style="margin-top:10px;"><span style="color:var(--accent-2); font-size:0.82rem; font-weight:700;">View details →</span></div>
                </div>
                """, unsafe_allow_html=True)

        if not warnings and not overloaded:
            st.markdown("""
            <div class="feed-card severity-success">
                <div class="feed-title">✅ All Systems Nominal</div>
                <div class="feed-body">No conflicts, bottlenecks, or data issues detected across tasks and team.</div>
            </div>
            """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# TASKS
# ══════════════════════════════════════════════════════════════
elif page == "Tasks":
    st.markdown('<div class="section-label"><div class="sl-left"><div class="icon">📋</div><h3>Task Management</h3></div></div>', unsafe_allow_html=True)

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

    if quick_search:
        q = quick_search.lower()
        current_tasks = [t for t in current_tasks if q in t["id"].lower() or q in t["name"].lower() or q in (t["assigned_to"] or "").lower()]

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

# ══════════════════════════════════════════════════════════════
# TEAM
# ══════════════════════════════════════════════════════════════
elif page == "Team":
    header_l, header_r = st.columns([3, 1])
    with header_l:
        st.markdown('<div class="section-label"><div class="sl-left"><div class="icon">👥</div><h3>Team Roster</h3></div></div>', unsafe_allow_html=True)

    current_team_all = get_team_members_with_db_id(active_id)
    total_members = len(current_team_all)
    avg_util_all = 0
    if current_team_all:
        avg_util_all = sum(min((m["logged_hrs_week"] / (m["capacity_hrs_week"] or 1) * 100), 999) for m in current_team_all) / total_members

    scol1, scol2 = st.columns(2)
    scol1.metric("Total Members", total_members)
    scol2.metric("Avg Utilization", f"{avg_util_all:.0f}%")

    fcol, ccol = st.columns([1, 2])
    with fcol:
        with st.expander("＋  Add New Team Member", expanded=(total_members == 0)):
            with st.form("member_form", clear_on_submit=True):
                mname    = st.text_input("Full Name", placeholder="e.g. Jane Doe")
                role_sel = st.selectbox("Role", ["Engineer", "Designer", "Data Scientist", "Security Analyst", "Project Manager", "QA"])
                capacity = st.number_input("Weekly Capacity (hrs)", value=40.0)
                logged     = st.number_input("Logged Hours This Week", value=0.0)
                skills_raw = st.text_input("Primary Skills (comma separated)", placeholder="Python, AWS, React")
                if st.form_submit_button("Provision Access", use_container_width=True):
                    if mname.strip():
                        skills = [s.strip() for s in skills_raw.split(",") if s.strip()]
                        add_team_member(active_id, mname.strip(), capacity, logged, skills)
                        st.success(f"**{mname}** added to the team.")
                        st.rerun()
                    else:
                        st.error("Name is required.")

        with st.expander("📥  Bulk Import Team (upload JSON)"):
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

    with ccol:
        current_team = current_team_all
        if quick_search:
            q = quick_search.lower()
            current_team = [m for m in current_team if q in m["name"].lower() or any(q in s.lower() for s in m["skills"])]

        if not current_team:
            st.markdown("""
            <div class="empty-state">
                <div class="es-icon">🧑‍💼</div>
                <div class="es-title">No team members yet</div>
                <div class="es-sub">Add your first team member from the panel on the left.</div>
            </div>""", unsafe_allow_html=True)
        else:
            grid_cols = st.columns(2)
            for idx, member in enumerate(current_team):
                cap  = member["capacity_hrs_week"] or 1
                log  = member["logged_hrs_week"]
                pct  = min((log / cap * 100), 999)
                if pct >= 100:  util_color, util_label, badge_cls = "#f87171", "Overloaded", "badge-red"
                elif pct >= 85: util_color, util_label, badge_cls = "#fbbf24", "High", "badge-yellow"
                elif pct >= 40: util_color, util_label, badge_cls = "#38bdf8", "Optimal", "badge-blue"
                else:            util_color, util_label, badge_cls = "#4ade80", "Available", "badge-green"

                skills_html = "".join(f'<span class="skill-tag">{s}</span>' for s in member["skills"]) if member["skills"] else '<span class="skill-tag">No skills tagged</span>'

                with grid_cols[idx % 2]:
                    st.markdown(f"""
                    <div class="member-card">
                        <div class="member-head">
                            <div class="member-id">
                                <div class="member-avatar">{initials(member['name'])}</div>
                                <div>
                                    <div class="member-name">{member['name']}</div>
                                    <div class="member-role">Team Member</div>
                                </div>
                            </div>
                            <span class="badge {badge_cls}">{util_label}</span>
                        </div>
                        <div class="util-label-row"><span>Utilization</span><span style="color:{util_color};font-weight:700;">{pct:.0f}%</span></div>
                        <div class="util-bar-bg"><div class="util-bar-fill" style="width:{min(pct,100)}%;background:{util_color};"></div></div>
                        <div style="text-align:right; font-size:0.72rem; color:var(--text-lo); margin-top:4px;">{log:.0f} / {cap:.0f} Hrs</div>
                        <div>{skills_html}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    ecol1, ecol2 = st.columns([1, 1])
                    with ecol1:
                        edit_key = f"edit_member_{member['db_id']}"
                        if st.button("Edit", key=f"btn_{edit_key}", use_container_width=True):
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

# ══════════════════════════════════════════════════════════════
# BUDGET
# ══════════════════════════════════════════════════════════════
elif page == "Budget":
    st.markdown('<div class="section-label"><div class="sl-left"><div class="icon">💰</div><h3>Budget</h3></div></div>', unsafe_allow_html=True)

    from db.repository import get_project_dates, update_project_dates
    from tools.budget_tools import calculate_pct_time_elapsed

    dates = get_project_dates(active_id)
    if dates and dates["start_date"] and dates["end_date"]:
        pct_time = calculate_pct_time_elapsed(dates["start_date"], dates["end_date"])
        st.markdown(f"""
        <div class="info-banner">
            <span>🗓️</span>
            <span>Timeline: {dates['start_date']} to {dates['end_date']} — <b>{pct_time:.1f}%</b> elapsed (calculated automatically)</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="warn-banner">⚠ This project has no start/end date set. Timeline % cannot be calculated automatically.</div>
        """, unsafe_allow_html=True)
        pct_time = 0.0

    with st.expander("Edit Project Timeline (e.g. if deadline is extended)"):
        with st.form("edit_dates_form"):
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

    st.markdown('<div class="divider-label"><span>Current Snapshot</span></div>', unsafe_allow_html=True)
    if current_budget:
        b1, b2, b3 = st.columns(3)
        spend_pct = (current_budget['actual_spend'] / current_budget['planned_spend'] * 100) if current_budget['planned_spend'] else 0
        with b1:
            st.markdown(f"""<div class="budget-stat"><div class="bs-label">Planned Spend</div><div class="bs-value">₹{current_budget['planned_spend']:,.0f}</div><div class="bs-sub">Total budget</div></div>""", unsafe_allow_html=True)
        with b2:
            st.markdown(f"""<div class="budget-stat"><div class="bs-label">Actual Spend</div><div class="bs-value">₹{current_budget['actual_spend']:,.0f}</div><div class="bs-sub">{spend_pct:.1f}% of plan</div></div>""", unsafe_allow_html=True)
        with b3:
            st.markdown(f"""<div class="budget-stat"><div class="bs-label">Timeline Elapsed</div><div class="bs-value">{pct_time:.1f}%</div><div class="bs-sub">Auto-calculated</div></div>""", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="es-icon">💳</div>
            <div class="es-title">No budget set yet</div>
            <div class="es-sub">Enter planned and actual spend below.</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider-label"><span>Update Budget</span></div>', unsafe_allow_html=True)
    with st.form("budget_form"):
        planned = st.number_input("Planned Spend (₹)", value=current_budget["planned_spend"] if current_budget else 50000.0)
        actual = st.number_input("Actual Spend (₹)", value=current_budget["actual_spend"] if current_budget else 0.0)
        st.caption(f"Timeline elapsed: {pct_time:.1f}% (auto-calculated from project dates)")
        if st.form_submit_button("Save Budget"):
            add_budget_entry(active_id, planned, actual, pct_time)
            st.success("Budget saved")
            st.rerun()

# ══════════════════════════════════════════════════════════════
# RUN ANALYSIS (AI ENGINE)
# ══════════════════════════════════════════════════════════════
elif page == "Run Analysis":
    tasks  = get_tasks(active_id)
    team   = get_team_members(active_id)
    budget = get_latest_budget_entry(active_id)

    hcol1, hcol2 = st.columns([3, 1])
    with hcol1:
        st.markdown(f"""
        <div class="hero-card">
            <div class="hero-left">
                <div class="hero-icon">🤖</div>
                <div>
                    <h1>Cognitive Engine Status</h1>
                    <p>Ready to process {len(tasks)} task(s) and evaluate {len(team)} team member profile(s).</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    from db.repository import get_last_data_change
    last_data_change = get_last_data_change(active_id)
    summary_check = get_project_summary(active_id)
    if last_data_change and summary_check["last_analysis"] and last_data_change > summary_check["last_analysis"]:
        st.markdown("""
        <div class="warn-banner">
            ⚠ Data has changed since the last analysis. Click "Execute Analysis" below to get up-to-date results.
        </div>
        """, unsafe_allow_html=True)

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
        run_col, _ = st.columns([1, 3])
        with run_col:
            run_clicked = st.button("▶  Execute Analysis", type="primary", use_container_width=True)

        if run_clicked:
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
                    <div class="feed-card severity-critical">
                        <div class="feed-title">⚡ {c['issue']}</div>
                        <div class="feed-reco">
                            <div class="fr-label">AI Recommendation</div>
                            <div class="fr-text">{c['recommendation']}</div>
                        </div>
                    </div>""", unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="feed-card severity-success">
                    <div class="feed-title">✅ No Conflicts Detected</div>
                    <div class="feed-body">All agents report healthy project status.</div>
                </div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="info-banner">
                <span>🔍</span>
                <span>Ready to analyze <b>{len(tasks)} task(s)</b> across <b>{len(team)} team member(s)</b>. Click "Execute Analysis" to run all agents.</span>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# HISTORY
# ══════════════════════════════════════════════════════════════
elif page == "History":
    st.markdown('<div class="section-label"><div class="sl-left"><div class="icon">🕑</div><h3>Analysis History</h3></div></div>', unsafe_allow_html=True)

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
