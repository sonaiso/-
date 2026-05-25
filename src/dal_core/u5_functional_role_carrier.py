"""
U₅ Functional Role Carrier (حامل الأدوار الوظيفية) - Canonical Position

Domain: U₅ = FunctionalRoleCarrier (CANONICAL POSITION)
Purpose: Assign functional roles AFTER boundary detection and true lafẓ identification
Transition: U₄ (TrueSingularLafẓ) → U₅ (FunctionalRole) → U₆ (MabniClosedClass)

ARCHITECTURAL NOTE:
    This is the CORRECT position for FunctionalRoleCarrier in the execution layer sequence.

    Canonical Path:
        U₂s ArabicSyllable
        → U₃ BoundaryAndAttachment    (identify boundaries: وَ, بِـ, كِتَاب, ـهِمْ)
        → U₄ TrueSingularLafẓ           (determine standalone vs. composite)
        → U₅ FunctionalRole             (assign HARF_JARR, ROOT, PRONOUN roles) ← THIS LAYER
        → U₆ MabniClosedClass
        → U₇ PreWeightContract
        → U₈ RootStem
        → U₉ Weight

IMPLEMENTATION:
    This module currently re-exports from the legacy u3_functional_roles.py implementation
    for backward compatibility. The implementation itself is correct and complete;
    only its POSITION in the layer sequence needed correction.

MIGRATION:
    - Legacy code using u3_functional_roles.py will continue to work
    - New code should import from this module (u5_functional_role_carrier.py)
    - The execution_layer_registry.py enforces correct layer ordering

CRITICAL LAWS:
    - لا دور وظيفي قبل فصل الحدود (No functional role before boundary separation)
    - لا دور وظيفي قبل لفظ مفرد حقيقي (No functional role before true singular lafẓ)
    - الدور ≠ الجذر (Role ≠ root)
    - الدور ≠ الوزن (Role ≠ weight)
    - الدور ≠ المعنى (Role ≠ meaning)

PR: EXEC-LAYER-REFACTOR
Created: 2026-05-25
"""

# Re-export all functional role definitions from legacy implementation
# This preserves backward compatibility while establishing correct layer position

from dal_core.u3_functional_roles import (
    # Role type taxonomy
    RoleSort,
    ClosedClassRole,
    PronounRole,
    RootRole,
    DerivationalRole,
    InflectionalRole,
    VerbFeatureRole,
    RelationPossessionRole,
    BuildInflectRole,

    # Role structures
    FunctionalRole,
    RoleCandidate,
    RoleAssignment,
    RoleCandidateSet,

    # Layer objects
    FunctionalRoleLayerObject,
    FunctionalRoleResult,

    # Failure types
    RoleFailureType,

    # CPB and operations
    CPB_FunctionalRole,

    # Any other exports from u3_functional_roles
)

# Explicit __all__ to make clear what's being re-exported
__all__ = [
    # Role types
    'RoleSort',
    'ClosedClassRole',
    'PronounRole',
    'RootRole',
    'DerivationalRole',
    'InflectionalRole',
    'VerbFeatureRole',
    'RelationPossessionRole',
    'BuildInflectRole',

    # Structures
    'FunctionalRole',
    'RoleCandidate',
    'RoleAssignment',
    'RoleCandidateSet',
    'FunctionalRoleLayerObject',
    'FunctionalRoleResult',

    # Failures
    'RoleFailureType',

    # CPB
    'CPB_FunctionalRole',
]


# ============================================================================
# Architectural Guidance
# ============================================================================

def get_layer_position_note() -> str:
    """
    Return architectural note about layer position.

    Use this in documentation or error messages to clarify layer ordering.
    """
    return """
    U₅ FunctionalRoleCarrier is the CANONICAL position for functional role assignment.

    It comes AFTER:
        - U₃ BoundaryAndAttachment (boundary detection)
        - U₄ TrueSingularLafẓ (lafẓ identification)

    It comes BEFORE:
        - U₆ MabniClosedClass (closed-class certification)
        - U₇ PreWeightContract (pre-weight analysis)
        - U₈ RootStem (root/stem extraction)
        - U₉ Weight (pattern/weight assignment)

    Legacy code may reference u3_functional_roles.py, but the canonical
    position is U₅ as defined in execution_layer_registry.py.
    """


# ============================================================================
# Layer Ordering Validation
# ============================================================================

def validate_preconditions(input_layer_name: str) -> tuple[bool, str]:
    """
    Validate that functional role assignment has required preconditions.

    Args:
        input_layer_name: Name of input layer (should be U₄)

    Returns:
        (is_valid, error_message) tuple
    """
    if input_layer_name not in {"U4_TRUE_SINGULAR_LAFZ", "u4", "TrueSingularLafz"}:
        return False, (
            f"FunctionalRole (U₅) requires U₄ TrueSingularLafẓ as input. "
            f"Got: {input_layer_name}. "
            f"Forbidden jump: Cannot go directly from U₂s Syllable to U₅ FunctionalRole. "
            f"Required path: U₂s → U₃ Boundary → U₄ TrueLafẓ → U₅ FunctionalRole"
        )

    return True, ""


def validate_next_layer(next_layer_name: str) -> tuple[bool, str]:
    """
    Validate that next layer after functional role is correct.

    Args:
        next_layer_name: Name of next layer (should be U₆)

    Returns:
        (is_valid, error_message) tuple
    """
    allowed_next = {"U6_MABNI_CLOSED_CLASS", "u6", "MabniClosedClass"}

    if next_layer_name not in allowed_next:
        return False, (
            f"FunctionalRole (U₅) should transition to U₆ MabniClosedClass. "
            f"Got: {next_layer_name}. "
            f"Forbidden: Cannot jump from U₅ directly to root/weight/meaning."
        )

    return True, ""
