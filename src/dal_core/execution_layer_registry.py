"""
Execution Layer Registry - Canonical U₀-U₉ Order (سجل الطبقات التنفيذية)

Purpose: Define official execution layer sequence and prevent architectural layer jumps

Critical Law: لا قفز بين الطبقات بلا دليل (No layer jump without evidence)

Execution Core (U₀-U₉): Closed, implemented, operational layers
    U₀ Unicode          → U₁ Grapheme
    U₁ Grapheme         → U₂p PhoneticProjection
    U₂p PhoneticProjection → U₂s ArabicSyllable
    U₂s ArabicSyllable  → U₃ BoundaryAndAttachment
    U₃ BoundaryAndAttachment → U₄ TrueSingularLafẓ
    U₄ TrueSingularLafẓ → U₅ FunctionalRole
    U₅ FunctionalRole   → U₆ MabniClosedClass
    U₆ MabniClosedClass → U₇ PreWeightContract
    U₇ PreWeightContract → U₈ RootStem
    U₈ RootStem         → U₉ Weight

Design Layers (U₁₀-U₁₅): Future design, not closed execution layers
    U₁₀ WordForm
    U₁₁ LexicalEntry
    U₁₂ MorphosyntacticFeature
    U₁₃ PhraseRelation
    U₁₄ SentenceStructure
    U₁₅ Dalālah

Forbidden Jumps:
    U₂s → FunctionalRole   (Missing Boundary + TrueLafẓ)
    U₂s → Root             (Missing 6 intermediate layers)
    U₂s → Weight           (Missing 7 intermediate layers)
    U₂s → Meaning          (Missing 10+ intermediate layers)
    Syllable → Hukm        (Missing all layers)

Architectural Note:
    Legacy U₃ FunctionalRoleCarrier existed before BoundaryAndAttachment was recognized
    as necessary intermediate layer. It is now U₅ in canonical ordering.

PR: EXEC-LAYER-REFACTOR
Created: 2026-05-25
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import FrozenSet, Optional, Set


class ExecutionLayer(Enum):
    """
    Canonical execution layer enumeration.

    Each layer represents one step in the evidence-based transition from
    raw Unicode to certified linguistic judgments.
    """
    U0_UNICODE = "u0_unicode"
    U1_GRAPHEME = "u1_grapheme"
    U2P_PHONETIC_PROJECTION = "u2p_phonetic_projection"
    U2S_ARABIC_SYLLABLE = "u2s_arabic_syllable"
    U3_BOUNDARY_ATTACHMENT = "u3_boundary_attachment"
    U4_TRUE_SINGULAR_LAFZ = "u4_true_singular_lafz"
    U5_FUNCTIONAL_ROLE = "u5_functional_role"
    U6_MABNI_CLOSED_CLASS = "u6_mabni_closed_class"
    U7_PRE_WEIGHT_CONTRACT = "u7_pre_weight_contract"
    U8_ROOT_STEM = "u8_root_stem"
    U9_WEIGHT = "u9_weight"

    # Higher layers (design phase)
    U10_WORD_FORM = "u10_word_form"
    U11_LEXICAL_ENTRY = "u11_lexical_entry"
    U12_MORPHOSYNTACTIC_FEATURE = "u12_morphosyntactic_feature"
    U13_PHRASE_RELATION = "u13_phrase_relation"
    U14_SENTENCE_STRUCTURE = "u14_sentence_structure"
    U15_DALALAH = "u15_dalalah"


@dataclass(frozen=True)
class LayerTransition:
    """
    Represents an allowed transition between execution layers.

    Attributes:
        from_layer: Source layer
        to_layer: Target layer
        requires_evidence: Whether evidence is required for this transition
        forbidden_without: Layers that must be passed through (cannot skip)
    """
    from_layer: ExecutionLayer
    to_layer: ExecutionLayer
    requires_evidence: bool = True
    forbidden_without: FrozenSet[ExecutionLayer] = frozenset()


# ============================================================================
# Canonical Execution Layer Order
# ============================================================================

# Execution Core Layers (U₀-U₉): Closed, implemented, operational
EXECUTION_CORE_LAYERS = [
    ExecutionLayer.U0_UNICODE,
    ExecutionLayer.U1_GRAPHEME,
    ExecutionLayer.U2P_PHONETIC_PROJECTION,
    ExecutionLayer.U2S_ARABIC_SYLLABLE,
    ExecutionLayer.U3_BOUNDARY_ATTACHMENT,
    ExecutionLayer.U4_TRUE_SINGULAR_LAFZ,
    ExecutionLayer.U5_FUNCTIONAL_ROLE,
    ExecutionLayer.U6_MABNI_CLOSED_CLASS,
    ExecutionLayer.U7_PRE_WEIGHT_CONTRACT,
    ExecutionLayer.U8_ROOT_STEM,
    ExecutionLayer.U9_WEIGHT,
]

# Design Layers (U₁₀-U₁₅): Future design, not closed execution layers
DESIGN_LAYERS = [
    ExecutionLayer.U10_WORD_FORM,
    ExecutionLayer.U11_LEXICAL_ENTRY,
    ExecutionLayer.U12_MORPHOSYNTACTIC_FEATURE,
    ExecutionLayer.U13_PHRASE_RELATION,
    ExecutionLayer.U14_SENTENCE_STRUCTURE,
    ExecutionLayer.U15_DALALAH,
]

# Complete layer order (for reference and tooling)
EXECUTION_LAYER_ORDER = EXECUTION_CORE_LAYERS + DESIGN_LAYERS


# ============================================================================
# Allowed Transitions (Canonical Path)
# ============================================================================

# Core execution layer transitions (U₀-U₉) - Operational
CORE_ALLOWED_TRANSITIONS = {
    # Foundation layers (U₀-U₂s)
    ExecutionLayer.U0_UNICODE: {ExecutionLayer.U1_GRAPHEME},
    ExecutionLayer.U1_GRAPHEME: {ExecutionLayer.U2P_PHONETIC_PROJECTION},
    ExecutionLayer.U2P_PHONETIC_PROJECTION: {ExecutionLayer.U2S_ARABIC_SYLLABLE},

    # Critical: U₂s MUST go to Boundary, NOT FunctionalRole
    ExecutionLayer.U2S_ARABIC_SYLLABLE: {ExecutionLayer.U3_BOUNDARY_ATTACHMENT},

    # Boundary → TrueLafẓ → FunctionalRole
    ExecutionLayer.U3_BOUNDARY_ATTACHMENT: {ExecutionLayer.U4_TRUE_SINGULAR_LAFZ},
    ExecutionLayer.U4_TRUE_SINGULAR_LAFZ: {ExecutionLayer.U5_FUNCTIONAL_ROLE},

    # Morphological layers
    ExecutionLayer.U5_FUNCTIONAL_ROLE: {ExecutionLayer.U6_MABNI_CLOSED_CLASS},
    ExecutionLayer.U6_MABNI_CLOSED_CLASS: {ExecutionLayer.U7_PRE_WEIGHT_CONTRACT},
    ExecutionLayer.U7_PRE_WEIGHT_CONTRACT: {ExecutionLayer.U8_ROOT_STEM},
    ExecutionLayer.U8_ROOT_STEM: {ExecutionLayer.U9_WEIGHT},
}

# NOTE: U₈ ROOT_STEM is now IMPLEMENTED and registered.
# U₈ is closed over real U₇ pre-weight contract output.

# Design layer transitions (U₁₀-U₁₅) - Future design, not closed execution
DESIGN_ALLOWED_TRANSITIONS = {
    # Transition from core to design layers
    ExecutionLayer.U9_WEIGHT: {ExecutionLayer.U10_WORD_FORM},

    # Design layer internal transitions (not yet closed)
    ExecutionLayer.U10_WORD_FORM: {ExecutionLayer.U11_LEXICAL_ENTRY},
    ExecutionLayer.U11_LEXICAL_ENTRY: {ExecutionLayer.U12_MORPHOSYNTACTIC_FEATURE},
    ExecutionLayer.U12_MORPHOSYNTACTIC_FEATURE: {ExecutionLayer.U13_PHRASE_RELATION},
    ExecutionLayer.U13_PHRASE_RELATION: {ExecutionLayer.U14_SENTENCE_STRUCTURE},
    ExecutionLayer.U14_SENTENCE_STRUCTURE: {ExecutionLayer.U15_DALALAH},
}

# Combined transitions (for compatibility and tooling)
ALLOWED_TRANSITIONS = {**CORE_ALLOWED_TRANSITIONS, **DESIGN_ALLOWED_TRANSITIONS}


# ============================================================================
# Forbidden Jumps (Architectural Violations)
# ============================================================================

FORBIDDEN_JUMPS = {
    # U₂s forbidden jumps (most critical)
    (ExecutionLayer.U2S_ARABIC_SYLLABLE, ExecutionLayer.U5_FUNCTIONAL_ROLE):
        "Missing U₃ BoundaryAndAttachment and U₄ TrueSingularLafẓ",

    (ExecutionLayer.U2S_ARABIC_SYLLABLE, ExecutionLayer.U8_ROOT_STEM):
        "Missing 6 intermediate layers (U₃-U₇)",

    (ExecutionLayer.U2S_ARABIC_SYLLABLE, ExecutionLayer.U9_WEIGHT):
        "Missing 7 intermediate layers (U₃-U₈)",

    # Other forbidden jumps
    (ExecutionLayer.U3_BOUNDARY_ATTACHMENT, ExecutionLayer.U5_FUNCTIONAL_ROLE):
        "Missing U₄ TrueSingularLafẓ",

    (ExecutionLayer.U5_FUNCTIONAL_ROLE, ExecutionLayer.U8_ROOT_STEM):
        "Missing U₆ MabniClosedClass and U₇ PreWeightContract",
}


# ============================================================================
# Layer Validation Functions
# ============================================================================

def is_core_transition_allowed(from_layer: ExecutionLayer, to_layer: ExecutionLayer) -> bool:
    """
    Check if a transition between execution core layers is allowed.

    Args:
        from_layer: Source layer
        to_layer: Target layer

    Returns:
        True if transition is in CORE_ALLOWED_TRANSITIONS, False otherwise
    """
    allowed = CORE_ALLOWED_TRANSITIONS.get(from_layer, set())
    return to_layer in allowed


def is_design_transition_allowed(from_layer: ExecutionLayer, to_layer: ExecutionLayer) -> bool:
    """
    Check if a transition between design layers is allowed.

    Args:
        from_layer: Source layer
        to_layer: Target layer

    Returns:
        True if transition is in DESIGN_ALLOWED_TRANSITIONS, False otherwise
    """
    allowed = DESIGN_ALLOWED_TRANSITIONS.get(from_layer, set())
    return to_layer in allowed


def is_transition_allowed(from_layer: ExecutionLayer, to_layer: ExecutionLayer, include_design: bool = False) -> bool:
    """
    Check if a transition between layers is allowed.

    By default, only execution core transitions (U₀-U₉) are allowed.
    Design layer transitions (U₁₀-U₁₅) require explicit opt-in.

    Args:
        from_layer: Source layer
        to_layer: Target layer
        include_design: If True, allow design layer transitions. Default False.

    Returns:
        True if transition is allowed, False otherwise

    Core Law:
        Design transition is not execution transition.
        U₉ → U₁₀ is NOT allowed by default.
    """
    if include_design:
        allowed = ALLOWED_TRANSITIONS.get(from_layer, set())
    else:
        allowed = CORE_ALLOWED_TRANSITIONS.get(from_layer, set())
    return to_layer in allowed


def get_forbidden_jump_reason(from_layer: ExecutionLayer, to_layer: ExecutionLayer) -> Optional[str]:
    """
    Get reason why a layer jump is forbidden.

    Args:
        from_layer: Source layer
        to_layer: Target layer

    Returns:
        Reason string if jump is forbidden, None if allowed
    """
    return FORBIDDEN_JUMPS.get((from_layer, to_layer))


def get_required_intermediate_layers(from_layer: ExecutionLayer, to_layer: ExecutionLayer) -> FrozenSet[ExecutionLayer]:
    """
    Get layers that must be traversed between from_layer and to_layer.

    Args:
        from_layer: Source layer
        to_layer: Target layer

    Returns:
        Frozen set of required intermediate layers
    """
    from_idx = EXECUTION_LAYER_ORDER.index(from_layer)
    to_idx = EXECUTION_LAYER_ORDER.index(to_layer)

    if to_idx <= from_idx:
        return frozenset()

    # All layers between from and to (exclusive)
    intermediate = EXECUTION_LAYER_ORDER[from_idx + 1:to_idx]
    return frozenset(intermediate)


def validate_layer_sequence(sequence: list[ExecutionLayer], include_design: bool = False) -> tuple[bool, Optional[str]]:
    """
    Validate that a sequence of layers follows canonical ordering.

    By default, only validates execution core transitions (U₀-U₉).
    Design layer transitions require explicit opt-in.

    Args:
        sequence: List of execution layers
        include_design: If True, allow design layer transitions. Default False.

    Returns:
        (is_valid, error_message) tuple

    Core Law:
        Design transition is not execution transition.
        Sequences ending beyond U₉ must explicitly set include_design=True.
    """
    if not sequence:
        return True, None

    for i in range(len(sequence) - 1):
        from_layer = sequence[i]
        to_layer = sequence[i + 1]

        if not is_transition_allowed(from_layer, to_layer, include_design=include_design):
            # Check if it's a known forbidden jump
            reason = get_forbidden_jump_reason(from_layer, to_layer)
            if reason:
                return False, f"Forbidden jump: {from_layer.value} → {to_layer.value}. Reason: {reason}"
            else:
                # Check if it's a design transition without opt-in
                if not include_design and is_design_transition_allowed(from_layer, to_layer):
                    return False, f"Design transition: {from_layer.value} → {to_layer.value}. Design layers (U₁₀-U₁₅) are not closed execution layers. Use include_design=True if intentional."
                return False, f"Invalid transition: {from_layer.value} → {to_layer.value}"

    return True, None


def is_core_layer(layer: ExecutionLayer) -> bool:
    """
    Check if a layer is part of the execution core (U₀-U₉).

    Args:
        layer: Layer to check

    Returns:
        True if layer is in EXECUTION_CORE_LAYERS, False otherwise
    """
    return layer in EXECUTION_CORE_LAYERS


def is_design_layer(layer: ExecutionLayer) -> bool:
    """
    Check if a layer is part of the design layers (U₁₀-U₁₅).

    Args:
        layer: Layer to check

    Returns:
        True if layer is in DESIGN_LAYERS, False otherwise
    """
    return layer in DESIGN_LAYERS


# ============================================================================
# Legacy Compatibility Mapping
# ============================================================================

LEGACY_LAYER_MAPPING = {
    # Old position → New position
    "legacy_u3_functional_role": ExecutionLayer.U5_FUNCTIONAL_ROLE,
    "legacy_u4_morpheme": ExecutionLayer.U6_MABNI_CLOSED_CLASS,
    "legacy_u5_stemroot": ExecutionLayer.U8_ROOT_STEM,
    "legacy_u6_pattern": ExecutionLayer.U9_WEIGHT,
}


def get_canonical_layer(legacy_name: str) -> Optional[ExecutionLayer]:
    """
    Map legacy layer name to canonical execution layer.

    Args:
        legacy_name: Legacy layer identifier

    Returns:
        Canonical ExecutionLayer or None if not found
    """
    return LEGACY_LAYER_MAPPING.get(legacy_name)
