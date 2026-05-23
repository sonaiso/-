"""
DalCandidate - الدال المرشح

PR-L3: Pure Dāl Geometry Contract

Core dataclass representing a fully-licensed linguistic signifier candidate.

Critical Law:
    الدال المرخّص له هندسة كاملة قبل السؤال عن معناه
    A licensed signifier has complete geometry before asking about meaning.

DalCandidate Properties (13 Mandatory Fields):
    1. phonic_carriers: Sound/grapheme carriers from C1
    2. haraka_operations: Haraka transformations from C2a
    3. syllable_licenses: CV/CVC/CVV patterns
    4. word_boundaries: Word boundary detection
    5. clitics: Clitic separation
    6. formula_candidates: Pattern candidates
    7. path_type: Morphological path
    8. pattern_status: Pattern recognition status
    9. terminal_state: I'rab/Bina status
    10. syntactic_readiness: Ready for syntax
    11. sentence_shape: Sentence type
    12. role_projection_candidates: Syntactic role candidates
    13. trace_id, residuals, rank: Governance

What DalCandidate Does:
    - Provides complete linguistic signifier geometry
    - Preserves full pipeline trace (C1→C2a→C2b)
    - Enforces architectural boundaries
    - Serves as hardened input to PR-L4 binding

What DalCandidate Does NOT Contain (7 Forbidden Fields):
    - NO meaning
    - NO dalalah
    - NO wadh
    - NO hukm
    - NO mutabaqah
    - NO tadammun
    - NO iltizam
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple, Optional, FrozenSet, Literal
from .dal_type import DalType
from .dal_structures import (
    PhonicCarrier,
    HarakaOperation,
    SyllableLicense,
    WordBoundaryInfo,
    CliticAnalysis,
    FormulaCandidate,
    PathType,
    PatternStatus,
    TerminalState,
    SyntacticReadiness,
    SentenceShape,
    RoleProjection,
)


@dataclass(frozen=True)
class DalCandidate:
    """
    Pure Dāl Geometry - الدال المرخّص الكامل

    A fully-licensed linguistic signifier with complete geometric structure.

    This is the output of C1→C2a→C2b pipeline, representing a signifier
    that has been validated through all phonological and morphological
    gates before entering semantic binding.

    PR-L3 Contract: 13 Mandatory Fields
    ====================================
    """

    # === 1. Phonic Carriers (C1) ===
    phonic_carriers: Tuple[PhonicCarrier, ...]
    """الحوامل الصوتية - Sound/grapheme carriers from C1 encoding"""

    # === 2. Haraka Operations (C2a) ===
    haraka_operations: Tuple[HarakaOperation, ...]
    """عمليات الحركة - Haraka transformations from C2a gates"""

    # === 3. Syllable Licenses (C2a) ===
    syllable_licenses: Tuple[SyllableLicense, ...]
    """تراخيص المقاطع - CV/CVC/CVV patterns licensed"""

    # === 4. Word Boundaries (C2b) ===
    word_boundaries: WordBoundaryInfo
    """حدود الكلمة - Word boundary detection"""

    # === 5. Clitic Analysis (C2b) ===
    clitics: CliticAnalysis
    """تحليل اللواصق - Clitic separation"""

    # === 6. Formula Candidates (C2b) ===
    formula_candidates: Tuple[FormulaCandidate, ...]
    """مرشحات الصيغة - Pattern candidates (فَعَل, فاعِل...)"""

    # === 7. Path Type (C2b) ===
    path_type: PathType
    """نوع المسار - Morphological path (jamid/mushtaqq/verb...)"""

    # === 8. Pattern Status (C2b) ===
    pattern_status: PatternStatus
    """حالة الوزن - Pattern recognition status"""

    # === 9. Terminal State (C2b) ===
    terminal_state: TerminalState
    """الحالة النهائية - I'rab/Bina status"""

    # === 10. Syntactic Readiness (C2b) ===
    syntactic_readiness: SyntacticReadiness
    """الجاهزية النحوية - Ready for syntactic structures"""

    # === 11. Sentence Shape (C2b) ===
    sentence_shape: Optional[SentenceShape]
    """شكل الجملة - Sentence type (None for word-level)"""

    # === 12. Role Projection (C2b) ===
    role_projection_candidates: Tuple[RoleProjection, ...]
    """مرشحات الدور - Syntactic role candidates"""

    # === 13. Governance ===
    trace_id: str
    """معرّف التتبع - Unique trace identifier"""

    residuals: FrozenSet[str]
    """البقايا - Residuals from all stages"""

    source_layer: Literal["PURE_DAL"] = "PURE_DAL"
    """طبقة المصدر - Must be PURE_DAL"""

    # Legacy fields (backward compatibility)
    signifier_form: str = ""
    dal_type: Optional[DalType] = None

    def __post_init__(self):
        """
        Validate DalCandidate construction.

        PR-L3 Contract Enforcement:
        1. All 13 mandatory fields must be valid
        2. All 7 forbidden fields must be absent
        3. Trace must exist
        4. At least one phonic carrier
        """
        # Hard gates
        if self.source_layer != "PURE_DAL":
            raise ValueError(f"source_layer must be PURE_DAL, got {self.source_layer}")

        if not self.trace_id:
            raise ValueError("trace_id is required")

        if len(self.phonic_carriers) == 0:
            raise ValueError("At least one phonic carrier required")

        # Validate no forbidden fields exist
        forbidden = {
            'meaning', 'dalalah', 'wadh', 'hukm',
            'mutabaqah', 'tadammun', 'iltizam'
        }
        annotations = set(self.__annotations__.keys())
        violations = forbidden & annotations
        if violations:
            raise ValueError(
                f"Forbidden semantic fields detected: {violations}. "
                "DalCandidate must not contain meaning/dalalah/wadh/hukm."
            )

    # ========================================================================
    # Properties
    # ========================================================================

    @property
    def is_known_type(self) -> bool:
        """Check if path type is known (not UNKNOWN)."""
        return self.path_type.is_known if self.path_type else False

    @property
    def has_residuals(self) -> bool:
        """Check if candidate has residuals."""
        return len(self.residuals) > 0

    @property
    def is_valid(self) -> bool:
        """
        Check if candidate is valid for binding.

        Valid PR-L3 candidate means:
        - All 13 mandatory fields present
        - Path type is known
        - Pattern status is known or candidate
        - Syntactic readiness is not blocked
        - No blocking residuals
        """
        return (
            bool(self.trace_id)
            and self.path_type.is_known
            and self.pattern_status != PatternStatus.UNKNOWN
            and self.syntactic_readiness != SyntacticReadiness.BLOCKED
            and len(self.phonic_carriers) > 0
        )

    @property
    def is_complete(self) -> bool:
        """
        Check if DalCandidate represents a complete structure.

        Complete means all pipeline stages succeeded:
        - Phonic carriers present
        - Syllables licensed
        - Boundaries detected
        - Pattern recognized (at least candidate)
        """
        return (
            len(self.phonic_carriers) > 0
            and len(self.syllable_licenses) > 0
            and self.word_boundaries.confidence > 0.5
            and self.pattern_status != PatternStatus.UNKNOWN
        )

    @property
    def surface_form_reconstructed(self) -> str:
        """
        Reconstruct surface form from phonic carriers.

        This is the actual signifier form derived from the geometry.
        """
        if self.signifier_form:  # Use legacy if available
            return self.signifier_form
        return ''.join(c.form for c in self.phonic_carriers)

    # ========================================================================
    # Methods
    # ========================================================================

    def get_stem(self) -> str:
        """Get the stem after clitic removal."""
        return self.clitics.stem

    def get_formula_confidence(self) -> float:
        """Get maximum confidence among formula candidates."""
        if not self.formula_candidates:
            return 0.0
        return max(f.confidence for f in self.formula_candidates)

    def get_role_confidence(self, role_type: 'RoleType') -> float:
        """Get confidence for a specific syntactic role."""
        matches = [r for r in self.role_projection_candidates if r.role_type == role_type]
        if not matches:
            return 0.0
        return max(r.confidence for r in matches)

    def __str__(self) -> str:
        status = "VALID" if self.is_valid else "INVALID"
        residual_count = len(self.residuals)
        form = self.surface_form_reconstructed[:20]
        return (
            f"DalCandidate[{status}]: {self.path_type.name} "
            f"(id={self.trace_id}, form='{form}', "
            f"pattern={self.pattern_status.name}, residuals={residual_count})"
        )

    def __repr__(self) -> str:
        return (
            f"DalCandidate(trace_id='{self.trace_id}', "
            f"path_type={self.path_type.name}, "
            f"pattern_status={self.pattern_status.name}, "
            f"carriers={len(self.phonic_carriers)}, "
            f"residuals={len(self.residuals)})"
        )


@dataclass(frozen=True)
class DalResult:
    """
    Result of DalGate processing.

    Either:
        - success=True, candidate=DalCandidate, failure=None
        - success=False, candidate=None, failure=DalFailure
    """

    success: bool
    candidate: Optional[DalCandidate] = None
    failure: Optional[DalFailure] = None

    def __post_init__(self):
        """Validate result state."""
        if self.success and self.candidate is None:
            raise ValueError("Success result must have candidate")
        if not self.success and self.failure is None:
            raise ValueError("Failure result must have failure")
        if self.success and self.failure is not None:
            raise ValueError("Success result cannot have failure")
        if not self.success and self.candidate is not None:
            raise ValueError("Failure result cannot have candidate")

    @property
    def is_success(self) -> bool:
        """Check if result is success."""
        return self.success

    @property
    def is_failure(self) -> bool:
        """Check if result is failure."""
        return not self.success

    def __str__(self) -> str:
        if self.success:
            return f"DalResult[SUCCESS]: {self.candidate}"
        else:
            return f"DalResult[FAILURE]: {self.failure}"

    def __repr__(self) -> str:
        return f"DalResult(success={self.success})"


# Forward reference for type checking
class DalFailure:
    """Forward declaration for DalFailure (defined in dal_gate.py)."""
    pass
