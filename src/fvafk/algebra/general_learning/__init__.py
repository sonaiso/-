"""General Learning: Rule-Learning Geometry for Algebraic Proofs.

Central Law:
    التعلم الذاتي ليس وظيفة اختيارية داخل الجبر العام؛
    بل هو البرهان أن الجبر عام.

    "Self-learning is not an optional feature within general algebra;
    it is the proof that the algebra is general."

Architecture:
    This module implements the **rule-learning geometry** that proves the
    algebra is general by demonstrating that:

    1. Rules are not merely declared - they are **learned from origins**
    2. Rules are tested on examples (positive and constraining)
    3. Rules face **counterexamples** and must adapt
    4. Rules are **refined** with explicit scope/constraints
    5. Rule modifications preserve **traces, residuals, and ranks**
    6. Rule changes are **explained** (why promoted, demoted, refined)

The Seven Components:
    1. **origin.py** — Extract invariant patterns from positive examples
    2. **invariant.py** — Detect stable features across examples
    3. **manaat.py** — Determine scope/basis (المناط) of rule application
    4. **rule_candidate.py** — Rule structure with evidence/rank/residuals
    5. **learner.py** — Self-learning loop with modification
    6. **verification.py** — Counterexample detection and refinement
    7. **explanation.py** — Explain why rules changed
    8. **residual_taxonomy.py** — Learning-specific residual types

Target Experiment (فاعل Pattern):
    Positive origins:
        كاتب (writer), زارع (farmer), عامل (worker)

    Initial rule candidate:
        "وزن فاعل يرشح علاقة فاعلية"
        "فاعل pattern licenses agentive relation"

    Constraining examples:
        طاهر (pure), حامض (sour), بارد (cold), كريم (generous), حكيم (wise)

    Expected refinement:
        "فاعل does not always indicate actual agency;
         it licenses agentive OR qualitative interpretation
         based on source event, lexicalization, usage, and context"

Guard:
    No rule may be learned without:
        - Origin examples (أصول موجبة)
        - Invariant extraction (استخراج الثابت)
        - Scope determination (تحديد المناط)
        - Counterexample testing (اختبار الأمثلة المقيّدة)
        - Modification trace (أثر التعديل)
        - Residual tracking (حفظ البقايا)
        - Rank history (رتبة التاريخ)
        - Explanation (التفسير)
"""

from __future__ import annotations

from .origin import Origin, OriginSet, extract_origin, make_origin_set
from .invariant import Invariant, InvariantKind, detect_invariants
from .manaat import Manaat, ManaatScope, determine_manaat
from .rule_candidate import RuleCandidate, RuleStatus, RuleModification, RefinementPolicy, make_rule_candidate
from .learner import GeneralLearner, LearningCycle
from .verification import verify_rule, detect_counterexamples, Counterexample, CounterexampleKind, VerificationResult
from .explanation import Explanation, ExplanationKind, explain_modification, explain_rank_change, explain_counterexample_handling
from .residual_taxonomy import (
    LearningResidual,
    make_origin_insufficient,
    make_invariant_unclear,
    make_manaat_ambiguous,
    make_counterexample_unresolved,
    make_counterexample_search_incomplete,
)

__all__ = [
    # Origin
    "Origin",
    "OriginSet",
    "extract_origin",
    "make_origin_set",
    # Invariant
    "Invariant",
    "InvariantKind",
    "detect_invariants",
    # Manaat
    "Manaat",
    "ManaatScope",
    "determine_manaat",
    # Rule Candidate
    "RuleCandidate",
    "RuleStatus",
    "RuleModification",
    "RefinementPolicy",
    "make_rule_candidate",
    # Learner
    "GeneralLearner",
    "LearningCycle",
    # Verification
    "verify_rule",
    "detect_counterexamples",
    "Counterexample",
    "CounterexampleKind",
    "VerificationResult",
    # Explanation
    "Explanation",
    "ExplanationKind",
    "explain_modification",
    "explain_rank_change",
    "explain_counterexample_handling",
    # Residuals
    "LearningResidual",
    "make_origin_insufficient",
    "make_invariant_unclear",
    "make_manaat_ambiguous",
    "make_counterexample_unresolved",
    "make_counterexample_search_incomplete",
]
