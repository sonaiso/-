# مخطط قبول المعمارية | Architectural Admission Schema

**Status**: Operational Framework
**Version**: 1.0
**Date**: 2026-05-24
**Authority**: Derived from Minimal Sufficiency Constitution

---

## Purpose

This document provides the **operational schema** for admitting new architectural constructs into the General Algebra, ensuring compliance with the **Minimal Sufficiency Constitution**.

---

## 1. Admission Process Flow

```text
New Construct Proposal
    ↓
MinimalSufficiencyCheck (REQUIRED)
    ↓
Existing Construct Analysis
    ↓
Smallest Possible Form Determination
    ↓
Risk Assessment
    ↓
Decision: ADMIT | REDUCE | MERGE | REJECT
```

---

## 2. MinimalSufficiencyCheck Schema

Every PR proposing a new construct **MUST** include a completed `MinimalSufficiencyCheck` section.

### Template (YAML Format)

```yaml
MinimalSufficiencyCheck:
  # Basic Information
  new_construct: "<name of proposed construct>"
  construct_type:
    - case
    - specific_rule
    - general_rule
    - method_extension
    - new_gate
    - new_layer
    - new_domain

  # Necessity Justification
  why_needed:
    question: "What distinction can the current system NOT represent?"
    answer: "<specific, concrete answer with examples>"

  # Existing Alternatives Analysis
  existing_constructs_checked:
    - construct: "<existing construct 1>"
      why_insufficient: "<specific reason with evidence>"
      attempted_representation: "<what was tried>"
      what_failed: "<what was lost: trace/rank/residuals/noleap>"

    - construct: "<existing construct 2>"
      why_insufficient: "<specific reason with evidence>"
      attempted_representation: "<what was tried>"
      what_failed: "<what was lost: trace/rank/residuals/noleap>"

  # Minimality Analysis
  smallest_possible_form:
    proposed_type: "<one of: case, specific_rule, general_rule, method_extension, new_layer, new_domain>"
    justification: "<why this is the smallest sufficient form>"

    reduction_attempts:
      - attempted_form: "<simpler form tried>"
        why_failed: "<specific reason it failed>"

  # Functional Requirements
  does_it_prevent_forbidden_leap:
    answer: true/false
    which_leap: "<describe the forbidden leap>"
    existing_gate_insufficient: "<why existing gates don't prevent it>"

  does_it_preserve_trace:
    answer: true/false
    how: "<mechanism of trace preservation>"

  does_it_affect_rank_policy:
    answer: true/false
    impact: "<describe impact on rank>"

  does_it_create_new_residual_type:
    answer: true/false
    which_residual: "<name and description>"
    why_needed: "<why existing residuals insufficient>"

  # Inflation Risk Assessment
  explosion_risk:
    level: low | medium | high
    justification: "<detailed risk analysis>"

    proliferation_potential:
      similar_constructs_possible: <number>
      mitigation: "<how to prevent proliferation>"

    complexity_increase:
      cognitive_load: low | medium | high
      integration_cost: low | medium | high

  # Final Recommendation
  decision:
    outcome: admit | reduce_to_case | reduce_to_specific_rule | merge_with_existing | reject
    rationale: "<comprehensive justification>"

    if_admitted:
      integration_plan: "<how it integrates>"
      documentation_updates: ["<file 1>", "<file 2>"]
      test_coverage: "<test plan>"
```

---

## 3. Decision Matrix

| Condition | Decision | Action |
|-----------|----------|--------|
| Can be represented as **case** | REDUCE | Implement as case, not rule/layer |
| Can be represented as **specific rule** | REDUCE | Implement as specific rule, not general rule/layer |
| Can be **merged** with existing construct | MERGE | Extend existing construct instead |
| No existing construct sufficient + minimal form | ADMIT | Proceed with implementation |
| Violates minimal sufficiency | REJECT | Do not implement |

---

## 4. Admission Criteria

A new construct is admitted **if and only if**:

### Necessary Conditions (ALL must be true)

1. ✅ **No existing construct** can represent the required distinction
2. ✅ **Smallest possible form** has been determined
3. ✅ **Trace** is preserved
4. ✅ **Rank** policy is maintained or properly updated
5. ✅ **Residuals** are properly handled
6. ✅ **NoLeap** protection is maintained
7. ✅ **Explosion risk** is low or adequately mitigated

### Sufficient Conditions (AT LEAST ONE must be true)

1. ✅ Prevents a **forbidden leap** not prevented by existing gates
2. ✅ Enables **trace preservation** not possible with existing constructs
3. ✅ Introduces **essential distinction** for domain coherence
4. ✅ Implements **constitutional requirement** from governing documents

---

## 5. Checklist for PR Authors

Before submitting a PR with new architectural constructs:

- [ ] I have completed the `MinimalSufficiencyCheck` section
- [ ] I have checked at least 3 existing constructs for sufficiency
- [ ] I have attempted to reduce this to a case/specific rule
- [ ] I have justified why the smallest form is still insufficient
- [ ] I have assessed explosion risk and provided mitigation
- [ ] I have documented how trace is preserved
- [ ] I have documented impact on rank policy
- [ ] I have provided test coverage for NoLeap guards
- [ ] I have updated relevant architectural documentation
- [ ] I have provided examples of accepted and rejected cases

---

## 6. Checklist for PR Reviewers

When reviewing a PR with new architectural constructs:

- [ ] `MinimalSufficiencyCheck` is present and complete
- [ ] Existing constructs were genuinely checked
- [ ] Reduction attempts were sincere and documented
- [ ] Explosion risk assessment is realistic
- [ ] Trace preservation mechanism is sound
- [ ] Rank policy impact is understood
- [ ] NoLeap protection is verified with tests
- [ ] Decision rationale is convincing
- [ ] Integration plan is clear
- [ ] Documentation is updated

---

## 7. Common Anti-Patterns (Auto-Reject)

The following patterns result in **automatic rejection**:

### Anti-Pattern 1: "Useful But Not Necessary"
```yaml
# BAD
why_needed:
  answer: "It would be useful to have this feature"

# GOOD
why_needed:
  answer: "Without this, trace is lost when X transitions to Y, violating Supreme Law §3"
```

### Anti-Pattern 2: Insufficient Alternative Analysis
```yaml
# BAD
existing_constructs_checked:
  - construct: "ExistingGate"
    why_insufficient: "Doesn't handle this case"

# GOOD
existing_constructs_checked:
  - construct: "ExistingGate"
    why_insufficient: "Loses trace during X→Y transition"
    attempted_representation: "Tried wrapping in TracePreserver but rank conflation occurred"
    what_failed: "Rank policy §7 violated - ZANNI promoted to CERTAIN"
```

### Anti-Pattern 3: No Reduction Attempt
```yaml
# BAD
smallest_possible_form:
  proposed_type: "new_layer"
  justification: "Need a new layer"

# GOOD
smallest_possible_form:
  proposed_type: "new_layer"
  justification: "After attempting case→specific_rule→general_rule, none preserve trace"
  reduction_attempts:
    - attempted_form: "case"
      why_failed: "Cannot generalize across domain boundary"
    - attempted_form: "specific_rule"
      why_failed: "Requires cross-layer composition not expressible in rules"
```

### Anti-Pattern 4: Vague Risk Assessment
```yaml
# BAD
explosion_risk:
  level: low
  justification: "Should be fine"

# GOOD
explosion_risk:
  level: medium
  justification: "Similar pattern could apply to 3 other domains, but constitutional §4.2 limits to evidence-based domains only"
  proliferation_potential:
    similar_constructs_possible: 3
    mitigation: "Documented in constitution that this pattern applies only where evidence-tracing is required"
```

---

## 8. Examples

### Example 1: REJECTED - Unnecessary Layer

```yaml
MinimalSufficiencyCheck:
  new_construct: "StyleAnalysisLayer"
  construct_type: new_layer

  why_needed:
    answer: "To analyze literary style"

  existing_constructs_checked:
    - construct: "RhetoricalGates"
      why_insufficient: "Doesn't have style analysis"

  decision:
    outcome: reject
    rationale: "No evidence that existing RhetoricalGates cannot represent style distinctions. No trace preservation requirement demonstrated. Violates Const. §4.1"
```

### Example 2: REDUCED - Layer to Specific Rule

```yaml
MinimalSufficiencyCheck:
  new_construct: "MetaphorDetectionLayer"
  construct_type: new_layer

  why_needed:
    answer: "To detect metaphorical usage"

  existing_constructs_checked:
    - construct: "DalalalGates"
      why_insufficient: "Handles literal meaning only"
      attempted_representation: "Tried adding metaphor case"
      what_failed: "Nothing - it worked"

  smallest_possible_form:
    proposed_type: "specific_rule"
    justification: "Can be implemented as specific rule in DalalalGates"

  decision:
    outcome: reduce_to_specific_rule
    rationale: "Metaphor detection is a specific_rule within existing Dalalah domain. Add as MajazDetectionRule, not new layer. Complies with Const. §4.3"
```

### Example 3: ADMITTED - Necessary Gate

```yaml
MinimalSufficiencyCheck:
  new_construct: "NameRealitySubGate"
  construct_type: new_gate

  why_needed:
    answer: "Prevents name→reality usurpation which existing gates don't block"

  existing_constructs_checked:
    - construct: "RealityTypeGate"
      why_insufficient: "Works on reality candidates, not name→reality transition"
      attempted_representation: "Tried pre-filtering names"
      what_failed: "Trace lost - cannot track which names were rejected vs admitted"

    - construct: "DomainGate"
      why_insufficient: "Operates on domain level, not name-referent binding"
      attempted_representation: "Tried domain-scoped name filtering"
      what_failed: "NoLeap violation - jumps from name to domain without referent candidate"

  smallest_possible_form:
    proposed_type: "new_gate"
    justification: "Cannot reduce to case/rule - requires gate-level trace preservation and cross-domain composition"
    reduction_attempts:
      - attempted_form: "specific_rule"
        why_failed: "Rule cannot maintain trace across Prior Information→Name→Reality path"

  does_it_prevent_forbidden_leap:
    answer: true
    which_leap: "name→reality without referent candidate + domain + evidence"
    existing_gate_insufficient: "No existing gate governs name-to-reality transition"

  explosion_risk:
    level: low
    justification: "Only one Name-Reality transition point. Cannot proliferate to other usurpations (those have separate gates)"

  decision:
    outcome: admit
    rationale: "Necessary gate preventing documented usurpation. Minimal form. Low explosion risk. Complies with Const. §2.1 and §4.4"
```

---

## 9. Integration with PR Template

The PR template must include:

```markdown
## Minimal Sufficiency Check

**REQUIRED for PRs adding new constructs (layers, gates, rules, domains)**

Complete the following or provide justification for exemption:

```yaml
MinimalSufficiencyCheck:
  new_construct: ""
  # ... (full template here)
```

**Exemption criteria**: Bug fixes, documentation updates, test additions, refactoring without new constructs.
```

---

## 10. Automated Validation

The `check_architectural_admission.py` tool validates:

1. ✅ `MinimalSufficiencyCheck` section present (if new construct detected)
2. ✅ All required fields completed
3. ✅ At least 2 existing constructs checked
4. ✅ At least 1 reduction attempt documented (if not a case)
5. ✅ Risk level justified
6. ✅ Decision rationale non-empty
7. ✅ If admitted: integration plan present

**Validation failure** = **PR cannot merge**

---

## 11. Authority Chain

```text
Minimal Sufficiency Constitution (Supreme Law)
    ↓
Architectural Admission Schema (Operational Law)
    ↓
PR Template (Enforcement Mechanism)
    ↓
check_architectural_admission.py (Automated Validation)
    ↓
Test Suite (Verification)
```

---

## 12. Revision Process

This schema can be revised **only if**:

1. Constitutional violation is discovered
2. Inflation has occurred despite schema
3. Legitimate construct repeatedly rejected incorrectly
4. New supreme law requires schema update

Revisions require:
- Documented constitutional basis
- Evidence of schema failure
- Proposed fix with test cases
- Review by constitutional authority

---

**End of Schema**

**Version**: 1.0
**Last Updated**: 2026-05-24
