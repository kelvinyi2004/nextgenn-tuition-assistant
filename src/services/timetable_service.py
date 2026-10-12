"""
Timetable scheduling and collision detection service.
Calculates mutual availability without disclosing third-party identities.
"""

import datetime as dt
from typing import List, Dict, Tuple, Optional
from src.core.models import LessonSlot


def parse_time(t_str: str) -> dt.time:
    """Parses HH:MM into a datetime.time object."""
    parts = t_str.strip().split(":")
    return dt.time(int(parts[0]), int(parts[1]))


def slots_overlap(s1: LessonSlot, s2: LessonSlot) -> bool:
    """Checks if two slots on the same date overlap in time."""
    if s1.date != s2.date:
        return False

    t1_start = parse_time(s1.start_time)
    t1_end = parse_time(s1.end_time)
    t2_start = parse_time(s2.start_time)
    t2_end = parse_time(s2.end_time)

    # Overlap occurs if start of s1 < end of s2 and start of s2 < end of s1
    return max(t1_start, t2_start) < min(t1_end, t2_end)


class TimetableService:
    def __init__(self):
        # Maps classroom_id -> List[LessonSlot]
        self.confirmed_timetables: Dict[str, List[LessonSlot]] = {}

    def add_lessons(self, classroom_id: str, slots: List[LessonSlot]):
        self.confirmed_timetables.setdefault(classroom_id, []).extend(slots)

    def check_conflicts(
        self, candidate_slot: LessonSlot, existing_slots: List[LessonSlot]
    ) -> List[LessonSlot]:
        """Finds any existing slots that conflict with the candidate slot."""
        conflicts = []
        for slot in existing_slots:
            if slots_overlap(candidate_slot, slot):
                conflicts.append(slot)
        return conflicts

    def generate_monthly_slots(
        self, year: int, month: int, weekday: int, start_time: str, duration_minutes: int = 60
    ) -> List[LessonSlot]:
        """
        Generates recurring slots for a given month and weekday (1=Monday ... 7=Sunday).
        """
        slots = []
        # Find first day of the month
        cur = dt.date(year, month, 1)
        # Advance to target weekday (cur.isoweekday(): 1=Mon, 7=Sun)
        days_ahead = (weekday - cur.isoweekday()) % 7
        cur += dt.timedelta(days=days_ahead)

        start_t = parse_time(start_time)
        end_dt = dt.datetime.combine(cur, start_t) + dt.timedelta(minutes=duration_minutes)
        end_time_str = end_dt.strftime("%H:%M")

        lesson_idx = 1
        while cur.month == month:
            slots.append(
                LessonSlot(
                    date=cur.isoformat(),
                    start_time=start_time,
                    end_time=end_time_str,
                    duration_minutes=duration_minutes,
                    lesson_id=f"{year}-{month:02d}-L{lesson_idx:03d}",
                )
            )
            lesson_idx += 1
            cur += dt.timedelta(days=7)

        return slots
