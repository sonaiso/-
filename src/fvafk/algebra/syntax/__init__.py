"""Phase 4: Algebraic syntax operations.

النحو الجبري لا يحكم بالمعنى النهائي، بل يرخص علاقة تركيبية محفوظة الأثر والرتبة والبقايا.

This module implements governed syntax operations that return :class:`Result`
with full provenance (value + rank + evidence + residuals + failures + trace).

Syntax operations:

- :class:`MabniClosedOperatorOperation`: Identifies closed operators (مبني)
- :class:`MurabOpenCarrierOperation`: Treats معرب as open relational carrier
- :class:`AmilFunctionOperation`: Represents العامل as operating function
- :class:`IrabRelationEffectOperation`: Represents الإعراب as relational effect
- :class:`NisbahBindingOperation`: Binds syntactic relation candidates

All operations bridge SYNTAX → SYNTAX and never promote to SEMANTICS or HUKM
without passing through the governed boundary.

Residual taxonomy:

- ``syntax.context_absent`` — Surrounding tokens needed
- ``syntax.operator_scope_unresolved`` — Operator scope not determined
- ``syntax.case_missing`` — Case marking not visible
- ``syntax.case_estimated`` — Case marking estimated (تقدير)
- ``syntax.case_ambiguous`` — Multiple case readings possible
- ``syntax.governor_ambiguous`` — Multiple عامل candidates
- ``syntax.ellipsis_possible`` — Possible ellipsis (حذف)
- ``syntax.attachment_ambiguous`` — Unclear attachment
- ``syntax.relation_candidate`` — Relation type not finalized
- ``syntax.word_order_ambiguous`` — Multiple word order interpretations

Example usage::

    from fvafk.algebra.syntax import governed_mabni_operator

    result = governed_mabni_operator("لم")
    assert result.rank == Rank.CANDIDATE  # No evidence yet
    assert len(result.residuals) > 0      # Has residuals

    # With evidence from SyntaxAdapter
    from fvafk.algebra.adapters import SyntaxAdapter
    from fvafk.algebra import Evidence

    evidence = (Evidence(kind="syntax.operator", source="adapter:SyntaxAdapter:1"),)
    result = governed_mabni_operator("لم", evidence=evidence)
    assert result.rank == Rank.LICENSED   # Promoted with evidence
    assert len(result.residuals) > 0      # Still has residuals
"""

from __future__ import annotations

from .operations import (
    MabniClosedOperatorOperation,
    MurabOpenCarrierOperation,
    AmilFunctionOperation,
    IrabRelationEffectOperation,
    NisbahBindingOperation,
    governed_mabni_operator,
    governed_murab_carrier,
    governed_amil_function,
    governed_irab_effect,
    governed_nisbah_binding,
)

from .residual_taxonomy import (
    SYNTAX_RESIDUAL_KINDS,
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


__all__ = [
    # Operations
    "MabniClosedOperatorOperation",
    "MurabOpenCarrierOperation",
    "AmilFunctionOperation",
    "IrabRelationEffectOperation",
    "NisbahBindingOperation",
    # Convenience wrappers
    "governed_mabni_operator",
    "governed_murab_carrier",
    "governed_amil_function",
    "governed_irab_effect",
    "governed_nisbah_binding",
    # Residual taxonomy
    "SYNTAX_RESIDUAL_KINDS",
    "make_context_absent",
    "make_operator_scope_unresolved",
    "make_case_missing",
    "make_case_estimated",
    "make_case_ambiguous",
    "make_governor_ambiguous",
    "make_ellipsis_possible",
    "make_attachment_ambiguous",
    "make_relation_candidate",
    "make_word_order_ambiguous",
]
