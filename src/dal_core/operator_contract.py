"""
Operator Contract Stub (عقد العامل)

Enforces that operators work ONLY on MufradProof, not on raw tokens.

This is a stub to enforce Theorem 6: Operators do not work on tokens.
Full syntax composition is NOT implemented in this phase.
"""

from dataclasses import dataclass
from typing import Any

from dal_core.residuals import Residual, ResidualType, ResidualSeverity


@dataclass(frozen=True)
class OperatorResult:
    """
    Result of operator application (stub).

    Full syntax composition not implemented yet.
    This exists only to enforce MufradProof consumption.
    """
    success: bool
    residuals: tuple[Residual, ...]
    message: str

    def __str__(self) -> str:
        status = "success" if self.success else "failure"
        return f"OperatorResult({status}, {len(self.residuals)} residuals)"


class OperatorContract:
    """
    عقد العامل (Operator Contract)

    Base contract for Arabic operators (عوامل).

    CRITICAL CONSTRAINT (Theorem 6):
    Operators MUST consume MufradProof, not raw tokens.

    FORBIDDEN:
    - operator.apply(token)
    - operator.apply(raw_string)
    - operator.apply(DForm)
    - operator.apply(Carrier)
    - operator.apply(ArabicAtom)

    ALLOWED:
    - operator.apply(mufrad_proof)
    - operator.apply(mufrad_proof_a, mufrad_proof_b, context)

    This is a stub. Full syntax composition is Phase 2+.
    """

    def apply(self, *nodes: Any) -> OperatorResult:
        """
        Apply operator to nodes.

        Args:
            *nodes: Must be MufradProof instances

        Returns:
            OperatorResult with validation

        Raises:
            TypeError if nodes are not MufradProof
        """
        from dal_core.mufrad_proof import MufradProof

        residuals = []

        # Enforce: all nodes must be MufradProof
        for i, node in enumerate(nodes):
            if not isinstance(node, MufradProof):
                # Get type name
                type_name = type(node).__name__

                # Check if it's a forbidden type
                forbidden_types = {
                    "str", "Carrier", "ArabicAtom", "OperativeUnit",
                    "FormCandidate", "TypedDal", "DClosed", "dict", "list"
                }

                if type_name in forbidden_types or isinstance(node, str):
                    residuals.append(Residual(
                        type=ResidualType.OPERATOR_ON_TOKEN_FORBIDDEN,
                        severity=ResidualSeverity.BLOCKER,
                        message=f"Operator cannot work on {type_name}. Must use MufradProof.",
                        location=f"node_{i}"
                    ))
                else:
                    residuals.append(Residual(
                        type=ResidualType.OPERATOR_ON_TOKEN_FORBIDDEN,
                        severity=ResidualSeverity.BLOCKER,
                        message=f"Node {i} is not MufradProof (got {type_name})",
                        location=f"node_{i}"
                    ))

        if residuals:
            return OperatorResult(
                success=False,
                residuals=tuple(residuals),
                message="Operator can only consume MufradProof"
            )

        # If all nodes are MufradProof, operator would proceed
        # (Full implementation is Phase 2+)
        return OperatorResult(
            success=True,
            residuals=tuple(),
            message="Stub: Full syntax composition not implemented"
        )

    def __str__(self) -> str:
        return "OperatorContract(stub)"


def reject_token_application(node: Any) -> OperatorResult:
    """
    Reject operator application on non-MufradProof node.

    Helper function to enforce Theorem 6.
    """
    from dal_core.mufrad_proof import MufradProof

    if isinstance(node, MufradProof):
        return OperatorResult(
            success=True,
            residuals=tuple(),
            message="Node is MufradProof"
        )

    type_name = type(node).__name__
    residual = Residual(
        type=ResidualType.OPERATOR_ON_TOKEN_FORBIDDEN,
        severity=ResidualSeverity.BLOCKER,
        message=f"Cannot apply operator to {type_name}. Use MufradProof.",
        location="operator_application"
    )

    return OperatorResult(
        success=False,
        residuals=(residual,),
        message=f"Rejected: {type_name} is not MufradProof"
    )
