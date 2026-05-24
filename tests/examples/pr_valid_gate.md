# Test PR: Valid Minimal Sufficiency Check (Should PASS)

## Type of Change
- [x] **New Architectural Construct**

## Description
This PR adds NameRealitySubGate to prevent name→reality usurpation.

```yaml
MinimalSufficiencyCheck:
  new_construct: "NameRealitySubGate"
  construct_type: new_gate

  why_needed:
    question: "What distinction can the current system NOT represent?"
    answer: "Prevents name→reality usurpation which existing gates don't block. Without this, names can claim reality without referent candidate, domain, or evidence, violating Supreme Law §3."

  existing_constructs_checked:
    - construct: "RealityTypeGate"
      why_insufficient: "Works on reality candidates, not name→reality transition"
      attempted_representation: "Tried pre-filtering names before RealityTypeGate"
      what_failed: "Trace lost - cannot track which names were rejected vs admitted during transition"

    - construct: "DomainGate"
      why_insufficient: "Operates on domain level, not name-referent binding"
      attempted_representation: "Tried domain-scoped name filtering"
      what_failed: "NoLeap violation - jumps from name to domain without intermediate referent candidate"

    - construct: "PriorInformationGate"
      why_insufficient: "Handles prior information admission, not name-reality binding"
      attempted_representation: "Tried encoding names as prior information"
      what_failed: "Rank conflation - names and information have different rank policies"

  smallest_possible_form:
    proposed_type: "new_gate"
    justification: "Cannot reduce to case/rule - requires gate-level trace preservation and cross-domain composition"

    reduction_attempts:
      - attempted_form: "case"
        why_failed: "Each name type (mental/technical/metaphorical) requires different domain checks - cannot be single case"

      - attempted_form: "specific_rule"
        why_failed: "Rule cannot maintain trace across Prior Information→Name→Reality path or enforce domain requirements"

      - attempted_form: "general_rule"
        why_failed: "Requires gate-level residual tracking and rank degradation not expressible in rules"

  does_it_prevent_forbidden_leap:
    answer: true
    which_leap: "name→reality without referent candidate + domain + evidence"
    existing_gate_insufficient: "No existing gate governs name-to-reality transition. RealityTypeGate assumes reality candidate already exists. DomainGate doesn't enforce referent binding."

  does_it_preserve_trace:
    answer: true
    how: "Maintains trace through name-referent-domain-evidence chain. Each admission/rejection produces traceable result with source."

  does_it_affect_rank_policy:
    answer: true
    impact: "Adds rank degradation when domain/evidence missing. MENTAL/TECHNICAL/NORMATIVE without domain → BLOCKED. Missing evidence → CANDIDATE rank."

  does_it_create_new_residual_type:
    answer: true
    which_residual: "R-NAME-MISSING-REFERENT, R-NAME-MISSING-DOMAIN, R-NAME-METAPHOR-AS-EXTERNAL"
    why_needed: "Existing residuals don't cover name-specific failures. Need typed residuals for name usurpation patterns."

  explosion_risk:
    level: low
    justification: "Only one Name-Reality transition point in the system. This gate is sub-gate of PriorInformationGeometry, architecturally constrained."

    proliferation_potential:
      similar_constructs_possible: 0
      mitigation: "Each usurpation type (trace→certainty, form→meaning, structure→judgment) has separate gate per Closure Framework. Name-Reality is single bounded transition."

    complexity_increase:
      cognitive_load: low
      integration_cost: low

  decision:
    outcome: admit
    rationale: "Necessary gate preventing documented usurpation (name→reality). Smallest sufficient form after reduction attempts. Complies with Constitutional §2.1, §4.4. Low explosion risk with architectural constraints."

    if_admitted:
      integration_plan: "Integrates as sub-gate within PriorInformationGeometry per architectural correction. Not standalone gate."
      documentation_updates:
        - "MINIMAL_SUFFICIENCY_CONSTITUTION.md - Example 2"
        - "CLOSURE_GATE_MATRIX.md - Gate A.2"
        - "PR_P1_PRIOR_INFORMATION_GEOMETRY_SUMMARY.md"
      test_coverage: "140+ test cases covering all blocking conditions, golden dataset with 22 cases"
```

## Changes Made
- Added NameRealitySubGate within PriorInformationGeometry
- Added 10 typed residuals for name failures
- Added RealityType enum with 7 existence types
- Implemented 140+ tests with full NoLeap coverage

## Testing
- [x] Unit tests added (140+)
- [x] Integration tests passing (9/9)
- [x] NoLeap guards tested
- [x] Residual handling tested
- [x] Golden dataset created (22 cases)

## Expected Result
**SHOULD PASS** because:
1. 3 existing constructs thoroughly analyzed
2. 3 reduction attempts documented with specific failures
3. Clear necessity justification (prevents usurpation, not just "useful")
4. Low explosion risk with mitigation
5. Complete trace/rank/residual handling
6. Complies with Minimal Sufficiency Constitution
