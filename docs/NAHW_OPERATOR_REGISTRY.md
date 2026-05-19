# NahwOperatorRegistry (PR #15)

## Position in the chain

```
MufradProof
→ PreSyntaxMufradVector
→ SentenceFrameCandidate
→ CaseSignMatrix
→ OperatorTriggerPotential
→ NahwOperatorRegistry              ← this layer
→ [future] OperatorCandidate
         → RelationCandidate
         → CaseEffectCandidate
         → ParseCompetition
         → MurakkabProof
```

The registry is the **second** layer that approaches operators. Its job
is exactly **one** thing:

> Take an `OperatorTriggerPotential` and return, per triggered family,
> the typed `NahwOperatorEntry` records documenting which operators
> *belong to* that family.

It does **not** apply operators, resolve competing entries, produce
relations, assign syntax roles, or produce case effects.

## Inputs

```python
registry = build_default_nahw_operator_registry()

# Family-keyed lookup:
entries = registry.entries_for_family(
    OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY,
)

# Trigger-keyed lookup (preferred):
results = registry.entries_for_trigger(trigger)
```

`entries_for_trigger` requires an `OperatorTriggerPotential`. Anything
else raises `TypeError`.

## Output

### `NahwOperatorEntry`

One documented operator entry. All fields are typed; strings are
forbidden in `family`, `expected_relation_families`,
`case_effect_policy_families`, `activation_conditions`, and
`blocking_conditions`.

| Field                          | Type                                       | Purpose                                                                          |
| ------------------------------ | ------------------------------------------ | -------------------------------------------------------------------------------- |
| `operator_id`                  | `str`                                      | Stable unique id (e.g. `"INNA"`, `"HARF_JARR_MIN"`).                             |
| `display_name_ar`              | `str`                                      | Arabic display name.                                                              |
| `source`                       | `OperatorSource`                           | Textual source: `QURAN`, `HADITH`, `KALAAM_ARAB`, `KITAB_SIBAWAYH`, …            |
| `school`                       | `NahwSchool`                               | `BASRI`, `KUFI`, `BAGHDADI`, `ANDALUSI`, `SHARED`, `UNATTRIBUTED`.               |
| `rank`                         | `LughaRank`                                | Attestation rank.                                                                |
| `family`                       | `OperatorTriggerFamily`                    | Lookup key.                                                                       |
| `input_signature`              | `OperatorInputSignature`                   | Expected arity + neighbour-type labels. **Descriptive, not verified here.**      |
| `activation_conditions`        | `tuple[ActivationCondition, ...]`          | Typed descriptive conditions.                                                     |
| `blocking_conditions`          | `tuple[BlockingCondition, ...]`            | Typed descriptive conditions.                                                     |
| `expected_relation_families`   | `tuple[ExpectedRelationFamily, ...]`       | Kind of relation expected to be invoked later (`ISN_LIKE`, `IDAFA_LIKE`, …).     |
| `case_effect_policy_families`  | `tuple[CaseEffectPolicyFamily, ...]`       | Kind of case-effect policy expected later (`JARR_POLICY_FAMILY`, …).             |
| `citations`                    | `tuple[Citation, ...]`                     | Textual citations.                                                                |
| `entry_residuals`              | `tuple[Residual, ...]`                     | Entry-level notes (school disagreement, irregularity, …).                        |
| `entry_trace_id`               | `str`                                      | Internal trace id.                                                                |

### `OperatorRegistryLookupResult`

One per family present in `trigger.triggered_families`:

| Field                 | Type                                  | Purpose                                                                       |
| --------------------- | ------------------------------------- | ----------------------------------------------------------------------------- |
| `trigger_id`          | `str`                                 | Equals `trigger.trigger_id`.                                                  |
| `frame_id`            | `str`                                 | Equals `trigger.frame_id`.                                                    |
| `matrix_id`           | `str`                                 | Equals `trigger.matrix_id`.                                                   |
| `family`              | `OperatorTriggerFamily`               | The family this lookup is for.                                                |
| `matched_entries`     | `tuple[NahwOperatorEntry, ...]`       | Every entry registered for the family. May be empty.                          |
| `rank`                | `LughaRank`                           | `trigger.rank` (never raised).                                                |
| `inherited_residuals` | `tuple[Residual, ...]`                | **Superset** of `trigger.get_all_residuals()`.                                |
| `lookup_residuals`    | `tuple[Residual, ...]`                | Registry-level info / warning residuals (never blockers).                     |

## Bright lines (what this layer must **never** do)

1. No `OperatorCandidate`, no `operator_binding`, no `apply`/`bind`/`resolve`/`choose`.
2. No `RelationCandidate`, no `relation_type`, no ISN/TADMN/TAQYID resolution.
3. No `CaseEffect`, no `marfoo_by`/`mansub_by`/`majroor_by`/`majzum_by`/`governed_by`.
4. No syntax roles (`faail`, `mafool`, `mubtada`, `khabar`, `mudaf`, `mudaf_ilayh`).
5. No meaning (`meaning`, `madlul`, `murad`, `haqiqa`, `majaz`).
6. No suppression of competing entries inside a family.
7. No suppression of competing families across trigger lookup.

These are enforced by:

- Field-name guard inside `__post_init__` (both `NahwOperatorEntry` and `OperatorRegistryLookupResult`).
- Typed-Enum guards on every metadata field; strings raise `TypeError`.
- No `apply` / `bind` / `resolve` / `choose` / `select` / `rank_entries`
  method on the registry (verified by introspection test).
- `lookup_residuals` are info or warning only — never blockers.

## The no-suppression invariants

### Inside one family

`POSSIBLE_NASIKH_INNA_FAMILY` has six seed entries (`INNA`, `ANNA`,
`KAANNA`, `LAKINNA`, `LAYTA`, `LAALLA`). The lookup returns **all six**
and emits a `REGISTRY_FAMILY_HAS_MULTIPLE_ENTRIES_PRESERVED` info
residual. The registry NEVER picks one.

### Across families

For `إنّ الكتابَ` (NASIKH_INNA + IBTIDAA both triggered), the registry
emits two `OperatorRegistryLookupResult`s — one per family — neither
dropped. This is the cross-layer extension of the PR #14 "competing
families preserved" invariant.

## IDAFA is construction-trigger only

The `IDAFA_CONSTRUCTION_OPERATOR` entry carries:

```python
expected_relation_families = (ExpectedRelationFamily.IDAFA_LIKE,)
case_effect_policy_families = (CaseEffectPolicyFamily.NO_CASE_EFFECT_POLICY_FAMILY,)
```

It does **not** assert any jarr-policy on the mudaf-ilayh. The case
effect of the mudaf-ilayh belongs to a later layer
(`OperatorCandidate` / `CaseEffectCandidate`).

## Family → entries table (seed)

| Family                                  | Seed entries                                                            |
| --------------------------------------- | ----------------------------------------------------------------------- |
| `POSSIBLE_JARR_OPERATOR_FAMILY`         | `HARF_JARR_MIN`, `…_ILA`, `…_AN`, `…_FI`, `…_BA`, `…_LAM`, `…_KAF`, `…_ALA` |
| `POSSIBLE_NASB_OPERATOR_FAMILY`         | `AN_MASDARIYYA`, `LAN`, `KAY`, `IDHAN`                                  |
| `POSSIBLE_JAZM_OPERATOR_FAMILY`         | `LAM_JAAZIMA`, `LAMMA`, `LA_NAHIYA`, `LAM_AMR`                          |
| `POSSIBLE_NASIKH_INNA_FAMILY`           | `INNA`, `ANNA`, `KAANNA`, `LAKINNA`, `LAYTA`, `LAALLA`                  |
| `POSSIBLE_NASIKH_LA_LILJINS_FAMILY`     | `LA_NAFI_LILJINS`                                                       |
| `POSSIBLE_NIDA_FAMILY`                  | `YA`, `AYYUHA`, `AYYATUHA`, `HAYYA`                                     |
| `POSSIBLE_ATF_FAMILY`                   | `WAW_ATF`, `FA_ATF`, `THUMMA`, `AW`, `AM`                               |
| `POSSIBLE_NAFI_FAMILY`                  | `MA_NAFIYA`, `LA_NAFIYA`, `LAYSA`                                       |
| `POSSIBLE_ISTIFHAM_FAMILY`              | `HAL`, `HAMZA_ISTIFHAM`, `MAN`, `MA_ISTIFHAM`, `KAYFA`, `AYNA`, `MATA`  |
| `POSSIBLE_VERBAL_GOVERNANCE_FAMILY`     | `FIIL_GOVERNANCE_GENERIC` (family-level entry)                          |
| `POSSIBLE_IBTIDAA_FAMILY`               | `IBTIDAA_OPERATOR` (abstract ma'nawi operator)                          |
| `POSSIBLE_IDAFA_FAMILY`                 | `IDAFA_CONSTRUCTION_OPERATOR` (construction-trigger only)               |
| `UNRESOLVED_TRIGGER`                    | *(none — by design)*                                                    |

## Pipeline integration

`NahwOperatorRegistry` is **opt-in only**, like the trigger layer above
it. It is not invoked by `pipeline.analyze_dal_mufrad`. The mufrad
pipeline still ends at lexical sign closure (`DMufrad`); the
frame / matrix / trigger / registry layers compose on top of it
explicitly when the caller needs them.

## What a PR #15 implementation **is allowed** to claim

```text
dal_core can look up typed NahwOperatorEntry candidates from an
OperatorTriggerPotential via NahwOperatorRegistry, preserving competing
entries and competing families.
```

## What a PR #15 implementation **must not** claim

```text
dal_core applies nahw operators.
dal_core produces OperatorCandidate.
dal_core produces RelationCandidate.
dal_core produces CaseEffect / CaseEffectCandidate.
dal_core resolves competing operators.
dal_core performs i'rab.
dal_core assigns syntactic roles
  (faail / mafool / mubtada / khabar / mudaf / mudaf_ilayh).
```

## Next stage (PR #16, proposed)

`OperatorCandidate`: consumes `(OperatorTriggerPotential, NahwOperatorRegistry)` and
emits per-frame typed candidate operators with `activation_conditions`
**evaluated**, `blocking_conditions` **evaluated**, and binding to
specific constituents proposed (still without resolution). Resolution
belongs to the later `ParseCompetition` stage.
