"""
Roster and enrollment service.
Authenticates phone numbers/LIDs against authorized classroom pairs.
"""

import json
from pathlib import Path
from typing import Dict, Optional, List

from src.config import ROSTER_FILE
from src.core.models import Participant, Classroom


class RosterService:
    def __init__(self, roster_path: Optional[Path] = None):
        self.roster_path = Path(roster_path or ROSTER_FILE)
        self.participants: Dict[str, Participant] = {}
        self.classrooms: Dict[str, Classroom] = {}
        self.load_roster()

    def load_roster(self):
        """Loads and parses the roster JSON file."""
        if not self.roster_path.exists():
            raise FileNotFoundError(f"Roster file not found: {self.roster_path}")

        with open(self.roster_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.participants = {}
        for pid, p in data.get("participants", {}).items():
            self.participants[pid] = Participant(
                id=pid,
                name=p["name"],
                role=p["role"],
                phone=str(p["phone"]).lstrip("+"),
                lid=str(p.get("lid")) if p.get("lid") else None,
            )

        self.classrooms = {}
        for cid, c in data.get("classrooms", {}).items():
            self.classrooms[cid] = Classroom(
                id=cid,
                title=c.get("title", cid),
                teacher_id=c["teacher"],
                student_id=c["student"],
                monthly_lessons=c.get("monthly_lessons", 4),
                duration_minutes=c.get("duration_minutes", 60),
                schedule_description=c.get("schedule", ""),
            )

    def find_participant_by_identifier(self, identifier: str) -> Optional[Participant]:
        """Finds a participant matching a cleaned phone number or LID."""
        clean = str(identifier).split("@")[0].split(":")[0].lstrip("+").strip()
        for p in self.participants.values():
            if p.phone == clean or (p.lid and p.lid == clean):
                return p
        return None

    def get_classroom(self, classroom_id: str) -> Optional[Classroom]:
        return self.classrooms.get(classroom_id)

    def get_classrooms_for_participant(self, participant_id: str) -> List[Classroom]:
        """Finds all classrooms where the participant is enrolled."""
        matched = []
        for c in self.classrooms.values():
            if c.teacher_id == participant_id or c.student_id == participant_id:
                matched.append(c)
        return matched
