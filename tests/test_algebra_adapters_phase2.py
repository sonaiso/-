"""Phase 2 adapter tests: FVAFK evidence adapters validation.

These tests prove the Phase 2 contracts:

1. **Read-only**: Adapters never mutate upstream objects.
2. **Evidence-only output**: Adapters produce Evidence, not bare values.
3. **Source citation**: Every Evidence cites upstream object.
4. **No semantic/hukm jump**: Adapters respect domain boundaries.
5. **CPB compliance**: Adapter Evidence passes CPB validation.
6. **Immutability**: BaseAdapter locks attributes after initialization.

Test coverage:

- BaseAdapter immutability and utility methods
- C1Adapter (encoding → GRAPHEME/PHONEME Evidence)
- C2aAdapter (phonology → PHONEME/SYLLABLE Evidence)
- C2bAdapter (RootExtractor → ROOT Evidence) — primary use case
- SyntaxAdapter (Link → SYNTAX Evidence)
- CPB validation for adapter outputs
- Domain boundary enforcement (no MORPH_SURFACE → SEMANTICS jump)
"""

from __future__ import annotations

import pytest

from fvafk.algebra import Domain, Evidence, Rank, Residual, Result, Carrier
from fvafk.algebra.adapters import (
    BaseAdapter,
    C1Adapter,
    C2aAdapter,
    C2bAdapter,
    SyntaxAdapter,
)
from fvafk.algebra.cpb import CPB, validate_cpb
from fvafk.c2b import RootExtractionResult, Root, RootType


# ---------------------------------------------------------------------------
# BaseAdapter immutability and contracts
# ---------------------------------------------------------------------------


def test_base_adapter_is_immutable_after_init():
    """BaseAdapter locks attribute assignment after __init__."""
    adapter = BaseAdapter(source_module="test")

    with pytest.raises(AttributeError, match="immutable"):
        adapter.source_module = "modified"  # type: ignore

    with pytest.raises(AttributeError, match="immutable"):
        adapter.new_field = "value"  # type: ignore


def test_base_adapter_forbids_attribute_deletion():
    """BaseAdapter forbids attribute deletion."""
    adapter = BaseAdapter(source_module="test")

    with pytest.raises(AttributeError, match="immutable"):
        del adapter.source_module  # type: ignore


def test_base_adapter_make_evidence_requires_citable_source():
    """make_evidence() requires either obj_id or span."""
    adapter = BaseAdapter(source_module="test")

    # obj_id provided — OK
    ev1 = adapter.make_evidence(
        kind="test.kind",
        obj_type="TestObject",
        obj_id="test123",
        detail="test detail",
    )
    assert ev1.source == "test:TestObject:test123"
    assert ev1.kind == "test.kind"

    # span provided — OK
    ev2 = adapter.make_evidence(
        kind="test.kind",
        obj_type="TestObject",
        span=(0, 5),
        detail="test detail",
    )
    assert ev2.source == "test:TestObject:span=0-5"

    # neither provided — ValueError
    with pytest.raises(ValueError, match="citable"):
        adapter.make_evidence(
            kind="test.kind",
            obj_type="TestObject",
            detail="no source",
        )


def test_base_adapter_make_residual_for_missing_id():
    """make_residual_for_missing_id() creates proper Residual."""
    adapter = BaseAdapter(source_module="test")

    residual = adapter.make_residual_for_missing_id("TestObject")
    assert residual.kind == "evidence.source_incomplete"
    assert "TestObject" in residual.description
    assert "stable id" in residual.description.lower()


# ---------------------------------------------------------------------------
# C1Adapter (encoding → GRAPHEME/PHONEME)
# ---------------------------------------------------------------------------


def test_c1_adapter_adapt_text_emits_encoding_evidence():
    """C1Adapter.adapt_text() emits encoding.validated Evidence."""
    adapter = C1Adapter()

    evidence_tuple = adapter.adapt_text("كاتب")

    assert len(evidence_tuple) >= 1
    ev = evidence_tuple[0]
    assert ev.kind == "encoding.validated"
    assert "كاتب" in ev.source
    assert "c1:" in ev.source


def test_c1_adapter_adapt_text_detects_normalization():
    """C1Adapter emits encoding.normalized when text changes."""
    adapter = C1Adapter()

    evidence_tuple = adapter.adapt_text("كَاتِب", normalized="كاتب")

    # Should have both validated and normalized Evidence
    kinds = {ev.kind for ev in evidence_tuple}
    assert "encoding.validated" in kinds
    assert "encoding.normalized" in kinds

    # Find the normalized Evidence
    norm_ev = next(ev for ev in evidence_tuple if ev.kind == "encoding.normalized")
    assert "كَاتِب" in norm_ev.detail
    assert "كاتب" in norm_ev.detail


def test_c1_adapter_adapt_dict_extracts_text_and_normalized():
    """C1Adapter.adapt() handles dict-like objects."""
    adapter = C1Adapter()

    obj = {"text": "كاتب", "normalized": "كاتب"}
    evidence_tuple = adapter.adapt(obj)

    assert len(evidence_tuple) >= 1
    assert any(ev.kind == "encoding.validated" for ev in evidence_tuple)


def test_c1_adapter_non_strict_returns_empty_for_unknown_type():
    """C1Adapter with strict=False returns () for unknown types."""
    adapter = C1Adapter(strict=False)

    result = adapter.adapt(12345)  # type: ignore
    assert result == ()


def test_c1_adapter_strict_raises_for_unknown_type():
    """C1Adapter with strict=True raises TypeError."""
    adapter = C1Adapter(strict=True)

    with pytest.raises(TypeError, match="expects dict or str"):
        adapter.adapt(12345)  # type: ignore


# ---------------------------------------------------------------------------
# C2aAdapter (phonology → PHONEME/SYLLABLE)
# ---------------------------------------------------------------------------


def test_c2a_adapter_adapt_gate_trace():
    """C2aAdapter adapts phonological gate traces."""
    adapter = C2aAdapter()

    trace = {"gate": "sukun_repair", "input": "كْتْب", "output": "كَتَبَ"}
    evidence_tuple = adapter.adapt(trace)

    assert len(evidence_tuple) >= 1
    ev = evidence_tuple[0]
    assert ev.kind == "phonology.gate_fired"
    assert "sukun_repair" in ev.detail
    assert "c2a:" in ev.source


def test_c2a_adapter_adapt_syllable_structure():
    """C2aAdapter adapts syllable structures."""
    adapter = C2aAdapter()

    syllable = {"pattern": "CVC", "span": (0, 3)}
    evidence_tuple = adapter.adapt(syllable)

    assert len(evidence_tuple) >= 1
    ev = evidence_tuple[0]
    assert ev.kind == "syllable.structure_detected"
    assert "CVC" in ev.detail
    assert "span=0-3" in ev.source


def test_c2a_adapter_adapt_gate_trace_convenience_method():
    """C2aAdapter.adapt_gate_trace() convenience method works."""
    adapter = C2aAdapter()

    evidence_tuple = adapter.adapt_gate_trace(
        gate_name="shadda_expansion",
        input_text="مدّ",
        output_text="مدد",
    )

    assert len(evidence_tuple) == 1
    ev = evidence_tuple[0]
    assert ev.kind == "phonology.gate_fired"
    assert "shadda_expansion" in ev.detail


# ---------------------------------------------------------------------------
# C2bAdapter (RootExtractor → ROOT) — PRIMARY USE CASE
# ---------------------------------------------------------------------------


def test_c2b_adapter_adapt_root_extraction_result():
    """C2bAdapter adapts RootExtractionResult to root.candidate Evidence."""
    root = Root(letters=("ك", "ت", "ب"), root_type=RootType.TRILATERAL)
    result = RootExtractionResult(
        root=root,
        normalized_word="كاتب",
        stripped_word="كاتب",
        prefix="",
        suffix="",
    )

    adapter = C2bAdapter()
    evidence_tuple = adapter.adapt(result)

    assert len(evidence_tuple) >= 1
    ev = evidence_tuple[0]
    assert ev.kind == "root.candidate"
    assert "c2b:" in ev.source
    assert "كاتب" in ev.source
    assert "('ك', 'ت', 'ب')" in ev.detail


def test_c2b_adapter_adapt_with_affixes():
    """C2bAdapter emits affix.detected Evidence for prefixes/suffixes."""
    root = Root(letters=("ك", "ت", "ب"), root_type=RootType.TRILATERAL)
    result = RootExtractionResult(
        root=root,
        normalized_word="والكاتب",
        stripped_word="كاتب",
        prefix="و+ال",
        suffix="",
    )

    adapter = C2bAdapter()
    evidence_tuple = adapter.adapt(result)

    # Should have root evidence + prefix evidence
    kinds = {ev.kind for ev in evidence_tuple}
    assert "root.candidate" in kinds
    assert "affix.detected" in kinds

    # Check prefix evidence
    prefix_ev = next(ev for ev in evidence_tuple if "prefix" in ev.detail)
    assert "و+ال" in prefix_ev.detail


def test_c2b_adapter_adapt_no_root_returns_empty():
    """C2bAdapter returns () when root is None."""
    result = RootExtractionResult(
        root=None,
        normalized_word="حتى",
        stripped_word="حتى",
        prefix="",
        suffix="",
    )

    adapter = C2bAdapter()
    evidence_tuple = adapter.adapt(result)

    assert evidence_tuple == ()


def test_c2b_adapter_adapt_with_residuals_detects_weak_letters():
    """C2bAdapter.adapt_with_residuals() emits root.weak_letters Residual."""
    # Root with multiple weak letters (و-ي-ا)
    root = Root(letters=("و", "ي", "ا"), root_type=RootType.TRILATERAL)
    result = RootExtractionResult(
        root=root,
        normalized_word="وَيَا",
        stripped_word="ويا",
        prefix="",
        suffix="",
    )

    adapter = C2bAdapter()
    evidence_tuple, residual_tuple = adapter.adapt_with_residuals(result)

    # Should have weak_letters residual
    assert any(r.kind == "root.weak_letters" for r in residual_tuple)


def test_c2b_adapter_adapt_with_residuals_detects_aggressive_stripping():
    """C2bAdapter detects aggressive affix stripping (stripped << normalized)."""
    root = Root(letters=("ك", "ت", "ب"), root_type=RootType.TRILATERAL)
    result = RootExtractionResult(
        root=root,
        normalized_word="استكتاب",  # 7 letters
        stripped_word="كت",  # 2 letters — ratio < 0.5
        prefix="است",
        suffix="اب",
    )

    adapter = C2bAdapter()
    evidence_tuple, residual_tuple = adapter.adapt_with_residuals(result)

    # Should have aggressive_stripping residual
    assert any(r.kind == "affix.aggressive_stripping" for r in residual_tuple)


def test_c2b_adapter_is_read_only():
    """C2bAdapter does not mutate RootExtractionResult."""
    root = Root(letters=("ك", "ت", "ب"), root_type=RootType.TRILATERAL)
    result = RootExtractionResult(
        root=root,
        normalized_word="كاتب",
        stripped_word="كاتب",
        prefix="",
        suffix="",
    )

    # Record original state
    original_root = result.root
    original_normalized = result.normalized_word

    adapter = C2bAdapter()
    adapter.adapt(result)

    # Verify no mutation
    assert result.root is original_root
    assert result.normalized_word == original_normalized


def test_c2b_adapter_strict_raises_for_wrong_type():
    """C2bAdapter with strict=True raises TypeError for non-RootExtractionResult."""
    adapter = C2bAdapter(strict=True)

    with pytest.raises(TypeError, match="expects RootExtractionResult"):
        adapter.adapt("not a RootExtractionResult")  # type: ignore


# ---------------------------------------------------------------------------
# SyntaxAdapter (Link → SYNTAX)
# ---------------------------------------------------------------------------


def test_syntax_adapter_adapt_link_object():
    """SyntaxAdapter adapts Link objects to syntax.relation_candidate."""
    # Mock Link object (dict-like for simplicity)
    link = {
        "link_type": "ISNADI",
        "source": "الطالب",
        "target": "مجتهد",
    }

    adapter = SyntaxAdapter()
    evidence_tuple = adapter.adapt(link)

    assert len(evidence_tuple) >= 1
    ev = evidence_tuple[0]
    assert ev.kind == "syntax.relation_candidate"
    assert "ISNADI" in ev.detail
    assert "syntax:" in ev.source


def test_syntax_adapter_link_weight_by_type():
    """SyntaxAdapter assigns higher weight to ISNADI than TAQYIDI."""
    adapter = SyntaxAdapter()

    link_isnadi = {"link_type": "ISNADI", "source": "A", "target": "B"}
    link_taqyidi = {"link_type": "TAQYIDI", "source": "A", "target": "B"}

    ev_isnadi = adapter.adapt(link_isnadi)[0]
    ev_taqyidi = adapter.adapt(link_taqyidi)[0]

    assert ev_isnadi.weight > ev_taqyidi.weight


def test_syntax_adapter_returns_empty_for_invalid_link():
    """SyntaxAdapter returns () for links missing required fields."""
    adapter = SyntaxAdapter()

    invalid_link = {"link_type": "ISNADI"}  # Missing source/target
    evidence_tuple = adapter.adapt(invalid_link)

    assert evidence_tuple == ()


# ---------------------------------------------------------------------------
# CPB validation for adapter outputs
# ---------------------------------------------------------------------------


def test_c2b_adapter_evidence_passes_cpb_validation():
    """C2bAdapter Evidence passes CPB validation for MORPH_SURFACE → ROOT."""
    root = Root(letters=("ك", "ت", "ب"), root_type=RootType.TRILATERAL)
    result = RootExtractionResult(
        root=root,
        normalized_word="كاتب",
        stripped_word="كاتب",
        prefix="",
        suffix="",
    )

    adapter = C2bAdapter()
    evidence_tuple = adapter.adapt(result)

    # Build a Result using this Evidence
    from fvafk.algebra import Trace, Result
    result_obj = Result(
        value="كاتب",
        rank=Rank.LICENSED,
        evidence=evidence_tuple,
        trace=Trace(operation="test"),
    )

    # Validate with CPB for MORPH_SURFACE → ROOT
    cpb = CPB(name="test_c2b_bridge", source=Domain.MORPH_SURFACE, target=Domain.ROOT)
    carrier = Carrier(domain=Domain.MORPH_SURFACE, value="كاتب", label="كاتب")

    validated = validate_cpb(cpb, carrier, result_obj)

    # Should pass without fatal failures
    assert validated.rank is not Rank.REFUTED
    assert not any(f.fatal for f in validated.failures)


# ---------------------------------------------------------------------------
# Domain boundary enforcement (no forbidden jumps)
# ---------------------------------------------------------------------------


def test_c2b_adapter_never_emits_semantic_or_hukm_evidence():
    """C2bAdapter never emits semantic.* or hukm.* Evidence kinds."""
    root = Root(letters=("ك", "ت", "ب"), root_type=RootType.TRILATERAL)
    result = RootExtractionResult(
        root=root,
        normalized_word="كاتب",
        stripped_word="كاتب",
        prefix="",
        suffix="",
    )

    adapter = C2bAdapter()
    evidence_tuple = adapter.adapt(result)

    for ev in evidence_tuple:
        assert not ev.kind.startswith("semantic.")
        assert not ev.kind.startswith("hukm.")


def test_syntax_adapter_never_emits_semantic_or_hukm_evidence():
    """SyntaxAdapter never emits semantic.* or hukm.* Evidence kinds."""
    link = {"link_type": "ISNADI", "source": "A", "target": "B"}

    adapter = SyntaxAdapter()
    evidence_tuple = adapter.adapt(link)

    for ev in evidence_tuple:
        assert not ev.kind.startswith("semantic.")
        assert not ev.kind.startswith("hukm.")


def test_adapters_respect_forbidden_bridges():
    """Adapter Evidence cannot be used to violate FORBIDDEN_BRIDGES.

    Specifically: MORPH_SURFACE → SEMANTICS is forbidden.
    """
    from fvafk.algebra.arabic_layers import is_bridge_allowed

    # MORPH_SURFACE → SEMANTICS is forbidden
    assert not is_bridge_allowed(Domain.MORPH_SURFACE, Domain.SEMANTICS)

    # Attempting to build a CPB for this bridge should fail
    with pytest.raises(ValueError, match="forbidden bridge"):
        CPB(
            name="illegal_bridge",
            source=Domain.MORPH_SURFACE,
            target=Domain.SEMANTICS,
        )


# ---------------------------------------------------------------------------
# Phase integration: Adapters work with ArabicAlgebraDecisionTree
# ---------------------------------------------------------------------------


def test_c2b_adapter_evidence_integrates_with_decision_tree():
    """C2bAdapter Evidence can be consumed by ArabicAlgebraDecisionTree.

    This is the Phase-2 acceptance criterion: adapters wire real FVAFK
    output into the algebra layer.
    """
    from fvafk.c2b import RootExtractor
    from fvafk.algebra import ArabicAlgebraDecisionTree

    # Extract root using real RootExtractor
    extractor = RootExtractor()
    extraction_result = extractor.extract_with_affixes("كاتب")

    # Adapt to Evidence
    adapter = C2bAdapter()
    evidence_tuple = adapter.adapt(extraction_result)

    # Verify evidence is non-empty and properly cited
    assert len(evidence_tuple) >= 1
    root_ev = evidence_tuple[0]
    assert root_ev.kind == "root.candidate"
    assert "c2b:" in root_ev.source

    # The decision tree does not consume adapter evidence directly in
    # Phase 2 (it still uses hand-built fixtures), but we verify the
    # Evidence is **compatible** with the tree's Result structure.
    tree = ArabicAlgebraDecisionTree()
    tree_result = tree.analyze("كاتب")

    # Tree result should have same surface
    assert tree_result.value.surface == extraction_result.normalized_word

    # Adapter evidence cites the same root
    if extraction_result.root:
        # Check that root letters appear in detail (format is tuple in detail)
        assert str(extraction_result.root.letters) in root_ev.detail


# ---------------------------------------------------------------------------
# Regression: Phase 0, 0.5, 1 contracts remain intact
# ---------------------------------------------------------------------------


def test_phase_0_rank_set_unchanged():
    """Phase 2 does not add new Rank values."""
    from fvafk.algebra import Rank

    canonical_ranks = {
        Rank.UNRESOLVED,
        Rank.CANDIDATE,
        Rank.LICENSED,
        Rank.CERTIFIED,
        Rank.REFUTED,
    }

    assert set(Rank) == canonical_ranks


def test_phase_0_bridge_matrix_unchanged():
    """Phase 2 does not modify ALLOWED_BRIDGES or FORBIDDEN_BRIDGES."""
    from fvafk.algebra.arabic_layers import ALLOWED_BRIDGES, FORBIDDEN_BRIDGES

    # Phase 0 bridge count
    assert len(ALLOWED_BRIDGES) == 8
    assert len(FORBIDDEN_BRIDGES) >= 6

    # Key forbidden bridges still present
    forbidden_pairs = list(FORBIDDEN_BRIDGES)
    assert (Domain.MORPH_SURFACE, Domain.MORPH_DEEP) in forbidden_pairs
    assert (Domain.MORPH_SURFACE, Domain.SEMANTICS) in forbidden_pairs
    assert (Domain.MORPH_DEEP, Domain.HUKM) in forbidden_pairs


def test_phase_1_surface_cap_still_enforced():
    """Phase 2 preserves Phase-1 surface cap: no CERTIFIED from surface.

    Surface matches still return LICENSED with certificate_allowed=False.
    """
    from fvafk.algebra import ArabicAlgebraDecisionTree

    tree = ArabicAlgebraDecisionTree()
    result = tree.analyze("كاتب")

    assert result.rank is Rank.LICENSED
    assert result.certificate_allowed is False
    assert len(result.residuals) >= 2  # context.absent + lexical.ambiguity
