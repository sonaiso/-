"""
Grapheme Phonetic Classifiers (U₁ Layer)

Classification functions that produce phonetic CANDIDATES, not certificates.

Critical Law: NO jumping to syllable/root/pattern/meaning at this layer.
"""

from typing import Optional, List, Tuple

from dal_core.grapheme_phonetic_projection import (
    GraphemeCarrierU1,
    PhoneticClass1,
    PhoneticCandidate,
    PhoneticProjectionResult,
    PolicyDeclaration,
    MakhrajCandidate,
    VowelCandidate,
    ClosureCandidate,
    ShaddahPolicy,
    TanweenPolicy,
    MaddPolicy,
    BoundaryPolicy,
    CLEAR_CONSONANTS,
    AMBIGUOUS_LETTERS,
    HAMZA_CARRIERS,
    SHORT_VOWEL_MARKS,
    LONG_VOWEL_COMPAT,
    TANWEEN_MARKS,
    SUKUN_MARK,
    SHADDA_MARK,
    RANK_CLEAR_CLASSIFICATION,
    RANK_POLICY_DEPENDENT,
    RANK_AMBIGUOUS_CANDIDATE,
    RANK_DEFERRED,
    RANK_RESIDUAL,
    has_mark,
    get_short_vowel,
    has_shadda,
    has_sukun,
    get_tanween,
)
from dal_core.residuals import Residual, make_blocker, make_warning, ResidualType
from dal_core.evidence import Evidence, make_evidence


# ============================================================================
# 1. Clear Consonant Classification
# ============================================================================

def classify_clear_consonant(grapheme: GraphemeCarrierU1) -> Optional[PhoneticProjectionResult]:
    """
    تصنيف الصامت الواضح (Clear Consonant Classification)

    Classifies unambiguous Arabic consonants: ب، ت، ج، د...

    Returns phonetic candidate, NOT a phonological certificate.
    """
    if grapheme.base not in CLEAR_CONSONANTS:
        return None

    # Create consonant candidate
    makhraj = MakhrajCandidate(
        region="تقريبي",  # Approximate, not final
        confidence=0.8,
        evidence=[make_evidence(
            "CLEAR_CONSONANTS table",
            f"Character {grapheme.base} is clear consonant"
        )]
    )

    candidate = PhoneticCandidate(
        makhraj_candidate=makhraj,
        length_candidate="single",
        confidence=0.8,
        rank=RANK_CLEAR_CLASSIFICATION
    )

    result = PhoneticProjectionResult(
        grapheme=grapheme,
        success=True,
        phonetic_class=PhoneticClass1.CLEAR_CONSONANT_C,
        candidates=[candidate],
        evidence=[make_evidence(
            "classify_clear_consonant",
            f"{grapheme.base} classified as clear consonant candidate"
        )],
        rank=RANK_CLEAR_CLASSIFICATION
    )

    return result


# ============================================================================
# 2. Clear Short Vowel Classification
# ============================================================================

def classify_short_vowel(grapheme: GraphemeCarrierU1) -> Optional[PhoneticProjectionResult]:
    """
    تصنيف الصائت القصير الواضح (Clear Short Vowel Classification)

    Classifies short vowel marks: َ ُ ِ
    MUST be attached to a carrier (base character).

    Critical: Orphan diacritics → residual
    """
    vowel_type = get_short_vowel(grapheme.marks)

    if vowel_type is None:
        return None

    # Check if vowel is attached to carrier
    if not grapheme.base or grapheme.base.isspace():
        # Orphan vowel - create residual
        residual = make_blocker(
            ResidualType.MALFORMED_ATOM,
            "Short vowel without carrier",
            location=f"position {grapheme.position}"
        )
        return PhoneticProjectionResult(
            grapheme=grapheme,
            success=False,
            phonetic_class=PhoneticClass1.RESIDUAL,
            residuals=[residual],
            rank=RANK_RESIDUAL
        )

    # Create vowel candidate
    vowel_cand = VowelCandidate(
        quality=vowel_type,
        length="short",
        confidence=0.85,
        evidence=[make_evidence(
            "SHORT_VOWEL_MARKS table",
            f"Mark classified as {vowel_type}"
        )]
    )

    candidate = PhoneticCandidate(
        vowel_candidate=vowel_cand,
        length_candidate="short",
        confidence=0.85,
        rank=RANK_CLEAR_CLASSIFICATION
    )

    result = PhoneticProjectionResult(
        grapheme=grapheme,
        success=True,
        phonetic_class=PhoneticClass1.CLEAR_SHORT_VOWEL_V,
        candidates=[candidate],
        evidence=[make_evidence(
            "classify_short_vowel",
            f"Short vowel {vowel_type} candidate on {grapheme.base}"
        )],
        rank=RANK_CLEAR_CLASSIFICATION
    )

    return result


# ============================================================================
# 3. Long Vowel Candidate Detection
# ============================================================================

def detect_long_vowel_candidate(
    current: GraphemeCarrierU1,
    next_grapheme: Optional[GraphemeCarrierU1]
) -> Optional[PhoneticProjectionResult]:
    """
    كشف مرشح الصائت الطويل (Long Vowel Candidate Detection)

    Detects long vowel candidates based on relation between two graphemes:
    - Current has short vowel: َ ُ ِ
    - Next is compatible letter: ا و ي

    Examples:
    - بَا → /bā/ candidate
    - بُو → /bū/ candidate
    - بِي → /bī/ candidate

    Critical: This is RELATION-BASED, not single grapheme classification.
    """
    if next_grapheme is None:
        return None

    # Check if current has short vowel
    vowel_type = get_short_vowel(current.marks)
    if vowel_type is None:
        return None

    # Check if next is compatible long vowel letter
    compat_letter = LONG_VOWEL_COMPAT.get(vowel_type)
    if compat_letter is None or next_grapheme.base != compat_letter:
        return None

    # Create long vowel candidate
    vowel_cand = VowelCandidate(
        quality=vowel_type,
        length="long",
        confidence=0.75,
        evidence=[make_evidence(
            "LONG_VOWEL_COMPAT table",
            f"{vowel_type} + {compat_letter} → long vowel candidate"
        )]
    )

    candidate = PhoneticCandidate(
        vowel_candidate=vowel_cand,
        length_candidate="long",
        confidence=0.75,
        rank=RANK_CLEAR_CLASSIFICATION
    )

    # Note: This affects TWO graphemes (current + next)
    result = PhoneticProjectionResult(
        grapheme=current,  # Anchored to first grapheme
        success=True,
        phonetic_class=PhoneticClass1.CLEAR_LONG_VOWEL_VV,
        candidates=[candidate],
        evidence=[make_evidence(
            "detect_long_vowel_candidate",
            f"Long vowel candidate: {current.base}{current.marks} + {next_grapheme.base}"
        )],
        rank=RANK_CLEAR_CLASSIFICATION
    )

    # Add residual note about second grapheme
    result.residuals.append(make_warning(
        ResidualType.AMBIGUOUS_SYMBOL,
        f"Next grapheme {next_grapheme.base} consumed by long vowel",
        location=f"position {next_grapheme.position}"
    ))

    return result


# ============================================================================
# 4. Sukun / Closure Candidate Classification
# ============================================================================

def classify_sukun_closure(grapheme: GraphemeCarrierU1) -> Optional[PhoneticProjectionResult]:
    """
    تصنيف السكون أو الإغلاق (Sukun/Closure Classification)

    Sukun mark (ْ) indicates potential syllable closure (coda).

    Critical: This is CANDIDATE for coda, not final syllable structure.
    Actual syllabification happens in U₂.
    """
    if not has_sukun(grapheme.marks):
        return None

    # Create closure candidate
    closure_cand = ClosureCandidate(
        is_coda=True,  # Candidate for coda
        is_sukun=True,  # Written sukun present
        confidence=0.7,
        evidence=[make_evidence(
            "sukun mark",
            f"Sukun on {grapheme.base} → closure candidate"
        )]
    )

    candidate = PhoneticCandidate(
        closure_candidate=closure_cand,
        length_candidate="closure",
        confidence=0.7,
        rank=RANK_POLICY_DEPENDENT
    )

    result = PhoneticProjectionResult(
        grapheme=grapheme,
        success=True,
        phonetic_class=PhoneticClass1.SUKUN_OR_CLOSURE,
        candidates=[candidate],
        evidence=[make_evidence(
            "classify_sukun_closure",
            f"Sukun mark → closure candidate (not final syllable)"
        )],
        rank=RANK_POLICY_DEPENDENT
    )

    # Add residual: final resolution needs context
    result.residuals.append(make_warning(
        ResidualType.AMBIGUOUS_SYMBOL,
        "Sukun closure needs syllable context (U₂)",
        location=f"position {grapheme.position}"
    ))

    return result


# ============================================================================
# 5. Shadda Policy Handler
# ============================================================================

def apply_shadda_policy(grapheme: GraphemeCarrierU1) -> Optional[PhoneticProjectionResult]:
    """
    تطبيق سياسة الشدة (Shadda Policy Application)

    Shadda (ّ) indicates gemination/doubling.

    Policy options:
    1. PreserveAsMark - keep as written mark
    2. ExpandToGeminateCandidate - suggest C₁ْ + C₂َ expansion
    3. DeferToU₂ - resolve in phonological layer

    Critical: We don't PERFORM expansion here, just declare candidates.
    """
    if not has_shadda(grapheme.marks):
        return None

    # Default policy: preserve + geminate candidate
    policy = PolicyDeclaration(
        policy_type="shadda",
        policy_choice=ShaddahPolicy.EXPAND_TO_GEMINATE_CANDIDATE,
        constraints={"requires_phonology_layer": True}
    )

    # Create gemination candidate
    # Example: نَّ → could expand to نْ + نَ
    # But we DON'T perform expansion here, just note the candidate

    geminate_candidate = PhoneticCandidate(
        makhraj_candidate=MakhrajCandidate(
            region="geminate_hypothesis",
            confidence=0.65,
            evidence=[make_evidence(
                "shadda mark",
                f"Shadda on {grapheme.base} → gemination candidate"
            )]
        ),
        length_candidate="geminate",
        confidence=0.65,
        rank=RANK_POLICY_DEPENDENT
    )

    policy.candidates.append(geminate_candidate)

    result = PhoneticProjectionResult(
        grapheme=grapheme,
        success=True,
        phonetic_class=PhoneticClass1.SHADDA_POLICY,
        candidates=[geminate_candidate],
        policies=[policy],
        evidence=[make_evidence(
            "apply_shadda_policy",
            f"Shadda → geminate candidate (expansion deferred)"
        )],
        rank=RANK_POLICY_DEPENDENT
    )

    # Critical residual: expansion not performed at U₁
    result.residuals.append(make_warning(
        ResidualType.AMBIGUOUS_SYMBOL,
        "Shadda expansion deferred to U₂ phonology layer",
        location=f"position {grapheme.position}"
    ))

    return result


# ============================================================================
# 6. Tanween Policy Handler
# ============================================================================

def apply_tanween_policy(grapheme: GraphemeCarrierU1) -> Optional[PhoneticProjectionResult]:
    """
    تطبيق سياسة التنوين (Tanween Policy Application)

    Tanween (ً ٌ ٍ) indicates nunation: vowel + /n/.

    Policy: Waqf-sensitive
    - In wasl (connected): /un/, /an/, /in/
    - In waqf (pausal): vowel only (or ā for /an/)

    Critical: We preserve BOTH candidates, don't choose.
    """
    tanween_info = get_tanween(grapheme.marks)
    if tanween_info is None:
        return None

    tanween_name, vowel_quality, nun = tanween_info

    # Default policy: preserve both wasl and waqf candidates
    policy = PolicyDeclaration(
        policy_type="tanween",
        policy_choice=TanweenPolicy.WAQF_SENSITIVE,
        constraints={
            "wasl_realization": f"{vowel_quality}+{nun}",
            "waqf_realization": vowel_quality
        }
    )

    # Wasl candidate: vowel + n
    wasl_candidate = PhoneticCandidate(
        vowel_candidate=VowelCandidate(
            quality=vowel_quality,
            length="short",
            confidence=0.7
        ),
        length_candidate="short+n",
        confidence=0.7,
        rank=RANK_POLICY_DEPENDENT
    )

    # Waqf candidate: vowel only
    waqf_candidate = PhoneticCandidate(
        vowel_candidate=VowelCandidate(
            quality=vowel_quality,
            length="short",
            confidence=0.7
        ),
        length_candidate="short",
        confidence=0.7,
        rank=RANK_POLICY_DEPENDENT
    )

    policy.candidates.extend([wasl_candidate, waqf_candidate])

    result = PhoneticProjectionResult(
        grapheme=grapheme,
        success=True,
        phonetic_class=PhoneticClass1.TANWEEN_POLICY,
        candidates=[wasl_candidate, waqf_candidate],
        policies=[policy],
        evidence=[make_evidence(
            "apply_tanween_policy",
            f"Tanween {tanween_name} → wasl/waqf candidates preserved"
        )],
        rank=RANK_POLICY_DEPENDENT
    )

    # Residual: boundary context needed
    result.residuals.append(make_warning(
        ResidualType.AMBIGUOUS_SYMBOL,
        "Tanween realization depends on waqf/wasl boundary",
        location=f"position {grapheme.position}"
    ))

    return result


# ============================================================================
# 7. Ambiguous Letter Handler (ا و ي)
# ============================================================================

def classify_ambiguous_letter(
    grapheme: GraphemeCarrierU1,
    prev_grapheme: Optional[GraphemeCarrierU1]
) -> Optional[PhoneticProjectionResult]:
    """
    تصنيف الحرف الملتبس (Ambiguous Letter Classification)

    Letters ا، و، ي can be:
    1. Part of long vowel (if preceded by compatible short vowel)
    2. Consonant /w/, /y/
    3. Hamza carrier (ا)

    Returns MULTIPLE candidates, doesn't choose.
    """
    if grapheme.base not in AMBIGUOUS_LETTERS:
        return None

    candidates = []
    evidence_list = []

    # Check for long vowel candidate (already covered by detect_long_vowel_candidate)
    # Here we handle OTHER functions

    if grapheme.base == 'و':
        # Could be consonant /w/
        consonant_cand = PhoneticCandidate(
            makhraj_candidate=MakhrajCandidate(
                region="labial_approximant",
                confidence=0.5
            ),
            confidence=0.5,
            rank=RANK_AMBIGUOUS_CANDIDATE
        )
        candidates.append(consonant_cand)
        evidence_list.append(make_evidence(
            "ambiguous و",
            "Could be consonant /w/ or long vowel carrier"
        ))

    elif grapheme.base == 'ي':
        # Could be consonant /y/
        consonant_cand = PhoneticCandidate(
            makhraj_candidate=MakhrajCandidate(
                region="palatal_approximant",
                confidence=0.5
            ),
            confidence=0.5,
            rank=RANK_AMBIGUOUS_CANDIDATE
        )
        candidates.append(consonant_cand)
        evidence_list.append(make_evidence(
            "ambiguous ي",
            "Could be consonant /y/ or long vowel carrier"
        ))

    elif grapheme.base in {'ا', 'ى'}:
        # Usually long vowel carrier or hamza carrier
        vowel_cand = PhoneticCandidate(
            vowel_candidate=VowelCandidate(
                quality="a_carrier",
                length="long",
                confidence=0.6
            ),
            confidence=0.6,
            rank=RANK_AMBIGUOUS_CANDIDATE
        )
        candidates.append(vowel_cand)
        evidence_list.append(make_evidence(
            "ambiguous ا/ى",
            "Long vowel carrier or hamza support"
        ))

    if not candidates:
        return None

    result = PhoneticProjectionResult(
        grapheme=grapheme,
        success=True,
        phonetic_class=PhoneticClass1.DEFERRED,
        candidates=candidates,
        evidence=evidence_list,
        rank=RANK_AMBIGUOUS_CANDIDATE
    )

    # Residual: needs context for resolution
    result.residuals.append(make_warning(
        ResidualType.AMBIGUOUS_SYMBOL,
        f"Ambiguous letter {grapheme.base} needs context",
        location=f"position {grapheme.position}"
    ))

    return result
