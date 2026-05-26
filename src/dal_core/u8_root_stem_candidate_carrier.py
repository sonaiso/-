"""
U₈ Root/Stem Candidate Carrier (حامل مرشحات الجذر والجذع)

Domain: U₈ = RootStemCandidateCarrier
Purpose: Open root/stem candidate paths based on U₇ pre-weight contract permission
Transition: U₇ (PreWeightContract) → U₈ (RootStemCandidate) → U₉ (Weight)

Critical Laws (Axioms):
    - Axiom 8.1: لا جذر قبل عقد ما قبل الوزن (No root before pre-weight contract)
    - Axiom 8.2: الجذر في U₈ مرشح لا شهادة (Root in U₈ is candidate, not certificate)
    - Axiom 8.3: لا وزن قبل مرشح الجذر (No weight before root candidate)
    - Axiom 8.4: المحجوب في U₇ محجوب في U₈ (Blocked in U₇ remains blocked in U₈)
    - Axiom 8.5: المرشح ≠ الشهادة (Candidate ≠ certificate)
    - Axiom 8.6: لا معنى قبل الوزن (No meaning before weight)

Type System:
    RootCandidate ≠ RootCertificate
    StemCandidate ≠ StemCertificate
    RootCandidate ⊬ Weight
    RootCandidate ⊬ Pattern
    RootCandidate ⊬ Meaning
    RootCandidate ⊬ Hukm

Architecture:
    U₇ (PreWeightContractLayerObject) → CPB₈ → U₈ (RootStemCandidateLayerObject) → CPB₉ → Weight

Key Principle:
    U₈ reads U₇ contract permissions and opens root/stem candidate paths.
    U₈ does NOT certify roots, does NOT determine weights, does NOT assign meanings.
    U₈ answers: "ما المرشحات الممكنة للجذر/الجذع؟" (What are possible root/stem candidates?)

Example Analysis:
    From U₇ units [وَ(blocked), بِ(blocked), كِتَاب(possible), ـهِمْ(blocked)]:
        - وَ → root_status=blocked, stem_status=blocked, no candidates
        - بِ → root_status=blocked, stem_status=blocked, no candidates
        - كِتَاب → root_candidates=[(ك,ت,ب)], stem_candidates=[كتاب], status=candidate
        - ـهِمْ → root_status=blocked, stem_status=blocked, pronoun path preserved

U₈ Output:
    Gives U₉:
        - Root candidate paths (triliteral/quadriliteral candidates, NOT certified)
        - Stem candidate paths (core surface structures, NOT certified)
        - Radical count hints (triliteral_possible/quadriliteral_possible)
        - Weak radical hints (weak_alif/weak_waw/weak_yaa possible)
        - Blocking potentials (jamid/proper_name/loanword/frozen_primitive)
        - Residuals (ambiguities, competing candidates)
        - Rank (zero → candidate → hypothesis, NO certificate)

U₈ Does NOT Give:
    - Root certificates (U₈+)
    - Stem certificates (U₈+)
    - Weight/pattern determination (U₉)
    - Meaning/semantic interpretation (U₁₅)
    - Reference resolution (U₁₅)
    - Grammatical hukm (U₇+)

PR: U8-ROOT-STEM-CANDIDATE
Created: 2026-05-26
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import List, Optional, FrozenSet, Dict, Any, Tuple
from uuid import uuid4

from dal_core.residuals import Residual, ResidualType, make_blocker, make_warning
from dal_core.foundation import (
    Rank,
    RankVector,
    ProofObject,
    make_proof_object,
    ResidualSet,
    merge_residuals,
    has_blocking_residuals
)
from dal_core.u7_pre_weight_contract_carrier import (
    PreWeightContractLayerObject,
    PreWeightContractUnit,
    ContractStatus,
    PathPermission,
)


# ============================================================================
# Type System - Root/Stem Candidate Classification
# ============================================================================

class RootCandidateStatus(Enum):
    """
    Root candidate status (NOT certificate).

    This is CANDIDATE classification, not root certification.
    U₈ determines if root candidates exist, NOT if they are verified/certified.
    """
    CANDIDATE = "candidate"                      # مرشح (possible root candidate)
    BLOCKED = "blocked"                          # محجوب (blocked by U₇)
    DEFERRED = "deferred"                        # مؤجل (deferred, needs evidence)
    UNRESOLVED = "unresolved"                    # غير محسوم (ambiguous)
    MULTIPLE_CANDIDATES = "multiple_candidates"  # مرشحات متعددة (competing candidates)


class StemCandidateStatus(Enum):
    """
    Stem candidate status (NOT certificate).

    This is CANDIDATE classification, not stem certification.
    """
    CANDIDATE = "candidate"                      # مرشح
    BLOCKED = "blocked"                          # محجوب
    DEFERRED = "deferred"                        # مؤجل
    UNRESOLVED = "unresolved"                    # غير محسوم
    MULTIPLE_CANDIDATES = "multiple_candidates"  # مرشحات متعددة


class RadicalCountHint(Enum):
    """
    Hint about radical count (NOT certificate).

    This is a HINT, not a final judgment.
    """
    TRILITERAL_POSSIBLE = "triliteral_possible"          # ثلاثي ممكن
    QUADRILITERAL_POSSIBLE = "quadriliteral_possible"    # رباعي ممكن
    QUINQUELITERAL_POSSIBLE = "quinqueliteral_possible"  # خماسي ممكن
    AMBIGUOUS = "ambiguous"                              # ملتبس
    UNRESOLVED = "unresolved"                            # غير محسوم


class WeakRadicalHint(Enum):
    """
    Hint about weak radicals (NOT certificate).

    This is a HINT, not a final judgment.
    """
    POSSIBLE_WEAK_ALIF = "possible_weak_alif"      # ممكن معتل الألف
    POSSIBLE_WEAK_WAW = "possible_weak_waw"        # ممكن معتل الواو
    POSSIBLE_WEAK_YAA = "possible_weak_yaa"        # ممكن معتل الياء
    POSSIBLE_DOUBLED = "possible_doubled"          # ممكن مضعّف
    POSSIBLE_HAMZATED = "possible_hamzated"        # ممكن مهموز
    SOUND = "sound"                                # سالم محتمل
    UNRESOLVED = "unresolved"                      # غير محسوم


class RootStemFailureType(Enum):
    """Failure types for root/stem candidate determination."""
    NO_PRE_WEIGHT_UNITS = "no_pre_weight_units"
    ALL_UNITS_BLOCKED = "all_units_blocked"
    INVALID_INPUT_LAYER = "invalid_input_layer"
    TRACE_LOSS = "trace_loss"


# ============================================================================
# Root/Stem Candidate Structures
# ============================================================================

@dataclass(frozen=True)
class RootCandidate:
    """
    Root candidate (NOT root certificate).

    This represents a POSSIBLE root, not a verified/certified root.
    """
    radicals: Tuple[str, ...]  # e.g., ("ك", "ت", "ب")
    radical_count: int  # 3 for triliteral, 4 for quadriliteral
    confidence: float  # [0.0, 1.0]
    evidence: Tuple[str, ...]  # Why this is a candidate
    weak_radical_positions: Tuple[int, ...]  # Indices of weak radicals (if any)
    hamza_positions: Tuple[int, ...]  # Indices of hamza radicals (if any)
    doubled: bool  # True if doubled radical (مضعّف)


@dataclass(frozen=True)
class StemCandidate:
    """
    Stem candidate (NOT stem certificate).

    This represents a POSSIBLE stem/core form, not a verified stem.
    """
    surface: str  # Stem surface (e.g., "كتاب", "كتب")
    confidence: float  # [0.0, 1.0]
    evidence: Tuple[str, ...]  # Why this is a candidate


# ============================================================================
# Core Structures
# ============================================================================

@dataclass(frozen=True)
class RootStemCandidateUnit:
    """
    U₈ root/stem candidate unit for a pre-weight contract unit.

    This represents ROOT/STEM CANDIDATES, NOT certificates.
    Candidates are HYPOTHESES requiring further evidence for certification.

    Forbidden fields (CRITICAL - these cause ValueError):
        - weight (that's U₉)
        - weight_certificate (that's U₉+)
        - pattern (that's U₉)
        - pattern_certificate (that's U₉+)
        - meaning (that's U₁₅)
        - dalalah (that's U₁₅)
        - ifadah (that's U₁₅)
        - hukm (that's U₇+)
        - final_irab (that's U₇+)
        - resolved_reference (that's U₁₅)
        - root_certificate (that's U₈+, NOT U₈)
        - stem_certificate (that's U₈+, NOT U₈)
    """
    uid: str
    surface: str  # Orthographic surface from U₇
    source_u7_unit_id: str  # Trace to U₇ pre-weight contract unit
    source_u7_trace: Tuple[str, ...]  # Ordered trace to U₇

    # Root/stem candidate paths (NOT certificates)
    root_status: RootCandidateStatus  # Root candidate status
    stem_status: StemCandidateStatus  # Stem candidate status

    # Root candidates (CANDIDATES, NOT certificates)
    root_candidate_paths: Tuple[RootCandidate, ...]  # Possible roots
    stem_candidate_paths: Tuple[StemCandidate, ...]  # Possible stems

    # Hints (NOT certificates)
    radical_count_hint: RadicalCountHint
    weak_radical_hint: WeakRadicalHint

    # Blocking potentials (hints about why extraction might fail)
    jamid_blocking_potential: PathPermission  # Frozen/non-derivational blocks root
    proper_name_blocking_potential: PathPermission  # Proper name blocks free root
    loanword_blocking_potential: PathPermission  # Loanword blocks Arabic root
    frozen_primitive_blocking_potential: PathPermission  # Frozen primitive blocks derivation

    # Evidence and blocking
    required_evidence: Tuple[str, ...]  # What evidence is needed for certification
    blocked_paths: Tuple[str, ...]  # Paths blocked at this layer
    residuals: FrozenSet[Residual]
    rank: Rank
    trace: Tuple[str, ...]  # Full ordered trace from U₀

    def __post_init__(self):
        """Validate root/stem candidate unit - CRITICAL constitutional checks."""
        # FORBIDDEN FIELDS - These MUST NOT exist
        forbidden_fields = [
            'weight', 'weight_certificate',
            'pattern', 'pattern_certificate',
            'meaning', 'dalalah', 'ifadah',
            'hukm', 'final_irab',
            'resolved_reference',
            'root_certificate',  # U₈ has candidates, NOT certificates
            'stem_certificate',  # U₈ has candidates, NOT certificates
        ]

        for field in forbidden_fields:
            if hasattr(self, field):
                raise ValueError(
                    f"RootStemCandidateUnit MUST NOT contain '{field}' field "
                    f"(Axiom 8.2-8.6 violation)"
                )


@dataclass(frozen=True)
class RootStemCandidateLayerObject:
    """
    U₈ layer object containing root/stem candidate classifications.

    Provides root/stem candidate paths for weight/pattern determination.
    Blocked units do NOT have candidate paths (blocked in U₇).
    Candidate units have POSSIBLE roots/stems (not certified).
    """
    uid: str
    units: Tuple[RootStemCandidateUnit, ...]  # Candidate units
    source_pre_weight_layer_id: str  # Trace to U₇ layer
    trace_7: Tuple[str, ...]  # Ordered trace to U₇
    residuals: FrozenSet[Residual]
    rank: Rank
    proof: Optional[ProofObject] = None

    def __post_init__(self):
        """Validate root/stem candidate layer object."""
        # FORBIDDEN FIELDS
        forbidden_fields = [
            'weight', 'weight_certificate',
            'pattern', 'pattern_certificate',
            'meaning', 'dalalah', 'ifadah',
            'hukm', 'final_irab',
            'resolved_reference',
            'root_certificate',
            'stem_certificate',
        ]

        for field in forbidden_fields:
            if hasattr(self, field):
                raise ValueError(
                    f"RootStemCandidateLayerObject MUST NOT contain '{field}' field"
                )


@dataclass(frozen=True)
class RootStemCandidateResult:
    """Result of root/stem candidate determination."""
    success: bool
    layer_object: Optional[RootStemCandidateLayerObject]
    failure_type: Optional[RootStemFailureType]
    message: str
    residuals: FrozenSet[Residual]


# ============================================================================
# CPB₈ - Completeness Predicate and Proof Builder
# ============================================================================

@dataclass(frozen=True)
class CPB8:
    """
    CPB₈: Completeness Predicate and Proof Builder for RootStemCandidate layer.

    Guards:
        - Root/stem candidate statuses determined
        - Candidate paths opened (for approved U₇ units)
        - Blocked units preserved (from U₇)
        - Pre-weight contract trace preserved
        - No forbidden fields (weight, pattern, meaning, hukm, certificates, etc.)
        - Allowed next gate: U₉ Weight (for candidates only)
    """

    @staticmethod
    def is_complete(layer_obj: RootStemCandidateLayerObject) -> bool:
        """Check if root/stem candidate layer object is complete."""
        if not layer_obj.units:
            return False

        if not layer_obj.source_pre_weight_layer_id:
            return False

        # Check no forbidden fields
        for unit in layer_obj.units:
            forbidden = [
                'weight', 'weight_certificate',
                'pattern', 'pattern_certificate',
                'meaning', 'dalalah', 'ifadah',
                'hukm', 'final_irab',
                'resolved_reference',
                'root_certificate',
                'stem_certificate',
            ]
            if any(hasattr(unit, field) for field in forbidden):
                return False

        return True

    @staticmethod
    def build_proof(layer_obj: RootStemCandidateLayerObject) -> ProofObject:
        """Build proof object for root/stem candidate layer."""
        # Count statuses
        blocked_count = sum(
            1 for u in layer_obj.units
            if u.root_status == RootCandidateStatus.BLOCKED
        )
        candidate_count = sum(
            1 for u in layer_obj.units
            if u.root_status == RootCandidateStatus.CANDIDATE
        )
        multiple_candidates_count = sum(
            1 for u in layer_obj.units
            if u.root_status == RootCandidateStatus.MULTIPLE_CANDIDATES
        )
        deferred_count = sum(
            1 for u in layer_obj.units
            if u.root_status == RootCandidateStatus.DEFERRED
        )

        # Count total root candidates across all units
        total_root_candidates = sum(
            len(u.root_candidate_paths) for u in layer_obj.units
        )
        total_stem_candidates = sum(
            len(u.stem_candidate_paths) for u in layer_obj.units
        )

        return make_proof_object(
            claim="U₈ root/stem candidate paths opened",
            scope="U8_ROOT_STEM_CANDIDATE",
            evidence=frozenset([
                f"units_count={len(layer_obj.units)}",
                f"blocked_count={blocked_count}",
                f"candidate_count={candidate_count}",
                f"multiple_candidates_count={multiple_candidates_count}",
                f"deferred_count={deferred_count}",
                f"total_root_candidates={total_root_candidates}",
                f"total_stem_candidates={total_stem_candidates}",
                f"trace_preserved={bool(layer_obj.source_pre_weight_layer_id)}",
                f"rank={layer_obj.rank.value}",
            ]),
            counter_evidence=frozenset(),
            trace_graph={},
            competitors=frozenset(),
            residuals=layer_obj.residuals,
            rank_vector={},
            allowed_next_gates=frozenset({"weight_pattern_gate"}),
            forbidden_next_gates=frozenset({
                "root_certificate",
                "stem_certificate",
                "weight_certificate",
                "pattern_certificate",
                "meaning_certificate",
                "hukm_certificate",
            }),
            limitations=frozenset([
                "no_root_certificate",
                "no_stem_certificate",
                "no_weight_determination",
                "no_pattern_determination",
                "no_meaning_assignment",
                "no_hukm_judgment",
                "candidate_is_hypothesis_not_certificate",
                "blocked_units_must_not_proceed_to_weight",
                "candidates_may_proceed_to_weight_with_evidence",
            ]),
        )


# ============================================================================
# Root/Stem Candidate Extraction Logic
# ============================================================================

def _extract_root_candidates(
    surface: str,
    contract_unit: PreWeightContractUnit
) -> Tuple[Tuple[RootCandidate, ...], List[str]]:
    """
    Extract root candidates from surface.

    This is CANDIDATE EXTRACTION, not root certification.
    Returns possible roots with evidence.

    Args:
        surface: Orthographic surface
        contract_unit: U₇ pre-weight contract unit

    Returns:
        (root_candidates_tuple, evidence_list)
    """
    evidence = []
    candidates = []

    # Remove diacritics for analysis
    surface_no_diacritics = ''.join(
        c for c in surface
        if c not in ['َ', 'ِ', 'ُ', 'ْ', 'ّ', 'ً', 'ٍ', 'ٌ']
    )

    # Simple triliteral extraction (placeholder - real implementation would be more sophisticated)
    if len(surface_no_diacritics) >= 3:
        # Try extracting consonants as potential root
        consonants = [c for c in surface_no_diacritics if c not in ['ا', 'و', 'ي', 'ى']]

        if len(consonants) >= 3:
            # Triliteral candidate
            root_radicals = tuple(consonants[:3])
            evidence.append(f"triliteral_extraction={'-'.join(root_radicals)}")
            evidence.append("simple_consonant_extraction")

            # Check for weak radicals
            weak_positions = tuple(
                i for i, c in enumerate(root_radicals)
                if c in ['ا', 'و', 'ي', 'ى']
            )

            # Check for hamza
            hamza_positions = tuple(
                i for i, c in enumerate(root_radicals)
                if c in ['أ', 'إ', 'آ', 'ؤ', 'ئ', 'ء']
            )

            # Check for doubled
            doubled = len(root_radicals) >= 2 and root_radicals[-1] == root_radicals[-2]

            candidate = RootCandidate(
                radicals=root_radicals,
                radical_count=3,
                confidence=0.5,  # Low confidence - needs lexical verification
                evidence=tuple(evidence),
                weak_radical_positions=weak_positions,
                hamza_positions=hamza_positions,
                doubled=doubled
            )
            candidates.append(candidate)

        # Check for quadriliteral
        if len(consonants) >= 4:
            root_radicals = tuple(consonants[:4])
            evidence.append(f"quadriliteral_possible={'-'.join(root_radicals)}")

            candidate = RootCandidate(
                radicals=root_radicals,
                radical_count=4,
                confidence=0.3,  # Lower confidence - quadriliterals are less common
                evidence=tuple(evidence),
                weak_radical_positions=(),
                hamza_positions=(),
                doubled=False
            )
            candidates.append(candidate)

    return (tuple(candidates), evidence)


def _extract_stem_candidates(
    surface: str,
    contract_unit: PreWeightContractUnit
) -> Tuple[Tuple[StemCandidate, ...], List[str]]:
    """
    Extract stem candidates from surface.

    This is CANDIDATE EXTRACTION, not stem certification.
    Returns possible stems with evidence.

    Args:
        surface: Orthographic surface
        contract_unit: U₇ pre-weight contract unit

    Returns:
        (stem_candidates_tuple, evidence_list)
    """
    evidence = []
    candidates = []

    # Remove diacritics for core stem
    surface_no_diacritics = ''.join(
        c for c in surface
        if c not in ['َ', 'ِ', 'ُ', 'ْ', 'ّ', 'ً', 'ٍ', 'ٌ']
    )

    # Simple stem: treat surface as potential stem
    evidence.append(f"surface_stem={surface_no_diacritics}")
    evidence.append("direct_surface_extraction")

    stem_candidate = StemCandidate(
        surface=surface_no_diacritics,
        confidence=0.6,
        evidence=tuple(evidence)
    )
    candidates.append(stem_candidate)

    return (tuple(candidates), evidence)


def _determine_radical_count_hint(
    root_candidates: Tuple[RootCandidate, ...]
) -> RadicalCountHint:
    """Determine radical count hint from root candidates."""
    if not root_candidates:
        return RadicalCountHint.UNRESOLVED

    radical_counts = set(c.radical_count for c in root_candidates)

    if len(radical_counts) > 1:
        return RadicalCountHint.AMBIGUOUS

    count = radical_counts.pop()
    if count == 3:
        return RadicalCountHint.TRILITERAL_POSSIBLE
    elif count == 4:
        return RadicalCountHint.QUADRILITERAL_POSSIBLE
    elif count == 5:
        return RadicalCountHint.QUINQUELITERAL_POSSIBLE
    else:
        return RadicalCountHint.UNRESOLVED


def _determine_weak_radical_hint(
    root_candidates: Tuple[RootCandidate, ...]
) -> WeakRadicalHint:
    """Determine weak radical hint from root candidates."""
    if not root_candidates:
        return WeakRadicalHint.UNRESOLVED

    # Check first candidate (simplified)
    candidate = root_candidates[0]

    if candidate.weak_radical_positions:
        # Check which weak letters appear
        weak_radicals = [candidate.radicals[i] for i in candidate.weak_radical_positions]
        if 'ا' in weak_radicals or 'ى' in weak_radicals:
            return WeakRadicalHint.POSSIBLE_WEAK_ALIF
        elif 'و' in weak_radicals:
            return WeakRadicalHint.POSSIBLE_WEAK_WAW
        elif 'ي' in weak_radicals:
            return WeakRadicalHint.POSSIBLE_WEAK_YAA

    if candidate.hamza_positions:
        return WeakRadicalHint.POSSIBLE_HAMZATED

    if candidate.doubled:
        return WeakRadicalHint.POSSIBLE_DOUBLED

    return WeakRadicalHint.SOUND


# ============================================================================
# Root/Stem Candidate Operations
# ============================================================================

def root_stem_candidate_8(
    pre_weight_layer: PreWeightContractLayerObject
) -> RootStemCandidateResult:
    """
    Determine root/stem candidates from U₇ pre-weight contract layer.

    Critical Examples:
        وَ → blocked (root blocked, stem blocked, no candidates)
        بِ → blocked (root blocked, stem blocked, no candidates)
        ـهِمْ → blocked (pronoun, no root/stem extraction)
        كَتَبَ → candidate (root candidates: [ك-ت-ب], stem candidates: [كتب])
        كَاتِب → candidate (root candidates: [ك-ت-ب], stem candidates: [كاتب])
        مَكْتَب → candidate (root candidates: [ك-ت-ب], stem candidates: [مكتب])

    Args:
        pre_weight_layer: U₇ layer object with pre-weight contract permissions

    Returns:
        RootStemCandidateResult with root/stem candidates

    Critical Law:
        U₇.root_path_permission = BLOCKED → U₈ must skip / emit blocked record
        U₇.root_path_permission = POSSIBLE → U₈ may open root/stem candidate paths

    Forbidden:
        - Root certification (U₈+)
        - Stem certification (U₈+)
        - Weight determination (U₉)
        - Pattern certification (U₉+)
        - Meaning assignment (U₁₅)
        - Hukm judgment (U₇+)
    """
    # Validate input
    if not pre_weight_layer.units:
        return RootStemCandidateResult(
            success=False,
            layer_object=None,
            failure_type=RootStemFailureType.NO_PRE_WEIGHT_UNITS,
            message="No pre-weight contract units in input",
            residuals=frozenset([make_blocker("no_units", "Cannot determine root/stem candidates without pre-weight units")])
        )

    # Process each pre-weight contract unit
    candidate_units = []
    all_residuals = []

    for contract_unit in pre_weight_layer.units:
        # Check if root path is BLOCKED
        if contract_unit.root_path_permission == PathPermission.BLOCKED:
            # Unit blocked - no root/stem extraction
            blocked_unit = RootStemCandidateUnit(
                uid=str(uuid4()),
                surface=contract_unit.surface,
                source_u7_unit_id=contract_unit.uid,
                source_u7_trace=contract_unit.source_u6_trace,
                root_status=RootCandidateStatus.BLOCKED,
                stem_status=StemCandidateStatus.BLOCKED,
                root_candidate_paths=(),  # No candidates
                stem_candidate_paths=(),  # No candidates
                radical_count_hint=RadicalCountHint.UNRESOLVED,
                weak_radical_hint=WeakRadicalHint.UNRESOLVED,
                jamid_blocking_potential=contract_unit.jamid_surface_potential,
                proper_name_blocking_potential=contract_unit.proper_name_surface_potential,
                loanword_blocking_potential=contract_unit.loanword_surface_potential,
                frozen_primitive_blocking_potential=contract_unit.frozen_primitive_potential,
                required_evidence=contract_unit.required_evidence,
                blocked_paths=tuple(list(contract_unit.blocked_paths) + ["root_extraction", "stem_extraction"]),
                residuals=contract_unit.residuals,
                rank=contract_unit.rank,
                trace=contract_unit.trace
            )
            candidate_units.append(blocked_unit)
            all_residuals.extend(list(contract_unit.residuals))
            continue

        # Unit has POSSIBLE permission - extract candidates
        root_candidates, root_evidence = _extract_root_candidates(
            contract_unit.surface,
            contract_unit
        )
        stem_candidates, stem_evidence = _extract_stem_candidates(
            contract_unit.surface,
            contract_unit
        )

        # Determine statuses
        if len(root_candidates) == 0:
            root_status = RootCandidateStatus.UNRESOLVED
        elif len(root_candidates) == 1:
            root_status = RootCandidateStatus.CANDIDATE
        else:
            root_status = RootCandidateStatus.MULTIPLE_CANDIDATES

        if len(stem_candidates) == 0:
            stem_status = StemCandidateStatus.UNRESOLVED
        elif len(stem_candidates) == 1:
            stem_status = StemCandidateStatus.CANDIDATE
        else:
            stem_status = StemCandidateStatus.MULTIPLE_CANDIDATES

        # Determine hints
        radical_count_hint = _determine_radical_count_hint(root_candidates)
        weak_radical_hint = _determine_weak_radical_hint(root_candidates)

        # Build required evidence
        required_evidence = list(contract_unit.required_evidence)
        required_evidence.append("lexical_attestation_for_root")
        required_evidence.append("weight_pattern_for_stem")

        # Build RootStemCandidateUnit
        candidate_unit = RootStemCandidateUnit(
            uid=str(uuid4()),
            surface=contract_unit.surface,
            source_u7_unit_id=contract_unit.uid,
            source_u7_trace=contract_unit.source_u6_trace,
            root_status=root_status,
            stem_status=stem_status,
            root_candidate_paths=root_candidates,
            stem_candidate_paths=stem_candidates,
            radical_count_hint=radical_count_hint,
            weak_radical_hint=weak_radical_hint,
            jamid_blocking_potential=contract_unit.jamid_surface_potential,
            proper_name_blocking_potential=contract_unit.proper_name_surface_potential,
            loanword_blocking_potential=contract_unit.loanword_surface_potential,
            frozen_primitive_blocking_potential=contract_unit.frozen_primitive_potential,
            required_evidence=tuple(required_evidence),
            blocked_paths=contract_unit.blocked_paths,
            residuals=contract_unit.residuals,
            rank=contract_unit.rank,
            trace=contract_unit.trace
        )

        candidate_units.append(candidate_unit)
        all_residuals.extend(list(contract_unit.residuals))

    # Build layer object
    layer_obj = RootStemCandidateLayerObject(
        uid=str(uuid4()),
        units=tuple(candidate_units),
        source_pre_weight_layer_id=pre_weight_layer.uid,
        trace_7=(pre_weight_layer.uid,),
        residuals=frozenset(all_residuals),
        rank=pre_weight_layer.rank,  # Inherit rank from U₇
        proof=None
    )

    # Build proof
    proof = CPB8.build_proof(layer_obj)
    layer_obj = RootStemCandidateLayerObject(
        uid=layer_obj.uid,
        units=layer_obj.units,
        source_pre_weight_layer_id=layer_obj.source_pre_weight_layer_id,
        trace_7=layer_obj.trace_7,
        residuals=layer_obj.residuals,
        rank=layer_obj.rank,
        proof=proof
    )

    return RootStemCandidateResult(
        success=True,
        layer_object=layer_obj,
        failure_type=None,
        message=f"Root/stem candidates determined: {len(candidate_units)} units processed",
        residuals=layer_obj.residuals
    )


# ============================================================================
# Exports
# ============================================================================

__all__ = [
    # Core types
    'RootCandidateStatus',
    'StemCandidateStatus',
    'RadicalCountHint',
    'WeakRadicalHint',

    # Candidate structures
    'RootCandidate',
    'StemCandidate',

    # Structures
    'RootStemCandidateUnit',
    'RootStemCandidateLayerObject',
    'RootStemCandidateResult',

    # Failures
    'RootStemFailureType',

    # CPB
    'CPB8',

    # Operations
    'root_stem_candidate_8',
]
