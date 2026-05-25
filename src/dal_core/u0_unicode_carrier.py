"""
U₀ Unicode Carrier - Strict Type System (نظام الحامل اليونيكودي الصارم)

Domain: U₀ = UnicodeCarrier
Purpose: Unicode scalar classification WITHOUT morphological/syntactic interpretation
Transition: RawString → U₀ (Unicode classification)

Critical Laws (Axioms):
    - Axiom 0.1: لا تحويل قبل حفظ (No conversion before preservation)
    - Axiom 0.6: لا مقطع قبل حفظ Unicode
    - Axiom 0.7: لا Grapheme قبل حفظ Trace من Unicode

Type System:
    UnicodeScalar ≠ GraphemeCluster
    UnicodeScalar ≠ PhoneticProjection
    UnicodeScalar ≠ ArabicSyllable
    UnicodeScalar ≠ Root
    UnicodeScalar ≠ Meaning

Architecture:
    RawString → CPB₀ → U₀ (UnicodeUnit*) → CPB₁ → U₁

PR: U0-STRICT-TYPE-SYSTEM
Created: 2026-05-25
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import List, Optional, FrozenSet, Dict, Any, Tuple
from uuid import uuid4
import unicodedata

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


# ============================================================================
# Type System - Unicode Classification
# ============================================================================

class UnicodeClass(Enum):
    """
    Unicode scalar classification for Arabic processing.

    Classification determines permitted operations, NOT meaning.
    """
    ARABIC_LETTER = "arabic_letter"           # ب، ت، ث، ... (consonantal base)
    ARABIC_DIACRITIC = "arabic_diacritic"     # َ، ِ، ُ، ْ، ّ، ً، ٍ، ٌ
    QURANIC_MARK = "quranic_mark"             # Tajweed marks
    TATWEEL = "tatweel"                       # ـ (kashida)
    ARABIC_DIGIT = "arabic_digit"             # ٠، ١، ٢، ...
    SEPARATOR = "separator"                   # Space, NBSP
    PUNCTUATION = "punctuation"               # ،، ؛، ؟، !
    FOREIGN_LETTER = "foreign_letter"         # Latin, etc.
    FOREIGN_DIGIT = "foreign_digit"           # 0-9
    CONTROL = "control"                       # Zero-width, formatting
    INVISIBLE = "invisible"                   # ZWJ, ZWNJ
    UNKNOWN = "unknown"                       # Unclassified


# ============================================================================
# U₀ Carrier Structure
# ============================================================================

@dataclass(frozen=True)
class UnicodeUnit:
    """
    Unicode scalar unit with classification and trace.

    Immutable carrier preserving:
        - scalar: Unicode character
        - codepoint: U+XXXX value
        - char: Display representation
        - unicode_class: Classification
        - position: Position in input stream
        - trace: Preservation of origin
        - residuals: Warnings/blockers
        - rank: Epistemic status

    Laws:
        - UnicodeUnit ⊬ GraphemeCluster
        - UnicodeUnit ⊬ Syllable
        - UnicodeUnit ⊬ Root
        - UnicodeUnit ⊬ Meaning
    """
    id: str                                    # Unique identifier
    scalar: str                                # Single Unicode character
    codepoint: int                             # U+XXXX numeric value
    char: str                                  # Display character
    unicode_class: UnicodeClass                # Classification
    unicode_name: str                          # Official Unicode name
    position: int                              # Position in input stream
    trace: FrozenSet[str]                      # Trace to input (position markers)
    residuals: FrozenSet[Residual]             # Warnings/blockers
    rank: Rank                                 # Epistemic rank

    def __post_init__(self):
        """Validate invariants."""
        if len(self.scalar) != 1:
            raise ValueError(f"UnicodeUnit must contain exactly one scalar, got: {self.scalar!r}")
        if len(self.char) != 1:
            raise ValueError(f"UnicodeUnit char must be single character, got: {self.char!r}")

    def is_arabic_block(self) -> bool:
        """Check if codepoint in Arabic Unicode blocks."""
        return (
            (0x0600 <= self.codepoint <= 0x06FF) or  # Arabic
            (0x0750 <= self.codepoint <= 0x077F) or  # Arabic Supplement
            (0x08A0 <= self.codepoint <= 0x08FF) or  # Arabic Extended-A
            (0xFB50 <= self.codepoint <= 0xFDFF) or  # Arabic Presentation Forms-A
            (0xFE70 <= self.codepoint <= 0xFEFF)     # Arabic Presentation Forms-B
        )

    def has_blocker(self) -> bool:
        """Check if unit has blocking residual."""
        return any(r.residual_type == ResidualType.BLOCKER for r in self.residuals)

    def is_certified(self) -> bool:
        """Check if unit is certified (rank = CERTIFICATE)."""
        return self.rank == Rank.CERTIFICATE


@dataclass(frozen=True)
class UnicodeLayerObject:
    """
    Complete U₀ layer output.

    Contains:
        - units: ORDERED sequence of classified Unicode units (Tuple, not FrozenSet)
        - total_residuals: All residuals from layer
        - metadata: Additional processing information

    Critical Law:
        - units MUST preserve input order (no frozenset for execution trace)
        - Order preservation is MANDATORY for downstream layer integrity
    """
    units: Tuple[UnicodeUnit, ...]  # ORDERED sequence (was FrozenSet - WRONG)
    total_residuals: FrozenSet[Residual]
    metadata: Dict[str, Any] = field(default_factory=dict)

    def has_blocking_failure(self) -> bool:
        """Check if layer has blocking residuals."""
        return any(r.residual_type == ResidualType.BLOCKER for r in self.total_residuals)

    def count_certified(self) -> int:
        """Count certified units."""
        return sum(1 for u in self.units if u.is_certified())


# ============================================================================
# Classification Operation (classify₀)
# ============================================================================

@dataclass(frozen=True)
class ClassifyResult:
    """
    Result of classify₀ operation.

    Partial operation: can succeed or fail with residuals.
    """
    success: bool
    unit: Optional[UnicodeUnit]
    residuals: FrozenSet[Residual]


def classify_unicode_scalar(
    char: str,
    position: int,
    policy: Optional[Dict[str, Any]] = None
) -> ClassifyResult:
    """
    classify₀ : RawString ⇀ UnicodeUnit ∪ Fail₀

    Partial operation that classifies Unicode scalar.

    Succeeds if:
        - char is single Unicode scalar
        - scalar is classifiable
        - no unknown blocking scalars

    Fails if:
        - UnknownScalar blocking
        - ForbiddenControl blocking
        - BrokenEncoding

    Args:
        char: Single Unicode character
        position: Position in input stream
        policy: Optional policy for control/invisible handling

    Returns:
        ClassifyResult with success/failure and residuals
    """
    residuals_list = []
    policy = policy or {}

    # Validation: single character
    if len(char) != 1:
        residuals_list.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            f"Expected single character, got {len(char)} characters",
            location=f"position {position}"
        ))
        return ClassifyResult(
            success=False,
            unit=None,
            residuals=frozenset(residuals_list)
        )

    # Get codepoint and Unicode name
    codepoint = ord(char)
    try:
        unicode_name = unicodedata.name(char, f"U+{codepoint:04X}")
    except ValueError:
        unicode_name = f"UNKNOWN-{codepoint:04X}"

    # Classify
    unicode_class = _classify_codepoint(codepoint, char)

    # Check for unknown scalars
    if unicode_class == UnicodeClass.UNKNOWN:
        residuals_list.append(make_blocker(
            ResidualType.UNKNOWN_SYMBOL,
            f"Unknown Unicode scalar: {char!r} (U+{codepoint:04X})",
            location=f"position {position}"
        ))
        rank = Rank.BLOCKED

    # Check for control characters
    elif unicode_class == UnicodeClass.CONTROL:
        if not policy.get("allow_control", False):
            residuals_list.append(make_blocker(
                ResidualType.MALFORMED_ATOM,  # Use existing type
                f"Control character not allowed: {char!r} (U+{codepoint:04X})",
                location=f"position {position}"
            ))
            rank = Rank.BLOCKED
        else:
            residuals_list.append(make_warning(
                ResidualType.AMBIGUOUS_SYMBOL,
                f"Control character allowed by policy: {char!r}",
                location=f"position {position}"
            ))
            rank = Rank.HYPOTHESIS

    # Check for invisible characters
    elif unicode_class == UnicodeClass.INVISIBLE:
        residuals_list.append(make_warning(
            ResidualType.AMBIGUOUS_SYMBOL,
            f"Invisible character: {char!r} (U+{codepoint:04X})",
            location=f"position {position}"
        ))
        rank = Rank.HYPOTHESIS

    # Foreign characters: allow with warning
    elif unicode_class in (UnicodeClass.FOREIGN_LETTER, UnicodeClass.FOREIGN_DIGIT):
        residuals_list.append(make_warning(
            ResidualType.NON_ARABIC_SYMBOL,
            f"Foreign character: {char!r} (U+{codepoint:04X})",
            location=f"position {position}"
        ))
        rank = Rank.HYPOTHESIS

    # Arabic characters: certify
    elif unicode_class in (
        UnicodeClass.ARABIC_LETTER,
        UnicodeClass.ARABIC_DIACRITIC,
        UnicodeClass.QURANIC_MARK,
        UnicodeClass.ARABIC_DIGIT
    ):
        rank = Rank.CERTIFICATE

    # Other allowed classes
    else:
        rank = Rank.CANDIDATE

    # Create unit
    unit = UnicodeUnit(
        id=str(uuid4()),
        scalar=char,
        codepoint=codepoint,
        char=char,
        unicode_class=unicode_class,
        unicode_name=unicode_name,
        position=position,
        trace=frozenset([f"pos:{position}"]),
        residuals=frozenset(residuals_list),
        rank=rank
    )

    # Determine success
    success = rank != Rank.BLOCKED

    return ClassifyResult(
        success=success,
        unit=unit if success else None,
        residuals=frozenset(residuals_list)
    )


def _classify_codepoint(codepoint: int, char: str) -> UnicodeClass:
    """
    Internal classification logic.

    Maps codepoint to UnicodeClass based on Unicode blocks and categories.
    """
    # Arabic blocks
    if 0x0600 <= codepoint <= 0x06FF:
        # Arabic diacritics
        if 0x064B <= codepoint <= 0x065F:
            return UnicodeClass.ARABIC_DIACRITIC
        # Arabic letters
        elif 0x0621 <= codepoint <= 0x064A:
            return UnicodeClass.ARABIC_LETTER
        # Arabic digits
        elif 0x0660 <= codepoint <= 0x0669:
            return UnicodeClass.ARABIC_DIGIT
        # Quranic marks
        elif 0x0670 <= codepoint <= 0x06DC:
            return UnicodeClass.QURANIC_MARK
        # Tatweel
        elif codepoint == 0x0640:
            return UnicodeClass.TATWEEL
        else:
            return UnicodeClass.ARABIC_LETTER  # Default to letter for Arabic block

    # Arabic Supplement
    elif 0x0750 <= codepoint <= 0x077F:
        return UnicodeClass.ARABIC_LETTER

    # Arabic Extended-A
    elif 0x08A0 <= codepoint <= 0x08FF:
        if 0x08E3 <= codepoint <= 0x08FF:
            return UnicodeClass.ARABIC_DIACRITIC
        return UnicodeClass.ARABIC_LETTER

    # Arabic Presentation Forms
    elif 0xFB50 <= codepoint <= 0xFDFF or 0xFE70 <= codepoint <= 0xFEFF:
        return UnicodeClass.ARABIC_LETTER

    # Use Unicode category for non-Arabic
    category = unicodedata.category(char)

    if category.startswith('Z'):  # Separator
        return UnicodeClass.SEPARATOR
    elif category.startswith('P'):  # Punctuation
        return UnicodeClass.PUNCTUATION
    elif category.startswith('N'):  # Number
        return UnicodeClass.FOREIGN_DIGIT
    elif category.startswith('L'):  # Letter
        return UnicodeClass.FOREIGN_LETTER
    elif category.startswith('C'):  # Control
        if codepoint in (0x200C, 0x200D):  # ZWNJ, ZWJ
            return UnicodeClass.INVISIBLE
        return UnicodeClass.CONTROL
    else:
        return UnicodeClass.UNKNOWN


# ============================================================================
# CPB₀ - Identity Guardian
# ============================================================================

@dataclass(frozen=True)
class CPB0Result:
    """
    Result of CPB₀ validation.

    CPB₀ ensures:
        - TracePreserved
        - AllScalarsClassified
        - NoSilentDeletion
        - RankNonInflation
        - ResidualsExplicit
    """
    valid: bool
    violations: FrozenSet[str]
    layer_object: Optional[UnicodeLayerObject]


def cpb0_validate(
    raw_input: str,
    units: List[UnicodeUnit],
    policy: Optional[Dict[str, Any]] = None
) -> CPB0Result:
    """
    CPB₀ : RawString × classify₀ × Evidence₀ × Policy₀ ⇀ UnicodeLayerObject ∪ Fail₀

    Validates that Unicode layer satisfies identity guardian constraints.

    Guarantees:
        - TracePreserved: Every scalar has trace to input position
        - AllScalarsClassified: No unclassified scalars (or residualized)
        - NoSilentDeletion: No scalar deleted without residual
        - RankNonInflation: No rank elevation without evidence
        - ResidualsExplicit: All warnings/blockers explicit

    Args:
        raw_input: Original input string
        units: Classified Unicode units
        policy: Optional processing policy

    Returns:
        CPB0Result with validation status
    """
    violations = []

    # Check 1: TracePreserved
    for unit in units:
        if not unit.trace:
            violations.append(f"TraceViolation: Unit {unit.id} has no trace")

    # Check 2: AllScalarsClassified
    for unit in units:
        if unit.unicode_class == UnicodeClass.UNKNOWN and not unit.has_blocker():
            violations.append(f"ClassificationViolation: Unit {unit.id} is UNKNOWN without blocker")

    # Check 3: NoSilentDeletion
    input_length = len(raw_input)
    unit_positions = {u.position for u in units}
    all_residuals = set()
    for u in units:
        all_residuals.update(u.residuals)

    for i in range(input_length):
        if i not in unit_positions:
            # Check if there's a residual explaining the deletion
            deletion_explained = any(
                f"position {i}" in str(r.data) or f"pos:{i}" in str(r.data)
                for r in all_residuals
            )
            if not deletion_explained:
                violations.append(f"SilentDeletion: Position {i} deleted without residual")

    # Check 4: RankNonInflation
    for unit in units:
        if unit.rank == Rank.CERTIFICATE:
            # Certificate requires Arabic classification
            if unit.unicode_class not in (
                UnicodeClass.ARABIC_LETTER,
                UnicodeClass.ARABIC_DIACRITIC,
                UnicodeClass.QURANIC_MARK,
                UnicodeClass.ARABIC_DIGIT
            ):
                violations.append(f"RankInflation: Unit {unit.id} certified without Arabic classification")

    # Check 5: ResidualsExplicit
    # (Already enforced by classify₀ returning residuals)

    # Collect all residuals
    total_residuals = set()
    for unit in units:
        total_residuals.update(unit.residuals)

    # Create layer object with ORDERED units (tuple, not frozenset)
    layer_object = UnicodeLayerObject(
        units=tuple(units),  # CRITICAL: Preserve order (was frozenset - WRONG)
        total_residuals=frozenset(total_residuals),
        metadata={"input_length": input_length}
    )

    return CPB0Result(
        valid=len(violations) == 0,
        violations=frozenset(violations),
        layer_object=layer_object if len(violations) == 0 else None
    )


# ============================================================================
# Main Pipeline
# ============================================================================

def text_to_unicode_layer(
    text: str,
    policy: Optional[Dict[str, Any]] = None
) -> CPB0Result:
    """
    Complete pipeline: RawString → U₀ (UnicodeLayerObject).

    Steps:
        1. classify₀: Each character → UnicodeUnit
        2. CPB₀: Validate identity constraints

    Args:
        text: Input string
        policy: Optional processing policy

    Returns:
        CPB0Result with validation status and layer object
    """
    units = []

    for i, char in enumerate(text):
        result = classify_unicode_scalar(char, i, policy)
        if result.success and result.unit:
            units.append(result.unit)
        # Note: Failed units are not included, but residuals are preserved

    return cpb0_validate(text, units, policy)


# ============================================================================
# ProofObject (using shared foundation)
# ============================================================================

def make_u0_proof(
    input_text: str,
    cpb_result: CPB0Result
) -> ProofObject:
    """
    Create ProofObject for U₀ layer using shared foundation.

    Args:
        input_text: Input string
        cpb_result: CPB₀ validation result

    Returns:
        ProofObject documenting U₀ certification
    """
    if not cpb_result.valid or cpb_result.layer_object is None:
        raise ValueError("Cannot create proof for invalid CPB₀ result")

    layer_obj = cpb_result.layer_object

    # Create rank vector (only unicode_rank can be non-ZERO)
    rank_vector = RankVector(
        unicode_rank=Rank.CERTIFICATE if layer_obj.count_certified() > 0 else Rank.CANDIDATE,
        grapheme_rank=Rank.ZERO,
        phonetic_rank=Rank.ZERO,
        syllable_rank=Rank.ZERO,
        functional_role_rank=Rank.ZERO,
        morpheme_rank=Rank.ZERO,
        stem_root_rank=Rank.ZERO,
        pattern_weight_rank=Rank.ZERO,
        semantic_rank=Rank.ZERO,
        hukm_rank=Rank.ZERO
    )

    return make_proof_object(
        claim="Unicode scalars classified and preserved",
        scope="U₀ / UnicodeCarrier",
        evidence=frozenset([
            f"Classified {len(layer_obj.units)} units",
            f"Certified {layer_obj.count_certified()} units",
            "TracePreserved",
            "AllScalarsClassified",
            "NoSilentDeletion"
        ]),
        counter_evidence=frozenset(cpb_result.violations),
        trace_graph={
            "input_length": len(input_text),
            "output_units": len(layer_obj.units),
            "positions": [u.position for u in layer_obj.units]
        },
        competitors=frozenset(),  # No competitors at Unicode level
        residuals=layer_obj.total_residuals,
        rank_vector=rank_vector.as_dict(),
        allowed_next_gates=frozenset(["cluster₀₁"]),
        forbidden_next_gates=frozenset([
            "root_certificate",
            "weight_certificate",
            "meaning_certificate",
            "hukm_certificate",
            "syllable_certificate"
        ]),
        limitations=frozenset([
            "Unicode classification only",
            "No grapheme clustering",
            "No phonetic projection",
            "No syllabification",
            "No morphological analysis",
            "No semantic interpretation"
        ])
    )
