"""
U₃ Boundary and Attachment Carrier (حامل الحدود والاتصال)

Domain: U₃ = BoundaryAndAttachmentCarrier
Purpose: Identify word boundaries and attachment relationships WITHOUT functional role commitment
Transition: U₂s (Syllable) → U₃ (BoundaryAndAttachment) → U₄ (TrueSingularLafẓ)

Critical Laws (Axioms):
    - Axiom 3.1: لا لفظ حقيقي قبل فصل الحدود (No true lafẓ before boundary separation)
    - Axiom 3.2: الاتصال ≠ الدور الوظيفي (Attachment ≠ Functional role)
    - Axiom 3.3: الحدود تحفظ أثر المقطع (Boundaries preserve syllable trace)
    - Axiom 3.4: لا جذر في U₃ (No root in U₃)
    - Axiom 3.5: لا وزن في U₃ (No weight in U₃)
    - Axiom 3.6: لا معنى في U₃ (No meaning in U₃)
    - Axiom 3.7: لا حكم في U₃ (No hukm in U₃)

Type System:
    BoundaryUnit ≠ Root
    BoundaryUnit ≠ Weight
    BoundaryUnit ≠ FunctionalRole
    BoundaryUnit ≠ Meaning

Architecture:
    U₂s (SyllableLayerObject) → CPB₃ → U₃ (BoundaryLayerObject) → CPB₄ → TrueSingularLafẓ

Example Analysis:
    وَبِكِتَابِهِمْ → [وَ, بِـ, كِتَاب, ـهِمْ]
        وَ = standalone_proclitic (potential conjunction)
        بِـ = attached_proclitic (potential preposition)
        كِتَاب = core_candidate (potential lexical unit)
        ـهِمْ = attached_enclitic (potential pronoun)

    Note: U₃ identifies STRUCTURE, not MEANING or ROLE
    Role assignment happens at U₅ (FunctionalRoleCarrier)

PR: EXEC-LAYER-REFACTOR
Created: 2026-05-25
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, FrozenSet, Dict, Any, Tuple
from uuid import uuid4

from dal_core.residuals import Residual, ResidualType, make_blocker, make_warning
from dal_core.foundation import (
    Rank,
    RankVector,
    ProofObject,
    make_proof_object,
    ResidualSet,
    merge_residuals,
    has_blocking_residuals
)
from dal_core.u2s_syllable_carrier import (
    ArabicSyllable,
    SyllableLayerObject
)


# ============================================================================
# Type System - Boundary Unit Classification
# ============================================================================

class BoundaryUnitType(Enum):
    """
    Types of boundary units identified from syllable sequences.

    Classification is STRUCTURAL, not functional or semantic.
    """
    STANDALONE_CORE = "standalone_core"              # كَتَبَ (complete unit)
    STANDALONE_PROCLITIC = "standalone_proclitic"    # وَ (detached conjunction)
    ATTACHED_PROCLITIC = "attached_proclitic"        # بِـ (attached prefix)
    ATTACHED_ENCLITIC = "attached_enclitic"          # ـهُ, ـهُمْ (attached suffix)
    CORE_CANDIDATE = "core_candidate"                # كِتَاب (potential lexical core)
    ORTHOGRAPHIC_COMPOUND = "orthographic_compound"  # Multiple units written together
    UNRESOLVED = "unresolved"                        # Cannot determine boundary


class AttachmentType(Enum):
    """
    Attachment relationship between boundary units.

    This describes HOW units connect, not WHAT they are.
    """
    NO_ATTACHMENT = "no_attachment"              # Standalone word
    PROCLITIC_TO_HOST = "proclitic_to_host"      # Prefix → host (بِـكِتَاب)
    ENCLITIC_TO_HOST = "enclitic_to_host"        # Host → suffix (كِتَابُـهُ)
    BOTH_SIDES = "both_sides"                    # Prefix → host → suffix (بِـكِتَابِـهِ)
    ORTHOGRAPHIC_ONLY = "orthographic_only"      # Written together, no morphological attachment
    AMBIGUOUS = "ambiguous"                      # Unclear attachment


class BoundaryEvidence(Enum):
    """Evidence types for boundary detection."""
    SPACE_SEPARATOR = "space_separator"              # Whitespace boundary
    ORTHOGRAPHIC_PATTERN = "orthographic_pattern"    # Known prefix/suffix patterns
    SYLLABLE_PATTERN = "syllable_pattern"            # Syllabic structure hints
    LEXICON_MATCH = "lexicon_match"                  # Known closed-class items
    MORPHOLOGICAL_CLUE = "morphological_clue"        # Morphological structure hints
    STATISTICAL = "statistical"                      # Frequency-based inference
    AMBIGUOUS_EVIDENCE = "ambiguous_evidence"        # Conflicting evidence


# ============================================================================
# Failure Types
# ============================================================================

class BoundaryFailureType(Enum):
    """Failure types for boundary detection."""
    NO_SYLLABLES = "no_syllables"                    # Empty input
    SINGLE_SYLLABLE_AMBIGUOUS = "single_syllable_ambiguous"  # Cannot determine if standalone
    CONFLICTING_EVIDENCE = "conflicting_evidence"    # Multiple interpretations
    UNKNOWN_PATTERN = "unknown_pattern"              # Pattern not in registry
    ORPHAN_ATTACHMENT = "orphan_attachment"          # Attachment without host


# ============================================================================
# Core Structures
# ============================================================================

@dataclass(frozen=True)
class BoundaryUnit:
    """
    Single boundary unit identified from syllable sequence.

    A boundary unit represents a STRUCTURAL segment, not a linguistic entity.
    It does NOT carry:
        - Functional role (that's U₅)
        - Root/stem (that's U₈)
        - Weight/pattern (that's U₉)
        - Meaning (that's U₁₅)
    """
    uid: str
    surface: str                                     # Surface form (كِتَاب, وَ, ـهُ)
    unit_type: BoundaryUnitType                      # STRUCTURAL type
    attachment_type: AttachmentType                  # HOW it attaches
    evidence: FrozenSet[BoundaryEvidence]            # Why this boundary was detected
    syllable_indices: Tuple[int, ...]                # Which syllables from U₂s
    trace_2s: str                                    # Trace to U₂s layer
    residuals: FrozenSet[Residual]                   # Warnings/blockers
    rank: Rank                                       # Epistemic rank

    def __post_init__(self):
        """Validate boundary unit."""
        # No root field allowed
        if hasattr(self, 'root'):
            raise ValueError("BoundaryUnit MUST NOT contain 'root' field (Axiom 3.4)")

        # No weight field allowed
        if hasattr(self, 'weight'):
            raise ValueError("BoundaryUnit MUST NOT contain 'weight' field (Axiom 3.5)")

        # No meaning field allowed
        if hasattr(self, 'meaning'):
            raise ValueError("BoundaryUnit MUST NOT contain 'meaning' field (Axiom 3.6)")

        # No functional_role field allowed
        if hasattr(self, 'functional_role'):
            raise ValueError("BoundaryUnit MUST NOT contain 'functional_role' field (Axiom 3.2)")


@dataclass(frozen=True)
class BoundaryLayerObject:
    """
    U₃ layer object containing boundary analysis results.

    Represents the output of boundary detection from syllable layer.
    """
    uid: str
    units: Tuple[BoundaryUnit, ...]                  # Identified boundary units
    trace_2s: str                                    # Trace to syllable layer
    residuals: FrozenSet[Residual]                   # Accumulated residuals
    rank: Rank                                       # Overall rank
    proof: Optional[ProofObject] = None              # Proof of boundary detection


@dataclass(frozen=True)
class BoundaryResult:
    """Result of boundary detection operation."""
    success: bool
    layer_object: Optional[BoundaryLayerObject]
    failure_type: Optional[BoundaryFailureType]
    message: str
    residuals: FrozenSet[Residual]


# ============================================================================
# CPB₃ - Completeness Predicate and Proof Builder
# ============================================================================

@dataclass(frozen=True)
class CPB3:
    """
    CPB₃: Completeness Predicate and Proof Builder for Boundary layer.

    Guards:
        - Units identified
        - Syllable trace preserved
        - No forbidden fields (root, weight, meaning, functional_role)
        - Allowed next gate: U₄ TrueSingularLafẓ ONLY
    """

    @staticmethod
    def is_complete(layer_obj: BoundaryLayerObject) -> bool:
        """Check if boundary layer object is complete."""
        if not layer_obj.units:
            return False

        if not layer_obj.trace_2s:
            return False

        # Check no forbidden fields in units
        for unit in layer_obj.units:
            if hasattr(unit, 'root') or hasattr(unit, 'weight') or hasattr(unit, 'meaning'):
                return False

        return True

    @staticmethod
    def build_proof(layer_obj: BoundaryLayerObject) -> ProofObject:
        """Build proof object for boundary layer."""
        return make_proof_object(
            layer_name="U3_BOUNDARY_ATTACHMENT",
            is_complete=CPB3.is_complete(layer_obj),
            evidence_items=[
                f"units_count={len(layer_obj.units)}",
                f"trace_2s={layer_obj.trace_2s[:50]}...",
                f"rank={layer_obj.rank.value}",
            ],
            allowed_next_gates=frozenset({"true_singular_lafz_gate"}),
            forbidden_gates=frozenset({
                "functional_role_direct",  # Must go through U₄ first
                "root_certificate",
                "weight_certificate",
                "meaning_certificate",
                "hukm_certificate",
            }),
        )


# ============================================================================
# Boundary Detection Operations (Skeleton)
# ============================================================================

def boundary_3(syllable_layer: SyllableLayerObject) -> BoundaryResult:
    """
    Identify boundaries and attachment from syllable layer.

    Critical Examples:
        كَتَبَ → [كَتَبَ] (standalone_core)
        بِكِتَابٍ → [بِـ, كِتَاب] (attached_proclitic + core_candidate)
        وَبِكِتَابِهِمْ → [وَ, بِـ, كِتَاب, ـهِمْ] (multiple units)

    Args:
        syllable_layer: U₂s layer object with syllables

    Returns:
        BoundaryResult with identified units or failure

    Forbidden:
        - Direct jump to FunctionalRole (U₅)
        - Direct jump to Root (U₈)
        - Direct jump to Weight (U₉)
        - Direct jump to Meaning (U₁₅)
    """
    # SKELETON IMPLEMENTATION
    # TODO: Implement full boundary detection algorithm

    if not syllable_layer.syllables:
        return BoundaryResult(
            success=False,
            layer_object=None,
            failure_type=BoundaryFailureType.NO_SYLLABLES,
            message="No syllables in input",
            residuals=frozenset([make_blocker("no_syllables", "Cannot detect boundaries without syllables")])
        )

    # For now, create a simple boundary unit representing the entire syllable sequence
    # Real implementation would analyze patterns, lexicon, morphology

    surface = "".join(syll.surface for syll in syllable_layer.syllables)

    boundary_unit = BoundaryUnit(
        uid=str(uuid4()),
        surface=surface,
        unit_type=BoundaryUnitType.UNRESOLVED,  # Needs real detection
        attachment_type=AttachmentType.NO_ATTACHMENT,
        evidence=frozenset([BoundaryEvidence.SYLLABLE_PATTERN]),
        syllable_indices=tuple(range(len(syllable_layer.syllables))),
        trace_2s=syllable_layer.uid,
        residuals=frozenset([make_warning("skeleton_implementation", "U₃ boundary detection is skeleton only")]),
        rank=Rank.CANDIDATE
    )

    layer_obj = BoundaryLayerObject(
        uid=str(uuid4()),
        units=(boundary_unit,),
        trace_2s=syllable_layer.uid,
        residuals=frozenset([make_warning("skeleton_implementation", "U₃ is skeleton implementation")]),
        rank=Rank.CANDIDATE,
        proof=None
    )

    # Build proof
    proof = CPB3.build_proof(layer_obj)
    layer_obj = BoundaryLayerObject(
        uid=layer_obj.uid,
        units=layer_obj.units,
        trace_2s=layer_obj.trace_2s,
        residuals=layer_obj.residuals,
        rank=layer_obj.rank,
        proof=proof
    )

    return BoundaryResult(
        success=True,
        layer_object=layer_obj,
        failure_type=None,
        message="Boundary detection complete (skeleton)",
        residuals=layer_obj.residuals
    )


# ============================================================================
# Helper Functions
# ============================================================================

def make_boundary_unit(
    surface: str,
    unit_type: BoundaryUnitType,
    attachment_type: AttachmentType,
    evidence: FrozenSet[BoundaryEvidence],
    syllable_indices: Tuple[int, ...],
    trace_2s: str,
) -> BoundaryUnit:
    """Factory function for creating boundary units."""
    return BoundaryUnit(
        uid=str(uuid4()),
        surface=surface,
        unit_type=unit_type,
        attachment_type=attachment_type,
        evidence=evidence,
        syllable_indices=syllable_indices,
        trace_2s=trace_2s,
        residuals=frozenset(),
        rank=Rank.CANDIDATE
    )
