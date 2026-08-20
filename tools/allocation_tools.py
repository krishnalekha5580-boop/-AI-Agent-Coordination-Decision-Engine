"""
allocation_tools.py

Utilities for recommending team member assignments based on
skill fit and current capacity/utilization.
"""

import logging
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

logger = logging.getLogger(__name__)

FULL_CAPACITY_THRESHOLD = 100  # utilization_pct at/above this = overloaded


@dataclass
class Candidate:
    """Represents a person eligible for task assignment."""
    name: str
    utilization_pct: float
    skills: List[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Candidate":
        try:
            return cls(
                name=data["name"],
                utilization_pct=data["utilization_pct"],
                skills=data.get("skills", []),
            )
        except KeyError as exc:
            raise ValueError(f"Candidate missing required field: {exc}") from exc


@dataclass
class AssignmentRecommendation:
    """Structured result of an assignment recommendation."""
    name: Optional[str]
    utilization_pct: Optional[float]
    skill_match: bool
    overloaded: bool
    message: str
    error: Optional[str] = None

    def __str__(self) -> str:
        return self.message


def recommend_assignee(
    candidates: List[Dict[str, Any]],
    required_skill: Optional[str] = None,
) -> AssignmentRecommendation:
    """
    Recommend the best-fit candidate for a task based on skill match
    and current utilization (lower utilization = more available).

    Args:
        candidates: List of dicts, each with 'name', 'utilization_pct',
            and optionally 'skills' (list of str).
        required_skill: Optional skill the assignee must have. If no
            candidate matches, falls back to the full candidate pool.

    Returns:
        AssignmentRecommendation with the chosen candidate, whether the
        skill matched, whether they're overloaded (>= 100% utilization),
        and a human-readable message. On invalid input, `error` is set
        and other fields are None/defaults.

    Example:
        >>> candidates = [
        ...     {"name": "Riya", "utilization_pct": 115, "skills": ["backend"]},
        ...     {"name": "Arjun", "utilization_pct": 75, "skills": ["frontend"]},
        ... ]
        >>> result = recommend_assignee(candidates, required_skill="backend")
        >>> result.overloaded
        True
    """
    if not candidates:
        logger.warning("recommend_assignee called with empty candidate list")
        return AssignmentRecommendation(
            name=None, utilization_pct=None, skill_match=False,
            overloaded=False, message="No candidates provided",
            error="empty_candidate_list",
        )

    try:
        parsed = [Candidate.from_dict(c) for c in candidates]
    except ValueError as exc:
        logger.error("Invalid candidate data: %s", exc)
        return AssignmentRecommendation(
            name=None, utilization_pct=None, skill_match=False,
            overloaded=False, message=str(exc), error="invalid_candidate_data",
        )

    skill_match = False
    pool = parsed

    if required_skill:
        skilled = [
            c for c in parsed
            if required_skill.lower() in (s.lower() for s in c.skills)
        ]
        if skilled:
            pool = skilled
            skill_match = True
        else:
            logger.info("No candidate found with skill '%s'; using full pool", required_skill)

    best = min(pool, key=lambda c: c.utilization_pct)
    overloaded = best.utilization_pct >= FULL_CAPACITY_THRESHOLD
    best_dict = next((c for c in candidates if c.get("name") == best.name), {})
    on_project = best_dict.get("on_project", True)

    if required_skill:
        skill_note = "with matching skill" if skill_match else "no exact skill match found, showing most available overall"
    else:
        skill_note = "no specific skill required"

    message = f"Recommend {best.name} (currently {best.utilization_pct}% utilized, {skill_note})"
    if not on_project:
        message += " — not currently on this project; would need to be added."
    if overloaded:
        message += " — WARNING: at or over full capacity; no one in the pool has spare bandwidth."
        logger.warning("Best available candidate %s is overloaded at %s%%", best.name, best.utilization_pct)

    return AssignmentRecommendation(
        name=best.name,
        utilization_pct=best.utilization_pct,
        skill_match=skill_match,
        overloaded=overloaded,
        message=message,
    )