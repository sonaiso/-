"""
Operator Candidate (مرشحات العوامل)

PR #17: Post-registry, pre-relation typed operator candidate layer.

ARCHITECTURE POSITION:
    SentenceFrameCandidate + CaseSignMatrix
            ↓
    OperatorTriggerPotential                  (PR #14 — typed candidate families)
            ↓
    NahwOperatorRegistry                      (PR #15 — typed operator ENTRIES)
            ↓
    OperatorCandidate                         (this module — typed CANDIDATE links)
            ↓
    [future] RelationCandidate → CaseEffectCandidate

GOVERNING RULES (do NOT relax):

1. An OperatorCandidate is a *typed link* between a TriggerSource and a
   NahwOperatorEntry. It NEVER:
     - applies an operator,
     - binds an operator to constituents,
     - resolves competition between candidates,
     - produces a RelationCandidate / CaseEffect / CaseEffectCandidate,
     - assigns syntax roles (faail / mafool / mubtada / khabar / mudaf /
       mudaf_ilayh / naat / badal),
     - asserts meaning (meaning / murad / madlul / haqiqa / majaz).

2. An OperatorCandidateSet preserves ALL competing candidates. Multiple
   candidates from different trigger sources or registry entries is normal and
   intentional. The set NEVER resolves competition.

3. Family matching: TriggerSource.family MUST equal NahwOperatorEntry.family.
   Any mismatch is a blocker.

4. Rank ceiling: candidate.rank ≤ min(trigger_source.rank, registry_entry.rank).

5. Residual inheritance: candidate.residuals includes inherited residuals from
   both trigger source and registry entry lookup path.

6. OperatorCandidateSetTrace is INDEPENDENT — it preserves ALL candidate ids,
   trigger source vector ids, and registry entry ids. It does NOT reuse a
   single candidate trace for the whole set.

7. get_all_residuals() MUST aggregate:
     - inherited_residuals (from trigger + registry path)
     - candidate_set_residuals (local to set construction)
     - all residuals from every OperatorCandidate in the set

8. Rank ceiling semantics:
     - OPERATOR_CANDIDATE_RANK_CEILED: normal rank lowering due to ceiling
     - OPERATOR_CANDIDATE_RANK_CEILING_VIOLATION: illegal rank elevation above ceiling
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
import uuid

from dal_core.nahw_operator_registry import NahwOperatorEntry, NahwOperatorRegistry
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
# Forbidden field guard (mirrors operator_trigger.py + nahw_operator_registry.py)
# ---------------------------------------------------------------------------

_FORBIDDEN_FIELDS: frozenset[str] = frozenset(
    {
        "operator_binding",
        "operator_application",
        "operator_id_resolved",
        "relation",
        "relation_type",
        "relation_candidate",
        "case_effect",
        "case_effect_candidate",
        "syntax_role",
        "faail",
        "mafool",
        "mafool_bih",
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


def _assert_no_forbidden_fields(obj: object, context: str = "") -> None:
    """
    Verify that an object does not have forbidden semantic/syntactic fields.

    Raises ValueError if any forbidden field is present.
    """
    for attr in dir(obj):
        if attr.startswith("_"):
            continue
        if attr in _FORBIDDEN_FIELDS:
            raise ValueError(
                f"Forbidden field '{attr}' found in {context or type(obj).__name__}. "
                f"OperatorCandidate layer must not carry operator application, "
                f"relation, case effect, syntax role, or meaning."
            )


# ---------------------------------------------------------------------------
# Core structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class OperatorCandidateTrace:
    """
    أثر مرشح عامل واحد

    Trace for a single OperatorCandidate linking trigger source to registry entry.
    """

    candidate_id: str
    trigger_source_vector_id: str
    registry_entry_id: str
    trigger_id: str
    frame_id: str
    matrix_id: str
    family: OperatorTriggerFamily
    derivation: str = "from_trigger_source_and_registry_entry"

    def __post_init__(self):
        """Validate trace integrity"""
        if not self.candidate_id:
            raise ValueError("OperatorCandidateTrace.candidate_id cannot be empty")
        if not self.trigger_source_vector_id:
            raise ValueError("OperatorCandidateTrace.trigger_source_vector_id cannot be empty")
        if not self.registry_entry_id:
            raise ValueError("OperatorCandidateTrace.registry_entry_id cannot be empty")


@dataclass(frozen=True)
class OperatorCandidate:
    """
    مرشح عامل

    A typed candidate link between a trigger source and a registry entry.
    Does NOT apply the operator, produce a relation, or assign case effects.
    """

    candidate_id: str
    trigger_source: TriggerSource
    registry_entry: NahwOperatorEntry
    family: OperatorTriggerFamily
    rank: LughaRank
    residuals: tuple[Residual, ...]
    trace: OperatorCandidateTrace

    def __post_init__(self):
        """Validate candidate integrity and governance rules"""
        # No forbidden fields
        _assert_no_forbidden_fields(self, "OperatorCandidate")

        # Family matching: trigger source family must equal registry entry family
        if self.trigger_source.family != self.registry_entry.family:
            raise ValueError(
                f"Family mismatch in OperatorCandidate {self.candidate_id}: "
                f"trigger source family {self.trigger_source.family} != "
                f"registry entry family {self.registry_entry.family}"
            )

        # Family must match both trigger source and registry entry
        if self.family != self.trigger_source.family:
            raise ValueError(
                f"Family mismatch in OperatorCandidate {self.candidate_id}: "
                f"candidate family {self.family} != trigger source family {self.trigger_source.family}"
            )

        if self.family != self.registry_entry.family:
            raise ValueError(
                f"Family mismatch in OperatorCandidate {self.candidate_id}: "
                f"candidate family {self.family} != registry entry family {self.registry_entry.family}"
            )

        # Rank ceiling: candidate rank must not exceed registry entry rank
        # (Trigger rank is checked at set level, not individual source level)
        if self.rank.value > self.registry_entry.rank.value:
            raise ValueError(
                f"Rank ceiling violation in OperatorCandidate {self.candidate_id}: "
                f"rank {self.rank} > registry entry rank {self.registry_entry.rank}"
            )

        # Trace must reference this candidate
        if self.trace.candidate_id != self.candidate_id:
            raise ValueError(
                f"Trace mismatch in OperatorCandidate {self.candidate_id}: "
                f"trace.candidate_id {self.trace.candidate_id} != candidate_id {self.candidate_id}"
            )

    def get_all_residuals(self) -> tuple[Residual, ...]:
        """
        Get all residuals for this candidate.

        For a single candidate, this is just the residuals tuple.
        For sets, this will aggregate across the hierarchy.
        """
        return self.residuals


@dataclass(frozen=True)
class OperatorCandidateSetTrace:
    """
    أثر مجموعة مرشحات العوامل

    DEDICATED trace for an OperatorCandidateSet.
    Does NOT reuse a single OperatorCandidateTrace.
    Preserves ALL candidate ids, trigger source vector ids, and registry entry ids.
    """

    set_id: str
    candidate_ids: tuple[str, ...]
    trigger_source_vector_ids: tuple[str, ...]
    registry_entry_ids: tuple[str, ...]
    families: tuple[OperatorTriggerFamily, ...]
    trigger_id: str
    frame_id: str
    matrix_id: str
    derivation: str = "from_operator_trigger_and_registry"

    def __post_init__(self):
        """Validate set trace integrity"""
        if not self.set_id:
            raise ValueError("OperatorCandidateSetTrace.set_id cannot be empty")

        # All tuples must have same length (one entry per candidate)
        if not (
            len(self.candidate_ids)
            == len(self.trigger_source_vector_ids)
            == len(self.registry_entry_ids)
            == len(self.families)
        ):
            raise ValueError(
                f"OperatorCandidateSetTrace tuple length mismatch: "
                f"candidate_ids={len(self.candidate_ids)}, "
                f"trigger_source_vector_ids={len(self.trigger_source_vector_ids)}, "
                f"registry_entry_ids={len(self.registry_entry_ids)}, "
                f"families={len(self.families)}"
            )


@dataclass(frozen=True)
class OperatorCandidateSet:
    """
    مجموعة مرشحات العوامل

    A set of competing OperatorCandidates. The set preserves ALL candidates;
    it does NOT resolve competition.
    """

    set_id: str
    candidates: tuple[OperatorCandidate, ...]
    set_trace: OperatorCandidateSetTrace
    inherited_residuals: tuple[Residual, ...]
    candidate_set_residuals: tuple[Residual, ...]

    def __post_init__(self):
        """Validate set integrity"""
        # No fake candidates (None) - check first before accessing attributes
        if any(c is None for c in self.candidates):
            raise ValueError(
                f"Fake candidate (None) detected in OperatorCandidateSet {self.set_id}"
            )

        # No forbidden fields
        _assert_no_forbidden_fields(self, "OperatorCandidateSet")

        # Set trace must reference this set
        if self.set_trace.set_id != self.set_id:
            raise ValueError(
                f"Set trace mismatch in OperatorCandidateSet {self.set_id}: "
                f"set_trace.set_id {self.set_trace.set_id} != set_id {self.set_id}"
            )

        # Set trace must preserve all candidate ids
        candidate_ids_in_set = {c.candidate_id for c in self.candidates}
        candidate_ids_in_trace = set(self.set_trace.candidate_ids)

        if candidate_ids_in_set != candidate_ids_in_trace:
            raise ValueError(
                f"Set trace candidate_ids mismatch in OperatorCandidateSet {self.set_id}: "
                f"candidates have {candidate_ids_in_set}, trace has {candidate_ids_in_trace}"
            )

    def get_all_residuals(self) -> tuple[Residual, ...]:
        """
        Get ALL residuals aggregated across the hierarchy.

        This MUST include:
        - inherited_residuals (from trigger + registry path)
        - candidate_set_residuals (local to set construction)
        - all residuals from every OperatorCandidate
        """
        # Start with inherited and set-level residuals
        all_residuals = list(self.inherited_residuals) + list(self.candidate_set_residuals)

        # Add residuals from every candidate
        for candidate in self.candidates:
            all_residuals.extend(candidate.get_all_residuals())

        # Deduplicate while preserving order
        seen = set()
        unique_residuals = []
        for r in all_residuals:
            # Use (type, message, location) as key for deduplication
            key = (r.type, r.message, r.location)
            if key not in seen:
                seen.add(key)
                unique_residuals.append(r)

        return tuple(unique_residuals)

    def is_empty(self) -> bool:
        """Check if this set has no candidates"""
        return len(self.candidates) == 0

    def has_blocking_residuals(self) -> bool:
        """Check if any residual in the hierarchy is a blocker"""
        return any(r.is_blocker() for r in self.get_all_residuals())


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------


@dataclass
class OperatorCandidateBuilder:
    """
    Builder for OperatorCandidateSet from OperatorTriggerPotential + NahwOperatorRegistry.

    Preserves all (TriggerSource × NahwOperatorEntry) pairs where families match.
    Does NOT resolve competition. Does NOT apply operators.
    """

    def build(
        self,
        trigger: OperatorTriggerPotential,
        registry: NahwOperatorRegistry,
    ) -> OperatorCandidateSet:
        """
        Build OperatorCandidateSet from trigger potential and registry.

        For each TriggerSource in the trigger potential:
        - Lookup all matching registry entries for that family
        - Create an OperatorCandidate for each (source, entry) pair
        - Preserve all candidates (no resolution)

        Args:
            trigger: OperatorTriggerPotential with typed trigger sources
            registry: NahwOperatorRegistry for operator entry lookup

        Returns:
            OperatorCandidateSet with all competing candidates preserved

        Raises:
            ValueError: If inputs are invalid or family mismatches occur
        """
        if trigger is None:
            raise ValueError("OperatorTriggerPotential cannot be None")
        if registry is None:
            raise ValueError("NahwOperatorRegistry cannot be None")

        set_id = f"operator_candidate_set_{uuid.uuid4().hex[:16]}"
        candidates: list[OperatorCandidate] = []
        candidate_set_residuals: list[Residual] = []

        # Collect all trigger source vector ids, registry entry ids, families
        all_candidate_ids: list[str] = []
        all_trigger_source_vector_ids: list[str] = []
        all_registry_entry_ids: list[str] = []
        all_families: list[OperatorTriggerFamily] = []

        # Build candidates from all trigger sources
        for source in trigger.sources:
            # Lookup registry entries for this family
            lookup_result = registry.lookup_by_family(source.family)

            if not lookup_result.entries:
                # No registry entries for this family
                candidate_set_residuals.append(
                    make_warning(
                        ResidualType.OPERATOR_CANDIDATE_NO_REGISTRY_ENTRY,
                        f"No registry entries for trigger family {source.family.value}",
                        location=f"trigger_source_{source.vector_id}",
                    )
                )
                continue

            # Create a candidate for each (source, entry) pair
            for entry in lookup_result.entries:
                # Verify family match
                if source.family != entry.family:
                    raise ValueError(
                        f"Family mismatch: trigger source family {source.family} != "
                        f"registry entry family {entry.family}"
                    )

                candidate_id = f"operator_candidate_{uuid.uuid4().hex[:16]}"

                # Rank ceiling: min of trigger rank (not individual source) and registry entry rank
                ceiling = min(trigger.rank, entry.rank)
                candidate_rank = ceiling

                # Collect residuals from trigger and registry lookup
                candidate_residuals: list[Residual] = []

                # Check for rank ceiling
                if trigger.rank != entry.rank:
                    # Rank was lowered due to ceiling
                    candidate_residuals.append(
                        make_info(
                            ResidualType.OPERATOR_CANDIDATE_RANK_CEILED,
                            f"Rank lowered to {ceiling.value} (ceiling from trigger {trigger.rank}, registry {entry.rank})",
                            location=candidate_id,
                        )
                    )

                # Build trace for this candidate
                candidate_trace = OperatorCandidateTrace(
                    candidate_id=candidate_id,
                    trigger_source_vector_id=source.vector_id,
                    registry_entry_id=entry.operator_id,
                    trigger_id=trigger.trigger_id,
                    frame_id=trigger.frame_id,
                    matrix_id=trigger.matrix_id,
                    family=source.family,
                )

                # Create candidate
                candidate = OperatorCandidate(
                    candidate_id=candidate_id,
                    trigger_source=source,
                    registry_entry=entry,
                    family=source.family,
                    rank=candidate_rank,
                    residuals=tuple(candidate_residuals),
                    trace=candidate_trace,
                )

                candidates.append(candidate)

                # Collect for set trace
                all_candidate_ids.append(candidate_id)
                all_trigger_source_vector_ids.append(source.vector_id)
                all_registry_entry_ids.append(entry.operator_id)
                all_families.append(source.family)

        # Check for multiple candidates (competition)
        if len(candidates) > 1:
            candidate_set_residuals.append(
                make_info(
                    ResidualType.OPERATOR_CANDIDATE_COMPETING_PRESERVED,
                    f"Multiple operator candidates preserved ({len(candidates)} candidates)",
                    location=set_id,
                )
            )

        # Build dedicated set trace
        set_trace = OperatorCandidateSetTrace(
            set_id=set_id,
            candidate_ids=tuple(all_candidate_ids),
            trigger_source_vector_ids=tuple(all_trigger_source_vector_ids),
            registry_entry_ids=tuple(all_registry_entry_ids),
            families=tuple(all_families),
            trigger_id=trigger.trigger_id,
            frame_id=trigger.frame_id,
            matrix_id=trigger.matrix_id,
        )

        # Inherit residuals from trigger potential
        inherited_residuals = trigger.get_all_residuals()

        # Build set
        candidate_set = OperatorCandidateSet(
            set_id=set_id,
            candidates=tuple(candidates),
            set_trace=set_trace,
            inherited_residuals=inherited_residuals,
            candidate_set_residuals=tuple(candidate_set_residuals),
        )

        return candidate_set
