"""Fractal Algebraic Base for Lafẓī Madlūl Layers.

Every layer in the lexical signified must implement the same algebraic pattern.
This module defines the fractal contract that each layer must satisfy.

## The Fractal Pattern

Each layer ``L`` is not just a transition node, but a complete algebra::

    A_L = (U_L, T_L, B_L, I_L, O_L, G_L, CPB_L, ρ_L, R_L, F_L)

This pattern **repeats fractally** across all 11 layers, from Trace to Word.

## Why Fractal?

If we build only transitions ``trace → letter → syllable → root``, we create
a **path**, not a **geometry**. The fractal pattern ensures:

1. Each layer is self-contained (internal closure)
2. Each layer has the same structure (self-similarity)
3. Transitions preserve properties (conservation laws)
4. No layer generates meaning (boundary enforcement)

"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional, Protocol, Tuple, TypeVar

from ..core import Rank, Trace


# ===========================================================================
# Fractal Pattern Components
# ===========================================================================


class LayerType(Enum):
    """Types of lexical layers in the fractal hierarchy."""

    TRACE = auto()              # L0: الأثر
    LETTER = auto()             # L1: الحرف
    HARAKAH = auto()            # L2: الحركة
    ATOM = auto()               # L3: الذرة (letter + harakah)
    SYLLABLE = auto()           # L4: المقطع
    SEQUENCE = auto()           # L5: التتابع
    ROOT_CANDIDATE = auto()     # L6: الجذر المرشح
    AFFIX_OPERATOR = auto()     # L7: الزيادة (operator)
    PATTERN_TEMPLATE = auto()   # L8: الوزن
    BUILT_FORM = auto()         # L9: الصيغة
    WORD_CANDIDATE = auto()     # L10: الكلمة المرشحة


T = TypeVar("T")


@dataclass(frozen=True)
class LayerAlgebra(Protocol):
    """Protocol defining the fractal algebraic structure each layer must implement.

    This is the **unified template** that repeats across all layers.

    Every layer L must provide:
        - U_L: Unit definition
        - T_L: Type system
        - B_L: Boundary tests
        - I_L: Internal bindings
        - O_L: Allowed operations
        - G_L: Licensing gates
        - CPB_L: Constraint-preserving binding
        - ρ_L: Rank policy
        - R_L: Residuals
        - F_L: Failure types
    """

    # U_L: الوحدة - Unit
    unit_type: LayerType
    unit_value: Any

    # T_L: الأنواع - Type System
    type_classification: str

    # B_L: الحدود - Boundaries
    boundaries: Dict[str, bool]

    # I_L: الربط الداخلي - Internal Bindings
    internal_bindings: Dict[str, Any]

    # O_L: العمليات - Operations
    allowed_operations: List[str]

    # G_L: البوابات - Gates
    licensing_status: str

    # CPB_L: الربط الحافظ - Constraint-Preserving Binding
    cpb_metadata: Dict[str, Any]

    # ρ_L: سياسة الرتبة - Rank Policy
    rank: Rank
    evidence: List[str]

    # R_L: البقايا - Residuals
    residuals: List[str]

    # F_L: أنواع الفشل - Failure Types
    failure_type: Optional[str]

    # Trace preservation
    trace: Trace


# ===========================================================================
# The Four Geometries of Each Layer
# ===========================================================================


class UnitGeometry:
    """هندسة الوحدة: What is the minimal unit of this layer?

    Each layer defines its own minimal lexical object.

    Examples:
        - Letter: single grapheme/phoneme
        - Harakah: single diacritic constraint
        - Atom: letter + harakah binding
        - Syllable: phonotactically valid atom sequence
        - Root: consonantal skeleton
        - Pattern: morphological template
    """

    @staticmethod
    def define_minimal_unit(layer: LayerType) -> str:
        """Return the minimal unit definition for a layer."""
        units = {
            LayerType.TRACE: "raw phonetic/graphic trace",
            LayerType.LETTER: "single grapheme/phoneme",
            LayerType.HARAKAH: "single diacritic constraint",
            LayerType.ATOM: "letter + harakah binding",
            LayerType.SYLLABLE: "phonotactically valid atom sequence",
            LayerType.SEQUENCE: "syllable chain",
            LayerType.ROOT_CANDIDATE: "consonantal skeleton",
            LayerType.AFFIX_OPERATOR: "augmentation operator",
            LayerType.PATTERN_TEMPLATE: "morphological template",
            LayerType.BUILT_FORM: "root ⊗ pattern",
            LayerType.WORD_CANDIDATE: "lexical candidate with usage status",
        }
        return units.get(layer, "undefined")


class BoundaryGeometry:
    """هندسة الحدود: Where does this layer start and end?

    Boundaries determine what belongs to the layer and what doesn't.

    Examples:
        - Letter: Is this letter from root or affix?
        - Harakah: Is this harakah binā' or i'rāb?
        - Syllable: Where does the syllable begin/end?
    """

    @staticmethod
    def boundary_questions(layer: LayerType) -> List[str]:
        """Return the boundary questions for a layer."""
        questions = {
            LayerType.LETTER: [
                "هل هذا الحرف من الجذر؟",
                "هل هو من الزيادة؟",
                "هل هو حرف معنى؟",
            ],
            LayerType.HARAKAH: [
                "هل هذه الحركة بنائية؟",
                "هل هي إعرابية؟",
                "هل هي وزنية؟",
            ],
            LayerType.SYLLABLE: [
                "أين يبدأ المقطع؟",
                "أين ينتهي؟",
                "هل هو مستقل؟",
            ],
            LayerType.ROOT_CANDIDATE: [
                "ما الحروف الأصلية؟",
                "ما الحروف الزائدة؟",
                "هل الترتيب محفوظ؟",
            ],
        }
        return questions.get(layer, [])


class BindingGeometry:
    """هندسة الربط: What binds to what within this layer?

    Internal bindings define the compositional structure.

    Examples:
        - Letter binds to Harakah → Atom
        - Atoms bind into Syllable
        - Root binds to Pattern → BuiltForm
    """

    @staticmethod
    def binding_targets(layer: LayerType) -> Dict[str, str]:
        """Return what this layer binds to."""
        bindings = {
            LayerType.LETTER: {"binds_to": "Harakah", "type": "phonetic"},
            LayerType.HARAKAH: {"binds_to": "Letter", "type": "positional"},
            LayerType.ATOM: {"binds_to": "Atom (sequence)", "type": "syllabic"},
            LayerType.ROOT_CANDIDATE: {"binds_to": "Pattern", "type": "slot_alignment"},
            LayerType.AFFIX_OPERATOR: {"binds_to": "Root", "type": "operator_application"},
        }
        return bindings.get(layer, {})


class InheritanceGeometry:
    """هندسة التوريث: What can this layer inherit to the next?

    Defines what properties are allowed/forbidden to pass to next layer.

    **Critical**: No layer inherits semantic meaning.

    Examples:
        - Letter inherits: build capability, phonetic potential
        - Letter PROHIBITS: meaning, semantic value
        - Root inherits: lexical material, domain possibility
        - Root PROHIBITS: direct meaning, maṣdar without verb
    """

    @staticmethod
    def allowed_inheritance(layer: LayerType) -> Dict[str, List[str]]:
        """Return what this layer allows/prohibits for inheritance."""
        inheritance = {
            LayerType.LETTER: {
                "inherits": ["build_capability", "phonetic_potential"],
                "prohibits": ["meaning", "semantic_value"],
            },
            LayerType.HARAKAH: {
                "inherits": ["pattern_constraint", "positional_constraint"],
                "prohibits": ["i'rab_judgment", "direct_case_effect"],
            },
            LayerType.ROOT_CANDIDATE: {
                "inherits": ["lexical_material", "domain_possibility"],
                "prohibits": ["direct_meaning", "masdar_without_verb"],
            },
            LayerType.PATTERN_TEMPLATE: {
                "inherits": ["formal_template", "semantic_potential"],
                "prohibits": ["fa'iliyyah_certainty", "maf'uliyyah_certainty"],
            },
        }
        return inheritance.get(layer, {"inherits": [], "prohibits": ["meaning"]})


# ===========================================================================
# Fractal Pattern Enforcement
# ===========================================================================


@dataclass
class FractalPattern:
    """The fractal pattern that repeats across all layers.

    This is the **self-similar structure** ensuring algebraic coherence.

    Pattern::

        تمييز → وحدة → حدود → ربط → بوابة → رتبة → بقايا → توريث
        discrimination → unit → boundaries → binding → gate → rank → residuals → inheritance
    """

    PATTERN_STAGES = [
        "discrimination",     # تمييز - distinguish this layer
        "unit",              # وحدة - define minimal unit
        "boundaries",        # حدود - test boundaries
        "binding",           # ربط - internal composition
        "gate",              # بوابة - licensing conditions
        "rank",              # رتبة - epistemic rank
        "residuals",         # بقايا - what remains unresolved
        "inheritance",       # توريث - what passes to next layer
    ]

    @classmethod
    def apply_to_layer(cls, layer_name: str) -> Dict[str, str]:
        """Apply the fractal pattern to a specific layer.

        Returns the pattern instantiated for that layer.
        """
        return {
            "discrimination": f"تمييز {layer_name}",
            "unit": f"وحدة {layer_name}",
            "boundaries": f"حدود {layer_name}",
            "binding": f"ربط {layer_name} الداخلي",
            "gate": f"بوابة ترخيص {layer_name}",
            "rank": f"رتبة {layer_name}",
            "residuals": f"بقايا {layer_name}",
            "inheritance": f"ما يورثه {layer_name}",
        }

    @classmethod
    def validate_layer_completeness(cls, layer: Any) -> Tuple[bool, List[str]]:
        """Validate that a layer implements all fractal pattern stages.

        Returns:
            (is_complete, missing_stages)
        """
        missing = []

        # Check required attributes
        required_attrs = [
            "unit_type",
            "unit_value",
            "boundaries",
            "internal_bindings",
            "rank",
            "residuals",
            "trace",
        ]

        for attr in required_attrs:
            if not hasattr(layer, attr):
                missing.append(attr)

        # Check for forbidden attributes (meaning leak)
        forbidden_attrs = ["meaning", "madlul", "semantic_value", "hukm"]
        for attr in forbidden_attrs:
            if hasattr(layer, attr):
                missing.append(f"FORBIDDEN:{attr}")

        return (len(missing) == 0, missing)


# ===========================================================================
# Layer Validation Utilities
# ===========================================================================


def validate_no_meaning_field(obj: Any) -> None:
    """Ensure object has no semantic meaning fields.

    Enforces the "No Meaning Jump Law" (قانون منع القفز إلى المعنى).

    Raises:
        ValueError: If forbidden semantic field detected.
    """
    FORBIDDEN_FIELDS = [
        "meaning",
        "madlul",
        "semantic_value",
        "hukm",
        "ifadah",
        "dalalah",
    ]

    for field in FORBIDDEN_FIELDS:
        if hasattr(obj, field):
            raise ValueError(
                f"Forbidden semantic field '{field}' in lafẓī layer "
                f"{obj.__class__.__name__}. "
                f"Lexical layers must not produce meaning."
            )


def validate_internal_closure(layer: Any) -> Tuple[bool, List[str]]:
    """Validate internal closure: layer is complete before transition.

    Implements "Internal Closure Law" (قانون الإغلاق الداخلي).

    Returns:
        (is_closed, incomplete_aspects)
    """
    incomplete = []

    # Check unit is defined
    if not hasattr(layer, "unit_value") or layer.unit_value is None:
        incomplete.append("unit_undefined")

    # Check boundaries are tested
    if not hasattr(layer, "boundaries") or not layer.boundaries:
        incomplete.append("boundaries_untested")

    # Check bindings are complete
    if hasattr(layer, "internal_bindings"):
        if not layer.internal_bindings:
            incomplete.append("bindings_incomplete")

    return (len(incomplete) == 0, incomplete)
