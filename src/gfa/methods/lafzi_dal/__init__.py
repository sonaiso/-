"""
Lafzi Dal Module - بوابة الدال

PR-L3: Pure Dāl Geometry Contract

Critical Law:
    الدال المرخّص له هندسة كاملة قبل السؤال عن معناه
    A licensed signifier has complete geometry before asking about meaning.

PR-L3 Purpose:
    Implement DalCandidate as fully-licensed linguistic signifier
    with complete geometric structure from C1→C2a→C2b pipeline.

What This Module Does:
    - Creates complete DalCandidate with 13 mandatory fields
    - Validates phonic carriers, haraka operations, syllables
    - Detects boundaries, clitics, patterns
    - Classifies path type, pattern status, terminal state
    - Projects syntactic readiness and role candidates
    - Preserves trace_id and residuals
    - Returns governed candidate results
    - Enforces 7 forbidden fields (no meaning/dalalah/wadh/hukm)

What This Module Does NOT Do:
    - Does NOT create meaning
    - Does NOT create Madlul (المدلول)
    - Does NOT create Dalalah (الدلالة)
    - Does NOT implement Wadh (الوضع)
    - Does NOT issue HUKM
    - Does NOT raise PredicateRank
    - Does NOT create semantic content
    - Does NOT perform learning
    - Does NOT implement upward transitions
    - Does NOT implement downward decomposition

Position in Architecture:
    C1 (Encoding)
    → C2a (Phonology Gates)
    → C2b (Morphology)
    → DalCandidate (PR-L3) ← THIS MODULE
        → DalMadlulBinding (PR-L4)
            → WadhGate (PR-L5)
                → Dālālah (future)

Critical:
    DalCandidate is a fully-licensed signifier candidate with complete
    geometric structure, not semantic execution. It is hardened input
    to PR-L4 binding, protected by 13 mandatory fields and 7 forbidden
    fields.
"""

from .dal_type import DalType
from .dal_structures import (
    # Phonic
    PhonicCarrier,
    # Haraka
    HarakaOperationType,
    HarakaOperation,
    # Syllable
    SyllableType,
    SyllableLicense,
    # Boundaries
    WordBoundaryInfo,
    # Clitics
    Clitic,
    CliticAnalysis,
    # Formulas
    FormulaClass,
    FormulaCandidate,
    # Classification
    PathType,
    PatternStatus,
    TerminalState,
    SyntacticReadiness,
    SentenceShape,
    # Roles
    RoleType,
    RoleProjection,
)
from .dal_candidate import DalCandidate, DalResult
from .dal_gate import DalGate, DalFailure
from .residual_taxonomy import (
    DalFailureKind,
    DalResidual,
    make_missing_lafzi_trace_residual,
    make_missing_registration_residual,
    make_missing_style_spec_residual,
    make_wrong_domain_residual,
    make_missing_neutral_binding_residual,
    make_trace_not_preserved_residual,
    make_residuals_not_preserved_residual,
    make_unknown_dal_type_residual,
    make_meaning_creation_attempted_residual,
    make_madlul_creation_attempted_residual,
    make_dalalah_creation_attempted_residual,
    make_wadh_implementation_attempted_residual,
    make_hukm_issuance_attempted_residual,
    make_rank_inflation_attempted_residual,
)

__all__ = [
    # Signifier types
    "DalType",
    # PR-L3 Structures
    "PhonicCarrier",
    "HarakaOperationType",
    "HarakaOperation",
    "SyllableType",
    "SyllableLicense",
    "WordBoundaryInfo",
    "Clitic",
    "CliticAnalysis",
    "FormulaClass",
    "FormulaCandidate",
    "PathType",
    "PatternStatus",
    "TerminalState",
    "SyntacticReadiness",
    "SentenceShape",
    "RoleType",
    "RoleProjection",
    # Core candidate
    "DalCandidate",
    "DalResult",
    # Gate
    "DalGate",
    "DalFailure",
    # Residual taxonomy
    "DalFailureKind",
    "DalResidual",
    "make_missing_lafzi_trace_residual",
    "make_missing_registration_residual",
    "make_missing_style_spec_residual",
    "make_wrong_domain_residual",
    "make_missing_neutral_binding_residual",
    "make_trace_not_preserved_residual",
    "make_residuals_not_preserved_residual",
    "make_unknown_dal_type_residual",
    "make_meaning_creation_attempted_residual",
    "make_madlul_creation_attempted_residual",
    "make_dalalah_creation_attempted_residual",
    "make_wadh_implementation_attempted_residual",
    "make_hukm_issuance_attempted_residual",
    "make_rank_inflation_attempted_residual",
]
