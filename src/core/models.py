"""
Data models for Classroom, Participant, LessonSlot, and RescheduleProposal.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Participant:
    id: str
    name: str
    role: str  # "teacher" or "student"
    phone: str
    lid: Optional[str] = None
    preferred_language: Optional[str] = None


@dataclass
class Classroom:
    id: str
    title: str
    teacher_id: str
    student_id: str
    monthly_lessons: int = 4
    duration_minutes: int = 60
    schedule_description: str = ""


@dataclass
class LessonSlot:
    date: str  # YYYY-MM-DD
    start_time: str  # HH:MM
    end_time: str  # HH:MM
    duration_minutes: int = 60
    status: str = "scheduled"  # scheduled, completed, rescheduled, cancelled
    lesson_id: Optional[str] = None


@dataclass
class RescheduleProposal:
    proposal_id: str
    classroom_id: str
    original_lesson_id: str
    proposer_role: str
    candidate_slots: List[LessonSlot] = field(default_factory=list)
    status: str = "pending"  # pending, accepted, rejected, expired
