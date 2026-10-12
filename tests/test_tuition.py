import unittest
from pathlib import Path

from src.core.security import contains_sensitive_data, sanitize_text, has_command_injection
from src.core.language import detect_language, is_ambiguous_message
from src.core.models import LessonSlot
from src.services.roster_service import RosterService
from src.services.timetable_service import TimetableService, slots_overlap
from src.services.reschedule_service import RescheduleService
from src.services.relay_service import RelayService


class TestTuitionSecurity(unittest.TestCase):
    def test_detect_sensitive_tokens(self):
        text_with_key = "My token is sk-proj-1234567890abcdef1234"
        self.assertTrue(contains_sensitive_data(text_with_key))
        sanitized = sanitize_text(text_with_key)
        self.assertNotIn("sk-proj", sanitized)
        self.assertIn("[REDACTED_CREDENTIAL]", sanitized)

    def test_detect_internal_paths(self):
        text_with_path = "Log file stored at /Users/sample_user/.hermes/creds.json"
        self.assertTrue(contains_sensitive_data(text_with_path))
        sanitized = sanitize_text(text_with_path)
        self.assertNotIn("/Users/sample_user", sanitized)
        self.assertIn("[REDACTED_PATH]", sanitized)

    def test_command_injection(self):
        self.assertTrue(has_command_injection("/help"))
        self.assertTrue(has_command_injection("Check /status now"))
        self.assertFalse(has_command_injection("Hello teacher, how are you?"))


class TestTuitionLanguage(unittest.TestCase):
    def test_language_detection(self):
        self.assertEqual(detect_language("老师这道数学题怎么做？"), "zh")
        self.assertEqual(detect_language("Please can you help me with this question on next lesson?"), "en")
        self.assertEqual(detect_language("Cikgu boleh tolong semak soalan latihan ini esok?"), "ms")

    def test_ambiguous_short_messages(self):
        self.assertTrue(is_ambiguous_message("hi"))
        self.assertTrue(is_ambiguous_message("ok"))
        self.assertIsNone(detect_language("ok"))


class TestRosterAndEnrollment(unittest.TestCase):
    def setUp(self):
        self.roster = RosterService()

    def test_roster_loading(self):
        self.assertIn("teacher_kelvin", self.roster.participants)
        self.assertIn("student_alex", self.roster.participants)

    def test_participant_authentication(self):
        p1 = self.roster.find_participant_by_identifier("60120000001")
        self.assertIsNotNone(p1)
        self.assertEqual(p1.id, "teacher_kelvin")

        p2 = self.roster.find_participant_by_identifier("100000000000003")
        self.assertIsNotNone(p2)
        self.assertEqual(p2.id, "student_alex")


class TestTimetableAndReschedule(unittest.TestCase):
    def setUp(self):
        self.timetable_svc = TimetableService()
        self.reschedule_svc = RescheduleService()

    def test_monthly_slot_generation(self):
        # 2026 October: 1st is Thursday. Saturday is weekday=6.
        slots = self.timetable_svc.generate_monthly_slots(
            year=2026, month=10, weekday=6, start_time="10:00", duration_minutes=60
        )
        self.assertTrue(len(slots) >= 4)
        self.assertEqual(slots[0].start_time, "10:00")
        self.assertEqual(slots[0].end_time, "11:00")

    def test_slot_collision(self):
        s1 = LessonSlot(date="2026-10-10", start_time="10:00", end_time="11:00")
        s2 = LessonSlot(date="2026-10-10", start_time="10:30", end_time="11:30")
        s3 = LessonSlot(date="2026-10-10", start_time="11:00", end_time="12:00")

        self.assertTrue(slots_overlap(s1, s2))
        self.assertFalse(slots_overlap(s1, s3))

    def test_reschedule_flow(self):
        c_slot = LessonSlot(date="2026-10-15", start_time="15:00", end_time="16:00")
        prop = self.reschedule_svc.create_proposal(
            classroom_id="kelvin_alex_math",
            original_lesson_id="2026-10-L002",
            proposer_role="student",
            candidate_slots=[c_slot],
        )
        self.assertEqual(prop.status, "pending")
        accepted = self.reschedule_svc.accept_proposal(prop.proposal_id, 0)
        self.assertEqual(accepted.date, "2026-10-15")
        self.assertEqual(prop.status, "accepted")


class TestEducationalRelay(unittest.TestCase):
    def setUp(self):
        self.roster = RosterService()
        self.relay_svc = RelayService()
        self.classroom = self.roster.get_classroom("kelvin_alex_math")
        self.student = self.roster.participants["student_alex"]
        self.teacher = self.roster.participants["teacher_kelvin"]

    def test_student_question_relay(self):
        payload = self.relay_svc.prepare_relay_payload(
            classroom=self.classroom,
            sender=self.student,
            kind="question",
            message="Teacher, could you explain question 5 on the worksheet?",
            has_photos=True,
        )
        self.assertEqual(payload["recipient_id"], "teacher_kelvin")
        self.assertEqual(payload["kind"], "question")
        self.assertTrue(payload["has_photos"])


if __name__ == "__main__":
    unittest.main()
