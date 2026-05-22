"""
Lafzi Wadh Module - الوضع اللفظي

Critical Law:
    الوضع ليس معنى معجمي مباشر
    Wadh is NOT direct lexical meaning injection.

This module implements WadhGeometry definitions for PR-L5A.

What PR-L5A Implements:
    - WadhSource classification
    - WadhTransmissionMode classification
    - WadhScope classification
    - WadhEvidence structure
    - WadhClaim structure
    - MawduLahStructure (placed-for candidate)
    - WadhResidual taxonomy

What PR-L5A Does NOT Implement:
    - WadhGate (→ PR-L5B)
    - Full Dalālah (→ PR-L6+)
    - Mutabaqah/Tadammun/Iltizam classification (→ PR-L6+)
    - Haqiqah/Majaz/Naql classification (→ PR-L7+)
    - HUKM issuance (→ Future)
    - Learning (→ Future)

Critical Laws Enforced:
    1. Lexicon report is evidence, NOT Wadh itself
    2. Reason alone CANNOT certify Arabic Wadh (requires transmission)
    3. WadhClaim does NOT create external meaning
    4. WadhClaim does NOT create full Dalālah
    5. WadhClaim does NOT issue HUKM
    6. WadhClaim does NOT classify Mutabaqah/Tadammun/Iltizam
    7. WadhClaim does NOT classify Haqiqah/Majaz/Naql
    8. MawduLahStructure is NOT external truth
    9. Unknown source/transmission/scope becomes residual
    10. Original Wadh unobserved becomes residual

Position in Architecture:
    RationalMethod
    └── NeutralBinding
        └── StyleSpec(LAFZI_DALALI)
            └── LafziMadlul Registration
                └── LafziTrace
                    ├── DālCandidate
                    └── MadlulLafziCandidate
                        └── DalMadlulBindingCandidate (PR-L4, certified)
                            └── WadhGeometry (PR-L5A) ← THIS MODULE
                                ├── WadhSource
                                ├── WadhTransmissionMode
                                ├── WadhScope
                                ├── WadhEvidence
                                ├── WadhClaim
                                ├── MawduLahStructure
                                └── WadhResidual
"""

from __future__ import annotations

# Source classification
from .wadh_source import (
    WadhSourceKind,
    WadhSource,
    make_lexicon_report_source,
    make_usage_attestation_source,
    make_explicit_stipulation_source,
    make_reason_inference_source,
    make_unknown_source,
)

# Transmission mode classification
from .wadh_transmission_mode import (
    WadhTransmissionKind,
    WadhTransmissionMode,
    make_riwayah_mode,
    make_naql_mode,
    make_usage_mode,
    make_istidlal_mode,
    make_unknown_mode,
)

# Scope classification
from .wadh_scope import (
    WadhScopeKind,
    WadhScope,
    make_lafzi_arabic_scope,
    make_lafzi_scope,
    make_istilahy_scope,
    make_urfi_scope,
    make_unknown_scope,
)

# Residual taxonomy
from .residual_taxonomy import (
    WadhResidualKind,
    WadhResidual,
    make_unknown_source_residual,
    make_unknown_transmission_residual,
    make_unknown_scope_residual,
    make_reason_alone_residual,
    make_original_wadh_unobserved_residual,
    make_binding_trace_lost_residual,
    make_external_meaning_injection_residual,
)

# Evidence structure
from .wadh_evidence import WadhEvidence

# Claim structures
from .wadh_claim import (
    WadhClaim,
    WadhClaimFailure,
    WadhClaimResult,
)

# MawduLah structure
from .mawdu_lah_structure import MawduLahStructure


__all__ = [
    # Source
    "WadhSourceKind",
    "WadhSource",
    "make_lexicon_report_source",
    "make_usage_attestation_source",
    "make_explicit_stipulation_source",
    "make_reason_inference_source",
    "make_unknown_source",

    # Transmission mode
    "WadhTransmissionKind",
    "WadhTransmissionMode",
    "make_riwayah_mode",
    "make_naql_mode",
    "make_usage_mode",
    "make_istidlal_mode",
    "make_unknown_mode",

    # Scope
    "WadhScopeKind",
    "WadhScope",
    "make_lafzi_arabic_scope",
    "make_lafzi_scope",
    "make_istilahy_scope",
    "make_urfi_scope",
    "make_unknown_scope",

    # Residuals
    "WadhResidualKind",
    "WadhResidual",
    "make_unknown_source_residual",
    "make_unknown_transmission_residual",
    "make_unknown_scope_residual",
    "make_reason_alone_residual",
    "make_original_wadh_unobserved_residual",
    "make_binding_trace_lost_residual",
    "make_external_meaning_injection_residual",

    # Evidence
    "WadhEvidence",

    # Claim
    "WadhClaim",
    "WadhClaimFailure",
    "WadhClaimResult",

    # MawduLah
    "MawduLahStructure",
]
