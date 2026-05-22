"""
Rational Method Kernel - الطريقة العقلية

Core Nabhani Principle:
    العقل = نقل الحس بالواقع إلى الدماغ + معلومات سابقة

The RationalMethod is the governing root of all thinking methods.

Four Pillars (الأركان الأربعة):
    1. Reality (الواقع)
    2. Sensory Transfer (نقل الحس)
    3. Cognitive Carrier (الدماغ الصالح)
    4. Prior Information (المعلومات السابقة)

Critical Laws:
    - No thought without all four pillars
    - Prior information ≠ Prior opinion
    - Prior opinion must be excluded
    - Judgment preserves trace and residuals
    - Existence rank does not certify predicate rank
    - Failures return governed objects, not bare exceptions
"""

from .prior_filter import (
    PriorInformation,
    PriorOpinion,
    FilteredPrior,
    filter_prior,
)

from .residual_taxonomy import (
    RationalResidual,
    RationalResidualKind,
)

from .aql_operation import (
    AqlOperation,
    AqlOperationInput,
    AqlOperationResult,
)

from .judgment import (
    AqlJudgment,
    ExistenceRank,
    PredicateRank,
)

from .rational_method import (
    RationalMethod,
)

from .neutral_binding import (
    NeutralBinding,
    NeutralBindingInput,
    NeutralBindingResult,
    NeutralBindingFailure,
)

__all__ = [
    "PriorInformation",
    "PriorOpinion",
    "FilteredPrior",
    "filter_prior",
    "RationalResidual",
    "RationalResidualKind",
    "AqlOperation",
    "AqlOperationInput",
    "AqlOperationResult",
    "AqlJudgment",
    "ExistenceRank",
    "PredicateRank",
    "RationalMethod",
    "NeutralBinding",
    "NeutralBindingInput",
    "NeutralBindingResult",
    "NeutralBindingFailure",
]
