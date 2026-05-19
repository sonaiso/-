"""
Frame Builder (بانى الإطار)

Builds sentence frame candidates from list of PreSyntaxMufradVector.

CRITICAL PRINCIPLES:
1. Builds frames from PreSyntaxMufradVector ONLY (not tokens)
2. Does NOT apply operators (operators work on frames)
3. Identifies structural patterns, not semantic meanings
4. Creates candidates, not definitive parses
5. Preserves rank ceiling and residual inheritance

Architecture:
```
list[PreSyntaxMufradVector]
  → FrameBuilder
  → list[SentenceFrameCandidate]
```

Each frame candidate represents a structural hypothesis.
Multiple candidates may compete.
Operators will later resolve competitions based on governance rules.
"""

from typing import Optional
import uuid

from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.sentence_frame import (
    SentenceFrameCandidate,
    NominalFrameCandidate,
    VerbalFrameCandidate,
    ParticleLedFrameCandidate,
    FragmentFrameCandidate,
    UnresolvedFrameCandidate,
    FrameType,
    calculate_frame_rank,
    collect_inherited_residuals,
)
from dal_core.type_ids import NounTypeID, VerbTypeID, ParticleTypeID
from dal_core.residuals import Residual, ResidualType, ResidualSeverity
from dal_core.evidence import Evidence


class FrameBuilder:
    """
    Builds sentence frame candidates from PreSyntaxMufradVector list.

    Strategy:
    1. Analyze constituent types (ISM, FIIL, HARF)
    2. Identify structural patterns
    3. Generate competing frame candidates
    4. Apply rank ceiling and residual inheritance
    5. Return candidates ordered by confidence
    """

    def __init__(self):
        self.frame_counter = 0

    def build_frames(
        self,
        constituents: tuple[PreSyntaxMufradVector, ...],
        source_text: Optional[str] = None,
    ) -> list[SentenceFrameCandidate]:
        """
        Build frame candidates from constituents.

        Returns:
            list of frame candidates, may be empty if no valid frames
        """
        if not constituents:
            return []

        # Check if all constituents allow consumption
        if not all(c.allows_operator_consumption() for c in constituents):
            # Build unresolved frame with blocker
            return [self._build_blocked_frame(constituents)]

        # Try to identify frame patterns
        candidates = []

        # Check for verbal frame (FIIL present)
        verbal_candidate = self._try_verbal_frame(constituents)
        if verbal_candidate:
            candidates.append(verbal_candidate)

        # Check for particle-led frame (HARF at start)
        particle_candidate = self._try_particle_led_frame(constituents)
        if particle_candidate:
            candidates.append(particle_candidate)

        # Check for nominal frame (ISM at start, no FIIL)
        nominal_candidate = self._try_nominal_frame(constituents)
        if nominal_candidate:
            candidates.append(nominal_candidate)

        # Check for fragment
        fragment_candidate = self._try_fragment_frame(constituents)
        if fragment_candidate:
            candidates.append(fragment_candidate)

        # If no candidates identified, create unresolved
        if not candidates:
            candidates.append(self._build_unresolved_frame(constituents))

        return candidates

    def _try_verbal_frame(
        self,
        constituents: tuple[PreSyntaxMufradVector, ...]
    ) -> Optional[VerbalFrameCandidate]:
        """
        Try to build verbal frame candidate.

        Pattern: FIIL + ...
        """
        # Find verb (first FIIL)
        verb_index = None
        for i, c in enumerate(constituents):
            if isinstance(c.type_id, VerbTypeID):
                verb_index = i
                break

        if verb_index is None:
            return None

        # Build verbal frame
        frame_id = self._generate_frame_id("verbal")
        frame_rank = calculate_frame_rank(constituents)
        inherited = collect_inherited_residuals(constituents)

        # No frame-specific residuals yet (operators will add those)
        frame_residuals = ()

        trace_id = f"frame_{frame_id}"

        return VerbalFrameCandidate(
            frame_id=frame_id,
            frame_type=FrameType.VERBAL,
            constituents=constituents,
            frame_rank=frame_rank,
            inherited_residuals=inherited,
            frame_specific_residuals=frame_residuals,
            trace_id=trace_id,
            verb_index=verb_index,
        )

    def _try_particle_led_frame(
        self,
        constituents: tuple[PreSyntaxMufradVector, ...]
    ) -> Optional[ParticleLedFrameCandidate]:
        """
        Try to build particle-led frame candidate.

        Pattern: HARF + ...
        """
        # Check if first constituent is HARF
        if not constituents:
            return None

        first = constituents[0]
        if not isinstance(first.type_id, ParticleTypeID):
            return None

        # Extract operator potential if available
        operator_potential = None
        if first.particle_operator_potential:
            operator_potential = first.particle_operator_potential.potential_type

        # Build particle-led frame
        frame_id = self._generate_frame_id("particle_led")
        frame_rank = calculate_frame_rank(constituents)
        inherited = collect_inherited_residuals(constituents)
        frame_residuals = ()
        trace_id = f"frame_{frame_id}"

        return ParticleLedFrameCandidate(
            frame_id=frame_id,
            frame_type=FrameType.PARTICLE_LED,
            constituents=constituents,
            frame_rank=frame_rank,
            inherited_residuals=inherited,
            frame_specific_residuals=frame_residuals,
            trace_id=trace_id,
            particle_index=0,
            particle_operator_potential=operator_potential,
        )

    def _try_nominal_frame(
        self,
        constituents: tuple[PreSyntaxMufradVector, ...]
    ) -> Optional[NominalFrameCandidate]:
        """
        Try to build nominal frame candidate.

        Pattern: ISM + ... (no FIIL, no leading HARF)
        """
        if not constituents:
            return None

        # Check first constituent is ISM
        first = constituents[0]
        if not isinstance(first.type_id, NounTypeID):
            return None

        # Verify no FIIL present (would be verbal frame)
        has_verb = any(isinstance(c.type_id, VerbTypeID) for c in constituents)
        if has_verb:
            return None

        # Build nominal frame
        frame_id = self._generate_frame_id("nominal")
        frame_rank = calculate_frame_rank(constituents)
        inherited = collect_inherited_residuals(constituents)
        frame_residuals = ()
        trace_id = f"frame_{frame_id}"

        return NominalFrameCandidate(
            frame_id=frame_id,
            frame_type=FrameType.NOMINAL,
            constituents=constituents,
            frame_rank=frame_rank,
            inherited_residuals=inherited,
            frame_specific_residuals=frame_residuals,
            trace_id=trace_id,
            lead_noun_index=0,
        )

    def _try_fragment_frame(
        self,
        constituents: tuple[PreSyntaxMufradVector, ...]
    ) -> Optional[FragmentFrameCandidate]:
        """
        Try to build fragment frame candidate.

        Fragments are incomplete structures:
        - Single noun without predicate
        - Prepositional phrase
        - Incomplete verbal (verb without required arguments)
        """
        if not constituents:
            return None

        # Single constituent is likely a fragment
        if len(constituents) == 1:
            reason = f"single_{constituents[0].type_value}"
        # HARF + single ISM might be prepositional phrase
        elif len(constituents) == 2:
            if (isinstance(constituents[0].type_id, ParticleTypeID) and
                isinstance(constituents[1].type_id, NounTypeID)):
                # Check if it's a jarr particle
                if constituents[0].type_id == ParticleTypeID.HARF_JARR:
                    reason = "prepositional_phrase"
                else:
                    reason = "particle_plus_noun"
            else:
                return None  # Let other patterns handle it
        else:
            return None  # Longer structures handled by other frame types

        frame_id = self._generate_frame_id("fragment")
        frame_rank = calculate_frame_rank(constituents)
        inherited = collect_inherited_residuals(constituents)
        frame_residuals = ()
        trace_id = f"frame_{frame_id}"

        return FragmentFrameCandidate(
            frame_id=frame_id,
            frame_type=FrameType.FRAGMENT,
            constituents=constituents,
            frame_rank=frame_rank,
            inherited_residuals=inherited,
            frame_specific_residuals=frame_residuals,
            trace_id=trace_id,
            fragment_reason=reason,
        )

    def _build_unresolved_frame(
        self,
        constituents: tuple[PreSyntaxMufradVector, ...]
    ) -> UnresolvedFrameCandidate:
        """
        Build unresolved frame when pattern unclear.
        """
        frame_id = self._generate_frame_id("unresolved")
        frame_rank = calculate_frame_rank(constituents)
        inherited = collect_inherited_residuals(constituents)
        frame_residuals = ()
        trace_id = f"frame_{frame_id}"

        # Identify competing possibilities
        competing = []
        has_noun = any(isinstance(c.type_id, NounTypeID) for c in constituents)
        has_verb = any(isinstance(c.type_id, VerbTypeID) for c in constituents)
        has_particle = any(isinstance(c.type_id, ParticleTypeID) for c in constituents)

        if has_noun:
            competing.append(FrameType.NOMINAL)
        if has_verb:
            competing.append(FrameType.VERBAL)
        if has_particle:
            competing.append(FrameType.PARTICLE_LED)
        if not competing:
            competing.append(FrameType.FRAGMENT)

        reason = "ambiguous_constituent_types"

        return UnresolvedFrameCandidate(
            frame_id=frame_id,
            frame_type=FrameType.UNRESOLVED,
            constituents=constituents,
            frame_rank=frame_rank,
            inherited_residuals=inherited,
            frame_specific_residuals=frame_residuals,
            trace_id=trace_id,
            competing_frame_types=tuple(competing),
            unresolved_reason=reason,
        )

    def _build_blocked_frame(
        self,
        constituents: tuple[PreSyntaxMufradVector, ...]
    ) -> UnresolvedFrameCandidate:
        """
        Build unresolved frame when constituents have blockers.
        """
        frame_id = self._generate_frame_id("blocked")
        frame_rank = calculate_frame_rank(constituents)
        inherited = collect_inherited_residuals(constituents)

        # Add frame-specific residual about blocking
        blocker = Residual(
            type=ResidualType.COMPOSITION_BLOCKER,
            severity=ResidualSeverity.BLOCKER,
            message="Frame constituents not ready for composition",
            location="FrameBuilder",
        )
        frame_residuals = (blocker,)

        trace_id = f"frame_{frame_id}"

        return UnresolvedFrameCandidate(
            frame_id=frame_id,
            frame_type=FrameType.UNRESOLVED,
            constituents=constituents,
            frame_rank=frame_rank,
            inherited_residuals=inherited,
            frame_specific_residuals=frame_residuals,
            trace_id=trace_id,
            competing_frame_types=(FrameType.UNRESOLVED,),
            unresolved_reason="constituents_blocked",
        )

    def _generate_frame_id(self, frame_type_str: str) -> str:
        """Generate unique frame ID"""
        self.frame_counter += 1
        return f"{frame_type_str}_{self.frame_counter}_{uuid.uuid4().hex[:8]}"


def build_sentence_frames(
    constituents: tuple[PreSyntaxMufradVector, ...],
    source_text: Optional[str] = None,
) -> list[SentenceFrameCandidate]:
    """
    Convenience function to build sentence frames.

    Args:
        constituents: Tuple of PreSyntaxMufradVector
        source_text: Optional source text for debugging

    Returns:
        List of frame candidates (may be empty)
    """
    builder = FrameBuilder()
    return builder.build_frames(constituents, source_text)
