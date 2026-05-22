"""
Semantic Learning Spine: Lexicon as Witness, Not Arbiter

Central Rule:
    المعجم يرخّص المطابقة، ولا يبني وحده شبكة الدلالة.
    The lexicon licenses mutābaqah but does not build the semantic network alone.

Core Principle:
    التعلم الذاتي الدلالي يبدأ عند اقتران الدال بالمدلول.
    Self-learning semantic network begins when signifier binds to signified.

    This binding is not in the signifier layer alone,
    nor in the signified layer alone,
    but in a third layer: binding signifier to signified.

Correct Division:
    1. Signifier alone (دال وحده)
       = Form / Trace / Carrier
       Does not produce meaning alone.

    2. Signified alone (مدلول وحده)
       = Candidate concept
       Does not produce dalālah alone.

    3. Signifier + Signified together (دال + مدلول معاً)
       = Beginning of dalālah
       Here begins algebraic semantic learning.

Lexicon API Agent Role:
    NOT: Final meaning arbiter
    NOT: Complete dalālah builder
    IS: Evidence provider for mutābaqah

    Returns: term → primary_sense
    With: source, edition, entry, sense_id, confidence

    Critical Distinction:
        Dictionary entry ≠ Ifādah
        Dictionary entry ≠ HUKM
        Dictionary entry = source-backed mutābaqah evidence

Self-Learning Does NOT Come From Lexicon Alone:
    Lexicon provides base:
        Source-backed mutābaqah

    Then algebra builds network:
        Mutābaqah from source
        → Taḍammun from licensed madlūl decomposition
        → Iltizām from licensed entailment network
        → Majāz/Naql from licensed transfer network
        → Nisbah
        → Ifādah
        → HUKM guard

    Formula:
        Source-backed Mutābaqah
        → Decomposition-backed Taḍammun
        → Entailment-network-backed Iltizām
        → Transfer-network-backed Majāz

Core Guard:
    Every semantic edge learned by the system must carry:
        - Relation type (نوع العلاقة)
        - Evidence (الدليل)
        - Gate (البوابة)
        - Rank (الرتبة)
        - Residuals (البقايا)
        - Trace (الأثر)
        - Replay (إعادة التشغيل)

    It must NOT learn like this:
        term → meaning

    It MUST learn like this:
        signifier + signified + binding_type + source/gate + rank + residuals

This is the backbone of the project:
    **Lexicon is witness to mutābaqah,
      Self-learning is building a signifier/signified network governed by algebra.**
"""

from __future__ import annotations

from fvafk.algebra import (
    Carrier,
    Domain,
    Evidence,
    Rank,
)
from fvafk.algebra.semantics import (
    DalCandidateOperation,
    MadlulCandidateOperation,
    WadhBindingOperation,
    MutabaqahGate,
    TadammunGate,
    IltizamGate,
    NisbahSemanticOperation,
)


# =============================================================================
# Test 1: Mutābaqah is Source-Backed, Not Algebraically Invented
# =============================================================================

def test_mutabaqah_is_source_backed_not_algebraically_invented():
    """
    Mutābaqah requires source-backed evidence (lexicon, usage, context).
    It cannot be algebraically invented without external evidence.

    Law: المطابقة من الوضع أو المصدر، لا من الجبر وحده
         (Mutābaqah from wadh'/source, not from algebra alone)

    Without evidence → CANDIDATE (not LICENSED)
    With lexicon/source evidence → LICENSED
    """
    gate = MutabaqahGate()

    # Part 1: Without evidence → CANDIDATE (unsupported claim)
    result_no_evidence = gate.run(binding="كتاب→written_object", evidence=())

    assert result_no_evidence.rank is Rank.CANDIDATE, \
        "Mutābaqah without source evidence must be CANDIDATE"

    # Part 2: With lexicon evidence → LICENSED (source-backed)
    lexicon_ev = (
        Evidence(
            kind="lexicon.entry",
            source="Lane's Lexicon:1850:entry_ktb",
            detail="primary_sense:written_object",
            weight=0.9
        ),
    )
    result_with_source = gate.run(binding="كتاب→written_object", evidence=lexicon_ev)

    assert result_with_source.rank is Rank.LICENSED, \
        "Mutābaqah with source evidence must be LICENSED"
    assert result_with_source.evidence, \
        "Mutābaqah must carry evidence trace"
    assert any(e.kind == "lexicon.entry" for e in result_with_source.evidence), \
        "Mutābaqah evidence must reference source (lexicon/usage/context)"

    # Part 3: Mutābaqah is pre-ifādah condition (never CERTIFIED alone)
    assert result_with_source.residuals, \
        "Mutābaqah always has insufficiency residual (pre-ifādah)"
    assert any(r.kind == "semantics.mutabaqah.insufficient" for r in result_with_source.residuals), \
        "Mutābaqah insufficient for ifādah alone"


# =============================================================================
# Test 2: Taḍammun Requires Decomposition of Licensed Madlūl
# =============================================================================

def test_tadammun_requires_decomposition_of_licensed_madlul():
    """
    Taḍammun (partial inclusion) requires decomposition analysis of madlūl.
    It cannot come from lexicon alone; it comes from analyzing the licensed madlūl.

    Law: التضمن من تحليل المدلول المرخص، لا من المعجم وحده
         (Taḍammun from licensed madlūl decomposition, not from lexicon alone)

    Flow:
        1. Lexicon provides: بيت → house (mutābaqah)
        2. Decomposition analyzes: house ⊃ {roof, walls, door, ...}
        3. Taḍammun: سقف (roof) is part of بيت (house)

    NOT: Lexicon says "سقف is part of بيت"
    BUT: Decomposition discovers "roof" ∈ components_of("house")
    """
    gate = TadammunGate()

    # Part 1: Without evidence → CANDIDATE
    result_no_evidence = gate.run(
        binding="سقف→roof",
        part="roof",
        evidence=()
    )

    assert result_no_evidence.rank is Rank.CANDIDATE, \
        "Taḍammun without decomposition evidence must be CANDIDATE"

    # Part 2: With decomposition evidence → LICENSED
    # Evidence shows: "roof" is component of "house" via licensed decomposition
    decomposition_ev = (
        Evidence(
            kind="decomposition.part_of",
            source="madlul_analysis:house→components",
            detail="roof:structural_component",
            weight=1.0
        ),
    )
    result_with_decomposition = gate.run(
        binding="سقف→roof",
        part="roof",
        evidence=decomposition_ev
    )

    assert result_with_decomposition.rank is Rank.LICENSED, \
        "Taḍammun with decomposition evidence must be LICENSED"
    assert result_with_decomposition.evidence, \
        "Taḍammun must carry decomposition evidence"
    assert any(e.kind == "decomposition.part_of" for e in result_with_decomposition.evidence), \
        "Taḍammun evidence must come from madlūl decomposition, not lexicon"

    # Part 3: Taḍammun is pre-ifādah condition (never CERTIFIED alone)
    assert result_with_decomposition.residuals, \
        "Taḍammun always has insufficiency residual (pre-ifādah)"
    assert any(r.kind == "semantics.tadammun.insufficient" for r in result_with_decomposition.residuals), \
        "Taḍammun insufficient for ifādah alone"


# =============================================================================
# Test 3: Iltizām Requires Entailment Network Gate and Evidence
# =============================================================================

def test_iltizam_requires_entailment_network_gate_and_evidence():
    """
    Iltizām (entailment) is NOT automatic.
    It requires explicit gate (logical, conventional, shariah, contextual).

    Law: الالتزام من شبكة اللزوم المرخصة، لا تلقائياً ولا من المعجم وحده
         (Iltizām from licensed entailment network, not automatically nor from lexicon alone)

    Gate Types:
        - logical: p → q (deductive entailment)
        - conventional: usage-based association
        - shariah: religious legal entailment
        - contextual: discourse-based inference

    Flow:
        1. Mutābaqah: طلوع الشمس → sunrise
        2. Iltizām gate: sunrise →[logical_causality] day
        3. Consequence: نهار (day)

    NOT: Lexicon says "sunrise entails day"
    BUT: Logical gate licenses causal entailment
    """
    gate = IltizamGate()

    # Part 1: Without gate_type → CANDIDATE (not licensed)
    result_no_gate = gate.run(
        binding="طلوع:الشمس→sunrise",
        consequence="day",
        gate_type="",  # No gate
        evidence=()
    )

    assert result_no_gate.rank is Rank.CANDIDATE, \
        "Iltizām without gate must be CANDIDATE"
    assert result_no_gate.residuals, \
        "Iltizām without gate must have residual"
    assert any(r.kind == "semantics.iltizam.gate_missing" for r in result_no_gate.residuals), \
        "Iltizām residual must indicate missing gate"

    # Part 2: With gate_type but no evidence → CANDIDATE
    result_gate_no_evidence = gate.run(
        binding="طلوع:الشمس→sunrise",
        consequence="day",
        gate_type="logical",
        evidence=()
    )

    assert result_gate_no_evidence.rank is Rank.CANDIDATE, \
        "Iltizām with gate but no evidence must be CANDIDATE"

    # Part 3: With gate_type AND evidence → LICENSED
    entailment_ev = (
        Evidence(
            kind="entailment.logical",
            source="causality_gate:sunrise→day",
            detail="physical_causation",
            weight=1.0
        ),
    )
    result_with_gate_and_evidence = gate.run(
        binding="طلوع:الشمس→sunrise",
        consequence="day",
        gate_type="logical",
        evidence=entailment_ev
    )

    assert result_with_gate_and_evidence.rank is Rank.LICENSED, \
        "Iltizām with gate and evidence must be LICENSED"
    assert result_with_gate_and_evidence.evidence, \
        "Iltizām must carry entailment gate evidence"
    assert any(e.kind == "entailment.logical" for e in result_with_gate_and_evidence.evidence), \
        "Iltizām evidence must reference explicit gate"
    assert not result_with_gate_and_evidence.residuals, \
        "Iltizām with complete gate has no residuals"

    # Part 4: Iltizām is pre-ifādah condition (not CERTIFIED alone)
    assert result_with_gate_and_evidence.rank is not Rank.CERTIFIED, \
        "Iltizām alone cannot be CERTIFIED (requires full ifādah)"


# =============================================================================
# Test 4: Majāz/Naql Are Transfer Network, Not Lexicon Alone
# =============================================================================

def test_majaz_and_naql_are_transfer_network_not_lexicon_alone():
    """
    Majāz (metaphor) and Naql (semantic transfer) require:
        1. Licensed literal meaning (mutābaqah)
        2. Transfer gate (resemblance, adjacency, causality, etc.)
        3. Transferred meaning
        4. Transfer evidence

    Law: المجاز والنقل من شبكة النقل المرخصة، لا من المعجم وحده
         (Majāz/Naql from licensed transfer network, not from lexicon alone)

    Flow:
        1. Mutābaqah: أسد → lion (literal)
        2. Transfer gate: resemblance (شبه)
        3. Majāz: أسد → brave_man (metaphor)

    NOT: Lexicon says "أسد means both lion and brave man"
    BUT: Transfer gate licenses metaphorical extension via resemblance

    Note: This test establishes the requirement even though MajazGate
          may not be fully implemented yet. The test documents the contract.
    """
    # For now, we test the principle using WadhBindingOperation
    # Future: Create dedicated MajazGate/NaqlOperation

    wadh_op = WadhBindingOperation()

    # Part 1: Literal meaning (mutābaqah) - lexicon-backed
    lexicon_ev = (
        Evidence(
            kind="lexicon.entry",
            source="lexicon:asd→lion",
            detail="literal_meaning",
            weight=1.0
        ),
    )
    literal_result = wadh_op.run(
        dal="أسد",
        madlul="lion",
        evidence=lexicon_ev
    )

    assert literal_result.rank is Rank.LICENSED, \
        "Literal meaning from lexicon must be LICENSED"

    # Part 2: Metaphorical meaning (majāz) - requires transfer gate
    # WITHOUT transfer gate evidence → CANDIDATE (not licensed)
    metaphor_no_gate = wadh_op.run(
        dal="أسد",
        madlul="brave_man",
        evidence=()  # No transfer gate
    )

    assert metaphor_no_gate.rank is Rank.CANDIDATE, \
        "Metaphor without transfer gate must be CANDIDATE"
    assert metaphor_no_gate.residuals, \
        "Metaphor without gate must have residual"

    # Part 3: Metaphorical meaning WITH transfer gate → LICENSED
    transfer_ev = (
        Evidence(
            kind="transfer.resemblance",
            source="transfer_gate:lion→brave_man",
            detail="resemblance:courage+strength",
            weight=0.8
        ),
    )
    metaphor_with_gate = wadh_op.run(
        dal="أسد",
        madlul="brave_man",
        evidence=transfer_ev
    )

    assert metaphor_with_gate.rank is Rank.LICENSED, \
        "Metaphor with transfer gate must be LICENSED"
    assert metaphor_with_gate.evidence, \
        "Metaphor must carry transfer evidence"
    assert any(e.kind == "transfer.resemblance" for e in metaphor_with_gate.evidence), \
        "Majāz evidence must reference transfer gate (resemblance/adjacency/causality)"


# =============================================================================
# Test 5: Nisbah Still Required After Three Dalālah Gates
# =============================================================================

def test_nisbah_still_required_after_three_dalalah_gates():
    """
    The three dalālah gates (mutābaqah, taḍammun, iltizām) are PRE-IFĀDAH conditions.
    They do NOT replace nisbah (predication/relation).

    Law: الدلالة الثلاثية (مطابقة، تضمن، التزام) شرط للإفادة، لا تكفي وحدها
         (Three dalālah types are conditions for ifādah, not sufficient alone)

    Even with licensed mutābaqah/taḍammun/iltizām, you still need:
        - Nisbah (ISN/TADMN/TAQYID)
        - Parties
        - Structure
        - References resolved
        - Speech force determined

    Flow:
        1. Mutābaqah: الطالب → student, مجتهد → diligent (source-backed)
        2. Nisbah: ISN (predication) between student and diligent
        3. Ifādah: "The student is diligent" (complete meaning)

    Mutābaqah alone does NOT produce ifādah.
    Nisbah is still required.
    """
    # Step 1: Licensed mutābaqah for two terms
    mutabaqah_gate = MutabaqahGate()

    lex_ev_1 = (Evidence(kind="lexicon.entry", source="lex:student", detail="الطالب"),)
    mutabaqah_1 = mutabaqah_gate.run(binding="الطالب→student", evidence=lex_ev_1)

    lex_ev_2 = (Evidence(kind="lexicon.entry", source="lex:diligent", detail="مجتهد"),)
    mutabaqah_2 = mutabaqah_gate.run(binding="مجتهد→diligent", evidence=lex_ev_2)

    assert mutabaqah_1.rank is Rank.LICENSED
    assert mutabaqah_2.rank is Rank.LICENSED

    # Step 2: Mutābaqah alone has insufficiency residual
    assert mutabaqah_1.residuals, \
        "Mutābaqah alone is insufficient for ifādah"
    assert mutabaqah_2.residuals, \
        "Mutābaqah alone is insufficient for ifādah"

    # Step 3: Nisbah (ISN predication) is still required
    nisbah_op = NisbahSemanticOperation()

    nisbah_ev = (Evidence(kind="syntax.isn", source="predication:student→diligent", detail="ISN"),)
    nisbah_result = nisbah_op.run(
        nisbah_type="ISN",
        parties="student:diligent",
        evidence=nisbah_ev
    )

    assert nisbah_result.rank is Rank.LICENSED, \
        "Nisbah with evidence must be LICENSED"
    assert not nisbah_result.residuals, \
        "ISN nisbah with evidence has no inherent residual (may lead to ifādah)"

    # Step 4: Principle verification
    # Mutābaqah ≠ Ifādah
    # Mutābaqah + Nisbah → potential Ifādah (with all other requirements)
    assert mutabaqah_1.residuals, \
        "Mutābaqah is NOT ifādah (residual proves insufficiency)"
    assert not nisbah_result.residuals, \
        "ISN nisbah can contribute to ifādah (no inherent insufficiency)"

    # The three dalālah gates are conditions, not replacements for nisbah
    # This test proves: Mutābaqah + Taḍammun + Iltizām are pre-ifādah
    # They do NOT eliminate the need for compositional semantics (nisbah)


# =============================================================================
# Mutation Resistance: Semantic Learning Spine Invariants
# =============================================================================

def test_semantic_edge_must_carry_full_provenance():
    """
    Every semantic edge in the learning network must carry:
        1. Relation type (نوع العلاقة)
        2. Evidence (الدليل)
        3. Gate (البوابة) - implicit in operation
        4. Rank (الرتبة)
        5. Residuals (البقايا)
        6. Trace (الأثر)
        7. Replay capability (إعادة التشغيل)

    No bare assertions allowed.
    """
    gate = MutabaqahGate()
    ev = (Evidence(kind="lexicon.entry", source="test", detail="test"),)
    result = gate.run(binding="test→test", evidence=ev)

    # All 7 components present
    assert result.value, "1. Relation/value present"
    assert result.evidence, "2. Evidence present"
    # Gate is implicit in MutabaqahGate
    assert result.rank, "4. Rank present"
    assert isinstance(result.residuals, tuple), "5. Residuals present (may be empty)"
    assert result.trace, "6. Trace present"
    # Replay tested separately

    # Principle: No bare output (لا مخرج عارٍ)
    assert result.rank is not Rank.UNRESOLVED or not result.evidence, \
        "Result with evidence cannot be UNRESOLVED (no bare assertions)"


def test_lexicon_provides_evidence_not_final_rank():
    """
    Lexicon provides Evidence, not Result with high rank.

    Law: المعجم شاهد، لا حاكم
         (Lexicon is witness, not judge)

    The lexicon/API returns evidence for mutābaqah.
    The algebra (gates) promote rank based on evidence.

    Lexicon does NOT directly issue LICENSED/CERTIFIED results.
    """
    # Simulate lexicon response: Evidence only
    lexicon_evidence = Evidence(
        kind="lexicon.entry",
        source="Lane:1850:ktb",
        detail="primary_sense:book",
        weight=0.95
    )

    # Lexicon provides evidence, algebra applies it
    gate = MutabaqahGate()
    result = gate.run(binding="كتاب→book", evidence=(lexicon_evidence,))

    # Evidence came from lexicon
    assert result.evidence
    assert any(e.source.startswith("Lane") for e in result.evidence)

    # But rank decision came from gate (algebra)
    assert result.rank is Rank.LICENSED, \
        "Gate (not lexicon) promotes rank based on evidence"

    # Principle: Lexicon provides evidence → Gate evaluates → Rank assigned
    # NOT: Lexicon directly assigns rank
