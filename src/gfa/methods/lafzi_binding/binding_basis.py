"""
BindingBasis - أساس الربط بين الدال والمدلول

Critical Law:
    الأساس ليس وضعاً كاملاً
    Basis is NOT full Wadh.

BindingBasis represents the evidence or hint that supports the binding
between Dāl and Madlūl-lafẓī, but does NOT constitute full Wadh (convention).

BindingBasis Types:
    PRIOR_INFORMATION: Binding supported by prior information
    USAGE_HINT: Binding supported by usage evidence
    LEXICAL_HINT: Binding supported by lexical evidence
    CONVENTIONAL_HINT: Binding supported by conventional evidence
    UNKNOWN_BASIS: Binding basis unknown → becomes residual

Critical Laws:
    1. BindingBasis is NOT Wadh (full convention)
    2. BindingBasis is evidence for possible binding
    3. UNKNOWN_BASIS becomes residual, not exception
    4. BindingBasis does NOT create meaning
    5. BindingBasis does NOT issue HUKM
    6. BindingBasis does NOT raise PredicateRank

IMPORTANT CLARIFICATIONS:

1. BindingBasis values are HINTS, not GATES:
   - CONVENTIONAL_HINT ≠ Wadh implementation
   - USAGE_HINT ≠ UsageGate implementation
   - LEXICAL_HINT ≠ Lexical certification
   - PRIOR_INFORMATION permits binding, does NOT certify Dalālah

2. Hints vs Gates:
   - Hint: Evidence suggesting possible binding
   - Gate: Validation enforcing requirements
   - BindingBasis provides hints only
   - Gates live in DalMadlulBindingGate

3. No semantic authority:
   - BindingBasis does NOT establish Wadh
   - BindingBasis does NOT certify meaning
   - BindingBasis does NOT prove signification
   - BindingBasis only supports binding candidacy

4. Future work:
   - Wadh implementation → PR-L5
   - UsageGate → PR-L5
   - Full Dalālah → PR-L6
   - Haqiqah/Majaz → PR-L7
"""

from __future__ import annotations
from enum import Enum, auto


class BindingBasis(Enum):
    """
    Evidence basis for Dāl/Madlūl binding.

    This is NOT full Wadh (convention).
    This is evidence that supports possible binding.

    Types:
        PRIOR_INFORMATION: Supported by PriorInformation
        USAGE_HINT: Supported by usage evidence
        LEXICAL_HINT: Supported by lexical evidence
        CONVENTIONAL_HINT: Supported by conventional evidence
        UNKNOWN_BASIS: Basis unknown (becomes residual)
    """

    PRIOR_INFORMATION = auto()
    USAGE_HINT = auto()
    LEXICAL_HINT = auto()
    CONVENTIONAL_HINT = auto()
    UNKNOWN_BASIS = auto()

    @property
    def is_known(self) -> bool:
        """Check if basis is known (not UNKNOWN_BASIS)."""
        return self != BindingBasis.UNKNOWN_BASIS

    @property
    def is_unknown(self) -> bool:
        """Check if basis is unknown."""
        return self == BindingBasis.UNKNOWN_BASIS

    @property
    def requires_residual(self) -> bool:
        """Check if this basis requires creating a residual."""
        return self == BindingBasis.UNKNOWN_BASIS

    def __str__(self) -> str:
        return self.name
