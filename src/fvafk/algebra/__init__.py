"""``fvafk.algebra`` — Arabic correspondence-preserving algebra (Phase 0).

A typed algebraic layer on top of FVAFK that enforces the constitution::

    لا مخرج عارٍ.
    Every Result = value + rank + evidence + residuals + failures + replay.

The package is intentionally standalone in Phase 0: it does not import
from ``fvafk.c1`` / ``c2a`` / ``c2b`` / ``syntax``. Phase 2 of
``docs/ARABIC_ALGEBRA_ROADMAP.md`` introduces the adapters that feed
results from those layers in as :class:`Evidence`.

Public surface
--------------

Core primitives:

- :class:`Trace`, :class:`Domain`, :class:`Carrier`
- :class:`Evidence`, :class:`Residual`, :class:`Failure`
- :class:`Rank`, :class:`Result`
- :class:`Operation` (protocol)

Bridges and policy:

- :class:`CPB`, :func:`validate_cpb`
- :class:`Policy`, :func:`default_policy`, :func:`apply_policy`

Analyzers and learners:

- :class:`ArabicAlgebraDecisionTree`, :class:`AnalysisReport`
- :class:`CodeChange`, :class:`CodeLearningTrace`
- :class:`ProblemTrace`, :class:`PatchProposal`, :class:`CodeLearningDecision`
- :class:`GovernedCodeLearningLoop`
- :class:`KnowledgeStore`

Governance and inspection:

- :class:`InspectionArtifact`, :class:`InspectionFinding`
- :class:`InspectionResidual`, :class:`InspectionReport`
- :class:`InspectionResidualKind`
- :func:`make_inspection_result`, :func:`inspection_result_to_legacy_dict`
"""

from __future__ import annotations

from .arabic_layers import (
    ALLOWED_BRIDGES,
    CANONICAL_ALLOWED_BRIDGES,
    CANONICAL_FORBIDDEN_BRIDGES,
    FORBIDDEN_BRIDGES,
    Domain,
    is_bridge_allowed,
    is_canonical_bridge_allowed,
    is_legacy_bridge_allowed,
)
from .code_learning import CodeChange, CodeLearningTrace
from .code_learning_loop import (
    CodeLearningDecision,
    GovernedCodeLearningLoop,
    PatchProposal,
    ProblemTrace,
)
from .core import (
    Carrier,
    Evidence,
    Failure,
    Operation,
    Rank,
    Residual,
    Result,
    Trace,
    empty_result,
)
from .cpb import CPB, validate_cpb
from .decision_tree import AnalysisReport, ArabicAlgebraDecisionTree
from .governance import (
    InspectionArtifact,
    InspectionFinding,
    InspectionResidual,
    InspectionReport,
    InspectionResidualKind,
    make_inspection_result,
    inspection_result_to_legacy_dict,
)
from .learning import KnowledgeStore
from .policies import Policy, apply_policy, default_policy

__all__ = [
    # arabic_layers
    "ALLOWED_BRIDGES",
    "FORBIDDEN_BRIDGES",
    "CANONICAL_ALLOWED_BRIDGES",
    "CANONICAL_FORBIDDEN_BRIDGES",
    "Domain",
    "is_bridge_allowed",
    "is_canonical_bridge_allowed",
    "is_legacy_bridge_allowed",
    # core
    "Carrier",
    "Evidence",
    "Failure",
    "Operation",
    "Rank",
    "Residual",
    "Result",
    "Trace",
    "empty_result",
    # cpb
    "CPB",
    "validate_cpb",
    # policies
    "Policy",
    "apply_policy",
    "default_policy",
    # decision_tree
    "AnalysisReport",
    "ArabicAlgebraDecisionTree",
    # code_learning
    "CodeChange",
    "CodeLearningTrace",
    # code_learning_loop
    "ProblemTrace",
    "PatchProposal",
    "CodeLearningDecision",
    "GovernedCodeLearningLoop",
    # learning
    "KnowledgeStore",
    # governance
    "InspectionArtifact",
    "InspectionFinding",
    "InspectionResidual",
    "InspectionReport",
    "InspectionResidualKind",
    "make_inspection_result",
    "inspection_result_to_legacy_dict",
]
