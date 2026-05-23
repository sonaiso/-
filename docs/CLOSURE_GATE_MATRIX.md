# مصفوفة بوابات الإغلاق (Closure Gate Matrix)

## Executable Implementation Matrix

**Status**: Implementation Specification
**Version**: 1.0
**Date**: 2026-05-23
**Parent Document**: [GOVERNED_CLOSURE_APPENDIX.md](./GOVERNED_CLOSURE_APPENDIX.md)

---

## Overview

This document provides an **executable implementation matrix** for all closure gates required by the Governed Closure Appendix.

Each gate follows the **canonical pattern** established by existing gates:
- WadhGate (PR-L5B) ✓
- MutabaqahGate (PR-L6A) ✓
- NeutralBinding (PR-N1) ✓
- Memory Geometry (PR-G1) ✓

---

## Gate Template Structure

```python
@dataclass(frozen=True)
class <Gate>Result:
    """Result of <Gate> admission/blocking."""
    status: GateStatus  # ADMITTED | BLOCKED
    candidate: Optional[<Candidate>Type]
    trace: Trace
    residuals: List[Residual]
    rank: PredicateRank
    failure: Optional[<Gate>Failure] = None

@dataclass(frozen=True)
class <Gate>Failure:
    """Governed failure for <Gate>."""
    kind: <Gate>FailureKind
    message: str
    blocker_residuals: List[Residual]
    evidence_gap: Optional[EvidenceGap] = None

class <Gate>:
    """
    <Gate> - <Arabic Name>

    Critical Law:
        <Primary governing principle>

    Forbidden Leap:
        <Input> → <Premature Output>

    What This Gate Does:
        - Admits or blocks <Candidate>
        - Validates <Evidence>
        - Preserves trace
        - Accumulates residuals
        - Returns governed failures

    What This Gate Does NOT Do:
        - Does NOT create <Forbidden Outputs>
        - Does NOT raise rank prematurely
        - Does NOT skip intermediate layers
    """

    def admit_<operation>(
        self,
        input: <InputType>,
        evidence: List[Evidence]
    ) -> <Gate>Result:
        """
        Admit or block <operation> based on evidence, trace, rank, residuals.

        Returns governed failure if conditions not met.
        """
        pass
```

---

## A. Reality & Trace Closure Gates

### A.1 RealityTypeGate

**File**: `src/gfa/foundations/reality/reality_type_gate.py`

```python
gate_id: "A1_REALITY_TYPE"
layer: "Reality & Trace"
forbidden_leap: "Name → Reality (without type determination)"
input_type: "RawName | RawConcept"
output_type: "RealityCandidate"

required_evidence:
  - existence_type_evidence: ExistenceTypeEvidence
  - domain_evidence: DomainEvidence
  - trace_evidence: Optional[TraceEvidence]

rank_policy:
  - ZANNI if existence_type inferred
  - CERTIFIED only if existence_type has attestation
  - UNKNOWN if type cannot be determined

residual_vector:
  - ambiguous_type: bool
  - domain_uncertain: bool
  - trace_incomplete: bool
  - external_verification_needed: bool

golden_cases:
  - "الماء" → EXTERNAL (water - external existence) ✓
  - "العقل" → MENTAL (mind - mental existence) requires domain
  - "العدالة" → NORMATIVE (justice - normative existence) requires domain
  - "أثر قدم" → EFFECTUAL (footprint - effectual existence) ✓

tests_required:
  - test_external_reality_admitted
  - test_mental_reality_requires_domain
  - test_normative_reality_requires_domain
  - test_ambiguous_reality_residualized
  - test_no_type_determination_blocks

dashboard_metric:
  - reality_type_coverage: float
  - ambiguous_reality_ratio: float
```

---

### A.2 NameRealityGate

**File**: `src/gfa/foundations/reality/name_reality_gate.py`

```python
gate_id: "A2_NAME_REALITY"
layer: "Reality & Trace"
forbidden_leap: "Name → Reality (without referent candidate)"
input_type: "str"  # name
output_type: "NamedRealityCandidate"

required_evidence:
  - referent_candidate: Any
  - referent_evidence: List[Evidence]
  - domain: str
  - ambiguity_assessment: Optional[AmbiguityScore]

rank_policy:
  - CANDIDATE if referent proposed but not verified
  - ZANNI if referent has indirect evidence
  - CERTIFIED only if referent has direct evidence in domain
  - BLOCKED if name has no referent candidate

residual_vector:
  - referent_ambiguity: float  # [0.0, 1.0]
  - domain_uncertainty: bool
  - multiple_referent_candidates: bool
  - technical_term_uncertainty: bool
  - metaphorical_uncertainty: bool

golden_cases:
  - "الماء" → physical referent, low ambiguity ✓
  - "العقل" → multiple referent candidates (faculty/reason/intellect), high ambiguity
  - "المجتمع" → abstract referent, requires domain specification
  - "الدولة" → institutional referent, requires historical/legal domain
  - "الحرية" → normative referent, requires philosophical/legal domain

tests_required:
  - test_physical_name_low_ambiguity
  - test_abstract_name_requires_domain
  - test_multiple_referents_residualized
  - test_no_referent_blocks
  - test_metaphorical_name_residualized
  - test_technical_name_requires_domain

dashboard_metric:
  - name_reality_leap_prevention: float
  - ambiguous_name_ratio: float
  - domain_specification_coverage: float
```

**Critical Law**:
```text
لا اسم يُعامل كواقع حتى يُثبت مسماه ومجاله
No name treated as reality until its referent and domain are established.
```

---

### A.3 TraceEffectGate

**File**: `src/gfa/foundations/reality/trace_effect_gate.py`

```python
gate_id: "A3_TRACE_EFFECT"
layer: "Reality & Trace"
forbidden_leap: "Trace → Certainty (without source and preservation assessment)"
input_type: "TraceObservation"
output_type: "TraceEffectCandidate"

required_evidence:
  - effect_type: TraceEffectType
  - source: str
  - transmission_chain: Optional[List[TransmissionLink]]
  - preservation_assessment: PreservationAssessment
  - distortion_assessment: DistortionAssessment

rank_policy:
  - CANDIDATE if trace observed but source unknown
  - ZANNI if source known but transmission uncertain
  - ZANNI if preservation_level < 0.8
  - ZANNI if distortion_risk > 0.3
  - CERTIFIED only if source direct + preservation high + distortion low
  - Never raises to YAQIN (certainty) - trace ≠ reality

residual_vector:
  - source_uncertainty: bool
  - transmission_gaps: int
  - preservation_degradation: float
  - distortion_risk: float
  - interpretation_ambiguity: bool

golden_cases:
  - Quranic text → TEXTUAL, high preservation, low distortion ✓
  - Historical report → TESTIMONIAL, transmission chain required
  - Archaeological artifact → MATERIAL, preservation assessment required
  - Behavioral pattern → BEHAVIORAL, statistical evidence required
  - Smoke → SENSORY, requires source inference (fire)

tests_required:
  - test_textual_trace_high_preservation
  - test_testimonial_trace_requires_chain
  - test_material_trace_preservation_assessment
  - test_sensory_trace_source_inference
  - test_unknown_source_blocks
  - test_high_distortion_risk_residualized
  - test_trace_never_becomes_certainty

dashboard_metric:
  - trace_to_certainty_leap_prevention: float
  - preservation_assessment_coverage: float
  - transmission_chain_documentation: float
```

**Critical Law**:
```text
الأثر لا يساوي الواقع
الأثر يرشح واقعًا برتبة وبقايا

Trace ≠ Reality
Trace nominates reality with rank and residuals.
```

---

## B. Signifier & Utterance Closure Gates

### B.1 PureDalGate

**File**: `src/gfa/methods/lafzi_dal/pure_dal_gate.py`

**Status**: ✓ Already implemented (PR-L3)

```python
gate_id: "B1_PURE_DAL"
layer: "Signifier & Utterance"
forbidden_leap: "RawArabicTrace → Meaning (without licensed signifier)"
input_type: "RawArabicTrace"
output_type: "LicensedSignifierObject"

required_evidence:
  - phonetic_material: PhonemicSequence
  - diacritic_material: DiacriticSequence
  - syllable_structure: SyllableStructure
  - boundary_markers: BoundaryMarkers

rank_policy:
  - CANDIDATE if diacritics incomplete
  - ZANNI if diacritics complete but boundary uncertain
  - CERTIFIED if diacritics complete + boundaries clear
  - BLOCKED if phonetic material invalid

residual_vector:
  - diacritic_gaps: List[Position]
  - boundary_ambiguity: bool
  - syllable_uncertainty: bool
  - affix_attachment_ambiguity: bool

forbidden_fields:
  - meaning: PROHIBITED
  - wadh: PROHIBITED
  - dalalah: PROHIBITED
  - hukm: PROHIBITED
  - mutabaqah: PROHIBITED

golden_cases:
  - "كتب" (no diacritics) → CANDIDATE, low rank
  - "كَتَبَ" (complete) → CERTIFIED dal, no meaning
  - "كِتَابٌ" (complete) → CERTIFIED dal, no meaning

tests_required:
  - test_incomplete_diacritics_lowers_rank
  - test_complete_diacritics_licensed
  - test_dal_does_not_carry_meaning
  - test_dal_does_not_carry_wadh
  - test_invalid_phonetic_blocked

dashboard_metric:
  - pure_dal_coverage: float
  - meaning_injection_prevention: float
```

**Reference**: PR-L3 (Pure Dal Geometry)

---

### B.2 SignifiedLayerGate

**File**: `src/gfa/methods/lafzi_dalalah/signified_layer_gate.py`

```python
gate_id: "B2_SIGNIFIED_LAYER"
layer: "Signifier & Utterance"
forbidden_leap: "LexicalMeaning → IntendedMeaning (without context gate)"
input_type: "LexicalMeaningCandidate"
output_type: "ContextualMeaningCandidate | IntendedMeaningCandidate"

required_evidence:
  - lexical_source: LexicalSource
  - context_evidence: Optional[ContextEvidence]
  - intention_markers: Optional[List[IntentionMarker]]

rank_policy:
  - Lexical layer: rank from source
  - Contextual layer: requires context evidence
  - Intended layer: requires intention markers
  - Each layer transition requires explicit evidence

residual_vector:
  - layer_transition_uncertainty: bool
  - context_ambiguity: bool
  - intention_inference_risk: float
  - multiple_contextual_possibilities: bool

transition_gates:
  - VERBAL → LEXICAL: requires lexicon witness
  - LEXICAL → CONTEXTUAL: requires context evidence
  - CONTEXTUAL → INTENDED: requires intention markers
  - No direct LEXICAL → JUDGMENT allowed

golden_cases:
  - "كتاب" → lexical: book, contextual depends on sentence
  - "رأيت أسدًا" → lexical: lion, contextual may be metaphorical (brave person)

tests_required:
  - test_lexical_to_contextual_requires_context
  - test_contextual_to_intended_requires_markers
  - test_no_direct_lexical_to_judgment
  - test_layer_skipping_blocked
  - test_each_layer_preserves_trace

dashboard_metric:
  - signified_layer_separation: float
  - premature_intention_inference_prevention: float
```

---

## C. Form & Structure Closure Gates

### C.1 DerivationalContinuumGate

**File**: `src/gfa/foundations/morphology/derivational_continuum_gate.py`

```python
gate_id: "C1_DERIVATIONAL_CONTINUUM"
layer: "Form & Structure"
forbidden_leap: "Root → ProductiveDerivation (without productivity evidence)"
input_type: "LexicalItem"
output_type: "DerivationalContinuumCandidate"

required_evidence:
  - root_evidence: Optional[RootEvidence]
  - derivational_evidence: Optional[DerivationalEvidence]
  - productivity_evidence: Optional[ProductivityEvidence]
  - lexical_attestation: List[AttestationEvidence]

rank_policy:
  - root_status and derivational_status are INDEPENDENT
  - Presence of root ≠ productive derivation
  - Frozen derivations marked separately
  - Technical transfers require domain evidence

residual_vector:
  - root_uncertainty: bool
  - productivity_uncertainty: bool
  - frozen_status_uncertainty: bool
  - etymological_speculation: bool

critical_law:
  root_status ≠ derivational_status

golden_cases:
  - "الأرض" → JAMID_RADICAL (has root ر-ض but not productive derivation)
  - "السماء" → JAMID_ORIGINAL (root uncertain, not productive)
  - "كَاتِب" → DERIVED_PRODUCTIVE (active participle, productive)
  - "مُعَلِّم" → DERIVED_PRODUCTIVE (active participle, productive)
  - "إنسان" → JAMID_PRESERVED (preserved by attestation, root disputed)

tests_required:
  - test_root_does_not_imply_productivity
  - test_frozen_derivation_marked
  - test_jamid_with_root_separated
  - test_productive_derivation_requires_evidence
  - test_technical_transfer_requires_domain
  - test_proper_name_marked_separately

dashboard_metric:
  - root_derivation_separation: float
  - productivity_assessment_coverage: float
  - frozen_derivation_detection: float
```

**Critical Law**:
```text
وجود جذر محتمل لا يعني اشتقاقًا منتجًا
Presence of possible root ≠ productive derivation
```

---

### C.2 MabniGate

**File**: `src/gfa/foundations/morphology/mabni_gate.py`

```python
gate_id: "C2_MABNI"
layer: "Form & Structure"
forbidden_leap: "Mabni → RootPattern (forced extraction)"
input_type: "LexicalItem"
output_type: "MabniCandidate"

required_evidence:
  - mabni_type: MabniType
  - operator_function: Optional[List[OperatorFunction]]
  - reference_potential: Optional[ReferenceCandidate]
  - syntactic_requirements: List[SyntacticRequirement]

rank_policy:
  - Mabni items identified by function, not form
  - No root extraction attempted
  - Operator function takes precedence
  - Reference potential evaluated independently

residual_vector:
  - function_ambiguity: bool
  - reference_domain_uncertainty: bool
  - complement_requirement_uncertainty: bool

forbidden_operations:
  - root_extraction: PROHIBITED for mabni
  - pattern_application: PROHIBITED for mabni
  - derivational_analysis: PROHIBITED for mabni

golden_cases:
  - "هذا" → DEMONSTRATIVE, reference_potential required
  - "الذي" → RELATIVE, requires relative clause
  - "من" → INTERROGATIVE | PARTICLE (function depends on context)
  - "في" → PARTICLE, requires complement
  - "هو" → PRONOUN, reference_potential required
  - "لم" → NEGATION_PARTICLE, requires verb

tests_required:
  - test_mabni_no_root_extraction
  - test_demonstrative_reference_potential
  - test_relative_requires_clause
  - test_particle_requires_complement
  - test_pronoun_reference_domain
  - test_mabni_pattern_prohibition

dashboard_metric:
  - mabni_forced_root_prevention: float
  - operator_function_identification: float
  - reference_potential_coverage: float
```

**Critical Law**:
```text
المبني لا يُجبر على هندسة الجذر والوزن
Mabni shall not be forced into root-pattern geometry.
```

---

### C.3 MurabAmilGate

**File**: `src/gfa/foundations/syntax/murab_amil_gate.py`

```python
gate_id: "C3_MURAB_AMIL"
layer: "Form & Structure"
forbidden_leap: "CaseMarking → SyntacticRelation (without 'amil)"
input_type: "TerminalForm"
output_type: "MurabCandidate + AmilCandidate"

required_evidence:
  - terminal_form: str
  - case_marking: CaseMarking
  - amil_candidate: Optional[AmilCandidate]
  - syntactic_context: SyntacticContext

rank_policy:
  - Case marking observed: CANDIDATE
  - 'Amil identified: ZANNI
  - 'Amil + relation verified: CERTIFIED
  - No 'amil ≠ no i'rab determination

residual_vector:
  - amil_uncertainty: bool
  - multiple_amil_candidates: bool
  - case_visibility_issue: bool
  - blocking_factors: List[BlockingFactor]

critical_law:
  - "لا إعراب بلا عامل" (No i'rab without 'amil)
  - "لا علامة بلا علاقة" (No marking without relation)
  - "لا علاقة بلا بوابة" (No relation without gate)

golden_cases:
  - "زيدٌ" (nominative) → requires 'amil (ibtida'/verb/etc.)
  - "زيدًا" (accusative) → requires 'amil (verb/inna/etc.)
  - "زيدٍ" (genitive) → requires 'amil (preposition/idafa)

tests_required:
  - test_case_marking_without_amil_incomplete
  - test_amil_identification_raises_rank
  - test_multiple_amil_candidates_residualized
  - test_amil_relation_verified
  - test_blocking_factors_prevent_i3rab

dashboard_metric:
  - case_without_amil_prevention: float
  - amil_identification_coverage: float
  - i3rab_relation_verification: float
```

**Reference**: Aligns with NahwOperatorRegistry (PR #16), OperatorTriggerPotential (PR #14)

---

### C.4 TenseCompositionGate

**File**: `src/gfa/foundations/syntax/tense_composition_gate.py`

```python
gate_id: "C4_TENSE_COMPOSITION"
layer: "Form & Structure"
forbidden_leap: "VerbForm → CompositionalTense (without particles/context)"
input_type: "VerbForm"
output_type: "TenseNasikhCandidate"

required_evidence:
  - word_level_tense: WordTense
  - tense_particles: List[TenseParticle]
  - compositional_context: CompositionalContext
  - nasikh_activation: Optional[NasikhActivation]

rank_policy:
  - Word-level tense: CERTIFIED from form
  - Compositional tense: requires particles/context
  - Nasikh activation: requires syntactic slots filled
  - Each level maintains separate rank

residual_vector:
  - compositional_ambiguity: bool
  - particle_scope_uncertainty: bool
  - nasikh_slot_gaps: List[SlotGap]
  - multiple_compositional_readings: bool

critical_law:
  - "زمن المفرد ≠ زمن التركيب" (Word tense ≠ compositional tense)
  - "كان في المفرد ≠ ناسخ دائم" (kāna in isolation ≠ always nasikh)

golden_cases:
  - "كتب" → word: PAST, compositional: depends on context
  - "قد كتب" → word: PAST, compositional: PERFECTIVE
  - "كان يكتب" → word: PAST + PRESENT, compositional: PAST_CONTINUOUS
  - "لم يكتب" → word: PRESENT, compositional: NEGATED_PAST
  - "سيكتب" → word: PRESENT, compositional: FUTURE
  - "كان" alone → NasikhCandidate, not activated
  - "كان زيدٌ قائمًا" → Nasikh activated (slots filled)

tests_required:
  - test_word_tense_separated_from_compositional
  - test_particles_modify_compositional_tense
  - test_nasikh_requires_activation
  - test_kana_alone_not_nasikh
  - test_nasikh_slots_required
  - test_multiple_compositional_readings

dashboard_metric:
  - word_compositional_tense_separation: float
  - nasikh_premature_activation_prevention: float
  - compositional_tense_coverage: float
```

---

### C.5 ReferenceGate

**File**: `src/gfa/foundations/syntax/reference_gate.py`

```python
gate_id: "C5_REFERENCE"
layer: "Form & Structure"
forbidden_leap: "Pronoun → FinalReferent (without search domain)"
input_type: "ReferentialMarker"
output_type: "ReferenceCandidate"

required_evidence:
  - reference_type: ReferenceType
  - search_domain: SearchDomain
  - agreement_constraints: List[AgreementConstraint]
  - candidate_referents: List[ReferentCandidate]

rank_policy:
  - Referential marker observed: CANDIDATE
  - Search domain identified: ZANNI
  - Single referent satisfies constraints: CERTIFIED
  - Multiple candidates remain: ZANNI with residuals
  - No candidates found: BLOCKED

residual_vector:
  - search_domain_ambiguity: bool
  - multiple_candidate_referents: List[ReferentCandidate]
  - agreement_violations: List[AgreementViolation]
  - elliptic_reconstruction_required: bool
  - discourse_boundary_uncertainty: bool

critical_law:
  - "العلامة الإحالية لا تثبت المرجع، إنما تفتح مجال بحث"
  - (Referential marker does not establish referent, it opens search domain)

golden_cases:
  - "هو" → requires prior mention or situational context
  - "هذا" → requires demonstrative context (near/far)
  - "الذي" → requires relative clause
  - "ضمير مستتر" → requires syntactic reconstruction

tests_required:
  - test_pronoun_opens_search_not_establishes
  - test_demonstrative_requires_context
  - test_relative_requires_clause
  - test_multiple_candidates_residualized
  - test_agreement_constraints_enforced
  - test_elliptic_referent_marked

dashboard_metric:
  - pronoun_to_referent_leap_prevention: float
  - search_domain_identification: float
  - referent_resolution_coverage: float
```

---

## D. Signification & Usage Closure Gates

### D.1 WadhGate

**File**: `src/gfa/methods/lafzi_wadh/wadh_gate.py`

**Status**: ✓ Already implemented (PR-L5B)

```python
gate_id: "D1_WADH"
layer: "Signification & Usage"
forbidden_leap: "Form → Meaning (without wadh evidence)"
input_type: "DalMadlulBindingCandidate"
output_type: "WadhClaim"

required_evidence:
  - wadh_evidence: WadhEvidence
  - wadh_source: WadhSource
  - transmission_mode: WadhTransmissionMode
  - wadh_scope: WadhScope
  - mawdu_lah_structure: MawduLahStructure

rank_policy:
  - Reason alone: INSUFFICIENT for Arabic wadh
  - Transmission required: SAMA | URF | NAQL
  - Unknown source: becomes blocker residual
  - Unknown transmission: becomes blocker residual
  - Success = ADMITTED, not CERTIFIED

residual_vector:
  - source_uncertainty: bool
  - transmission_uncertainty: bool
  - scope_uncertainty: bool
  - competing_wadh_claims: List[WadhClaim]

forbidden_outputs:
  - external_meaning: PROHIBITED
  - dalalah: PROHIBITED (deferred to higher layer)
  - hukm: PROHIBITED
  - mutabaqah: PROHIBITED (separate gate)
  - tadammun: PROHIBITED
  - iltizam: PROHIBITED

golden_cases:
  - Quranic term → SHAR source, high rank
  - Lexicon entry → SAMA source, attestation required
  - Technical term → ISTILAH source, domain required

tests_required:
  - test_reason_alone_insufficient
  - test_transmission_required
  - test_unknown_source_blocks
  - test_wadh_does_not_create_meaning
  - test_wadh_does_not_create_dalalah

dashboard_metric:
  - wadh_source_coverage: float
  - form_to_meaning_leap_prevention: float
```

**Reference**: PR-L5B (WadhGate Implementation)

---

### D.2 UsageGate

**File**: `src/gfa/methods/lafzi_dalalah/usage_gate.py`

```python
gate_id: "D2_USAGE"
layer: "Signification & Usage"
forbidden_leap: "Wadh → ContextualUsage (without context evidence)"
input_type: "WadhClaim"
output_type: "UsageCandidate"

required_evidence:
  - usage_type: UsageType
  - context_evidence: List[ContextEvidence]
  - transfer_path: Optional[List[TransferStep]]
  - qarina: Optional[List[ContextualIndicator]]

rank_policy:
  - Literal usage: inherits wadh rank
  - Metaphorical usage: requires qarina
  - Technical usage: requires domain evidence
  - Transferred usage: requires transfer path evidence
  - Each usage type has specific evidence requirements

residual_vector:
  - literal_metaphorical_ambiguity: bool
  - qarina_uncertainty: bool
  - transfer_path_speculation: bool
  - multiple_usage_possibilities: bool
  - domain_shift_uncertainty: bool

critical_law:
  - "الوضع الأصلي لا يكفي لإثبات الاستعمال السياقي"
  - (Original wadh insufficient for contextual usage)

golden_cases:
  - "أسد" in "رأيت أسدًا" → literal (animal)
  - "أسد" in "رأيت أسدًا يخطب" → metaphorical (brave person), requires qarina
  - "الماء" in chemistry → technical usage, requires domain
  - "صلاة" in Islamic context → technical/legal usage

tests_required:
  - test_literal_usage_inherits_wadh
  - test_metaphorical_requires_qarina
  - test_no_qarina_blocks_metaphorical
  - test_technical_usage_requires_domain
  - test_transfer_path_required
  - test_multiple_usages_residualized

dashboard_metric:
  - wadh_to_usage_leap_prevention: float
  - qarina_evidence_coverage: float
  - metaphorical_usage_detection: float
```

---

### D.3 SpeechForceGate

**File**: `src/gfa/methods/maqam/speech_force_gate.py`

**Status**: ✓ Partially implemented (Maqam Theory gates)

```python
gate_id: "D3_SPEECH_FORCE"
layer: "Signification & Usage"
forbidden_leap: "Imperative → Obligation (without normative gate)"
input_type: "UtteranceStructure"
output_type: "SpeechForceCandidate"

required_evidence:
  - force_type: SpeechForceType
  - force_markers: List[ForceMarker]
  - context: UtteranceContext
  - possible_functions: List[PragmaticFunction]

rank_policy:
  - Force markers observed: CANDIDATE
  - Context supports force: ZANNI
  - Force does NOT equal normative status
  - Each force type ≠ single function

residual_vector:
  - force_function_ambiguity: bool
  - multiple_pragmatic_functions: bool
  - rhetorical_uncertainty: bool

critical_laws:
  - "الخبر ≠ الصدق" (Declarative ≠ Truth)
  - "الأمر ≠ الوجوب" (Imperative ≠ Obligation)
  - "النهي ≠ التحريم" (Prohibitive ≠ Legal prohibition)
  - "الاستفهام ≠ الجهل" (Interrogative ≠ Ignorance)

golden_cases:
  - "اكتب" → IMPERATIVE force, functions: obligation | request | advice | permission
  - "لا تكتب" → PROHIBITIVE force, functions: prohibition | advice | warning
  - "هل كتبت؟" → INTERROGATIVE force, functions: question | reproach | denial
  - "زيد قائم" → DECLARATIVE force, functions: statement | claim | assertion

tests_required:
  - test_imperative_not_obligation
  - test_prohibitive_not_legal_prohibition
  - test_interrogative_multiple_functions
  - test_declarative_not_truth
  - test_force_markers_identified
  - test_force_function_separated

dashboard_metric:
  - force_to_norm_leap_prevention: float
  - force_function_separation: float
  - pragmatic_function_coverage: float
```

**Reference**: Maqam Theory gates (InterrogativeGate, VocativeGate, ImperativeGate)

---

## E. Statement & Judgment Closure Gates

### E.1 StructuralValidityGate

**File**: `src/gfa/foundations/syntax/structural_validity_gate.py`

```python
gate_id: "E1_STRUCTURAL_VALIDITY"
layer: "Statement & Judgment"
forbidden_leap: "StructuralValidity → Truth (without evidence)"
input_type: "SyntacticStructure"
output_type: "StatementCandidate"

required_evidence:
  - structural_completeness: StructuralCompleteness
  - grammatical_validity: GrammaticalValidity
  - semantic_coherence: Optional[SemanticCoherence]

rank_policy:
  - Structural validity: LINGUISTIC domain only
  - Does NOT establish truth
  - Does NOT establish external validity
  - Produces CLAIM, not JUDGMENT

residual_vector:
  - semantic_coherence_issues: List[CoherenceIssue]
  - pragmatic_anomaly: bool
  - domain_shift_required: bool

critical_law:
  - "صحة التركيب ≠ صحة الحكم"
  - (Structural validity ≠ Judgment validity)

golden_cases:
  - "زيد قائم" → structurally valid, produces claim
  - "الجبل طار" → structurally valid, semantically anomalous, produces claim
  - "قائم زيد" → structurally invalid (word order issue)

tests_required:
  - test_structural_validity_not_truth
  - test_valid_structure_produces_claim
  - test_semantic_anomaly_residualized
  - test_invalid_structure_blocked
  - test_structural_validity_linguistic_domain_only

dashboard_metric:
  - structure_to_truth_leap_prevention: float
  - claim_production_coverage: float
```

---

### E.2 HukmEvidenceGate

**File**: `src/gfa/foundations/hukm/hukm_evidence_gate.py`

```python
gate_id: "E2_HUKM_EVIDENCE"
layer: "Statement & Judgment"
forbidden_leap: "Statement → Judgment (without manat + evidence)"
input_type: "StatementCandidate"
output_type: "HukmCandidate"

required_evidence:
  - claim: str
  - domain: str
  - manat: Manat  # criterion
  - conditions: List[Condition]
  - blockers_assessment: List[Blocker]
  - evidence: List[Evidence]

rank_policy:
  - Claim without evidence: CANDIDATE
  - Claim with partial evidence: ZANNI
  - Claim with complete evidence + no blockers: CERTIFIED
  - Blockers present: rank reduced or BLOCKED
  - Domain shift requires re-validation

residual_vector:
  - manat_uncertainty: bool
  - condition_gaps: List[ConditionGap]
  - blocker_presence: List[Blocker]
  - evidence_gaps: List[EvidenceGap]
  - domain_applicability_uncertainty: bool

critical_law:
  - "لا حكم بلا دليل" (No judgment without evidence)
  - "لا تنزيل بلا تحقيق مناط" (No instantiation without criterion realization)

golden_cases:
  - "الماء طاهر" → requires: which water? what purity domain (fiqh/chemistry)?
  - "زيد عادل" → requires: what justice domain? what evidence?
  - "السماء زرقاء" → requires: observation domain, context

tests_required:
  - test_statement_without_evidence_candidate
  - test_manat_required
  - test_conditions_required
  - test_blockers_assessed
  - test_domain_specified
  - test_evidence_gaps_residualized
  - test_no_evidence_blocks_judgment

dashboard_metric:
  - statement_to_judgment_leap_prevention: float
  - manat_realization_coverage: float
  - evidence_requirement_enforcement: float
```

---

### E.3 DomainTransferGate

**File**: `src/gfa/foundations/domain/domain_transfer_gate.py`

```python
gate_id: "E3_DOMAIN_TRANSFER"
layer: "Statement & Judgment"
forbidden_leap: "DomainRule_A → DomainRule_B (without transfer license)"
input_type: "DomainRule"
output_type: "DomainTransferCandidate"

required_evidence:
  - source_domain: str
  - target_domain: str
  - transfer_license: Optional[TransferLicense]
  - primitive_mapping: Optional[PrimitiveMapping]
  - validity_preservation: Optional[ValidityPreservation]

rank_policy:
  - Same domain: preserves rank
  - Related domains with license: ZANNI
  - Unrelated domains: BLOCKED
  - Transfer without validation: CANDIDATE with high residuals

residual_vector:
  - primitive_mapping_gaps: List[MappingGap]
  - validity_preservation_uncertainty: bool
  - domain_boundary_ambiguity: bool
  - analogy_strength: float

forbidden_transfers:
  - Grammatical → Empirical (without validation)
  - Statistical → Certainty (without conditions)
  - Lexical → Intent (without pragmatic gate)
  - Linguistic → Ontological (without domain shift validation)

golden_cases:
  - Grammar rule → empirical claim: BLOCKED
  - Statistical correlation → certainty: BLOCKED
  - Lexical meaning → speaker intent: requires pragmatic gate
  - Mathematical proof → physical law: requires empirical validation

tests_required:
  - test_same_domain_preserves_rank
  - test_unrelated_domain_blocked
  - test_grammatical_to_empirical_blocked
  - test_statistical_to_certainty_blocked
  - test_transfer_license_required
  - test_primitive_mapping_required

dashboard_metric:
  - domain_leap_prevention: float
  - transfer_license_coverage: float
  - validity_preservation_verification: float
```

---

## F. Governance & Testing Closure Gates

### F.1 PriorFilterGate

**File**: `src/gfa/foundations/prior/prior_filter_gate.py`

**Status**: ✓ Partially implemented (NeutralBinding PR-N1)

```python
gate_id: "F1_PRIOR_FILTER"
layer: "Governance & Testing"
forbidden_leap: "PriorOpinion → PriorInformation (without evidence)"
input_type: "PriorItem"
output_type: "PriorInformationCandidate | FilteredPrior"

required_evidence:
  - content: Any
  - domain: str
  - source: PriorSource
  - evidence_trace: EvidenceTrace
  - rank: PredicateRank

rank_policy:
  - Opinion: FILTERED (not admitted as information)
  - Rule with source: ADMITTED as PriorInformation
  - Definition with evidence: ADMITTED
  - Impression/bias/taste: FILTERED

residual_vector:
  - contamination_risk: float
  - source_uncertainty: bool
  - opinion_injection_risk: float

critical_law:
  - "PriorInformation ≠ PriorOpinion"
  - "لا رأي سابق يدخل بوصفه معلومة"
  - (No prior opinion enters as information)

filtered_items:
  - انطباع (impression)
  - تحيز (bias)
  - ذوق (taste)
  - عادة (habit)
  - تفسير غير موثق (undocumented interpretation)
  - حكم سابق بلا دليل (prior judgment without evidence)

golden_cases:
  - "Grammar rule from source" → ADMITTED as PriorInformation
  - "Personal interpretation" → FILTERED
  - "Undocumented practice" → FILTERED
  - "Definition from lexicon" → ADMITTED
  - "Bias" → FILTERED

tests_required:
  - test_opinion_filtered
  - test_rule_with_source_admitted
  - test_impression_filtered
  - test_bias_filtered
  - test_undocumented_interpretation_filtered
  - test_prior_judgment_without_evidence_filtered

dashboard_metric:
  - opinion_to_information_leap_prevention: float
  - prior_contamination_prevention: float
  - source_verification_coverage: float
```

**Reference**: PR-N1 (NeutralBinding)

---

### F.2 CognitiveAuditGate

**File**: `src/gfa/foundations/cognitive/cognitive_audit_gate.py`

**Status**: ✓ Partially implemented (Memory Geometry PR-G1)

```python
gate_id: "F2_COGNITIVE_AUDIT"
layer: "Governance & Testing"
forbidden_leap: "MemoryTrace → Evidence (without source validation)"
input_type: "CognitiveState"
output_type: "CognitiveStateCandidate"

required_evidence:
  - attention_focus: Any
  - memory_trace: List[MemoryTrace]
  - source_trace: SourceTrace
  - decay_assessment: DecayAssessment
  - error_risk_assessment: ErrorRiskAssessment

rank_policy:
  - Memory recall: NOT evidence
  - Attention: affects priority, NOT rank
  - Error: learning trace, not failure
  - Correction: trace-preserving update

residual_vector:
  - memory_decay: float  # mandatory
  - recall_distortion: float  # mandatory
  - attention_bias: float
  - error_risk: float
  - source_uncertainty: bool

critical_laws:
  - "الذاكرة ≠ دليل" (Memory ≠ Evidence)
  - "الانتباه ≠ حكم" (Attention ≠ Judgment)
  - "الاستحضار ≠ تحقق" (Recall ≠ Realization)
  - "الفشل = أثر تعلم" (Failure = Learning trace)

forbidden_promotions:
  - Memory → Evidence: PROHIBITED
  - Attention → Judgment: PROHIBITED
  - Recall → Certainty: PROHIBITED

golden_cases:
  - Recalled rule → trace with decay residuals, NOT evidence
  - Attentional focus → priority marker, NOT rank promotion
  - Error → learning trace, correction path opened
  - Memory of lexicon entry → requires re-verification

tests_required:
  - test_memory_not_evidence
  - test_attention_not_judgment
  - test_recall_not_certainty
  - test_memory_decay_mandatory
  - test_recall_distortion_mandatory
  - test_error_as_learning_trace
  - test_correction_preserves_trace

dashboard_metric:
  - memory_to_evidence_leap_prevention: float
  - cognitive_bias_detection: float
  - error_learning_trace_coverage: float
```

**Reference**: PR-G1 (Memory Geometry Kernel)

---

### F.3 MaturityDashboard

**File**: `src/gfa/governance/maturity_dashboard.py`

```python
gate_id: "F3_MATURITY_DASHBOARD"
layer: "Governance & Testing"
forbidden_leap: "ProgrammingSuccess → EpistemologicalTruth"
input_type: "ProjectState"
output_type: "MaturityReport"

required_metrics:
  - typed_contract_coverage: float  # [0.0, 1.0]
  - no_leap_coverage: float
  - rank_inflation_risk: float
  - residual_debt: float
  - trace_coverage: float
  - golden_dataset_coverage: float
  - claim_inflation_risk: float
  - layer_completion: float

rank_policy:
  - Achievement measured by completion, not file count
  - Each gate must have: type, implementation, evidence, rank, residuals, tests, trace
  - Governance metrics track real progress

residual_vector:
  - incomplete_gates: List[GateID]
  - untested_gates: List[GateID]
  - missing_golden_cases: List[GateID]
  - claim_without_evidence: List[str]

critical_law:
  - "لا يُحسب الإنجاز بعدد الملفات، بل باكتمال النوع والدليل والرتبة والبقايا والاختبار والأثر"
  - (Achievement not counted by file count, but by completion of type, evidence, rank, residuals, testing, trace)

dashboard_components:
  - Typed Contract Coverage
  - NoLeap Coverage
  - Rank Inflation Risk
  - Residual Debt
  - Trace Coverage
  - Golden Dataset Coverage
  - Claim Inflation Risk
  - Layer Completion
  - Gate Implementation Status
  - Test Coverage per Gate
  - Evidence Coverage per Claim

golden_cases:
  - High file count, low completion → LOW maturity
  - Complete gates with tests → HIGH maturity
  - Claims without evidence → maturity BLOCKED

tests_required:
  - test_file_count_not_achievement
  - test_gate_completion_required
  - test_golden_dataset_required
  - test_claims_require_evidence
  - test_residual_debt_tracked
  - test_rank_inflation_detected

dashboard_metric:
  - overall_maturity_score: float
  - governance_effectiveness: float
  - epistemological_soundness: float
```

---

## Implementation Priority

### Phase 1: Critical Foundations (3-4 weeks)

1. **RealityTypeGate** (A.1) - Foundation for all reality handling
2. **NameRealityGate** (A.2) - Prevents most common epistemological errors
3. **DerivationalContinuumGate** (C.1) - Core morphological principle
4. **MabniGate** (C.2) - Protects against forced root extraction

### Phase 2: Signification Chain (3-4 weeks)

5. **SignifiedLayerGate** (B.2) - Prevents meaning layer confusion
6. **UsageGate** (D.2) - Completes wadh → usage transition
7. **StructuralValidityGate** (E.1) - Separates syntax from truth

### Phase 3: Judgment & Domain (2-3 weeks)

8. **HukmEvidenceGate** (E.2) - Critical for claim → judgment
9. **DomainTransferGate** (E.3) - Prevents domain leaps

### Phase 4: Advanced Features (2-3 weeks)

10. **TraceEffectGate** (A.3) - Trace handling
11. **MurabAmilGate** (C.3) - I'rab completeness
12. **TenseCompositionGate** (C.4) - Compositional tense
13. **ReferenceGate** (C.5) - Reference resolution

### Phase 5: Governance (1-2 weeks)

14. **MaturityDashboard** (F.3) - Track all gates

**Total Estimated Time**: 11-16 weeks for complete implementation

---

## Testing Strategy

### Per-Gate Testing Requirements

Each gate must have:

1. **Admission tests** - Valid inputs admitted
2. **Blocking tests** - Invalid inputs blocked
3. **Leap prevention tests** - Forbidden transitions caught
4. **Rank policy tests** - Correct rank assignment
5. **Residual tests** - Proper residual accumulation
6. **Trace preservation tests** - Trace continuity maintained
7. **Golden case tests** - All golden cases pass
8. **Failure mode tests** - Governed failures returned

### Integration Testing

1. **Gate chain tests** - Sequential gate transitions
2. **Cross-layer tests** - Layer boundary enforcement
3. **Rank propagation tests** - Rank never inflates
4. **Residual accumulation tests** - Residuals preserved across gates

### Governance Testing

1. **Dashboard accuracy** - Metrics reflect reality
2. **Claim verification** - All claims evidenced
3. **Maturity assessment** - Progress measured correctly

---

## Success Criteria

A gate is considered **CERTIFIED** when:

1. ✓ Type contracts defined and enforced
2. ✓ All required evidence types implemented
3. ✓ Rank policy implemented and tested
4. ✓ Residual vector complete
5. ✓ Forbidden operations blocked
6. ✓ All golden cases pass
7. ✓ All test categories covered (8 types)
8. ✓ Documentation complete
9. ✓ Integrated into dashboard
10. ✓ Reviewed and approved

---

## Alignment with Existing Architecture

### Already Implemented Gates

- **WadhGate** (D.1) - PR-L5B ✓
- **MutabaqahGate** - PR-L6A ✓
- **PureDalGate** (B.1) - PR-L3 ✓
- **NeutralBinding/PriorFilter** (F.1) - PR-N1 ✓
- **Memory Geometry/CognitiveAudit** (F.2) - PR-G1 ✓
- **Maqam Gates/SpeechForce** (D.3) - Maqam Theory ✓

### Partially Implemented

- **MurabAmilGate** (C.3) - NahwOperatorRegistry (PR #16) provides foundation
- **TenseCompositionGate** (C.4) - Partial support in syntax theory

### Need Full Implementation

- All gates in Phase 1-4 above not marked as implemented

---

## Conclusion

This matrix provides an **executable roadmap** for implementing the complete closure framework. Each gate specification can be directly converted to:

1. Python dataclass definitions
2. Test suites
3. Documentation
4. Dashboard metrics

The result will be a **complete epistemological usurpation prevention system** for Arabic NLP that extends beyond linguistics into general knowledge algebra.

---

**Next Action**: Begin Phase 1 implementation starting with **RealityTypeGate** and **NameRealityGate**.
