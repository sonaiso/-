"""
Operator Trigger Potential (محفزات العوامل المرشحة)

PR #14: Post-matrix, pre-operator candidate-family layer.

ARCHITECTURE POSITION:
    SentenceFrameCandidate + CaseSignMatrix          (input — only legal sources)
            ↓
    OperatorTriggerPotential                          (this module — typed candidate families)
            ↓
    [future] NahwOperatorRegistry → OperatorCandidate
                                  → RelationCandidate
                                  → CaseEffectCandidate

GOVERNING RULES (do NOT relax):
1. Inputs are ONLY a SentenceFrameCandidate AND its CaseSignMatrix; both must
   share the same frame_id. Anything else raises TypeError / ValueError.
2. Output is a *candidate operator FAMILY* set, NEVER:
     - a specific operator (no operator_id, no operator binding),
     - a relation (no relation_type, no ISN/TADMN/TAQYID resolution),
     - a case judgment (no marfoo_by/mansub_by/majroor_by/majzum_by),
     - a syntax role (no faail/mafool/mubtada/khabar/mudaf/mudaf_ilayh),
     - a semantic meaning (no meaning/murad/madlul/haqiqa/majaz).
3. `triggered_families` is a tuple of typed `OperatorTriggerFamily` enum
   members. Strings appear only in optional `to_explanation()` output.
4. Competing trigger families are PRESERVED, never silently resolved. If two
   families (e.g. POSSIBLE_NASIKH_INNA_FAMILY and POSSIBLE_IBTIDAA_FAMILY)
   both have evidence in the same frame, both are emitted, and a
   `TRIGGER_COMPETING_FAMILIES_PRESERVED` info residual is recorded. The
   trigger layer NEVER decides between them; that belongs to a later
   ParseCompetition / OperatorCandidate stage.
5. Rank ceiling extends: trigger.rank ≤ matrix.rank ≤ frame.frame_rank.
6. Residual inheritance extends: trigger.inherited_residuals ⊇
   matrix.get_all_residuals() ⊇ frame.get_all_residuals(). Nothing is erased.
7. Every governance residual is a member of the central ResidualType taxonomy.
8. POSSIBLE_IDAFA_FAMILY is a *construction trigger only* — it does NOT
   assert mudaf / mudaf_ilayh / idafa-relation / jarr-judgment. It only says
   "an adjacent ISM + ISM pattern with jarr-compatible sign evidence may
   later trigger an idafa-family operator/relation candidate."
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional
import uuid

from dal_core.case_sign_matrix import (
    CaseCompatibilityFamily,
    CaseSignMatrix,
)
from dal_core.ranks import LughaRank
from dal_core.residuals import (
    Residual,
    ResidualType,
    make_blocker,
    make_info,
    make_warning,
)
from dal_core.sentence_frame import (
    FragmentFrameCandidate,
    NominalFrameCandidate,
    SentenceFrameCandidate,
    UnresolvedFrameCandidate,
    VerbalFrameCandidate,
)
from dal_core.type_ids import NounTypeID, ParticleTypeID, VerbTypeID


# ---------------------------------------------------------------------------
# Operator trigger families (typed enum — NOT strings)
# ---------------------------------------------------------------------------


class OperatorTriggerFamily(Enum):
    """
    عائلة محفز العامل

    A typed candidate family expressing "some operator from this family MAY
    later apply to this frame". Never identifies a specific operator, never
    binds a constituent, never produces a case effect.
    """

    POSSIBLE_JARR_OPERATOR_FAMILY = "possible_jarr_operator_family"
    POSSIBLE_NASB_OPERATOR_FAMILY = "possible_nasb_operator_family"
    POSSIBLE_JAZM_OPERATOR_FAMILY = "possible_jazm_operator_family"
    POSSIBLE_NASIKH_INNA_FAMILY = "possible_nasikh_inna_family"
    POSSIBLE_NASIKH_LA_LILJINS_FAMILY = "possible_nasikh_la_liljins_family"
    POSSIBLE_NIDA_FAMILY = "possible_nida_family"
    POSSIBLE_ATF_FAMILY = "possible_atf_family"
    POSSIBLE_NAFI_FAMILY = "possible_nafi_family"
    POSSIBLE_ISTIFHAM_FAMILY = "possible_istifham_family"
    POSSIBLE_VERBAL_GOVERNANCE_FAMILY = "possible_verbal_governance_family"
    POSSIBLE_IBTIDAA_FAMILY = "possible_ibtidaa_family"
    POSSIBLE_IDAFA_FAMILY = "possible_idafa_family"
    UNRESOLVED_TRIGGER = "unresolved_trigger"


# Particle → trigger family mapping. Kept module-level so both the builder
# and external readers can introspect the same table without duplication.
_PARTICLE_FAMILY_MAP: dict[ParticleTypeID, OperatorTriggerFamily] = {
    ParticleTypeID.HARF_JARR: OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
    ParticleTypeID.HARF_NASB: OperatorTriggerFamily.POSSIBLE_NASB_OPERATOR_FAMILY,
    ParticleTypeID.HARF_JAZM: OperatorTriggerFamily.POSSIBLE_JAZM_OPERATOR_FAMILY,
    ParticleTypeID.HARF_NASIKH_INNA: OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY,
    ParticleTypeID.HARF_NASIKH_LA_NAFI_LILJINS: OperatorTriggerFamily.POSSIBLE_NASIKH_LA_LILJINS_FAMILY,
    ParticleTypeID.HARF_NIDA: OperatorTriggerFamily.POSSIBLE_NIDA_FAMILY,
    ParticleTypeID.HARF_ATF: OperatorTriggerFamily.POSSIBLE_ATF_FAMILY,
    ParticleTypeID.HARF_NAFI: OperatorTriggerFamily.POSSIBLE_NAFI_FAMILY,
    ParticleTypeID.HARF_ISTIFHAM: OperatorTriggerFamily.POSSIBLE_ISTIFHAM_FAMILY,
}


# Forbidden tokens — same governance bar as PR #13. Any string that would
# encode an operator binding, relation, case judgment, syntax role, or
# meaning must never appear inside a trigger artifact's stored state.
_FORBIDDEN_TOKENS: tuple[str, ...] = (
    "marfoo",
    "mansub",
    "majrur",
    "majroor",
    "majzum",
    "majzoom",
    "governed_by",
    "operator_id",
    "operator_binding",
    "relation_type",
    "faail",
    "mafool",
    "mubtada",
    "khabar",
    "mudaf",
    "mudaf_ilayh",
    "case_effect",
    "syntax_role",
    "marfoo_by",
    "mansub_by",
    "majroor_by",
    "majzum_by",
    "meaning",
    "madlul",
    "murad",
    "haqiqa",
    "majaz",
)


# Forbidden dataclass field names. Field absence (per dal_core convention),
# not None values, is what enforces the contract.
_FORBIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "operator",
        "operator_id",
        "operator_binding",
        "relation",
        "relation_type",
        "case_effect",
        "syntax_role",
        "faail",
        "mafool",
        "mubtada",
        "khabar",
        "mudaf",
        "mudaf_ilayh",
        "naat",
        "badal",
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
)


def _scan_forbidden(value: object, where: str) -> None:
    """Reject any string field carrying an operator-or-judgment token."""
    if isinstance(value, str):
        lowered = value.lower()
        for tok in _FORBIDDEN_TOKENS:
            if tok in lowered:
                raise ValueError(
                    f"OperatorTriggerPotential governance violation at "
                    f"{where}: forbidden token '{tok}' in value {value!r}. "
                    f"The trigger layer may only carry candidate operator "
                    f"FAMILIES, never operators, relations, case effects, "
                    f"syntax roles, or meaning."
                )


# ---------------------------------------------------------------------------
# TriggerSource (one fact, flat tuple, full trace)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TriggerSource:
    """
    مصدر محفز العامل

    A single audit-trail record explaining *why* a trigger family was
    emitted. Pure pointer; no grammatical decision. The proof object stores
    these in a flat tuple — one source per fact — so that the same family
    may legitimately appear in multiple sources without losing per-source
    trace.
    """

    family: OperatorTriggerFamily
    """The candidate trigger family this source attests to."""

    frame_index: int
    """Index of the constituent inside `frame.constituents`."""

    vector_id: str
    """`PreSyntaxMufradVector.mufrad_id` of the triggering constituent."""

    matrix_row_index: Optional[int]
    """
    Matching `CaseSignMatrix.rows` index, or None when the trigger is
    purely particle-typed and does not consult the matrix row contents.
    """

    triggering_type_id: str
    """Symbolic name of the constituent type (e.g. 'HARF_JARR', 'FIIL_MUDARI', 'ISM_COMMON')."""

    compatibility_evidence: tuple[CaseCompatibilityFamily, ...]
    """
    The matrix row's compatibility families consulted for this trigger.
    Empty tuple when matrix_row_index is None or when the row carried no
    compatibility evidence.
    """

    source_trace_id: str
    """Trace id, normally the originating matrix row's `row_trace_id`."""

    def __post_init__(self) -> None:
        if not isinstance(self.family, OperatorTriggerFamily):
            raise TypeError(
                "TriggerSource.family must be an OperatorTriggerFamily "
                f"enum member; got {type(self.family).__name__}."
            )
        if not isinstance(self.compatibility_evidence, tuple):
            raise TypeError(
                "TriggerSource.compatibility_evidence must be a tuple of "
                "CaseCompatibilityFamily."
            )
        for fam in self.compatibility_evidence:
            if not isinstance(fam, CaseCompatibilityFamily):
                raise TypeError(
                    "TriggerSource.compatibility_evidence must contain "
                    "only CaseCompatibilityFamily enum members; got "
                    f"{type(fam).__name__}. Strings are forbidden."
                )
        if not self.vector_id:
            raise ValueError("TriggerSource.vector_id is required.")
        if not self.triggering_type_id:
            raise ValueError("TriggerSource.triggering_type_id is required.")
        if not self.source_trace_id:
            raise ValueError("TriggerSource.source_trace_id is required.")
        if self.matrix_row_index is not None and self.matrix_row_index < 0:
            raise ValueError(
                "TriggerSource.matrix_row_index must be >= 0 when set."
            )
        if self.frame_index < 0:
            raise ValueError("TriggerSource.frame_index must be >= 0.")
        # Forbidden field-name leak check (defensive)
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        leaks = field_names & _FORBIDDEN_FIELDS
        if leaks:
            raise ValueError(
                f"TriggerSource contains forbidden fields: {leaks}"
            )
        # Forbidden-token scan on all string fields.
        _scan_forbidden(self.vector_id, "source.vector_id")
        _scan_forbidden(self.triggering_type_id, "source.triggering_type_id")
        _scan_forbidden(self.source_trace_id, "source.source_trace_id")


# ---------------------------------------------------------------------------
# OperatorTriggerTrace
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OperatorTriggerTrace:
    """
    أثر محفزات العوامل

    Minimal mandatory trace. Each trigger object is recoverable backward
    to (a) the originating `SentenceFrameCandidate` (via `frame_trace_id`)
    and (b) the consumed `CaseSignMatrix` (via `matrix_id` /
    `matrix_trace_id`), and through those to the source MufradProofs.
    """

    frame_id: str
    frame_trace_id: str
    matrix_id: str
    matrix_trace_id: str
    derivation: str = "from_case_sign_matrix"

    def __post_init__(self) -> None:
        if not self.frame_id:
            raise ValueError("OperatorTriggerTrace.frame_id is required.")
        if not self.frame_trace_id:
            raise ValueError(
                "OperatorTriggerTrace.frame_trace_id is required."
            )
        if not self.matrix_id:
            raise ValueError("OperatorTriggerTrace.matrix_id is required.")
        if not self.matrix_trace_id:
            raise ValueError(
                "OperatorTriggerTrace.matrix_trace_id is required."
            )
        _scan_forbidden(self.frame_id, "trace.frame_id")
        _scan_forbidden(self.frame_trace_id, "trace.frame_trace_id")
        _scan_forbidden(self.matrix_id, "trace.matrix_id")
        _scan_forbidden(self.matrix_trace_id, "trace.matrix_trace_id")
        _scan_forbidden(self.derivation, "trace.derivation")


# ---------------------------------------------------------------------------
# OperatorTriggerPotential
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OperatorTriggerPotential:
    """
    محفزات العوامل المرشحة

    Candidate operator FAMILY potentials produced from a single
    (SentenceFrameCandidate, CaseSignMatrix) pair. Carries:
      - typed `triggered_families` (deduped, deterministic order),
      - flat `sources` tuple (one TriggerSource per fact),
      - rank ≤ matrix.rank (rank ceiling chain),
      - inherited residuals (superset of matrix residuals),
      - trigger-specific residuals (new at this stage only),
      - trace recoverable to the frame and matrix.

    Invariants enforced in `__post_init__`:
      1. No forbidden dataclass field names.
      2. `frame_id == trace.frame_id` and `matrix_id == trace.matrix_id`.
      3. `rank.value ≤` every source's matrix row rank is *not* re-derived
         here (the builder is the single source of truth for rank); but
         residual inheritance and the central-taxonomy check are enforced.
      4. All residuals (inherited + trigger) use central `ResidualType`.
      5. Every `triggered_families` entry is reachable from at least one
         `TriggerSource` (no orphan families).
      6. Every `TriggerSource.matrix_row_index` (when set) is in range.
      7. Forbidden-token scan on `trigger_id`, `frame_id`, `matrix_id`.
      8. Competing families are PRESERVED — there is NO post-construction
         pruning of families based on perceived strength. The invariant
         is structural: any two distinct families both reachable from
         sources MUST both appear in `triggered_families`.
    """

    trigger_id: str
    frame_id: str
    matrix_id: str

    triggered_families: tuple[OperatorTriggerFamily, ...]
    sources: tuple[TriggerSource, ...]

    rank: LughaRank
    inherited_residuals: tuple[Residual, ...]
    trigger_residuals: tuple[Residual, ...]

    trace: OperatorTriggerTrace

    def __post_init__(self) -> None:
        # 1) Forbidden field-name check (defensive).
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        leaks = field_names & _FORBIDDEN_FIELDS
        if leaks:
            raise ValueError(
                f"OperatorTriggerPotential contains forbidden fields: {leaks}"
            )

        # 2) Required ids non-empty.
        if not self.trigger_id:
            raise ValueError("OperatorTriggerPotential.trigger_id is required.")
        if not self.frame_id:
            raise ValueError("OperatorTriggerPotential.frame_id is required.")
        if not self.matrix_id:
            raise ValueError(
                "OperatorTriggerPotential.matrix_id is required."
            )

        # 3) trace ↔ self id consistency.
        if self.frame_id != self.trace.frame_id:
            raise ValueError(
                f"OperatorTriggerPotential.frame_id ({self.frame_id}) does "
                f"not match trace.frame_id ({self.trace.frame_id})."
            )
        if self.matrix_id != self.trace.matrix_id:
            raise ValueError(
                f"OperatorTriggerPotential.matrix_id ({self.matrix_id}) "
                f"does not match trace.matrix_id ({self.trace.matrix_id})."
            )

        # 4) triggered_families typed enum tuple.
        if not isinstance(self.triggered_families, tuple):
            raise TypeError(
                "OperatorTriggerPotential.triggered_families must be a "
                "tuple of OperatorTriggerFamily."
            )
        for fam in self.triggered_families:
            if not isinstance(fam, OperatorTriggerFamily):
                raise TypeError(
                    "OperatorTriggerPotential.triggered_families must "
                    "contain only OperatorTriggerFamily enum members; got "
                    f"{type(fam).__name__}: {fam!r}. Strings are forbidden."
                )
        # Deduplication invariant: the stored tuple itself must be unique.
        if len(set(self.triggered_families)) != len(self.triggered_families):
            raise ValueError(
                "OperatorTriggerPotential.triggered_families must be "
                "deduplicated."
            )

        # 5) sources typed tuple.
        if not isinstance(self.sources, tuple):
            raise TypeError(
                "OperatorTriggerPotential.sources must be a tuple of "
                "TriggerSource."
            )
        for src in self.sources:
            if not isinstance(src, TriggerSource):
                raise TypeError(
                    "OperatorTriggerPotential.sources must contain only "
                    "TriggerSource."
                )

        # 6) Every triggered family must be reachable from at least one
        #    source. This together with the no-pruning rule implements the
        #    "preserve competing families" invariant.
        source_families = {src.family for src in self.sources}
        unreachable = set(self.triggered_families) - source_families
        if unreachable:
            raise ValueError(
                "OperatorTriggerPotential.triggered_families contains "
                f"families with no supporting source: {unreachable}."
            )
        # Symmetric: every family attested by a source MUST be in
        # triggered_families. This forbids silent suppression of a competing
        # family at construction time.
        missing = source_families - set(self.triggered_families)
        if missing:
            raise ValueError(
                "OperatorTriggerPotential silently dropped attested "
                f"competing families: {missing}. Competing trigger families "
                "must be preserved; resolution belongs to a later stage."
            )

        # 7) All residuals must use central ResidualType taxonomy.
        for r in self.inherited_residuals + self.trigger_residuals:
            if not isinstance(r.type, ResidualType):
                raise TypeError(
                    "OperatorTriggerPotential residuals must use central "
                    f"ResidualType taxonomy; got {type(r.type).__name__}."
                )

        # 8) Forbidden-token scan on string identity fields.
        _scan_forbidden(self.trigger_id, "trigger.trigger_id")
        _scan_forbidden(self.frame_id, "trigger.frame_id")
        _scan_forbidden(self.matrix_id, "trigger.matrix_id")

    # ----- public helpers -----------------------------------------------

    def get_all_residuals(self) -> tuple[Residual, ...]:
        return self.inherited_residuals + self.trigger_residuals

    def has_blocking_residuals(self) -> bool:
        return any(r.is_blocker() for r in self.get_all_residuals())

    def families_for_row(self, row_index: int) -> tuple[OperatorTriggerFamily, ...]:
        """All families attested by any source whose matrix_row_index == row_index."""
        out: list[OperatorTriggerFamily] = []
        for src in self.sources:
            if src.matrix_row_index == row_index and src.family not in out:
                out.append(src.family)
        return tuple(out)

    def sources_by_family(self) -> dict[OperatorTriggerFamily, tuple[TriggerSource, ...]]:
        """
        Helper grouping (per clarification #3): the proof object stores
        sources flat; this helper computes the grouping on demand.
        """
        grouped: dict[OperatorTriggerFamily, list[TriggerSource]] = {}
        for src in self.sources:
            grouped.setdefault(src.family, []).append(src)
        return {fam: tuple(srcs) for fam, srcs in grouped.items()}

    def to_explanation(self) -> list[dict]:
        """
        Optional human-readable serialization. Strings appear ONLY here,
        never in stored state. This is the only place where family names
        are emitted as text.
        """
        return [
            {
                "family": src.family.value,
                "frame_index": src.frame_index,
                "vector_id": src.vector_id,
                "matrix_row_index": src.matrix_row_index,
                "triggering_type_id": src.triggering_type_id,
                "compatibility_evidence": [
                    f.value for f in src.compatibility_evidence
                ],
                "source_trace_id": src.source_trace_id,
            }
            for src in self.sources
        ]


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def _is_noun(vector) -> bool:  # type: ignore[no-untyped-def]
    return isinstance(vector.type_id, NounTypeID)


def _is_verb(vector) -> bool:  # type: ignore[no-untyped-def]
    return isinstance(vector.type_id, VerbTypeID)


def _is_particle(vector) -> bool:  # type: ignore[no-untyped-def]
    return isinstance(vector.type_id, ParticleTypeID)


def _type_id_name(vector) -> str:  # type: ignore[no-untyped-def]
    """Symbolic type id name; falls back to type_value when type_id is None."""
    if vector.type_id is not None:
        return vector.type_id.name
    return vector.type_value or "UNKNOWN"


def build_operator_trigger_potential(
    frame: SentenceFrameCandidate,
    matrix: CaseSignMatrix,
) -> OperatorTriggerPotential:
    """
    Build an OperatorTriggerPotential from a (frame, matrix) pair.

    This is the ONLY public entry point. Strict input typing:
      - `frame` must be a `SentenceFrameCandidate`,
      - `matrix` must be a `CaseSignMatrix`,
      - both must share `frame_id`.

    The builder NEVER:
      - applies an operator,
      - assigns a syntax role,
      - produces a case effect or relation,
      - suppresses a competing trigger family.

    The builder MAY:
      - emit multiple competing families when evidence supports them,
      - emit `UNRESOLVED_TRIGGER` only when no other family is supported,
      - propagate matrix blockers as trigger residuals.
    """
    # 1) Strict input typing.
    if not isinstance(frame, SentenceFrameCandidate):
        raise TypeError(
            "build_operator_trigger_potential requires a "
            "SentenceFrameCandidate as the first argument; got "
            f"{type(frame).__name__}. The trigger layer never consumes raw "
            "tokens or strings."
        )
    if not isinstance(matrix, CaseSignMatrix):
        raise TypeError(
            "build_operator_trigger_potential requires a CaseSignMatrix "
            f"as the second argument; got {type(matrix).__name__}."
        )

    # 2) Frame identity consistency.
    if frame.frame_id != matrix.frame_id:
        raise ValueError(
            f"frame.frame_id ({frame.frame_id}) does not match "
            f"matrix.frame_id ({matrix.frame_id}). The trigger layer "
            "operates on a single (frame, matrix) pair."
        )

    # 3) Empty frame guard (frame builders already prevent this, but keep
    #    a symmetric defensive check).
    if not frame.constituents:
        raise ValueError(
            "build_operator_trigger_potential requires a non-empty frame."
        )

    sources: list[TriggerSource] = []
    trigger_residuals: list[Residual] = []

    # Pre-compute per-row compatibility evidence (kept aligned with
    # frame.constituents — the matrix layer guarantees row[i] ↔ constituent[i]
    # via row_vector_ids).
    rows = matrix.rows

    # -----------------------------------------------------------------
    # Pass 1: per-constituent particle / verb / nominal-lead triggers.
    # -----------------------------------------------------------------
    for i, constituent in enumerate(frame.constituents):
        row = rows[i] if i < len(rows) else None
        compat = row.compatibility_families if row is not None else ()
        trace_id = (
            row.row_trace_id
            if row is not None
            else (constituent.trace_id or f"vec-{constituent.mufrad_id}")
        )

        # (a) Particle triggers — read constituent's type_id only.
        if _is_particle(constituent):
            family = _PARTICLE_FAMILY_MAP.get(constituent.type_id)
            if family is not None:
                sources.append(
                    TriggerSource(
                        family=family,
                        frame_index=i,
                        vector_id=constituent.mufrad_id,
                        matrix_row_index=i if row is not None else None,
                        triggering_type_id=_type_id_name(constituent),
                        compatibility_evidence=compat,
                        source_trace_id=trace_id,
                    )
                )
            elif constituent.type_id == ParticleTypeID.HARF_UNRESOLVED:
                trigger_residuals.append(
                    make_warning(
                        ResidualType.TRIGGER_PARTICLE_TYPE_UNRESOLVED,
                        f"Particle at index {i} has unresolved type_id; "
                        "no specific trigger family emitted.",
                        location=constituent.mufrad_id,
                    )
                )
            # Other ParticleTypeID values (e.g. HARF_IBTIDA, HARF_TAFSIR)
            # do not map to operator families in this PR; they are
            # silently no-op at the trigger layer (later PRs may add
            # families without changing the contract).

    # (b) Verbal-frame governance trigger — once, on verb_index.
    if isinstance(frame, VerbalFrameCandidate):
        vi = frame.verb_index
        if 0 <= vi < len(frame.constituents):
            verb = frame.constituents[vi]
            row = rows[vi] if vi < len(rows) else None
            compat = row.compatibility_families if row is not None else ()
            trace_id = (
                row.row_trace_id
                if row is not None
                else (verb.trace_id or f"vec-{verb.mufrad_id}")
            )
            sources.append(
                TriggerSource(
                    family=OperatorTriggerFamily.POSSIBLE_VERBAL_GOVERNANCE_FAMILY,
                    frame_index=vi,
                    vector_id=verb.mufrad_id,
                    matrix_row_index=vi if row is not None else None,
                    triggering_type_id=_type_id_name(verb),
                    compatibility_evidence=compat,
                    source_trace_id=trace_id,
                )
            )

    # (c) Nominal-frame ibtidaa trigger — on lead_noun_index. Per
    #     clarification #2, this is NOT suppressed by the presence of a
    #     preceding nasikh / operator-bearing particle. Competing families
    #     are preserved; resolution is the next stage's job.
    if isinstance(frame, NominalFrameCandidate):
        li = frame.lead_noun_index
        if 0 <= li < len(frame.constituents):
            lead = frame.constituents[li]
            row = rows[li] if li < len(rows) else None
            compat = row.compatibility_families if row is not None else ()
            trace_id = (
                row.row_trace_id
                if row is not None
                else (lead.trace_id or f"vec-{lead.mufrad_id}")
            )
            sources.append(
                TriggerSource(
                    family=OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY,
                    frame_index=li,
                    vector_id=lead.mufrad_id,
                    matrix_row_index=li if row is not None else None,
                    triggering_type_id=_type_id_name(lead),
                    compatibility_evidence=compat,
                    source_trace_id=trace_id,
                )
            )

    # (d) Idafa trigger — adjacent ISM + ISM with jarr-compatible evidence
    #     on the second. CONSTRUCTION TRIGGER ONLY (per clarification #1):
    #     it does NOT assert mudaf / mudaf_ilayh / idafa-relation /
    #     jarr-judgment.
    for i in range(len(frame.constituents) - 1):
        first = frame.constituents[i]
        second = frame.constituents[i + 1]
        if not (_is_noun(first) and _is_noun(second)):
            continue
        row_second = rows[i + 1] if (i + 1) < len(rows) else None
        if row_second is None:
            continue
        if CaseCompatibilityFamily.JARR_COMPATIBLE not in row_second.compatibility_families:
            continue
        sources.append(
            TriggerSource(
                family=OperatorTriggerFamily.POSSIBLE_IDAFA_FAMILY,
                frame_index=i + 1,
                vector_id=second.mufrad_id,
                matrix_row_index=i + 1,
                triggering_type_id=_type_id_name(second),
                compatibility_evidence=row_second.compatibility_families,
                source_trace_id=row_second.row_trace_id,
            )
        )

    # -----------------------------------------------------------------
    # Pass 2: frame-level fallbacks (unresolved / fragment-empty).
    # -----------------------------------------------------------------
    if isinstance(frame, UnresolvedFrameCandidate):
        # An unresolved frame yields no specific family; record an
        # UNRESOLVED_TRIGGER source pointing at the lead constituent and a
        # blocker residual. Any per-constituent triggers from Pass 1 are
        # preserved (competing families rule), but the frame-level blocker
        # warns the consumer that the frame structure itself is unresolved.
        head = frame.constituents[0]
        row = rows[0] if rows else None
        compat = row.compatibility_families if row is not None else ()
        trace_id = (
            row.row_trace_id
            if row is not None
            else (head.trace_id or f"vec-{head.mufrad_id}")
        )
        sources.append(
            TriggerSource(
                family=OperatorTriggerFamily.UNRESOLVED_TRIGGER,
                frame_index=0,
                vector_id=head.mufrad_id,
                matrix_row_index=0 if row is not None else None,
                triggering_type_id=_type_id_name(head),
                compatibility_evidence=compat,
                source_trace_id=trace_id,
            )
        )
        trigger_residuals.append(
            make_blocker(
                ResidualType.TRIGGER_UNRESOLVED_FRAME,
                "Unresolved frame; no concrete operator trigger family "
                "can be emitted from frame structure alone.",
                location=frame.frame_id,
            )
        )

    if isinstance(frame, FragmentFrameCandidate) and not sources:
        # Fragment that fired no rule above — emit UNRESOLVED_TRIGGER once
        # and a WARNING (not blocker) residual.
        head = frame.constituents[0]
        row = rows[0] if rows else None
        compat = row.compatibility_families if row is not None else ()
        trace_id = (
            row.row_trace_id
            if row is not None
            else (head.trace_id or f"vec-{head.mufrad_id}")
        )
        sources.append(
            TriggerSource(
                family=OperatorTriggerFamily.UNRESOLVED_TRIGGER,
                frame_index=0,
                vector_id=head.mufrad_id,
                matrix_row_index=0 if row is not None else None,
                triggering_type_id=_type_id_name(head),
                compatibility_evidence=compat,
                source_trace_id=trace_id,
            )
        )
        trigger_residuals.append(
            make_warning(
                ResidualType.TRIGGER_FRAGMENT_NO_FAMILY,
                "Fragment frame triggered no operator family; emitting "
                "UNRESOLVED_TRIGGER as the only candidate.",
                location=frame.frame_id,
            )
        )

    # If after both passes nothing was emitted (e.g. nominal frame whose
    # head is a noun but no trigger rule fired and no fragment fallback
    # applied), record an UNRESOLVED_TRIGGER so the proof object is never
    # source-less. This keeps the invariant: triggered_families ≠ ().
    if not sources:
        head = frame.constituents[0]
        row = rows[0] if rows else None
        compat = row.compatibility_families if row is not None else ()
        trace_id = (
            row.row_trace_id
            if row is not None
            else (head.trace_id or f"vec-{head.mufrad_id}")
        )
        sources.append(
            TriggerSource(
                family=OperatorTriggerFamily.UNRESOLVED_TRIGGER,
                frame_index=0,
                vector_id=head.mufrad_id,
                matrix_row_index=0 if row is not None else None,
                triggering_type_id=_type_id_name(head),
                compatibility_evidence=compat,
                source_trace_id=trace_id,
            )
        )
        trigger_residuals.append(
            make_warning(
                ResidualType.TRIGGER_FRAGMENT_NO_FAMILY,
                "No trigger family could be derived from frame structure; "
                "emitting UNRESOLVED_TRIGGER.",
                location=frame.frame_id,
            )
        )

    # -----------------------------------------------------------------
    # Dedup families preserving insertion order (PRESERVES competition).
    # -----------------------------------------------------------------
    families_ordered: list[OperatorTriggerFamily] = []
    for src in sources:
        if src.family not in families_ordered:
            families_ordered.append(src.family)

    # Competing-families info residual (per new invariant #5): if two or
    # more *distinct, non-UNRESOLVED* families are present, record an INFO
    # residual making the competition explicit in the trace.
    non_unresolved = [
        f for f in families_ordered if f is not OperatorTriggerFamily.UNRESOLVED_TRIGGER
    ]
    if len(non_unresolved) >= 2:
        trigger_residuals.append(
            make_info(
                ResidualType.TRIGGER_COMPETING_FAMILIES_PRESERVED,
                "Multiple candidate operator families preserved without "
                f"resolution: {[f.value for f in non_unresolved]}. "
                "Resolution belongs to a later ParseCompetition / "
                "OperatorCandidate stage.",
                location=frame.frame_id,
            )
        )

    # -----------------------------------------------------------------
    # Matrix-blocker propagation: keep the families, but loudly mark that
    # the matrix carries blockers an operator stage will need to address.
    # -----------------------------------------------------------------
    matrix_blockers = tuple(
        r for r in matrix.get_all_residuals() if r.is_blocker()
    )
    if matrix_blockers:
        # Per-family warning so a downstream operator stage can see why
        # each candidate family is at risk without scanning the whole
        # residual list.
        for fam in families_ordered:
            trigger_residuals.append(
                make_warning(
                    ResidualType.TRIGGER_BLOCKED_BY_MATRIX_RESIDUAL,
                    f"Trigger family {fam.name} emitted with upstream "
                    f"blocking residuals from the matrix "
                    f"({len(matrix_blockers)} blocker(s)).",
                    location=frame.frame_id,
                )
            )

    # -----------------------------------------------------------------
    # Inherit ALL matrix residuals (preserves residual inheritance theorem).
    # -----------------------------------------------------------------
    inherited = matrix.get_all_residuals()

    # Rank ceiling: trigger.rank = min(matrix.rank, min over sources of
    # their matrix-row rank). Bounded above by matrix.rank.
    rank = matrix.rank
    for src in sources:
        if src.matrix_row_index is not None and src.matrix_row_index < len(rows):
            row_rank = rows[src.matrix_row_index].rank
            if row_rank.value < rank.value:
                rank = row_rank

    trigger_id = f"trigger-{uuid.uuid4().hex[:12]}"
    trace = OperatorTriggerTrace(
        frame_id=frame.frame_id,
        frame_trace_id=frame.trace_id,
        matrix_id=matrix.matrix_id,
        matrix_trace_id=matrix.trace.frame_trace_id,
    )

    return OperatorTriggerPotential(
        trigger_id=trigger_id,
        frame_id=frame.frame_id,
        matrix_id=matrix.matrix_id,
        triggered_families=tuple(families_ordered),
        sources=tuple(sources),
        rank=rank,
        inherited_residuals=inherited,
        trigger_residuals=tuple(trigger_residuals),
        trace=trace,
    )


class OperatorTriggerPotentialBuilder:
    """Thin OO wrapper around `build_operator_trigger_potential` for
    symmetry with `FrameBuilder` and `CaseSignMatrixBuilder`."""

    def build(
        self,
        frame: SentenceFrameCandidate,
        matrix: CaseSignMatrix,
    ) -> OperatorTriggerPotential:
        return build_operator_trigger_potential(frame, matrix)
