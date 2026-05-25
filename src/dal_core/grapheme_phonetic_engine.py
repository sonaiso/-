"""
Grapheme Phonetic Projection Engine (U₁ Layer)

Main projection function that orchestrates classification and validation.

Critical Laws (No-Jumping Validation):
1. NO syllable formation (CV, CVC, CVV patterns)
2. NO root extraction
3. NO pattern matching (أوزان)
4. NO semantic interpretation
5. Trace preservation mandatory
6. Residuals accumulate, never erased
"""

from typing import List, Optional, Tuple

from dal_core.grapheme_phonetic_projection import (
    GraphemeCarrierU1,
    PhoneticClass1,
    PhoneticProjectionResult,
    GRAPHEME_PHONETIC_HYPOTHESIS_RANK,
    RANK_RESIDUAL,
    extract_marks_from_grapheme,
)
from dal_core.grapheme_phonetic_classifiers import (
    classify_clear_consonant,
    classify_short_vowel,
    detect_long_vowel_candidate,
    classify_sukun_closure,
    apply_shadda_policy,
    apply_tanween_policy,
    classify_ambiguous_letter,
)
from dal_core.atoms import ArabicAtom, carriers_to_atoms
from dal_core.carriers import Carrier, text_to_carriers
from dal_core.residuals import Residual, make_blocker, make_warning, ResidualType
from dal_core.evidence import Evidence, make_evidence


# ============================================================================
# Main Projection Function
# ============================================================================

def project_phonetic1(
    grapheme: GraphemeCarrierU1,
    prev_grapheme: Optional[GraphemeCarrierU1] = None,
    next_grapheme: Optional[GraphemeCarrierU1] = None
) -> PhoneticProjectionResult:
    """
    إسقاط صوتي أولي (Initial Phonetic Projection)

    Projects a grapheme to initial phonetic candidates.

    Args:
        grapheme: Current grapheme to project
        prev_grapheme: Previous grapheme (for context)
        next_grapheme: Next grapheme (for long vowel detection)

    Returns:
        PhoneticProjectionResult with candidates, policies, and residuals

    Critical: Returns CANDIDATES, not certificates.
    Maximum rank: GRAPHEME_PHONETIC_HYPOTHESIS_RANK
    """
    # Try classifiers in order of specificity

    # 1. Clear consonant
    result = classify_clear_consonant(grapheme)
    if result is not None:
        return result

    # 2. Short vowel (on carrier)
    result = classify_short_vowel(grapheme)
    if result is not None:
        return result

    # 3. Long vowel candidate (requires next grapheme)
    if next_grapheme is not None:
        result = detect_long_vowel_candidate(grapheme, next_grapheme)
        if result is not None:
            return result

    # 4. Sukun/closure
    result = classify_sukun_closure(grapheme)
    if result is not None:
        return result

    # 5. Shadda policy
    result = apply_shadda_policy(grapheme)
    if result is not None:
        return result

    # 6. Tanween policy
    result = apply_tanween_policy(grapheme)
    if result is not None:
        return result

    # 7. Ambiguous letters (ا و ي)
    result = classify_ambiguous_letter(grapheme, prev_grapheme)
    if result is not None:
        return result

    # 8. Unclassified - create residual result
    return PhoneticProjectionResult(
        grapheme=grapheme,
        success=False,
        phonetic_class=PhoneticClass1.RESIDUAL,
        residuals=[make_blocker(
            ResidualType.UNKNOWN_ATOM,
            f"Cannot classify grapheme: {grapheme.get_full_grapheme()}",
            location=f"position {grapheme.position}"
        )],
        evidence=[make_evidence(
            "project_phonetic1",
            f"Grapheme {grapheme.get_full_grapheme()} unclassifiable",
            confidence=0.0
        )],
        rank=RANK_RESIDUAL
    )


# ============================================================================
# Batch Projection
# ============================================================================

def project_sequence(graphemes: List[GraphemeCarrierU1]) -> List[PhoneticProjectionResult]:
    """
    إسقاط تسلسل (Sequence Projection)

    Projects a sequence of graphemes with context awareness.

    Returns list of projection results, one per grapheme.
    """
    results = []

    for i, grapheme in enumerate(graphemes):
        prev_g = graphemes[i - 1] if i > 0 else None
        next_g = graphemes[i + 1] if i < len(graphemes) - 1 else None

        result = project_phonetic1(grapheme, prev_g, next_g)
        results.append(result)

    return results


# ============================================================================
# Trace Preservation
# ============================================================================

def preserve_trace_u0_to_u1(
    carrier: Carrier,
    atom: Optional[ArabicAtom],
    grapheme: GraphemeCarrierU1
) -> None:
    """
    حفظ الأثر من U₀ إلى U₁ (Preserve Trace from U₀ to U₁)

    Links U₁ grapheme back to U₀ carrier and atom.

    Critical: Trace must NEVER be lost.
    """
    grapheme.trace0 = carrier
    grapheme.source_atom = atom


def accumulate_residuals(
    existing: List[Residual],
    new: List[Residual]
) -> List[Residual]:
    """
    تراكم البقايا (Accumulate Residuals)

    Residuals accumulate, never get erased.

    Law: Res(output) = Res(input) ⊕ NewResiduals - DischargedByProof
    """
    # Simple concatenation (in real system, would check for duplicates)
    return existing + new


# ============================================================================
# No-Jumping Validation
# ============================================================================

def validate_no_syllable_formation(result: PhoneticProjectionResult) -> Tuple[bool, List[str]]:
    """
    التحقق من عدم تكوين المقطع (Validate No Syllable Formation)

    Ensures that phonetic projection does NOT produce syllable structures.

    Forbidden:
    - CV, CVC, CVV syllable patterns
    - Syllable boundary marking
    - Prosodic structure

    Returns: (is_valid, violation_messages)
    """
    violations = []

    # Check if any candidate claims to be a syllable
    for candidate in result.candidates:
        # Check for forbidden syllable-related features
        if hasattr(candidate, 'syllable_type'):
            violations.append(f"Candidate contains syllable_type field")

        if hasattr(candidate, 'syllable_boundary'):
            violations.append(f"Candidate contains syllable_boundary field")

        # Check length candidates for syllable patterns
        if candidate.length_candidate in {'CV', 'CVC', 'CVV', 'CVCC'}:
            violations.append(
                f"length_candidate '{candidate.length_candidate}' looks like syllable pattern"
            )

    return len(violations) == 0, violations


def validate_no_root_extraction(result: PhoneticProjectionResult) -> Tuple[bool, List[str]]:
    """
    التحقق من عدم استخراج الجذر (Validate No Root Extraction)

    Ensures no root extraction at this layer.

    Forbidden:
    - Root consonants identification
    - Root type (trilateral, quadrilateral)
    """
    violations = []

    for candidate in result.candidates:
        if hasattr(candidate, 'root_consonants'):
            violations.append("Candidate contains root_consonants field")

        if hasattr(candidate, 'root_type'):
            violations.append("Candidate contains root_type field")

    # Check grapheme itself
    if hasattr(result.grapheme, 'root'):
        violations.append("Grapheme contains root field")

    return len(violations) == 0, violations


def validate_no_pattern_matching(result: PhoneticProjectionResult) -> Tuple[bool, List[str]]:
    """
    التحقق من عدم مطابقة الوزن (Validate No Pattern Matching)

    Ensures no morphological pattern (وزن) matching.

    Forbidden:
    - Pattern identification (فَعَل، فاعل، etc.)
    - Morphological class
    """
    violations = []

    for candidate in result.candidates:
        if hasattr(candidate, 'pattern'):
            violations.append("Candidate contains pattern field")

        if hasattr(candidate, 'wazn'):
            violations.append("Candidate contains wazn field")

        if hasattr(candidate, 'morph_class'):
            violations.append("Candidate contains morph_class field")

    return len(violations) == 0, violations


def validate_rank_ceiling(result: PhoneticProjectionResult) -> Tuple[bool, List[str]]:
    """
    التحقق من سقف الرتبة (Validate Rank Ceiling)

    Ensures rank does not exceed grapheme_phonetic_hypothesis.

    Maximum allowed rank: GRAPHEME_PHONETIC_HYPOTHESIS_RANK (0.5)
    """
    violations = []

    if result.rank > GRAPHEME_PHONETIC_HYPOTHESIS_RANK:
        violations.append(
            f"Rank {result.rank} exceeds maximum {GRAPHEME_PHONETIC_HYPOTHESIS_RANK}"
        )

    for candidate in result.candidates:
        if candidate.rank > GRAPHEME_PHONETIC_HYPOTHESIS_RANK:
            violations.append(
                f"Candidate rank {candidate.rank} exceeds maximum"
            )

    return len(violations) == 0, violations


def validate_trace_preserved(result: PhoneticProjectionResult) -> Tuple[bool, List[str]]:
    """
    التحقق من حفظ الأثر (Validate Trace Preserved)

    Ensures trace to U₀ is preserved.
    """
    violations = []

    if result.grapheme.trace0 is None and result.grapheme.source_atom is None:
        violations.append("No trace to U₀ (carrier or atom)")

    return len(violations) == 0, violations


def validate_phonetic_projection(result: PhoneticProjectionResult) -> Tuple[bool, List[str]]:
    """
    التحقق الشامل (Comprehensive Validation)

    Validates all no-jumping laws.

    Returns: (is_valid, all_violations)
    """
    all_violations = []

    # 1. No syllable formation
    valid, viols = validate_no_syllable_formation(result)
    if not valid:
        all_violations.extend(viols)

    # 2. No root extraction
    valid, viols = validate_no_root_extraction(result)
    if not valid:
        all_violations.extend(viols)

    # 3. No pattern matching
    valid, viols = validate_no_pattern_matching(result)
    if not valid:
        all_violations.extend(viols)

    # 4. Rank ceiling
    valid, viols = validate_rank_ceiling(result)
    if not valid:
        all_violations.extend(viols)

    # 5. Trace preserved
    valid, viols = validate_trace_preserved(result)
    if not valid:
        all_violations.extend(viols)

    return len(all_violations) == 0, all_violations


# ============================================================================
# High-Level API: Text to U₁ Projection
# ============================================================================

def text_to_grapheme_projections(text: str) -> Tuple[List[PhoneticProjectionResult], List[Residual]]:
    """
    نص إلى إسقاطات صوتية (Text to Grapheme Projections)

    Complete pipeline: text → U₀ (carriers/atoms) → U₁ (grapheme projections)

    Returns: (projection_results, all_residuals)
    """
    all_residuals = []

    # Step 1: Text → U₀ Carriers
    carriers, carrier_residuals = text_to_carriers(text)
    all_residuals.extend(carrier_residuals)

    # Step 2: Carriers → Atoms
    atoms, atom_residuals = carriers_to_atoms(carriers)
    all_residuals.extend(atom_residuals)

    # Step 3: Build graphemes from atoms
    graphemes = []
    i = 0
    position = 0

    while i < len(atoms):
        atom = atoms[i]

        # Base character
        if atom.kind.name in {'LETTER', 'SPACE', 'PUNCT', 'HAMZA'}:
            base = atom.carrier.char
            marks = []

            # Collect following marks
            j = i + 1
            while j < len(atoms) and atoms[j].is_mark():
                marks.append(atoms[j].carrier.char)
                j += 1

            # Create grapheme
            grapheme = GraphemeCarrierU1(
                base=base,
                marks=marks,
                position=position,
                trace0=atom.carrier,
                source_atom=atom,
                grapheme_class=atom.kind.value,
                residuals=list(atom.residuals)  # Copy atom residuals
            )

            graphemes.append(grapheme)
            i = j
            position += 1
        else:
            # Orphan mark or unknown - skip
            i += 1

    # Step 4: Project phonetics
    projection_results = project_sequence(graphemes)

    # Step 5: Validate all projections
    for result in projection_results:
        is_valid, violations = validate_phonetic_projection(result)
        if not is_valid:
            # Add validation violations as residuals
            for viol in violations:
                result.residuals.append(make_blocker(
                    ResidualType.MALFORMED_STRUCTURE,
                    f"No-jumping validation failed: {viol}",
                    location=f"position {result.grapheme.position}"
                ))
            all_residuals.extend(result.residuals)

    return projection_results, all_residuals


# ============================================================================
# Theorem Verification
# ============================================================================

def verify_grapheme_phonetic_projection_theorem(
    results: List[PhoneticProjectionResult]
) -> Tuple[bool, str]:
    """
    التحقق من مبرهنة الإسقاط الصوتي الكتابي
    (Verify Grapheme Phonetic Projection Theorem)

    Theorem Statement:
    ∀G ∈ U₁, phon_project1(G) ∈ PhoneticCandidate1⁺ ∪ Residual1 ∪ Fail1

    Verification:
    - All graphemes produce either candidates OR residuals
    - No grapheme produces syllable/root/pattern
    - Trace preserved
    - Rank ≤ grapheme_phonetic_hypothesis
    """
    for result in results:
        # Must have either candidates OR residuals
        has_output = len(result.candidates) > 0 or len(result.residuals) > 0

        if not has_output:
            return False, f"Grapheme at position {result.grapheme.position} has no output"

        # Validate no-jumping
        is_valid, violations = validate_phonetic_projection(result)
        if not is_valid:
            return False, f"No-jumping violation: {violations[0]}"

    return True, "Theorem verified: all graphemes produce valid phonetic projections"
