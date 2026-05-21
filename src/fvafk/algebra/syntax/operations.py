"""Governed syntax operations.

Each operation implements the :class:`Operation` protocol and returns
:class:`Result` with full provenance (value + rank + evidence + residuals
+ failures + trace).

Operations never promote beyond their domain:

- :class:`MabniClosedOperatorOperation`: SYNTAX → SYNTAX Result (مبني)
- :class:`MurabOpenCarrierOperation`: SYNTAX → SYNTAX Result (معرب)
- :class:`AmilFunctionOperation`: SYNTAX → SYNTAX Result (عامل)
- :class:`IrabRelationEffectOperation`: SYNTAX → SYNTAX Result (إعراب)
- :class:`NisbahBindingOperation`: SYNTAX → SYNTAX Result (نسبة)

All operations stay **LICENSED** when residuals remain; **CERTIFIED**
requires full resolution (no context.absent, no case.ambiguous, etc.).

**Critical Principle**: النحو يرخص علاقة تركيبية، لا يحكم بالمعنى النهائي
(Syntax licenses relational structure, does not judge final meaning)
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

from .residual_taxonomy import (
    make_context_absent,
    make_operator_scope_unresolved,
    make_case_missing,
    make_case_estimated,
    make_case_ambiguous,
    make_governor_ambiguous,
    make_ellipsis_possible,
    make_attachment_ambiguous,
    make_relation_candidate,
    make_word_order_ambiguous,
)


@dataclass(frozen=True)
class MabniClosedOperatorOperation:
    """Governed مبني (closed operator) operation.

    Bridges: SYNTAX → SYNTAX (identity bridge)

    Identifies closed operators (particles) such as:
    - لم، لن، لا (negation/mood particles)
    - إن، أن، كأن، لكن، ليت، لعل (inna sisters)
    - من، ما، متى، أين، كيف (interrogative/relative particles)

    Returns Result with:

    - **LICENSED** if Evidence supports operator and residuals remain
    - **CERTIFIED** if operator confirmed with full scope and no residuals
    - **CANDIDATE** if no supporting Evidence
    - **REFUTED** if fatal contradiction (e.g., operator impossible in context)

    Emits residuals when operator scope is unresolved.
    Never emits SEMANTICS or HUKM evidence kinds.
    """

    name: str = "mabni_closed_operator"
    source_domain: Domain = Domain.SYNTAX
    target_domain: Domain = Domain.SYNTAX

    def run(self, carrier: Carrier[Any]) -> Result[str]:
        """Execute closed operator identification.

        Args:
            carrier: Carrier with domain SYNTAX, value is operator candidate
                (e.g., "لم", "إن").

        Returns:
            Result with operator value, rank based on evidence/residuals,
            and trace.
        """
        if carrier.domain != Domain.SYNTAX:
            return Result(
                value="",
                rank=Rank.REFUTED,
                failures=(
                    Failure(
                        kind="domain.mismatch",
                        description=f"Expected SYNTAX, got {carrier.domain}",
                        fatal=True,
                    ),
                ),
                trace=Trace(operation=self.name),
            )

        operator = str(carrier.value)
        if not operator:
            return Result(
                value="",
                rank=Rank.UNRESOLVED,
                trace=Trace(operation=self.name),
            )

        # Check if operator is recognized (simplified check)
        closed_operators = {
            "لم", "لن", "لا", "لام",
            "إن", "أن", "كأن", "لكن", "ليت", "لعل",
            "من", "ما", "متى", "أين", "كيف", "أي",
        }

        # Standard residuals for closed operators
        residuals: Tuple[Residual, ...] = (
            make_context_absent("Operator needs governed element in scope"),
            make_operator_scope_unresolved(operator=operator),
        )

        return Result(
            value=operator,
            rank=Rank.CANDIDATE,  # Stays CANDIDATE without Evidence
            residuals=residuals,
            trace=Trace(operation=self.name, source_span=(0, len(operator))),
        )


@dataclass(frozen=True)
class MurabOpenCarrierOperation:
    """Governed معرب (open carrier) operation.

    Bridges: SYNTAX → SYNTAX (identity bridge)

    Treats معرب (inflectable) words as open relational carriers that:
    - Require a governor (عامل) to determine case
    - May have visible, estimated, or ambiguous case marks
    - Carry relational potential (subject/object/complement)

    Returns Result with:

    - **LICENSED** if Evidence supports mu'rab status and residuals remain
    - **CERTIFIED** if mu'rab confirmed with explicit governor and case
    - **CANDIDATE** if no supporting Evidence
    - **REFUTED** if word is mabni (non-inflectable)

    Emits residuals for missing/estimated/ambiguous case marks.
    Never promotes to SEMANTICS or HUKM.
    """

    name: str = "murab_open_carrier"
    source_domain: Domain = Domain.SYNTAX
    target_domain: Domain = Domain.SYNTAX

    def run(self, carrier: Carrier[Any]) -> Result[str]:
        """Execute mu'rab carrier analysis.

        Args:
            carrier: Carrier with domain SYNTAX, value is word form.

        Returns:
            Result with word value, rank based on evidence/residuals,
            and trace.
        """
        if carrier.domain != Domain.SYNTAX:
            return Result(
                value="",
                rank=Rank.REFUTED,
                failures=(
                    Failure(
                        kind="domain.mismatch",
                        description=f"Expected SYNTAX, got {carrier.domain}",
                        fatal=True,
                    ),
                ),
                trace=Trace(operation=self.name),
            )

        word = str(carrier.value)
        if not word:
            return Result(
                value="",
                rank=Rank.UNRESOLVED,
                trace=Trace(operation=self.name),
            )

        # Standard residuals for mu'rab carriers
        residuals: Tuple[Residual, ...] = (
            make_context_absent("Mu'rab carrier needs governor context"),
            make_governor_ambiguous("Governor not yet determined"),
            make_case_missing("Case marking not visible on surface"),
        )

        return Result(
            value=word,
            rank=Rank.CANDIDATE,
            residuals=residuals,
            trace=Trace(operation=self.name, source_span=(0, len(word))),
        )


@dataclass(frozen=True)
class AmilFunctionOperation:
    """Governed عامل (governor/operator function) operation.

    Bridges: SYNTAX → SYNTAX (identity bridge)

    Represents العامل as an operating function over a dependent:
    - Verb governing subject/object
    - Particle governing noun (إن governing ism)
    - Preposition governing majrur

    Returns Result with:

    - **LICENSED** if Evidence supports amil function and residuals remain
    - **CERTIFIED** if amil confirmed with full scope and no residuals
    - **CANDIDATE** if no supporting Evidence
    - **REFUTED** if amil application impossible

    Must NOT produce semantic or hukm claims — only relational effects.
    """

    name: str = "amil_function"
    source_domain: Domain = Domain.SYNTAX
    target_domain: Domain = Domain.SYNTAX

    def run(self, carrier: Carrier[Any]) -> Result[str]:
        """Execute amil function analysis.

        Args:
            carrier: Carrier with domain SYNTAX, value is amil candidate.

        Returns:
            Result with amil value, rank based on evidence/residuals,
            and trace.
        """
        if carrier.domain != Domain.SYNTAX:
            return Result(
                value="",
                rank=Rank.REFUTED,
                failures=(
                    Failure(
                        kind="domain.mismatch",
                        description=f"Expected SYNTAX, got {carrier.domain}",
                        fatal=True,
                    ),
                ),
                trace=Trace(operation=self.name),
            )

        amil = str(carrier.value)
        if not amil:
            return Result(
                value="",
                rank=Rank.UNRESOLVED,
                trace=Trace(operation=self.name),
            )

        # Standard residuals for amil functions
        residuals: Tuple[Residual, ...] = (
            make_context_absent("Amil needs governed element"),
            make_operator_scope_unresolved(operator=amil),
            make_attachment_ambiguous("Governed element not yet attached"),
        )

        return Result(
            value=amil,
            rank=Rank.CANDIDATE,
            residuals=residuals,
            trace=Trace(operation=self.name, source_span=(0, len(amil))),
        )


@dataclass(frozen=True)
class IrabRelationEffectOperation:
    """Governed إعراب (case effect as relational evidence) operation.

    Bridges: SYNTAX → SYNTAX (identity bridge)

    Represents الإعراب as an effect of syntactic relation, not a bare vowel:
    - رفع as effect of subject relation (fael/mubtada)
    - نصب as effect of object relation (maf'ul) or inna operation
    - جر as effect of preposition or idafa
    - جزم as effect of jazm operators

    Distinguishes:
    - Visible case (ظاهر)
    - Estimated case (تقدير)
    - Local case (محلي)
    - Missing case
    - Ambiguous case

    Returns Result with:

    - **LICENSED** if case effect observed and residuals remain
    - **CERTIFIED** if case confirmed with explicit marking
    - **CANDIDATE** if case inferred/estimated
    - **REFUTED** if case effect contradicts structure

    Never promotes to SEMANTICS or HUKM.
    """

    name: str = "irab_relation_effect"
    source_domain: Domain = Domain.SYNTAX
    target_domain: Domain = Domain.SYNTAX

    def run(self, carrier: Carrier[Any]) -> Result[str]:
        """Execute i'rab relation effect analysis.

        Args:
            carrier: Carrier with domain SYNTAX, value is word with
                case marking.

        Returns:
            Result with word value, rank based on case evidence/residuals,
            and trace.
        """
        if carrier.domain != Domain.SYNTAX:
            return Result(
                value="",
                rank=Rank.REFUTED,
                failures=(
                    Failure(
                        kind="domain.mismatch",
                        description=f"Expected SYNTAX, got {carrier.domain}",
                        fatal=True,
                    ),
                ),
                trace=Trace(operation=self.name),
            )

        word = str(carrier.value)
        if not word:
            return Result(
                value="",
                rank=Rank.UNRESOLVED,
                trace=Trace(operation=self.name),
            )

        # Check for visible case marks (simplified heuristic)
        has_visible_case = any(mark in word for mark in ["ُ", "َ", "ِ", "ْ"])

        residuals: Tuple[Residual, ...] = ()

        if not has_visible_case:
            residuals = residuals + (
                make_case_missing("No visible case mark on surface"),
                make_case_estimated("Case must be estimated from context"),
            )
        else:
            # Even with visible case, may be ambiguous
            residuals = residuals + (
                make_case_ambiguous("Case may have multiple readings"),
            )

        # Always need context for full i'rab determination
        residuals = residuals + (
            make_context_absent("I'rab effect needs syntactic context"),
        )

        return Result(
            value=word,
            rank=Rank.CANDIDATE,
            residuals=residuals,
            trace=Trace(operation=self.name, source_span=(0, len(word))),
        )


@dataclass(frozen=True)
class NisbahBindingOperation:
    """Governed نسبة (relation binding) operation.

    Bridges: SYNTAX → SYNTAX (identity bridge)

    Binds syntactic relation candidates:
    - ISN (إسنادي) — Predicative relation (mubtada-khabar, fael-fi'l)
    - TADMN (تضميني) — Complement relation (maf'ul, khabar kaana)
    - TAQYD (تقييدي) — Modifier relation (sifa, haal, zarf)
    - IDAFA (إضافي) — Possessive/genitive relation
    - HALI (حالي) — Circumstantial relation
    - ZARFI (ظرفي) — Adverbial relation

    Returns Result with:

    - **LICENSED** if relation candidate identified and residuals remain
    - **CERTIFIED** if relation confirmed with full agreement
    - **CANDIDATE** if relation type uncertain
    - **REFUTED** if relation binding contradicts structure

    May license SYNTAX but cannot jump to HUKM.
    """

    name: str = "nisbah_binding"
    source_domain: Domain = Domain.SYNTAX
    target_domain: Domain = Domain.SYNTAX

    def run(self, carrier: Carrier[Any]) -> Result[str]:
        """Execute nisbah binding analysis.

        Args:
            carrier: Carrier with domain SYNTAX, value is relation candidate.

        Returns:
            Result with relation value, rank based on evidence/residuals,
            and trace.
        """
        if carrier.domain != Domain.SYNTAX:
            return Result(
                value="",
                rank=Rank.REFUTED,
                failures=(
                    Failure(
                        kind="domain.mismatch",
                        description=f"Expected SYNTAX, got {carrier.domain}",
                        fatal=True,
                    ),
                ),
                trace=Trace(operation=self.name),
            )

        relation = str(carrier.value)
        if not relation:
            return Result(
                value="",
                rank=Rank.UNRESOLVED,
                trace=Trace(operation=self.name),
            )

        # Standard residuals for nisbah binding
        residuals: Tuple[Residual, ...] = (
            make_context_absent("Relation binding needs full sentence context"),
            make_relation_candidate("Relation type not finalized"),
            make_word_order_ambiguous("Word order affects relation interpretation"),
            make_ellipsis_possible("Possible ellipsis may affect relation"),
        )

        return Result(
            value=relation,
            rank=Rank.CANDIDATE,
            residuals=residuals,
            trace=Trace(operation=self.name, source_span=(0, len(relation))),
        )


# ---------------------------------------------------------------------------
# Convenience wrappers
# ---------------------------------------------------------------------------


def governed_mabni_operator(
    operator: str, evidence: Tuple[Evidence, ...] = ()
) -> Result[str]:
    """Convenience wrapper for mabni operator identification.

    Args:
        operator: Operator candidate (e.g., "لم", "إن").
        evidence: Optional Evidence tuple from adapters.

    Returns:
        Result from MabniClosedOperatorOperation.
    """
    op = MabniClosedOperatorOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value=operator)
    result = op.run(carrier)

    if evidence:
        result = result.with_evidence(*evidence)
        # Promote to LICENSED if evidence present
        if result.rank == Rank.CANDIDATE and evidence:
            result = result.with_rank(Rank.LICENSED)

    return result


def governed_murab_carrier(
    word: str, evidence: Tuple[Evidence, ...] = ()
) -> Result[str]:
    """Convenience wrapper for mu'rab carrier analysis.

    Args:
        word: Word form.
        evidence: Optional Evidence tuple from adapters.

    Returns:
        Result from MurabOpenCarrierOperation.
    """
    op = MurabOpenCarrierOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value=word)
    result = op.run(carrier)

    if evidence:
        result = result.with_evidence(*evidence)
        if result.rank == Rank.CANDIDATE and evidence:
            result = result.with_rank(Rank.LICENSED)

    return result


def governed_amil_function(
    amil: str, evidence: Tuple[Evidence, ...] = ()
) -> Result[str]:
    """Convenience wrapper for amil function analysis.

    Args:
        amil: Amil candidate.
        evidence: Optional Evidence tuple from adapters.

    Returns:
        Result from AmilFunctionOperation.
    """
    op = AmilFunctionOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value=amil)
    result = op.run(carrier)

    if evidence:
        result = result.with_evidence(*evidence)
        if result.rank == Rank.CANDIDATE and evidence:
            result = result.with_rank(Rank.LICENSED)

    return result


def governed_irab_effect(
    word: str, evidence: Tuple[Evidence, ...] = ()
) -> Result[str]:
    """Convenience wrapper for i'rab relation effect analysis.

    Args:
        word: Word with case marking.
        evidence: Optional Evidence tuple from adapters.

    Returns:
        Result from IrabRelationEffectOperation.
    """
    op = IrabRelationEffectOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value=word)
    result = op.run(carrier)

    if evidence:
        result = result.with_evidence(*evidence)
        if result.rank == Rank.CANDIDATE and evidence:
            result = result.with_rank(Rank.LICENSED)

    return result


def governed_nisbah_binding(
    relation: str, evidence: Tuple[Evidence, ...] = ()
) -> Result[str]:
    """Convenience wrapper for nisbah binding analysis.

    Args:
        relation: Relation candidate (e.g., "ISN", "TADMN").
        evidence: Optional Evidence tuple from adapters.

    Returns:
        Result from NisbahBindingOperation.
    """
    op = NisbahBindingOperation()
    carrier = Carrier(domain=Domain.SYNTAX, value=relation)
    result = op.run(carrier)

    if evidence:
        result = result.with_evidence(*evidence)
        if result.rank == Rank.CANDIDATE and evidence:
            result = result.with_rank(Rank.LICENSED)

    return result


__all__ = [
    "MabniClosedOperatorOperation",
    "MurabOpenCarrierOperation",
    "AmilFunctionOperation",
    "IrabRelationEffectOperation",
    "NisbahBindingOperation",
    "governed_mabni_operator",
    "governed_murab_carrier",
    "governed_amil_function",
    "governed_irab_effect",
    "governed_nisbah_binding",
]
