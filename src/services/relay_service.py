"""
Educational message relay service.
Routes student questions to assigned teachers, and teacher feedback/homework to students.
"""

from typing import Dict, Any, Optional
from src.core.models import Classroom, Participant
from src.core.security import contains_sensitive_data, sanitize_text


class RelayService:
    def __init__(self):
        pass

    def prepare_relay_payload(
        self,
        classroom: Classroom,
        sender: Participant,
        kind: str,
        message: str,
        has_photos: bool = False,
        has_voice: bool = False,
    ) -> Dict[str, Any]:
        """
        Validates sender role, determines recipient, sanitizes content,
        and constructs an educational relay packet.
        """
        # Determine valid routing
        if sender.role == "student":
            if kind not in ("question", "reschedule_request"):
                raise ValueError("Students may only submit questions or reschedule requests.")
            recipient_id = classroom.teacher_id
        elif sender.role == "teacher":
            if kind not in ("answer", "homework", "lesson_update", "reschedule_response"):
                raise ValueError("Teachers may only submit answers, homework, or lesson updates.")
            recipient_id = classroom.student_id
        else:
            raise ValueError(f"Unknown participant role: {sender.role}")

        # Sanitize message body to prevent credential/path leaks
        safe_message = sanitize_text(message)

        return {
            "classroom_id": classroom.id,
            "sender_id": sender.id,
            "recipient_id": recipient_id,
            "kind": kind,
            "message": safe_message,
            "has_photos": has_photos,
            "has_voice": has_voice,
            "was_sanitized": safe_message != message,
        }
