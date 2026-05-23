"""
Prior Information Geometry - نظام المعلومات السابقة

Critical Architectural Correction:

NameRealityGate is NOT an isolated ontological gate.
NameRealityGate is a sub-gate inside the Prior Information System.

Why?

The question "Does this name refer to reality or usurp reality?"
cannot be answered from the name alone.
It must be answered from within the prior domain system.

PriorInformationGeometry Architecture:

PriorInformationGeometry =
    DomainRegistry
    + PriorInformationGate
    + PriorOpinionFilter
    + NameRealitySubGate (✓ NOT standalone)
    + EvidenceCompatibilityCheck
    + DomainTransferGuard
    + ResidualVector
    + RankPolicy
    + Trace

Critical Laws:

1. Reality is not "bare" - it enters via:
   - Effect (أثر)
   - Domain (مجال)
   - Prior information (معلومة سابقة)
   - Evidence (دليل)
   - Rank (رتبة)

2. A name usurps reality when prior information system fails to constrain it:
   - No domain
   - No referent candidate
   - No evidence
   - No rank
   - No residuals

3. RealityCandidate is NOT produced from raw name.
   RealityCandidate is produced only from scoped prior information
   and evidence-compatible referent binding.
"""

from .domain_candidate import DomainCandidate
from .prior_information_candidate import (
    PriorInformationCandidate,
    PriorContentType,
)
from .prior_opinion_candidate import (
    PriorOpinionCandidate,
    OpinionType,
)
from .reality_type import RealityType
from .named_reality_candidate import NamedRealityCandidate
from .prior_information_gate import (
    PriorInformationGate,
    PriorInformationGateResult,
    PriorInformationGateFailure,
    PriorInformationFailureKind,
)
from .name_reality_subgate import (
    NameRealitySubGate,
    NameRealitySubGateResult,
    NameRealitySubGateFailure,
    NameRealityFailureKind,
)
from .residuals import (
    PriorInformationResidualKind,
    make_prior_missing_domain_residual,
    make_prior_missing_source_residual,
    make_prior_missing_evidence_residual,
    make_prior_untestable_residual,
    make_prior_opinion_contamination_residual,
    make_name_only_residual,
    make_name_missing_referent_residual,
    make_name_missing_domain_residual,
    make_name_metaphor_as_external_residual,
    make_name_technical_without_domain_residual,
)

__all__ = [
    "DomainCandidate",
    "PriorInformationCandidate",
    "PriorContentType",
    "PriorOpinionCandidate",
    "OpinionType",
    "RealityType",
    "NamedRealityCandidate",
    "PriorInformationGate",
    "PriorInformationGateResult",
    "PriorInformationGateFailure",
    "PriorInformationFailureKind",
    "NameRealitySubGate",
    "NameRealitySubGateResult",
    "NameRealitySubGateFailure",
    "NameRealityFailureKind",
    "PriorInformationResidualKind",
    "make_prior_missing_domain_residual",
    "make_prior_missing_source_residual",
    "make_prior_missing_evidence_residual",
    "make_prior_untestable_residual",
    "make_prior_opinion_contamination_residual",
    "make_name_only_residual",
    "make_name_missing_referent_residual",
    "make_name_missing_domain_residual",
    "make_name_metaphor_as_external_residual",
    "make_name_technical_without_domain_residual",
]
