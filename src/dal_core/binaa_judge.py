"""
Binaa / I'rab Judge (قاضي البناء/الإعراب)

==============================================================================
ANTI-HALLUCINATION GUARD
==============================================================================
This judge MUST NOT use ``syllable_count``, ``syllable_shapes``, or any
descriptive output of D1 (SYLLABIC) as input. The number/shape of syllables
is a *descriptive* axis; the binaa/i'rab axis is *judicial*. Crossing them
is the exact hallucination this entire module was built to prevent.

If you ever feel tempted to write::

    if len(form) <= 5: return MABNI

…stop. That is conflating two orthogonal axes. The judge's inputs are
SOLELY:

  1. ``DalType`` from D5 (IDENTITY_AXIS),
  2. ``VerbTypeID`` or evidence of nun-niswa / nun-tawkid on the SURFACE
     form for verbs only,
  3. The closed mabni-noun registry for nouns.

==============================================================================

Rule order (each rule fires only if previous rules did not match):

  R1  HARF                       ⇒ MABNI, INVARIANT_PROPER
  R2  FIIL = ماضٍ                ⇒ MABNI, BINAA_FATH (default surface)
  R3  FIIL = أمر                 ⇒ MABNI, BINAA_SUKUN (default surface)
  R4  FIIL = مضارع + نون النسوة  ⇒ MABNI, BINAA_SUKUN
  R5  FIIL = مضارع + نون التوكيد ⇒ MABNI, BINAA_FATH
  R6  FIIL = مضارع otherwise     ⇒ MUERAB
  R7  ISM   in mabni registry    ⇒ MABNI, registry-supplied subtype
  R8  ISM   otherwise            ⇒ MUERAB

  R0  Insufficient evidence to even reach R1 ⇒ UNRESOLVED + residual.
"""

from dataclasses import dataclass
from typing import Optional

from dal_core.d_type import DalType
from dal_core.evidence import Evidence, make_evidence
from dal_core.mabni_registry import (
    MabniRegistry,
    get_default_mabni_registry,
)
from dal_core.mufrad_axes import BinaaJudgment, BinaaSubtype
from dal_core.residuals import Residual, ResidualSeverity, ResidualType
from dal_core.type_ids import VerbTypeID


# =============================================================================
# Input contract — only what the rules actually need
# =============================================================================


@dataclass(frozen=True)
class BinaaJudgeInput:
    """The minimal typed bundle the binaa judge accepts.

    Intentionally does NOT include ``syllable_count``, ``syllable_shapes``,
    or anything from D1. Adding any such field is a guard violation.
    """

    dal_type: DalType
    """Identity from D5."""

    surface_form: str
    """Vocalized surface form. Used ONLY for nun-niswa / nun-tawkid detection
    on verbs and for registry lookup on nouns."""

    verb_type_id: Optional[VerbTypeID] = None
    """Tense identifier when ``dal_type == FIIL``. Required to disambiguate
    madi / amr / mudari rules."""


# =============================================================================
# Result
# =============================================================================


@dataclass(frozen=True)
class BinaaJudgmentResult:
    judgment: BinaaJudgment
    subtype: Optional[BinaaSubtype]
    evidence: Evidence
    residuals: tuple[Residual, ...]


# =============================================================================
# Surface predicates for mudari exceptions
# =============================================================================


# Strip tashkeel for robust ending checks.
_TASHKEEL = set("\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652\u0670\u0653\u0654\u0655\u0656\u0657\u0658\u0659\u065a\u065b\u065c\u065d\u065e\u065f")


def _strip_tashkeel(s: str) -> str:
    return "".join(ch for ch in s if ch not in _TASHKEEL)


def _ends_with_nun_niswa(vocalized: str) -> bool:
    """نون النسوة: an unvocalized ``نَ`` immediately attached to a verb stem
    end. Distinguishing it from nun-tawkid-khafifa (نْ with sukun) and from
    raf' nun on verbs of the five (يفعلون/يفعلان/تفعلين) is what justifies
    a dedicated predicate.

    Heuristic guard (sufficient for the rule, not a full morphological
    analyzer): the vocalized form ends with ``نَ`` AND not with the
    five-verbs raf' nuns ``ـونَ / ـانَ / ـينَ``.
    """
    s = vocalized
    if not s.endswith("نَ"):
        return False
    bare = _strip_tashkeel(s)
    # Exclude the raf' nun of the five verbs.
    for ending in ("ون", "ان", "ين"):
        if bare.endswith(ending):
            return False
    return True


def _ends_with_nun_tawkid(vocalized: str) -> bool:
    """نون التوكيد المباشرة:
       - الثقيلة: ends with ``نَّ`` (shadda + fatha).
       - الخفيفة: ends with ``نْ``.
    Indirect tawkid (e.g. separated by alif) is intentionally not handled
    here; the judge errs on the side of MUERAB when uncertain.
    """
    return vocalized.endswith("نَّ") or vocalized.endswith("نْ")


# =============================================================================
# Public judge
# =============================================================================


def judge_binaa(
    input_: BinaaJudgeInput,
    registry: Optional[MabniRegistry] = None,
) -> BinaaJudgmentResult:
    """Apply the rule order described at the module docstring.

    Args:
        input_: typed bundle (no D1 fields permitted).
        registry: optional override; defaults to the singleton mabni registry.

    Returns:
        A ``BinaaJudgmentResult`` with judgment, optional subtype, the
        triggering evidence, and any residuals (non-empty only on UNRESOLVED).
    """
    reg = registry or get_default_mabni_registry()

    # R0 — guard against missing identity.
    if input_.dal_type is None or input_.dal_type == DalType.AMBIGUOUS:
        return BinaaJudgmentResult(
            judgment=BinaaJudgment.UNRESOLVED,
            subtype=None,
            evidence=make_evidence(
                source="binaa_judge.R0",
                reason="DalType is missing or AMBIGUOUS; cannot judge binaa.",
                confidence=0.0,
            ),
            residuals=(
                Residual(
                    type=ResidualType.MUFRAD_MABNI_MURAB_UNRESOLVED,
                    severity=ResidualSeverity.BLOCKER,
                    message="Identity axis (D5) not resolved before binaa judge.",
                ),
            ),
        )

    # R1 — HARF.
    if input_.dal_type == DalType.HARF:
        return BinaaJudgmentResult(
            judgment=BinaaJudgment.MABNI,
            subtype=BinaaSubtype.INVARIANT_PROPER,
            evidence=make_evidence(
                source="binaa_judge.R1",
                reason="All particles (حروف) are MABNI by lexical category.",
                confidence=1.0,
            ),
            residuals=(),
        )

    # R2..R6 — FIIL.
    if input_.dal_type == DalType.FIIL:
        return _judge_verb(input_)

    # R7..R8 — ISM.
    if input_.dal_type == DalType.ISM:
        return _judge_noun(input_, reg)

    # Unknown DalType value — defensive UNRESOLVED.
    return BinaaJudgmentResult(
        judgment=BinaaJudgment.UNRESOLVED,
        subtype=None,
        evidence=make_evidence(
            source="binaa_judge.R0",
            reason=f"Unrecognized DalType {input_.dal_type!r}.",
            confidence=0.0,
        ),
        residuals=(
            Residual(
                type=ResidualType.MUFRAD_MABNI_MURAB_UNRESOLVED,
                severity=ResidualSeverity.BLOCKER,
                message=f"Unrecognized DalType {input_.dal_type!r}.",
            ),
        ),
    )


# =============================================================================
# Sub-judges
# =============================================================================


def _judge_verb(input_: BinaaJudgeInput) -> BinaaJudgmentResult:
    vid = input_.verb_type_id

    # R2 — past tense.
    if vid == VerbTypeID.FIIL_MADI:
        return BinaaJudgmentResult(
            judgment=BinaaJudgment.MABNI,
            subtype=BinaaSubtype.BINAA_FATH,
            evidence=make_evidence(
                source="binaa_judge.R2",
                reason="الفعل الماضي مبني (default surface: fath).",
                confidence=1.0,
            ),
            residuals=(),
        )

    # R3 — imperative.
    if vid == VerbTypeID.FIIL_AMR:
        return BinaaJudgmentResult(
            judgment=BinaaJudgment.MABNI,
            subtype=BinaaSubtype.BINAA_SUKUN,
            evidence=make_evidence(
                source="binaa_judge.R3",
                reason="فعل الأمر مبني (default surface: sukun).",
                confidence=1.0,
            ),
            residuals=(),
        )

    # R4..R6 — present tense exceptions.
    if vid == VerbTypeID.FIIL_MUDARI:
        # R4 — nun niswa.
        if _ends_with_nun_niswa(input_.surface_form):
            return BinaaJudgmentResult(
                judgment=BinaaJudgment.MABNI,
                subtype=BinaaSubtype.BINAA_SUKUN,
                evidence=make_evidence(
                    source="binaa_judge.R4",
                    reason="المضارع المتصل بنون النسوة مبني على السكون.",
                    confidence=1.0,
                ),
                residuals=(),
            )
        # R5 — direct nun tawkid.
        if _ends_with_nun_tawkid(input_.surface_form):
            return BinaaJudgmentResult(
                judgment=BinaaJudgment.MABNI,
                subtype=BinaaSubtype.BINAA_FATH,
                evidence=make_evidence(
                    source="binaa_judge.R5",
                    reason="المضارع المتصل بنون التوكيد المباشرة مبني على الفتح.",
                    confidence=1.0,
                ),
                residuals=(),
            )
        # R6 — default mudari.
        return BinaaJudgmentResult(
            judgment=BinaaJudgment.MUERAB,
            subtype=None,
            evidence=make_evidence(
                source="binaa_judge.R6",
                reason="المضارع معرب ما لم يتصل بنون النسوة أو بنون التوكيد المباشرة.",
                confidence=1.0,
            ),
            residuals=(),
        )

    # Verb without a known tense subtype → unresolved.
    return BinaaJudgmentResult(
        judgment=BinaaJudgment.UNRESOLVED,
        subtype=None,
        evidence=make_evidence(
            source="binaa_judge.R0",
            reason="VerbTypeID missing or not one of MADI/AMR/MUDARI.",
            confidence=0.0,
        ),
        residuals=(
            Residual(
                type=ResidualType.MUFRAD_MABNI_MURAB_UNRESOLVED,
                severity=ResidualSeverity.BLOCKER,
                message="Cannot judge a verb without its tense subtype.",
            ),
        ),
    )


def _judge_noun(
    input_: BinaaJudgeInput,
    registry: MabniRegistry,
) -> BinaaJudgmentResult:
    matches = registry.lookup(input_.surface_form)

    if matches:
        # R7 — closed mabni noun. Take the first entry's subtype as the
        # canonical surface description; if multiple entries disagree on
        # subtype we still accept the first deterministically — but only
        # if all agree on the SUBTYPE; otherwise emit INVARIANT_PROPER.
        subtypes = {e.binaa_subtype for e in matches}
        subtype = matches[0].binaa_subtype if len(subtypes) == 1 else BinaaSubtype.INVARIANT_PROPER
        categories = ", ".join(sorted({e.category.value for e in matches}))
        return BinaaJudgmentResult(
            judgment=BinaaJudgment.MABNI,
            subtype=subtype,
            evidence=make_evidence(
                source="binaa_judge.R7",
                reason=f"Noun is in the closed mabni registry ({categories}).",
                confidence=1.0,
            ),
            residuals=(),
        )

    # R8 — default to MUERAB.
    return BinaaJudgmentResult(
        judgment=BinaaJudgment.MUERAB,
        subtype=None,
        evidence=make_evidence(
            source="binaa_judge.R8",
            reason="Noun not in the closed mabni registry; defaults to MUERAB.",
            confidence=0.95,
        ),
        residuals=(),
    )


__all__ = [
    "BinaaJudgeInput",
    "BinaaJudgmentResult",
    "judge_binaa",
]
