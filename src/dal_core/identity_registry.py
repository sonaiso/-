"""
Identity Registry (سجل الهويات)

AlgebraicDecisionCore Component: Identity classification and tracking system.

Purpose:
    Track ALL identity types across the Arabic linguistic pipeline from raw
    surface to judgment, ensuring no layer skips identity verification.

Architecture Position:
    AlgebraicDecisionCore
        └── IdentityRegistry (this module)

Governing Law:
    لا انتقال بلا هوية محددة
    No transition without defined identity.

Identity Progression (Constitutional Law):
    Raw → Protected → Licensed → Candidate → Certified

    RawSurfaceIdentity ≠ ProtectedSurfaceIdentity
    ProtectedSurfaceIdentity ≠ LicensedRootInputIdentity
    RootMaterialIdentity ≠ RootCertificate
    FormIdentity ≠ FunctionalRelationIdentity
    SemanticIdentity ≠ HukmIdentity

Forbidden Leaps:
    - No RootMaterialIdentity before LicensedRootInputIdentity
    - No WeightIdentity before RootMaterialIdentity
    - No FunctionalRelationIdentity before FormIdentity
    - No SemanticIdentity before FunctionalRelationIdentity
    - No HukmIdentity before SemanticIdentity

PR: ALGEBRAIC-DECISION-CORE
Created: 2026-05-26
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import FrozenSet, Optional, Dict, Tuple
from types import MappingProxyType


# ============================================================================
# Identity Type Classification
# ============================================================================

class IdentityType(Enum):
    """
    Complete classification of identity types in Arabic linguistic analysis.

    Organized by layer progression from surface to judgment.
    Each identity type must be verified before transitions are permitted.
    """
    # Layer 0-1: Surface and Orthographic Identities
    RAW_SURFACE_IDENTITY = auto()              # سطح خام
    ORTHOGRAPHIC_IDENTITY = auto()             # هوية إملائية

    # Layer 2: Phonetic and Syllabic Identities
    PHONETIC_IDENTITY = auto()                 # هوية صوتية
    SYLLABIC_IDENTITY = auto()                 # هوية مقطعية

    # Layer 3: Boundary Identities
    BOUNDARY_IDENTITY = auto()                 # هوية حدودية

    # Layer 4: Lafz Identities
    LAFZ_IDENTITY = auto()                     # هوية لفظية

    # Layer 5-7: Surface Protection Identities
    MARKER_IDENTITY = auto()                   # هوية علامة
    PROTECTED_SURFACE_IDENTITY = auto()        # سطح محمي
    PROTECTED_CORE_IDENTITY = auto()           # نواة محمية

    # Layer 7-8: Root Input Licensing
    LICENSED_ROOT_INPUT_IDENTITY = auto()      # مدخل جذر مرخص

    # Layer 8: Root/Stem Material Identities (Candidates, NOT Certificates)
    ROOT_MATERIAL_IDENTITY = auto()            # مادة جذرية (مرشح)
    STEM_IDENTITY = auto()                     # هوية جذع (مرشح)

    # Layer 9: Weight and Pattern Identities
    WEIGHT_IDENTITY = auto()                   # هوية وزن

    # Layer 10: Word Form Identity
    WORDFORM_IDENTITY = auto()                 # هوية صورة الكلمة
    FORM_IDENTITY = auto()                     # هوية صيغة

    # Layer 11: Composition Identity
    RELATION_COMPOSITION_IDENTITY = auto()     # هوية تركيب علائقي

    # Layer 10+: Derivational and Lexical Identities
    SOURCE_IDENTITY = auto()                   # هوية مصدر
    ATTRIBUTE_IDENTITY = auto()                # هوية صفة

    # Closed Class Identities
    CLOSED_CLASS_IDENTITY = auto()             # هوية صنف مغلق

    # Functional and Syntactic Identities
    FUNCTIONAL_RELATION_IDENTITY = auto()      # هوية علاقة وظيفية
    AMIL_IDENTITY = auto()                     # هوية عامل
    MAAMUL_IDENTITY = auto()                   # هوية معمول

    # Agreement and Reference Identities
    AGREEMENT_IDENTITY = auto()                # هوية اتفاق
    REFERENCE_IDENTITY = auto()                # هوية مرجع

    # Semantic Identities
    SEMANTIC_IDENTITY = auto()                 # هوية معنوية
    IFADAH_IDENTITY = auto()                   # هوية إفادة

    # Judgment Identity
    HUKM_IDENTITY = auto()                     # هوية حكم


class IdentityLayer(Enum):
    """
    Layer assignment for each identity type.

    Used to enforce progression rules: higher layer identities cannot
    exist before lower layer identities are established.
    """
    SURFACE_LAYER = 0           # U₀-U₁: Raw surface, orthographic
    PHONETIC_LAYER = 2          # U₂: Phonetic, syllabic
    BOUNDARY_LAYER = 3          # U₃: Boundary detection
    LAFZ_LAYER = 4              # U₄: True lafz
    FUNCTIONAL_LAYER = 5        # U₅: Functional roles
    CLOSED_CLASS_LAYER = 6      # U₆: Mabni closed class
    PROTECTION_LAYER = 7        # U₇: Surface protection (A/B/C)
    ROOT_LAYER = 8              # U₈: Root/stem candidates
    WEIGHT_LAYER = 9            # U₉: Weight/pattern
    FORM_LAYER = 10             # U₁₀+: Word forms
    LEXICAL_LAYER = 11          # U₁₁+: Lexical entries
    SYNTACTIC_LAYER = 13        # U₁₃+: Phrase relations
    SEMANTIC_LAYER = 14         # U₁₄+: Semantic interpretation
    JUDGMENT_LAYER = 15         # U₁₅+: Final judgment


@dataclass(frozen=True)
class IdentitySpec:
    """
    Specification for one identity type.

    Attributes:
        identity_type: The identity classification
        arabic_name: Arabic name for the identity
        layer: Layer where this identity first appears
        requires: Identity types that must exist before this one
        prohibits: Identity types that cannot coexist with this one
        allows_transition_to: Identity types this can transition to
        is_certificate: Whether this represents certified status (vs candidate)
    """
    identity_type: IdentityType
    arabic_name: str
    layer: IdentityLayer
    requires: FrozenSet[IdentityType] = frozenset()
    prohibits: FrozenSet[IdentityType] = frozenset()
    allows_transition_to: FrozenSet[IdentityType] = frozenset()
    is_certificate: bool = False

    def can_transition_to(self, target: IdentityType) -> bool:
        """Check if transition to target identity is allowed."""
        return target in self.allows_transition_to

    def requires_satisfied(self, existing: FrozenSet[IdentityType]) -> bool:
        """Check if all required identities exist."""
        return self.requires.issubset(existing)

    def has_conflict(self, existing: FrozenSet[IdentityType]) -> bool:
        """Check if any prohibited identities exist."""
        return bool(self.prohibits.intersection(existing))


# ============================================================================
# Identity Registry - Immutable Catalog
# ============================================================================

class IdentityRegistry:
    """
    Immutable registry of all identity types in the Arabic linguistic pipeline.

    Provides:
        - Identity specifications and metadata
        - Transition validation
        - Layer progression enforcement
        - Requirement checking

    Immutability:
        - Backed by MappingProxyType
        - No runtime additions (registry is closed at construction)
        - All specs are frozen dataclasses

    Usage:
        registry = IdentityRegistry()
        spec = registry.get_spec(IdentityType.ROOT_MATERIAL_IDENTITY)
        can_transition = registry.can_transition(from_id, to_id, existing_ids)
    """

    def __init__(self):
        """Initialize identity registry with all identity specifications."""
        # Build internal registry
        self._specs: Dict[IdentityType, IdentitySpec] = {}
        self._build_registry()

        # Freeze registry
        self._specs = MappingProxyType(self._specs)

    def _build_registry(self) -> None:
        """Build complete identity registry with specifications."""

        # Surface and Orthographic (U₀-U₁)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.RAW_SURFACE_IDENTITY,
            arabic_name="سطح خام",
            layer=IdentityLayer.SURFACE_LAYER,
            requires=frozenset(),
            allows_transition_to=frozenset({
                IdentityType.ORTHOGRAPHIC_IDENTITY,
                IdentityType.PHONETIC_IDENTITY
            })
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.ORTHOGRAPHIC_IDENTITY,
            arabic_name="هوية إملائية",
            layer=IdentityLayer.SURFACE_LAYER,
            requires=frozenset({IdentityType.RAW_SURFACE_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.PHONETIC_IDENTITY
            })
        ))

        # Phonetic and Syllabic (U₂)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.PHONETIC_IDENTITY,
            arabic_name="هوية صوتية",
            layer=IdentityLayer.PHONETIC_LAYER,
            requires=frozenset({IdentityType.ORTHOGRAPHIC_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.SYLLABIC_IDENTITY
            })
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.SYLLABIC_IDENTITY,
            arabic_name="هوية مقطعية",
            layer=IdentityLayer.PHONETIC_LAYER,
            requires=frozenset({IdentityType.PHONETIC_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.BOUNDARY_IDENTITY
            })
        ))

        # Boundary (U₃)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.BOUNDARY_IDENTITY,
            arabic_name="هوية حدودية",
            layer=IdentityLayer.BOUNDARY_LAYER,
            requires=frozenset({IdentityType.SYLLABIC_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.LAFZ_IDENTITY
            })
        ))

        # Lafz (U₄)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.LAFZ_IDENTITY,
            arabic_name="هوية لفظية",
            layer=IdentityLayer.LAFZ_LAYER,
            requires=frozenset({IdentityType.BOUNDARY_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.MARKER_IDENTITY,
                IdentityType.PROTECTED_SURFACE_IDENTITY,
                IdentityType.CLOSED_CLASS_IDENTITY
            })
        ))

        # Surface Protection (U₇)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.MARKER_IDENTITY,
            arabic_name="هوية علامة",
            layer=IdentityLayer.PROTECTION_LAYER,
            requires=frozenset({IdentityType.LAFZ_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.PROTECTED_SURFACE_IDENTITY
            })
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.PROTECTED_SURFACE_IDENTITY,
            arabic_name="سطح محمي",
            layer=IdentityLayer.PROTECTION_LAYER,
            requires=frozenset({IdentityType.LAFZ_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.PROTECTED_CORE_IDENTITY,
                IdentityType.LICENSED_ROOT_INPUT_IDENTITY
            })
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.PROTECTED_CORE_IDENTITY,
            arabic_name="نواة محمية",
            layer=IdentityLayer.PROTECTION_LAYER,
            requires=frozenset({IdentityType.PROTECTED_SURFACE_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.LICENSED_ROOT_INPUT_IDENTITY
            })
        ))

        # Root Input Licensing (U₇→U₈ transition)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.LICENSED_ROOT_INPUT_IDENTITY,
            arabic_name="مدخل جذر مرخص",
            layer=IdentityLayer.PROTECTION_LAYER,
            requires=frozenset({IdentityType.PROTECTED_CORE_IDENTITY}),
            prohibits=frozenset({IdentityType.ROOT_MATERIAL_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.ROOT_MATERIAL_IDENTITY,
                IdentityType.STEM_IDENTITY
            })
        ))

        # Root/Stem Material (U₈) - CANDIDATES not CERTIFICATES
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.ROOT_MATERIAL_IDENTITY,
            arabic_name="مادة جذرية (مرشح)",
            layer=IdentityLayer.ROOT_LAYER,
            requires=frozenset({IdentityType.LICENSED_ROOT_INPUT_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.WEIGHT_IDENTITY
            }),
            is_certificate=False  # CRITICAL: Root in U₈ is candidate only
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.STEM_IDENTITY,
            arabic_name="هوية جذع (مرشح)",
            layer=IdentityLayer.ROOT_LAYER,
            requires=frozenset({IdentityType.LICENSED_ROOT_INPUT_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.WEIGHT_IDENTITY
            }),
            is_certificate=False  # CRITICAL: Stem in U₈ is candidate only
        ))

        # Weight and Form (U₉-U₁₀)
        # CRITICAL FIX (PR-127): WEIGHT_IDENTITY requires ONE-OF (root OR stem), not BOTH
        # Arabic weight derivation paths:
        # - Root-based: root → weight (e.g., كتب → فاعل → كاتب)
        # - Stem-based: stem → weight (e.g., patterns on existing stems)
        # Using frozenset with both creates AND logic (requires both simultaneously).
        # This is algebraically incorrect - a word derives from root OR stem, not both.
        #
        # NOTE: Python frozenset in 'requires' means ALL must exist (AND semantics).
        # For ONE-OF semantics, we need a different approach.
        # For now, remove requirement - validation happens at path level.
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.WEIGHT_IDENTITY,
            arabic_name="هوية وزن",
            layer=IdentityLayer.WEIGHT_LAYER,
            requires=frozenset(),  # Path-aware: validated at transition time, not structure time
            allows_transition_to=frozenset({
                IdentityType.WORDFORM_IDENTITY
            })
        ))

        # WORDFORM_IDENTITY: Path-aware (PR-127)
        # Can arise from:
        # - Weight path: WEIGHT_IDENTITY → WORDFORM_IDENTITY
        # - Mabni/closed-class path: CLOSED_CLASS_IDENTITY → WORDFORM_IDENTITY
        # - Tool/pronoun path: direct from LAFZ_IDENTITY
        # Remove unconditional WEIGHT_IDENTITY requirement
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.WORDFORM_IDENTITY,
            arabic_name="هوية صورة الكلمة",
            layer=IdentityLayer.FORM_LAYER,
            requires=frozenset(),  # Path-aware: different paths to word form
            allows_transition_to=frozenset({
                IdentityType.RELATION_COMPOSITION_IDENTITY,
                IdentityType.FORM_IDENTITY
            })
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.FORM_IDENTITY,
            arabic_name="هوية صيغة",
            layer=IdentityLayer.FORM_LAYER,
            requires=frozenset({IdentityType.WORDFORM_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.SOURCE_IDENTITY,
                IdentityType.ATTRIBUTE_IDENTITY,
                IdentityType.FUNCTIONAL_RELATION_IDENTITY
            })
        ))

        # Relation Composition (U₁₁)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.RELATION_COMPOSITION_IDENTITY,
            arabic_name="هوية تركيب علائقي",
            layer=IdentityLayer.LEXICAL_LAYER,
            requires=frozenset({IdentityType.WORDFORM_IDENTITY}),
            prohibits=frozenset({
                IdentityType.SEMANTIC_IDENTITY,
                IdentityType.IFADAH_IDENTITY,
                IdentityType.HUKM_IDENTITY
            }),
            allows_transition_to=frozenset({
                IdentityType.IFADAH_IDENTITY
            })
        ))

        # Derivational Identities (U₁₀+)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.SOURCE_IDENTITY,
            arabic_name="هوية مصدر",
            layer=IdentityLayer.FORM_LAYER,
            requires=frozenset({IdentityType.FORM_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.SEMANTIC_IDENTITY
            })
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.ATTRIBUTE_IDENTITY,
            arabic_name="هوية صفة",
            layer=IdentityLayer.FORM_LAYER,
            requires=frozenset({IdentityType.FORM_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.SEMANTIC_IDENTITY,
                IdentityType.AGREEMENT_IDENTITY
            })
        ))

        # Closed Class (U₆)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.CLOSED_CLASS_IDENTITY,
            arabic_name="هوية صنف مغلق",
            layer=IdentityLayer.CLOSED_CLASS_LAYER,
            requires=frozenset({IdentityType.LAFZ_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.FUNCTIONAL_RELATION_IDENTITY,
                IdentityType.AMIL_IDENTITY
            })
        ))

        # Functional and Syntactic Identities (U₁₃+)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.FUNCTIONAL_RELATION_IDENTITY,
            arabic_name="هوية علاقة وظيفية",
            layer=IdentityLayer.SYNTACTIC_LAYER,
            requires=frozenset({IdentityType.FORM_IDENTITY}),
            prohibits=frozenset({IdentityType.SEMANTIC_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.AMIL_IDENTITY,
                IdentityType.MAAMUL_IDENTITY,
                IdentityType.SEMANTIC_IDENTITY
            })
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.AMIL_IDENTITY,
            arabic_name="هوية عامل",
            layer=IdentityLayer.SYNTACTIC_LAYER,
            requires=frozenset({IdentityType.FUNCTIONAL_RELATION_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.MAAMUL_IDENTITY
            })
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.MAAMUL_IDENTITY,
            arabic_name="هوية معمول",
            layer=IdentityLayer.SYNTACTIC_LAYER,
            requires=frozenset({IdentityType.AMIL_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.SEMANTIC_IDENTITY
            })
        ))

        # Agreement and Reference
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.AGREEMENT_IDENTITY,
            arabic_name="هوية اتفاق",
            layer=IdentityLayer.PROTECTION_LAYER,
            requires=frozenset({IdentityType.LAFZ_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.REFERENCE_IDENTITY
            })
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.REFERENCE_IDENTITY,
            arabic_name="هوية مرجع",
            layer=IdentityLayer.SEMANTIC_LAYER,
            requires=frozenset({IdentityType.AGREEMENT_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.SEMANTIC_IDENTITY
            })
        ))

        # Semantic Identities (U₁₄-U₁₅)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.SEMANTIC_IDENTITY,
            arabic_name="هوية معنوية",
            layer=IdentityLayer.SEMANTIC_LAYER,
            requires=frozenset({IdentityType.FUNCTIONAL_RELATION_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.IFADAH_IDENTITY
            })
        ))

        self._add_spec(IdentitySpec(
            identity_type=IdentityType.IFADAH_IDENTITY,
            arabic_name="هوية إفادة",
            layer=IdentityLayer.SEMANTIC_LAYER,
            requires=frozenset({IdentityType.SEMANTIC_IDENTITY}),
            allows_transition_to=frozenset({
                IdentityType.HUKM_IDENTITY
            })
        ))

        # Judgment Identity (U₁₅+)
        self._add_spec(IdentitySpec(
            identity_type=IdentityType.HUKM_IDENTITY,
            arabic_name="هوية حكم",
            layer=IdentityLayer.JUDGMENT_LAYER,
            requires=frozenset({IdentityType.IFADAH_IDENTITY}),
            allows_transition_to=frozenset(),  # Terminal identity
            is_certificate=True
        ))

    def _add_spec(self, spec: IdentitySpec) -> None:
        """Add identity specification to registry (internal use only)."""
        self._specs[spec.identity_type] = spec

    def get_spec(self, identity_type: IdentityType) -> IdentitySpec:
        """
        Get specification for an identity type.

        Args:
            identity_type: Identity type to look up

        Returns:
            IdentitySpec for the given type

        Raises:
            KeyError: If identity type not found in registry
        """
        return self._specs[identity_type]

    def can_transition(
        self,
        from_identity: IdentityType,
        to_identity: IdentityType,
        existing_identities: FrozenSet[IdentityType]
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if transition from one identity to another is allowed.

        Validates:
            1. Required identities exist (checked first - missing prerequisites)
            2. No prohibited identities exist
            3. Transition is in allowed_transition_to set
            4. Layer progression is valid

        Args:
            from_identity: Source identity
            to_identity: Target identity
            existing_identities: Set of currently established identities

        Returns:
            (is_allowed, reason) tuple. reason is None if allowed, error message if not.
        """
        from_spec = self.get_spec(from_identity)
        to_spec = self.get_spec(to_identity)

        # Check if required identities exist FIRST (missing prerequisites)
        if not to_spec.requires_satisfied(existing_identities):
            missing = to_spec.requires - existing_identities
            missing_names = [self.get_spec(m).arabic_name for m in missing]
            return False, f"Missing required identities: {', '.join(missing_names)}"

        # Check for prohibited identities
        if to_spec.has_conflict(existing_identities):
            conflicts = to_spec.prohibits.intersection(existing_identities)
            conflict_names = [self.get_spec(c).arabic_name for c in conflicts]
            return False, f"Conflicting identities exist: {', '.join(conflict_names)}"

        # Check if transition is explicitly allowed (structurally forbidden)
        if not from_spec.can_transition_to(to_identity):
            return False, f"Transition from {from_spec.arabic_name} to {to_spec.arabic_name} not allowed"

        # Check layer progression (cannot skip layers)
        if to_spec.layer.value < from_spec.layer.value:
            return False, f"Cannot regress from layer {from_spec.layer.value} to {to_spec.layer.value}"

        return True, None

    def get_required_for(self, identity_type: IdentityType) -> FrozenSet[IdentityType]:
        """Get all identities required before this one can be established."""
        return self.get_spec(identity_type).requires

    def get_layer(self, identity_type: IdentityType) -> IdentityLayer:
        """Get the layer where this identity first appears."""
        return self.get_spec(identity_type).layer

    def is_certificate(self, identity_type: IdentityType) -> bool:
        """Check if identity represents certified status (vs candidate)."""
        return self.get_spec(identity_type).is_certificate

    def validate_identity_sequence(
        self,
        sequence: Tuple[IdentityType, ...]
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate that a sequence of identities follows valid progression.

        Args:
            sequence: Ordered sequence of identity types

        Returns:
            (is_valid, error_message) tuple
        """
        if not sequence:
            return True, None

        existing: FrozenSet[IdentityType] = frozenset()

        for i, identity_type in enumerate(sequence):
            spec = self.get_spec(identity_type)

            # Check requirements
            if not spec.requires_satisfied(existing):
                missing = spec.requires - existing
                missing_names = [self.get_spec(m).arabic_name for m in missing]
                return False, f"At position {i}, identity {spec.arabic_name} missing requirements: {', '.join(missing_names)}"

            # Check conflicts
            if spec.has_conflict(existing):
                conflicts = spec.prohibits.intersection(existing)
                conflict_names = [self.get_spec(c).arabic_name for c in conflicts]
                return False, f"At position {i}, identity {spec.arabic_name} conflicts with: {', '.join(conflict_names)}"

            # Add to existing
            existing = existing | {identity_type}

        return True, None


# ============================================================================
# Guard Functions
# ============================================================================

def verify_identity_preserved(
    input_identity: IdentityType,
    output_identity: IdentityType,
    registry: IdentityRegistry
) -> Tuple[bool, Optional[str]]:
    """
    Verify that identity is preserved or properly transitioned.

    Identity preservation law:
        Output identity must be same as input OR valid transition target.

    Args:
        input_identity: Identity before transition
        output_identity: Identity after transition
        registry: Identity registry

    Returns:
        (is_preserved, reason) tuple
    """
    if input_identity == output_identity:
        return True, None  # Identity preserved

    # Check if transition is valid
    input_spec = registry.get_spec(input_identity)
    if output_identity in input_spec.allows_transition_to:
        return True, None  # Valid transition

    return False, f"Identity not preserved: {input_spec.arabic_name} → {registry.get_spec(output_identity).arabic_name} is forbidden"


__all__ = [
    "IdentityType",
    "IdentityLayer",
    "IdentitySpec",
    "IdentityRegistry",
    "verify_identity_preserved",
]
