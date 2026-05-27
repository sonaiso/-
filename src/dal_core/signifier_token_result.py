"""
SignifierTokenResult (نتيجة الدال الوظيفي)

GARA-FT-0 Boundary Object - Constitutional implementation following PR #130.

This module implements the MINIMAL boundary object wrapper for MufradProof → SignifierToken
transformation, with strict constitutional prohibitions enforced.

CRITICAL PRINCIPLE:
This is a BOUNDARY OBJECT, not a complete tokenizer.
- Input: MufradProof only
- Output: SignifierTokenResult (wrapper containing token + optional readiness reference)
- Forbidden: Neural encodings, syntax relations, semantic interpretation, case effects

CONSTITUTIONAL LAWS ENFORCED:
1. No semantic leak (meaning/murad/madlul/semantic/ifadah/hukm)
2. No syntax roles (faail/mafool/mubtada/khabar/syntax_role)
3. No case effects (raf/nasb/jarr as grammatical judgments)
4. No applied operators (governed_by/governs/operator_applied)
5. No relations (ISN/TADMIN/TAQYID/relation/relation_type)
6. No RelationCandidate production (requires RelationAlgebraCore activation)

See: docs/GARA_FT_0_BOUNDARY_SPEC.md
"""

from dataclasses import dataclass
from typing import Optional

from dal_core.mufrad_proof import MufradProof
from dal_core.dal_algebra import AlgebraicFailure


# Constitutional prohibition registry
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


@dataclass(frozen=True)
class SignifierToken:
    """
    الدال الوظيفي - Operational Signifier Unit

    Constitutional Position:
    ----------------------
    - IS: Operational unit with licensed identity from MufradProof
    - IS: Wrapper around MufradProof for functional transformations
    - IS: Input to future PreSyntaxReadiness layer (GARA-FT-1)

    - IS NOT: Neural encoding (no GARA-T5)
    - IS NOT: Syntax node (no graph participation)
    - IS NOT: Applied operator (no governance)
    - IS NOT: Relation participant (no RelationCandidate)

    Allowed Fields:
    --------------
    - proof: MufradProof (immutable evidence)

    Forbidden Fields (enforced by frozen dataclass):
    ----------------
    - meaning, murad, madlul (semantic)
    - syntax_role, faail, mafool (syntax)
    - case_effect, raf, nasb (governance)
    - relation, isn, tadmin (composition)

    Usage:
    ------
    >>> proof = MufradProof(...)
    >>> token = SignifierToken(proof=proof)
    >>> token.proof.form  # Access underlying proof

    Constitutional Validation:
    -------------------------
    Frozen dataclass prevents field addition at runtime.
    Attempting to add forbidden fields raises AttributeError:

    >>> token.meaning = "book"  # AttributeError (frozen)
    >>> token.syntax_role = "faail"  # AttributeError (frozen)
    """

    proof: MufradProof  # Evidence from morphological layer

    def __post_init__(self):
        """
        Validate constitutional compliance.

        Ensures:
        1. Proof is valid MufradProof instance
        2. No semantic fields can be added (enforced by frozen=True)

        Raises:
            TypeError: If proof is not MufradProof
        """
        if not isinstance(self.proof, MufradProof):
            raise TypeError(
                f"SignifierToken requires MufradProof, got {type(self.proof)}"
            )


@dataclass(frozen=True)
class SignifierTokenResult:
    """
    نتيجة إنتاج الدال الوظيفي

    Result wrapper for GARA-FT-0 boundary operation.

    Constitutional Position:
    ----------------------
    - IS: Result wrapper containing operational outcome
    - IS: Bundle of (SignifierToken OR AlgebraicFailure)
    - IS: Boundary object enforcing constitutional prohibitions

    - IS NOT: The token itself (wrapper ≠ payload)
    - IS NOT: Neural result (no embeddings)
    - IS NOT: Syntax result (no relations)

    Result Semantics:
    ----------------
    A result is NOT the same as its payload:

    - Result = wrapper with success/failure discriminator
    - Payload = SignifierToken (the actual operational unit)

    This distinction is critical:
    >>> result = SignifierTokenResult(...)
    >>> isinstance(result, SignifierToken)  # False
    >>> isinstance(result.signifier_token, SignifierToken)  # True

    Mutual Exclusion:
    ----------------
    Exactly ONE of the following must be non-None:
    - signifier_token (success)
    - failure (failure)

    Both cannot be present simultaneously.

    Fields:
    ------
    - signifier_token: Optional[SignifierToken]
      The operational signifier unit (present on success)

    - failure: Optional[AlgebraicFailure]
      Algebraic failure reason (present on failure)

    Usage:
    ------
    Success case:
    >>> result = SignifierTokenResult(
    ...     signifier_token=SignifierToken(proof=proof),
    ...     failure=None
    ... )
    >>> result.is_success  # True
    >>> result.signifier_token.proof  # Access proof

    Failure case:
    >>> result = SignifierTokenResult(
    ...     signifier_token=None,
    ...     failure=AlgebraicFailure(reason="Constitutional violation")
    ... )
    >>> result.is_failure  # True
    >>> result.failure.reason  # Access reason

    Constitutional Guarantees:
    -------------------------
    1. No RelationCandidate production (not in scope)
    2. No semantic fields (meaning/murad/madlul)
    3. No syntax roles (faail/mafool)
    4. No case effects (raf/nasb/jarr)
    5. No applied operators (governed_by)
    6. No relations (ISN/TADMIN/TAQYID)

    These are enforced by:
    - Frozen dataclass (no runtime field addition)
    - Minimal field set (only token + failure)
    - Constitutional tests (test_signifier_token_result.py)
    """

    signifier_token: Optional[SignifierToken]
    failure: Optional[AlgebraicFailure]

    def __post_init__(self):
        """
        Validate result mutual exclusion invariant.

        Ensures exactly one of:
        - signifier_token (success)
        - failure (failure)

        is present.

        Raises:
            ValueError: If both present or both absent
        """
        present_count = sum([
            self.signifier_token is not None,
            self.failure is not None
        ])

        if present_count == 0:
            raise ValueError(
                "SignifierTokenResult requires exactly one: "
                "signifier_token OR failure (both are None)"
            )

        if present_count > 1:
            raise ValueError(
                "SignifierTokenResult requires exactly one: "
                "signifier_token OR failure (both are present)"
            )

    @property
    def is_success(self) -> bool:
        """Result represents successful token construction."""
        return self.failure is None and self.signifier_token is not None

    @property
    def is_failure(self) -> bool:
        """Result represents failed token construction."""
        return self.failure is not None and self.signifier_token is None


def create_signifier_token_result(
    proof: MufradProof
) -> SignifierTokenResult:
    """
    Convert MufradProof to SignifierTokenResult.

    GARA-FT-0 boundary operation: MufradProof → SignifierTokenResult

    This is the MINIMAL transformation:
    - Wraps MufradProof in SignifierToken
    - Returns success result
    - No complex transformations
    - No neural encodings
    - No syntax analysis

    Constitutional Guarantees:
    -------------------------
    1. No semantic leak
    2. No syntax roles
    3. No case effects
    4. No relations
    5. No RelationCandidate production

    Parameters:
    ----------
    proof : MufradProof
        Morphologically complete singular word proof

    Returns:
    -------
    SignifierTokenResult
        Success result containing SignifierToken wrapper,
        or failure result if proof invalid

    Examples:
    --------
    >>> proof = MufradProof(...)  # From morphological layer
    >>> result = create_signifier_token_result(proof)
    >>> result.is_success  # True
    >>> result.signifier_token.proof == proof  # True
    """
    if not isinstance(proof, MufradProof):
        return SignifierTokenResult(
            signifier_token=None,
            failure=AlgebraicFailure(
                reason=f"Expected MufradProof, got {type(proof)}"
            )
        )

    try:
        token = SignifierToken(proof=proof)
        return SignifierTokenResult(
            signifier_token=token,
            failure=None
        )
    except (TypeError, ValueError) as e:
        return SignifierTokenResult(
            signifier_token=None,
            failure=AlgebraicFailure(
                reason=f"SignifierToken construction failed: {e}"
            )
        )


__all__ = [
    'SignifierToken',
    'SignifierTokenResult',
    'create_signifier_token_result',
]
