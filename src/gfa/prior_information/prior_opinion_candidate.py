"""
Prior Opinion Candidate - مرشح الرأي السابق

Opinion that must be excluded from evidence chain.

Critical Laws:
1. Prior opinion cannot serve as evidence
2. Opinion must be filtered before rational operations
3. Contamination risk must be tracked
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Tuple
from uuid import uuid4


class OpinionType(Enum):
    """
    Type of prior opinion.

    IMPRESSION: Unverified impression (انطباع)
    BIAS: Systematic bias (تحيز)
    PREFERENCE: Personal preference (تفضيل)
    UNVERIFIED_INTERPRETATION: Interpretation without evidence (تفسير غير موثق)
    PRIOR_JUDGMENT: Judgment without supporting evidence (حكم سابق بلا دليل)
    HABIT: Habitual assumption (عادة)
    TASTE: Aesthetic preference (ذوق)
    """

    IMPRESSION = auto()              # انطباع
    BIAS = auto()                    # تحيز
    PREFERENCE = auto()              # تفضيل
    UNVERIFIED_INTERPRETATION = auto()  # تفسير غير موثق
    PRIOR_JUDGMENT = auto()          # حكم سابق بلا دليل
    HABIT = auto()                   # عادة
    TASTE = auto()                   # ذوق


@dataclass(frozen=True)
class PriorOpinionCandidate:
    """
    مرشح الرأي السابق - Prior Opinion Candidate

    Opinion that must be excluded from rational operations.

    Critical Properties:
    - content: Opinion content
    - opinion_type: Type of opinion
    - source: Where this opinion originated
    - contamination_risk: Risk if allowed into evidence chain
    - allowed_as_evidence: Always False (constitutional)

    Critical Laws:
    - Cannot serve as evidence
    - Cannot enter as prior information
    - Must be filtered before operations
    - Creates residual when detected
    """

    content: str
    opinion_type: OpinionType
    source: Optional[str] = None
    contamination_risk: float = 1.0  # High by default
    allowed_as_evidence: bool = False  # Always False
    trace_id: str = field(default_factory=lambda: uuid4().hex)

    def __post_init__(self):
        """Ensure allowed_as_evidence is always False."""
        if self.allowed_as_evidence:
            object.__setattr__(self, "allowed_as_evidence", False)

    def why_excluded(self) -> str:
        """Explain why this opinion is excluded."""
        reasons = {
            OpinionType.IMPRESSION: "انطباع غير موثق - Unverified impression",
            OpinionType.BIAS: "تحيز - Systematic bias",
            OpinionType.PREFERENCE: "تفضيل شخصي - Personal preference",
            OpinionType.UNVERIFIED_INTERPRETATION: "تفسير بلا دليل - Interpretation without evidence",
            OpinionType.PRIOR_JUDGMENT: "حكم سابق بلا دليل - Prior judgment without evidence",
            OpinionType.HABIT: "عادة - Habitual assumption",
            OpinionType.TASTE: "ذوق - Aesthetic preference",
        }
        return f"{reasons.get(self.opinion_type, 'Unknown opinion type')}: {self.content[:50]}"

    def get_contamination_residual(self) -> str:
        """Get residual for contamination risk."""
        return f"R-PRIOR-OPINION-CONTAMINATION:{self.opinion_type.name}:{self.contamination_risk:.2f}"

    def __str__(self) -> str:
        return f"PriorOpinion({self.opinion_type.name}: {self.content[:30]}...)"
