"""
Constitutional evaluation gate (mandatory post-step for every ModelOutput).

Every output produced by :class:`T5AdapterRunner` flows through this gate
before being returned to the caller. The gate delegates the actual
evaluation to :class:`dal_core.constitutional_evaluator.ConstitutionalEvaluator`
(PR #147) and then enforces the chosen :class:`EvaluationMode`.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from dal_core.constitutional_evaluator import (
    ConstitutionalEvaluator,
    ConstitutionalViolationReport,
    ConstitutionalViolationSeverity,
)
from dal_core.model_output import ModelOutput
from dal_core.training_example import TrainingExample

from .config import EvaluationMode


class T5ConstitutionalViolationError(RuntimeError):
    """Raised by :class:`ConstitutionalEvaluationGate` in STRICT mode.

    Attributes:
        report: The :class:`ConstitutionalViolationReport` describing
            every detected violation. Always populated; ``critical``
            list is non-empty.
        model_output: The offending :class:`ModelOutput`. Exposed for
            forensic inspection but the gate does not return it normally
            (the runner must not surface it through ``run()``).
    """

    def __init__(
        self,
        report: ConstitutionalViolationReport,
        model_output: ModelOutput,
    ) -> None:
        critical_violations: Tuple = tuple(
            v for v in report.violations
            if v.severity == ConstitutionalViolationSeverity.CRITICAL
        )
        summary = ", ".join(v.violation_type.name for v in critical_violations)
        super().__init__(
            f"T5 model output rejected by ConstitutionalEvaluator "
            f"({len(critical_violations)} critical violations: {summary})"
        )
        self.report = report
        self.model_output = model_output
        self.critical_violations = critical_violations


@dataclass(frozen=True)
class EvaluatedModelOutput:
    """Bundle of a :class:`ModelOutput` and its evaluation report.

    Only ``ConstitutionalEvaluationGate.evaluate`` constructs this. In
    STRICT mode, instances with critical violations are never returned
    (the gate raises instead); in OBSERVE mode they may be returned with
    ``report.passed = False``.
    """

    model_output: ModelOutput
    report: ConstitutionalViolationReport
    mode: EvaluationMode


@dataclass(frozen=True)
class ConstitutionalEvaluationGate:
    """The mandatory evaluator for every real T5 ``ModelOutput``.

    Fields:
        mode: ``STRICT`` (raise on critical violations) or ``OBSERVE``
            (always return with report).
    """

    mode: EvaluationMode = EvaluationMode.STRICT

    def __post_init__(self) -> None:
        if not isinstance(self.mode, EvaluationMode):
            raise ValueError("ConstitutionalEvaluationGate.mode must be EvaluationMode")

    def evaluate(
        self,
        model_output: ModelOutput,
        source_example: TrainingExample,
    ) -> EvaluatedModelOutput:
        """Run :class:`ConstitutionalEvaluator` and enforce ``mode``."""
        report = ConstitutionalEvaluator.evaluate_model_output(
            model_output, source_example
        )

        if self.mode == EvaluationMode.STRICT and report.critical_violations_count > 0:
            raise T5ConstitutionalViolationError(report, model_output)

        return EvaluatedModelOutput(
            model_output=model_output,
            report=report,
            mode=self.mode,
        )
