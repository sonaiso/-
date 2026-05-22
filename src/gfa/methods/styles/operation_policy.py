"""
OperationPolicy - سياسة العمليات

Defines what operations are allowed or forbidden in each domain.

Nabhani Core Principle:
    العمليات تتقيد بالمجال
    Operations are constrained by domain.

Critical Laws:
    1. Each domain has allowed operations
    2. Each domain has forbidden operations
    3. Forbidden operations are blocked with governed failure
    4. Operation policy does NOT execute operations
    5. Operation policy only declares constraints

Position:
    OperationPolicy is declaration layer, not execution layer.
    OperationPolicy does NOT perform operations.
    OperationPolicy only declares allowed/forbidden.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .domain_spec import ThinkingDomain


class OperationKind(Enum):
    """
    Kinds of operations that may occur in reasoning.

    Different domains allow different operations.
    """

    # Rational operations (all domains)
    BIND = "bind"  # Neutral binding
    FILTER_PRIOR = "filter_prior"  # Prior filtering
    PRESERVE_TRACE = "preserve_trace"  # Trace preservation

    # Experimental operations (material domain)
    MEASURE = "measure"
    OBSERVE = "observe"
    EXPERIMENT = "experiment"

    # Logical operations (formal domain)
    DERIVE = "derive"
    PROVE = "prove"
    REFUTE = "refute"

    # Linguistic operations (lafzi domain)
    PARSE = "parse"
    BIND_WADH = "bind_wadh"  # Bind وضع
    BIND_ISTIMAL = "bind_istimal"  # Bind استعمال
    EXTRACT_DAL = "extract_dal"  # Extract دال
    INFER_MADLUL = "infer_madlul"  # Infer مدلول

    # Textual operations (normative domain)
    INTERPRET_NASS = "interpret_nass"  # Interpret نص
    APPLY_QIYAS = "apply_qiyas"  # Apply قياس
    CONSULT_IJMA = "consult_ijma"  # Consult إجماع

    # Programming operations (execution domain)
    EXECUTE = "execute"
    TYPE_CHECK = "type_check"
    COMPILE = "compile"
    TEST = "test"

    # Forbidden meta-operations (for all styles)
    CREATE_MEANING = "create_meaning"  # FORBIDDEN
    ISSUE_HUKM = "issue_hukm"  # FORBIDDEN (only RationalMethod)
    CERTIFY_WITHOUT_EVIDENCE = "certify_without_evidence"  # FORBIDDEN
    INFLATE_RANK = "inflate_rank"  # FORBIDDEN
    JUMP_DOMAIN = "jump_domain"  # FORBIDDEN without bridge


@dataclass(frozen=True)
class AllowedOperation:
    """
    An operation that is allowed in a domain.
    """
    kind: OperationKind
    description: str
    requires_evidence: bool = True


@dataclass(frozen=True)
class ForbiddenOperation:
    """
    An operation that is forbidden in a domain.
    """
    kind: OperationKind
    reason: str
    severity: str = "blocker"  # "blocker", "high", "medium"


@dataclass(frozen=True)
class OperationPolicy:
    """
    Policy governing operations in a domain.

    OperationPolicy declares what operations are allowed or forbidden.
    It does NOT execute operations.
    It does NOT perform reasoning.

    Critical Laws:
        - OperationPolicy is domain-bound
        - OperationPolicy does NOT execute operations
        - OperationPolicy does NOT implement ScientificMethod
        - OperationPolicy does NOT implement LogicalStyle
        - OperationPolicy does NOT implement LafziMadlul
        - OperationPolicy only declares constraints
        - Forbidden operations are blocked with governed failure
    """
    domain: ThinkingDomain

    # Operations allowed in this domain
    allowed_operations: frozenset[AllowedOperation]

    # Operations forbidden in this domain
    forbidden_operations: frozenset[ForbiddenOperation]

    def __post_init__(self):
        """Validate operation policy construction."""
        # Check no overlap between allowed and forbidden
        allowed_kinds = {op.kind for op in self.allowed_operations}
        forbidden_kinds = {op.kind for op in self.forbidden_operations}

        overlap = allowed_kinds & forbidden_kinds
        if overlap:
            raise ValueError(
                f"Operations cannot be both allowed and forbidden: {overlap}"
            )

    def allows_operation(self, kind: OperationKind) -> bool:
        """Check if operation is allowed in this domain."""
        return any(op.kind == kind for op in self.allowed_operations)

    def forbids_operation(self, kind: OperationKind) -> bool:
        """Check if operation is forbidden in this domain."""
        return any(op.kind == kind for op in self.forbidden_operations)

    def get_forbidden_operation(self, kind: OperationKind) -> ForbiddenOperation | None:
        """Get forbidden operation details if operation is forbidden."""
        for op in self.forbidden_operations:
            if op.kind == kind:
                return op
        return None

    def is_blocker(self, kind: OperationKind) -> bool:
        """Check if forbidden operation is a blocker."""
        forbidden = self.get_forbidden_operation(kind)
        return forbidden is not None and forbidden.severity == "blocker"


# Common forbidden operations for all style specs

UNIVERSAL_FORBIDDEN_OPERATIONS = frozenset([
    ForbiddenOperation(
        kind=OperationKind.CREATE_MEANING,
        reason="StyleSpec does not create meaning",
        severity="blocker"
    ),
    ForbiddenOperation(
        kind=OperationKind.ISSUE_HUKM,
        reason="StyleSpec does not issue judgment",
        severity="blocker"
    ),
    ForbiddenOperation(
        kind=OperationKind.CERTIFY_WITHOUT_EVIDENCE,
        reason="StyleSpec does not certify without evidence",
        severity="blocker"
    ),
    ForbiddenOperation(
        kind=OperationKind.INFLATE_RANK,
        reason="StyleSpec does not inflate rank",
        severity="blocker"
    ),
    ForbiddenOperation(
        kind=OperationKind.JUMP_DOMAIN,
        reason="StyleSpec does not allow domain jump without bridge",
        severity="blocker"
    ),
])

# Common allowed operations for all domains

UNIVERSAL_ALLOWED_OPERATIONS = frozenset([
    AllowedOperation(
        kind=OperationKind.BIND,
        description="Neutral binding (from RationalMethod)",
        requires_evidence=False
    ),
    AllowedOperation(
        kind=OperationKind.FILTER_PRIOR,
        description="Filter prior information from opinion",
        requires_evidence=False
    ),
    AllowedOperation(
        kind=OperationKind.PRESERVE_TRACE,
        description="Preserve trace and residuals",
        requires_evidence=False
    ),
])


# Factory functions for domain-specific policies

def make_material_operation_policy() -> OperationPolicy:
    """Create operation policy for material/experimental domain."""
    allowed = UNIVERSAL_ALLOWED_OPERATIONS | frozenset([
        AllowedOperation(
            kind=OperationKind.MEASURE,
            description="Measure physical quantities",
            requires_evidence=True
        ),
        AllowedOperation(
            kind=OperationKind.OBSERVE,
            description="Observe physical phenomena",
            requires_evidence=True
        ),
        AllowedOperation(
            kind=OperationKind.EXPERIMENT,
            description="Conduct controlled experiments",
            requires_evidence=True
        ),
    ])

    forbidden = UNIVERSAL_FORBIDDEN_OPERATIONS | frozenset([
        ForbiddenOperation(
            kind=OperationKind.PROVE,
            reason="Material domain uses observation, not formal proof",
            severity="high"
        ),
        ForbiddenOperation(
            kind=OperationKind.INTERPRET_NASS,
            reason="Material domain does not interpret textual sources",
            severity="blocker"
        ),
    ])

    return OperationPolicy(
        domain=ThinkingDomain.MATERIAL_EXPERIMENTAL,
        allowed_operations=allowed,
        forbidden_operations=forbidden,
    )


def make_formal_operation_policy() -> OperationPolicy:
    """Create operation policy for formal/logical domain."""
    allowed = UNIVERSAL_ALLOWED_OPERATIONS | frozenset([
        AllowedOperation(
            kind=OperationKind.DERIVE,
            description="Derive conclusions from axioms",
            requires_evidence=True
        ),
        AllowedOperation(
            kind=OperationKind.PROVE,
            description="Construct formal proofs",
            requires_evidence=True
        ),
        AllowedOperation(
            kind=OperationKind.REFUTE,
            description="Refute claims via counterexample",
            requires_evidence=True
        ),
    ])

    forbidden = UNIVERSAL_FORBIDDEN_OPERATIONS | frozenset([
        ForbiddenOperation(
            kind=OperationKind.MEASURE,
            reason="Formal domain does not measure physical quantities",
            severity="blocker"
        ),
        ForbiddenOperation(
            kind=OperationKind.EXPERIMENT,
            reason="Formal domain does not conduct experiments",
            severity="blocker"
        ),
    ])

    return OperationPolicy(
        domain=ThinkingDomain.FORMAL_LOGICAL,
        allowed_operations=allowed,
        forbidden_operations=forbidden,
    )


def make_lafzi_operation_policy() -> OperationPolicy:
    """
    Create operation policy for lafzi/dalali domain.

    This is DECLARATION ONLY.
    Actual LafziMadlul implementation is NOT part of this PR.
    """
    allowed = UNIVERSAL_ALLOWED_OPERATIONS | frozenset([
        AllowedOperation(
            kind=OperationKind.PARSE,
            description="Parse linguistic structure",
            requires_evidence=False
        ),
        AllowedOperation(
            kind=OperationKind.BIND_WADH,
            description="Bind وضع (conventional meaning)",
            requires_evidence=True
        ),
        AllowedOperation(
            kind=OperationKind.BIND_ISTIMAL,
            description="Bind استعمال (usage)",
            requires_evidence=True
        ),
        AllowedOperation(
            kind=OperationKind.EXTRACT_DAL,
            description="Extract دال (signifier)",
            requires_evidence=False
        ),
        AllowedOperation(
            kind=OperationKind.INFER_MADLUL,
            description="Infer مدلول (signified)",
            requires_evidence=True
        ),
    ])

    forbidden = UNIVERSAL_FORBIDDEN_OPERATIONS | frozenset([
        ForbiddenOperation(
            kind=OperationKind.MEASURE,
            reason="Linguistic domain does not measure",
            severity="blocker"
        ),
        ForbiddenOperation(
            kind=OperationKind.PROVE,
            reason="Linguistic domain does not use formal proof",
            severity="high"
        ),
        ForbiddenOperation(
            kind=OperationKind.EXECUTE,
            reason="Linguistic domain does not execute code",
            severity="blocker"
        ),
    ])

    return OperationPolicy(
        domain=ThinkingDomain.LAFZI_DALALI,
        allowed_operations=allowed,
        forbidden_operations=forbidden,
    )


def make_textual_operation_policy() -> OperationPolicy:
    """Create operation policy for textual/normative domain."""
    allowed = UNIVERSAL_ALLOWED_OPERATIONS | frozenset([
        AllowedOperation(
            kind=OperationKind.INTERPRET_NASS,
            description="Interpret نص (text)",
            requires_evidence=True
        ),
        AllowedOperation(
            kind=OperationKind.APPLY_QIYAS,
            description="Apply قياس (analogical reasoning)",
            requires_evidence=True
        ),
        AllowedOperation(
            kind=OperationKind.CONSULT_IJMA,
            description="Consult إجماع (consensus)",
            requires_evidence=True
        ),
    ])

    forbidden = UNIVERSAL_FORBIDDEN_OPERATIONS | frozenset([
        ForbiddenOperation(
            kind=OperationKind.MEASURE,
            reason="Normative domain does not measure",
            severity="blocker"
        ),
        ForbiddenOperation(
            kind=OperationKind.EXPERIMENT,
            reason="Normative domain does not experiment",
            severity="blocker"
        ),
        ForbiddenOperation(
            kind=OperationKind.EXECUTE,
            reason="Normative domain does not execute code",
            severity="blocker"
        ),
    ])

    return OperationPolicy(
        domain=ThinkingDomain.TEXTUAL_NORMATIVE,
        allowed_operations=allowed,
        forbidden_operations=forbidden,
    )


def make_programming_operation_policy() -> OperationPolicy:
    """Create operation policy for programming/execution domain."""
    allowed = UNIVERSAL_ALLOWED_OPERATIONS | frozenset([
        AllowedOperation(
            kind=OperationKind.EXECUTE,
            description="Execute code",
            requires_evidence=False
        ),
        AllowedOperation(
            kind=OperationKind.TYPE_CHECK,
            description="Type check code",
            requires_evidence=False
        ),
        AllowedOperation(
            kind=OperationKind.COMPILE,
            description="Compile code",
            requires_evidence=False
        ),
        AllowedOperation(
            kind=OperationKind.TEST,
            description="Run tests",
            requires_evidence=False
        ),
    ])

    forbidden = UNIVERSAL_FORBIDDEN_OPERATIONS | frozenset([
        ForbiddenOperation(
            kind=OperationKind.INTERPRET_NASS,
            reason="Programming domain does not interpret text",
            severity="blocker"
        ),
        ForbiddenOperation(
            kind=OperationKind.APPLY_QIYAS,
            reason="Programming domain does not use qiyas",
            severity="blocker"
        ),
    ])

    return OperationPolicy(
        domain=ThinkingDomain.PROGRAMMING_EXECUTION,
        allowed_operations=allowed,
        forbidden_operations=forbidden,
    )
