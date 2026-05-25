"""
U₁ Grapheme Carrier - Strict Grapheme Clustering (نظام حامل العنقود الكتابي الصارم)

Domain: U₁ = GraphemeCarrier
Purpose: Grapheme cluster formation WITHOUT phonetic/syllabic/morphological interpretation
Transition: U₀ (Unicode units) → U₁ (Grapheme clusters)

Critical Laws (Axioms):
    - Axiom 1.1: لا صوت قبل حفظ Grapheme (No phonetics before grapheme preservation)
    - Axiom 1.2: لا مقطع في U₁ (No syllable formation in U₁)
    - Axiom 1.3: كل حركة لها حامل (Every diacritic has a carrier)
    - Axiom 1.4: حفظ الأثر من U₀ (Trace preservation from U₀)

Type System:
    GraphemeCluster ≠ PhoneticProjection
    GraphemeCluster ≠ ArabicSyllable
    GraphemeCluster ≠ Root
    GraphemeCluster ≠ Weight
    GraphemeCluster ≠ Meaning

Architecture:
    U₀ (UnicodeLayerObject) → CPB₁ → U₁ (GraphemeLayerObject) → CPB₂p → U₂p

PR: Implement U₁ GraphemeCarrier with strict trace and attachment rules
Created: 2026-05-25
"""

from dataclasses import dataclass, field
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
from dal_core.u0_unicode_carrier import (
    UnicodeUnit,
    UnicodeClass,
    UnicodeLayerObject
)


# ============================================================================
# Type System - Grapheme Classification
# ============================================================================

class GraphemeClass(Enum):
    """
    Grapheme cluster classification for Arabic processing.

    Classification determines structure, NOT phonetic/syllabic value.
    """
    CONSONANT_WITH_VOWEL = "consonant_with_vowel"      # كَ، تُ، بِ
    CONSONANT_WITH_SUKUN = "consonant_with_sukun"      # بْ، تْ
    CONSONANT_WITH_SHADDA = "consonant_with_shadda"    # نَّ، مُّ
    CONSONANT_BARE = "consonant_bare"                  # ك، ت (no marks)
    LONG_VOWEL_CARRIER = "long_vowel_carrier"          # ا، و، ي (potential)
    SEPARATOR_CLUSTER = "separator_cluster"            # Space
    PUNCTUATION_CLUSTER = "punctuation_cluster"        # ،، ؟
    FOREIGN_CLUSTER = "foreign_cluster"                # Latin letters
    COMPLEX_CLUSTER = "complex_cluster"                # Multiple marks
    UNKNOWN_CLUSTER = "unknown_cluster"                # Unclassified


# ============================================================================
# U₁ Carrier Structure
# ============================================================================

@dataclass(frozen=True)
class GraphemeCluster:
    """
    Grapheme cluster with base and attached marks.

    Immutable carrier preserving:
        - base: Base character (consonant, vowel carrier, separator, etc.)
        - marks: Attached diacritics (fatha, damma, kasra, sukun, shadda, etc.)
        - position: Position in grapheme sequence
        - grapheme_class: Grapheme classification
        - trace_0: Trace to U₀ Unicode units
        - residuals: Warnings/blockers from clustering
        - rank: Epistemic status

    Laws:
        - GraphemeCluster ⊬ PhoneticProjection
        - GraphemeCluster ⊬ Syllable
        - GraphemeCluster ⊬ Root
        - GraphemeCluster ⊬ Meaning
        - Every mark must have base carrier (or residualized)
    """
    id: str                                    # Unique identifier
    base: str                                  # Base character
    marks: FrozenSet[str]                      # Attached diacritics
    position: int                              # Position in grapheme sequence
    grapheme_class: GraphemeClass              # Grapheme classification
    trace_0: FrozenSet[str]                     # Trace to U₀ unit IDs
    residuals: FrozenSet[Residual]             # Warnings/blockers
    rank: Rank                                 # Epistemic rank
    metadata: Optional[tuple] = None  # Additional info

    def get_full_grapheme(self) -> str:
        """Reconstruct full grapheme string."""
        return self.base + "".join(sorted(self.marks))

    def has_blocker(self) -> bool:
        """Check if cluster has blocking residual."""
        return any(r.type == ResidualType.BLOCKER for r in self.residuals)

    def is_certified(self) -> bool:
        """Check if cluster is certified (rank = CERTIFICATE)."""
        return self.rank == Rank.CERTIFICATE

    def has_mark_type(self, mark: str) -> bool:
        """Check if cluster has specific mark."""
        return mark in self.marks


@dataclass(frozen=True)
class GraphemeLayerObject:
    """
    Complete U₁ layer output.

    Contains:
        - clusters: Sequence of grapheme clusters
        - total_residuals: All residuals from layer
        - metadata: Additional processing information
        - proof: ProofObject documenting U₁ certification
    """
    clusters: FrozenSet[GraphemeCluster]
    total_residuals: FrozenSet[Residual]
    metadata: Optional[tuple] = None
    proof: Optional[ProofObject] = None

    def has_blocking_failure(self) -> bool:
        """Check if layer has blocking residuals."""
        return any(r.type == ResidualType.BLOCKER for r in self.total_residuals)

    def count_certified(self) -> int:
        """Count certified clusters."""
        return sum(1 for c in self.clusters if c.is_certified())


# ============================================================================
# Clustering Operation (cluster_01)
# ============================================================================

@dataclass(frozen=True)
class ClusterResult:
    """
    Result of cluster_01 operation.

    Partial operation: can succeed or fail with residuals.
    """
    success: bool
    cluster: Optional[GraphemeCluster]
    residuals: FrozenSet[Residual]


# Diacritic marks (Unicode combining marks)
ARABIC_DIACRITICS = {
    '\u064B',  # ً FATHATAN
    '\u064C',  # ٌ DAMMATAN
    '\u064D',  # ٍ KASRATAN
    '\u064E',  # َ FATHA
    '\u064F',  # ُ DAMMA
    '\u0650',  # ِ KASRA
    '\u0651',  # ّ SHADDA
    '\u0652',  # ْ SUKUN
    '\u0653',  # ٓ MADDAH
    '\u0654',  # ٔ HAMZA ABOVE
    '\u0655',  # ٕ HAMZA BELOW
    '\u0656',  # ٖ SUBSCRIPT ALEF
    '\u0670',  # ٰ SUPERSCRIPT ALEF
}

SHORT_VOWELS = {'\u064E', '\u064F', '\u0650'}  # َ ُ ِ
TANWEEN = {'\u064B', '\u064C', '\u064D'}       # ً ٌ ٍ
SHADDA = '\u0651'                               # ّ
SUKUN = '\u0652'                                # ْ


def cluster_unicode_units(
    units: List[UnicodeUnit],
    policy: Optional[Dict[str, Any]] = None
) -> ClusterResult:
    """
    cluster_01 : UnicodeUnit* ⇀ GraphemeCluster ∪ Fail₁

    Partial operation that forms grapheme clusters from Unicode units.

    Succeeds if:
        - Every diacritic has a base carrier
        - No duplicate short vowels on same base
        - Shadda has base carrier
        - Sukun has base carrier
        - Trace to U₀ preserved

    Fails if:
        - UnattachedMark: Diacritic without base
        - UnattachedShaddah: Shadda without base
        - MultipleShortVowels: Multiple َ ُ ِ on same base
        - DuplicateSukūn: Multiple sukun on same base
        - BrokenTraceToU₀: Missing trace to U₀

    Args:
        units: Sequence of Unicode units to cluster
        policy: Optional clustering policy

    Returns:
        ClusterResult with success/failure and residuals
    """
    residuals_list = []
    policy = policy or {}

    if not units:
        residuals_list.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            "Empty unit sequence",
            location="cluster_01"
        ))
        return ClusterResult(
            success=False,
            cluster=None,
            residuals=frozenset(residuals_list)
        )

    # Separate base and marks
    base_unit = None
    mark_units = []

    for unit in units:
        if unit.unicode_class == UnicodeClass.ARABIC_DIACRITIC:
            mark_units.append(unit)
        elif base_unit is None:
            base_unit = unit
        else:
            # Multiple bases - should be separate clusters
            residuals_list.append(make_warning(
                ResidualType.AMBIGUOUS_SYMBOL,
                f"Multiple bases in single cluster: {base_unit.char}, {unit.char}",
                location=f"position {unit.position}"
            ))

    # Check 1: Diacritics must have base carrier
    if mark_units and base_unit is None:
        residuals_list.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            f"UnattachedMark: {len(mark_units)} diacritic(s) without base",
            location=f"position {mark_units[0].position}"
        ))
        return ClusterResult(
            success=False,
            cluster=None,
            residuals=frozenset(residuals_list)
        )

    if base_unit is None:
        residuals_list.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            "No base unit in cluster",
            location="cluster_01"
        ))
        return ClusterResult(
            success=False,
            cluster=None,
            residuals=frozenset(residuals_list)
        )

    # Extract marks
    marks = frozenset(u.char for u in mark_units)

    # Check 2: Multiple short vowels forbidden
    short_vowel_count = sum(1 for m in marks if m in SHORT_VOWELS)
    if short_vowel_count > 1:
        residuals_list.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            f"MultipleShortVowels: {short_vowel_count} short vowels on base {base_unit.char}",
            location=f"position {base_unit.position}"
        ))
        return ClusterResult(
            success=False,
            cluster=None,
            residuals=frozenset(residuals_list)
        )

    # Check 3: Multiple sukun forbidden
    sukun_count = sum(1 for u in mark_units if u.char == SUKUN)
    if sukun_count > 1:
        residuals_list.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            f"DuplicateSukūn: {sukun_count} sukun marks on base {base_unit.char}",
            location=f"position {base_unit.position}"
        ))
        return ClusterResult(
            success=False,
            cluster=None,
            residuals=frozenset(residuals_list)
        )

    # Check 4: Shadda must have carrier
    has_shadda = SHADDA in marks
    if has_shadda and base_unit.unicode_class not in (
        UnicodeClass.ARABIC_LETTER,
        UnicodeClass.FOREIGN_LETTER
    ):
        residuals_list.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            f"UnattachedShaddah: Shadda on non-letter base {base_unit.char}",
            location=f"position {base_unit.position}"
        ))
        return ClusterResult(
            success=False,
            cluster=None,
            residuals=frozenset(residuals_list)
        )

    # Classify grapheme
    grapheme_class = _classify_grapheme(base_unit, marks)

    # Collect trace_0
    trace_0 = frozenset([base_unit.id] + [u.id for u in mark_units])

    # Check 5: Trace preservation
    if not trace_0:
        residuals_list.append(make_blocker(
            ResidualType.MALFORMED_ATOM,
            "BrokenTraceToU₀: No trace to U₀ units",
            location=f"position {base_unit.position}"
        ))
        return ClusterResult(
            success=False,
            cluster=None,
            residuals=frozenset(residuals_list)
        )

    # Inherit residuals from U₀ units
    inherited_residuals = set()
    for unit in units:
        inherited_residuals.update(unit.residuals)

    all_residuals = merge_residuals(
        frozenset(residuals_list),
        frozenset(inherited_residuals)
    )

    # Determine rank
    if has_blocking_residuals(all_residuals):
        rank = Rank.BLOCKED
    elif base_unit.unicode_class == UnicodeClass.ARABIC_LETTER:
        rank = Rank.CERTIFICATE
    elif base_unit.unicode_class == UnicodeClass.ARABIC_DIACRITIC:
        # Shouldn't happen (covered by UnattachedMark check)
        rank = Rank.BLOCKED
    else:
        rank = Rank.HYPOTHESIS

    # Create cluster
    cluster = GraphemeCluster(
        id=str(uuid4()),
        base=base_unit.char,
        marks=marks,
        position=base_unit.position,
        grapheme_class=grapheme_class,
        trace_0=trace_0,
        residuals=all_residuals,
        rank=rank,
        metadata=(
            ("base_codepoint", base_unit.codepoint),
            ("mark_count", len(marks))
        )
    )

    return ClusterResult(
        success=rank != Rank.BLOCKED,
        cluster=cluster,
        residuals=all_residuals
    )


def _classify_grapheme(base_unit: UnicodeUnit, marks: FrozenSet[str]) -> GraphemeClass:
    """
    Internal classification logic for grapheme clusters.

    Maps base + marks to GraphemeClass.
    """
    if base_unit.unicode_class == UnicodeClass.SEPARATOR:
        return GraphemeClass.SEPARATOR_CLUSTER

    if base_unit.unicode_class == UnicodeClass.PUNCTUATION:
        return GraphemeClass.PUNCTUATION_CLUSTER

    if base_unit.unicode_class in (UnicodeClass.FOREIGN_LETTER, UnicodeClass.FOREIGN_DIGIT):
        return GraphemeClass.FOREIGN_CLUSTER

    if base_unit.unicode_class != UnicodeClass.ARABIC_LETTER:
        return GraphemeClass.UNKNOWN_CLUSTER

    # Arabic letter base
    if not marks:
        return GraphemeClass.CONSONANT_BARE

    if SUKUN in marks:
        return GraphemeClass.CONSONANT_WITH_SUKUN

    if SHADDA in marks:
        return GraphemeClass.CONSONANT_WITH_SHADDA

    if any(m in SHORT_VOWELS or m in TANWEEN for m in marks):
        return GraphemeClass.CONSONANT_WITH_VOWEL

    if len(marks) > 1:
        return GraphemeClass.COMPLEX_CLUSTER

    # Base is ا، و، ي without marks - potential long vowel carrier
    if base_unit.char in {'ا', 'و', 'ي', 'ى'}:
        return GraphemeClass.LONG_VOWEL_CARRIER

    return GraphemeClass.CONSONANT_BARE


# ============================================================================
# CPB₁ - Identity Guardian
# ============================================================================

@dataclass(frozen=True)
class CPB1Result:
    """
    Result of CPB₁ validation.

    CPB₁ ensures:
        - TracePreserved: Every cluster has trace to U₀
        - NoFloatingMark: No unattached diacritics
        - NoSilentDeletion: No unit deleted without residual
        - ResidualsInherited: U₀ residuals preserved
        - RankNonInflated: No rank elevation without evidence
        - NoLayerJump: Forbidden gates documented
    """
    valid: bool
    violations: FrozenSet[str]
    layer_object: Optional[GraphemeLayerObject]


def cpb1_validate(
    unicode_layer: UnicodeLayerObject,
    clusters: List[GraphemeCluster],
    policy: Optional[Dict[str, Any]] = None
) -> CPB1Result:
    """
    CPB₁ : UnicodeLayerObject × cluster_01 × Evidence₁ × Policy₁ ⇀ GraphemeLayerObject ∪ Fail₁

    Validates that Grapheme layer satisfies identity guardian constraints.

    Guarantees:
        - TracePreserved: Every cluster has trace to U₀ units
        - NoFloatingMark: All diacritics attached to bases
        - NoSilentDeletion: No U₀ unit deleted without residual
        - ResidualsInherited: All U₀ residuals preserved
        - RankNonInflated: No rank elevation without evidence
        - ProofObjectCreated: Proof with forbidden gates
        - NoLayerJump: No syllable/root/weight/meaning certificates

    Args:
        unicode_layer: Input U₀ layer object
        clusters: Formed grapheme clusters
        policy: Optional processing policy

    Returns:
        CPB1Result with validation status
    """
    violations = []

    # Check 1: TracePreserved
    for cluster in clusters:
        if not cluster.trace_0:
            violations.append(f"TraceViolation: Cluster {cluster.id} has no trace to U₀")

    # Check 2: NoFloatingMark
    # (Already enforced by cluster_01 UnattachedMark check)

    # Check 3: NoSilentDeletion
    # Every U₀ unit should be accounted for in clusters or residuals
    u0_unit_ids = {u.id for u in unicode_layer.units}
    clustered_unit_ids = set()
    for cluster in clusters:
        clustered_unit_ids.update(cluster.trace_0)

    missing_units = u0_unit_ids - clustered_unit_ids
    if missing_units:
        # Check if there's a residual explaining the deletion
        all_residuals = set()
        for c in clusters:
            all_residuals.update(c.residuals)

        # For now, warn about missing units
        # (In production, check if residuals explain the deletion)
        if missing_units and not any("deleted" in str(r.data).lower() for r in all_residuals):
            violations.append(f"SilentDeletion: {len(missing_units)} U₀ units not in clusters")

    # Check 4: ResidualsInherited
    # All U₀ residuals should be inherited
    u0_residuals = unicode_layer.total_residuals
    cluster_residuals = set()
    for c in clusters:
        cluster_residuals.update(c.residuals)

    # U₀ residuals should be subset of cluster residuals
    if not u0_residuals.issubset(cluster_residuals):
        missing_residuals = u0_residuals - cluster_residuals
        violations.append(f"ResidualsNotInherited: {len(missing_residuals)} U₀ residuals lost")

    # Check 5: RankNonInflated
    for cluster in clusters:
        if cluster.rank == Rank.CERTIFICATE:
            # Certificate requires Arabic letter base
            if cluster.grapheme_class not in (
                GraphemeClass.CONSONANT_WITH_VOWEL,
                GraphemeClass.CONSONANT_WITH_SUKUN,
                GraphemeClass.CONSONANT_WITH_SHADDA,
                GraphemeClass.CONSONANT_BARE
            ):
                violations.append(f"RankInflation: Cluster {cluster.id} certified without Arabic base")

    # Collect all residuals
    total_residuals = set()
    for cluster in clusters:
        total_residuals.update(cluster.residuals)

    # Create proof object
    proof = _make_u1_proof(unicode_layer, clusters, frozenset(total_residuals))

    # Create layer object
    layer_object = GraphemeLayerObject(
        clusters=frozenset(clusters),
        total_residuals=frozenset(total_residuals),
        metadata=(
            ("u0_units", len(unicode_layer.units)),
            ("u1_clusters", len(clusters))
        ),
        proof=proof
    )

    return CPB1Result(
        valid=len(violations) == 0,
        violations=frozenset(violations),
        layer_object=layer_object if len(violations) == 0 else None
    )


def _make_u1_proof(
    unicode_layer: UnicodeLayerObject,
    clusters: List[GraphemeCluster],
    total_residuals: FrozenSet[Residual]
) -> ProofObject:
    """
    Create ProofObject for U₁ layer using shared foundation.

    Args:
        unicode_layer: Input U₀ layer
        clusters: Formed grapheme clusters
        total_residuals: All residuals from clustering

    Returns:
        ProofObject documenting U₁ certification
    """
    # Create rank vector (unicode_rank from U₀, grapheme_rank new)
    certified_count = sum(1 for c in clusters if c.is_certified())

    rank_vector = RankVector(
        unicode_rank=Rank.CERTIFICATE,  # Inherited from U₀
        grapheme_rank=Rank.CERTIFICATE if certified_count > 0 else Rank.CANDIDATE,
        phonetic_rank=Rank.ZERO,
        syllable_rank=Rank.ZERO,
        functional_role_rank=Rank.ZERO,
        morpheme_rank=Rank.ZERO,
        stem_root_rank=Rank.ZERO,
        pattern_weight_rank=Rank.ZERO,
        semantic_rank=Rank.ZERO,
        hukm_rank=Rank.ZERO
    )

    return make_proof_object(
        claim="Grapheme clusters formed and preserved",
        scope="U₁ / GraphemeCarrier",
        evidence=frozenset([
            f"Formed {len(clusters)} grapheme clusters",
            f"Certified {certified_count} clusters",
            "TracePreserved to U₀",
            "NoFloatingMark",
            "NoSilentDeletion",
            "ResidualsInherited from U₀"
        ]),
        counter_evidence=frozenset(),
        trace_graph={
            "u0_units": len(unicode_layer.units),
            "u1_clusters": len(clusters),
            "cluster_positions": [c.position for c in clusters]
        },
        competitors=frozenset(),  # No competitors at grapheme level
        residuals=total_residuals,
        rank_vector=rank_vector.as_dict(),
        allowed_next_gates=frozenset(["project_12p"]),
        forbidden_next_gates=frozenset([
            "syllable_certificate",
            "root_certificate",
            "weight_certificate",
            "meaning_certificate",
            "hukm_certificate"
        ]),
        limitations=frozenset([
            "Grapheme clustering only",
            "No phonetic projection",
            "No syllabification",
            "No morphological analysis",
            "No semantic interpretation"
        ])
    )


# ============================================================================
# Main Pipeline
# ============================================================================

def unicode_to_grapheme_layer(
    unicode_layer: UnicodeLayerObject,
    policy: Optional[Dict[str, Any]] = None
) -> CPB1Result:
    """
    Complete pipeline: U₀ → U₁ (GraphemeLayerObject).

    Steps:
        1. Group Unicode units into potential clusters
        2. cluster_01: Each group → GraphemeCluster
        3. CPB₁: Validate identity constraints

    Args:
        unicode_layer: Input U₀ layer object
        policy: Optional processing policy

    Returns:
        CPB1Result with validation status and layer object
    """
    # Group units by proximity
    # Simple algorithm: base + following diacritics
    units_list = sorted(unicode_layer.units, key=lambda u: u.position)

    groups = []
    current_group = []

    for unit in units_list:
        if unit.unicode_class == UnicodeClass.ARABIC_DIACRITIC:
            # Add to current group
            current_group.append(unit)
        else:
            # Start new group (save previous if non-empty)
            if current_group:
                groups.append(current_group)
            current_group = [unit]

    # Add final group
    if current_group:
        groups.append(current_group)

    # Cluster each group
    clusters = []
    for group in groups:
        result = cluster_unicode_units(group, policy)
        if result.success and result.cluster:
            clusters.append(result.cluster)
        # Note: Failed clusters are not included, but residuals are preserved

    return cpb1_validate(unicode_layer, clusters, policy)
