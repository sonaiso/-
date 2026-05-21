"""Governed morphology operations.

Each operation implements the :class:`Operation` protocol and returns
:class:`Result` with full provenance (value + rank + evidence + residuals
+ failures + trace).

Operations never promote beyond their domain:

- :class:`PatternMatchOperation`: MORPH_SURFACE → MORPH_SURFACE Result
- :class:`RootExtractionOperation`: MORPH_SURFACE → ROOT Result
- :class:`AffixDetectionOperation`: MORPH_SURFACE → MORPH_SURFACE Result

All operations stay **LICENSED** when residuals remain; **CERTIFIED**
requires full resolution (no context.absent, no lexical.ambiguity, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Tuple

from fvafk.algebra import (
    Carrier,
    Domain,
    Evidence,
    Failure,
    Operation,
    Rank,
    Residual,
    Result,
    Trace,
)
from fvafk.algebra.adapters import C2bAdapter

from .residual_taxonomy import (
    make_context_absent,
    make_lexical_ambiguity,
    make_pattern_collision,
    make_root_ambiguous,
    make_weak_letter_present,
    make_affix_aggressive_strip,
)


@dataclass(frozen=True)
class PatternMatchOperation:
    """Governed pattern matching operation.

    Bridges: MORPH_SURFACE → MORPH_SURFACE (identity bridge)

    Takes a MORPH_SURFACE carrier (surface pattern candidate like "فاعل")
    and Evidence from adapters, returns Result with:

    - **LICENSED** if Evidence supports pattern and residuals remain
    - **CERTIFIED** if Evidence supports pattern and no residuals
    - **CANDIDATE** if no supporting Evidence
    - **REFUTED** if fatal contradiction (e.g., pattern impossible given root)

    Never emits SEMANTICS or HUKM evidence kinds.
    """

    name: str = "pattern_match"
    source_domain: Domain = Domain.MORPH_SURFACE
    target_domain: Domain = Domain.MORPH_SURFACE

    def run(self, carrier: Carrier[Any]) -> Result[str]:
        """Execute pattern matching.

        Args:
            carrier: Carrier with domain MORPH_SURFACE, value is pattern
                candidate (e.g., "فاعل").

        Returns:
            Result with pattern value, rank based on evidence/residuals,
            and trace.
        """
        if carrier.domain != Domain.MORPH_SURFACE:
            return Result(
                value="",
                rank=Rank.REFUTED,
                failures=(
                    Failure(
                        kind="domain.mismatch",
                        description=f"Expected MORPH_SURFACE, got {carrier.domain}",
                        fatal=True,
                    ),
                ),
                trace=Trace(operation=self.name),
            )

        pattern = str(carrier.value)
        if not pattern:
            return Result(
                value="",
                rank=Rank.UNRESOLVED,
                trace=Trace(operation=self.name),
            )

        # For now, return CANDIDATE with standard residuals
        # Real implementation would check Evidence from adapters
        residuals: Tuple[Residual, ...] = (
            make_context_absent("Pattern match needs surrounding tokens"),
            make_lexical_ambiguity(f"Pattern '{pattern}' has multiple meanings"),
        )

        return Result(
            value=pattern,
            rank=Rank.CANDIDATE,  # Stays CANDIDATE without Evidence
            residuals=residuals,
            trace=Trace(operation=self.name, source_span=(0, len(pattern))),
        )


@dataclass(frozen=True)
class RootExtractionOperation:
    """Governed root extraction operation.

    Bridges: MORPH_SURFACE → ROOT

    Takes a MORPH_SURFACE carrier and Evidence from C2bAdapter, returns
    Result with:

    - **LICENSED** if C2bAdapter provides ROOT evidence and residuals remain
    - **CERTIFIED** if ROOT evidence present and no residuals
    - **CANDIDATE** if no ROOT evidence
    - **REFUTED** if fatal contradiction (e.g., impossible root)

    **Never promotes to SEMANTICS or HUKM** — root extraction supports
    ROOT domain only.
    """

    name: str = "root_extraction"
    source_domain: Domain = Domain.MORPH_SURFACE
    target_domain: Domain = Domain.ROOT

    def run(self, carrier: Carrier[Any]) -> Result[str]:
        """Execute root extraction.

        Args:
            carrier: Carrier with domain MORPH_SURFACE, value is surface
                form (e.g., "كاتب").

        Returns:
            Result with root value (e.g., "ك-ت-ب"), rank based on
            evidence/residuals, and trace.
        """
        if carrier.domain != Domain.MORPH_SURFACE:
            return Result(
                value="",
                rank=Rank.REFUTED,
                failures=(
                    Failure(
                        kind="domain.mismatch",
                        description=f"Expected MORPH_SURFACE, got {carrier.domain}",
                        fatal=True,
                    ),
                ),
                trace=Trace(operation=self.name),
            )

        surface = str(carrier.value)
        if not surface:
            return Result(
                value="",
                rank=Rank.UNRESOLVED,
                trace=Trace(operation=self.name),
            )

        # Placeholder: real implementation would use C2bAdapter evidence
        # For now, return CANDIDATE with standard residuals
        residuals: Tuple[Residual, ...] = (
            make_context_absent("Root extraction needs context"),
            make_root_ambiguous(f"'{surface}' has multiple root candidates"),
        )

        # Detect weak letters (simplified heuristic)
        weak_letters = []
        for char in ["و", "ي", "ا"]:
            if char in surface:
                weak_letters.append(char)

        if weak_letters:
            residuals = residuals + (
                make_weak_letter_present(weak_letters=", ".join(weak_letters)),
            )

        return Result(
            value="???",  # Placeholder root
            rank=Rank.CANDIDATE,
            residuals=residuals,
            trace=Trace(operation=self.name, source_span=(0, len(surface))),
        )


@dataclass(frozen=True)
class AffixDetectionOperation:
    """Governed affix detection operation.

    Bridges: MORPH_SURFACE → MORPH_SURFACE (identity bridge)

    Takes a MORPH_SURFACE carrier and detects prefixes/suffixes, returns
    Result with:

    - **Residuals for aggressive stripping** when affix removal may have
      damaged stem
    - **Residuals for weak letters** when affixes contain و، ي، alif
    - **LICENSED** if Evidence supports affix set and residuals remain
    - **CERTIFIED** if affix set confirmed and no residuals

    Never promotes beyond MORPH_SURFACE domain.
    """

    name: str = "affix_detection"
    source_domain: Domain = Domain.MORPH_SURFACE
    target_domain: Domain = Domain.MORPH_SURFACE

    def run(self, carrier: Carrier[Any]) -> Result[str]:
        """Execute affix detection.

        Args:
            carrier: Carrier with domain MORPH_SURFACE, value is surface
                form.

        Returns:
            Result with detected affixes (or empty if none), rank based
            on evidence/residuals, and trace.
        """
        if carrier.domain != Domain.MORPH_SURFACE:
            return Result(
                value="",
                rank=Rank.REFUTED,
                failures=(
                    Failure(
                        kind="domain.mismatch",
                        description=f"Expected MORPH_SURFACE, got {carrier.domain}",
                        fatal=True,
                    ),
                ),
                trace=Trace(operation=self.name),
            )

        surface = str(carrier.value)
        if not surface:
            return Result(
                value="",
                rank=Rank.UNRESOLVED,
                trace=Trace(operation=self.name),
            )

        # Placeholder affix detection (simplified)
        residuals: Tuple[Residual, ...] = ()

        # Check for common prefixes
        if surface.startswith("ال"):
            residuals = residuals + (
                make_affix_aggressive_strip(affix="ال", position="prefix"),
            )
        elif surface.startswith("ب") or surface.startswith("و"):
            residuals = residuals + (
                make_affix_aggressive_strip(
                    affix=surface[0], position="prefix"
                ),
            )

        # Check for common suffixes
        if surface.endswith("ة") or surface.endswith("ه"):
            residuals = residuals + (
                make_affix_aggressive_strip(
                    affix=surface[-1], position="suffix"
                ),
            )

        # Add context residual
        residuals = residuals + (
            make_context_absent("Affix detection needs grammatical context"),
        )

        return Result(
            value=surface,
            rank=Rank.CANDIDATE,
            residuals=residuals,
            trace=Trace(operation=self.name, source_span=(0, len(surface))),
        )


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------


def governed_pattern_match(
    pattern: str, evidence: Tuple[Evidence, ...] = ()
) -> Result[str]:
    """Convenience wrapper for pattern matching.

    Args:
        pattern: Pattern candidate (e.g., "فاعل").
        evidence: Optional Evidence tuple from adapters.

    Returns:
        Result from PatternMatchOperation.
    """
    op = PatternMatchOperation()
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value=pattern)
    result = op.run(carrier)

    if evidence:
        result = result.with_evidence(*evidence)
        # Promote to LICENSED if evidence present
        if result.rank == Rank.CANDIDATE and evidence:
            result = result.with_rank(Rank.LICENSED)

    return result


def governed_root_extract(
    surface: str, evidence: Tuple[Evidence, ...] = ()
) -> Result[str]:
    """Convenience wrapper for root extraction.

    Args:
        surface: Surface form (e.g., "كاتب").
        evidence: Optional Evidence tuple from C2bAdapter.

    Returns:
        Result from RootExtractionOperation.
    """
    op = RootExtractionOperation()
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value=surface)
    result = op.run(carrier)

    if evidence:
        result = result.with_evidence(*evidence)
        # Promote to LICENSED if evidence present
        if result.rank == Rank.CANDIDATE and evidence:
            result = result.with_rank(Rank.LICENSED)

    return result


def governed_affix_detect(
    surface: str, evidence: Tuple[Evidence, ...] = ()
) -> Result[str]:
    """Convenience wrapper for affix detection.

    Args:
        surface: Surface form.
        evidence: Optional Evidence tuple from adapters.

    Returns:
        Result from AffixDetectionOperation.
    """
    op = AffixDetectionOperation()
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value=surface)
    result = op.run(carrier)

    if evidence:
        result = result.with_evidence(*evidence)
        # Promote to LICENSED if evidence present
        if result.rank == Rank.CANDIDATE and evidence:
            result = result.with_rank(Rank.LICENSED)

    return result


__all__ = [
    "PatternMatchOperation",
    "RootExtractionOperation",
    "AffixDetectionOperation",
    "governed_pattern_match",
    "governed_root_extract",
    "governed_affix_detect",
]
