"""
db/repository.py

Data access layer. All reads/writes to the database go through these
functions. Field names match the raw inputs tools/*.py expect --
percentages (utilization, budget status) are computed by the tools,
not stored pre-computed here.
"""
import bcrypt
from typing import List, Dict, Any, Optional
from db.session import get_session
from db.models import Project, TeamMember, Task, BudgetEntry, Finding, User, Person, ProjectAssignment
from datetime import datetime


# ---------- Authentication ----------

def create_user(username: str, password: str, security_question: str = None, security_answer: str = None) -> int:
    """Create a new user with a securely hashed password. Raises ValueError if username exists."""
    session = get_session()
    try:
        existing = session.query(User).filter_by(username=username).first()
        if existing:
            raise ValueError("Username already exists")

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        answer_hash = None
        if security_answer:
            answer_hash = bcrypt.hashpw(security_answer.lower().strip().encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        user = User(
            username=username,
            password_hash=password_hash,
            security_question=security_question,
            security_answer_hash=answer_hash
        )
        session.add(user)
        session.commit()
        return user.id
    finally:
        session.close()
    
def get_security_question(username: str) -> Optional[str]:
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user:
            return user.security_question
        return None
    finally:
        session.close()


def reset_password(username: str, security_answer: str, new_password: str) -> bool:
    """Reset password if the security answer matches. Returns True if successful."""
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user or not user.security_answer_hash:
            return False

        if not bcrypt.checkpw(security_answer.lower().strip().encode("utf-8"), user.security_answer_hash.encode("utf-8")):
            return False

        user.password_hash = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
        session.commit()
        return True
    finally:
        session.close()


def verify_user(username: str, password: str) -> Optional[int]:
    """Check username/password. Returns user_id if valid, None if invalid."""
    session = get_session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if not user:
            return None
        if bcrypt.checkpw(password.encode("utf-8"), user.password_hash.encode("utf-8")):
            return user.id
        return None
    finally:
        session.close()

# ---------- Global People ----------

def get_or_create_person(name: str, capacity_hrs_week: float = 40.0, skills: Optional[List[str]] = None) -> int:
    """Find an existing global person by name, or create them if they don't exist yet."""
    session = get_session()
    try:
        existing = session.query(Person).filter_by(name=name).first()
        if existing:
            return existing.id
        person = Person(name=name, capacity_hrs_week=capacity_hrs_week, skills=skills or [])
        session.add(person)
        session.commit()
        return person.id
    finally:
        session.close()


def assign_person_to_project(person_id: int, project_id: int, logged_hrs_week: float = 0.0) -> int:
    """Link a person to a project, or update their hours if already assigned."""
    session = get_session()
    try:
        existing = session.query(ProjectAssignment).filter_by(person_id=person_id, project_id=project_id).first()
        if existing:
            existing.logged_hrs_week = logged_hrs_week
            session.commit()
            return existing.id
        assignment = ProjectAssignment(person_id=person_id, project_id=project_id, logged_hrs_week=logged_hrs_week)
        session.add(assignment)
        session.commit()
        return assignment.id
    finally:
        session.close()


def get_person_total_logged_hours(person_id: int) -> float:
    """Sum a person's logged hours across ALL their active project assignments."""
    session = get_session()
    try:
        assignments = session.query(ProjectAssignment).filter_by(person_id=person_id).all()
        return sum(a.logged_hrs_week for a in assignments)
    finally:
        session.close()


def get_project_team_v2(project_id: int) -> List[Dict[str, Any]]:
    """Get a project's team using the new global-people system, with TRUE cross-project utilization."""
    session = get_session()
    try:
        assignments = session.query(ProjectAssignment).filter_by(project_id=project_id).all()
        result = []
        for a in assignments:
            person = session.query(Person).filter_by(id=a.person_id).first()
            if not person:
                continue
            total_logged = get_person_total_logged_hours(a.person_id)
            result.append({
                "person_id": person.id,
                "name": person.name,
                "capacity_hrs_week": person.capacity_hrs_week,
                "logged_hrs_week_this_project": a.logged_hrs_week,
                "logged_hrs_week_total": total_logged,
                "skills": person.skills or [],
            })
        return result
    finally:
        session.close()


def get_all_people() -> List[Dict[str, Any]]:
    """List every global person in the system, for selection when staffing a new project."""
    session = get_session()
    try:
        people = session.query(Person).all()
        result = []
        for p in people:
            total_logged = get_person_total_logged_hours(p.id)
            pct = (total_logged / p.capacity_hrs_week * 100) if p.capacity_hrs_week else 0
            result.append({
                "id": p.id,
                "name": p.name,
                "capacity_hrs_week": p.capacity_hrs_week,
                "total_logged_hrs_week": total_logged,
                "overall_utilization_pct": round(pct, 1),
                "skills": p.skills or [],
            })
        return result
    finally:
        session.close()
                    
# ---------- Projects ----------
def create_project(name: str, start_date: str = None, end_date: str = None) -> int:
    session = get_session()
    try:
        project = Project(name=name, start_date=start_date, end_date=end_date)
        session.add(project)
        session.commit()
        return project.id
    finally:
        session.close()

def create_project_with_description(name: str, description: str, start_date: str = None, end_date: str = None) -> int:
    """Create a project with a description field."""
    session = get_session()
    try:
        project = Project(name=name, description=description, start_date=start_date, end_date=end_date)
        session.add(project)
        session.commit()
        return project.id
    finally:
        session.close()


def get_project_description(project_id: int) -> Optional[str]:
    session = get_session()
    try:
        project = session.query(Project).filter_by(id=project_id).first()
        return project.description if project else None
    finally:
        session.close()


def copy_default_team_to_project(project_id: int, default_team: List[Dict[str, Any]]):
    """Seed a new project with a standard starting team roster."""
    for member in default_team:
        add_team_member(
            project_id=project_id,
            name=member["name"],
            capacity_hrs_week=member.get("capacity_hrs_week", 40),
            logged_hrs_week=member.get("logged_hrs_week", 0),
            skills=member.get("skills", [])
        )

def list_projects() -> List[Dict[str, Any]]:
    session = get_session()
    try:
        projects = session.query(Project).order_by(Project.created_at.desc()).all()
        return [
            {"id": p.id, "name": p.name, "created_at": p.created_at,
             "start_date": p.start_date, "end_date": p.end_date}
            for p in projects
        ]
    finally:
        session.close()


def get_project_dates(project_id: int) -> Optional[Dict[str, str]]:
    session = get_session()
    try:
        project = session.query(Project).filter_by(id=project_id).first()
        if not project:
            return None
        return {"start_date": project.start_date, "end_date": project.end_date}
    finally:
        session.close()

def update_project_dates(project_id: int, start_date: str, end_date: str):
    session = get_session()
    try:
        project = session.query(Project).filter_by(id=project_id).first()
        if project:
            project.start_date = start_date
            project.end_date = end_date
            session.commit()
    finally:
        session.close()

def delete_project(project_id: int):
    """Delete a project and all its related data (tasks, team, budget, findings) via cascade."""
    session = get_session()
    try:
        project = session.query(Project).filter_by(id=project_id).first()
        if project:
            session.delete(project)
            session.commit()
            return True
        return False
    finally:
        session.close()

def rename_project(project_id: int, new_name: str):
    session = get_session()
    try:
        project = session.query(Project).filter_by(id=project_id).first()
        if project:
            project.name = new_name
            session.commit()
    finally:
        session.close()
# ---------- Team Members ----------

def add_team_member(
    project_id: int,
    name: str,
    capacity_hrs_week: float,
    logged_hrs_week: float,
    skills: Optional[List[str]] = None,
) -> int:
    session = get_session()
    try:
        member = TeamMember(
            project_id=project_id,
            name=name,
            capacity_hrs_week=capacity_hrs_week,
            logged_hrs_week=logged_hrs_week,
            skills=skills or [],
        )
        session.add(member)
        session.commit()
        return member.id
    finally:
        session.close()

def get_last_data_change(project_id: int) -> Optional[datetime]:
    """Find the most recent updated_at timestamp across tasks, team members, and budget entries for a project."""
    session = get_session()
    try:
        timestamps = []

        latest_task = session.query(Task).filter_by(project_id=project_id).order_by(Task.updated_at.desc()).first()
        if latest_task and latest_task.updated_at:
            timestamps.append(latest_task.updated_at)

        latest_member = session.query(TeamMember).filter_by(project_id=project_id).order_by(TeamMember.updated_at.desc()).first()
        if latest_member and latest_member.updated_at:
            timestamps.append(latest_member.updated_at)

        latest_budget = session.query(BudgetEntry).filter_by(project_id=project_id).order_by(BudgetEntry.updated_at.desc()).first()
        if latest_budget and latest_budget.updated_at:
            timestamps.append(latest_budget.updated_at)

        return max(timestamps) if timestamps else None
    finally:
        session.close()

def get_team_members(project_id: int) -> List[Dict[str, Any]]:
    """Returns dicts with capacity_hrs_week/logged_hrs_week -- ready to pass into calculate_utilization()."""
    session = get_session()
    try:
        members = session.query(TeamMember).filter_by(project_id=project_id).all()
        return [
            {
                "name": m.name,
                "capacity_hrs_week": m.capacity_hrs_week,
                "logged_hrs_week": m.logged_hrs_week,
                "skills": m.skills or [],
            }
            for m in members
        ]
    finally:
        session.close()


# ---------- Tasks ----------

def add_task(
    project_id: int,
    task_key: str,
    title: str,
    progress_pct: float = 0.0,
    planned_end: Optional[str] = None,
    depends_on: Optional[List[str]] = None,
    assigned_to: Optional[str] = None,
    required_skill: Optional[str] = None,
) -> int:
    session = get_session()
    try:
        task = Task(
            project_id=project_id,
            task_key=task_key,
            title=title,
            progress_pct=progress_pct,
            planned_end=planned_end,
            depends_on=depends_on or [],
            assigned_to=assigned_to,
            required_skill=required_skill,
        )
        session.add(task)
        session.commit()
        return task.id
    finally:
        session.close()


def get_tasks(project_id: int) -> List[Dict[str, Any]]:
    session = get_session()
    try:
        tasks = session.query(Task).filter_by(project_id=project_id).all()
        return [
            {
                "id": t.task_key,
                "name": t.title,
                "progress_pct": t.progress_pct,
                "planned_end": t.planned_end,
                "depends_on": t.depends_on or [],
                "assigned_to": t.assigned_to,
                "required_skill": t.required_skill,
            }
            for t in tasks
        ]
    finally:
        session.close()

def save_generated_tasks(project_id: int, generated_tasks: list, default_deadline: str = None):
    count = 0
    for t in generated_tasks:
        add_task(
            project_id=project_id,
            task_key=t.get("id", f"T{count+1}"),
            title=t.get("name", "Untitled task"),
            progress_pct=0,
            planned_end=default_deadline,
            depends_on=[],
            assigned_to=t.get("assigned_to"),
            required_skill=t.get("required_skill"),
        )
        count += 1
    return count
# ---------- Budget ----------

def add_budget_entry(project_id: int, planned_spend: float, actual_spend: float, pct_time_elapsed: float) -> int:
    session = get_session()
    try:
        entry = BudgetEntry(
            project_id=project_id,
            planned_spend=planned_spend,
            actual_spend=actual_spend,
            pct_time_elapsed=pct_time_elapsed,
        )
        session.add(entry)
        session.commit()
        return entry.id
    finally:
        session.close()


def get_latest_budget_entry(project_id: int) -> Optional[Dict[str, Any]]:
    """Returns raw dollar figures -- ready to pass into check_budget_status()."""
    session = get_session()
    try:
        entry = (
            session.query(BudgetEntry)
            .filter_by(project_id=project_id)
            .order_by(BudgetEntry.recorded_at.desc())
            .first()
        )
        if not entry:
            return None
        return {
            "planned_spend": entry.planned_spend,
            "actual_spend": entry.actual_spend,
            "pct_time_elapsed": entry.pct_time_elapsed,
        }
    finally:
        session.close()

def get_or_create_project(name: str) -> int:
    session = get_session()
    try:
        existing = session.query(Project).filter_by(name=name).first()
        if existing:
            return existing.id
        project = Project(name=name)
        session.add(project)
        session.commit()
        return project.id
    finally:
        session.close()

def get_project_summary(project_id: int) -> Dict[str, Any]:
    """Quick counts and status for a project overview dashboard."""
    tasks = get_tasks(project_id)
    team = get_team_members(project_id)
    budget = get_latest_budget_entry(project_id)
    recent = get_recent_findings(project_id, limit=1)

    return {
        "task_count": len(tasks),
        "team_count": len(team),
        "has_budget": budget is not None,
        "last_analysis": recent[0]["created_at"] if recent else None,
    }


# ---------- Task Update/Delete ----------

def update_task(task_db_id: int, title: str, progress_pct: float, planned_end: str, depends_on: List[str], assigned_to: str):
    session = get_session()
    try:
        task = session.query(Task).filter_by(id=task_db_id).first()
        if task:
            task.title = title
            task.progress_pct = progress_pct
            task.planned_end = planned_end
            task.depends_on = depends_on
            task.assigned_to = assigned_to
            session.commit()
    finally:
        session.close()


def delete_task(task_db_id: int):
    session = get_session()
    try:
        task = session.query(Task).filter_by(id=task_db_id).first()
        if task:
            session.delete(task)
            session.commit()
    finally:
        session.close()


def get_tasks_with_db_id(project_id: int) -> List[Dict[str, Any]]:
    """Same as get_tasks but includes the internal database id, needed for edit/delete."""
    session = get_session()
    try:
        tasks = session.query(Task).filter_by(project_id=project_id).all()
        return [
            {
                "db_id": t.id,
                "id": t.task_key,
                "name": t.title,
                "progress_pct": t.progress_pct,
                "planned_end": t.planned_end,
                "depends_on": t.depends_on or [],
                "assigned_to": t.assigned_to,
            }
            for t in tasks
        ]
    finally:
        session.close()


# ---------- Team Member Update/Delete ----------

def update_team_member(member_db_id: int, name: str, capacity_hrs_week: float, logged_hrs_week: float, skills: List[str]):
    session = get_session()
    try:
        member = session.query(TeamMember).filter_by(id=member_db_id).first()
        if member:
            member.name = name
            member.capacity_hrs_week = capacity_hrs_week
            member.logged_hrs_week = logged_hrs_week
            member.skills = skills
            session.commit()
    finally:
        session.close()


def delete_team_member(member_db_id: int):
    session = get_session()
    try:
        member = session.query(TeamMember).filter_by(id=member_db_id).first()
        if member:
            session.delete(member)
            session.commit()
    finally:
        session.close()


def get_team_members_with_db_id(project_id: int) -> List[Dict[str, Any]]:
    """Same as get_team_members but includes the internal database id, needed for edit/delete."""
    session = get_session()
    try:
        members = session.query(TeamMember).filter_by(project_id=project_id).all()
        return [
            {
                "db_id": m.id,
                "name": m.name,
                "capacity_hrs_week": m.capacity_hrs_week,
                "logged_hrs_week": m.logged_hrs_week,
                "skills": m.skills or [],
            }
            for m in members
        ]
    finally:
        session.close()
# ---------- Findings ----------

def save_finding(project_id: int, agent_name: str, target: str, finding: str, details: Optional[Dict] = None) -> int:
    session = get_session()
    try:
        row = Finding(
            project_id=project_id,
            agent_name=agent_name,
            target=target,
            finding=finding,
            details=details or {},
        )
        session.add(row)
        session.commit()
        return row.id
    finally:
        session.close()


def get_recent_findings(project_id: int, limit: int = 20) -> List[Dict[str, Any]]:
    session = get_session()
    try:
        rows = (
            session.query(Finding)
            .filter_by(project_id=project_id)
            .order_by(Finding.created_at.desc())
            .limit(limit)
            .all()
        )
        return [
            {
                "agent_name": r.agent_name,
                "target": r.target,
                "finding": r.finding,
                "details": r.details or {},
                "created_at": r.created_at,
            }
            for r in rows
        ]
    finally:
        session.close()

def bulk_add_tasks(project_id: int, tasks: List[Dict[str, Any]]) -> int:
    """Add multiple tasks at once from a list of dicts (e.g. from JSON/CSV upload)."""
    count = 0
    for t in tasks:
        add_task(
            project_id=project_id,
            task_key=t.get("id") or t.get("task_key"),
            title=t.get("name") or t.get("title"),
            progress_pct=t.get("progress_pct", 0),
            planned_end=t.get("planned_end"),
            depends_on=t.get("depends_on", []),
            assigned_to=t.get("assigned_to"),
        )
        count += 1
    return count


def bulk_add_team_members(project_id: int, members: List[Dict[str, Any]]) -> int:
    """Add multiple team members at once from a list of dicts."""
    count = 0
    for m in members:
        add_team_member(
            project_id=project_id,
            name=m.get("name"),
            capacity_hrs_week=m.get("capacity_hrs_week", 40),
            logged_hrs_week=m.get("logged_hrs_week", 0),
            skills=m.get("skills", []),
        )
        count += 1
    return count