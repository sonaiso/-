"""
U₄ True Singular Lafẓ Carrier (حامل اللفظ المفرد الحقيقي)

Domain: U₄ = TrueSingularLafẓCarrier
Purpose: Distinguish true singular lafẓ from orthographic compounds WITHOUT functional role
Transition: U₃ (BoundaryAndAttachment) → U₄ (TrueSingularLafẓ) → U₅ (FunctionalRole)

Critical Laws (Axioms):
    - Axiom 4.1: لفظ مفرد حقيقي ≠ تركيب كتابي (True lafẓ ≠ orthographic compound)
    - Axiom 4.2: اللفظ الحقيقي بعد فصل الحدود (True lafẓ after boundary separation)
    - Axiom 4.3: اللفظ ≠ الدور الوظيفي (Lafẓ ≠ functional role)
    - Axiom 4.4: لا جذر في U₄ (No root in U₄)
    - Axiom 4.5: لا وزن في U₄ (No weight in U₄)
    - Axiom 4.6: لا معنى في U₄ (No meaning in U₄)

Type System:
    TrueLafẓ ≠ Root
    TrueLafẓ ≠ Weight
    TrueLafẓ ≠ FunctionalRole
    TrueLafẓ ≠ Meaning
    TrueLafẓ ≠ Hukm

Architecture:
    U₃ (BoundaryLayerObject) → CPB₄ → U₄ (TrueLafẓLayerObject) → CPB₅ → FunctionalRole

Example Analysis:
    From U₃ boundary units [وَ, بِـ, كِتَاب, ـهِمْ]:
        - وَ → TRUE_LAFZ (standalone conjunction)
        - بِـكِتَابِـهِمْ → ORTHOGRAPHIC_COMPOUND (written together, but 3 units)

    Decision: Are they true singular lafẓ or composite?
        وَ = true_singular (standalone)
        بِـ = true_singular (can standalone as question marker)
        كِتَاب = true_singular (lexical core)
        ـهِمْ = NOT_STANDALONE (requires host)
        بِكِتَاب = COMPOSITE (preposition + noun)
        كِتَابِهِمْ = COMPOSITE (noun + pronoun)
        بِكِتَابِهِمْ = COMPOSITE (all three)

PR: EXEC-LAYER-REFACTOR
Created: 2026-05-25
"""

from dataclasses import dataclass
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
from dal_core.u3_boundary_attachment_carrier import (
    BoundaryUnit,
    BoundaryLayerObject
)


# ============================================================================
# Type System - Lafẓ Classification
# ============================================================================

class TrueLafzUnitType(Enum):
    """
    Classification of boundary units into lafẓ eligibility types.

    This is STRUCTURAL classification, not semantic or functional.
    U₄ determines eligibility to be a true singular lafẓ, NOT the meaning/role/root.
    """
    TRUE_SINGULAR_CORE_CANDIDATE = "true_singular_core_candidate"  # كِتَابٌ (eligible as true lafẓ)
    BOUND_PROCLITIC = "bound_proclitic"                            # وَ, فَ, بِـ, لِـ, سَـ
    ATTACHED_ENCLITIC = "attached_enclitic"                        # Generic enclitic
    ATTACHED_PRONOUN_CANDIDATE = "attached_pronoun_candidate"      # ـهُ, ـهَا, ـهِمْ
    ORTHOGRAPHIC_COMPOSITE = "orthographic_composite"              # Multiple units written together
    BLOCKED = "blocked"                                            # Cannot be determined


# ============================================================================
# Failure Types
# ============================================================================

class LafzFailureType(Enum):
    """Failure types for lafẓ determination."""
    NO_BOUNDARY_UNITS = "no_boundary_units"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    ORPHAN_ATTACHMENT = "orphan_attachment"


# ============================================================================
# Surface Potential Profile Structures (U₄-B)
# ============================================================================

@dataclass(frozen=True)
class TerminalProfile:
    """
    Terminal surface profile - NOT iʿrāb, NOT case marking.

    U₄ responsibility: describe terminal surface patterns
    U₅+ responsibility: assign grammatical case/mood

    Constitutional Law:
        Surface existence → boolean
        Surface interpretation → hint (possible/unlikely/unresolved)

    FORBIDDEN FIELDS:
        - case_marking (that's U₇+)
        - i3rab_status (that's U₇+)
        - mood_marking (that's U₇+)
    """
    ending_surface: str                    # النهاية كما هي
    terminal_diacritic: Optional[str]      # الحركة الأخيرة
    has_tanwin_surface: bool               # سطح التنوين موجود
    has_sukun_surface: bool                # سكون موجود
    has_taa_marbutah_surface: bool         # تاء مربوطة موجودة
    has_long_vowel_terminal_surface: bool  # حرف مد نهائي
    mabni_surface_hint: str                # "possible" | "unlikely" | "unresolved"
    murab_surface_hint: str                # "possible" | "unlikely" | "unresolved"
    residuals: Tuple[str, ...]

    def __post_init__(self):
        """Validate no forbidden fields."""
        if hasattr(self, 'case_marking'):
            raise ValueError("TerminalProfile MUST NOT contain 'case_marking' field")
        if hasattr(self, 'i3rab_status'):
            raise ValueError("TerminalProfile MUST NOT contain 'i3rab_status' field")
        if hasattr(self, 'mood_marking'):
            raise ValueError("TerminalProfile MUST NOT contain 'mood_marking' field")


@dataclass(frozen=True)
class DefinitenessSurfacePotential:
    """
    Definiteness surface patterns - NOT resolved reference.

    U₄ responsibility: identify الـ, tanwīn, pronoun surfaces
    U₅+ responsibility: resolve reference (muḥaddad vs nākira)

    FORBIDDEN FIELDS:
        - resolved_reference (that's U₅+)
        - is_definite (boolean certificate - use hint instead)
        - referent (that's U₁₅)
    """
    has_al_surface: bool                   # الـ موجود في السطح
    has_tanwin_surface: bool               # تنوين موجود في السطح
    has_attached_pronoun_surface: bool     # ضمير متصل موجود
    definite_surface_hint: str             # "possible" | "unlikely" | "unresolved"
    indefinite_surface_hint: str           # "possible" | "unlikely" | "unresolved"
    reference_surface_hint: str            # "possible" | "unlikely" | "unresolved"
    residuals: Tuple[str, ...]

    def __post_init__(self):
        """Validate no forbidden fields."""
        if hasattr(self, 'resolved_reference'):
            raise ValueError("DefinitenessSurfacePotential MUST NOT contain 'resolved_reference' field")
        if hasattr(self, 'is_definite'):
            raise ValueError("DefinitenessSurfacePotential MUST NOT contain 'is_definite' field")
        if hasattr(self, 'referent'):
            raise ValueError("DefinitenessSurfacePotential MUST NOT contain 'referent' field")


@dataclass(frozen=True)
class QuantitySurfacePotential:
    """
    Quantity surface patterns - NOT counted reality.

    U₄ responsibility: identify dual/plural surface markers
    U₅+ responsibility: determine actual quantity

    FORBIDDEN FIELDS:
        - quantity (certified singular/dual/plural)
        - counted_entities (that's U₁₅)
    """
    dual_surface_hint: str                 # "possible" | "unlikely" | "unresolved"
    plural_surface_hint: str               # "possible" | "unlikely" | "unresolved"
    singular_surface_hint: str             # "possible" | "unlikely" | "unresolved"
    number_word_surface_hint: str          # هل يبدو كرقم لفظي؟
    counted_object_surface_hint: str       # هل يبدو كمعدود؟
    residuals: Tuple[str, ...]

    def __post_init__(self):
        """Validate no forbidden fields."""
        if hasattr(self, 'quantity'):
            raise ValueError("QuantitySurfacePotential MUST NOT contain 'quantity' field")
        if hasattr(self, 'counted_entities'):
            raise ValueError("QuantitySurfacePotential MUST NOT contain 'counted_entities' field")


@dataclass(frozen=True)
class VerbSurfacePotential:
    """
    Verb surface patterns - NOT tense certificate.

    U₄ responsibility: identify verb-like surface patterns
    U₅+ responsibility: determine tense/aspect/mood

    FORBIDDEN FIELDS:
        - tense (that's U₅+)
        - voice (that's U₅+)
        - valency (that's U₅+)
        - aspect (that's U₅+)
        - mood (that's U₅+)
    """
    verb_surface_hint: str                 # "possible" | "unlikely" | "unresolved"
    past_surface_hint: str                 # "possible" | "unlikely" | "unresolved"
    present_surface_hint: str              # "possible" | "unlikely" | "unresolved"
    imperative_surface_hint: str           # "possible" | "unlikely" | "unresolved"
    has_present_prefix_surface: bool       # يـ، تـ، أـ، نـ موجود
    has_verbal_suffix_surface: bool        # ـتَ، ـتُمْ، ـنَ موجود
    residuals: Tuple[str, ...]

    def __post_init__(self):
        """Validate no forbidden fields."""
        if hasattr(self, 'tense'):
            raise ValueError("VerbSurfacePotential MUST NOT contain 'tense' field")
        if hasattr(self, 'voice'):
            raise ValueError("VerbSurfacePotential MUST NOT contain 'voice' field")
        if hasattr(self, 'valency'):
            raise ValueError("VerbSurfacePotential MUST NOT contain 'valency' field")
        if hasattr(self, 'aspect'):
            raise ValueError("VerbSurfacePotential MUST NOT contain 'aspect' field")
        if hasattr(self, 'mood'):
            raise ValueError("VerbSurfacePotential MUST NOT contain 'mood' field")


@dataclass(frozen=True)
class DownstreamPathHints:
    """
    Hints for downstream layers - NOT commitments.

    These are possibilities, not certainties.
    U₄ opens paths, U₅+ walk them.

    FORBIDDEN FIELDS:
        - pattern_family_hints (too close to U₉)
        - root_hints (U₈ territory)
        - weight_hints (U₉ territory)
    """
    may_open_functional_role_path: bool
    may_open_closed_class_path: bool
    may_open_verb_candidate_path: bool
    may_open_noun_candidate_path: bool
    may_open_reference_path: bool
    may_open_quantity_path: bool
    blocked_paths: Tuple[str, ...]         # مسارات محظورة

    def __post_init__(self):
        """Validate no forbidden fields."""
        if hasattr(self, 'pattern_family_hints'):
            raise ValueError("DownstreamPathHints MUST NOT contain 'pattern_family_hints' field")
        if hasattr(self, 'root_hints'):
            raise ValueError("DownstreamPathHints MUST NOT contain 'root_hints' field")
        if hasattr(self, 'weight_hints'):
            raise ValueError("DownstreamPathHints MUST NOT contain 'weight_hints' field")


# ============================================================================
# Core Structures
# ============================================================================

@dataclass(frozen=True)
class TrueLafzUnit:
    """
    U₄ classification of a boundary unit's lafẓ eligibility.

    This represents STRUCTURAL analysis: can this unit be a true singular lafẓ?
    NOT what the unit means, its role, root, or weight.

    U₄-B Extension: Surface potential profiles for TRUE_SINGULAR_CORE_CANDIDATE units.
    These profiles are HINTS/POTENTIALS only, never certificates.

    Forbidden fields:
        - root (that's U₈)
        - weight (that's U₉)
        - functional_role (that's U₅)
        - meaning (that's U₁₅)
        - hukm (that's U₇+)
        - iʿrab (that's U₇+)
    """
    uid: str
    surface: str                                     # Orthographic surface from U₃
    unit_type: TrueLafzUnitType                      # Classification type
    source_boundary_unit_id: str                     # Trace to U₃ boundary unit
    trace_3: Tuple[str, ...]                         # Ordered trace to U₃
    evidence: Tuple[str, ...]                        # Why this classification
    residuals: FrozenSet[Residual]
    rank: Rank

    # U₄-B: Surface potential profiles (optional, only for TRUE_SINGULAR_CORE_CANDIDATE)
    terminal_profile: Optional[TerminalProfile] = None
    definiteness_surface_potential: Optional[DefinitenessSurfacePotential] = None
    quantity_surface_potential: Optional[QuantitySurfacePotential] = None
    verb_surface_potential: Optional[VerbSurfacePotential] = None
    downstream_path_hints: Optional[DownstreamPathHints] = None

    def __post_init__(self):
        """Validate true lafẓ unit."""
        # No root field allowed
        if hasattr(self, 'root'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'root' field (Axiom 4.4)")

        # No weight field allowed
        if hasattr(self, 'weight'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'weight' field (Axiom 4.5)")

        # No meaning field allowed
        if hasattr(self, 'meaning'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'meaning' field (Axiom 4.6)")

        # No functional_role field allowed
        if hasattr(self, 'functional_role'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'functional_role' field (Axiom 4.3)")

        # No hukm field allowed
        if hasattr(self, 'hukm'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'hukm' field")

        # No iʿrab field allowed
        if hasattr(self, 'iʿrab') or hasattr(self, 'i3rab'):
            raise ValueError("TrueLafzUnit MUST NOT contain 'iʿrab' field")


@dataclass(frozen=True)
class TrueLafzLayerObject:
    """
    U₄ layer object containing true lafẓ eligibility analysis.

    Represents classification of boundary units into lafẓ eligibility categories.
    """
    uid: str
    units: Tuple[TrueLafzUnit, ...]                  # Classified units
    source_boundary_layer_id: str                    # Trace to U₃ layer
    trace_3: Tuple[str, ...]                         # Ordered trace to U₃
    residuals: FrozenSet[Residual]
    rank: Rank
    proof: Optional[ProofObject] = None


@dataclass(frozen=True)
class TrueLafzResult:
    """Result of true lafẓ determination."""
    success: bool
    layer_object: Optional[TrueLafzLayerObject]
    failure_type: Optional[LafzFailureType]
    message: str
    residuals: FrozenSet[Residual]


# ============================================================================
# CPB₄ - Completeness Predicate and Proof Builder
# ============================================================================

@dataclass(frozen=True)
class CPB4:
    """
    CPB₄: Completeness Predicate and Proof Builder for TrueSingularLafẓ layer.

    Guards:
        - Candidates identified
        - Boundary trace preserved
        - No forbidden fields (root, weight, meaning, functional_role)
        - Allowed next gate: U₅ FunctionalRole ONLY
    """

    @staticmethod
    def is_complete(layer_obj: TrueLafzLayerObject) -> bool:
        """Check if true lafẓ layer object is complete."""
        if not layer_obj.units:
            return False

        if not layer_obj.source_boundary_layer_id:
            return False

        # Check no forbidden fields
        for unit in layer_obj.units:
            if (hasattr(unit, 'root') or hasattr(unit, 'weight') or
                hasattr(unit, 'meaning') or hasattr(unit, 'functional_role') or
                hasattr(unit, 'hukm') or hasattr(unit, 'iʿrab')):
                return False

        return True

    @staticmethod
    def build_proof(layer_obj: TrueLafzLayerObject) -> ProofObject:
        """Build proof object for true lafẓ layer."""
        return make_proof_object(
            claim="U₄ true singular lafẓ eligibility determination complete",
            scope="U4_TRUE_SINGULAR_LAFZ",
            evidence=frozenset([
                f"units_count={len(layer_obj.units)}",
                f"trace_preserved={bool(layer_obj.source_boundary_layer_id)}",
                f"rank={layer_obj.rank.value}",
            ]),
            counter_evidence=frozenset(),
            trace_graph={},
            competitors=frozenset(),
            residuals=layer_obj.residuals,
            rank_vector={},
            allowed_next_gates=frozenset({"functional_role_gate"}),
            forbidden_next_gates=frozenset({
                "root_certificate",
                "weight_certificate",
                "meaning_certificate",
                "hukm_certificate",
                "i3rab_certificate",
            }),
            limitations=frozenset([
                "no_root_extraction",
                "no_weight_determination",
                "no_meaning_assignment",
                "no_functional_role_commitment",
                "no_hukm_judgment",
                "no_i3rab_assignment",
            ]),
        )


# ============================================================================
# Surface Potential Profile Builders (U₄-B)
# ============================================================================

def _build_terminal_profile(surface: str) -> TerminalProfile:
    """
    Build terminal profile from orthographic surface.

    Analysis is STRUCTURAL, not grammatical:
    - Detects ة, ـً, ى, ء patterns
    - Does NOT assign case/mood

    Args:
        surface: Orthographic surface string

    Returns:
        TerminalProfile with surface observations only
    """
    if not surface:
        return TerminalProfile(
            ending_surface="",
            terminal_diacritic=None,
            has_tanwin_surface=False,
            has_sukun_surface=False,
            has_taa_marbutah_surface=False,
            has_long_vowel_terminal_surface=False,
            mabni_surface_hint="unresolved",
            murab_surface_hint="unresolved",
            residuals=()
        )

    # Extract terminal characters
    ending_surface = surface[-2:] if len(surface) >= 2 else surface
    terminal_char = surface[-1] if surface else ""

    # Check for tanwīn (ـً ـٌ ـٍ)
    has_tanwin = terminal_char in ["ً", "ٌ", "ٍ"]

    # Check for sukūn (ْ)
    has_sukun = terminal_char in ["ْ"]

    # Check for tāʾ marbūṭa (ة)
    has_taa_marbutah = "ة" in surface

    # Check for long vowel terminal (ا ى و)
    has_long_vowel_terminal = terminal_char in ["ا", "ى", "و"]

    # Extract terminal diacritic
    terminal_diacritic = terminal_char if terminal_char in ["َ", "ُ", "ِ", "ْ", "ً", "ٌ", "ٍ", "ّ"] else None

    # Surface hints (NOT certificates)
    # مبني hint: if sukūn terminal or long vowel, possibly مبني
    mabni_hint = "possible" if (has_sukun or has_long_vowel_terminal) else "unlikely"

    # معرب hint: if tanwīn or vowel diacritics, possibly معرب
    murab_hint = "possible" if (has_tanwin or terminal_diacritic in ["َ", "ُ", "ِ"]) else "unresolved"

    return TerminalProfile(
        ending_surface=ending_surface,
        terminal_diacritic=terminal_diacritic,
        has_tanwin_surface=has_tanwin,
        has_sukun_surface=has_sukun,
        has_taa_marbutah_surface=has_taa_marbutah,
        has_long_vowel_terminal_surface=has_long_vowel_terminal,
        mabni_surface_hint=mabni_hint,
        murab_surface_hint=murab_hint,
        residuals=()
    )


def _build_definiteness_surface_potential(surface: str, unit_type: TrueLafzUnitType) -> DefinitenessSurfacePotential:
    """
    Build definiteness potential from surface and type.

    Checks:
    - الـ prefix present
    - Tanwīn markers (indefinite indicators)
    - Particle nature (particles can't take الـ)

    Does NOT determine if reference is resolved.

    Args:
        surface: Orthographic surface
        unit_type: Unit classification type

    Returns:
        DefinitenessSurfacePotential with surface hints only
    """
    # Check for الـ prefix
    has_al = surface.startswith("ال") or surface.startswith("الـ")

    # Check for tanwīn (indefinite marker)
    has_tanwin = any(c in surface for c in ["ً", "ٌ", "ٍ"])

    # Check for attached pronoun (in unit type context - this unit itself)
    has_attached_pronoun = unit_type == TrueLafzUnitType.ATTACHED_PRONOUN_CANDIDATE

    # Surface hints (NOT resolved reference)
    definite_hint = "possible" if has_al else ("unlikely" if has_tanwin else "unresolved")
    indefinite_hint = "possible" if has_tanwin else ("unlikely" if has_al else "unresolved")
    reference_hint = "possible" if (has_al or has_attached_pronoun) else "unresolved"

    return DefinitenessSurfacePotential(
        has_al_surface=has_al,
        has_tanwin_surface=has_tanwin,
        has_attached_pronoun_surface=has_attached_pronoun,
        definite_surface_hint=definite_hint,
        indefinite_surface_hint=indefinite_hint,
        reference_surface_hint=reference_hint,
        residuals=()
    )


def _build_quantity_surface_potential(surface: str) -> QuantitySurfacePotential:
    """
    Build quantity potential from surface.

    Checks:
    - Dual markers (ـان, ـين)
    - Plural markers (ـون, ـين, ـات)
    - Single character patterns

    Does NOT certify actual quantity.

    Args:
        surface: Orthographic surface

    Returns:
        QuantitySurfacePotential with surface hints only
    """
    # Check for dual markers
    has_dual_marker = surface.endswith("ان") or surface.endswith("ين") or "ـان" in surface or "ـين" in surface

    # Check for plural markers
    has_plural_marker = (
        surface.endswith("ون") or surface.endswith("ين") or surface.endswith("ات") or
        "ـون" in surface or "ـين" in surface or "ـات" in surface
    )

    # Surface hints (NOT certificates)
    dual_hint = "possible" if has_dual_marker else "unlikely"
    plural_hint = "possible" if has_plural_marker else "unlikely"
    singular_hint = "possible" if not (has_dual_marker or has_plural_marker) else "unlikely"

    # Number word and counted object hints (basic surface check)
    number_word_hint = "unresolved"  # Needs semantic analysis
    counted_object_hint = "unresolved"  # Needs semantic analysis

    return QuantitySurfacePotential(
        dual_surface_hint=dual_hint,
        plural_surface_hint=plural_hint,
        singular_surface_hint=singular_hint,
        number_word_surface_hint=number_word_hint,
        counted_object_surface_hint=counted_object_hint,
        residuals=()
    )


def _build_verb_surface_potential(surface: str) -> VerbSurfacePotential:
    """
    Build verb surface potential.

    Checks:
    - Verb prefixes (يـ, تـ, أـ, نـ)
    - Verb suffixes (ـتَ, ـتُمْ, ـنَ)
    - Past patterns (CaCaCa)

    Does NOT certify tense/aspect/mood.

    Args:
        surface: Orthographic surface

    Returns:
        VerbSurfacePotential with surface hints only
    """
    # Check for present verb prefixes
    has_present_prefix = any(surface.startswith(p) for p in ["ي", "ت", "أ", "ن"])

    # Check for verbal suffixes
    has_verbal_suffix = any(s in surface for s in ["ـتَ", "ـتُمْ", "ـنَ", "تَ", "تُمْ", "نَ", "تُ", "تِ"])

    # Surface hints (NOT tense certificates)
    # Present hint: if has present prefix
    present_hint = "possible" if has_present_prefix else "unlikely"

    # Past hint: if no present prefix and appears to be trilateral pattern
    past_hint = "possible" if not has_present_prefix else "unlikely"

    # Imperative hint: if starts with consonant (no prefix)
    imperative_hint = "unresolved"  # Needs more context

    # General verb hint
    verb_hint = "possible" if (has_present_prefix or has_verbal_suffix) else "unresolved"

    return VerbSurfacePotential(
        verb_surface_hint=verb_hint,
        past_surface_hint=past_hint,
        present_surface_hint=present_hint,
        imperative_surface_hint=imperative_hint,
        has_present_prefix_surface=has_present_prefix,
        has_verbal_suffix_surface=has_verbal_suffix,
        residuals=()
    )


def _build_downstream_path_hints(
    unit_type: TrueLafzUnitType,
    verb_potential: VerbSurfacePotential,
    definiteness_potential: DefinitenessSurfacePotential,
    quantity_potential: QuantitySurfacePotential
) -> DownstreamPathHints:
    """
    Build hints for U₅+ layers.

    Combines evidence from other potentials to suggest paths.
    These are HINTS, not commitments.

    Args:
        unit_type: Unit classification type
        verb_potential: Verb surface potential
        definiteness_potential: Definiteness surface potential
        quantity_potential: Quantity surface potential

    Returns:
        DownstreamPathHints with path possibilities
    """
    # Functional role path: always possible for core candidates
    may_open_functional_role = (unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE)

    # Closed class path: for proclitics
    may_open_closed_class = (unit_type == TrueLafzUnitType.BOUND_PROCLITIC)

    # Verb candidate path: if verb surface hint is possible
    may_open_verb = (verb_potential.verb_surface_hint == "possible")

    # Noun candidate path: if not verb or if unresolved
    may_open_noun = (verb_potential.verb_surface_hint != "possible")

    # Reference path: if definiteness hints reference
    may_open_reference = (definiteness_potential.reference_surface_hint == "possible")

    # Quantity path: if dual/plural hints present
    may_open_quantity = (
        quantity_potential.dual_surface_hint == "possible" or
        quantity_potential.plural_surface_hint == "possible"
    )

    # Blocked paths (none by default at U₄)
    blocked = ()

    return DownstreamPathHints(
        may_open_functional_role_path=may_open_functional_role,
        may_open_closed_class_path=may_open_closed_class,
        may_open_verb_candidate_path=may_open_verb,
        may_open_noun_candidate_path=may_open_noun,
        may_open_reference_path=may_open_reference,
        may_open_quantity_path=may_open_quantity,
        blocked_paths=blocked
    )


# ============================================================================
# True Lafẓ Classification Logic
# ============================================================================

# Known proclitics (particles that attach before core)
KNOWN_PROCLITICS = frozenset([
    "وَ", "فَ",           # Conjunctions (standalone capable)
    "بِ", "بِـ",         # Preposition (requires host)
    "لِ", "لِـ",         # Preposition (requires host)
    "كَ", "كَـ",         # Comparison (requires host)
    "سَ", "سَـ",         # Future marker (requires host)
])

# Known pronoun enclitics (attach after core)
KNOWN_PRONOUN_ENCLITICS = frozenset([
    "ـهُ", "هُ",         # 3ms
    "ـهَا", "هَا",       # 3fs
    "ـهُمْ", "هُمْ",     # 3mp
    "ـهِمْ", "هِمْ",     # 3mp genitive
    "ـكَ", "كَ",         # 2ms
    "ـكِ", "كِ",         # 2fs
    "ـنَا", "نَا",       # 1p
])


def _classify_boundary_unit(unit: BoundaryUnit) -> TrueLafzUnitType:
    """
    Classify a boundary unit into lafẓ eligibility type.

    Decision tree:
    1. If unit.surface in KNOWN_PROCLITICS → BOUND_PROCLITIC
    2. If unit.surface in KNOWN_PRONOUN_ENCLITICS → ATTACHED_PRONOUN_CANDIDATE
    3. If unit_type == STANDALONE_CORE or CORE_CANDIDATE → TRUE_SINGULAR_CORE_CANDIDATE
    4. If unit_type == ATTACHED_ENCLITIC → ATTACHED_ENCLITIC (or PRONOUN if known)
    5. Else → TRUE_SINGULAR_CORE_CANDIDATE (conservative default)
    """
    from dal_core.u3_boundary_attachment_carrier import BoundaryUnitType

    surface = unit.surface

    # Check known proclitics
    if surface in KNOWN_PROCLITICS:
        return TrueLafzUnitType.BOUND_PROCLITIC

    # Check known pronoun enclitics
    if surface in KNOWN_PRONOUN_ENCLITICS:
        return TrueLafzUnitType.ATTACHED_PRONOUN_CANDIDATE

    # Check boundary unit type from U₃
    if unit.unit_type == BoundaryUnitType.STANDALONE_CORE:
        return TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE

    if unit.unit_type == BoundaryUnitType.CORE_CANDIDATE:
        return TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE

    if unit.unit_type == BoundaryUnitType.STANDALONE_PROCLITIC:
        return TrueLafzUnitType.BOUND_PROCLITIC

    if unit.unit_type == BoundaryUnitType.ATTACHED_PROCLITIC:
        return TrueLafzUnitType.BOUND_PROCLITIC

    if unit.unit_type == BoundaryUnitType.ATTACHED_ENCLITIC:
        # Check if it's a known pronoun
        if surface in KNOWN_PRONOUN_ENCLITICS:
            return TrueLafzUnitType.ATTACHED_PRONOUN_CANDIDATE
        else:
            return TrueLafzUnitType.ATTACHED_ENCLITIC

    if unit.unit_type == BoundaryUnitType.ORTHOGRAPHIC_COMPOUND:
        return TrueLafzUnitType.ORTHOGRAPHIC_COMPOSITE

    if unit.unit_type == BoundaryUnitType.UNRESOLVED:
        return TrueLafzUnitType.BLOCKED

    # Conservative default: treat as core candidate
    return TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE


# ============================================================================
# True Lafẓ Operations
# ============================================================================

def true_lafz_4(boundary_layer: BoundaryLayerObject) -> TrueLafzResult:
    """
    Determine true singular lafẓ eligibility from boundary units.

    Critical Examples:
        كَتَبَ → TRUE_SINGULAR_CORE_CANDIDATE (single core unit)
        بِكِتَابٍ → بِـ (BOUND_PROCLITIC) + كِتَابٍ (TRUE_SINGULAR_CORE_CANDIDATE)
        وَبِكِتَابِهِمْ → وَ (BOUND_PROCLITIC) + بِـ (BOUND_PROCLITIC) + كِتَابِ (TRUE_SINGULAR_CORE_CANDIDATE) + ـهِمْ (ATTACHED_PRONOUN_CANDIDATE)
        ـهُمْ → ATTACHED_PRONOUN_CANDIDATE (not standalone)

    Args:
        boundary_layer: U₃ layer object with boundary units

    Returns:
        TrueLafzResult with classified lafẓ eligibility units

    Forbidden:
        - Direct jump to Root (U₈)
        - Direct jump to Weight (U₉)
        - Direct jump to Meaning (U₁₅)
        - Direct jump to FunctionalRole (U₅) without going through U₄
    """
    # Validate input
    if not boundary_layer.units:
        return TrueLafzResult(
            success=False,
            layer_object=None,
            failure_type=LafzFailureType.NO_BOUNDARY_UNITS,
            message="No boundary units in input",
            residuals=frozenset([make_blocker("no_units", "Cannot determine lafẓ eligibility without boundary units")])
        )

    # Classify each boundary unit
    lafz_units = []
    all_residuals = []

    for unit in boundary_layer.units:
        # Determine unit type
        unit_type = _classify_boundary_unit(unit)

        # Build evidence
        evidence_items = [
            f"boundary_type={unit.unit_type.value}",
            f"surface={unit.surface}",
            f"classified_as={unit_type.value}",
        ]

        # U₄-B: Build surface potential profiles for TRUE_SINGULAR_CORE_CANDIDATE
        terminal_profile = None
        definiteness_potential = None
        quantity_potential = None
        verb_potential = None
        downstream_hints = None

        if unit_type == TrueLafzUnitType.TRUE_SINGULAR_CORE_CANDIDATE:
            # Build all 5 potential profiles
            terminal_profile = _build_terminal_profile(unit.surface)
            definiteness_potential = _build_definiteness_surface_potential(unit.surface, unit_type)
            quantity_potential = _build_quantity_surface_potential(unit.surface)
            verb_potential = _build_verb_surface_potential(unit.surface)
            downstream_hints = _build_downstream_path_hints(
                unit_type,
                verb_potential,
                definiteness_potential,
                quantity_potential
            )

            # Add profile construction to evidence
            evidence_items.append("surface_potentials_built=true")

        # Create TrueLafzUnit
        lafz_unit = TrueLafzUnit(
            uid=str(uuid4()),
            surface=unit.surface,
            unit_type=unit_type,
            source_boundary_unit_id=unit.uid,
            trace_3=(boundary_layer.uid,),
            evidence=tuple(evidence_items),
            residuals=unit.residuals,  # Preserve residuals from U₃
            rank=unit.rank,
            # U₄-B: Add surface potential profiles
            terminal_profile=terminal_profile,
            definiteness_surface_potential=definiteness_potential,
            quantity_surface_potential=quantity_potential,
            verb_surface_potential=verb_potential,
            downstream_path_hints=downstream_hints
        )
        lafz_units.append(lafz_unit)
        all_residuals.extend(list(unit.residuals))

    # Build layer object
    layer_obj = TrueLafzLayerObject(
        uid=str(uuid4()),
        units=tuple(lafz_units),
        source_boundary_layer_id=boundary_layer.uid,
        trace_3=(boundary_layer.uid,),
        residuals=frozenset(all_residuals),
        rank=boundary_layer.rank,  # Inherit rank from U₃
        proof=None
    )

    # Build proof
    proof = CPB4.build_proof(layer_obj)
    layer_obj = TrueLafzLayerObject(
        uid=layer_obj.uid,
        units=layer_obj.units,
        source_boundary_layer_id=layer_obj.source_boundary_layer_id,
        trace_3=layer_obj.trace_3,
        residuals=layer_obj.residuals,
        rank=layer_obj.rank,
        proof=proof
    )

    return TrueLafzResult(
        success=True,
        layer_object=layer_obj,
        failure_type=None,
        message=f"True lafẓ eligibility determined: {len(lafz_units)} units classified",
        residuals=layer_obj.residuals
    )
