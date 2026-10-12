"""
Lesson rescheduling negotiation service.
Coordinates replacement time proposals, multi-slot options, and confirmations.
"""

from typing import Dict, Optional, List
from src.core.models import RescheduleProposal, LessonSlot


class RescheduleService:
    def __init__(self):
        # Maps proposal_id -> RescheduleProposal
        self.proposals: Dict[str, RescheduleProposal] = {}
        self.proposal_counter = 1

    def create_proposal(
        self,
        classroom_id: str,
        original_lesson_id: str,
        proposer_role: str,
        candidate_slots: List[LessonSlot],
    ) -> RescheduleProposal:
        """Creates a new structured rescheduling proposal."""
        prop_id = f"R{self.proposal_counter:03d}"
        self.proposal_counter += 1

        proposal = RescheduleProposal(
            proposal_id=prop_id,
            classroom_id=classroom_id,
            original_lesson_id=original_lesson_id,
            proposer_role=proposer_role,
            candidate_slots=candidate_slots,
            status="pending",
        )
        self.proposals[prop_id] = proposal
        return proposal

    def accept_proposal(self, proposal_id: str, selected_slot_index: int = 0) -> Optional[LessonSlot]:
        """Accepts a proposal and returns the selected lesson slot."""
        proposal = self.proposals.get(proposal_id)
        if not proposal or proposal.status != "pending":
            return None

        if 0 <= selected_slot_index < len(proposal.candidate_slots):
            chosen = proposal.candidate_slots[selected_slot_index]
            proposal.status = "accepted"
            return chosen

        return None

    def reject_proposal(self, proposal_id: str) -> bool:
        """Rejects a pending proposal."""
        proposal = self.proposals.get(proposal_id)
        if not proposal or proposal.status != "pending":
            return False

        proposal.status = "rejected"
        return True
