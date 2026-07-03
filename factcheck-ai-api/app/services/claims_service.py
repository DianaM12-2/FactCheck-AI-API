from app.models.claim import PharmacyClaim, ClaimStatus
from typing import List, Optional


class ClaimsService:
    """In-memory claims store. Replace with DB layer for production."""

    def __init__(self):
        self._claims: dict[str, PharmacyClaim] = {}
        self._seed_data()

    def _seed_data(self):
        samples = [
            ("Maria Garcia",   "Lisinopril",   45.00),
            ("James Wilson",   "Metformin",    120.00),
            ("Sarah Johnson",  "Atorvastatin", 650.00),
        ]
        for name, med, amount in samples:
            claim = PharmacyClaim(patient_name=name, medication=med, amount=amount)
            claim.evaluate_risk(self.count_by_patient(name))
            self._claims[claim.claim_id] = claim

    def get_all(self) -> List[dict]:
        return [c.to_dict() for c in self._claims.values()]

    def get_by_id(self, claim_id: str) -> Optional[PharmacyClaim]:
        return self._claims.get(claim_id)

    def create(self, data: dict) -> PharmacyClaim:
        claim = PharmacyClaim(
            patient_name=data["patient_name"],
            medication=data["medication"],
            amount=float(data["amount"]),
        )
        existing = self.count_by_patient(claim.patient_name)
        claim.evaluate_risk(existing)
        self._claims[claim.claim_id] = claim
        return claim

    def delete(self, claim_id: str) -> bool:
        if claim_id in self._claims:
            del self._claims[claim_id]
            return True
        return False

    def get_flagged(self) -> List[dict]:
        return [c.to_dict() for c in self._claims.values() if c.flagged]

    def count_by_patient(self, name: str) -> int:
        return sum(1 for c in self._claims.values() if c.patient_name == name)

    def get_analytics(self) -> dict:
        all_claims = list(self._claims.values())
        amounts = [c.amount for c in all_claims]
        return {
            "total_claims":   len(all_claims),
            "total_amount":   round(sum(amounts), 2),
            "average_amount": round(sum(amounts) / len(amounts), 2) if amounts else 0,
            "flagged_count":  sum(1 for c in all_claims if c.flagged),
            "approved_count": sum(1 for c in all_claims if c.status == ClaimStatus.APPROVED),
            "pending_count":  sum(1 for c in all_claims if c.status == ClaimStatus.PENDING),
        }
