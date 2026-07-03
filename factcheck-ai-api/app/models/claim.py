from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import uuid


class ClaimStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    FLAGGED = "flagged"


@dataclass
class PharmacyClaim:
    """
    Represents a pharmacy claim.
    Demonstrates Python OOP with dataclasses, enums, and type hints.
    """
    patient_name: str
    medication: str
    amount: float
    claim_id: str = field(default_factory=lambda: f"RX-{str(uuid.uuid4())[:8].upper()}")
    status: ClaimStatus = ClaimStatus.PENDING
    flagged: bool = False
    flag_reason: Optional[str] = None
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def evaluate_risk(self, existing_count: int = 0) -> None:
        """Evaluate claim for fraud risk."""
        if self.amount > 500:
            self.flagged = True
            self.flag_reason = f"High-value claim: ${self.amount:.2f} exceeds $500 threshold"
            self.status = ClaimStatus.FLAGGED
        if existing_count >= 3:
            self.flagged = True
            self.flag_reason = f"Duplicate risk: patient has {existing_count} existing claims"
            self.status = ClaimStatus.FLAGGED

    def approve(self) -> None:
        self.status = ClaimStatus.APPROVED

    def reject(self) -> None:
        self.status = ClaimStatus.REJECTED

    def to_dict(self) -> dict:
        return {
            "claim_id":   self.claim_id,
            "patient":    self.patient_name,
            "medication": self.medication,
            "amount":     self.amount,
            "status":     self.status.value,
            "flagged":    self.flagged,
            "flag_reason":self.flag_reason,
            "created_at": self.created_at,
        }
