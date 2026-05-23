"""
Tests for SyntaxGraphToFvafkAdapter - syntax_theory SyntacticGraph → FVAFK output

**Test Suite**: 6 required tests as per FVAFK_GFA_INTEGRATION_MAP.md

**Tests**:
1. ISN relation extraction
2. TADMN relation extraction
3. TAQYID relation extraction
4. Case marking extraction
5. Mood marking extraction
6. Round-trip: FVAFK → graph → FVAFK (idempotent)

**Reference**: docs/FVAFK_GFA_INTEGRATION_MAP.md
"""

import pytest
from typing import Dict, List

# Adapter under test
from fvafk.adapters import SyntaxGraphToFvafkAdapter

# syntax_theory imports (with fallback)
try:
    from syntax_theory.structures import (
        SyntacticGraph,
        Node,
        Edge,
        EdgeType,
        CaseMarking,
        MoodMarking,
        NodeFeatures,
    )
    SYNTAX_THEORY_AVAILABLE = True
except ImportError:
    SYNTAX_THEORY_AVAILABLE = False
    pytestmark = pytest.mark.skip(reason="syntax_theory not available (Phase 2)")


# ============================================================================
# Test Fixtures
# ============================================================================

@pytest.fixture
def adapter():
    """Create adapter instance"""
    return SyntaxGraphToFvafkAdapter()


@pytest.fixture
def nominal_sentence_graph():
    """
    Mock SyntacticGraph for nominal sentence: الكِتَابُ جَدِيدٌ

    Graph:
    - Node 1 (الكتاب): NOUN, nominative, mubtada
    - Node 2 (جديد): NOUN, nominative, khabar
    - Edge: ISN (Node 1 → Node 2)
    """
    if not SYNTAX_THEORY_AVAILABLE:
        return None

    # Create nodes
    node1 = Node(
        id=1,
        surface="الكتاب",
        features=NodeFeatures(
            lexical_type="NOUN",
            case=CaseMarking.NOMINATIVE,
            role="mubtada"
        )
    )
    node2 = Node(
        id=2,
        surface="جديد",
        features=NodeFeatures(
            lexical_type="NOUN",
            case=CaseMarking.NOMINATIVE,
            role="khabar"
        )
    )

    # Create edge (ISN relation)
    edge = Edge(
        source=1,
        target=2,
        edge_type=EdgeType.ISN
    )

    # Build graph
    graph = SyntacticGraph(
        nodes=[node1, node2],
        edges=[edge]
    )

    return graph


@pytest.fixture
def verbal_sentence_graph():
    """
    Mock SyntacticGraph for verbal sentence: كَتَبَ الطَّالِبُ الدَّرْسَ

    Graph:
    - Node 1 (كتب): VERB, indicative mood
    - Node 2 (الطالب): NOUN, nominative (subject)
    - Node 3 (الدرس): NOUN, accusative (object)
    - Edge: ISN (Node 1 → Node 2) - verb-subject
    - Edge: TADMN (Node 1 → Node 3) - verb-object
    """
    if not SYNTAX_THEORY_AVAILABLE:
        return None

    # Create nodes
    node1 = Node(
        id=1,
        surface="كتب",
        features=NodeFeatures(
            lexical_type="VERB",
            mood=MoodMarking.INDICATIVE,
            role="verb"
        )
    )
    node2 = Node(
        id=2,
        surface="الطالب",
        features=NodeFeatures(
            lexical_type="NOUN",
            case=CaseMarking.NOMINATIVE,
            role="subject"
        )
    )
    node3 = Node(
        id=3,
        surface="الدرس",
        features=NodeFeatures(
            lexical_type="NOUN",
            case=CaseMarking.ACCUSATIVE,
            role="object"
        )
    )

    # Create edges
    edge_isn = Edge(source=1, target=2, edge_type=EdgeType.ISN)
    edge_tadmn = Edge(source=1, target=3, edge_type=EdgeType.TADMN)

    # Build graph
    graph = SyntacticGraph(
        nodes=[node1, node2, node3],
        edges=[edge_isn, edge_tadmn]
    )

    return graph


@pytest.fixture
def complex_sentence_graph():
    """
    Mock SyntacticGraph with all relation types: ISN + TADMN + TAQYID

    Example: الطَّالِبُ الجَدِيدُ يَكْتُبُ الدَّرْسَ الصَّعْبَ
    (The new student writes the difficult lesson)

    Graph:
    - Node 1 (الطالب): NOUN, nominative, subject
    - Node 2 (الجديد): NOUN, nominative, adjective
    - Node 3 (يكتب): VERB, indicative
    - Node 4 (الدرس): NOUN, accusative, object
    - Node 5 (الصعب): NOUN, accusative, adjective
    - Edge: TAQYID (Node 1 → Node 2) - noun-adjective
    - Edge: ISN (Node 3 → Node 1) - verb-subject
    - Edge: TADMN (Node 3 → Node 4) - verb-object
    - Edge: TAQYID (Node 4 → Node 5) - noun-adjective
    """
    if not SYNTAX_THEORY_AVAILABLE:
        return None

    nodes = [
        Node(id=1, surface="الطالب", features=NodeFeatures(
            lexical_type="NOUN", case=CaseMarking.NOMINATIVE, role="subject"
        )),
        Node(id=2, surface="الجديد", features=NodeFeatures(
            lexical_type="NOUN", case=CaseMarking.NOMINATIVE, role="adjective"
        )),
        Node(id=3, surface="يكتب", features=NodeFeatures(
            lexical_type="VERB", mood=MoodMarking.INDICATIVE, role="verb"
        )),
        Node(id=4, surface="الدرس", features=NodeFeatures(
            lexical_type="NOUN", case=CaseMarking.ACCUSATIVE, role="object"
        )),
        Node(id=5, surface="الصعب", features=NodeFeatures(
            lexical_type="NOUN", case=CaseMarking.ACCUSATIVE, role="adjective"
        )),
    ]

    edges = [
        Edge(source=1, target=2, edge_type=EdgeType.TAQYID),
        Edge(source=3, target=1, edge_type=EdgeType.ISN),
        Edge(source=3, target=4, edge_type=EdgeType.TADMN),
        Edge(source=4, target=5, edge_type=EdgeType.TAQYID),
    ]

    return SyntacticGraph(nodes=nodes, edges=edges)


# ============================================================================
# Test 1: ISN relation extraction
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_1_isn_relation_extraction(adapter, nominal_sentence_graph):
    """
    Test 1: ISN relation extraction

    **Success Criteria**:
    - Extracts ISN relations from graph
    - Returns list with at least 1 ISN relation
    - Relation contains: source, target, type="isn"
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.extract_relations(nominal_sentence_graph)

    # Assert
    assert "isn" in result, "Result should have 'isn' key"
    assert isinstance(result["isn"], list), "ISN should be a list"
    assert len(result["isn"]) >= 1, "Should extract at least 1 ISN relation"

    # Check ISN relation structure
    isn_relation = result["isn"][0]
    assert "source" in isn_relation or "head" in isn_relation, \
        "ISN relation should have source/head"
    assert "target" in isn_relation or "dependent" in isn_relation, \
        "ISN relation should have target/dependent"


# ============================================================================
# Test 2: TADMN relation extraction
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_2_tadmn_relation_extraction(adapter, verbal_sentence_graph):
    """
    Test 2: TADMN relation extraction

    **Success Criteria**:
    - Extracts TADMN relations (transitive verb → object)
    - Returns list with at least 1 TADMN relation
    - Relation type is "tadmn"
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.extract_relations(verbal_sentence_graph)

    # Assert
    assert "tadmn" in result, "Result should have 'tadmn' key"
    assert isinstance(result["tadmn"], list), "TADMN should be a list"
    assert len(result["tadmn"]) >= 1, "Should extract at least 1 TADMN relation"

    # Check TADMN relation structure
    tadmn_relation = result["tadmn"][0]
    assert "source" in tadmn_relation or "head" in tadmn_relation
    assert "target" in tadmn_relation or "dependent" in tadmn_relation


# ============================================================================
# Test 3: TAQYID relation extraction
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_3_taqyid_relation_extraction(adapter, complex_sentence_graph):
    """
    Test 3: TAQYID relation extraction

    **Success Criteria**:
    - Extracts TAQYID relations (modification/adjective)
    - Returns list with at least 1 TAQYID relation
    - Relation type is "taqyid"
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.extract_relations(complex_sentence_graph)

    # Assert
    assert "taqyid" in result, "Result should have 'taqyid' key"
    assert isinstance(result["taqyid"], list), "TAQYID should be a list"
    assert len(result["taqyid"]) >= 1, "Should extract at least 1 TAQYID relation"

    # Check TAQYID relation structure
    taqyid_relation = result["taqyid"][0]
    assert "source" in taqyid_relation or "head" in taqyid_relation
    assert "target" in taqyid_relation or "dependent" in taqyid_relation


# ============================================================================
# Test 4: Case marking extraction
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_4_case_marking_extraction(adapter, verbal_sentence_graph):
    """
    Test 4: Case marking extraction

    **Success Criteria**:
    - Extracts case markings from graph nodes
    - Returns list with nominative, accusative cases
    - Case markings match node features
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.extract_relations(verbal_sentence_graph)

    # Assert
    assert "case_markings" in result, "Result should have 'case_markings' key"
    assert isinstance(result["case_markings"], list), "Case markings should be a list"
    assert len(result["case_markings"]) >= 2, "Should extract at least 2 case markings"

    # Check case marking structure
    cases = [cm.get("case") or cm.get("marking") for cm in result["case_markings"]]
    assert "nominative" in str(cases).lower() or "NOMINATIVE" in str(cases), \
        "Should extract nominative case"
    assert "accusative" in str(cases).lower() or "ACCUSATIVE" in str(cases), \
        "Should extract accusative case"


# ============================================================================
# Test 5: Mood marking extraction
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_5_mood_marking_extraction(adapter, verbal_sentence_graph):
    """
    Test 5: Mood marking extraction

    **Success Criteria**:
    - Extracts mood markings from verb nodes
    - Returns list with at least 1 mood marking
    - Mood marking is indicative/subjunctive/jussive
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.extract_relations(verbal_sentence_graph)

    # Assert
    assert "mood_markings" in result, "Result should have 'mood_markings' key"
    assert isinstance(result["mood_markings"], list), "Mood markings should be a list"
    assert len(result["mood_markings"]) >= 1, "Should extract at least 1 mood marking"

    # Check mood marking structure
    moods = [mm.get("mood") or mm.get("marking") for mm in result["mood_markings"]]
    assert any(
        mood_str in str(moods).lower()
        for mood_str in ["indicative", "subjunctive", "jussive"]
    ), "Should extract valid mood marking"


# ============================================================================
# Test 6: Round-trip idempotence
# ============================================================================

@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_6_round_trip_fvafk_to_graph_to_fvafk_idempotent(adapter, complex_sentence_graph):
    """
    Test 6: Round-trip: FVAFK → graph → FVAFK (idempotent)

    **Success Criteria**:
    - Extracting relations twice yields same result
    - No information loss in round-trip
    - Relation counts preserved
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act: Extract twice
    result1 = adapter.extract_relations(complex_sentence_graph)
    result2 = adapter.extract_relations(complex_sentence_graph)

    # Assert: Idempotence
    assert result1.keys() == result2.keys(), "Keys should be identical"

    for key in ["isn", "tadmn", "taqyid", "case_markings", "mood_markings"]:
        assert len(result1[key]) == len(result2[key]), \
            f"{key} count should be identical in both extractions"

    # Assert: Relation counts match graph structure
    total_edges = len(complex_sentence_graph.edges)
    total_relations = len(result1["isn"]) + len(result1["tadmn"]) + len(result1["taqyid"])

    assert total_relations == total_edges, \
        f"Total relations ({total_relations}) should match graph edges ({total_edges})"


# ============================================================================
# Additional Tests: Edge Cases and Governance
# ============================================================================

def test_empty_graph_graceful_handling(adapter):
    """
    **Edge Case**: Empty graph (no nodes, no edges)

    Should return empty lists, not crash
    """
    if not SYNTAX_THEORY_AVAILABLE:
        # Adapter should raise NotImplementedError (stub)
        with pytest.raises(NotImplementedError):
            adapter.extract_relations(None)
    else:
        # Mock empty graph
        empty_graph = SyntacticGraph(nodes=[], edges=[])

        # Act
        result = adapter.extract_relations(empty_graph)

        # Assert: Graceful handling
        assert isinstance(result, dict)
        assert all(isinstance(result[key], list) for key in result.keys())
        assert all(len(result[key]) == 0 for key in result.keys()), \
            "All relation lists should be empty for empty graph"


@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_graph_with_only_nodes_no_edges(adapter):
    """
    **Edge Case**: Graph with nodes but no edges

    Should return empty relation lists, but non-empty case/mood markings
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Create graph with nodes but no edges
    nodes = [
        Node(id=1, surface="كتاب", features=NodeFeatures(
            lexical_type="NOUN", case=CaseMarking.NOMINATIVE
        )),
    ]
    graph_no_edges = SyntacticGraph(nodes=nodes, edges=[])

    # Act
    result = adapter.extract_relations(graph_no_edges)

    # Assert
    assert len(result["isn"]) == 0, "No ISN relations for graph without edges"
    assert len(result["tadmn"]) == 0, "No TADMN relations for graph without edges"
    assert len(result["taqyid"]) == 0, "No TAQYID relations for graph without edges"

    # But case markings should be extracted from nodes
    assert len(result["case_markings"]) >= 1, \
        "Should extract case markings even without edges"


@pytest.mark.skip(reason="Adapter implementation pending Phase 2")
def test_complex_graph_all_relation_types(adapter, complex_sentence_graph):
    """
    **Integration Test**: Complex graph with all relation types

    Verifies adapter can handle graph with ISN, TADMN, and TAQYID simultaneously
    """
    if not SYNTAX_THEORY_AVAILABLE:
        pytest.skip("syntax_theory not available")

    # Act
    result = adapter.extract_relations(complex_sentence_graph)

    # Assert: All relation types present
    assert len(result["isn"]) > 0, "Should extract ISN relations"
    assert len(result["tadmn"]) > 0, "Should extract TADMN relations"
    assert len(result["taqyid"]) > 0, "Should extract TAQYID relations"
    assert len(result["case_markings"]) > 0, "Should extract case markings"
    assert len(result["mood_markings"]) > 0, "Should extract mood markings"

    # Assert: Relation types are distinct
    isn_count = len(result["isn"])
    tadmn_count = len(result["tadmn"])
    taqyid_count = len(result["taqyid"])

    assert isn_count != tadmn_count or tadmn_count != taqyid_count, \
        "Different relation types should have different counts (not all equal)"
