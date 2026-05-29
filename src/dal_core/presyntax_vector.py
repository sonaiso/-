"""
PreSyntax Mufrad Vector (شعاع المفرد قبل التركيب)

Typed, non-semantic interface exported from MufradProof for operator consumption.

CRITICAL PRINCIPLE:
Operators do NOT work on raw tokens or strings.
Operators work ONLY on PreSyntaxMufradVector extracted from MufradProof.

This vector provides:
1. Stable type identification
2. Morphological feature summary
3. Surface effect observations
4. Case sign potentials (NOT case effects)
5. Rank and residuals
6. Composition readiness

It does NOT provide:
- meaning, semantic, madlul, murad
- haqiqa/majaz distinction
- syntax roles (faail, mafool, mubtada, khabar)
- case effects (marfoo_by, mansub_by, majroor_by)
- operator governance
"""

from dataclasses import dataclass
from typing import Optional

from dal_core.type_ids import NounTypeID, VerbTypeID, ParticleTypeID
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual
from dal_core.morph_features import (
    CandidateStatus,
    VerbFeatureProof,
    NounInflectionClass,
    ParticleOperatorPotential,
)
from dal_core.surface_effects import SurfaceEffect
from dal_core.case_signs import CaseSignPotential
from dal_core.composition_readiness import CompositionReadiness
from dal_core.mufrad_axes import BinaaJudgment, IshtiqaqJudgment


@dataclass(frozen=True)
class PreSyntaxMufradVector:
    """
    شعاع المفرد قبل التركيب

    Typed numerical interface for operator consumption.

    This is the ONLY interface that nahw operators may access.
    Operators cannot work on tokens, strings, or raw MufradProof.

    Mathematical foundation:
    ```
    O_j : PreSyntaxMufradVector^k → CandidateSet
    ```

    NOT:
    ```
    O_j : Token^k → CaseEffect
    ```

    This prevents hallucination by enforcing governed proof pipeline.
    """

    # Identity and position
    mufrad_id: str
    """Unique identifier for this mufrad proof"""

    raw_span: tuple[int, int]
    """Character span in source text (start, end)"""

    # Type identification (operational codes)
    type_value: str
    """Type string identifier (ISM, FIIL, HARF)"""

    type_id: NounTypeID | VerbTypeID | ParticleTypeID | None
    """Operational type ID for operator matching"""

    type_rank: LughaRank
    """Rank of type determination"""

    # Morphological status (candidates, not meanings)
    mabni_murab_status: CandidateStatus
    """Building/inflection status"""

    noun_inflection_class: Optional[NounInflectionClass]
    """Noun inflection class if ISM"""

    verb_features: Optional[VerbFeatureProof]
    """Verb features if FIIL"""

    particle_operator_potential: Optional[ParticleOperatorPotential]
    """Operator potential if HARF"""

    # Surface observations
    surface_effects: tuple[SurfaceEffect, ...]
    """Surface phonological/orthographic effects"""

    case_sign_potentials: tuple[CaseSignPotential, ...]
    """
    Case sign observations (ALLOWED).

    These are surface potentials, NOT case effects.
    Operators will use these to produce CaseEffectCandidates.
    """

    # Governance metadata
    morph_rank: LughaRank
    """Rank from morphological analysis"""

    final_rank: LughaRank
    """Weakest rank in proof chain"""

    residuals: tuple[Residual, ...]
    """Unresolved residuals from analysis"""

    trace_id: str
    """Trace identifier for witness chain"""

    # PR #159: Separate linguistic identity from trace provenance
    identity_ids: tuple[str, ...] = ()
    """
    Linguistic identity IDs (form, root, pattern, clitic).

    CRITICAL: identity_ids ≠ trace_ids
    - identity_ids: linguistic features preserved through transitions
    - trace_ids: provenance witness chain

    Constitutional law: Do NOT use trace_ids as substitute for identity.
    """

    carrier_ids: tuple[str, ...] = ()
    """
    Carrier IDs from Unicode/Atom layer.

    CRITICAL: carrier_ids ≠ text_fallback
    - carrier_ids: explicit Unicode/Atom provenance
    - text fallback: provisional when carrier_ids unavailable

    Constitutional law: Text fallback is residual, not full provenance.
    """

    competitors_count: int
    """Number of unresolved morphological competitors"""

    composition_readiness: CompositionReadiness
    """Explicit readiness level for composition"""

    # =========================================================================
    # Classified mufrad axes (PR-F)
    # =========================================================================
    # These two fields lift the PR-A axis judgments into the operator-facing
    # vector. They default to UNRESOLVED so existing constructors keep
    # working; pipelines that compute the judges should populate them.

    binaa_judgment: BinaaJudgment = BinaaJudgment.UNRESOLVED
    """Classified binaa/i'rab judgment lifted from the underlying
    MufradProof. ``UNRESOLVED`` acts as a 5th-gate blocker on operator
    consumption (see :meth:`allows_operator_consumption`)."""

    ishtiqaq_judgment: IshtiqaqJudgment = IshtiqaqJudgment.UNRESOLVED
    """Classified ishtiqaq/jamid judgment lifted from the underlying
    MufradProof. For nouns, ``UNRESOLVED`` is also a 5th-gate blocker."""

    def __post_init__(self):
        """Validate that this vector contains no forbidden fields"""
        # Check for forbidden field names in dataclass
        forbidden_fields = [
            'meaning', 'semantic', 'madlul', 'murad',
            'haqiqa', 'majaz', 'literal', 'metaphor',
            'case_effect', 'syntax_role',
            'faail', 'mafool', 'mubtada', 'khabar',
            'marfoo_by', 'mansub_by', 'majroor_by', 'majzum_by',
            'governed_by_operator', 'operator_id', 'relation_type',
        ]

        # Get all field names from dataclass
        field_names = {f.name for f in self.__dataclass_fields__.values()}

        # Check for violations
        violations = field_names.intersection(forbidden_fields)
        if violations:
            raise ValueError(
                f"PreSyntaxMufradVector contains forbidden fields: {violations}. "
                f"This vector must NOT contain semantic, syntax role, or case effect fields."
            )

    def allows_operator_consumption(self) -> bool:
        """
        Check if this vector is ready for operator consumption.

        This is a governed gate that enforces:
        1. Minimum composition readiness
        2. No blocking residuals
        3. Valid trace to raw input
        4. Unresolved competitors checked for certificate level
        5. Rank preserved from MufradProof

        Returns:
            bool: True only if ALL gate conditions pass
        """
        # Gate 1: Basic readiness check
        if not self.composition_readiness.allows_composition():
            return False

        # Gate 2: Block if blocking residuals present
        if self.has_blocking_residuals():
            return False

        # Gate 3: Require valid trace to raw input
        if not self.trace_id or self.trace_id == "":
            return False

        # Gate 4: For certificate-level composition, reject unresolved competitors
        if self.composition_readiness.allows_certificate():
            if self.competitors_count > 0:
                return False

        # Gate 5 (PR-F): block on unresolved mufrad axes.
        # An operator MUST NOT consume a vector whose binaa axis is
        # unresolved — the structural-frozen vs inflectable distinction
        # is a pre-syntactic input to every operator. For nouns we also
        # require the ishtiqaq axis to be resolved (mushtaq-vs-jamid),
        # since several operators (e.g. اسم فاعل governance) depend on
        # that classification. For verbs and particles the ishtiqaq axis
        # is NOT_APPLICABLE by design, and that is not a blocker.
        if self.binaa_judgment == BinaaJudgment.UNRESOLVED:
            return False
        is_noun = (self.type_value or "").upper() == "ISM" or (
            self.type_id is not None and self.type_id.name.startswith("ISM")
        )
        if is_noun and self.ishtiqaq_judgment == IshtiqaqJudgment.UNRESOLVED:
            return False

        # All gates passed
        return True

    def allows_certificate_composition(self) -> bool:
        """
        Check if this vector supports certificate-level composition.
        """
        return self.composition_readiness.allows_certificate()

    def has_blocking_residuals(self) -> bool:
        """Check if any blocker residuals present"""
        from dal_core.residuals import has_blocking_residuals as check_blocking
        return check_blocking(self.residuals)

    def get_type_signature(self) -> str:
        """
        Get type signature for operator matching.

        Returns string like "ISM_COMMON" or "FIIL_MADI" or "HARF_JARR"
        """
        if self.type_id is not None:
            return self.type_id.value
        return self.type_value

    def summary(self) -> str:
        """Human-readable summary"""
        type_sig = self.get_type_signature()
        readiness = self.composition_readiness.value
        competitors = f"{self.competitors_count} competitors" if self.competitors_count > 0 else "no competitors"
        residuals_count = len(self.residuals)

        return (
            f"PreSyntaxVector[{self.mufrad_id}]: "
            f"type={type_sig}, readiness={readiness}, "
            f"{competitors}, residuals={residuals_count}"
        )
