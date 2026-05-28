"""
PreSyntaxReadinessResult (نتيجة الجاهزية النحوية)

GARA-FT-1 Boundary Object - Second constitutional layer after SignifierTokenResult.

This module implements the boundary object for pre-syntactic readiness extraction,
consuming SignifierTokenResult and producing readiness/potential data WITHOUT:
- Meaning, semantic interpretation
- Syntax roles (faail/mafool/mubtada/khabar)
- Applied operators or governance
- Relations (ISN/TADMIN/TAQYID)
- Ifādah or Hukm

CRITICAL PRINCIPLE:
PreSyntaxReadinessResult is a SEPARATE boundary layer from SignifierTokenResult.
It consumes SignifierTokenResult but does NOT mutate or enrich it.

CONSTITUTIONAL LAWS ENFORCED:
1. No semantic leak (meaning/murad/madlul/semantic/ifadah/hukm)
2. No syntax roles (faail/mafool/mubtada/khabar/syntax_role)
3. No case effects - only CaseSignPotential (observation, not judgment)
4. No applied operators (governed_by/governs/operator_applied)
5. No relations (ISN/TADMIN/TAQYID/relation/relation_type)
6. No RelationCandidate production (requires RelationAlgebraCore activation)
7. SignifierTokenResult remains boundary-only (not modified)

LAYER POSITION:
```
MufradProof
  → SignifierTokenResult        # PR #131: boundary wrapper only
  → PreSyntaxReadinessResult    # PR #132: readiness only (THIS)
  → OperatorCandidateResult     # FUTURE
  → RelationAlgebraCore         # FUTURE: only here relation may begin
```

See: docs/GARA_FT_0_BOUNDARY_SPEC.md
"""

from dataclasses import dataclass
from typing import Optional

from dal_core.signifier_token_result import SignifierTokenResult, SignifierToken
from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.dal_algebra import AlgebraicFailure


# Constitutional prohibition registry (extended from SignifierTokenResult)
_SEMANTIC_LEAK_PREVENTION = frozenset({
    "meaning", "murad", "madlul", "semantic",
    "haqiqa", "majaz", "ifadah", "hukm"
})

_SYNTAX_ROLE_PREVENTION = frozenset({
    "faail", "mafool", "mubtada", "khabar",
    "syntax_role", "governed_by", "governs"
})

_CASE_EFFECT_PREVENTION = frozenset({
    "case_effect", "raf", "nasb", "jarr",
    "marfoo_by", "mansub_by", "majroor_by"
})

_APPLIED_OPERATOR_PREVENTION = frozenset({
    "applied_operator", "operator_binding",
    "operator_applied", "governs", "governed_nodes"
})

_RELATION_PREVENTION = frozenset({
    "relation", "relation_type", "relation_binding",
    "isn_subject", "isn_predicate",
    "tadmin_incorporated", "taqyid_restricted",
    "wasf_described", "idafah_possessor"
})

_OPERATOR_CANDIDATE_PREVENTION = frozenset({
    "operator_candidate", "relation_candidate",
    "ifadah_candidate", "hukm_candidate"
})


@dataclass(frozen=True)
class PreSyntaxReadinessResult:
    """
    نتيجة الجاهزية النحوية

    Result wrapper for GARA-FT-1 boundary operation.

    Constitutional Position:
    ----------------------
    - IS: Result wrapper containing pre-syntactic readiness data
    - IS: Consumer of SignifierTokenResult (input boundary)
    - IS: Producer of PreSyntaxMufradVector (output readiness)
    - IS: Separate boundary layer from SignifierTokenResult

    - IS NOT: Modification of SignifierTokenResult (separate object)
    - IS NOT: Syntax analyzer (no roles, no governance)
    - IS NOT: Semantic interpreter (no meaning, no ifadah)
    - IS NOT: Relation builder (no ISN/TADMIN/TAQYID)
    - IS NOT: Operator applicator (potentials only, not applied)

    Result Semantics:
    ----------------
    PreSyntaxReadinessResult ≠ SignifierTokenResult

    - SignifierTokenResult: MufradProof → SignifierToken wrapper (boundary)
    - PreSyntaxReadinessResult: SignifierTokenResult → PreSyntaxMufradVector (readiness)

    This is a SEPARATE layer, not an enrichment of the previous layer.

    Mutual Exclusion:
    ----------------
    Exactly ONE of the following must be non-None:
    - readiness_vector (success)
    - failure (failure)

    Both cannot be present simultaneously.

    Fields:
    ------
    - source_token_result: SignifierTokenResult
      Input from previous boundary layer (preserved, not mutated)

    - readiness_vector: Optional[PreSyntaxMufradVector]
      Pre-syntactic readiness interface (present on success)

    - failure: Optional[AlgebraicFailure]
      Algebraic failure reason (present on failure)

    Usage:
    ------
    Success case:
    >>> token_result = SignifierTokenResult(...)
    >>> readiness_result = create_presyntax_readiness_result(token_result)
    >>> readiness_result.is_success  # True
    >>> readiness_result.readiness_vector  # PreSyntaxMufradVector

    Failure case (input failure):
    >>> token_result = SignifierTokenResult(signifier_token=None, failure=...)
    >>> readiness_result = create_presyntax_readiness_result(token_result)
    >>> readiness_result.is_failure  # True
    >>> readiness_result.failure.reason  # "Input SignifierTokenResult failed"

    Constitutional Guarantees:
    -------------------------
    1. No RelationCandidate production (not in scope)
    2. No OperatorCandidate production (not in scope)
    3. No semantic fields (meaning/murad/madlul)
    4. No syntax roles (faail/mafool)
    5. No case effects (raf/nasb/jarr - only CaseSignPotential)
    6. No applied operators (governed_by - only OperatorTriggerPotential)
    7. No relations (ISN/TADMIN/TAQYID)
    8. No ifādah or hukm
    9. SignifierTokenResult preserved as-is (not mutated)

    These are enforced by:
    - Frozen dataclass (no runtime field addition)
    - Minimal field set (source + vector + failure)
    - Input validation (rejects failed SignifierTokenResult)
    - Constitutional tests (test_presyntax_readiness_result.py)
    """

    source_token_result: SignifierTokenResult
    readiness_vector: Optional[PreSyntaxMufradVector]
    failure: Optional[AlgebraicFailure]

    def __post_init__(self):
        """
        Validate result mutual exclusion invariant.

        Ensures exactly one of:
        - readiness_vector (success)
        - failure (failure)

        is present.

        Raises:
            ValueError: If both present or both absent
            TypeError: If source_token_result is not SignifierTokenResult
        """
        if not isinstance(self.source_token_result, SignifierTokenResult):
            raise TypeError(
                f"PreSyntaxReadinessResult requires SignifierTokenResult input, "
                f"got {type(self.source_token_result)}"
            )

        present_count = sum([
            self.readiness_vector is not None,
            self.failure is not None
        ])

        if present_count == 0:
            raise ValueError(
                "PreSyntaxReadinessResult requires exactly one: "
                "readiness_vector OR failure (both are None)"
            )

        if present_count > 1:
            raise ValueError(
                "PreSyntaxReadinessResult requires exactly one: "
                "readiness_vector OR failure (both are present)"
            )

    @property
    def is_success(self) -> bool:
        """Result represents successful readiness extraction."""
        return self.failure is None and self.readiness_vector is not None

    @property
    def is_failure(self) -> bool:
        """Result represents failed readiness extraction."""
        return self.failure is not None and self.readiness_vector is None


def create_presyntax_readiness_result(
    token_result: SignifierTokenResult
) -> PreSyntaxReadinessResult:
    """
    Extract PreSyntaxMufradVector from SignifierTokenResult.

    GARA-FT-1 boundary operation: SignifierTokenResult → PreSyntaxReadinessResult

    This operation:
    - Consumes SignifierTokenResult (input boundary)
    - Extracts PreSyntaxMufradVector from underlying MufradProof
    - Returns PreSyntaxReadinessResult (separate output boundary)
    - Does NOT modify SignifierTokenResult

    Constitutional Guarantees:
    -------------------------
    1. No semantic leak
    2. No syntax roles
    3. No case effects (only potentials)
    4. No applied operators (only trigger potentials)
    5. No relations
    6. No RelationCandidate or OperatorCandidate production
    7. SignifierTokenResult remains unchanged

    Parameters:
    ----------
    token_result : SignifierTokenResult
        Result from GARA-FT-0 boundary operation

    Returns:
    -------
    PreSyntaxReadinessResult
        Success result containing PreSyntaxMufradVector,
        or failure result if token_result failed or extraction failed

    Examples:
    --------
    >>> token_result = SignifierTokenResult(signifier_token=SignifierToken(...), ...)
    >>> readiness_result = create_presyntax_readiness_result(token_result)
    >>> readiness_result.is_success  # True
    >>> readiness_result.readiness_vector  # PreSyntaxMufradVector from MufradProof
    """
    if not isinstance(token_result, SignifierTokenResult):
        return PreSyntaxReadinessResult(
            source_token_result=SignifierTokenResult(
                signifier_token=None,
                failure=AlgebraicFailure(
                    reason=f"Expected SignifierTokenResult, got {type(token_result)}"
                )
            ),
            readiness_vector=None,
            failure=AlgebraicFailure(
                reason=f"Expected SignifierTokenResult, got {type(token_result)}"
            )
        )

    # Reject failed input
    if token_result.is_failure:
        return PreSyntaxReadinessResult(
            source_token_result=token_result,
            readiness_vector=None,
            failure=AlgebraicFailure(
                reason="Input SignifierTokenResult failed, cannot extract readiness"
            )
        )

    # Extract PreSyntaxMufradVector from underlying MufradProof
    try:
        signifier_token = token_result.signifier_token
        if signifier_token is None:
            return PreSyntaxReadinessResult(
                source_token_result=token_result,
                readiness_vector=None,
                failure=AlgebraicFailure(
                    reason="SignifierTokenResult has no signifier_token"
                )
            )

        mufrad_proof = signifier_token.proof

        # Extract PreSyntaxMufradVector using MufradProof's method
        readiness_vector = mufrad_proof.to_presyntax_vector()

        return PreSyntaxReadinessResult(
            source_token_result=token_result,
            readiness_vector=readiness_vector,
            failure=None
        )

    except (TypeError, ValueError, AttributeError) as e:
        return PreSyntaxReadinessResult(
            source_token_result=token_result,
            readiness_vector=None,
            failure=AlgebraicFailure(
                reason=f"PreSyntaxMufradVector extraction failed: {e}"
            )
        )


__all__ = [
    'PreSyntaxReadinessResult',
    'create_presyntax_readiness_result',
]
