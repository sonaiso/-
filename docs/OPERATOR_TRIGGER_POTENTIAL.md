# OperatorTriggerPotential (PR #14)

## Position in the chain

```
MufradProof
→ PreSyntaxMufradVector
→ SentenceFrameCandidate
→ CaseSignMatrix
→ OperatorTriggerPotential          ← this layer
→ [future] NahwOperatorRegistry
         → OperatorCandidate
         → RelationCandidate
         → CaseEffectCandidate
         → ParseCompetition
         → MurakkabProof
```

The trigger layer is the **first** layer that begins to approach operators.
Its job is exactly **one** thing:

> Read a `(SentenceFrameCandidate, CaseSignMatrix)` pair and emit typed
> **candidate operator families** that *might* be invoked by a later
> operator stage.

It does **not** apply operators, produce relations, assign syntax roles,
or produce case effects.

## Inputs

```python
build_operator_trigger_potential(
    frame: SentenceFrameCandidate,
    matrix: CaseSignMatrix,
) -> OperatorTriggerPotential
```

Both inputs are required and **must share the same `frame_id`**. Anything
else raises `TypeError` / `ValueError`.

## Output

`OperatorTriggerPotential` carries:

| Field                 | Type                                  | Purpose                                                                                       |
| --------------------- | ------------------------------------- | --------------------------------------------------------------------------------------------- |
| `trigger_id`          | `str`                                 | Unique id (UUID-suffixed).                                                                    |
| `frame_id`            | `str`                                 | Must equal `matrix.frame_id`.                                                                 |
| `matrix_id`           | `str`                                 | Must equal `matrix.matrix_id`.                                                                |
| `triggered_families`  | `tuple[OperatorTriggerFamily, ...]`   | Deduplicated, insertion-ordered. Typed enum members only — never strings.                     |
| `sources`             | `tuple[TriggerSource, ...]`           | One source per fact (flat). The same family may appear in multiple sources without grouping.  |
| `rank`                | `LughaRank`                           | `min(matrix.rank, min source-row rank)`. Always `≤ matrix.rank ≤ frame.frame_rank`.           |
| `inherited_residuals` | `tuple[Residual, ...]`                | **Superset** of `matrix.get_all_residuals()`; residual inheritance theorem is preserved.       |
| `trigger_residuals`   | `tuple[Residual, ...]`                | Residuals raised at this stage only (competing-families info, matrix-blocker propagation, …). |
| `trace`               | `OperatorTriggerTrace`                | Recoverable backward to frame and matrix (and through them to MufradProofs).                  |

## Family table

| Family                                  | Fired by                                                                          |
| --------------------------------------- | --------------------------------------------------------------------------------- |
| `POSSIBLE_JARR_OPERATOR_FAMILY`         | constituent typed `ParticleTypeID.HARF_JARR`                                      |
| `POSSIBLE_NASB_OPERATOR_FAMILY`         | `ParticleTypeID.HARF_NASB`                                                        |
| `POSSIBLE_JAZM_OPERATOR_FAMILY`         | `ParticleTypeID.HARF_JAZM`                                                        |
| `POSSIBLE_NASIKH_INNA_FAMILY`           | `ParticleTypeID.HARF_NASIKH_INNA`                                                 |
| `POSSIBLE_NASIKH_LA_LILJINS_FAMILY`     | `ParticleTypeID.HARF_NASIKH_LA_NAFI_LILJINS`                                      |
| `POSSIBLE_NIDA_FAMILY`                  | `ParticleTypeID.HARF_NIDA`                                                        |
| `POSSIBLE_ATF_FAMILY`                   | `ParticleTypeID.HARF_ATF`                                                         |
| `POSSIBLE_NAFI_FAMILY`                  | `ParticleTypeID.HARF_NAFI`                                                        |
| `POSSIBLE_ISTIFHAM_FAMILY`              | `ParticleTypeID.HARF_ISTIFHAM`                                                    |
| `POSSIBLE_VERBAL_GOVERNANCE_FAMILY`     | `VerbalFrameCandidate` (fired once on `verb_index`)                               |
| `POSSIBLE_IBTIDAA_FAMILY`               | `NominalFrameCandidate` (fired once on `lead_noun_index`) — **never suppressed**  |
| `POSSIBLE_IDAFA_FAMILY`                 | adjacent ISM + ISM where second row has `JARR_COMPATIBLE` evidence                |
| `UNRESOLVED_TRIGGER`                    | unresolved frame, fragment with no rule firing, or empty fallback                 |

## Bright lines (what this layer must **never** do)

1. No `OperatorCandidate`, no `operator_id`, no operator binding.
2. No `RelationCandidate`, no `relation_type`, no ISN / TADMN / TAQYID resolution.
3. No `CaseEffect`, no `marfoo_by`/`mansub_by`/`majroor_by`/`majzum_by`/`governed_by`.
4. No syntax roles (`faail`, `mafool`, `mubtada`, `khabar`, `mudaf`, `mudaf_ilayh`, `naat`, `badal`, …).
5. No meaning (`meaning`, `madlul`, `murad`, `haqiqa`, `majaz`).
6. **No silent suppression of competing families**, even when one looks "stronger" than another.

These are enforced by:

- Field-name guard inside `__post_init__` (rejects any dataclass field with a forbidden name).
- Forbidden-token scan over every string field.
- Family typing: `triggered_families` and `TriggerSource.family` must be `OperatorTriggerFamily` enum members.

## The no-suppression invariant (PR #14 clarification #2)

If the same frame yields evidence for both:

```
POSSIBLE_NASIKH_INNA_FAMILY     (from HARF_NASIKH_INNA at index 0)
POSSIBLE_IBTIDAA_FAMILY         (from the lead ISM at index 1)
```

the trigger object emits **both** families and records a
`TRIGGER_COMPETING_FAMILIES_PRESERVED` info residual that explicitly names
the competing families. Resolution belongs to a later
`ParseCompetition` / `OperatorCandidate` stage, never to the trigger layer.

This invariant is also enforced structurally: constructing an
`OperatorTriggerPotential` whose `triggered_families` drops a family
attested by any `TriggerSource` raises `ValueError`.

## Idafa as construction trigger only (PR #14 clarification #1)

`POSSIBLE_IDAFA_FAMILY` says exactly:

> An adjacent `ISM` + `ISM` pattern with `JARR_COMPATIBLE` evidence on the
> second constituent may later trigger an idafa-family operator/relation
> candidate.

It does **not** assert that the first is `mudaf`, the second is
`mudaf_ilayh`, or that any idafa-relation / jarr-judgment holds. Those
claims are reserved for `RelationCandidate` / `CaseEffectCandidate`.

## Worked examples

### `في البيتِ` (HARF_JARR + ISM)

```python
trigger.triggered_families == (
    OperatorTriggerFamily.POSSIBLE_JARR_OPERATOR_FAMILY,
)
```

Sources: one, pointing at index 0 (the particle), with
`compatibility_evidence` containing `JARR_COMPATIBLE` for the noun's row.

### `إنَّ الكتابَ` (HARF_NASIKH_INNA + ISM in a nominal frame)

```python
set(trigger.triggered_families) == {
    OperatorTriggerFamily.POSSIBLE_NASIKH_INNA_FAMILY,
    OperatorTriggerFamily.POSSIBLE_IBTIDAA_FAMILY,
}
# Plus one TRIGGER_COMPETING_FAMILIES_PRESERVED info residual.
```

Both families are emitted (no suppression).

### `كَتَبَ الطالبُ الدرسَ` (verbal frame)

```python
trigger.triggered_families == (
    OperatorTriggerFamily.POSSIBLE_VERBAL_GOVERNANCE_FAMILY,
)
```

One source, on `verb_index`. The trigger does **not** attempt to identify
subject or object — that belongs to `OperatorCandidate` after consulting
verb valency.

## Inherited limitation (carry-over from PR #13)

Substitute signs (ALIF / WAW / YA / NUN_*) still resolve to
`CaseCompatibilityFamily.UNRESOLVED` in the matrix because
`NounInflectionClass` does not yet encode `DUAL / SOUND_MASC_PLURAL /
FIVE_NOUNS / AFAAL_KHAMSA` as values. The matrix's blocker residuals
(`SUBSTITUTE_SIGN_REQUIRES_INFLECTION_CLASS`,
`CASE_SIGN_COMPATIBILITY_UNRESOLVED`) propagate unchanged to
`trigger.inherited_residuals`, and the trigger layer additionally records
a per-family `TRIGGER_BLOCKED_BY_MATRIX_RESIDUAL` warning. A later PR
expanding `NounInflectionClass` will lift these blockers without changing
this layer's contract.

## Pipeline integration

`OperatorTriggerPotential` is **opt-in only**. It is **not** invoked by
`pipeline.analyze_dal_mufrad`. The mufrad pipeline still ends at lexical
sign closure (`DMufrad`); the frame / matrix / trigger layers compose on
top of it explicitly when the caller needs them.

## What a PR #14 implementation **is allowed** to claim

```text
dal_core can emit typed OperatorTriggerFamily candidates from
SentenceFrameCandidate + CaseSignMatrix.
```

## What a PR #14 implementation **must not** claim

```text
dal_core applies nahw operators.
dal_core produces CaseEffect.
dal_core resolves i'rab.
dal_core assigns syntax roles.
```
