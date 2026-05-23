"""
DalCandidateBuilder - بناء الدال المرخّص

PR-L3 Phase 2: Actual Pipeline Integration

Constructs fully-licensed DalCandidate from raw Arabic text via C1→C2a→C2b pipeline.

Critical Law:
    الدال يُبنى من الأثر الخام، لا يُنشأ يدويًا
    Dal is built from raw trace, not created manually.

Pipeline:
    Raw Arabic Text
    → C1 Encoding (phonic carriers)
    → C2a Phonology (haraka operations, syllable licenses)
    → C2b Morphology (boundaries, clitics, patterns, classification)
    → DalCandidate (13 mandatory fields)

What This Module Does:
    - Integrates with existing FVAFK components
    - Constructs complete DalCandidate from pipeline
    - Preserves trace through all stages
    - Returns governed failures as residuals

What This Module Does NOT Do:
    - Does NOT create meaning
    - Does NOT create wadh
    - Does NOT create dalalah
    - Does NOT create hukm
"""

from __future__ import annotations

import uuid
from typing import Tuple, FrozenSet, Optional, List
from dataclasses import dataclass

from .dal_candidate import DalCandidate
from .dal_structures import (
    PhonicCarrier,
    HarakaOperation,
    HarakaOperationType,
    SyllableLicense,
    SyllableType,
    WordBoundaryInfo,
    Clitic,
    CliticAnalysis,
    FormulaCandidate,
    FormulaClass,
    PathType,
    PatternStatus,
    TerminalState,
    SyntacticReadiness,
    SentenceShape,
    RoleProjection,
    RoleType,
)

# Import FVAFK components
try:
    from fvafk.c1.encoder import C1Encoder
    from fvafk.c2a.gate_framework import GateOrchestrator, GateStatus
    from fvafk.c2a.gates import (
        GateSukun,
        GateShadda,
        GateTanwin,
        GateHamza,
        GateWaqf,
    )
    from fvafk.c2b.root_extractor import RootExtractor
    from fvafk.c2b.pattern_matcher import PatternMatcher
    from fvafk.c2b.word_classifier import WordClassifier
    FVAFK_AVAILABLE = True
except ImportError:
    FVAFK_AVAILABLE = False


@dataclass(frozen=True)
class BuilderResult:
    """Result of DalCandidate construction."""
    candidate: Optional[DalCandidate]
    success: bool
    residuals: FrozenSet[str]
    trace_id: str


class DalCandidateBuilder:
    """
    بناء الدال - DalCandidate Builder

    Orchestrates C1→C2a→C2b pipeline to construct
    complete DalCandidate from raw Arabic signal.

    PR-L3 Phase 2: Actual pipeline integration, not mock.
    """

    def __init__(self):
        """Initialize builder with pipeline components."""
        self.residuals_accumulator: List[str] = []

        # C1 Encoding
        if FVAFK_AVAILABLE:
            self.encoder = C1Encoder()
        else:
            self.encoder = None

        # C2a Phonology Gates
        if FVAFK_AVAILABLE:
            self.phonology_gates = GateOrchestrator([
                GateSukun(),
                GateShadda(),
                GateTanwin(),
                GateHamza(),
                GateWaqf(),
            ])
        else:
            self.phonology_gates = None

        # C2b Morphology
        if FVAFK_AVAILABLE:
            self.root_extractor = RootExtractor()
        else:
            self.root_extractor = None

    def build(self, raw_signal: str) -> BuilderResult:
        """
        Build complete DalCandidate from raw Arabic text.

        Args:
            raw_signal: Raw Arabic text (e.g., "كَتَبَ")

        Returns:
            BuilderResult with candidate and residuals

        Critical:
            Returns governed failures (residuals), not exceptions.
        """
        self.residuals_accumulator = []
        trace_id = self._generate_trace_id()

        try:
            # Phase 1: C1 Encoding
            phonic_carriers = self._extract_phonic_carriers(raw_signal)
            if not phonic_carriers:
                self.residuals_accumulator.append("c1_encoding_failed")
                return self._failure_result(trace_id)

            # Phase 2: C2a Phonology
            haraka_ops, syllables = self._apply_phonology(phonic_carriers)

            # Phase 3: C2b Morphology
            boundaries = self._detect_word_boundaries(raw_signal)
            clitics = self._analyze_clitics(raw_signal)
            formulas = self._generate_formula_candidates(raw_signal, clitics)
            path = self._classify_path_type(formulas)
            pattern = self._determine_pattern_status(formulas)
            terminal = self._resolve_terminal_state(path)

            # Phase 4: C2b Syntax Readiness
            readiness = self._assess_syntactic_readiness(terminal, path)
            shape = self._analyze_sentence_shape(path)
            roles = self._project_role_candidates(path)

            # Construct DalCandidate
            candidate = DalCandidate(
                phonic_carriers=phonic_carriers,
                haraka_operations=haraka_ops,
                syllable_licenses=syllables,
                word_boundaries=boundaries,
                clitics=clitics,
                formula_candidates=formulas,
                path_type=path,
                pattern_status=pattern,
                terminal_state=terminal,
                syntactic_readiness=readiness,
                sentence_shape=shape,
                role_projection_candidates=roles,
                trace_id=trace_id,
                residuals=frozenset(self.residuals_accumulator),
                source_layer="PURE_DAL",
                signifier_form=raw_signal,  # Backward compatibility
            )

            return BuilderResult(
                candidate=candidate,
                success=True,
                residuals=frozenset(self.residuals_accumulator),
                trace_id=trace_id
            )

        except Exception as e:
            self.residuals_accumulator.append(f"builder_exception:{type(e).__name__}")
            return self._failure_result(trace_id)

    # ========================================================================
    # Phase 1: C1 Encoding
    # ========================================================================

    def _extract_phonic_carriers(
        self, raw_signal: str
    ) -> Tuple[PhonicCarrier, ...]:
        """Extract phonic carriers from C1 encoding."""
        if not self.encoder or not raw_signal:
            self.residuals_accumulator.append("c1_encoder_unavailable")
            # Fallback: create minimal carriers from graphemes
            carriers = []
            for i, char in enumerate(raw_signal):
                if not char.isspace():
                    carriers.append(
                        PhonicCarrier(
                            form=char,
                            phoneme=None,
                            position=i,
                            features=frozenset(["grapheme"])
                        )
                    )
            return tuple(carriers) if carriers else ()

        try:
            segments = self.encoder.encode(raw_signal)
            carriers = []
            for i, seg in enumerate(segments):
                carriers.append(
                    PhonicCarrier(
                        form=str(seg.text) if hasattr(seg, 'text') else str(seg),
                        phoneme=None,  # C1Encoder doesn't provide phoneme
                        position=i,
                        features=frozenset([
                            str(seg.kind.name) if hasattr(seg, 'kind') else "segment"
                        ])
                    )
                )
            return tuple(carriers)
        except Exception as e:
            self.residuals_accumulator.append(f"c1_encoding_error:{type(e).__name__}")
            return ()

    # ========================================================================
    # Phase 2: C2a Phonology
    # ========================================================================

    def _apply_phonology(
        self, carriers: Tuple[PhonicCarrier, ...]
    ) -> Tuple[Tuple[HarakaOperation, ...], Tuple[SyllableLicense, ...]]:
        """Apply C2a phonology gates."""
        operations = []
        syllables = []

        if not self.phonology_gates:
            self.residuals_accumulator.append("c2a_gates_unavailable")
            return (), ()

        try:
            # Convert carriers to segments for gates
            segments = [c.form for c in carriers]
            output, results = self.phonology_gates.run(segments)

            # Extract operations from gate results
            for result in results:
                if result.status == GateStatus.REPAIR:
                    # Map gate_id to operation type
                    op_type = self._map_gate_to_operation_type(result.gate_id)
                    op = HarakaOperation(
                        operation_type=op_type,
                        position=0,  # Gates don't track position precisely
                        input_form=''.join(result.input_units) if result.input_units else "",
                        output_form=''.join(result.output_units) if result.output_units else "",
                        gate_name=result.gate_id
                    )
                    operations.append(op)

            # Create minimal syllable licenses
            # (Simplified: one CV syllable per 2 carriers)
            for i in range(0, len(carriers), 2):
                if i + 1 < len(carriers):
                    syl = SyllableLicense(
                        syllable_type=SyllableType.CV,
                        onset=carriers[i].form,
                        nucleus=carriers[i + 1].form if i + 1 < len(carriers) else "",
                        coda=None,
                        position=i // 2,
                        is_valid=True
                    )
                    syllables.append(syl)

        except Exception as e:
            self.residuals_accumulator.append(f"c2a_phonology_error:{type(e).__name__}")

        return tuple(operations), tuple(syllables)

    def _map_gate_to_operation_type(self, gate_id: str) -> HarakaOperationType:
        """Map gate ID to HarakaOperationType."""
        mapping = {
            "gate_sukun": HarakaOperationType.SUKUN,
            "gate_shadda": HarakaOperationType.SHADDA,
            "gate_tanwin": HarakaOperationType.TANWIN,
            "gate_hamza": HarakaOperationType.HAMZA,
            "gate_waqf": HarakaOperationType.WAQF,
        }
        return mapping.get(gate_id, HarakaOperationType.SUKUN)

    # ========================================================================
    # Phase 3: C2b Morphology
    # ========================================================================

    def _detect_word_boundaries(self, raw_signal: str) -> WordBoundaryInfo:
        """Detect word boundaries."""
        # Simplified: treat entire input as one word
        return WordBoundaryInfo(
            start_position=0,
            end_position=len(raw_signal),
            boundary_markers=frozenset(["input_boundary"]),
            confidence=0.9
        )

    def _analyze_clitics(self, raw_signal: str) -> CliticAnalysis:
        """Analyze clitics using simple pattern matching."""
        stem = raw_signal
        prefixes = []
        suffixes = []

        # Simple prefix detection (ال، و، ف، ب)
        if stem.startswith("ال"):
            prefixes.append(Clitic("ال", 0, True, "article"))
            stem = stem[2:]
        elif stem and stem[0] in "وفبك":
            prefixes.append(Clitic(stem[0], 0, True, "conjunction"))
            stem = stem[1:]

        # Simple suffix detection (ة)
        if stem.endswith("ة"):
            suffixes.append(Clitic("ة", len(stem) - 1, False, "feminine"))
            stem = stem[:-1]

        return CliticAnalysis(
            stem=stem if stem else raw_signal,
            prefixes=tuple(prefixes),
            suffixes=tuple(suffixes),
            has_clitics=len(prefixes) + len(suffixes) > 0
        )

    def _generate_formula_candidates(
        self, raw_signal: str, clitics: CliticAnalysis
    ) -> Tuple[FormulaCandidate, ...]:
        """Generate formula candidates."""
        candidates = []

        if not self.root_extractor:
            self.residuals_accumulator.append("root_extractor_unavailable")
            return ()

        try:
            result = self.root_extractor.extract(clitics.stem)
            if result:
                candidates.append(
                    FormulaCandidate(
                        pattern="فَعَلَ",  # Simplified
                        root=''.join(result.letters) if hasattr(result, 'letters') else None,
                        formula_class=FormulaClass.VERB_PAST,
                        confidence=0.7,
                        residuals=frozenset()
                    )
                )
        except Exception as e:
            self.residuals_accumulator.append(f"formula_generation_error:{type(e).__name__}")

        return tuple(candidates)

    def _classify_path_type(
        self, formulas: Tuple[FormulaCandidate, ...]
    ) -> PathType:
        """Classify morphological path type."""
        if not formulas:
            return PathType.UNKNOWN

        # Simple classification based on formula class
        fc = formulas[0].formula_class
        if fc in (FormulaClass.VERB_PAST, FormulaClass.VERB_PRESENT, FormulaClass.VERB_COMMAND):
            return PathType.VERB
        elif fc in (FormulaClass.ACTIVE_PARTICIPLE, FormulaClass.PASSIVE_PARTICIPLE):
            return PathType.MUSHTAQQ
        else:
            return PathType.JAMID

    def _determine_pattern_status(
        self, formulas: Tuple[FormulaCandidate, ...]
    ) -> PatternStatus:
        """Determine pattern recognition status."""
        if not formulas:
            return PatternStatus.UNKNOWN
        if len(formulas) == 1 and formulas[0].confidence > 0.8:
            return PatternStatus.KNOWN
        elif len(formulas) > 1:
            return PatternStatus.MULTIPLE
        else:
            return PatternStatus.CANDIDATE

    def _resolve_terminal_state(self, path_type: PathType) -> TerminalState:
        """Resolve terminal i'rab/bina state."""
        if path_type == PathType.VERB:
            return TerminalState.MABNI
        elif path_type in (PathType.JAMID, PathType.MUSHTAQQ):
            return TerminalState.MURAB
        else:
            return TerminalState.UNKNOWN

    # ========================================================================
    # Phase 4: C2b Syntax Readiness
    # ========================================================================

    def _assess_syntactic_readiness(
        self, terminal: TerminalState, path: PathType
    ) -> SyntacticReadiness:
        """Assess syntactic readiness."""
        if terminal == TerminalState.UNKNOWN or path == PathType.UNKNOWN:
            return SyntacticReadiness.BLOCKED
        return SyntacticReadiness.READY

    def _analyze_sentence_shape(self, path_type: PathType) -> Optional[SentenceShape]:
        """Analyze potential sentence shape."""
        if path_type == PathType.VERB:
            return SentenceShape.VERBAL
        elif path_type in (PathType.JAMID, PathType.MUSHTAQQ):
            return SentenceShape.NOMINAL
        return None

    def _project_role_candidates(
        self, path_type: PathType
    ) -> Tuple[RoleProjection, ...]:
        """Project syntactic role candidates."""
        roles = []

        if path_type == PathType.VERB:
            # Verb can be predicate, needs subject
            roles.append(
                RoleProjection(
                    role_type=RoleType.FAIL,
                    confidence=0.8,
                    requirements=frozenset(["subject_agreement"])
                )
            )
        elif path_type == PathType.MUSHTAQQ:
            # Participle can be subject, object, or attribute
            roles.append(
                RoleProjection(
                    role_type=RoleType.FAIL,
                    confidence=0.6,
                    requirements=frozenset(["subject_role"])
                )
            )
            roles.append(
                RoleProjection(
                    role_type=RoleType.MAFOOL,
                    confidence=0.5,
                    requirements=frozenset(["object_role"])
                )
            )
        elif path_type == PathType.JAMID:
            # Noun can be many things
            roles.append(
                RoleProjection(
                    role_type=RoleType.MUBTADA,
                    confidence=0.7,
                    requirements=frozenset(["nominal_sentence"])
                )
            )

        return tuple(roles)

    # ========================================================================
    # Governance
    # ========================================================================

    def _generate_trace_id(self) -> str:
        """Generate unique trace ID."""
        return f"dal_{uuid.uuid4().hex[:8]}"

    def _failure_result(self, trace_id: str) -> BuilderResult:
        """Create failure result with residuals."""
        return BuilderResult(
            candidate=None,
            success=False,
            residuals=frozenset(self.residuals_accumulator),
            trace_id=trace_id
        )
