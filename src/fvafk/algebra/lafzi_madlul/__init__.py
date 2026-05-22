"""Lafẓī Madlūl Fractal Algebra (المدلول اللفظي الفركتالي).

This package implements the foundational algebraic structure for lexical
signifieds - the formal/phonological/morphological structures that exist
**before semantic meaning**.

## Core Principle

    المدلول اللفظي لا يتماسك بالانتقال وحده.
    يتماسك بأن تكون كل طبقة فيه جبراً كاملاً،
    ثم يكون الانتقال بينها حافظاً لا مولداً لمعنى.

    "The lexical signified does not cohere through transitions alone.
    It coheres when each layer is a complete algebra,
    and transitions between layers preserve without generating meaning."

## Fractal Pattern

Every layer ``L`` implements the same algebraic structure::

    A_L = (U_L, T_L, B_L, I_L, O_L, G_L, CPB_L, ρ_L, R_L, F_L)

Where:
    - U_L: Unit (الوحدة) - minimal lexical object
    - T_L: Type system (الأنواع)
    - B_L: Boundaries (الحدود) - where layer starts/ends
    - I_L: Internal bindings (الربط الداخلي)
    - O_L: Allowed operations (العمليات المسموحة)
    - G_L: Licensing gates (بوابات الترخيص)
    - CPB_L: Constraint-preserving binding (الربط الحافظ)
    - ρ_L: Rank policy (سياسة الرتبة)
    - R_L: Residuals (البقايا)
    - F_L: Failure types (أنواع الفشل)

## The 11 Layers

1. **Trace** (الأثر) - raw phonetic/graphic trace
2. **Letter** (الحرف) - grapheme/phoneme unit
3. **Harakah** (الحركة) - diacritic constraint
4. **Atom** (الذرة) - letter + harakah binding
5. **Syllable** (المقطع) - phonotactic unit
6. **Sequence** (التتابع) - syllable chain + phonetic economy
7. **RootCandidate** (الجذر المرشح) - consonantal skeleton
8. **AffixOperator** (الزيادة) - augmentation as operator
9. **PatternTemplate** (الوزن) - morphological template
10. **BuiltForm** (الصيغة) - root ⊗ pattern application
11. **WordCandidate** (الكلمة المرشحة) - lexical candidate

## Three Governing Laws

1. **Internal Closure Law** (قانون الإغلاق الداخلي)::

       لا انتقال قبل اكتمال الجبر الداخلي للطبقة

   No transition before internal algebra completion.

2. **Preservation Law** (قانون الحفظ)::

       كل انتقال يحفظ الأثر والرتبة والبقايا

   Every transition preserves trace, rank, and residuals.

3. **No Meaning Jump Law** (قانون منع القفز إلى المعنى)::

       لا طبقة لفظية تصدر معنى

   No lexical layer produces semantic meaning.

## Usage Example

    >>> from fvafk.algebra.lafzi_madlul import LetterAlgebra, HarakahAlgebra
    >>> from fvafk.algebra.lafzi_madlul import cpb_letter_harakah
    >>>
    >>> # Build letter algebra
    >>> letter = LetterAlgebra.from_form("ك")
    >>> # Build harakah algebra
    >>> harakah = HarakahAlgebra.from_form("َ")
    >>> # CPB binding preserves both without generating meaning
    >>> atom = cpb_letter_harakah(letter, harakah)
    >>> assert atom.rank <= max(letter.rank, harakah.rank)
    >>> assert not hasattr(atom, "meaning")  # No semantic field!

"""

from .fractal_algebra import (
    LayerAlgebra,
    FractalPattern,
    UnitGeometry,
    BoundaryGeometry,
    BindingGeometry,
    InheritanceGeometry,
)

from .layer_algebras import (
    TraceAlgebra,
    LetterAlgebra,
    HarakahAlgebra,
    AtomAlgebra,
    SyllableAlgebra,
    SequenceAlgebra,
    RootCandidateAlgebra,
    AffixOperatorAlgebra,
    PatternTemplateAlgebra,
    BuiltFormAlgebra,
    WordCandidateAlgebra,
)

from .transitions import (
    AlgebraicTransition,
    internal_closure_law,
    preservation_law,
    no_meaning_jump_law,
    cpb_letter_harakah,
    cpb_root_pattern,
)

from .residual_taxonomy import (
    LafziResidual,
    LetterResidual,
    HarakahResidual,
    SyllableResidual,
    RootResidual,
    PatternResidual,
    FormResidual,
)

__all__ = [
    # Fractal base
    "LayerAlgebra",
    "FractalPattern",
    "UnitGeometry",
    "BoundaryGeometry",
    "BindingGeometry",
    "InheritanceGeometry",
    # Layer algebras
    "TraceAlgebra",
    "LetterAlgebra",
    "HarakahAlgebra",
    "AtomAlgebra",
    "SyllableAlgebra",
    "SequenceAlgebra",
    "RootCandidateAlgebra",
    "AffixOperatorAlgebra",
    "PatternTemplateAlgebra",
    "BuiltFormAlgebra",
    "WordCandidateAlgebra",
    # Transitions
    "AlgebraicTransition",
    "internal_closure_law",
    "preservation_law",
    "no_meaning_jump_law",
    "cpb_letter_harakah",
    "cpb_root_pattern",
    # Residuals
    "LafziResidual",
    "LetterResidual",
    "HarakahResidual",
    "SyllableResidual",
    "RootResidual",
    "PatternResidual",
    "FormResidual",
]
