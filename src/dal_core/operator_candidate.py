"""
Operator Candidate (المرشح العاملي)

PR #17: Post-registry, pre-relation candidate-linking layer.

ARCHITECTURE POSITION:
    OperatorTriggerPotential + NahwOperatorRegistry  (input — only legal sources)
            ↓
    OperatorCandidateSet                              (this module — typed pairs)
            ↓
    [future] RelationCandidate
          → CaseEffectCandidate
          → ParseCompetition

GOVERNING RULES (do NOT relax):
1. Inputs are ONLY an OperatorTriggerPotential AND a NahwOperatorRegistry; both
   must be typed. Anything else raises TypeError.
2. Output is a *candidate link* set between TriggerSource objects and
   NahwOperatorEntry objects, NEVER:
     - an applied operator (no operator_id binding, no operator application),
     - a relation (no relation_type, no ISN/TADMN/TAQYID resolution),
     - a case judgment (no marfoo_by/mansub_by/majroor_by/majzum_by),
     - a syntax role (no faail/mafool/mubtada/khabar/mudaf/mudaf_ilayh),
     - a semantic meaning (no meaning/murad/madlul/haqiqa/majaz),
     - governance (no governs/produces_relation/produces_case).
3. Every OperatorCandidate must be tied to a specific TriggerSource AND a
   specific NahwOperatorEntry. The pairing rule is:
     TriggerSource.family == NahwOperatorEntry.family
4. Competing candidates are PRESERVED, never silently resolved. If multiple
   sources match multiple entries, all (source, entry) pairs are preserved.
5. Rank ceiling extends: candidate.rank ≤ min(trigger.rank, lookup_result.rank,
   registry_entry.rank).
6. Residual inheritance extends: candidate.inherited_residuals ⊇
   trigger.get_all_residuals() ⊇ matrix.get_all_residuals() ⊇
   frame.get_all_residuals(). Nothing is erased.
7. Every governance residual is a member of the central ResidualType taxonomy.
8. For UNRESOLVED_TRIGGER or any trigger family with no registry entries:
   - produce NO fake candidate
   - keep candidates=()
   - emit OPERATOR_CANDIDATE_NO_REGISTRY_ENTRIES residual
   - rank ≤ trigger.rank with explicit trace
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import uuid

from dal_core.nahw_operator_registry import (
    NahwOperatorEntry,
    NahwOperatorRegistry,
    OperatorRegistryLookupResult,
)
from dal_core.operator_trigger import (
    OperatorTriggerFamily,
    OperatorTriggerPotential,
    TriggerSource,
)
from dal_core.ranks import LughaRank
from dal_core.residuals import (
    Residual,
    ResidualType,
    make_blocker,
    make_info,
    make_warning,
)


# ---------------------------------------------------------------------------
# Forbidden field names (defensive governance)
# ---------------------------------------------------------------------------

_FORBIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "operator",
        "operator_id",
        "operator_binding",
        "applied_operator",
        "operator_application",
        "resolved_operator",
        "relation",
        "relation_type",
        "case_effect",
        "case_effect_candidate",
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
        "governs",
        "governance",
        "applies_to",
        "produces_relation",
        "produces_case",
        "matches_relation",
        "case_policy_applied",
        "meaning",
        "semantic",
        "madlul",
        "murad",
        "haqiqa",
        "majaz",
        "grounding",
    }
)


# ---------------------------------------------------------------------------
# OperatorCandidateTrace
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OperatorCandidateTrace:
    """
    أثر المرشح العاملي

    Minimal mandatory trace linking candidate back to:
    - trigger_id (from OperatorTriggerPotential)
    - trigger_source.vector_id (from specific TriggerSource)
    - registry_entry_id (from NahwOperatorEntry)
    - frame_id, matrix_id (chain provenance)
    """

    candidate_id: str
    """Unique identifier for this candidate."""

    trigger_id: str
    """OperatorTriggerPotential.trigger_id this candidate originated from."""

    trigger_source_vector_id: str
    """TriggerSource.vector_id of the specific trigger source."""

    registry_entry_id: str
    """NahwOperatorEntry.operator_id this candidate links to."""

    frame_id: str
    """SentenceFrameCandidate.frame_id (chain provenance)."""

    matrix_id: str
    """CaseSignMatrix.matrix_id (chain provenance)."""

    derivation: str = "from_operator_trigger_and_registry"
    """Fixed derivation marker."""

    def __post_init__(self) -> None:
        if not self.candidate_id:
            raise ValueError("OperatorCandidateTrace.candidate_id is required.")
        if not self.trigger_id:
            raise ValueError("OperatorCandidateTrace.trigger_id is required.")
        if not self.trigger_source_vector_id:
            raise ValueError(
                "OperatorCandidateTrace.trigger_source_vector_id is required."
            )
        if not self.registry_entry_id:
            raise ValueError(
                "OperatorCandidateTrace.registry_entry_id is required."
            )
        if not self.frame_id:
            raise ValueError("OperatorCandidateTrace.frame_id is required.")
        if not self.matrix_id:
            raise ValueError("OperatorCandidateTrace.matrix_id is required.")
        if self.derivation != "from_operator_trigger_and_registry":
            raise ValueError(
                "OperatorCandidateTrace.derivation must be "
                "'from_operator_trigger_and_registry'."
            )


# ---------------------------------------------------------------------------
# OperatorCandidate
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OperatorCandidate:
    """
    مرشح عاملي

    A typed (TriggerSource, NahwOperatorEntry) pair.

    This is NOT an applied operator. This is NOT a relation. This is NOT a
    case effect. It is a candidate link saying: "This registry entry is a
    possible operator candidate for this trigger source."

    FORBIDDEN: No apply, bind, resolve, governs, produces_* methods or fields.
    """

    candidate_id: str
    """Unique identifier for this candidate."""

    trigger_id: str
    """OperatorTriggerPotential.trigger_id this candidate originated from."""

    frame_id: str
    """SentenceFrameCandidate.frame_id (chain provenance)."""

    matrix_id: str
    """CaseSignMatrix.matrix_id (chain provenance)."""

    trigger_family: OperatorTriggerFamily
    """The candidate trigger family (from TriggerSource.family)."""

    trigger_source: TriggerSource
    """The specific TriggerSource this candidate is tied to."""

    registry_entry_id: str
    """NahwOperatorEntry.operator_id this candidate links to."""

    registry_entry: NahwOperatorEntry
    """
    The specific NahwOperatorEntry this candidate links to.

    Since PR #16 made NahwOperatorRegistry immutable, it is safe to reference
    the entry directly. Still preserve explicit trace fields for auditability.
    """

    rank: LughaRank
    """
    Candidate rank ceiling:
    rank ≤ min(trigger.rank, lookup_result.rank, registry_entry.rank)
    """

    inherited_residuals: tuple[Residual, ...]
    """
    Residuals inherited from trigger (which inherits from matrix, frame, etc.).
    Must include trigger.get_all_residuals().
    """

    candidate_residuals: tuple[Residual, ...]
    """Residuals specific to this candidate (e.g., rank ceiling violations)."""

    trace: OperatorCandidateTrace
    """Trace linking back to trigger source and registry entry."""

    def __post_init__(self) -> None:
        # Field-name leak check (defensive)
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        leaks = field_names & _FORBIDDEN_FIELDS
        if leaks:
            raise ValueError(
                f"OperatorCandidate contains forbidden fields: {leaks}. "
                f"The candidate layer may only carry typed (TriggerSource, "
                f"RegistryEntry) pairs, never operators, relations, case "
                f"effects, syntax roles, or meaning."
            )

        # Type checks
        if not self.candidate_id:
            raise ValueError("OperatorCandidate.candidate_id is required.")
        if not self.trigger_id:
            raise ValueError("OperatorCandidate.trigger_id is required.")
        if not self.frame_id:
            raise ValueError("OperatorCandidate.frame_id is required.")
        if not self.matrix_id:
            raise ValueError("OperatorCandidate.matrix_id is required.")
        if not isinstance(self.trigger_family, OperatorTriggerFamily):
            raise TypeError(
                "OperatorCandidate.trigger_family must be an "
                "OperatorTriggerFamily enum member; got "
                f"{type(self.trigger_family).__name__}."
            )
        if not isinstance(self.trigger_source, TriggerSource):
            raise TypeError(
                "OperatorCandidate.trigger_source must be a TriggerSource; "
                f"got {type(self.trigger_source).__name__}."
            )
        if not self.registry_entry_id:
            raise ValueError("OperatorCandidate.registry_entry_id is required.")
        if not isinstance(self.registry_entry, NahwOperatorEntry):
            raise TypeError(
                "OperatorCandidate.registry_entry must be a NahwOperatorEntry; "
                f"got {type(self.registry_entry).__name__}."
            )
        if not isinstance(self.rank, LughaRank):
            raise TypeError(
                "OperatorCandidate.rank must be a LughaRank; got "
                f"{type(self.rank).__name__}."
            )
        if not isinstance(self.inherited_residuals, tuple):
            raise TypeError(
                "OperatorCandidate.inherited_residuals must be a tuple."
            )
        if not isinstance(self.candidate_residuals, tuple):
            raise TypeError(
                "OperatorCandidate.candidate_residuals must be a tuple."
            )
        for r in self.inherited_residuals + self.candidate_residuals:
            if not isinstance(r, Residual):
                raise TypeError(
                    "OperatorCandidate residuals must be Residual instances."
                )
            if not isinstance(r.type, ResidualType):
                raise TypeError(
                    "OperatorCandidate residuals must use central ResidualType "
                    f"taxonomy; got {type(r.type).__name__}."
                )
        if not isinstance(self.trace, OperatorCandidateTrace):
            raise TypeError(
                "OperatorCandidate.trace must be an OperatorCandidateTrace; "
                f"got {type(self.trace).__name__}."
            )

        # Family matching: TriggerSource.family must equal NahwOperatorEntry.family
        if self.trigger_source.family != self.registry_entry.family:
            raise ValueError(
                f"OperatorCandidate family mismatch: "
                f"trigger_source.family={self.trigger_source.family.value} "
                f"but registry_entry.family={self.registry_entry.family.value}. "
                f"Every candidate must pair matching families only."
            )

        # Trace consistency
        if self.trace.candidate_id != self.candidate_id:
            raise ValueError(
                "OperatorCandidate.trace.candidate_id must match candidate_id."
            )
        if self.trace.trigger_id != self.trigger_id:
            raise ValueError(
                "OperatorCandidate.trace.trigger_id must match trigger_id."
            )
        if self.trace.trigger_source_vector_id != self.trigger_source.vector_id:
            raise ValueError(
                "OperatorCandidate.trace.trigger_source_vector_id must match "
                "trigger_source.vector_id."
            )
        if self.trace.registry_entry_id != self.registry_entry_id:
            raise ValueError(
                "OperatorCandidate.trace.registry_entry_id must match "
                "registry_entry_id."
            )
        if self.trace.frame_id != self.frame_id:
            raise ValueError(
                "OperatorCandidate.trace.frame_id must match frame_id."
            )
        if self.trace.matrix_id != self.matrix_id:
            raise ValueError(
                "OperatorCandidate.trace.matrix_id must match matrix_id."
            )

    def get_all_residuals(self) -> tuple[Residual, ...]:
        """Return all residuals (inherited + candidate-specific)."""
        return self.inherited_residuals + self.candidate_residuals


# ---------------------------------------------------------------------------
# OperatorCandidateSet
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OperatorCandidateSet:
    """
    مجموعة المرشحين العامليين

    The complete set of all (TriggerSource, RegistryEntry) pair candidates
    for a given OperatorTriggerPotential.

    PRESERVES ALL COMPETING CANDIDATES. Never resolves competition.
    """

    trigger_id: str
    """OperatorTriggerPotential.trigger_id this set originated from."""

    frame_id: str
    """SentenceFrameCandidate.frame_id (chain provenance)."""

    matrix_id: str
    """CaseSignMatrix.matrix_id (chain provenance)."""

    candidates: tuple[OperatorCandidate, ...]
    """
    All candidates, preserving all competing (TriggerSource, RegistryEntry)
    pairs. Empty tuple if no registry entries matched any trigger family.
    """

    rank: LughaRank
    """
    Candidate set rank ceiling:
    - If candidates non-empty: rank ≤ min(candidate.rank for candidate in candidates)
    - If candidates empty: rank ≤ trigger.rank
    """

    inherited_residuals: tuple[Residual, ...]
    """Residuals inherited from trigger (includes matrix, frame, etc.)."""

    candidate_set_residuals: tuple[Residual, ...]
    """Residuals specific to this candidate set (e.g., no entries, competition)."""

    trace: OperatorCandidateTrace
    """
    Trace linking back to trigger. When candidates=(), trace points to
    trigger with a placeholder registry_entry_id.
    """

    competitors_preserved: bool
    """
    True when multiple candidates exist or when any trigger family had
    multiple registry entries. Signals unresolved competition.
    """

    def __post_init__(self) -> None:
        # Field-name leak check (defensive)
        field_names = {f.name for f in self.__dataclass_fields__.values()}
        leaks = field_names & _FORBIDDEN_FIELDS
        if leaks:
            raise ValueError(
                f"OperatorCandidateSet contains forbidden fields: {leaks}. "
                f"The candidate set layer may only carry typed (TriggerSource, "
                f"RegistryEntry) pairs, never operators, relations, case "
                f"effects, syntax roles, or meaning."
            )

        # Type checks
        if not self.trigger_id:
            raise ValueError("OperatorCandidateSet.trigger_id is required.")
        if not self.frame_id:
            raise ValueError("OperatorCandidateSet.frame_id is required.")
        if not self.matrix_id:
            raise ValueError("OperatorCandidateSet.matrix_id is required.")
        if not isinstance(self.candidates, tuple):
            raise TypeError("OperatorCandidateSet.candidates must be a tuple.")
        for c in self.candidates:
            if not isinstance(c, OperatorCandidate):
                raise TypeError(
                    "OperatorCandidateSet.candidates entries must be "
                    f"OperatorCandidate; got {type(c).__name__}."
                )
        if not isinstance(self.rank, LughaRank):
            raise TypeError(
                "OperatorCandidateSet.rank must be a LughaRank; got "
                f"{type(self.rank).__name__}."
            )
        if not isinstance(self.inherited_residuals, tuple):
            raise TypeError(
                "OperatorCandidateSet.inherited_residuals must be a tuple."
            )
        if not isinstance(self.candidate_set_residuals, tuple):
            raise TypeError(
                "OperatorCandidateSet.candidate_set_residuals must be a tuple."
            )
        for r in self.inherited_residuals + self.candidate_set_residuals:
            if not isinstance(r, Residual):
                raise TypeError(
                    "OperatorCandidateSet residuals must be Residual instances."
                )
            if not isinstance(r.type, ResidualType):
                raise TypeError(
                    "OperatorCandidateSet residuals must use central "
                    f"ResidualType taxonomy; got {type(r.type).__name__}."
                )
        if not isinstance(self.trace, OperatorCandidateTrace):
            raise TypeError(
                "OperatorCandidateSet.trace must be an OperatorCandidateTrace; "
                f"got {type(self.trace).__name__}."
            )
        if not isinstance(self.competitors_preserved, bool):
            raise TypeError(
                "OperatorCandidateSet.competitors_preserved must be a bool."
            )

    def get_all_residuals(self) -> tuple[Residual, ...]:
        """Return all residuals (inherited + set-specific)."""
        return self.inherited_residuals + self.candidate_set_residuals

    def has_unresolved_competition(self) -> bool:
        """
        Check if multiple candidates exist (unresolved competition).

        Returns True if len(candidates) >= 2, indicating that multiple
        (TriggerSource, RegistryEntry) pairs exist and no resolution has
        been applied.
        """
        return len(self.candidates) >= 2


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


def build_operator_candidates(
    trigger: OperatorTriggerPotential,
    registry: NahwOperatorRegistry,
) -> OperatorCandidateSet:
    """
    بناء المرشحين العامليين

    Build typed (TriggerSource, NahwOperatorEntry) pair candidates from
    trigger and registry.

    GOVERNING RULES:
    1. Accepts only OperatorTriggerPotential and NahwOperatorRegistry.
    2. Uses registry.entries_for_trigger(trigger) for lookup.
    3. For every matching TriggerSource and NahwOperatorEntry where
       source.family == entry.family, creates one OperatorCandidate.
    4. Preserves all competing entries. Does NOT choose one.
    5. Preserves all competing trigger families. Does NOT suppress one.
    6. If a trigger family has no registry entries, preserves a residual
       but does NOT invent an operator.
    7. Candidate rank: rank ≤ min(trigger.rank, lookup_result.rank, entry.rank)
    8. CandidateSet rank:
       - If candidates non-empty: rank ≤ min(candidate.rank)
       - If candidates empty: rank ≤ trigger.rank
    9. Residual inheritance: candidate.inherited_residuals ⊇
       trigger.get_all_residuals()
    10. No candidate may erase registry lookup residuals.

    Args:
        trigger: OperatorTriggerPotential from prior layer
        registry: NahwOperatorRegistry (immutable catalog)

    Returns:
        OperatorCandidateSet with all (source, entry) pair candidates preserved

    Raises:
        TypeError: If inputs are not the required types
        ValueError: If trigger or registry is invalid
    """
    # Input validation
    if not isinstance(trigger, OperatorTriggerPotential):
        raise TypeError(
            "build_operator_candidates requires an OperatorTriggerPotential; "
            f"got {type(trigger).__name__}. The candidate layer never consumes "
            "raw tokens, frames, or matrices directly."
        )
    if not isinstance(registry, NahwOperatorRegistry):
        raise TypeError(
            "build_operator_candidates requires a NahwOperatorRegistry; got "
            f"{type(registry).__name__}."
        )

    # Lookup registry entries for all trigger families
    lookup_results = registry.entries_for_trigger(trigger)

    # Inherited residuals from trigger (includes matrix, frame, etc.)
    inherited = trigger.get_all_residuals()

    # Build candidates: for each (TriggerSource, RegistryEntry) pair where
    # source.family == entry.family, create one OperatorCandidate.
    candidates: list[OperatorCandidate] = []
    candidate_set_residuals: list[Residual] = []

    # Track whether we have any competition
    total_entries_count = sum(len(lr.matched_entries) for lr in lookup_results)
    total_sources_count = len(trigger.trigger_sources)
    competitors_preserved = False

    for lookup_result in lookup_results:
        family = lookup_result.family
        matched_entries = lookup_result.matched_entries

        if not matched_entries:
            # No registry entries for this family
            candidate_set_residuals.append(
                make_warning(
                    ResidualType.OPERATOR_CANDIDATE_NO_REGISTRY_ENTRIES,
                    f"Trigger family {family.value} has no registry entries; "
                    f"no candidates created for this family. Resolution is the "
                    f"responsibility of a later ParseCompetition stage.",
                    location=trigger.trigger_id,
                )
            )
            continue

        # Find all trigger sources matching this family
        matching_sources = [
            src for src in trigger.trigger_sources if src.family == family
        ]

        if not matching_sources:
            # This should not happen if registry.entries_for_trigger works
            # correctly, but defensive check
            candidate_set_residuals.append(
                make_warning(
                    ResidualType.OPERATOR_CANDIDATE_NO_REGISTRY_ENTRIES,
                    f"Trigger family {family.value} has registry entries but "
                    f"no matching TriggerSource; no candidates created. This "
                    f"indicates a registry/trigger mismatch.",
                    location=trigger.trigger_id,
                )
            )
            continue

        # Create one candidate per (source, entry) pair
        for source in matching_sources:
            for entry in matched_entries:
                # Verify family matching (defensive)
                if source.family != entry.family:
                    continue  # Skip mismatched pairs

                candidate_id = f"candidate-{uuid.uuid4().hex[:12]}"

                # Candidate rank ceiling: min(trigger.rank, lookup.rank, entry.rank)
                candidate_rank = min(
                    trigger.rank,
                    lookup_result.rank,
                    entry.rank,
                    key=lambda r: r.value,
                )

                # Candidate-specific residuals
                cand_residuals: list[Residual] = []

                # Inherit lookup residuals
                lookup_residuals_inherited = lookup_result.lookup_residuals

                # Check for rank ceiling violation
                if candidate_rank.value < trigger.rank.value:
                    cand_residuals.append(
                        make_info(
                            ResidualType.OPERATOR_CANDIDATE_RANK_CEILING_VIOLATION,
                            f"Candidate rank {candidate_rank.name} is lower than "
                            f"trigger rank {trigger.rank.name} due to registry "
                            f"entry or lookup result rank ceiling.",
                            location=candidate_id,
                        )
                    )

                # Create trace
                trace = OperatorCandidateTrace(
                    candidate_id=candidate_id,
                    trigger_id=trigger.trigger_id,
                    trigger_source_vector_id=source.vector_id,
                    registry_entry_id=entry.operator_id,
                    frame_id=trigger.frame_id,
                    matrix_id=trigger.matrix_id,
                )

                # Create candidate
                candidate = OperatorCandidate(
                    candidate_id=candidate_id,
                    trigger_id=trigger.trigger_id,
                    frame_id=trigger.frame_id,
                    matrix_id=trigger.matrix_id,
                    trigger_family=family,
                    trigger_source=source,
                    registry_entry_id=entry.operator_id,
                    registry_entry=entry,
                    rank=candidate_rank,
                    inherited_residuals=inherited + lookup_residuals_inherited,
                    candidate_residuals=tuple(cand_residuals),
                    trace=trace,
                )
                candidates.append(candidate)

    # Check for competition
    if len(candidates) >= 2:
        competitors_preserved = True
        candidate_set_residuals.append(
            make_info(
                ResidualType.OPERATOR_CANDIDATE_COMPETITION_PRESERVED,
                f"Multiple operator candidates ({len(candidates)}) preserved "
                f"without resolution. Resolution belongs to a later "
                f"ParseCompetition stage.",
                location=trigger.trigger_id,
            )
        )
    elif total_entries_count >= 2 or total_sources_count >= 2:
        # Even if we only have 1 candidate, if there were multiple entries
        # or sources, mark competition as preserved
        competitors_preserved = True

    # Candidate set rank
    if candidates:
        set_rank = min((c.rank for c in candidates), key=lambda r: r.value)
    else:
        # No candidates: rank ≤ trigger.rank
        set_rank = trigger.rank

    # Create trace for the set (placeholder if empty)
    set_trace_id = f"candidate-set-{uuid.uuid4().hex[:12]}"
    set_trace = OperatorCandidateTrace(
        candidate_id=set_trace_id,
        trigger_id=trigger.trigger_id,
        trigger_source_vector_id=(
            candidates[0].trigger_source.vector_id
            if candidates
            else "no-sources"
        ),
        registry_entry_id=(
            candidates[0].registry_entry_id if candidates else "no-entries"
        ),
        frame_id=trigger.frame_id,
        matrix_id=trigger.matrix_id,
    )

    # Build candidate set
    candidate_set = OperatorCandidateSet(
        trigger_id=trigger.trigger_id,
        frame_id=trigger.frame_id,
        matrix_id=trigger.matrix_id,
        candidates=tuple(candidates),
        rank=set_rank,
        inherited_residuals=inherited,
        candidate_set_residuals=tuple(candidate_set_residuals),
        trace=set_trace,
        competitors_preserved=competitors_preserved,
    )

    return candidate_set
