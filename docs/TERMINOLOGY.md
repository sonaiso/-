# Terminology

**Purpose**: Precise definitions of core terms used in General Cognitive Algebra

**Principle**: Every term must have a **typed contract** not just a description

---

## General Cognitive Terms

### Reality (الواقع)

**Definition**: That which exists or occurs independently of observation, accessible through sensory transfer.

**Type**: `RealityTrace` (see `src/gfa/reality/reality_trace.py`)

**Properties**:
- Has existence type (PHYSICAL, CONCEPTUAL, LINGUISTIC, etc.)
- Anchored in time and place
- Produces existential effect
- Accessible through channel (sensory/instrumental)

**NOT**:
- ❌ Reality is not "interpretation"
- ❌ Reality is not "meaning"
- ❌ Reality is not "judgment"

**Law**: No knowledge without reality trace

---

### SensoryTrace (الأثر الحسي)

**Definition**: Record of sensory/instrumental transfer from reality to processor.

**Type**: `SensoryEvent` (see `src/gfa/sensory_transfer/sensory_event.py`)

**Properties**:
- Has sensory channel (visual, auditory, instrumental)
- Time-anchored
- Preserves reality reference
- Does NOT certify reality
- Does NOT raise reality rank

**NOT**:
- ❌ Sensory trace is not "proof"
- ❌ Sensory trace is not "certified fact"
- ❌ Sensory repetition does not create knowledge without prior information

**Law**: Sensory trace ≠ knowledge (requires binding with prior information)

---

### CognitiveCarrier (المعالج الصالح / الدماغ الصالح)

**Definition**: Processor with capacities for attention, memory, comparison, binding, interpretation.

**Type**: `CognitiveCarrierGeometry` (see `src/gfa/cognitive_carrier/cognitive_carrier.py`)

**10 Mandatory Capacities**:
1. sensory_capacity
2. attention_capacity
3. memory_capacity
4. comparison_capacity
5. binding_capacity
6. interpretation_capacity
7. feedback_capacity
8. output_capacity
9. primitive_learning_capacity
10. reflection_capacity

**NOT**:
- ❌ Capacity ≠ correctness
- ❌ Attention ≠ certification
- ❌ Memory recall ≠ original trace
- ❌ Binding ≠ raising rank

**Law**: Carrier does NOT create meaning, does NOT certify, does NOT raise rank

---

### PriorInformationSystem (المعلومات السابقة)

**Definition**: Structured knowledge base (NOT opinions) available before current trace processing.

**Type**: `FirstPriorUnit` (current), `PriorInformationSystem` (planned PR-C1)

**14 Mandatory Fields** (FirstPriorUnit):
1. entity_or_effect
2. existence_type
3. domain
4. distinction
5. boundary
6. time_anchor
7. place_anchor
8. reference_anchor
9. channel
10. retention_state
11. comparability_state
12. primitive_bindability
13. residuals
14. rank

**NOT**:
- ❌ PriorInformation ≠ PriorOpinion
- ❌ Prior beliefs do NOT enter binding
- ❌ Opinions are blocked or quarantined

**Law**: PriorInformation enters binding, PriorOpinion is blocked

---

### PriorOpinion (الرأي السابق)

**Definition**: Pre-existing belief or interpretation (NOT knowledge).

**Type**: `PriorOpinion` (see `src/gfa/methods/rational/prior_filter.py`)

**Properties**:
- Has bias_risk assessment
- `allowed_as_evidence = False`
- Blocked from binding operations
- Can contaminate PriorInformation if not filtered

**NOT**:
- ❌ Opinion does not enter binding
- ❌ Opinion does not substitute for evidence

**Law**: PriorOpinion contamination is a blocker residual

---

### GovernedBinding (الربط المرخّص)

**Definition**: Licensed transition between typed domains with full provenance.

**Type**: Implemented via `NeutralBinding`, `DalMadlulBindingGate` (general contract planned PR-C2)

**Required Elements**:
- left (input candidate)
- right (input candidate)
- prior_information (PriorInformationSystem, not Opinion)
- evidence (scoped Evidence)
- layer (LayerSpec)
- scope (domain boundary)

**Output**: `Result` with full provenance

**NOT**:
- ❌ Governed binding ≠ free association
- ❌ Binding ≠ meaning creation
- ❌ Binding success ≠ rank promotion

**Law**: Binding is neutral relation, not semantic interpretation

---

### Tasawwur (التصور)

**Definition**: Conceptualization of entity/effect from bound information (NOT judgment).

**Type**: `TasawwurCandidate` (planned PR-C3)

**Properties**:
- Result of binding with prior information
- Can be incomplete (residuals allowed)
- Does NOT produce judgment
- Does NOT produce meaning directly

**NOT**:
- ❌ Tasawwur ≠ Hukm
- ❌ Conceptualization ≠ judgment
- ❌ Tasawwur alone is not ifādah

**Law**: Tasawwur is necessary but not sufficient for Hukm

---

### Nisbah (النسبة)

**Definition**: Relational binding between two tasawwurat (conceptualizations).

**Type**: `NisbahCandidate` (planned PR-C4)

**Properties**:
- Requires two licensed tasawwurat
- Can be incomplete (e.g., conditional without jawāb)
- Does NOT automatically produce ifādah

**NOT**:
- ❌ Nisbah ≠ Ifādah
- ❌ Relational structure ≠ semantic completion
- ❌ Iḍāfah alone is not ifādah

**Law**: النسبة الإضافية لا تصبح إفادة (Iḍāfah relation alone does not become ifādah)

---

### Ifadah (الإفادة)

**Definition**: Semantic completion (complete predication that can be affirmed or denied).

**Type**: `IfadahCandidate` (planned PR-C5)

**8 Requirements**:
1. Licensed parties
2. Licensed dāl/madlūl binding
3. Licensed dalālah (mutābaqah/taḍammun/iltizām)
4. Licensed nisbah
5. Complete structure
6. Resolved references or residuals
7. Known speech force or residual
8. Full residual accounting

**NOT**:
- ❌ Ifādah ≠ Hukm
- ❌ Semantic completion ≠ judgment
- ❌ Ifādah with residuals cannot be CERTIFIED

**Law**: الإفادة ذات البقايا لا تُعتَمد (Ifādah with residuals cannot be certified)

---

### Hukm (الحكم)

**Definition**: Judgment about reality (requires ifādah + external authority + evidence).

**Type**: `HukmCandidate` (planned PR-C6)

**Properties**:
- Requires complete ifādah
- Requires external authority validation
- Requires evidence beyond form
- Aspirational (not fully automatable)

**NOT**:
- ❌ Hukm is not produced by form analysis
- ❌ Hukm is not inferred from semantics alone
- ❌ Khabar is not hukm
- ❌ Amr is not obligation (at semantic layer)

**Law**: الحكم يحتاج سلطة خارجية (Hukm requires external authority)

---

## Arabic Linguistic Terms

### Dāl (الدال)

**Definition**: Signifier form (what is written/spoken), without meaning claim.

**Type**: `DalCandidate` (see `src/gfa/methods/lafzi_dal/`)

**13 Mandatory Fields**:
- surface_form, normalized_form, path_type, formula_candidate
- terminal_state, root_candidate, pattern_candidate, weak_letter_info
- affix_info, reference_status, rank, residuals, evidence_trace

**Forbidden Fields**:
- ❌ meaning
- ❌ dalalah
- ❌ wadh
- ❌ hukm

**Law**: الدال وحده ليس معنى (Dāl alone is not meaning)

---

### Madlūl-Lafẓī (المدلول اللفظي)

**Definition**: Signified meaning candidates (lexical possibilities), not speaker intent.

**Type**: Lafẓī Madlūl Fractal Algebra (see `src/fvafk/algebra/lafzi_madlul/`)

**Properties**:
- Multiple candidates per dāl (polysemy)
- Requires wadh' (conventional binding)
- Does NOT claim speaker intent (murad)

**NOT**:
- ❌ Madlūl ≠ Murad (speaker intent)
- ❌ Lexical meaning ≠ contextual meaning

**Law**: المدلول وحده ليس دلالة (Madlūl alone is not dalālah)

---

### Wadh (الوضع)

**Definition**: Conventional binding between signifier and signified (social contract).

**Type**: `WadhClaim` (see `src/gfa/methods/lafzi_wadh/`)

**Evidence Types**:
- Lexical attestation (سماع)
- Conventional usage (عرف)
- Shariah usage (شرع) where applicable
- Transmission (رواية/نقل)

**21 Laws Enforced** (see WadhGate):
- Reason alone cannot certify Arabic Wadh (requires transmission)
- Unknown source/transmission become blocker residuals
- Lexicon report is evidence NOT Wadh
- Does NOT create meaning/Dalālah/HUKM

**Law**: لا وضع بلا رواية (No wadh' without transmission for Arabic)

---

### Dalālah (الدلالة)

**Definition**: Semantic relation between signifier and signified.

**Three Types**:
1. **المطابقة (Mutābaqah)**: Direct correspondence (whole meaning)
2. **التضمن (Taḍammun)**: Partial inclusion (part of meaning)
3. **الالتزام (Iltizām)**: Entailment (necessary consequence)

**Type**: Implemented via gates (see `src/fvafk/algebra/semantics/operations.py`, `src/gfa/methods/lafzi_dalalah/mutabaqah_gate.py`)

**NOT**:
- ❌ Mutābaqah alone is not ifādah
- ❌ Taḍammun alone is not ifādah
- ❌ Iltizām is not automatic (requires gate)

**Law**: المطابقة والتضمن والالتزام قبل الإفادة (Mutābaqah, taḍammun, iltizām are before ifādah, not ifādah itself)

---

### Mutabaqah (المطابقة)

**Definition**: Direct correspondence between signifier and **whole** of signified.

**Type**: `MutabaqahGate` (see `src/gfa/methods/lafzi_dalalah/mutabaqah_gate.py`)

**29 Tests Enforced**:
- Mutābaqah = whole of placed-for only
- Does NOT create Tadammun/Iltizam/Haqiqah/Majaz/HUKM
- String gloss alone is not mawḍūʿ lah whole

**NOT**:
- ❌ Mutābaqah ≠ Ifādah
- ❌ Direct correspondence ≠ complete meaning

**Law**: المطابقة لا تصبح إفادة وحدها (Mutābaqah alone does not become ifādah)

---

### Tadammun (التضمن)

**Definition**: Partial inclusion (signifier indicates part of signified).

**Type**: `TadammunGate` (see `src/fvafk/algebra/semantics/operations.py`)

**Properties**:
- Indicates subset of meaning
- Requires gate (not automatic)
- Does NOT produce ifādah

**Law**: التضمن لا يصبح إفادة وحده (Taḍammun alone does not become ifādah)

---

### Iltizam (الالتزام)

**Definition**: Entailment (signifier requires necessary consequence).

**Type**: `IltizamGate` (see `src/fvafk/algebra/semantics/operations.py`)

**Properties**:
- Requires explicit gate (not automatic inference)
- Requires evidence
- Does NOT produce ifādah

**Law**: الالتزام ليس تلقائياً (Iltizām is not automatic)

---

## Governance Terms

### Residual (البقية)

**Definition**: Explicit unresolved item that blocks certification.

**Types** (planned PR-F1):
- **LinguisticResidual**: missing_haraka, ambiguous_formula, context_absent
- **ImplementationFailure**: AttributeError, Exception, gate_crash

**Properties**:
- Preserved across operations
- Blocks CERTIFIED rank
- May downgrade rank
- Must NOT include implementation exceptions in successful results

**Law**: Residuals must be preserved, not hidden

---

### Failure (الفشل)

**Definition**: Typed contradiction that actively refutes a claim.

**Type**: `Failure` (see `src/fvafk/algebra/core.py`)

**Properties**:
- Has kind (typed failure classification)
- Has fatal flag (forces REFUTED if true)
- Preserved in Result

**Law**: Fatal failure forces REFUTED rank

---

### Rank (الرتبة)

**Definition**: Epistemic status of a claim.

**Type**: `Rank` enum (see `src/fvafk/algebra/core.py`)

**Values**:
```
UNRESOLVED (0) - No analysis attempted
CANDIDATE (1)  - Possible but weak
LICENSED (2)   - Supported by evidence, residuals remain
CERTIFIED (3)  - Supported and residual-free
REFUTED (-)    - Fatal contradiction
```

**Laws**:
- LICENSED/CERTIFIED require evidence
- CERTIFIED forbidden while residuals remain
- Fatal failure forces REFUTED
- Success of later layer does NOT raise earlier layer rank

---

### Trace (الأثر)

**Definition**: Provenance record enabling replay and audit.

**Type**: `Trace` (see `src/fvafk/algebra/core.py`)

**Properties**:
- Records operation name
- Records inputs
- Records transformation path
- Enables reversibility
- Preserved in Result

**Law**: All operations must be replay-able

---

### NoLeap (منع القفز)

**Definition**: Prohibition of direct transitions between non-adjacent layers.

**Enforcement**: 17 hard gates (see `tests/fvafk/algebra/test_semantic_boundary_hardening.py`, `test_ifadah_forbidden_jumps.py`)

**Forbidden Jumps**:
- ❌ Dal → Meaning
- ❌ Madlūl → Murad
- ❌ Wadh → Dalālah
- ❌ Mutābaqah → Ifādah
- ❌ Ifādah → Hukm
- ❌ Morphology → Semantics
- ❌ Syntax → Hukm

**Law**: No layer may claim outputs of a later layer

---

## Result Contract (العقد المخرج)

### Result (النتيجة)

**Definition**: The ONLY permitted output type.

**Type**: `Result[T]` (see `src/fvafk/algebra/core.py`)

**6 Required Fields**:
1. `value: T` - The actual output
2. `rank: Rank` - Epistemic status
3. `evidence: FrozenSet[Evidence]` - Supporting observations
4. `residuals: FrozenSet[Residual]` - Unresolved items
5. `failures: FrozenSet[Failure]` - Contradictions
6. `trace: Trace` - Provenance record

**4 Invariants** (enforced at construction):
1. LICENSED/CERTIFIED require evidence
2. CERTIFIED forbids residuals
3. Fatal failure forces REFUTED
4. Implementation failures cannot appear in successful residuals (after PR-F1)

**Law**: لا مخرج عارٍ (No bare output)

---

## Typography Conventions

**When Writing Documentation**:
- Use **"Arabic as revealing model"** not "Arabic proves the mind"
- Use **"governed binding"** not "free association"
- Use **"current implementation"** vs **"target architecture"**
- Use **"5/13 layers"** not "General Cognitive Algebra" (without qualification)
- Use **"research implementation"** not "production tool"
- Use **"boundary guards"** not "semantic understanding"
- Use **"foundation hardening"** not "minor fixes"

**When Writing Code**:
- Use typed dataclasses with `frozen=True`
- Use `FrozenSet` for immutable collections
- Use explicit enums for states
- Use `@abstractmethod` for contracts
- Use descriptive variable names (no abbreviations)
- Use full docstrings with type annotations

---

**Last Updated**: 2026-05-23 (PR-F0)
