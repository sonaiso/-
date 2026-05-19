"""
Case Sign Matrix (مصفوفة علامات الإعراب)

PR #13: Post-frame, pre-operator compatibility layer.

ARCHITECTURE POSITION:
    SentenceFrameCandidate            (input — only legal source)
            ↓
    CaseSignMatrix                    (this module — compatibility evidence)
            ↓
    [future] OperatorTriggerPotential → NahwOperatorRegistry → CaseEffect

GOVERNING RULES (do NOT relax):
1. Input is ONLY a SentenceFrameCandidate (never raw tokens, never strings).
2. Output is compatibility evidence (CaseCompatibilityFamily), NOT case
   judgments (no marfoo_by, mansub_by, faail, mubtada, governed_by, etc.).
3. No CaseEffect, no operator binding, no relation, no syntax role.
4. Two internal layers per row (NEVER collapsed into one field):
       SurfaceSignObservation  →  CaseCompatibilityFamily(...)
5. Substitute signs (ALIF/WAW/YA/NUN_*) NEVER imply rafa/nasb/jarr/jazm
   without explicit morph evidence from PreSyntaxMufradVector. Missing
   evidence → UNRESOLVED + SUBSTITUTE_SIGN_REQUIRES_INFLECTION_CLASS +
   CASE_SIGN_COMPATIBILITY_UNRESOLVED.
6. Building signs (mabni words with visible final harakah) produce ONLY
   BUILDING_COMPATIBLE, never mixed with case families. mabni_murab_status
   (CandidateStatus) is NOT proof of being mabni; valued evidence required
   (noun_inflection_class.inflection_type == "mabni" or
   CaseSignFamily.BUILDING).
7. compatibility_families is a tuple of typed enum members, never strings.
   Strings appear only in optional explanation output.
8. Matrix rank ≤ frame rank (rank ceiling theorem preserved).
9. Matrix inherits ALL frame residuals (residual inheritance preserved).
10. Every governance residual is a member of ResidualType in residuals.py.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
import uuid

from dal_core.case_signs import (
    CaseSignFamily,
    CaseSignPotential,
    CaseSignValue,
)
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.ranks import LughaRank
from dal_core.residuals import (
    Residual,
    ResidualSeverity,
    ResidualType,
    make_blocker,
    make_info,
    make_warning,
)
from dal_core.sentence_frame import SentenceFrameCandidate
from dal_core.surface_effects import SurfaceEffect


# ---------------------------------------------------------------------------
# Compatibility families (typed enum — NOT strings)
# ---------------------------------------------------------------------------


class CaseCompatibilityFamily(Enum):
    """
    عائلة التوافق الإعرابي

    Downstream interpretation family compatible with an observed surface sign.

    These are COMPATIBILITIES, not case judgments. The actual CaseEffect
    will only be produced later by a NahwOperatorRegistry once an operator
    binds to the relevant constituent. A row in `CaseSignMatrix` may declare
    that an observed sign is "compatible with rafa", but it never declares
    that the word IS marfoo'.
    """

    RAFA_COMPATIBLE = "rafa_compatible"
    NASB_COMPATIBLE = "nasb_compatible"
    JARR_COMPATIBLE = "jarr_compatible"
    JAZM_COMPATIBLE = "jazm_compatible"
    BUILDING_COMPATIBLE = "building_compatible"
    UNRESOLVED = "unresolved"


# Module-level constants used by both row __post_init__ and the builder
# to keep the building/case mutual-exclusion rule defined in one place.
_MABNI_VALUE = "mabni"
_CASE_FAMILIES: frozenset[CaseCompatibilityFamily] = frozenset(
    {
        CaseCompatibilityFamily.RAFA_COMPATIBLE,
        CaseCompatibilityFamily.NASB_COMPATIBLE,
        CaseCompatibilityFamily.JARR_COMPATIBLE,
        CaseCompatibilityFamily.JAZM_COMPATIBLE,
    }
)


# Forbidden tokens that must never appear anywhere in matrix state or
# serialization. Any of these would indicate the surface sign has been
# collapsed into a grammatical judgment (which belongs to operators only).
_FORBIDDEN_TOKENS = (
    "marfoo",
    "mansub",
    "majrur",
    "majroor",
    "majzum",
    "majzoom",
    "governed_by",
    "operator",
    "relation",
    "faail",
    "mafool",
    "mubtada",
    "khabar",
    "case_effect",
    "syntax_role",
    "marfoo_by",
    "mansub_by",
    "majroor_by",
    "majzum_by",
)


def _scan_forbidden(value: object, where: str) -> None:
    """Reject any string field carrying a case-judgment token."""
    if isinstance(value, str):
        lowered = value.lower()
        for tok in _FORBIDDEN_TOKENS:
            if tok in lowered:
                raise ValueError(
                    f"CaseSignMatrix governance violation at {where}: "
                    f"forbidden token '{tok}' in value {value!r}. "
                    f"The matrix may only carry compatibility evidence, "
                    f"never grammatical case judgments."
                )


# ---------------------------------------------------------------------------
# Layer 1: SurfaceSignObservation  (surface fact ONLY)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class SurfaceSignObservation:
    """
    رصد العلامة السطحية (Layer 1)

    A pure surface observation. Carries the observed sign and its family
    but DOES NOT decide a compatibility family. Compatibility belongs to
    Layer 2 (`CaseCompatibilityFamily`) and is computed by the builder
    from this observation plus morph evidence read from
    PreSyntaxMufradVector.

    `requires_operator` is always True at the matrix stage: by construction,
    the matrix never asserts a case; only an operator may do so later.
    """

    observed_sign: CaseSignValue
    """The specific surface sign observed (e.g. DAMMA, ALIF, NUN_DELETED)."""

    sign_family: CaseSignFamily
    """The family of the observed sign (ORIGINAL/SUBSTITUTE/BUILDING/ESTIMATED/UNRESOLVED)."""

    source_surface_effect: Optional[SurfaceEffect] = None
    """The SurfaceEffect from PreSyntaxMufradVector that backs this observation."""

    source_potential: Optional[CaseSignPotential] = None
    """The CaseSignPotential from PreSyntaxMufradVector that backs this observation."""

    requires_operator: bool = True
    """Always True: matrix never assigns a case effect."""

    requires_inflection_class: bool = False
    """Set True by the builder for substitute signs and unresolved-mabni building signs."""

    def __post_init__(self) -> None:
        # requires_operator must be True at this stage. Defensive guard.
        if self.requires_operator is not True:
            raise ValueError(
                "SurfaceSignObservation.requires_operator must be True; "
                "the matrix never produces case judgments."
            )


# ---------------------------------------------------------------------------
# Layer 2 + row: CaseSignMatrixRow
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CaseSignMatrixRow:
    """
    صف مصفوفة العلامات (one row per constituent)

    A row contains:
    - identity of the constituent (vector_id, raw_span, type_id)
    - Layer 1: surface_observations  (tuple of SurfaceSignObservation)
    - Layer 2: compatibility_families (tuple of CaseCompatibilityFamily)
    - rank and residuals
    - row_trace_id linking back to the PreSyntaxMufradVector

    Layer 1 and Layer 2 are SEPARATE fields. The row never compresses a
    surface sign directly into a case compatibility family on the same axis.

    A row never carries: operator binding, relation, syntax role, case
    effect, or any semantic / meaning field. This is enforced by both a
    field-name check and a forbidden-token scan over all string fields.
    """

    # Identity (copied from constituent vector)
    vector_id: str
    word_index: int
    raw_span: tuple[int, int]
    type_id: str

    # Layer 1 — surface
    surface_observations: tuple[SurfaceSignObservation, ...]

    # Layer 2 — compatibility (typed enum tuple; never strings)
    compatibility_families: tuple[CaseCompatibilityFamily, ...]

    # Governance
    rank: LughaRank
    residuals: tuple[Residual, ...]
    row_trace_id: str

    def __post_init__(self) -> None:
        # 1) Forbidden field names — defensive (these would belong to operators).
        forbidden_fields = {
            "case_effect",
            "operator",
            "operator_id",
            "relation",
            "relation_type",
            "syntax_role",
            "faail",
            "mafool",
            "mubtada",
            "khabar",
            "marfoo_by",
            "mansub_by",
            "majroor_by",
            "majzum_by",
            "governed_by",
            "governed_by_operator",
            "meaning",
            "semantic",
            "madlul",
            "murad",
            "haqiqa",
            "majaz",
        }
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        leaks = field_names & forbidden_fields
        if leaks:
            raise ValueError(
                f"CaseSignMatrixRow contains forbidden fields: {leaks}"
            )

        # 2) Identity must be present.
        if not self.vector_id:
            raise ValueError("CaseSignMatrixRow.vector_id is required.")
        if not self.row_trace_id:
            raise ValueError("CaseSignMatrixRow.row_trace_id is required.")
        if not isinstance(self.raw_span, tuple) or len(self.raw_span) != 2:
            raise ValueError(
                "CaseSignMatrixRow.raw_span must be a (start, end) tuple."
            )

        # 3) compatibility_families MUST be typed enum members, never strings.
        if not isinstance(self.compatibility_families, tuple):
            raise TypeError(
                "CaseSignMatrixRow.compatibility_families must be a tuple "
                "of CaseCompatibilityFamily."
            )
        for fam in self.compatibility_families:
            if not isinstance(fam, CaseCompatibilityFamily):
                raise TypeError(
                    "CaseSignMatrixRow.compatibility_families must contain "
                    "only CaseCompatibilityFamily enum members; got "
                    f"{type(fam).__name__}: {fam!r}. Strings are forbidden."
                )

        # 4) surface_observations typed and non-empty.
        if not isinstance(self.surface_observations, tuple):
            raise TypeError(
                "CaseSignMatrixRow.surface_observations must be a tuple "
                "of SurfaceSignObservation."
            )
        for obs in self.surface_observations:
            if not isinstance(obs, SurfaceSignObservation):
                raise TypeError(
                    "CaseSignMatrixRow.surface_observations must contain "
                    "only SurfaceSignObservation."
                )

        # 5) Building/case mutual-exclusion rule: a row that declares
        #    BUILDING_COMPATIBLE must NOT also declare any of the four
        #    case-compatibility families. (Building is not a case.)
        if CaseCompatibilityFamily.BUILDING_COMPATIBLE in self.compatibility_families:
            overlap = _CASE_FAMILIES.intersection(self.compatibility_families)
            if overlap:
                raise ValueError(
                    "CaseSignMatrixRow: BUILDING_COMPATIBLE cannot be "
                    f"combined with case families: {overlap}. Building "
                    "must not be mixed with case judgments."
                )

        # 6) Forbidden-token scan on string-valued fields.
        _scan_forbidden(self.vector_id, "row.vector_id")
        _scan_forbidden(self.type_id, "row.type_id")
        _scan_forbidden(self.row_trace_id, "row.row_trace_id")

    def has_blocking_residuals(self) -> bool:
        return any(r.is_blocker() for r in self.residuals)


# ---------------------------------------------------------------------------
# Matrix trace
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CaseSignMatrixTrace:
    """
    أثر مصفوفة العلامات

    Minimal but mandatory trace. Each row is recoverable to its
    PreSyntaxMufradVector by `row_vector_ids[i] == rows[i].vector_id`.
    """

    frame_id: str
    frame_trace_id: str
    row_vector_ids: tuple[str, ...]
    derivation: str = "from_sentence_frame"

    def __post_init__(self) -> None:
        if not self.frame_id:
            raise ValueError("CaseSignMatrixTrace.frame_id is required.")
        if not self.frame_trace_id:
            raise ValueError(
                "CaseSignMatrixTrace.frame_trace_id is required."
            )
        if not isinstance(self.row_vector_ids, tuple):
            raise TypeError(
                "CaseSignMatrixTrace.row_vector_ids must be a tuple."
            )
        for vid in self.row_vector_ids:
            if not isinstance(vid, str) or not vid:
                raise ValueError(
                    "CaseSignMatrixTrace.row_vector_ids must contain "
                    "non-empty strings."
                )


# ---------------------------------------------------------------------------
# Matrix
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class CaseSignMatrix:
    """
    مصفوفة علامات الإعراب

    Compatibility evidence produced from a single SentenceFrameCandidate.

    Invariants enforced in __post_init__:
    - matrix.frame_id matches the originating frame.
    - matrix.rank ≤ frame_rank (rank ceiling theorem).
    - matrix.inherited_residuals ⊇ frame.get_all_residuals()
      (residual inheritance theorem; frame residuals are never erased).
    - trace.row_vector_ids has the same length as rows and matches
      row.vector_id elementwise.
    - matrix carries NO case effect, operator, relation, or syntax role.
    """

    matrix_id: str
    frame_id: str

    rows: tuple[CaseSignMatrixRow, ...]

    rank: LughaRank
    inherited_residuals: tuple[Residual, ...]
    matrix_residuals: tuple[Residual, ...]

    trace: CaseSignMatrixTrace

    def __post_init__(self) -> None:
        # 1) Forbidden field names.
        forbidden_fields = {
            "case_effect",
            "operator",
            "operator_id",
            "relation",
            "syntax_role",
            "faail",
            "mafool",
            "mubtada",
            "khabar",
            "meaning",
            "semantic",
            "madlul",
            "murad",
        }
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        leaks = field_names & forbidden_fields
        if leaks:
            raise ValueError(
                f"CaseSignMatrix contains forbidden fields: {leaks}"
            )

        # 2) Trace ↔ rows alignment.
        if len(self.trace.row_vector_ids) != len(self.rows):
            raise ValueError(
                f"CaseSignMatrix trace.row_vector_ids length "
                f"({len(self.trace.row_vector_ids)}) does not match rows "
                f"length ({len(self.rows)})."
            )
        for i, (vid, row) in enumerate(zip(self.trace.row_vector_ids, self.rows)):
            if vid != row.vector_id:
                raise ValueError(
                    f"CaseSignMatrix trace.row_vector_ids[{i}] = {vid!r} "
                    f"!= rows[{i}].vector_id = {row.vector_id!r}."
                )

        # 3) Frame identity consistency.
        if self.frame_id != self.trace.frame_id:
            raise ValueError(
                f"CaseSignMatrix.frame_id ({self.frame_id}) does not match "
                f"trace.frame_id ({self.trace.frame_id})."
            )

        # 4) All governance residuals must be central ResidualType members.
        for r in self.inherited_residuals + self.matrix_residuals:
            if not isinstance(r.type, ResidualType):
                raise TypeError(
                    "CaseSignMatrix residuals must use central ResidualType "
                    f"taxonomy; got {type(r.type).__name__}."
                )

    # ----- public helpers -----------------------------------------------

    def get_all_residuals(self) -> tuple[Residual, ...]:
        return self.inherited_residuals + self.matrix_residuals

    def has_blocking_residuals(self) -> bool:
        return any(r.is_blocker() for r in self.get_all_residuals())

    def to_explanation(self) -> list[dict]:
        """
        Optional human-readable serialization. Strings appear ONLY here,
        never in stored state. This is the only place where compatibility
        family names are emitted as text.
        """
        out: list[dict] = []
        for row in self.rows:
            out.append(
                {
                    "vector_id": row.vector_id,
                    "word_index": row.word_index,
                    "raw_span": list(row.raw_span),
                    "type_id": row.type_id,
                    "surface_observations": [
                        {
                            "observed_sign": obs.observed_sign.name,
                            "sign_family": obs.sign_family.name,
                            "requires_operator": obs.requires_operator,
                            "requires_inflection_class": obs.requires_inflection_class,
                        }
                        for obs in row.surface_observations
                    ],
                    "compatibility_families": [
                        fam.value for fam in row.compatibility_families
                    ],
                    "rank": row.rank.name,
                    "residuals_count": len(row.residuals),
                    "row_trace_id": row.row_trace_id,
                }
            )
        return out


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def _is_mabni_by_value(vector: PreSyntaxMufradVector) -> bool:
    """
    True ONLY if the constituent has explicit *valued* evidence of being mabni.

    Per confirmation #2: `mabni_murab_status` is a `CandidateStatus`, which
    expresses *certainty* not *value*; it is not by itself proof of being
    mabni. We require either:
      - noun_inflection_class.inflection_type == "mabni"
      - some case_sign_potential with sign_family == CaseSignFamily.BUILDING
    """
    nic = vector.noun_inflection_class
    if nic is not None:
        if isinstance(nic.inflection_type, str) and nic.inflection_type.strip().lower() == _MABNI_VALUE:
            return True
    for pot in vector.case_sign_potentials:
        if pot.sign_family == CaseSignFamily.BUILDING:
            return True
    return False


def _mabni_status_resolved(vector: PreSyntaxMufradVector) -> bool:
    """True iff mabni/murab determination has been resolved (any value)."""
    from dal_core.morph_features import CandidateStatus

    return vector.mabni_murab_status in (
        CandidateStatus.RESOLVED_CERTAIN,
        CandidateStatus.RESOLVED_PROBABLE,
        CandidateStatus.NOT_APPLICABLE,
        CandidateStatus.BLOCKED,
    )


def _declension_pattern(vector: PreSyntaxMufradVector) -> Optional[str]:
    """Reserved for future use once NounInflectionClass exposes richer
    morph-class values (e.g. dual / sound-masc-plural / five-nouns).
    Currently unused: the matrix never opens substitute-sign compatibility
    from declension_pattern alone (per confirmation #1)."""
    nic = vector.noun_inflection_class
    if nic is None:
        return None
    val = nic.declension_pattern
    return val.strip().lower() if isinstance(val, str) else None


def _inflection_type(vector: PreSyntaxMufradVector) -> Optional[str]:
    """Reserved for future use; see `_declension_pattern`."""
    nic = vector.noun_inflection_class
    if nic is None:
        return None
    val = nic.inflection_type
    return val.strip().lower() if isinstance(val, str) else None


# Per-confirmation #1: we do NOT introduce new enum members for DUAL /
# FIVE_NOUNS / SOUND_MASC_PLURAL / AFAAL_KHAMSA / MAMNOO_MIN_SARF. We read
# whatever evidence is *already* explicitly present on the constituent. If
# evidence is missing, we never infer; we emit UNRESOLVED + residuals.

# The current NounInflectionClass exposes only `inflection_type` and
# `declension_pattern` (free strings). Triptote/diptote/indeclinable do not
# discriminate dual / sound-masc-plural / five-nouns, so substitute signs
# generally fall to UNRESOLVED here. That is by design and is exactly what
# the reviewer requested: do not invent compatibility without evidence.


def _families_for_original_sign(
    sign: CaseSignValue, vector: PreSyntaxMufradVector
) -> tuple[tuple[CaseCompatibilityFamily, ...], list[Residual]]:
    """
    Compatibility for ORIGINAL signs (damma/fatha/kasra/sukun).

    Building rule (confirmation #2):
      - If valued evidence proves mabni → BUILDING_COMPATIBLE only.
      - If mabni/murab status unresolved → UNRESOLVED + residuals.
      - Otherwise → the canonical case family for that diacritic.
    """
    residuals: list[Residual] = []

    if _is_mabni_by_value(vector):
        return (CaseCompatibilityFamily.BUILDING_COMPATIBLE,), residuals

    if not _mabni_status_resolved(vector):
        residuals.append(
            make_blocker(
                ResidualType.MATRIX_BUILDING_STATUS_UNRESOLVED,
                f"Cannot decide building vs case for sign {sign.name}: "
                "mabni/murab status is unresolved.",
                location=vector.mufrad_id,
            )
        )
        residuals.append(
            make_blocker(
                ResidualType.CASE_SIGN_COMPATIBILITY_UNRESOLVED,
                f"Compatibility unresolved for original sign {sign.name}.",
                location=vector.mufrad_id,
            )
        )
        return (CaseCompatibilityFamily.UNRESOLVED,), residuals

    if sign == CaseSignValue.DAMMA:
        return (CaseCompatibilityFamily.RAFA_COMPATIBLE,), residuals
    if sign == CaseSignValue.FATHA:
        return (CaseCompatibilityFamily.NASB_COMPATIBLE,), residuals
    if sign == CaseSignValue.KASRA:
        return (CaseCompatibilityFamily.JARR_COMPATIBLE,), residuals
    if sign == CaseSignValue.SUKUN:
        return (CaseCompatibilityFamily.JAZM_COMPATIBLE,), residuals

    # Defensive: any other value falls through to UNRESOLVED.
    residuals.append(
        make_warning(
            ResidualType.CASE_SIGN_COMPATIBILITY_UNRESOLVED,
            f"Original sign {sign.name} not recognized for direct mapping.",
            location=vector.mufrad_id,
        )
    )
    return (CaseCompatibilityFamily.UNRESOLVED,), residuals


def _families_for_substitute_sign(
    sign: CaseSignValue, vector: PreSyntaxMufradVector
) -> tuple[
    tuple[CaseCompatibilityFamily, ...],
    list[Residual],
    bool,  # requires_inflection_class
]:
    """
    Compatibility for SUBSTITUTE signs (ALIF/WAW/YA/NUN_*/WEAK_*).

    Per confirmation #1: do NOT infer rafa/nasb/jarr/jazm without explicit
    morph-class evidence. The current NounInflectionClass does not encode
    DUAL / SOUND_MASC_PLURAL / FIVE_NOUNS / AFAAL_KHAMSA as values, so the
    safe and correct behaviour at this stage is UNRESOLVED + residuals.

    This keeps the matrix honest: substitute signs always carry
    `requires_inflection_class = True` in their SurfaceSignObservation.
    """
    residuals: list[Residual] = [
        make_blocker(
            ResidualType.SUBSTITUTE_SIGN_REQUIRES_INFLECTION_CLASS,
            f"Substitute sign {sign.name} requires explicit morph-class "
            "evidence (e.g. dual, sound-masc-plural, five-nouns, "
            "af'aal-khamsa) before any rafa/nasb/jarr/jazm compatibility "
            "may be opened.",
            location=vector.mufrad_id,
        ),
        make_blocker(
            ResidualType.CASE_SIGN_COMPATIBILITY_UNRESOLVED,
            f"Compatibility for substitute sign {sign.name} is unresolved "
            "without morph evidence; operator may not assign case from "
            "this row alone.",
            location=vector.mufrad_id,
        ),
    ]
    return (CaseCompatibilityFamily.UNRESOLVED,), residuals, True


def _families_for_estimated_sign(
    sign: CaseSignValue,
    vector: PreSyntaxMufradVector,
    source_potential: Optional[CaseSignPotential],
) -> tuple[tuple[CaseCompatibilityFamily, ...], list[Residual]]:
    """Estimated signs require a strong trace; otherwise residual + UNRESOLVED."""
    residuals: list[Residual] = []
    trace_id = source_potential.trace_id if source_potential else ""
    if not trace_id:
        residuals.append(
            make_blocker(
                ResidualType.ESTIMATED_SIGN_REQUIRES_TRACE_IN_MATRIX,
                f"Estimated sign {sign.name} lacks trace; cannot open "
                "case compatibility.",
                location=vector.mufrad_id,
            )
        )
        residuals.append(
            make_blocker(
                ResidualType.CASE_SIGN_COMPATIBILITY_UNRESOLVED,
                f"Estimated sign {sign.name} has unresolved compatibility "
                "without trace.",
                location=vector.mufrad_id,
            )
        )
        return (CaseCompatibilityFamily.UNRESOLVED,), residuals

    # If trace exists, map ESTIMATED_DAMMA/FATHA/KASRA to their original
    # families, but ALSO route through the building-status check.
    canonical = {
        CaseSignValue.ESTIMATED_DAMMA: CaseSignValue.DAMMA,
        CaseSignValue.ESTIMATED_FATHA: CaseSignValue.FATHA,
        CaseSignValue.ESTIMATED_KASRA: CaseSignValue.KASRA,
    }.get(sign)
    if canonical is None:
        residuals.append(
            make_warning(
                ResidualType.CASE_SIGN_COMPATIBILITY_UNRESOLVED,
                f"Estimated sign {sign.name} not mappable to a canonical family.",
                location=vector.mufrad_id,
            )
        )
        return (CaseCompatibilityFamily.UNRESOLVED,), residuals
    fams, more = _families_for_original_sign(canonical, vector)
    residuals.extend(more)
    return fams, residuals


def _families_for_building_sign(
    sign: CaseSignValue, vector: PreSyntaxMufradVector
) -> tuple[tuple[CaseCompatibilityFamily, ...], list[Residual]]:
    """BUILDING family signs always produce only BUILDING_COMPATIBLE."""
    return (CaseCompatibilityFamily.BUILDING_COMPATIBLE,), []


def _row_from_potential(
    potential: CaseSignPotential, vector: PreSyntaxMufradVector
) -> tuple[SurfaceSignObservation, tuple[CaseCompatibilityFamily, ...], list[Residual]]:
    """
    Build (Layer 1 observation, Layer 2 families, residuals) for one
    CaseSignPotential observed on a constituent.
    """
    sign = potential.sign_value
    family = potential.sign_family

    if family == CaseSignFamily.BUILDING:
        fams, res = _families_for_building_sign(sign, vector)
        requires_class = False
    elif family == CaseSignFamily.ORIGINAL:
        fams, res = _families_for_original_sign(sign, vector)
        requires_class = False
    elif family == CaseSignFamily.SUBSTITUTE:
        fams, res, requires_class = _families_for_substitute_sign(sign, vector)
    elif family == CaseSignFamily.ESTIMATED:
        fams, res = _families_for_estimated_sign(sign, vector, potential)
        requires_class = False
    else:
        # UNRESOLVED / unknown family.
        res = [
            make_blocker(
                ResidualType.CASE_SIGN_COMPATIBILITY_UNRESOLVED,
                f"Sign family {family.name} for {sign.name} is unresolved.",
                location=vector.mufrad_id,
            )
        ]
        fams = (CaseCompatibilityFamily.UNRESOLVED,)
        requires_class = False

    observation = SurfaceSignObservation(
        observed_sign=sign,
        sign_family=family,
        source_surface_effect=potential.observed_surface,
        source_potential=potential,
        requires_operator=True,
        requires_inflection_class=requires_class,
    )
    return observation, fams, res


def _build_row_for_vector(
    vector: PreSyntaxMufradVector, word_index: int
) -> CaseSignMatrixRow:
    """Build one CaseSignMatrixRow from one PreSyntaxMufradVector."""
    observations: list[SurfaceSignObservation] = []
    families_acc: list[CaseCompatibilityFamily] = []
    residuals_acc: list[Residual] = []

    if not vector.case_sign_potentials:
        # No surface case sign at all → row carries UNRESOLVED + residual.
        # An operator may still produce a CaseEffect later from other
        # evidence (e.g. position), but the matrix cannot pre-decide.
        residuals_acc.append(
            make_warning(
                ResidualType.MATRIX_UNRESOLVED_REQUIRED_SIGN,
                "No CaseSignPotential present on constituent; matrix row "
                "carries UNRESOLVED.",
                location=vector.mufrad_id,
            )
        )
        residuals_acc.append(
            make_warning(
                ResidualType.CASE_SIGN_COMPATIBILITY_UNRESOLVED,
                "Compatibility unresolved: no surface sign observed.",
                location=vector.mufrad_id,
            )
        )
        families_acc.append(CaseCompatibilityFamily.UNRESOLVED)
    else:
        for potential in vector.case_sign_potentials:
            obs, fams, res = _row_from_potential(potential, vector)
            observations.append(obs)
            for fam in fams:
                if fam not in families_acc:
                    families_acc.append(fam)
            residuals_acc.extend(res)

    # Compose final families: enforce BUILDING_COMPATIBLE / case-family
    # exclusion at the row level too (defensive — also enforced by the
    # row's __post_init__).
    if CaseCompatibilityFamily.BUILDING_COMPATIBLE in families_acc:
        families_acc = [f for f in families_acc if f not in _CASE_FAMILIES]

    type_id_str: str
    if vector.type_id is not None:
        type_id_str = vector.type_id.value
    else:
        type_id_str = vector.type_value

    row = CaseSignMatrixRow(
        vector_id=vector.mufrad_id,
        word_index=word_index,
        raw_span=vector.raw_span,
        type_id=type_id_str,
        surface_observations=tuple(observations),
        compatibility_families=tuple(families_acc),
        rank=vector.final_rank,
        residuals=tuple(residuals_acc),
        row_trace_id=vector.trace_id or f"row-{vector.mufrad_id}",
    )
    return row


def build_case_sign_matrix(frame: SentenceFrameCandidate) -> CaseSignMatrix:
    """
    Build a CaseSignMatrix from a SentenceFrameCandidate.

    This is the ONLY public entry point. The input type is strictly
    `SentenceFrameCandidate`; passing anything else raises TypeError.
    """
    if not isinstance(frame, SentenceFrameCandidate):
        raise TypeError(
            "build_case_sign_matrix requires a SentenceFrameCandidate; "
            f"got {type(frame).__name__}. The matrix never consumes raw "
            "tokens or strings."
        )

    rows: list[CaseSignMatrixRow] = []
    matrix_residuals: list[Residual] = []
    min_rank = frame.frame_rank

    for i, vector in enumerate(frame.constituents):
        row = _build_row_for_vector(vector, word_index=i)
        rows.append(row)
        # Propagate row blockers into matrix-level residuals so a downstream
        # operator can see them without scanning each row.
        for r in row.residuals:
            if r.is_blocker():
                matrix_residuals.append(r)
        if row.rank.value < min_rank.value:
            min_rank = row.rank

    # Inherit ALL frame residuals (preserve residual inheritance theorem).
    inherited = frame.get_all_residuals()

    matrix_id = f"matrix-{uuid.uuid4().hex[:12]}"

    trace = CaseSignMatrixTrace(
        frame_id=frame.frame_id,
        frame_trace_id=frame.trace_id,
        row_vector_ids=tuple(r.vector_id for r in rows),
    )

    return CaseSignMatrix(
        matrix_id=matrix_id,
        frame_id=frame.frame_id,
        rows=tuple(rows),
        rank=min_rank,
        inherited_residuals=inherited,
        matrix_residuals=tuple(matrix_residuals),
        trace=trace,
    )


class CaseSignMatrixBuilder:
    """Thin OO wrapper around `build_case_sign_matrix` for symmetry with FrameBuilder."""

    def build(self, frame: SentenceFrameCandidate) -> CaseSignMatrix:
        return build_case_sign_matrix(frame)
