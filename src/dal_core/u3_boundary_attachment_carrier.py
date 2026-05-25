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
from dal_core.foundation import (
    PotentialPath,
    PotentialPathStatus,
    make_potential_path,
    certify_potential_path,
    block_potential_path,
    NeutralBoundaryPotential,
    make_neutral_boundary_potential,
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
            claim="U₃ boundary detection complete",
            scope="U3_BOUNDARY_ATTACHMENT",
            evidence=frozenset([
                f"units_count={len(layer_obj.units)}",
                f"trace_preserved={bool(layer_obj.trace_2s)}",
                f"rank={layer_obj.rank.value}",
            ]),
            counter_evidence=frozenset(),
            trace_graph={},
            competitors=frozenset(),
            residuals=layer_obj.residuals,
            rank_vector={},  # Empty for now - U₃ not in valid keys yet
            allowed_next_gates=frozenset({"true_singular_lafz_gate"}),
            forbidden_next_gates=frozenset({
                "functional_role_direct",  # Must go through U₄ first
                "root_certificate",
                "weight_certificate",
                "meaning_certificate",
                "hukm_certificate",
            }),
            limitations=frozenset(),
            metadata=None,
        )


# ============================================================================
# Boundary Detection Operations
# ============================================================================

def _detect_proclitic_at_start(surface: str) -> Optional[Tuple[str, str]]:
    """
    Detect proclitic at start of surface form.

    Returns:
        (proclitic, remainder) if found, None otherwise
    """
    # Try multi-character proclitics first
    for length in [2, 1]:
        prefix = surface[:length]
        if prefix in PROCLITICS:
            return (prefix, surface[length:])
    return None


def _detect_enclitic_at_end(surface: str) -> Optional[Tuple[str, str]]:
    """
    Detect enclitic at end of surface form.

    Returns:
        (core, enclitic) if found, None otherwise
    """
    # Try multi-character enclitics first (longest match)
    # Note: Arabic with diacritics can be 4+ chars (e.g., هِمْ = 4 chars)
    for length in [5, 4, 3, 2, 1]:
        if len(surface) > length:
            suffix = surface[-length:]
            # Check both with and without tatweel variants
            if suffix in ENCLITICS:
                return (surface[:-length], suffix)
    return None


def _detect_boundaries(surface: str, syllable_layer: SyllableLayerObject) -> List[BoundaryUnit]:
    """
    Detect boundary units from surface form.

    Strategy:
        1. Scan for proclitics from start (greedy left-to-right)
        2. Scan for enclitics from end (greedy right-to-left)
        3. Remaining middle part = core candidate

    Returns:
        List of boundary units
    """
    units = []
    remaining = surface
    current_syllable_idx = 0

    # Convert syllables to list for indexing
    syllables_list = list(syllable_layer.syllables) if hasattr(syllable_layer, 'syllables') else []
    all_indices = list(range(len(syllables_list)))

    # Get trace
    if hasattr(syllable_layer, 'uid'):
        trace_2s = syllable_layer.uid
    elif hasattr(syllable_layer, 'metadata'):
        trace_2s = str(syllable_layer.metadata) if syllable_layer.metadata else str(uuid4())
    else:
        trace_2s = str(uuid4())

    # Detect proclitics (from left)
    while remaining:
        proclitic_match = _detect_proclitic_at_start(remaining)
        if proclitic_match:
            proclitic, rest = proclitic_match
            proclitic_info = PROCLITICS[proclitic]

            # Determine unit type based on standalone/attached
            if proclitic_info[1] == "standalone":
                unit_type = BoundaryUnitType.STANDALONE_PROCLITIC
                attachment = AttachmentType.NO_ATTACHMENT
            else:
                unit_type = BoundaryUnitType.ATTACHED_PROCLITIC
                attachment = AttachmentType.PROCLITIC_TO_HOST

            # Calculate syllable indices for this proclitic
            proclitic_len = len(proclitic)
            unit_indices = []
            char_count = 0
            for idx in range(current_syllable_idx, len(syllables_list)):
                syll = syllables_list[idx]
                # Get syllable surface
                if hasattr(syll, 'surface'):
                    syll_surf = syll.surface
                elif hasattr(syll, 'get_phonetic_string'):
                    syll_surf = syll.get_phonetic_string()
                else:
                    onset_str = "".join(sorted(syll.onset)) if syll.onset else ""
                    nucleus_str = "".join(sorted(syll.nucleus)) if syll.nucleus else ""
                    coda_str = "".join(sorted(syll.coda)) if syll.coda else ""
                    syll_surf = f"{onset_str}{nucleus_str}{coda_str}"

                char_count += len(syll_surf)
                unit_indices.append(idx)
                if char_count >= proclitic_len:
                    current_syllable_idx = idx + 1
                    break

            units.append(make_boundary_unit(
                surface=proclitic,
                unit_type=unit_type,
                attachment_type=attachment,
                evidence=proclitic_info[2],
                syllable_indices=tuple(unit_indices),
                trace_2s=trace_2s,
            ))

            remaining = rest
        else:
            break

    # Detect enclitics (from right)
    enclitic_units = []
    while remaining:
        enclitic_match = _detect_enclitic_at_end(remaining)
        if enclitic_match:
            core_part, enclitic = enclitic_match

            if enclitic in ENCLITICS:
                enclitic_info = ENCLITICS[enclitic]

                # Enclitics attach to host
                unit_type = BoundaryUnitType.ATTACHED_ENCLITIC
                attachment = AttachmentType.ENCLITIC_TO_HOST

                # Calculate syllable indices (from end)
                enclitic_len = len(enclitic)
                unit_indices = []
                char_count = 0
                for idx in range(len(syllables_list) - 1, -1, -1):
                    syll = syllables_list[idx]
                    # Get syllable surface
                    if hasattr(syll, 'surface'):
                        syll_surf = syll.surface
                    elif hasattr(syll, 'get_phonetic_string'):
                        syll_surf = syll.get_phonetic_string()
                    else:
                        onset_str = "".join(sorted(syll.onset)) if syll.onset else ""
                        nucleus_str = "".join(sorted(syll.nucleus)) if syll.nucleus else ""
                        coda_str = "".join(sorted(syll.coda)) if syll.coda else ""
                        syll_surf = f"{onset_str}{nucleus_str}{coda_str}"

                    char_count += len(syll_surf)
                    unit_indices.insert(0, idx)
                    if char_count >= enclitic_len:
                        break

                enclitic_units.insert(0, make_boundary_unit(
                    surface=enclitic,
                    unit_type=unit_type,
                    attachment_type=attachment,
                    evidence=enclitic_info[1],
                    syllable_indices=tuple(unit_indices),
                    trace_2s=trace_2s,
                ))

                remaining = core_part
            else:
                break
        else:
            break

    # Remaining part is the core candidate
    if remaining:
        # Calculate syllable indices for core
        core_indices = []
        for idx in range(current_syllable_idx, len(syllables_list)):
            if idx not in [i for unit in (units + enclitic_units) for i in unit.syllable_indices]:
                core_indices.append(idx)

        if not core_indices:
            # Use all remaining syllables
            used_indices = set([i for unit in (units + enclitic_units) for i in unit.syllable_indices])
            core_indices = [i for i in all_indices if i not in used_indices]

        # Determine core type
        if not units and not enclitic_units:
            unit_type = BoundaryUnitType.STANDALONE_CORE
            attachment = AttachmentType.NO_ATTACHMENT
        else:
            unit_type = BoundaryUnitType.CORE_CANDIDATE
            if units and enclitic_units:
                attachment = AttachmentType.BOTH_SIDES
            elif units:
                attachment = AttachmentType.PROCLITIC_TO_HOST
            else:
                attachment = AttachmentType.ENCLITIC_TO_HOST

        units.append(make_boundary_unit(
            surface=remaining,
            unit_type=unit_type,
            attachment_type=attachment,
            evidence=frozenset([BoundaryEvidence.SYLLABLE_PATTERN]),
            syllable_indices=tuple(core_indices) if core_indices else tuple(all_indices),
            trace_2s=trace_2s,
        ))

    # Add enclitic units after core
    units.extend(enclitic_units)

    return units


def boundary_3(syllable_layer: SyllableLayerObject) -> BoundaryResult:
    """
    Identify boundaries and attachment from syllable layer.

    Critical Examples:
        كَتَبَ → [كَتَبَ] (standalone_core)
        بِكِتَابٍ → [بِـ, كِتَابٍ] (attached_proclitic + core_candidate)
        وَبِكِتَابِهِمْ → [وَ, بِـ, كِتَابِ, ـهِمْ] (multiple units)

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
    # Convert frozenset to tuple for iteration
    syllables_list = list(syllable_layer.syllables) if hasattr(syllable_layer, 'syllables') else []

    if not syllables_list:
        return BoundaryResult(
            success=False,
            layer_object=None,
            failure_type=BoundaryFailureType.NO_SYLLABLES,
            message="No syllables in input",
            residuals=frozenset([make_blocker("no_syllables", "Cannot detect boundaries without syllables")])
        )

    # Get surface form from syllables
    # Handle both old and new syllable structures
    surface_parts = []
    for syll in syllables_list:
        if hasattr(syll, 'surface'):
            # Old structure with surface attribute
            surface_parts.append(syll.surface)
        elif hasattr(syll, 'get_phonetic_string'):
            # New structure - use phonetic string
            surface_parts.append(syll.get_phonetic_string())
        else:
            # Fallback - reconstruct from onset/nucleus/coda
            onset_str = "".join(sorted(syll.onset)) if syll.onset else ""
            nucleus_str = "".join(sorted(syll.nucleus)) if syll.nucleus else ""
            coda_str = "".join(sorted(syll.coda)) if syll.coda else ""
            surface_parts.append(f"{onset_str}{nucleus_str}{coda_str}")

    surface = "".join(surface_parts)

    # Detect boundary units
    detected_units = _detect_boundaries(surface, syllable_layer)

    # Create potential path
    # Get trace - handle both old and new structures
    if hasattr(syllable_layer, 'uid'):
        trace_2s = syllable_layer.uid
    elif hasattr(syllable_layer, 'metadata'):
        trace_2s = str(syllable_layer.metadata) if syllable_layer.metadata else str(uuid4())
    else:
        trace_2s = str(uuid4())

    potential_path = PotentialBoundaryPath(
        uid=str(uuid4()),
        units=tuple(detected_units),
        evidence=frozenset([BoundaryEvidence.LEXICON_MATCH, BoundaryEvidence.SYLLABLE_PATTERN]),
        residuals=frozenset(),
        rank=Rank.HYPOTHESIS,
        trace_2s=trace_2s,
    )

    # Apply boundary gate
    gate_result = apply_boundary_gate([potential_path])

    # Check if path was certified
    if gate_result.certified_paths:
        # Use first certified path
        certified_path = gate_result.certified_paths[0]

        # Build layer object
        layer_obj = certified_path.to_layer_object()

        # Build proof
        proof = CPB3.build_proof(layer_obj)
        layer_obj = BoundaryLayerObject(
            uid=layer_obj.uid,
            units=layer_obj.units,
            trace_2s=layer_obj.trace_2s,
            residuals=layer_obj.residuals | gate_result.residuals,
            rank=Rank.STRONG_HYPOTHESIS,
            proof=proof
        )

        return BoundaryResult(
            success=True,
            layer_object=layer_obj,
            failure_type=None,
            message=f"Boundary detection complete: {len(layer_obj.units)} units identified",
            residuals=layer_obj.residuals
        )
    else:
        # Path was blocked
        if gate_result.blocked_paths:
            blocked_path = gate_result.blocked_paths[0]
            return BoundaryResult(
                success=False,
                layer_object=None,
                failure_type=BoundaryFailureType.ORPHAN_ATTACHMENT,
                message="Boundary detection failed gate constraints",
                residuals=blocked_path.residuals | gate_result.residuals
            )
        else:
            return BoundaryResult(
                success=False,
                layer_object=None,
                failure_type=BoundaryFailureType.UNKNOWN_PATTERN,
                message="No valid boundary analysis found",
                residuals=frozenset([make_warning("no_valid_path", "No boundary path passed gate")])
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
    residuals: FrozenSet[Residual] = frozenset(),
    rank: Rank = Rank.CANDIDATE,
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
        residuals=residuals,
        rank=rank
    )


# ============================================================================
# Closed-Class Lexicon (Minimal for Testing)
# ============================================================================

# Proclitics - elements that attach BEFORE the core
PROCLITICS = {
    # Conjunction/coordinating particles
    "وَ": ("conjunction", "standalone", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "فَ": ("conjunction", "standalone", frozenset([BoundaryEvidence.LEXICON_MATCH])),

    # Prepositions (require host)
    "بِ": ("preposition", "attached", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "بِـ": ("preposition", "attached", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "لِ": ("preposition", "attached", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "لِـ": ("preposition", "attached", frozenset([BoundaryEvidence.LEXICON_MATCH])),

    # Future/intention marker
    "سَ": ("future_particle", "attached", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "سَـ": ("future_particle", "attached", frozenset([BoundaryEvidence.LEXICON_MATCH])),

    # Note: كَ (comparison particle) NOT included to avoid false positive on verbs like كَتَبَ
    # It requires more sophisticated context detection
}

# Enclitics - elements that attach AFTER the core
ENCLITICS = {
    # Attached pronouns - singular (with and without tatweel)
    "ـهُ": ("pronoun_3ms", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "هُ": ("pronoun_3ms", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "ـهَا": ("pronoun_3fs", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "هَا": ("pronoun_3fs", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "ـكَ": ("pronoun_2ms", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "كَ": ("pronoun_2ms", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "ـكِ": ("pronoun_2fs", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "كِ": ("pronoun_2fs", frozenset([BoundaryEvidence.LEXICON_MATCH])),

    # Attached pronouns - plural (with and without tatweel)
    "ـهُمْ": ("pronoun_3mp", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "هُمْ": ("pronoun_3mp", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "ـهِمْ": ("pronoun_3mp_genitive", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "هِمْ": ("pronoun_3mp_genitive", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "ـنَا": ("pronoun_1p", frozenset([BoundaryEvidence.LEXICON_MATCH])),
    "نَا": ("pronoun_1p", frozenset([BoundaryEvidence.LEXICON_MATCH])),
}


# ============================================================================
# PotentialBoundaryPath - Competing Boundary Analysis
# ============================================================================

@dataclass(frozen=True)
class PotentialBoundaryPath:
    """
    Represents a potential boundary analysis path.

    For a syllable sequence like بِكِتَابٍ, competing paths might be:
        Path1: [بِـ, كِتَابٍ] - proclitic + core
        Path2: [بِكِتَابٍ] - single lexicalized unit (if in lexicon)

    Each path awaits evidence and gate evaluation to become certificate.
    """
    uid: str
    units: Tuple[BoundaryUnit, ...]                  # Proposed boundary units
    evidence: FrozenSet[BoundaryEvidence]            # Evidence for this analysis
    residuals: FrozenSet[Residual]                   # Residuals for this path
    rank: Rank                                       # Current epistemic rank
    trace_2s: str                                    # Trace to syllable layer

    def to_layer_object(self, proof: Optional[ProofObject] = None) -> BoundaryLayerObject:
        """Convert path to BoundaryLayerObject."""
        return BoundaryLayerObject(
            uid=str(uuid4()),
            units=self.units,
            trace_2s=self.trace_2s,
            residuals=self.residuals,
            rank=self.rank,
            proof=proof
        )


# ============================================================================
# BoundaryGate - Constraint-Based Filter
# ============================================================================

@dataclass(frozen=True)
class BoundaryGateResult:
    """Result of applying boundary gate to potential paths."""
    certified_paths: Tuple[PotentialBoundaryPath, ...]   # Paths that passed gate
    blocked_paths: Tuple[PotentialBoundaryPath, ...]     # Paths blocked by gate
    residuals: FrozenSet[Residual]                       # Gate-level residuals


def apply_boundary_gate(paths: List[PotentialBoundaryPath]) -> BoundaryGateResult:
    """
    Apply boundary gate constraints to filter valid boundary analyses.

    Hard Constraints (infinite cost - blocks path):
        1. Orphan enclitic (enclitic without host)
        2. Empty core (no lexical core identified)
        3. Invalid unit sequence

    Soft Constraints (penalty - reduces rank):
        1. Unusual proclitic combination
        2. Ambiguous boundary
        3. Missing lexicon evidence

    Args:
        paths: List of potential boundary paths

    Returns:
        BoundaryGateResult with certified and blocked paths
    """
    certified = []
    blocked = []
    gate_residuals = set()

    for path in paths:
        path_blockers = []

        # Hard constraint 1: Check for orphan enclitic
        has_core = any(
            u.unit_type in (BoundaryUnitType.CORE_CANDIDATE,
                           BoundaryUnitType.STANDALONE_CORE)
            for u in path.units
        )
        has_enclitic = any(
            u.unit_type == BoundaryUnitType.ATTACHED_ENCLITIC
            for u in path.units
        )

        if has_enclitic and not has_core:
            path_blockers.append(make_blocker(
                "orphan_enclitic",
                "Enclitic found without host core"
            ))

        # Hard constraint 2: Check for empty analysis
        if not path.units:
            path_blockers.append(make_blocker(
                "empty_analysis",
                "No boundary units identified"
            ))

        # If any blockers, mark path as blocked
        if path_blockers:
            blocked_path = PotentialBoundaryPath(
                uid=path.uid,
                units=path.units,
                evidence=path.evidence,
                residuals=path.residuals | frozenset(path_blockers),
                rank=Rank.BLOCKED,
                trace_2s=path.trace_2s
            )
            blocked.append(blocked_path)
        else:
            # Path passes hard constraints
            certified.append(path)

    return BoundaryGateResult(
        certified_paths=tuple(certified),
        blocked_paths=tuple(blocked),
        residuals=frozenset(gate_residuals)
    )
