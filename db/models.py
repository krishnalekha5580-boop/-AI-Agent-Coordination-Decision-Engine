"""
db/models.py

SQLAlchemy models for the AI Agent Project Management & Decision Engine.

Field names are matched exactly to what tools/risk_tools.py, resource_tools.py,
budget_tools.py, and allocation_tools.py expect as raw input -- percentages
like utilization and budget status are computed BY THE TOOLS, not stored
pre-computed, so the tools' logic stays the single source of truth.
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, ForeignKey, DateTime, JSON
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    team_members = relationship("TeamMember", back_populates="project", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
    budget_entries = relationship("BudgetEntry", back_populates="project", cascade="all, delete-orphan")
    findings = relationship("Finding", back_populates="project", cascade="all, delete-orphan")


class TeamMember(Base):
    """Matches tools/resource_tools.py: calculate_utilization(logged_hrs, capacity_hrs)."""
    __tablename__ = "team_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    name = Column(String, nullable=False)
    capacity_hrs_week = Column(Float, nullable=False, default=40.0)
    logged_hrs_week = Column(Float, nullable=False, default=0.0)
    skills = Column(JSON, default=list)  # used by allocation_tools.recommend_assignee

    project = relationship("Project", back_populates="team_members")


class Task(Base):
    """Matches tools/risk_tools.py: check_dependency_status, assess_progress_risk."""
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    task_key = Column(String, nullable=False)     # e.g. "T1" (was "id" in JSON)
    title = Column(String, nullable=False)          # was "name" in JSON
    progress_pct = Column(Float, nullable=False, default=0.0)
    planned_end = Column(String, nullable=True)     # kept as "YYYY-MM-DD" string, matches calculate_days_remaining
    depends_on = Column(JSON, default=list)         # e.g. ["T1"]
    assigned_to = Column(String, nullable=True)

    project = relationship("Project", back_populates="tasks")


class BudgetEntry(Base):
    """Matches tools/budget_tools.py: check_budget_status(planned_spend, actual_spend, pct_time_elapsed)."""
    __tablename__ = "budget_entries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    planned_spend = Column(Float, nullable=False)
    actual_spend = Column(Float, nullable=False)
    pct_time_elapsed = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="budget_entries")


class Finding(Base):
    __tablename__ = "findings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    agent_name = Column(String, nullable=False)
    target = Column(String, nullable=False)
    finding = Column(String, nullable=False)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    project = relationship("Project", back_populates="findings")