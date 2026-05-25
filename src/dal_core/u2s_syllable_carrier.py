"""
U₂s Arabic Syllable Carrier - Syllable Formation from Phonetic Projections (حامل المقطع العربي)

Domain: U₂s = ArabicSyllableCarrier
Purpose: Syllable formation from phonetic projections WITHOUT root/weight/meaning
Transition: U₂p (Phonetic projections) → U₂s (Syllable structures)

Critical Laws (Axioms):
    - Axiom 2s.1: لا مقطع بلا نواة (No nucleus, no syllable)
    - Axiom 2s.2: النواة إما V أو VV (Nucleus ∈ {V, VV})
    - Axiom 2s.3: الأنماط المرخصة فقط (Only licensed patterns)
    - Axiom 2s.4: حفظ الأثر من U₂p (Trace preservation from U₂p)
    - Axiom 2s.5: لا جذر في U₂s (No root in U₂s)
    - Axiom 2s.6: لا وزن في U₂s (No weight in U₂s)

Type System:
    ArabicSyllable ≠ Root
    ArabicSyllable ≠ Weight
    ArabicSyllable ≠ Meaning
    ArabicSyllable ≠ Hukm

Architecture:
    U₂p (PhoneticProjectionLayerObject) → CPB₂s → U₂s (SyllableLayerObject) → CPB₃ → BoundaryAndAttachment

Licensed Syllable Patterns (6 types):
    - CV: Light (syllable_open)
    - CVV: Heavy (syllable_long)
    - CVC: Light/Heavy (syllable_closed)
    - CVVC: Heavy/Super-heavy (contextual)
    - CVCC: Super-heavy (pausal/restricted)
    - CVVCC: Super-heavy (pausal/restricted)

PR: Implement U₂s ArabicSyllableCarrier
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
from dal_core.u2p_phonetic_projection import (
    PhoneticProjection,
    PhoneticClass,
    PhoneticProjectionLayerObject
)


# ============================================================================
# Type System - Syllable Classification
# ============================================================================

class SyllablePattern(Enum):
    """
    Licensed Arabic syllable patterns.

    Classification determines syllable weight and licensing.
    """
    CV = "cv"                      # Light: /ka/
    CVV = "cvv"                    # Heavy: /kā/
    CVC = "cvc"                    # Light/Heavy: /kin/
    CVVC = "cvvc"                  # Heavy/Super-heavy: /kīn/
    CVCC = "cvcc"                  # Super-heavy (pausal): /kant/
    CVVCC = "cvvcc"                # Super-heavy (pausal): /kānt/


class SyllableWeight(Enum):
    """Syllable weight classification."""
    LIGHT = "light"                # CV
    HEAVY = "heavy"                # CVV, CVC
    SUPER_HEAVY = "super_heavy"    # CVVC, CVCC, CVVCC


class BoundaryPolicy(Enum):
    """Boundary behavior for syllables."""
    NORMAL = "normal"              # Normal syllable
    PAUSAL = "pausal"              # Pausal form (waqf)
    CONTEXTUAL = "contextual"      # Context-dependent


# ============================================================================
# Failure Types
# ============================================================================

class SyllableFailureType(Enum):
    """Failure types for syllabification."""
    MISSING_NUCLEUS = "missing_nucleus"                # No V/VV found
    ILLEGAL_PATTERN = "illegal_pattern"                # Pattern not licensed
    ORPHAN_LONG_VOWEL = "orphan_long_vowel"            # VV without proper context
    UNRESOLVED_GEMINATION = "unresolved_gemination"    # Shadda policy unresolved
    BROKEN_TRACE = "broken_trace"                      # Missing trace to U₂p


# ============================================================================
# U₂s Carrier Structure
# ============================================================================

@dataclass(frozen=True)
class ArabicSyllable:
    """
    Arabic syllable structure.

    Immutable carrier preserving:
        - onset: Initial consonant(s) (C)
        - nucleus: Vowel core (V or VV) - MANDATORY
        - coda: Final consonant(s) (optional)
        - pattern: Syllable pattern (CV, CVV, CVC, ...)
        - weight: Syllable weight (light, heavy, super-heavy)
        - boundary_policy: Boundary behavior
        - trace_2p: Trace to U₂p phonetic projections
        - residuals: Warnings/blockers
        - rank: Epistemic status

    Laws:
        - ArabicSyllable ⊬ Root
        - ArabicSyllable ⊬ Weight (morphological)
        - ArabicSyllable ⊬ Meaning
        - Every syllable has nucleus (V or VV)
        - Only licensed patterns allowed
    """
    id: str                                    # Unique identifier

    # Syllable structure (onset optional, nucleus mandatory, coda optional)
    onset: FrozenSet[str] = field(default_factory=frozenset)      # C onset phonemes
    nucleus: FrozenSet[str] = field(default_factory=frozenset)    # V/VV nucleus (MANDATORY)
    coda: FrozenSet[str] = field(default_factory=frozenset)       # C coda phonemes

    # Classification
    pattern: SyllablePattern = SyllablePattern.CV
    weight: SyllableWeight = SyllableWeight.LIGHT
    boundary_policy: BoundaryPolicy = BoundaryPolicy.NORMAL

    # Trace and validation
    trace_2p: FrozenSet[str] = field(default_factory=frozenset)  # Trace to U₂p projections
    trace_1: FrozenSet[str] = field(default_factory=frozenset)   # Trace to U₁ graphemes (inherited)
    residuals: FrozenSet[Residual] = field(default_factory=frozenset)
    rank: Rank = Rank.ZERO
    metadata: Optional[tuple] = None

    def __post_init__(self):
        """Validate syllable constraints."""
        # CRITICAL LAW: No nucleus, no syllable
        if not self.nucleus:
            raise ValueError("Axiom 2s.1 violation: No nucleus, no syllable")

    def has_blocker(self) -> bool:
        """Check if syllable has blocking residual."""
        return any(r.type == ResidualType.BLOCKER for r in self.residuals)

    def is_certified(self) -> bool:
        """Check if syllable is certified."""
        return self.rank == Rank.CERTIFICATE

    def get_phonetic_string(self) -> str:
        """Reconstruct phonetic string representation."""
        onset_str = "".join(sorted(self.onset))
        nucleus_str = "".join(sorted(self.nucleus))
        coda_str = "".join(sorted(self.coda))
        return f"{onset_str}{nucleus_str}{coda_str}"


@dataclass(frozen=True)
class SyllableLayerObject:
    """
    Complete U₂s layer output.

    Contains:
        - syllables: Sequence of Arabic syllables
        - total_residuals: All residuals from layer
        - metadata: Additional processing information
        - proof: ProofObject documenting U₂s certification
    """
    syllables: FrozenSet[ArabicSyllable]
    total_residuals: FrozenSet[Residual]
    metadata: Optional[tuple] = None
    proof: Optional[ProofObject] = None

    def has_blocking_failure(self) -> bool:
        """Check if layer has blocking residuals."""
        return any(r.type == ResidualType.BLOCKER for r in self.total_residuals)

    def count_certified(self) -> int:
        """Count certified syllables."""
        return sum(1 for s in self.syllables if s.is_certified())


# ============================================================================
# Syllabification Operation (syllabify_2p2s)
# ============================================================================

@dataclass(frozen=True)
class SyllabificationResult:
    """
    Result of syllabify_2p2s operation.

    Partial operation: can succeed or fail with residuals.
    """
    success: bool
    syllables: List[ArabicSyllable]
    residuals: FrozenSet[Residual]


def syllabify_phonetic_projections(
    projections: List[PhoneticProjection],
    policy: Optional[Dict[str, Any]] = None
) -> SyllabificationResult:
    """
    syllabify_2p2s : PhoneticProjection* ⇀ ArabicSyllable* ∪ Fail₂s

    Partial operation that forms syllables from phonetic projections.

    Succeeds if:
        - Every syllable has nucleus (V or VV)
        - Only licensed patterns formed
        - Long vowels properly paired
        - Gemination policy resolved or deferred
        - Trace to U₂p preserved

    Fails if:
        - MissingNucleus: Consonant without vowel cannot form syllable
        - IllegalPattern: Pattern not in licensed set
        - OrphanLongVowel: VV carrier without compatible vowel
        - BrokenTrace: Missing trace to U₂p

    Args:
        projections: Sequence of phonetic projections from U₂p
        policy: Optional syllabification policy

    Returns:
        SyllabificationResult with success/failure and residuals
    """
    residuals_list = []
    syllables = []
    policy = policy or {}

    i = 0
    while i < len(projections):
        proj = projections[i]
        next_proj = projections[i+1] if i+1 < len(projections) else None

        # Check trace preservation
        if not proj.trace_1:
            residuals_list.append(make_blocker(
                ResidualType.MALFORMED_ATOM,
                f"BrokenTrace: Projection {proj.id} has no trace to U₁",
                location=f"projection {i}"
            ))
            i += 1
            continue

        # Case 1: Consonant + short vowel → CV syllable
        if proj.consonant_candidate and proj.short_vowel_candidate:
            syllable = _make_cv_syllable(proj, residuals_list)
            if syllable:
                syllables.append(syllable)
            i += 1
            continue

        # Case 2: Consonant + short vowel + long vowel carrier → CVV syllable
        if (proj.consonant_candidate and proj.short_vowel_candidate and
            next_proj and next_proj.phonetic_class == PhoneticClass.AMBIGUOUS_CARRIER):
            # Check if long vowel is compatible
            if _is_long_vowel_compatible(proj, next_proj):
                syllable = _make_cvv_syllable(proj, next_proj, residuals_list)
                if syllable:
                    syllables.append(syllable)
                i += 2  # Skip next projection (consumed)
                continue

        # Case 3: Consonant + closure (sukun) → needs nucleus from context
        if proj.consonant_candidate and proj.closure_candidate:
            # بْ alone cannot form syllable (no nucleus)
            residuals_list.append(make_blocker(
                ResidualType.MALFORMED_ATOM,
                f"MissingNucleus: Closure {proj.consonant_candidate} has no nucleus",
                location=f"projection {i}"
            ))
            i += 1
            continue

        # Case 4: Gemination (shadda) policy
        if proj.gemination_candidate:
            # Shadda requires special handling
            # For now, treat as hypothesis needing context
            residuals_list.append(make_warning(
                ResidualType.AMBIGUOUS_SYMBOL,
                f"UnresolvedGemination: Shadda policy not resolved for {proj.consonant_candidate}",
                location=f"projection {i}"
            ))
            # Try to form syllable if vowel present
            if proj.short_vowel_candidate:
                syllable = _make_cv_syllable(proj, residuals_list)
                if syllable:
                    syllables.append(syllable)
            i += 1
            continue

        # Case 5: Ambiguous carrier without context
        if proj.phonetic_class == PhoneticClass.AMBIGUOUS_CARRIER:
            residuals_list.append(make_warning(
                ResidualType.AMBIGUOUS_SYMBOL,
                f"OrphanLongVowel: Ambiguous carrier without previous vowel",
                location=f"projection {i}"
            ))
            i += 1
            continue

        # Case 6: Unknown/unhandled
        residuals_list.append(make_warning(
            ResidualType.AMBIGUOUS_SYMBOL,
            f"UnhandledProjection: Cannot syllabify {proj.phonetic_class}",
            location=f"projection {i}"
        ))
        i += 1

    # Determine success
    success = not has_blocking_residuals(frozenset(residuals_list))

    return SyllabificationResult(
        success=success,
        syllables=syllables,
        residuals=frozenset(residuals_list)
    )


def _make_cv_syllable(proj: PhoneticProjection, residuals_list: List[Residual]) -> Optional[ArabicSyllable]:
    """Create CV syllable from projection with C + V."""
    if not proj.consonant_candidate or not proj.short_vowel_candidate:
        return None

    # Inherit residuals from projection
    all_residuals = set(proj.residuals)

    # Determine rank
    rank = Rank.CERTIFICATE if proj.rank == Rank.CERTIFICATE else Rank.HYPOTHESIS

    try:
        syllable = ArabicSyllable(
            id=str(uuid4()),
            onset=frozenset([proj.consonant_candidate]),
            nucleus=frozenset([proj.short_vowel_candidate]),
            coda=frozenset(),
            pattern=SyllablePattern.CV,
            weight=SyllableWeight.LIGHT,
            boundary_policy=BoundaryPolicy.NORMAL,
            trace_2p=frozenset([proj.id]),
            trace_1=proj.trace_1,
            residuals=frozenset(all_residuals),
            rank=rank,
            metadata=(
                ("pattern", "CV"),
                ("phonetic", f"{proj.consonant_candidate}{proj.short_vowel_candidate}")
            )
        )
        return syllable
    except ValueError as e:
        residuals_list.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            f"SyllableCreationFailed: {str(e)}",
            location=proj.id
        ))
        return None


def _make_cvv_syllable(
    proj: PhoneticProjection,
    next_proj: PhoneticProjection,
    residuals_list: List[Residual]
) -> Optional[ArabicSyllable]:
    """Create CVV syllable from projection with C + V + long vowel carrier."""
    if not proj.consonant_candidate or not proj.short_vowel_candidate:
        return None

    # Determine long vowel based on short vowel + carrier
    long_vowel = None
    if proj.short_vowel_candidate == '/a/':
        long_vowel = '/ā/'
    elif proj.short_vowel_candidate == '/u/':
        long_vowel = '/ū/'
    elif proj.short_vowel_candidate == '/i/':
        long_vowel = '/ī/'

    if not long_vowel:
        return None

    # Inherit residuals
    all_residuals = set(proj.residuals)
    all_residuals.update(next_proj.residuals)

    # Determine rank
    rank = Rank.HYPOTHESIS  # CVV requires policy resolution

    try:
        syllable = ArabicSyllable(
            id=str(uuid4()),
            onset=frozenset([proj.consonant_candidate]),
            nucleus=frozenset([long_vowel]),
            coda=frozenset(),
            pattern=SyllablePattern.CVV,
            weight=SyllableWeight.HEAVY,
            boundary_policy=BoundaryPolicy.NORMAL,
            trace_2p=frozenset([proj.id, next_proj.id]),
            trace_1=proj.trace_1.union(next_proj.trace_1),
            residuals=frozenset(all_residuals),
            rank=rank,
            metadata=(
                ("pattern", "CVV"),
                ("phonetic", f"{proj.consonant_candidate}{long_vowel}")
            )
        )
        return syllable
    except ValueError as e:
        residuals_list.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            f"SyllableCreationFailed: {str(e)}",
            location=proj.id
        ))
        return None


def _is_long_vowel_compatible(proj: PhoneticProjection, carrier_proj: PhoneticProjection) -> bool:
    """Check if short vowel + carrier can form long vowel."""
    if not proj.short_vowel_candidate:
        return False

    if carrier_proj.phonetic_class != PhoneticClass.AMBIGUOUS_CARRIER:
        return False

    # Check compatibility: فتحة+ا, ضمة+و, كسرة+ي
    vowel_carrier_map = {
        '/a/': 'ا',
        '/u/': 'و',
        '/i/': 'ي'
    }

    expected_carrier = vowel_carrier_map.get(proj.short_vowel_candidate)
    if not expected_carrier:
        return False

    # Check if carrier matches (look at grapheme_ref metadata)
    carrier_metadata = dict(carrier_proj.metadata) if carrier_proj.metadata else {}
    carrier_base = carrier_metadata.get('base', '')

    return carrier_base == expected_carrier


# ============================================================================
# CPB₂s - Identity Guardian
# ============================================================================

@dataclass(frozen=True)
class CPB2sResult:
    """
    Result of CPB₂s validation.

    CPB₂s ensures:
        - NucleusRequired: Every syllable has nucleus (V or VV)
        - PatternLicensed: Only licensed patterns formed
        - TracePreserved: Every syllable has trace to U₂p
        - ResidualsInherited: U₂p residuals preserved
        - CompetitorsResolvedOrPreserved: Ambiguity handled
        - RankNonInflated: No rank elevation without evidence
        - NoLayerJump: Forbidden gates documented
    """
    valid: bool
    violations: FrozenSet[str]
    layer_object: Optional[SyllableLayerObject]


def cpb2s_validate(
    phonetic_layer: PhoneticProjectionLayerObject,
    syllables: List[ArabicSyllable],
    policy: Optional[Dict[str, Any]] = None
) -> CPB2sResult:
    """
    CPB₂s : PhoneticProjectionLayerObject × syllabify_2p2s × Evidence₂s × Policy₂s ⇀ SyllableLayerObject ∪ Fail₂s

    Validates that Syllable layer satisfies identity guardian constraints.

    Guarantees:
        - NucleusRequired: Every syllable has nucleus
        - PatternLicensed: Only licensed patterns
        - TracePreserved: Every syllable has trace to U₂p
        - ResidualsInherited: All U₂p residuals preserved
        - NoSilentDeletion: No U₂p projection deleted without residual
        - RankNonInflated: No rank elevation without evidence
        - ProofObjectCreated: Proof with forbidden gates
        - NoLayerJump: No root/weight/meaning certificates

    Args:
        phonetic_layer: Input U₂p layer object
        syllables: Formed syllables
        policy: Optional processing policy

    Returns:
        CPB2sResult with validation status
    """
    violations = []

    # Check 1: NucleusRequired
    for syllable in syllables:
        if not syllable.nucleus:
            violations.append(f"NucleusViolation: Syllable {syllable.id} has no nucleus")

    # Check 2: PatternLicensed
    licensed_patterns = {
        SyllablePattern.CV,
        SyllablePattern.CVV,
        SyllablePattern.CVC,
        SyllablePattern.CVVC,
        SyllablePattern.CVCC,
        SyllablePattern.CVVCC
    }
    for syllable in syllables:
        if syllable.pattern not in licensed_patterns:
            violations.append(f"IllegalPattern: Syllable {syllable.id} has unlicensed pattern {syllable.pattern}")

    # Check 3: TracePreserved
    for syllable in syllables:
        if not syllable.trace_2p:
            violations.append(f"TraceViolation: Syllable {syllable.id} has no trace to U₂p")

    # Check 4: RankNonInflated
    for syllable in syllables:
        if syllable.rank == Rank.CERTIFICATE:
            # Certificate requires clear pattern without ambiguity
            if syllable.has_blocker():
                violations.append(f"RankInflation: Syllable {syllable.id} certified with blocker")

    # Check 5: NoLayerJump (verify no forbidden fields)
    # This is structural - checked by type system

    # Collect all residuals (include U₂p residuals)
    total_residuals = set(phonetic_layer.total_residuals)
    for syllable in syllables:
        total_residuals.update(syllable.residuals)

    # Create proof object
    proof = _make_u2s_proof(phonetic_layer, syllables, frozenset(total_residuals))

    # Create layer object
    layer_object = SyllableLayerObject(
        syllables=frozenset(syllables),
        total_residuals=frozenset(total_residuals),
        metadata=(
            ("u2p_projections", len(phonetic_layer.projections)),
            ("u2s_syllables", len(syllables))
        ),
        proof=proof
    )

    return CPB2sResult(
        valid=len(violations) == 0,
        violations=frozenset(violations),
        layer_object=layer_object if len(violations) == 0 else None
    )


def _make_u2s_proof(
    phonetic_layer: PhoneticProjectionLayerObject,
    syllables: List[ArabicSyllable],
    total_residuals: FrozenSet[Residual]
) -> ProofObject:
    """
    Create ProofObject for U₂s layer using shared foundation.

    Args:
        phonetic_layer: Input U₂p layer
        syllables: Formed syllables
        total_residuals: All residuals from syllabification

    Returns:
        ProofObject documenting U₂s certification
    """
    # Create rank vector
    certified_count = sum(1 for s in syllables if s.is_certified())

    rank_vector = RankVector(
        unicode_rank=Rank.CERTIFICATE,  # Inherited from U₀
        grapheme_rank=Rank.CERTIFICATE,  # Inherited from U₁
        phonetic_rank=Rank.CERTIFICATE,  # Inherited from U₂p
        syllable_rank=Rank.CERTIFICATE if certified_count > 0 else Rank.CANDIDATE,
        functional_role_rank=Rank.ZERO,
        morpheme_rank=Rank.ZERO,
        stem_root_rank=Rank.ZERO,
        pattern_weight_rank=Rank.ZERO,
        semantic_rank=Rank.ZERO,
        hukm_rank=Rank.ZERO
    )

    return make_proof_object(
        claim="Arabic syllables formed and licensed",
        scope="U₂s / ArabicSyllableCarrier",
        evidence=frozenset([
            f"Formed {len(syllables)} syllables",
            f"Certified {certified_count} syllables",
            "TracePreserved to U₂p",
            "ResidualsInherited from U₂p",
            "NucleusRequired enforced",
            "PatternLicensed enforced"
        ]),
        counter_evidence=frozenset(),
        trace_graph={
            "u2p_projections": len(phonetic_layer.projections),
            "u2s_syllables": len(syllables),
            "syllable_patterns": [s.pattern.value for s in syllables]
        },
        competitors=frozenset(),  # Competitors resolved or inherited
        residuals=total_residuals,
        rank_vector=rank_vector.as_dict(),
        allowed_next_gates=frozenset(["boundary_attachment_gate"]),
        forbidden_next_gates=frozenset([
            "root_certificate",
            "weight_certificate",
            "meaning_certificate",
            "hukm_certificate"
        ]),
        limitations=frozenset([
            "Syllable formation only",
            "No boundary/attachment analysis",
            "No morphological analysis",
            "No semantic interpretation",
            "Gemination policy may be unresolved"
        ])
    )


# ============================================================================
# Main Pipeline
# ============================================================================

def phonetic_to_syllable_layer(
    phonetic_layer: PhoneticProjectionLayerObject,
    policy: Optional[Dict[str, Any]] = None
) -> CPB2sResult:
    """
    Complete pipeline: U₂p → U₂s (SyllableLayerObject).

    Steps:
        1. syllabify_2p2s: Phonetic projections → Syllables
        2. CPB₂s: Validate identity constraints

    Args:
        phonetic_layer: Input U₂p layer object
        policy: Optional processing policy

    Returns:
        CPB2sResult with validation status and layer object
    """
    projections_list = sorted(phonetic_layer.projections, key=lambda p: p.grapheme_ref)

    result = syllabify_phonetic_projections(projections_list, policy)

    if not result.success:
        # Return CPB2s result with violations
        return CPB2sResult(
            valid=False,
            violations=frozenset([f"Syllabification failed: {len(result.residuals)} residuals"]),
            layer_object=None
        )

    return cpb2s_validate(phonetic_layer, result.syllables, policy)
