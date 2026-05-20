"""
Dal Algebra Signature (توقيع جبر الدال)

F1: Foundational typed transition contract for dal_core.

CRITICAL PRINCIPLE:
Every stage transition in dal_core must declare:
1. Typed input and typed output
2. Evidence trail
3. Rank constraints
4. Residual propagation
5. Trace of transformation
6. Competing candidates
7. Forbidden outputs

MATHEMATICAL IDEA:
μᵢ : InputType × Optional[Guard/Registry] → CandidateSet[OutputType]

Each transition μᵢ must expose:
- input_type: Type specification
- output_type: Type specification
- evidence: Justification trail
- rank: Attestation level constraint
- residuals: Issue/warning/blocker propagation
- trace: Transformation provenance
- competitors: Alternative hypotheses
- forbidden_outputs: Stage-specific prohibitions

OUT OF SCOPE (this PR):
- Full rank algebra (F2)
- Full residual algebra (F3)
- CandidateSet base inheritance migration (F4)
- NoMeaning scanner (F5)
- RelationCandidate
- CaseEffectCandidate
- Operator application logic
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, TypeVar, Generic, Optional, Any
from enum import Enum

from dal_core.ranks import LughaRank
from dal_core.evidence import Evidence
from dal_core.residuals import Residual


# ---------------------------------------------------------------------------
# Core Type Variables
# ---------------------------------------------------------------------------

InputT = TypeVar("InputT")
OutputT = TypeVar("OutputT")


# ---------------------------------------------------------------------------
# 8-Layer Transition Domain Architecture (F1 Extended)
# ---------------------------------------------------------------------------


class TransitionDomain(Enum):
    """
    مجالات الانتقال الثمانية (8 Transition Domains)

    Architecture based on:
    "هذه ليست شجرة صرف فقط. هذه خريطة جبر الدال قبل المعنى"

    These are NOT linear pipeline stages, but:
    "شبكة انتقالات جزئية، لا pipeline واحد"
    (Partial transition network, not a single pipeline)

    Some words follow root→wazn path, others follow functional/particle path,
    others follow frozen/lexical path, and some remain unresolved until
    lexicon or context is available.
    """

    GRAPHOPHONEMIC = "رسم_صوت"
    """D0: GraphophonemicLayer - Written form + sound (رمز كتابي، فونيم، حركة)"""

    SYLLABIC = "مقطعي"
    """D1: SyllableLayer - Phonetic (CV/CVC) vs operational syllables"""

    PRE_MORPH = "ما_قبل_الصرف"
    """D2: PreMorphLayer - Functional/particle/built/clitic classification"""

    ORIGIN = "أصل"
    """D3: OriginLayer - Root (جذر) vs non-root functional unit"""

    TEMPLATE = "قالب"
    """D4: TemplateLayer - Pattern/wazn (generative, descriptive, functional, frozen)"""

    IDENTITY_AXIS = "محاور_هوية"
    """D5: IdentityAxisLayer - Parallel axes (derivation, i'rab, origin, composition, function)"""

    DIRECTIONAL_ANALYSIS = "تحليل_اتجاهي"
    """D6: DirectionalAnalysisLayer - Bidirectional form analysis (forward/backward scan)"""

    JUDGMENT = "حكم"
    """D7: JudgmentLayer - Licensed judgment with evidence/rank/residuals"""


class TemplateKind(Enum):
    """
    أنواع القوالب (Template Types)

    Critical distinction from problem statement:
    "وزن ظاهر لا يرقى مباشرة إلى وزن عميق"
    (Surface pattern does not directly promote to deep pattern)
    """

    GENERATED_MORPHOLOGICAL = "وزن_صرفي_مولّد"
    """Pattern-based generative morphology (فَعَلَ, فاعِل, مَفْعول)"""

    DESCRIPTIVE_MORPHOLOGICAL = "وزن_صرفي_واصف"
    """Descriptive post-hoc categorization (not generative)"""

    FUNCTIONAL_BUILT = "قالب_وظيفي_مبني"
    """Functional template for particles/built units (بنية وظيفية)"""

    LEXICAL_JAMID = "قالب_جامد_سماعي"
    """Frozen lexical template (attested, not derived)"""

    SURFACE = "وزن_ظاهر"
    """Surface pattern (what appears phonetically)"""

    DEEP = "وزن_عميق"
    """Deep pattern (after إعلال, إبدال analysis)"""

    UNRESOLVED = "بنية_غير_محسومة"
    """Unresolved structure (needs lexicon/context)"""


class OriginKind(Enum):
    """
    أنواع الأصل (Origin Types)

    From problem statement:
    "الأصل قد يكون جذر، وقد يكون وحدة غير جذرية"
    (Origin may be root, or may be non-root unit)
    """

    ROOT = "جذر"
    """Root origin (ثنائي، ثلاثي، رباعي، صحيح، معتل، مهموز، مضعف)"""

    NON_ROOT_FUNCTIONAL = "وحدة_وظيفية_غير_جذرية"
    """Non-root functional unit (particles, pronouns)"""

    CLITIC = "ضمير_متصل"
    """Clitic (external attachment)"""

    BUILT_UNIT = "وحدة_مبنية"
    """Built unit (frozen functional)"""

    LEXICAL_JAMID = "جامد_معجمي"
    """Frozen lexical (يد، دم، شمس، ماء)"""

    UNKNOWN = "غير_معروف"
    """Unknown/unresolved origin"""


class EvidencePolarity(Enum):
    """
    قطبية الدليل (Evidence Polarity)

    From problem statement judgment layer:
    "فرضيات متعددة، أدلة، أدلة مضادة"
    (Multiple hypotheses, evidence, counter-evidence)
    """

    SUPPORTING = "داعم"
    """Evidence supporting this hypothesis"""

    COUNTER = "مضاد"
    """Counter-evidence (evidence against this hypothesis)"""

    NEUTRAL = "محايد"
    """Neutral evidence"""


class AttestationPolicy(Enum):
    """
    سياسة السماع (Attestation Policy)

    From problem statement:
    "لا حكم قطعي بلا معجم أو سياق عند الحاجة"
    (No certificate without lexicon/context when needed)
    """

    NOT_REQUIRED = "غير_مطلوب"
    """Attestation not required (pattern-based)"""

    OPTIONAL = "اختياري"
    """Attestation optional (improves confidence)"""

    REQUIRED_FOR_CERTIFICATE = "مطلوب_للترخيص"
    """Attestation required for certificate rank"""

    REQUIRED_FOR_ANY_ACCEPTANCE = "مطلوب_لأي_قبول"
    """Attestation required for any acceptance (frozen words)"""


class IdentityAxis(Enum):
    """
    محاور الهوية (Identity Axes)

    From problem statement:
    "هذه ليست طبقة واحدة خطية، بل محاور متوازية"
    (Not a single linear layer, but parallel axes)

    A word may carry candidates in multiple axes simultaneously:
    - اسمًا (nominal)
    - مبنيًا (frozen)
    - منقولًا (transferred)
    - عربيًا (Arabic)
    - مركبًا (compound)
    """

    DERIVATION = "اشتقاق"
    """Derivation axis: جامد/مشتق/منقول"""

    IRAB = "إعراب"
    """I'rab axis: معرب/مبني"""

    ORIGIN = "أصل"
    """Origin axis: عربي/دخيل/معرّب"""

    COMPOSITION = "تركيب"
    """Composition axis: مفرد/مركب/منحوت"""

    FUNCTION = "وظيفة"
    """Function axis: اسمي/فعلي/حرفي/أداتي"""


# ---------------------------------------------------------------------------
# Typed Input/Output Contracts
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DalTypedInput:
    """
    مدخل مُنَمَّط (Typed Input)

    Base contract for all dal_core stage inputs.

    Every input must declare:
    - input_type_name: Human-readable type identifier
    - source_stage: Which stage produced this input
    """

    input_type_name: str
    """Human-readable type identifier (e.g., 'MufradProof', 'SentenceFrameCandidate')"""

    source_stage: str
    """Stage that produced this input (e.g., 'mufrad_proof', 'frame_builder')"""

    def get_type_signature(self) -> str:
        """Get full type signature for contract validation."""
        return f"{self.source_stage}::{self.input_type_name}"


@dataclass(frozen=True)
class DalTypedOutput:
    """
    مخرج مُنَمَّط (Typed Output)

    Base contract for all dal_core stage outputs.

    Every output must declare:
    - output_type_name: Human-readable type identifier
    - target_stage: Which stage will consume this output
    """

    output_type_name: str
    """Human-readable type identifier (e.g., 'OperatorCandidate', 'PreSyntaxMufradVector')"""

    target_stage: str
    """Stage that will consume this output (e.g., 'operator_candidate', 'relation_builder')"""

    def get_type_signature(self) -> str:
        """Get full type signature for contract validation."""
        return f"{self.target_stage}::{self.output_type_name}"


# ---------------------------------------------------------------------------
# Evidence, Trace, and Guard Contracts
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DalEvidence:
    """
    دليل الدال (Dal Evidence)

    Evidence trail for a dal transformation.

    Extends base Evidence with dal-specific fields:
    - transformation_type: What kind of transformation was applied
    - evidence_chain: Chain of supporting evidence
    """

    transformation_type: str
    """Type of transformation (e.g., 'syllabification', 'pattern_matching', 'operator_lookup')"""

    evidence_chain: tuple[Evidence, ...]
    """Chain of supporting evidence from lower layers"""

    def get_evidence_summary(self) -> str:
        """Get summary of evidence chain."""
        if not self.evidence_chain:
            return f"{self.transformation_type}: no evidence"

        sources = [e.source for e in self.evidence_chain]
        return f"{self.transformation_type}: {', '.join(sources)}"


@dataclass(frozen=True)
class DalTrace:
    """
    أثر الدال (Dal Trace)

    Transformation provenance trace.

    Every transition must record:
    - stage_name: Which stage performed this transformation
    - input_signature: Type signature of input
    - output_signature: Type signature of output
    - transformation_id: Unique transformation identifier
    - parent_trace_id: Optional parent trace for chaining
    """

    stage_name: str
    """Stage that performed this transformation"""

    input_signature: str
    """Type signature of input (from DalTypedInput.get_type_signature())"""

    output_signature: str
    """Type signature of output (from DalTypedOutput.get_type_signature())"""

    transformation_id: str
    """Unique identifier for this transformation"""

    parent_trace_id: Optional[str] = None
    """Optional parent trace for chaining"""

    def get_trace_path(self) -> str:
        """Get full trace path."""
        if self.parent_trace_id:
            return f"{self.parent_trace_id} → {self.transformation_id}"
        return self.transformation_id


@dataclass(frozen=True)
class DalTransitionGuard:
    """
    حارس التحول (Transition Guard)

    Precondition/postcondition guard for a transition.

    Guards specify:
    - guard_type: What is being guarded
    - condition: Human-readable condition description
    - required: Whether this guard is mandatory
    """

    guard_type: str
    """Type of guard (e.g., 'input_validation', 'rank_ceiling', 'forbidden_field')"""

    condition: str
    """Human-readable condition description"""

    required: bool = True
    """Whether this guard is mandatory (True) or advisory (False)"""

    def check(self, obj: Any) -> tuple[bool, str]:
        """
        Check guard condition against an object.

        Returns:
            (satisfied, message) tuple

        Note: This is a placeholder. Actual guard logic should be implemented
        by specific guard subclasses or validation functions.
        """
        # Placeholder - actual implementation should be in validation functions
        return True, f"Guard {self.guard_type} not yet implemented"


# ---------------------------------------------------------------------------
# Forbidden Outputs Contract
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DalForbiddenOutput:
    """
    مخرج ممنوع (Forbidden Output)

    Stage-specific forbidden field names and patterns.

    Each stage must declare what outputs are forbidden:
    - forbidden_field_names: Field names that must not appear
    - stage_name: Which stage these prohibitions apply to
    - reason: Why these fields are forbidden
    """

    forbidden_field_names: frozenset[str]
    """Field names that must not appear in outputs"""

    stage_name: str
    """Stage these prohibitions apply to"""

    reason: str
    """Why these fields are forbidden at this stage"""

    def contains_forbidden_field(self, field_name: str) -> bool:
        """Check if a field name is forbidden."""
        return field_name in self.forbidden_field_names

    def get_violation_message(self, field_name: str) -> str:
        """Get violation message for a forbidden field."""
        if self.contains_forbidden_field(field_name):
            return f"Field '{field_name}' is forbidden at stage '{self.stage_name}': {self.reason}"
        return ""


# ---------------------------------------------------------------------------
# Transition Contract
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DalTransitionContract:
    """
    عقد التحول (Transition Contract)

    Complete contract for a dal_core stage transition.

    REQUIRED FIELDS:
    - input_type: Type specification for inputs
    - output_type: Type specification for outputs
    - stage_name: Name of this transformation stage
    - rank_constraint: Rank ceiling/floor constraint
    - forbidden_outputs: Stage-specific forbidden fields

    OPTIONAL FIELDS (8-Layer Architecture Extensions):
    - transition_domain: Which of the 8 domains this transition operates in
    - template_kind: For TEMPLATE domain transitions
    - origin_kind: For ORIGIN domain transitions
    - identity_axes: For IDENTITY_AXIS domain transitions (may have multiple)
    - requires_lexicon: Whether lexicon lookup is required
    - requires_attestation: Attestation policy for this transition
    - requires_context: Whether context is required
    - allows_unresolved: Whether unresolved outputs are acceptable
    - evidence_policy: How evidence should be gathered
    - counter_evidence_policy: How counter-evidence is handled

    ORIGINAL OPTIONAL FIELDS:
    - guards: Precondition/postcondition guards
    - evidence_required: Whether evidence trail is mandatory
    - trace_required: Whether transformation trace is mandatory
    - competitors_allowed: Whether competing candidates are allowed
    """

    input_type: DalTypedInput
    """Type specification for inputs"""

    output_type: DalTypedOutput
    """Type specification for outputs"""

    stage_name: str
    """Name of this transformation stage"""

    rank_constraint: Optional[LughaRank] = None
    """Rank ceiling constraint (output.rank ≤ input.rank)"""

    forbidden_outputs: tuple[DalForbiddenOutput, ...] = field(default_factory=tuple)
    """Stage-specific forbidden fields"""

    guards: tuple[DalTransitionGuard, ...] = field(default_factory=tuple)
    """Precondition/postcondition guards"""

    evidence_required: bool = True
    """Whether evidence trail is mandatory"""

    trace_required: bool = True
    """Whether transformation trace is mandatory"""

    competitors_allowed: bool = True
    """Whether competing candidates are allowed"""

    # ---------------------------------------------------------------------------
    # 8-Layer Architecture Extensions
    # ---------------------------------------------------------------------------

    transition_domain: Optional[TransitionDomain] = None
    """Which of the 8 transition domains this operates in"""

    template_kind: Optional[TemplateKind] = None
    """For TEMPLATE domain: which template type (generative, descriptive, etc.)"""

    origin_kind: Optional[OriginKind] = None
    """For ORIGIN domain: which origin type (root, functional, etc.)"""

    identity_axes: tuple[IdentityAxis, ...] = field(default_factory=tuple)
    """For IDENTITY_AXIS domain: which parallel axes are analyzed"""

    requires_lexicon: bool = False
    """Whether lexicon lookup is required for this transition"""

    requires_attestation: AttestationPolicy = AttestationPolicy.NOT_REQUIRED
    """Attestation policy: required for certificate/acceptance, optional, or not required"""

    requires_context: bool = False
    """Whether context is required for this transition"""

    allows_unresolved: bool = True
    """Whether unresolved outputs are acceptable (pending lexicon/context)"""

    evidence_polarity_tracking: bool = False
    """Whether to track supporting vs counter-evidence"""

    residual_policy: Optional[str] = None
    """How residuals should be handled (free-form for now)"""

    def validate_contract(self) -> tuple[bool, list[str]]:
        """
        Validate that contract is well-formed.

        Returns:
            (is_valid, violations) tuple
        """
        violations = []

        # Check input/output types are specified
        if not self.input_type.input_type_name:
            violations.append("input_type.input_type_name is empty")

        if not self.output_type.output_type_name:
            violations.append("output_type.output_type_name is empty")

        # Check stage name is specified
        if not self.stage_name:
            violations.append("stage_name is empty")

        return len(violations) == 0, violations

    def get_contract_signature(self) -> str:
        """Get full contract signature."""
        input_sig = self.input_type.get_type_signature()
        output_sig = self.output_type.get_type_signature()
        return f"{self.stage_name}: {input_sig} → {output_sig}"


# ---------------------------------------------------------------------------
# Candidate Set Protocol
# ---------------------------------------------------------------------------


class DalCandidateSetProtocol(Protocol[OutputT]):
    """
    بروتوكول مجموعة المرشحين (Candidate Set Protocol)

    Protocol that all dal_core candidate sets should follow.

    REQUIRED METHODS:
    - get_candidates() -> tuple: Return all candidates
    - get_rank() -> LughaRank: Return rank ceiling
    - get_residuals() -> tuple: Return all residuals
    - get_trace() -> DalTrace: Return transformation trace
    - get_competitors() -> tuple: Return competing candidates

    OPTIONAL METHODS:
    - is_empty() -> bool: Check if candidate set is empty
    - has_residuals() -> bool: Check if any residuals exist
    """

    def get_candidates(self) -> tuple[OutputT, ...]:
        """Return all candidates (may be empty tuple)."""
        ...

    def get_rank(self) -> LughaRank:
        """Return rank ceiling for this candidate set."""
        ...

    def get_residuals(self) -> tuple[Residual, ...]:
        """Return all residuals (may be empty tuple)."""
        ...

    def get_trace(self) -> DalTrace:
        """Return transformation trace."""
        ...

    def get_competitors(self) -> tuple[OutputT, ...]:
        """Return competing candidates (may be same as get_candidates)."""
        ...

    def is_empty(self) -> bool:
        """Check if candidate set is empty (no candidates)."""
        return len(self.get_candidates()) == 0

    def has_residuals(self) -> bool:
        """Check if any residuals exist."""
        return len(self.get_residuals()) > 0


# ---------------------------------------------------------------------------
# Transition Protocol
# ---------------------------------------------------------------------------


class DalTransitionProtocol(Protocol[InputT, OutputT]):
    """
    بروتوكول التحول (Transition Protocol)

    Protocol for dal_core stage transitions.

    REQUIRED METHODS:
    - get_contract() -> DalTransitionContract: Return transition contract
    - apply(input: InputT, ...) -> DalCandidateSetProtocol[OutputT]: Apply transformation

    Mathematical signature:
        μᵢ : InputType × Optional[Guard/Registry] → CandidateSet[OutputType]
    """

    def get_contract(self) -> DalTransitionContract:
        """Return the transition contract for this stage."""
        ...

    def apply(self, input_obj: InputT, **kwargs: Any) -> DalCandidateSetProtocol[OutputT]:
        """
        Apply the transformation.

        Args:
            input_obj: Typed input
            **kwargs: Optional guards, registries, or other context

        Returns:
            Candidate set of typed outputs
        """
        ...


# ---------------------------------------------------------------------------
# Validation Helper Functions
# ---------------------------------------------------------------------------


def validate_transition_contract(contract: DalTransitionContract) -> None:
    """
    Validate that a transition contract is well-formed.

    Raises:
        ValueError: If contract is invalid
    """
    is_valid, violations = contract.validate_contract()

    if not is_valid:
        violation_msg = "\n".join(f"  - {v}" for v in violations)
        raise ValueError(
            f"Invalid DalTransitionContract for stage '{contract.stage_name}':\n"
            f"{violation_msg}"
        )


def validate_candidate_set_shape(
    candidate_set: DalCandidateSetProtocol[Any],
    allow_empty: bool = True
) -> None:
    """
    Validate that a candidate set has the correct shape.

    Checks:
    1. Empty sets are allowed (if allow_empty=True)
    2. No None candidates in the set
    3. All required methods are present

    Raises:
        ValueError: If candidate set shape is invalid
    """
    candidates = candidate_set.get_candidates()

    # Check for empty set
    if not allow_empty and len(candidates) == 0:
        raise ValueError("Candidate set is empty but allow_empty=False")

    # Check for None candidates
    if any(c is None for c in candidates):
        raise ValueError("Candidate set contains None candidates (forbidden)")

    # Verify required methods are callable
    required_methods = ['get_rank', 'get_residuals', 'get_trace', 'get_competitors']
    for method_name in required_methods:
        if not hasattr(candidate_set, method_name):
            raise ValueError(f"Candidate set missing required method: {method_name}")


def ensure_no_forbidden_outputs(
    obj: Any,
    forbidden_outputs: tuple[DalForbiddenOutput, ...],
    stage_name: str
) -> None:
    """
    Ensure an object does not contain forbidden field names.

    Checks:
    1. Object does not have forbidden field names as attributes
    2. If object is a dict-like, does not have forbidden keys

    Raises:
        ValueError: If forbidden fields are found
    """
    violations = []

    for forbidden_spec in forbidden_outputs:
        if forbidden_spec.stage_name != stage_name:
            continue

        # Check object attributes
        if hasattr(obj, '__dict__'):
            for field_name in forbidden_spec.forbidden_field_names:
                if hasattr(obj, field_name):
                    violations.append(
                        forbidden_spec.get_violation_message(field_name)
                    )

        # Check dict-like keys
        if hasattr(obj, 'keys'):
            for field_name in forbidden_spec.forbidden_field_names:
                if field_name in obj:  # type: ignore
                    violations.append(
                        forbidden_spec.get_violation_message(field_name)
                    )

    if violations:
        violation_msg = "\n".join(f"  - {v}" for v in violations)
        raise ValueError(
            f"Forbidden outputs detected at stage '{stage_name}':\n"
            f"{violation_msg}"
        )


# ---------------------------------------------------------------------------
# Module Exports
# ---------------------------------------------------------------------------

__all__ = [
    # Type variables
    "InputT",
    "OutputT",
    # 8-Layer Architecture Enums
    "TransitionDomain",
    "TemplateKind",
    "OriginKind",
    "EvidencePolarity",
    "AttestationPolicy",
    "IdentityAxis",
    # Typed input/output
    "DalTypedInput",
    "DalTypedOutput",
    # Evidence and trace
    "DalEvidence",
    "DalTrace",
    # Guards and contracts
    "DalTransitionGuard",
    "DalForbiddenOutput",
    "DalTransitionContract",
    # Protocols
    "DalCandidateSetProtocol",
    "DalTransitionProtocol",
    # Validation helpers
    "validate_transition_contract",
    "validate_candidate_set_shape",
    "ensure_no_forbidden_outputs",
]
