"""
Nahw Operator Registry (سجل العوامل النحوية)

PR #15: Post-trigger, pre-operator typed entries lookup layer.

ARCHITECTURE POSITION:
    SentenceFrameCandidate + CaseSignMatrix
            ↓
    OperatorTriggerPotential                  (PR #14 — typed candidate families)
            ↓
    NahwOperatorRegistry                      (this module — typed operator ENTRIES)
            ↓
    [future] OperatorCandidate → RelationCandidate → CaseEffectCandidate

GOVERNING RULES (do NOT relax):

1. The registry is a *read-only catalogue* of documented operator entries.
   It NEVER:
     - applies an operator,
     - binds an operator to constituents,
     - resolves competition between operator entries inside a family,
     - resolves competition between trigger families,
     - produces an OperatorCandidate / RelationCandidate / CaseEffect /
       CaseEffectCandidate,
     - assigns syntax roles (faail / mafool / mubtada / khabar / mudaf /
       mudaf_ilayh / naat / badal),
     - asserts meaning (meaning / murad / madlul / haqiqa / majaz).

2. Lookup keyed by `OperatorTriggerFamily`. Every entry stores:
       operator_id, display_name_ar, source, school, rank, family,
       input_signature, activation_conditions, blocking_conditions,
       expected_relation_families, case_effect_policy_families,
       citations, entry_residuals, entry_trace_id.

3. `expected_relation_families` and `case_effect_policy_families` are
   typed Enum *families* — never a specific relation type and never a
   specific case effect. The registry documents *what kind* of effect an
   operator from this family is *expected to invoke*, not what it does.

4. `activation_conditions` and `blocking_conditions` are typed Enums
   describing context conditions; the registry NEVER evaluates them. They
   are descriptive metadata for later stages.

5. Competing entries inside the same family are PRESERVED. Multiple
   entries in `entries_for_family(...)` is normal and intentional.

6. The IDAFA entry is a *construction operator only*: it MUST NOT carry
   any case-effect policy family that would assert jarr-judgment on the
   mudaf-ilayh. The policy family for IDAFA is `NO_CASE_EFFECT_POLICY_FAMILY`
   (the case effect belongs to a later layer).
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Optional

from dal_core.operator_trigger import OperatorTriggerFamily, OperatorTriggerPotential
from dal_core.ranks import LughaRank
from dal_core.residuals import (
    Residual,
    ResidualType,
    make_info,
    make_warning,
)


# ---------------------------------------------------------------------------
# Forbidden field / token guard (mirrors operator_trigger.py)
# ---------------------------------------------------------------------------

_FORBIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "operator_binding",
        "operator_id_resolved",
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


# ---------------------------------------------------------------------------
# Typed Enums (descriptive metadata only — NO evaluation here)
# ---------------------------------------------------------------------------


class OperatorSource(Enum):
    """مصدر تثبيت العامل في كلام العرب."""

    QURAN = "quran"
    HADITH = "hadith"
    KALAAM_ARAB = "kalaam_arab"
    KITAB_SIBAWAYH = "kitab_sibawayh"
    MUFASSAL = "mufassal"
    KHASAIS = "khasais"
    OTHER = "other"


class NahwSchool(Enum):
    """المدرسة النحوية."""

    BASRI = "basri"
    KUFI = "kufi"
    BAGHDADI = "baghdadi"
    ANDALUSI = "andalusi"
    SHARED = "shared"
    UNATTRIBUTED = "unattributed"


class ExpectedRelationFamily(Enum):
    """
    عائلة العلاقة المتوقعة.

    Documents the *kind* of relation an operator from this family is
    expected to eventually invoke (e.g. an ISN-like attachment, an
    idafa-like construction). NEVER a specific RelationCandidate.
    """

    ISN_LIKE = "isn_like"
    TADMN_LIKE = "tadmn_like"
    TAQYID_LIKE = "taqyid_like"
    IDAFA_LIKE = "idafa_like"
    ATF_LIKE = "atf_like"
    NIDA_LIKE = "nida_like"
    UNRESOLVED_EXPECTED_RELATION = "unresolved_expected_relation"


class CaseEffectPolicyFamily(Enum):
    """
    عائلة سياسة الأثر الإعرابي.

    Documents the *kind* of case-effect policy an operator from this
    family is expected to apply (e.g. rafa-policy, nasb-policy, mixed
    rafa+nasb for kana/inna families). NEVER an actual CaseEffect.
    """

    RAFI_POLICY_FAMILY = "rafi_policy_family"
    NASB_POLICY_FAMILY = "nasb_policy_family"
    JARR_POLICY_FAMILY = "jarr_policy_family"
    JAZM_POLICY_FAMILY = "jazm_policy_family"
    MIXED_RAFI_NASB_POLICY_FAMILY = "mixed_rafi_nasb_policy_family"
    NO_CASE_EFFECT_POLICY_FAMILY = "no_case_effect_policy_family"


class ActivationCondition(Enum):
    """
    شرط تفعيل العامل.

    Descriptive metadata only — the registry NEVER evaluates these.
    """

    IMMEDIATELY_PRECEDES_ISM = "immediately_precedes_ism"
    IMMEDIATELY_PRECEDES_FIIL_MUDARI = "immediately_precedes_fiil_mudari"
    IMMEDIATELY_PRECEDES_NOMINAL_FRAME = "immediately_precedes_nominal_frame"
    LEADS_FRAME = "leads_frame"
    ADJACENT_TO_ANOTHER_ISM = "adjacent_to_another_ism"
    HEADS_VERBAL_FRAME = "heads_verbal_frame"
    HEADS_NOMINAL_FRAME = "heads_nominal_frame"


class BlockingCondition(Enum):
    """
    شرط حجب العامل.

    Descriptive metadata only — the registry NEVER evaluates these.
    """

    BLOCKED_IF_PRECEDED_BY_HARF_JARR = "blocked_if_preceded_by_harf_jarr"
    BLOCKED_IF_FOLLOWS_VERB = "blocked_if_follows_verb"
    BLOCKED_IF_FRAME_UNRESOLVED = "blocked_if_frame_unresolved"
    BLOCKED_IF_FRAGMENT_FRAME = "blocked_if_fragment_frame"


# ---------------------------------------------------------------------------
# Supporting typed records
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OperatorInputSignature:
    """
    توصيف شكل المدخلات المتوقعة لعامل.

    *Descriptive only*; the registry does NOT verify a vector matches it.
    """

    expected_arity: int
    """Number of PreSyntaxMufradVector slots the operator is expected to read."""

    expected_neighbour_types: tuple[str, ...] = ()
    """
    Symbolic neighbour type-id names (e.g. ('ISM_COMMON',) or
    ('FIIL_MUDARI',)). Tuple of strings — purely descriptive labels.
    """

    notes: str = ""
    """Free-text descriptive note."""

    def __post_init__(self) -> None:
        if self.expected_arity < 0:
            raise ValueError(
                "OperatorInputSignature.expected_arity must be >= 0."
            )
        if not isinstance(self.expected_neighbour_types, tuple):
            raise TypeError(
                "OperatorInputSignature.expected_neighbour_types must be a tuple."
            )
        for t in self.expected_neighbour_types:
            if not isinstance(t, str) or not t:
                raise TypeError(
                    "OperatorInputSignature.expected_neighbour_types entries "
                    "must be non-empty strings."
                )


@dataclass(frozen=True)
class Citation:
    """
    استشهاد نصي على إثبات العامل.

    Pure documentation record. The registry never re-verifies the
    citation's content.
    """

    source: OperatorSource
    reference: str  # e.g. "Q 2:1", "Sibawayh I/45", "Mufassal §3"
    note: str = ""

    def __post_init__(self) -> None:
        if not isinstance(self.source, OperatorSource):
            raise TypeError(
                "Citation.source must be an OperatorSource enum member; got "
                f"{type(self.source).__name__}."
            )
        if not self.reference:
            raise ValueError("Citation.reference is required.")


# ---------------------------------------------------------------------------
# NahwOperatorEntry
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class NahwOperatorEntry:
    """
    مدخل عامل نحوي.

    One documented operator entry inside the registry. NOT an operator
    application, NOT an OperatorCandidate, NOT a binding. Contains only
    typed descriptive metadata.
    """

    operator_id: str
    display_name_ar: str
    source: OperatorSource
    school: NahwSchool
    rank: LughaRank
    family: OperatorTriggerFamily
    input_signature: OperatorInputSignature
    activation_conditions: tuple[ActivationCondition, ...]
    blocking_conditions: tuple[BlockingCondition, ...]
    expected_relation_families: tuple[ExpectedRelationFamily, ...]
    case_effect_policy_families: tuple[CaseEffectPolicyFamily, ...]
    citations: tuple[Citation, ...]
    entry_residuals: tuple[Residual, ...]
    entry_trace_id: str

    def __post_init__(self) -> None:
        # 1) Forbidden field-name guard (defensive — fails immediately if
        #    someone subclasses and adds a forbidden field).
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        leaks = field_names & _FORBIDDEN_FIELDS
        if leaks:
            raise ValueError(
                f"NahwOperatorEntry contains forbidden fields: {leaks}. "
                "The registry layer never carries operator bindings, "
                "relations, case effects, syntax roles, or meaning."
            )

        # 2) Required string fields.
        if not self.operator_id:
            raise ValueError("NahwOperatorEntry.operator_id is required.")
        if not self.display_name_ar:
            raise ValueError("NahwOperatorEntry.display_name_ar is required.")
        if not self.entry_trace_id:
            raise ValueError("NahwOperatorEntry.entry_trace_id is required.")

        # 3) Typed-only enum fields.
        if not isinstance(self.source, OperatorSource):
            raise TypeError(
                "NahwOperatorEntry.source must be an OperatorSource enum "
                f"member; got {type(self.source).__name__}."
            )
        if not isinstance(self.school, NahwSchool):
            raise TypeError(
                "NahwOperatorEntry.school must be a NahwSchool enum member; "
                f"got {type(self.school).__name__}."
            )
        if not isinstance(self.rank, LughaRank):
            raise TypeError(
                "NahwOperatorEntry.rank must be a LughaRank enum member; "
                f"got {type(self.rank).__name__}."
            )
        if not isinstance(self.family, OperatorTriggerFamily):
            raise TypeError(
                "NahwOperatorEntry.family must be an OperatorTriggerFamily "
                f"enum member; got {type(self.family).__name__}. Strings "
                "are forbidden."
            )
        if not isinstance(self.input_signature, OperatorInputSignature):
            raise TypeError(
                "NahwOperatorEntry.input_signature must be an "
                f"OperatorInputSignature; got {type(self.input_signature).__name__}."
            )

        # 4) Typed-only tuples.
        self._check_enum_tuple(
            self.activation_conditions,
            ActivationCondition,
            "activation_conditions",
        )
        self._check_enum_tuple(
            self.blocking_conditions,
            BlockingCondition,
            "blocking_conditions",
        )
        self._check_enum_tuple(
            self.expected_relation_families,
            ExpectedRelationFamily,
            "expected_relation_families",
        )
        self._check_enum_tuple(
            self.case_effect_policy_families,
            CaseEffectPolicyFamily,
            "case_effect_policy_families",
        )

        # 5) Citations must be typed.
        if not isinstance(self.citations, tuple):
            raise TypeError(
                "NahwOperatorEntry.citations must be a tuple of Citation."
            )
        for c in self.citations:
            if not isinstance(c, Citation):
                raise TypeError(
                    "NahwOperatorEntry.citations entries must be Citation "
                    f"instances; got {type(c).__name__}."
                )

        # 6) entry_residuals must use central ResidualType taxonomy.
        if not isinstance(self.entry_residuals, tuple):
            raise TypeError(
                "NahwOperatorEntry.entry_residuals must be a tuple of Residual."
            )
        for r in self.entry_residuals:
            if not isinstance(r, Residual):
                raise TypeError(
                    "NahwOperatorEntry.entry_residuals entries must be "
                    f"Residual; got {type(r).__name__}."
                )
            if not isinstance(r.type, ResidualType):
                raise TypeError(
                    "NahwOperatorEntry.entry_residuals must use central "
                    f"ResidualType taxonomy; got {type(r.type).__name__}."
                )

    @staticmethod
    def _check_enum_tuple(
        value: object, enum_cls: type, field_name: str
    ) -> None:
        if not isinstance(value, tuple):
            raise TypeError(
                f"NahwOperatorEntry.{field_name} must be a tuple of "
                f"{enum_cls.__name__}."
            )
        for item in value:
            if not isinstance(item, enum_cls):
                raise TypeError(
                    f"NahwOperatorEntry.{field_name} must contain only "
                    f"{enum_cls.__name__} enum members; got "
                    f"{type(item).__name__}: {item!r}. Strings are forbidden."
                )


# ---------------------------------------------------------------------------
# OperatorRegistryLookupResult
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OperatorRegistryLookupResult:
    """
    نتيجة استعلام السجل لعائلة محفز واحدة من ضمن trigger.

    Read-only wrapper around (family, matched_entries) for a single
    `OperatorTriggerFamily` looked up against a given
    `OperatorTriggerPotential`. Inherits residuals from the trigger and
    appends its own lookup-level residuals; never resolves competition.
    """

    trigger_id: str
    frame_id: str
    matrix_id: str
    family: OperatorTriggerFamily
    matched_entries: tuple[NahwOperatorEntry, ...]
    rank: LughaRank
    inherited_residuals: tuple[Residual, ...]
    lookup_residuals: tuple[Residual, ...]

    def __post_init__(self) -> None:
        # Forbidden field guard.
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        leaks = field_names & _FORBIDDEN_FIELDS
        if leaks:
            raise ValueError(
                f"OperatorRegistryLookupResult contains forbidden fields: {leaks}."
            )

        if not self.trigger_id:
            raise ValueError(
                "OperatorRegistryLookupResult.trigger_id is required."
            )
        if not self.frame_id:
            raise ValueError(
                "OperatorRegistryLookupResult.frame_id is required."
            )
        if not self.matrix_id:
            raise ValueError(
                "OperatorRegistryLookupResult.matrix_id is required."
            )
        if not isinstance(self.family, OperatorTriggerFamily):
            raise TypeError(
                "OperatorRegistryLookupResult.family must be an "
                f"OperatorTriggerFamily; got {type(self.family).__name__}."
            )
        if not isinstance(self.matched_entries, tuple):
            raise TypeError(
                "OperatorRegistryLookupResult.matched_entries must be a tuple."
            )
        for e in self.matched_entries:
            if not isinstance(e, NahwOperatorEntry):
                raise TypeError(
                    "OperatorRegistryLookupResult.matched_entries entries "
                    f"must be NahwOperatorEntry; got {type(e).__name__}."
                )
            if e.family is not self.family:
                raise ValueError(
                    f"OperatorRegistryLookupResult: entry {e.operator_id!r} "
                    f"belongs to family {e.family.value} but lookup is for "
                    f"family {self.family.value}."
                )
        if not isinstance(self.rank, LughaRank):
            raise TypeError(
                "OperatorRegistryLookupResult.rank must be a LughaRank."
            )
        for r in self.inherited_residuals + self.lookup_residuals:
            if not isinstance(r, Residual):
                raise TypeError(
                    "OperatorRegistryLookupResult residuals must be Residual."
                )
            if not isinstance(r.type, ResidualType):
                raise TypeError(
                    "OperatorRegistryLookupResult residuals must use central "
                    f"ResidualType taxonomy; got {type(r.type).__name__}."
                )

    def get_all_residuals(self) -> tuple[Residual, ...]:
        return self.inherited_residuals + self.lookup_residuals


# ---------------------------------------------------------------------------
# NahwOperatorRegistry
# ---------------------------------------------------------------------------


class NahwOperatorRegistry:
    """
    سجل العوامل النحوية.

    Immutable, read-only catalogue. Built once from a tuple of
    `NahwOperatorEntry` instances; afterwards exposes only lookup
    methods. The registry has *no* `apply`, `bind`, `resolve`, `choose`,
    or `rank_entries` method by design.
    """

    __slots__ = ("_entries", "_by_family", "_by_id", "_frozen")

    def __init__(self, entries: tuple[NahwOperatorEntry, ...]):
        if not isinstance(entries, tuple):
            raise TypeError(
                "NahwOperatorRegistry requires a tuple of NahwOperatorEntry."
            )
        by_family: dict[OperatorTriggerFamily, list[NahwOperatorEntry]] = {}
        by_id: dict[str, NahwOperatorEntry] = {}
        for e in entries:
            if not isinstance(e, NahwOperatorEntry):
                raise TypeError(
                    "NahwOperatorRegistry entries must be NahwOperatorEntry; "
                    f"got {type(e).__name__}."
                )
            if e.operator_id in by_id:
                raise ValueError(
                    "NahwOperatorRegistry: duplicate operator_id "
                    f"{e.operator_id!r}."
                )
            by_id[e.operator_id] = e
            by_family.setdefault(e.family, []).append(e)

        # Freeze internals into immutable tuples and wrap dicts with
        # MappingProxyType to prevent mutation.
        object.__setattr__(self, "_entries", tuple(entries))
        object.__setattr__(
            self,
            "_by_family",
            MappingProxyType({fam: tuple(es) for fam, es in by_family.items()}),
        )
        object.__setattr__(self, "_by_id", MappingProxyType(dict(by_id)))
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name: str, value: object) -> None:
        """Prevent post-init reassignment of internal storage."""
        if getattr(self, "_frozen", False):
            raise AttributeError(
                "NahwOperatorRegistry is immutable after construction; "
                f"cannot set attribute {name!r}."
            )
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        """Prevent deletion of internal storage."""
        raise AttributeError(
            "NahwOperatorRegistry is immutable; "
            f"cannot delete attribute {name!r}."
        )

    # ----- read-only accessors ------------------------------------------

    def all_entries(self) -> tuple[NahwOperatorEntry, ...]:
        return self._entries  # type: ignore[attr-defined]

    def all_families(self) -> frozenset[OperatorTriggerFamily]:
        return frozenset(self._by_family.keys())  # type: ignore[attr-defined]

    def entry_by_id(self, operator_id: str) -> Optional[NahwOperatorEntry]:
        return self._by_id.get(operator_id)  # type: ignore[attr-defined]

    def entries_for_family(
        self, family: OperatorTriggerFamily
    ) -> tuple[NahwOperatorEntry, ...]:
        if not isinstance(family, OperatorTriggerFamily):
            raise TypeError(
                "NahwOperatorRegistry.entries_for_family requires an "
                "OperatorTriggerFamily enum member; got "
                f"{type(family).__name__}. Strings are forbidden."
            )
        return self._by_family.get(family, ())  # type: ignore[attr-defined]

    def entries_for_trigger(
        self, trigger: OperatorTriggerPotential
    ) -> tuple[OperatorRegistryLookupResult, ...]:
        """
        Look up registry entries for every family present in a trigger.

        Returns one `OperatorRegistryLookupResult` per family in
        `trigger.triggered_families`, in the same order. Every result
        inherits `trigger.get_all_residuals()` (residual inheritance
        theorem extends to this layer) and adds lookup-specific
        info/warning residuals. NEVER resolves competition.
        """
        if not isinstance(trigger, OperatorTriggerPotential):
            raise TypeError(
                "NahwOperatorRegistry.entries_for_trigger requires an "
                "OperatorTriggerPotential; got "
                f"{type(trigger).__name__}. The registry layer never "
                "consumes raw tokens, frames, or matrices directly."
            )

        inherited = trigger.get_all_residuals()
        results: list[OperatorRegistryLookupResult] = []

        # Rank ceiling: registry-level rank is min(trigger.rank, max entry
        # rank seen for the family). We use trigger.rank as the ceiling
        # and never raise it, preserving the trigger.rank ≤ matrix.rank
        # ≤ frame.frame_rank chain.
        for family in trigger.triggered_families:
            entries = self.entries_for_family(family)
            lookup_residuals: list[Residual] = []

            if not entries:
                lookup_residuals.append(
                    make_warning(
                        ResidualType.REGISTRY_FAMILY_HAS_NO_ENTRIES,
                        f"No NahwOperatorEntry registered for family "
                        f"{family.value}; the lookup returns an empty tuple. "
                        "Resolution is the responsibility of a later stage.",
                        location=trigger.trigger_id,
                    )
                )
            elif len(entries) >= 2:
                lookup_residuals.append(
                    make_info(
                        ResidualType.REGISTRY_FAMILY_HAS_MULTIPLE_ENTRIES_PRESERVED,
                        f"Family {family.value} has {len(entries)} entries "
                        "preserved without resolution: "
                        f"{[e.operator_id for e in entries]}. Resolution "
                        "belongs to a later OperatorCandidate / "
                        "ParseCompetition stage.",
                        location=trigger.trigger_id,
                    )
                )

            # School-disagreement info: if multiple schools attest a
            # family among its entries, surface it (info only).
            if entries:
                schools = {e.school for e in entries}
                if len(schools - {NahwSchool.SHARED}) >= 2:
                    lookup_residuals.append(
                        make_info(
                            ResidualType.REGISTRY_ENTRY_HAS_SCHOOL_DISAGREEMENT,
                            "Multiple nahw schools attest family "
                            f"{family.value}: "
                            f"{sorted(s.value for s in schools)}.",
                            location=trigger.trigger_id,
                        )
                    )

            # Rank ceiling propagation (info residual when an entry's
            # rank exceeds the trigger's rank — we *do not* lower the
            # entry, but we DO clamp the lookup-level rank).
            if entries and any(e.rank > trigger.rank for e in entries):
                lookup_residuals.append(
                    make_info(
                        ResidualType.REGISTRY_LOOKUP_RANK_CEILED,
                        f"Some entries for family {family.value} have rank "
                        f"above trigger.rank={trigger.rank.name}; lookup "
                        "rank is clamped to trigger.rank.",
                        location=trigger.trigger_id,
                    )
                )

            results.append(
                OperatorRegistryLookupResult(
                    trigger_id=trigger.trigger_id,
                    frame_id=trigger.frame_id,
                    matrix_id=trigger.matrix_id,
                    family=family,
                    matched_entries=entries,
                    rank=trigger.rank,
                    inherited_residuals=inherited,
                    lookup_residuals=tuple(lookup_residuals),
                )
            )

        return tuple(results)


# ---------------------------------------------------------------------------
# Default registry construction (seed data lives in a separate module to
# keep data and logic separate; importing here also exports the public
# convenience builder).
# ---------------------------------------------------------------------------


def build_default_nahw_operator_registry() -> NahwOperatorRegistry:
    """
    Build the default NahwOperatorRegistry with the PR #15 seed entries.

    The seed covers every non-UNRESOLVED `OperatorTriggerFamily` with at
    least one documented entry. It is intentionally minimal-expanded;
    later PRs may add entries without changing the contract.
    """
    # Local import to avoid a circular import at module load.
    from dal_core.nahw_operator_registry_seed import build_seed_entries

    return NahwOperatorRegistry(build_seed_entries())
