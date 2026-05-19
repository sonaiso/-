# Seed Knowledge-Base Files

This directory contains minimal seed JSON files used by Stage 8B (Verb Bab / Governance) and Stage 8C (Valency Matrix) tests and loaders.  
**These are seed-only datasets** — not exhaustive dictionaries. They provide just enough entries to satisfy the unit and smoke tests.

---

## `verb_abwab.json`

**Schema:** `{ "<triliteral-root>": "<bab-string>" }`

Maps a normalized triliteral root to one of the six canonical bab (past-present pattern) values:

| Root | Bab |
|------|-----|
| ضرب  | فَعَلَ-يَفْعِلُ |
| رسم  | فَعَلَ-يَفْعُلُ |
| نفع  | فَعَلَ-يَفْعَلُ |
| فرح  | فَعِلَ-يَفْعَلُ |
| قرب  | فَعُلَ-يَفْعُلُ |
| حسب  | فَعِلَ-يَفْعِلُ |

**Note:** `ظلم` is intentionally absent so that tests asserting `bab=unknown` for unsupported roots remain green.

Loaded by `src/orchestrator/l8b_verb_bab_governance.py` → `_load_abwab_kb()`.

---

## `valency_seed.json`

**Schema:** JSON array of objects with fields:

```json
{
  "root": "<triliteral-root>",
  "class": "<valency-class>",
  "required_roles": ["<role>", ...],
  "optional_roles": ["<role>", ...]
}
```

Supported `class` values: `transitive_one_object`, `intransitive_basic`, `intransitive_prepositional`, `double_object`.

Loaded by `src/orchestrator/valency/loader.py` → `load_valency_kb()`.

---

## `verb_governance.json`

**Schema:** `{ "<lemma>": { <entry> } }`

Each entry supports:

| Field | Type | Description |
|-------|------|-------------|
| `governance_family` | string | e.g. `basic_transitive`, `intransitive_basic`, `intransitive_prepositional`, `double_object`, `mental_verb`, `transformational_verb` |
| `transitivity` | string | `متعدي` or `لازم` |
| `objects` | int | Expected object count (0, 1, or 2) |
| `prepositional_required` | bool | Whether a preposition is obligatory |
| `required_prepositions` | list of strings | e.g. `["على"]`, `["إلى"]` |
| `special_class` | string | e.g. `أفعال القلوب`, `أفعال التحويل` |

Loaded by `src/orchestrator/l8b_verb_bab_governance.py` → `_load_kb()` and also by `src/orchestrator/verb_governance.py` → `load_verb_governance()`.

---

## Extending the seed data

To add more roots, append entries following the same schema.  
Do **not** add `ظلم` to `verb_abwab.json` — this would break tests that verify unknown-bab handling.
