"""
Governed Trace T5 Contract (عقد T5 المحكوم بالأثر)

PR #142: Constitutional contract for T5 trace consumption.

Constitutional Laws:
    1. T5 is NOT an Arabic analyzer
    2. T5 is NOT a candidate generator
    3. T5 is NOT a rank upgrader
    4. T5 is NOT a residual resolver
    5. T5 is NOT an ifādah closer
    6. T5 is NOT a hukm/reality producer

    T5 may ONLY:
        - Consume existing immutable AlgorithmTracePayload
        - Produce bounded explanations referencing existing trace elements
        - Suggest repairs that require algorithm rerun (NOT execute repairs)

Forbidden Pipeline:
    ❌ Raw Arabic → T5 → Candidate
    ❌ Raw Arabic → T5 → Rank
    ❌ T5 → Residual resolution
    ❌ T5 → Ifādah closure
    ❌ T5 → Hukm
    ❌ T5 → Reality

Permitted Pipeline:
    ✅ AlgorithmTracePayload → GovernedTraceT5Input → ExplanationCandidate
    ✅ AlgorithmTracePayload → GovernedTraceT5Input → RepairSuggestionCandidate

Constitutional Formula:
    الجبر = الدستور (Algebra = Constitution)
    الخوارزمية = تنفيذ الدستور (Algorithm = Constitutional Execution)
    AlgorithmTracePayload = أثر التنفيذ (Trace = Execution Evidence)
    GovernedTraceT5Contract = عقد استهلاك الأثر (Contract = Trace Consumption Contract)
    T5 = مستهلك الأثر (T5 = Bounded Trace Explainer)

Supreme Law:
    T5 لا ينتج طبقة جديدة؛ T5 يشرح أثر طبقة أنتجتها الخوارزمية
    (T5 does not produce new layers; T5 explains traces of layers produced by algorithms)

Reference:
    User requirement: PR #142 specification (2026-05-28)
    Builds on: PR #141 (AlgorithmTracePayload)

Created: 2026-05-28
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Tuple, Optional, Union

from dal_core.algorithm_trace_payload import (
    AlgorithmTracePayload,
    TraceConsumerOperation,
)


# ============================================================================
# Forbidden T5 Operations (Constitutional Declaration)
# ============================================================================

class ForbiddenT5Operation(Enum):
    """
    Operations that T5 is constitutionally FORBIDDEN from performing.

    These operations violate the constitutional boundary:
        T5 is a trace explainer, NOT a constitutional fact producer.

    Forbidden Operations:
        - CREATE_CANDIDATE: Only algorithms create candidates
        - UPGRADE_RANK: Only proof procedures modify rank
        - DELETE_RESIDUALS: Only gates resolve residuals
        - CLOSE_IFADAH: Only ifadah closure gates
        - PRODUCE_HUKM: Only judgment layer
        - PRODUCE_REALITY: Only reality establishment layer
        - ANALYZE_RAW_ARABIC: Only algorithms analyze Arabic text
        - MODIFY_TRACE: Traces are immutable audit evidence
        - EXECUTE_REPAIR: Only algorithms execute repairs
        - RESOLVE_RESIDUALS: Only discharge procedures resolve residuals
        - PRODUCE_SEMANTIC_CERTAINTY: Only semantic gates produce certainty

    Constitutional Enforcement:
        - Contract structure prevents these operations
        - Validators reject outputs claiming these operations
        - Tests verify forbidden operations cannot be performed
    """
    CREATE_CANDIDATE = auto()
    UPGRADE_RANK = auto()
    DELETE_RESIDUALS = auto()
    CLOSE_IFADAH = auto()
    PRODUCE_HUKM = auto()
    PRODUCE_REALITY = auto()
    ANALYZE_RAW_ARABIC = auto()
    MODIFY_TRACE = auto()
    EXECUTE_REPAIR = auto()
    RESOLVE_RESIDUALS = auto()
    PRODUCE_SEMANTIC_CERTAINTY = auto()


# ============================================================================
# Trace Consumer Context
# ============================================================================

@dataclass(frozen=True)
class TraceConsumerContext:
    """
    Optional bounded context for trace consumption.

    Constitutional Guards:
        - Context may provide user query or explanation scope
        - Context MUST NOT contain instructions for forbidden operations
        - Context MUST NOT override constitutional boundaries

    Fields:
        user_query: Optional user question about the trace
        explanation_scope: Optional scope limitation (e.g., "relations only")
        max_referenced_elements: Optional limit on elements to reference

    Forbidden Context Content:
        - "create new candidate"
        - "upgrade rank"
        - "resolve residuals"
        - "close ifadah"
        - "produce hukm"
    """
    user_query: Optional[str] = None
    explanation_scope: Optional[str] = None
    max_referenced_elements: Optional[int] = None

    def __post_init__(self):
        """Validate trace consumer context."""
        if self.max_referenced_elements is not None:
            if not isinstance(self.max_referenced_elements, int):
                raise TypeError(
                    f"max_referenced_elements must be int or None, "
                    f"got {type(self.max_referenced_elements)}"
                )
            if self.max_referenced_elements < 1:
                raise ValueError("max_referenced_elements must be >= 1")

        # Validate that context doesn't contain forbidden instructions
        forbidden_phrases = [
            "create",  # Catches "create candidate", "create new candidate", etc.
            "upgrade",  # Catches "upgrade rank"
            "delete",  # Catches "delete residual"
            "resolve",  # Catches "resolve residual"
            "close ifadah",
            "produce hukm",
            "produce reality",
        ]

        if self.user_query:
            query_lower = self.user_query.lower()
            for phrase in forbidden_phrases:
                if phrase in query_lower:
                    raise ValueError(
                        f"TraceConsumerContext.user_query contains forbidden instruction: '{phrase}'"
                    )

        if self.explanation_scope:
            scope_lower = self.explanation_scope.lower()
            for phrase in forbidden_phrases:
                if phrase in scope_lower:
                    raise ValueError(
                        f"TraceConsumerContext.explanation_scope contains forbidden instruction: '{phrase}'"
                    )


# ============================================================================
# Governed Trace T5 Input
# ============================================================================

@dataclass(frozen=True)
class GovernedTraceT5Input:
    """
    Input contract for T5 trace consumption.

    Constitutional Laws:
        1. Input MUST be AlgorithmTracePayload (never raw Arabic text)
        2. Operation MUST be from permitted set
        3. Context MUST NOT contain forbidden instructions

    Fields:
        trace: Algorithm trace to consume (required)
        operation: Trace consumer operation (required)
        context: Optional bounded context

    Forbidden Inputs:
        - Raw Arabic text (string)
        - Forbidden operations
        - Context with forbidden instructions
    """
    trace: AlgorithmTracePayload
    operation: TraceConsumerOperation
    context: Optional[TraceConsumerContext] = None

    def __post_init__(self):
        """Validate governed trace T5 input."""
        # Validate trace
        if not isinstance(self.trace, AlgorithmTracePayload):
            raise TypeError(
                f"GovernedTraceT5Input.trace must be AlgorithmTracePayload, "
                f"got {type(self.trace)}"
            )

        # Validate operation
        if not isinstance(self.operation, TraceConsumerOperation):
            raise TypeError(
                f"GovernedTraceT5Input.operation must be TraceConsumerOperation, "
                f"got {type(self.operation)}"
            )

        # Validate operation is permitted
        if not self.operation.is_permitted():
            raise ValueError(
                f"GovernedTraceT5Input.operation must be permitted, "
                f"got forbidden operation: {self.operation}"
            )

        # Validate context
        if self.context is not None:
            if not isinstance(self.context, TraceConsumerContext):
                raise TypeError(
                    f"GovernedTraceT5Input.context must be TraceConsumerContext or None, "
                    f"got {type(self.context)}"
                )


# ============================================================================
# Explanation Candidate (T5 Output Type A)
# ============================================================================

@dataclass(frozen=True)
class ExplanationCandidate:
    """
    T5-generated explanation of existing trace elements.

    Constitutional Laws:
        1. ExplanationCandidate ONLY explains what algorithms produced
        2. ExplanationCandidate CANNOT create new candidates
        3. ExplanationCandidate CANNOT modify ranks
        4. ExplanationCandidate CANNOT close ifadah
        5. ExplanationCandidate CANNOT produce hukm
        6. ExplanationCandidate MUST reference only existing trace elements

    Structure Enforcement:
        - NO fields for: new_candidate, upgraded_rank, resolved_residuals,
          closed_ifadah, produced_hukm, produced_reality
        - ONLY fields for: referencing existing trace elements

    Fields:
        source_trace_id: References AlgorithmTracePayload.trace_id (NOT source_algorithm)
        operation: Which permitted operation was performed
        explanation_text: Natural language explanation
        referenced_candidate_ids: Candidate IDs from trace (read-only references)
        referenced_rank_values: Rank values from trace (read-only references)
        referenced_residual_ids: Residual IDs from trace (read-only references)
        referenced_gate_ids: Gate/operation IDs from trace (read-only references)
        confidence: Explanation confidence [0.0, 1.0]

    Forbidden Fields (enforced by absence):
        - new_candidate
        - upgraded_rank
        - resolved_residuals
        - closed_ifadah
        - produced_hukm
        - produced_reality
        - modified_trace
    """
    source_trace_id: str
    operation: TraceConsumerOperation
    explanation_text: str
    referenced_candidate_ids: Tuple[str, ...]
    referenced_rank_values: Tuple[str, ...]
    referenced_residual_ids: Tuple[str, ...]
    referenced_gate_ids: Tuple[str, ...]
    confidence: float

    def __post_init__(self):
        """Validate explanation candidate."""
        # Validate source_trace_id
        if not self.source_trace_id:
            raise ValueError("ExplanationCandidate requires non-empty source_trace_id")
        if not isinstance(self.source_trace_id, str):
            raise TypeError(
                f"source_trace_id must be str, got {type(self.source_trace_id)}"
            )

        # Validate operation
        if not isinstance(self.operation, TraceConsumerOperation):
            raise TypeError(
                f"operation must be TraceConsumerOperation, got {type(self.operation)}"
            )
        if not self.operation.is_permitted():
            raise ValueError(
                f"ExplanationCandidate.operation must be permitted, "
                f"got forbidden operation: {self.operation}"
            )

        # Validate explanation_text
        if not self.explanation_text:
            raise ValueError("ExplanationCandidate requires non-empty explanation_text")
        if not isinstance(self.explanation_text, str):
            raise TypeError(
                f"explanation_text must be str, got {type(self.explanation_text)}"
            )

        # Validate referenced_candidate_ids
        if not isinstance(self.referenced_candidate_ids, tuple):
            raise TypeError(
                f"referenced_candidate_ids must be tuple, "
                f"got {type(self.referenced_candidate_ids)}"
            )

        # Validate referenced_rank_values
        if not isinstance(self.referenced_rank_values, tuple):
            raise TypeError(
                f"referenced_rank_values must be tuple, "
                f"got {type(self.referenced_rank_values)}"
            )

        # Validate referenced_residual_ids
        if not isinstance(self.referenced_residual_ids, tuple):
            raise TypeError(
                f"referenced_residual_ids must be tuple, "
                f"got {type(self.referenced_residual_ids)}"
            )

        # Validate referenced_gate_ids
        if not isinstance(self.referenced_gate_ids, tuple):
            raise TypeError(
                f"referenced_gate_ids must be tuple, "
                f"got {type(self.referenced_gate_ids)}"
            )

        # Validate confidence
        if not isinstance(self.confidence, (int, float)):
            raise TypeError(f"confidence must be float, got {type(self.confidence)}")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(
                f"confidence must be in [0.0, 1.0], got {self.confidence}"
            )


# ============================================================================
# Repair Suggestion Candidate (T5 Output Type B)
# ============================================================================

@dataclass(frozen=True)
class RepairSuggestionCandidate:
    """
    T5-suggested repair that REQUIRES algorithm rerun (NOT executed repair).

    Constitutional Laws:
        1. RepairSuggestionCandidate ONLY suggests repairs
        2. RepairSuggestionCandidate CANNOT execute repairs
        3. RepairSuggestionCandidate CANNOT resolve residuals
        4. RepairSuggestionCandidate MUST require algorithm rerun
        5. Actual repair execution belongs to algorithms/gates only

    Structure Enforcement:
        - NO fields for: executed_repair, new_candidate, resolved_residuals
        - ONLY fields for: suggesting which gate/operation might help

    Fields:
        source_trace_id: References AlgorithmTracePayload.trace_id (NOT source_algorithm)
        blocked_by_residual_ids: Residual IDs that block progress
        suggested_gate: Which gate/operation might resolve blockage
        suggested_rerun: Whether algorithm rerun is suggested
        explanation: Why this repair might work
        requires_algorithm_rerun: MUST always be True (constitutional requirement)

    Forbidden Fields (enforced by absence):
        - executed_repair
        - new_candidate
        - resolved_residuals
        - upgraded_rank
        - closed_ifadah
    """
    source_trace_id: str
    blocked_by_residual_ids: Tuple[str, ...]
    suggested_gate: Optional[str]
    suggested_rerun: bool
    explanation: str
    requires_algorithm_rerun: bool

    def __post_init__(self):
        """Validate repair suggestion candidate."""
        # Validate source_trace_id
        if not self.source_trace_id:
            raise ValueError(
                "RepairSuggestionCandidate requires non-empty source_trace_id"
            )
        if not isinstance(self.source_trace_id, str):
            raise TypeError(
                f"source_trace_id must be str, got {type(self.source_trace_id)}"
            )

        # Validate blocked_by_residual_ids
        if not isinstance(self.blocked_by_residual_ids, tuple):
            raise TypeError(
                f"blocked_by_residual_ids must be tuple, "
                f"got {type(self.blocked_by_residual_ids)}"
            )

        # Validate suggested_gate
        if self.suggested_gate is not None:
            if not isinstance(self.suggested_gate, str):
                raise TypeError(
                    f"suggested_gate must be str or None, "
                    f"got {type(self.suggested_gate)}"
                )

        # Validate suggested_rerun
        if not isinstance(self.suggested_rerun, bool):
            raise TypeError(
                f"suggested_rerun must be bool, got {type(self.suggested_rerun)}"
            )

        # Validate explanation
        if not self.explanation:
            raise ValueError(
                "RepairSuggestionCandidate requires non-empty explanation"
            )
        if not isinstance(self.explanation, str):
            raise TypeError(f"explanation must be str, got {type(self.explanation)}")

        # Constitutional requirement: repair suggestions MUST require algorithm rerun
        if not isinstance(self.requires_algorithm_rerun, bool):
            raise TypeError(
                f"requires_algorithm_rerun must be bool, "
                f"got {type(self.requires_algorithm_rerun)}"
            )
        if not self.requires_algorithm_rerun:
            raise ValueError(
                "RepairSuggestionCandidate.requires_algorithm_rerun MUST be True "
                "(constitutional law: T5 cannot execute repairs, only suggest them)"
            )


# ============================================================================
# Governed Trace T5 Output (Discriminated Union)
# ============================================================================

# Type alias for output union
GovernedTraceT5Output = Union[ExplanationCandidate, RepairSuggestionCandidate]


# ============================================================================
# Governed Trace T5 Validator
# ============================================================================

class GovernedTraceT5Validator:
    """
    Validator enforcing constitutional boundaries on T5 trace consumption.

    Constitutional Enforcement:
        1. Input trace must be immutable AlgorithmTracePayload
        2. Operation must be permitted
        3. Explanations reference only existing trace elements
        4. Confidence bounded in [0.0, 1.0]
        5. No output may claim new constitutional facts
        6. Repair suggestions must require algorithm rerun
        7. No output may close ifadah, produce hukm, or produce reality

    Methods:
        - validate_input: Validate GovernedTraceT5Input
        - validate_output: Validate GovernedTraceT5Output
        - validate_explanation: Validate ExplanationCandidate
        - validate_repair_suggestion: Validate RepairSuggestionCandidate
        - validate_explanation_references: Validate references belong to trace
    """

    @staticmethod
    def validate_input(input_obj: GovernedTraceT5Input) -> None:
        """
        Validate GovernedTraceT5Input.

        Constitutional Guards:
            - Input must be AlgorithmTracePayload (not raw Arabic)
            - Operation must be permitted
            - Context must not contain forbidden instructions

        Args:
            input_obj: Input to validate

        Raises:
            ValueError: If input violates constitutional boundaries
            TypeError: If input has wrong type
        """
        if not isinstance(input_obj, GovernedTraceT5Input):
            raise TypeError(
                f"Input must be GovernedTraceT5Input, got {type(input_obj)}"
            )

        # Validate trace is AlgorithmTracePayload
        if not isinstance(input_obj.trace, AlgorithmTracePayload):
            raise ValueError(
                "GovernedTraceT5Input.trace must be AlgorithmTracePayload "
                "(raw Arabic input is forbidden)"
            )

        # Validate operation is permitted
        if not input_obj.operation.is_permitted():
            raise ValueError(
                f"Operation {input_obj.operation} is forbidden. "
                f"Only permitted operations allowed."
            )

        # Context validation done in __post_init__

    @staticmethod
    def validate_output(output: GovernedTraceT5Output) -> None:
        """
        Validate GovernedTraceT5Output.

        Constitutional Guards:
            - Output must be ExplanationCandidate or RepairSuggestionCandidate
            - Output must not claim to create candidates
            - Output must not claim to modify rank
            - Output must not claim to close ifadah
            - Output must not claim to produce hukm/reality

        Args:
            output: Output to validate

        Raises:
            ValueError: If output violates constitutional boundaries
            TypeError: If output has wrong type
        """
        if isinstance(output, ExplanationCandidate):
            GovernedTraceT5Validator.validate_explanation(output)
        elif isinstance(output, RepairSuggestionCandidate):
            GovernedTraceT5Validator.validate_repair_suggestion(output)
        else:
            raise TypeError(
                f"Output must be ExplanationCandidate or RepairSuggestionCandidate, "
                f"got {type(output)}"
            )

    @staticmethod
    def validate_explanation(explanation: ExplanationCandidate) -> None:
        """
        Validate ExplanationCandidate.

        Constitutional Guards:
            - Explanation must reference only existing trace elements
            - Confidence must be in [0.0, 1.0]
            - No forbidden fields (new_candidate, upgraded_rank, etc.)

        Args:
            explanation: Explanation to validate

        Raises:
            ValueError: If explanation violates constitutional boundaries
            TypeError: If explanation has wrong type
        """
        if not isinstance(explanation, ExplanationCandidate):
            raise TypeError(
                f"Explanation must be ExplanationCandidate, got {type(explanation)}"
            )

        # Verify no forbidden methods exist
        forbidden_attrs = [
            "new_candidate",
            "create_candidate",
            "upgraded_rank",
            "upgrade_rank",
            "resolved_residuals",
            "resolve_residuals",
            "delete_residuals",
            "closed_ifadah",
            "close_ifadah",
            "produced_hukm",
            "produce_hukm",
            "to_hukm",
            "produced_reality",
            "produce_reality",
            "to_reality",
            "modified_trace",
            "modify_trace",
        ]

        for attr in forbidden_attrs:
            if hasattr(explanation, attr):
                raise ValueError(
                    f"ExplanationCandidate MUST NOT have forbidden attribute: {attr}"
                )

        # Confidence validation done in __post_init__

    @staticmethod
    def validate_repair_suggestion(suggestion: RepairSuggestionCandidate) -> None:
        """
        Validate RepairSuggestionCandidate.

        Constitutional Guards:
            - Suggestion must require algorithm rerun
            - No executed repair fields
            - No resolved residuals fields

        Args:
            suggestion: Repair suggestion to validate

        Raises:
            ValueError: If suggestion violates constitutional boundaries
            TypeError: If suggestion has wrong type
        """
        if not isinstance(suggestion, RepairSuggestionCandidate):
            raise TypeError(
                f"Suggestion must be RepairSuggestionCandidate, got {type(suggestion)}"
            )

        # Constitutional requirement: must require algorithm rerun
        if not suggestion.requires_algorithm_rerun:
            raise ValueError(
                "RepairSuggestionCandidate.requires_algorithm_rerun MUST be True "
                "(T5 cannot execute repairs)"
            )

        # Verify no forbidden methods exist
        forbidden_attrs = [
            "executed_repair",
            "execute_repair",
            "new_candidate",
            "create_candidate",
            "resolved_residuals",
            "resolve_residuals",
            "delete_residuals",
            "upgraded_rank",
            "upgrade_rank",
            "closed_ifadah",
            "close_ifadah",
        ]

        for attr in forbidden_attrs:
            if hasattr(suggestion, attr):
                raise ValueError(
                    f"RepairSuggestionCandidate MUST NOT have forbidden attribute: {attr}"
                )

    @staticmethod
    def validate_explanation_references(
        explanation: ExplanationCandidate,
        source_trace: AlgorithmTracePayload
    ) -> None:
        """
        Validate that explanation references belong to source trace.

        Constitutional Guard:
            Explanation MUST reference only elements from the source trace.

        Validates:
            - referenced_candidate_ids exist in trace
            - referenced_residual_ids exist in trace
            - referenced_gate_ids exist in trace (via residual_sources or trace fields)
            - referenced_rank_values match ranks in trace

        Args:
            explanation: Explanation to validate
            source_trace: Source algorithm trace

        Raises:
            ValueError: If explanation references elements not in source trace
        """
        # Collect all valid candidate IDs from trace
        valid_candidate_ids = {
            cand.candidate_id for cand in source_trace.candidates
        }

        # Validate referenced candidate IDs
        for ref_id in explanation.referenced_candidate_ids:
            if ref_id not in valid_candidate_ids:
                raise ValueError(
                    f"ExplanationCandidate references candidate_id '{ref_id}' "
                    f"not found in source trace"
                )

        # Collect all valid residual IDs from trace
        # Residuals are embedded in candidate payloads via residual_payload.residuals
        valid_residual_ids = set()
        for cand in source_trace.candidates:
            # ResidualSet has .residuals field which is a FrozenSet[Residual]
            residual_set = cand.residual_payload.residuals
            # Extract residual IDs from the frozenset
            for residual in residual_set.residuals:
                valid_residual_ids.add(str(residual))

        # Validate referenced residual IDs
        for ref_id in explanation.referenced_residual_ids:
            if ref_id not in valid_residual_ids:
                raise ValueError(
                    f"ExplanationCandidate references residual_id '{ref_id}' "
                    f"not found in source trace"
                )

        # Collect all valid gate IDs from trace
        # Gates appear in residual_sources and candidate traces
        valid_gate_ids = set()
        for cand in source_trace.candidates:
            # Gates from residual sources
            valid_gate_ids.update(cand.residual_payload.residual_sources)
            # Gates from operational trace
            valid_gate_ids.update(cand.trace)

        # Validate referenced gate IDs
        for ref_id in explanation.referenced_gate_ids:
            if ref_id not in valid_gate_ids:
                raise ValueError(
                    f"ExplanationCandidate references gate_id '{ref_id}' "
                    f"not found in source trace"
                )

        # Collect all valid rank values from trace
        valid_rank_values = {
            cand.rank_payload.rank.name for cand in source_trace.candidates
        }

        # Validate referenced rank values
        for ref_rank in explanation.referenced_rank_values:
            if ref_rank not in valid_rank_values:
                raise ValueError(
                    f"ExplanationCandidate references rank '{ref_rank}' "
                    f"not found in source trace"
                )
