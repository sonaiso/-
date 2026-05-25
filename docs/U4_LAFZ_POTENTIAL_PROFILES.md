# U₄ Lafẓ Surface Potential Profiles

## Constitutional Law

**U₄-B describes surface. U₄-B opens guarded potentials. U₄-B does NOT certify.**

```
U₄-B يصف سطح اللفظ، ويفتح إمكانات محروسة، ولا يشهد بصرف ولا نحو ولا معنى ولا إحالة ولا عدد ولا زمن.
```

## Core Principle

U₄ identifies **potentials**, not **certainties**:
- Terminal patterns (not case)
- Definiteness capacity (not resolved reference)
- Quantity patterns (not counted reality)
- Verb surface (not tense)
- Path hints (not commitments)

## Surface Existence vs Surface Interpretation

**Critical Rule:**

```
Surface existence → boolean (allowed)
Surface interpretation → hint (required: "possible", "unlikely", "unresolved")
```

### Examples

**✅ Allowed (surface existence):**
- `has_tanwin_surface: bool`
- `has_al_surface: bool`
- `has_present_prefix_surface: bool`

**✅ Required (surface interpretation):**
- `verb_surface_hint: str`  (not `is_verb: bool`)
- `past_surface_hint: str`  (not `is_past: bool`)
- `dual_surface_hint: str`  (not `is_dual: bool`)

**❌ Forbidden (certificates):**
- `tense: Tense`
- `quantity: Quantity`
- `resolved_reference: Reference`
- `case_marking: CaseMarking`

## The Five Potential Profiles

### 1. TerminalProfile

```python
@dataclass(frozen=True)
class TerminalProfile:
    ending_surface: str                    # النهاية كما هي
    terminal_diacritic: Optional[str]      # الحركة الأخيرة
    has_tanwin_surface: bool               # سطح التنوين موجود
    has_sukun_surface: bool                # سكون موجود
    has_taa_marbutah_surface: bool         # تاء مربوطة موجودة
    has_long_vowel_terminal_surface: bool  # حرف مد نهائي
    mabni_surface_hint: str                # "possible" | "unlikely" | "unresolved"
    murab_surface_hint: str                # "possible" | "unlikely" | "unresolved"
    residuals: Tuple[str, ...]
```

**Responsibility:**
- U₄: Describe terminal surface patterns
- U₅+: Assign grammatical case/mood

**Forbidden:**
- `case_marking` (that's U₇+)
- `i3rab_status` (that's U₇+)
- `mood_marking` (that's U₇+)

### 2. DefinitenessSurfacePotential

```python
@dataclass(frozen=True)
class DefinitenessSurfacePotential:
    has_al_surface: bool                   # الـ موجود في السطح
    has_tanwin_surface: bool               # تنوين موجود في السطح
    has_attached_pronoun_surface: bool     # ضمير متصل موجود
    definite_surface_hint: str             # "possible" | "unlikely" | "unresolved"
    indefinite_surface_hint: str           # "possible" | "unlikely" | "unresolved"
    reference_surface_hint: str            # "possible" | "unlikely" | "unresolved"
    residuals: Tuple[str, ...]
```

**Responsibility:**
- U₄: Identify الـ, tanwīn, pronoun surfaces
- U₅+: Resolve reference (muḥaddad vs nākira)

**Forbidden:**
- `resolved_reference` (that's U₅+)
- `is_definite` (boolean certificate - use hint instead)
- `referent` (that's U₁₅)

### 3. QuantitySurfacePotential

```python
@dataclass(frozen=True)
class QuantitySurfacePotential:
    dual_surface_hint: str                 # "possible" | "unlikely" | "unresolved"
    plural_surface_hint: str               # "possible" | "unlikely" | "unresolved"
    singular_surface_hint: str             # "possible" | "unlikely" | "unresolved"
    number_word_surface_hint: str          # هل يبدو كرقم لفظي؟
    counted_object_surface_hint: str       # هل يبدو كمعدود؟
    residuals: Tuple[str, ...]
```

**Responsibility:**
- U₄: Identify dual/plural surface markers
- U₅+: Determine actual quantity

**Forbidden:**
- `quantity` (certified singular/dual/plural)
- `counted_entities` (that's U₁₅)

### 4. VerbSurfacePotential

```python
@dataclass(frozen=True)
class VerbSurfacePotential:
    verb_surface_hint: str                 # "possible" | "unlikely" | "unresolved"
    past_surface_hint: str                 # "possible" | "unlikely" | "unresolved"
    present_surface_hint: str              # "possible" | "unlikely" | "unresolved"
    imperative_surface_hint: str           # "possible" | "unlikely" | "unresolved"
    has_present_prefix_surface: bool       # يـ، تـ، أـ، نـ موجود
    has_verbal_suffix_surface: bool        # ـتَ، ـتُمْ، ـنَ موجود
    residuals: Tuple[str, ...]
```

**Responsibility:**
- U₄: Identify verb-like surface patterns
- U₅+: Determine tense/aspect/mood

**Forbidden:**
- `tense` (that's U₅+)
- `voice` (that's U₅+)
- `valency` (that's U₅+)
- `aspect` (that's U₅+)
- `mood` (that's U₅+)

### 5. DownstreamPathHints

```python
@dataclass(frozen=True)
class DownstreamPathHints:
    may_open_functional_role_path: bool
    may_open_closed_class_path: bool
    may_open_verb_candidate_path: bool
    may_open_noun_candidate_path: bool
    may_open_reference_path: bool
    may_open_quantity_path: bool
    blocked_paths: Tuple[str, ...]         # مسارات محظورة
```

**Responsibility:**
- U₄: Suggest possible paths for U₅+
- U₅+: Walk the paths with evidence

**Forbidden:**
- `pattern_family_hints` (too close to U₉)
- `root_hints` (U₈ territory)
- `weight_hints` (U₉ territory)

## Examples

### Example 1: كَتَبَ (Past Verb)

```python
TrueLafzUnit(
    surface="كَتَبَ",
    unit_type=TRUE_SINGULAR_CORE_CANDIDATE,

    terminal_profile=TerminalProfile(
        ending_surface="بَ",
        terminal_diacritic="َ",
        has_tanwin_surface=False,
        has_sukun_surface=False,
        mabni_surface_hint="unlikely",
        murab_surface_hint="unresolved"
    ),

    verb_surface_potential=VerbSurfacePotential(
        verb_surface_hint="possible",
        past_surface_hint="possible",
        present_surface_hint="unlikely",
        has_present_prefix_surface=False
    ),

    downstream_path_hints=DownstreamPathHints(
        may_open_verb_candidate_path=True,
        may_open_noun_candidate_path=False
    )
)
```

**Note:** NO `tense` field. Only `past_surface_hint="possible"`.

### Example 2: بِكِتَابٍ (Preposition + Indefinite Noun)

```python
# Unit 1: بِـ (BOUND_PROCLITIC)
TrueLafzUnit(
    surface="بِ",
    unit_type=BOUND_PROCLITIC,
    # No profiles for proclitics
)

# Unit 2: كِتَابٍ (TRUE_SINGULAR_CORE_CANDIDATE)
TrueLafzUnit(
    surface="كِتَابٍ",
    unit_type=TRUE_SINGULAR_CORE_CANDIDATE,

    terminal_profile=TerminalProfile(
        ending_surface="بٍ",
        terminal_diacritic="ٍ",
        has_tanwin_surface=True,
        has_sukun_surface=False
    ),

    definiteness_surface_potential=DefinitenessSurfacePotential(
        has_al_surface=False,
        has_tanwin_surface=True,
        definite_surface_hint="unlikely",
        indefinite_surface_hint="possible"
    )
)
```

**Note:** NO `resolved_reference` field. Only `indefinite_surface_hint="possible"`.

### Example 3: وَبِكِتَابِهِمْ (With Attached Pronoun)

```python
# Unit 3: كِتَابِ (TRUE_SINGULAR_CORE_CANDIDATE)
TrueLafzUnit(
    surface="كِتَابِ",
    unit_type=TRUE_SINGULAR_CORE_CANDIDATE,

    definiteness_surface_potential=DefinitenessSurfacePotential(
        has_al_surface=False,
        has_tanwin_surface=False,
        has_attached_pronoun_surface=False,  # Pronoun is separate unit
        reference_surface_hint="possible"    # Due to following pronoun
    )
)

# Unit 4: ـهِمْ (ATTACHED_PRONOUN_CANDIDATE)
TrueLafzUnit(
    surface="ـهِمْ",
    unit_type=ATTACHED_PRONOUN_CANDIDATE,
    # No profiles for pronouns
)
```

**Note:** NO `resolved_referent`. Only `reference_surface_hint="possible"`.

### Example 4: فَسَيَكْتُبُونَهَا (Future Verb)

```python
# Unit 3: يَكْتُبُونَ (TRUE_SINGULAR_CORE_CANDIDATE)
TrueLafzUnit(
    surface="يَكْتُبُونَ",
    unit_type=TRUE_SINGULAR_CORE_CANDIDATE,

    verb_surface_potential=VerbSurfacePotential(
        verb_surface_hint="possible",
        past_surface_hint="unlikely",
        present_surface_hint="possible",  # NOT "future"!
        has_present_prefix_surface=True
    ),

    quantity_surface_potential=QuantitySurfacePotential(
        plural_surface_hint="possible",    # ـون marker
        singular_surface_hint="unlikely"
    )
)
```

**Note:** سَـ is separate proclitic. U₄ doesn't certify "future", only "present_surface".

### Example 5: كَاتِب (Active Participle)

```python
TrueLafzUnit(
    surface="كَاتِب",
    unit_type=TRUE_SINGULAR_CORE_CANDIDATE,

    verb_surface_potential=VerbSurfacePotential(
        verb_surface_hint="unresolved",    # Could be noun or verb
        has_present_prefix_surface=False
    ),

    downstream_path_hints=DownstreamPathHints(
        may_open_verb_candidate_path=True,
        may_open_noun_candidate_path=True  # Ambiguous
    )
)
```

**Note:** NO `weight` field. NO `pattern` field. Only hints.

### Example 6: مَكْتَب (Noun of Place)

```python
TrueLafzUnit(
    surface="مَكْتَب",
    unit_type=TRUE_SINGULAR_CORE_CANDIDATE,

    verb_surface_potential=VerbSurfacePotential(
        verb_surface_hint="unlikely",
        has_present_prefix_surface=False
    ),

    downstream_path_hints=DownstreamPathHints(
        may_open_verb_candidate_path=False,
        may_open_noun_candidate_path=True
    )
)
```

**Note:** NO `weight` field. NO `pattern` field. Only hints.

## U₄ Complete Status

After U₄-B implementation:

```
U₀ Unicode ✅
U₁ Grapheme ✅
U₂p PhoneticProjection ✅
U₂s ArabicSyllable ✅
U₃ BoundaryAndAttachment ✅
U₄ TrueSingularLafẓ ✅ COMPLETE
  ├─ A: Eligibility Classification ✅
  └─ B: Surface Potential Profiles ✅
U₅ FunctionalRole ⏸ (ready to start)
```

## Forbidden Fields List

U₄ MUST NOT contain:

### Morphological (U₈/U₉)
- `root`
- `weight`
- `pattern`

### Semantic (U₁₅)
- `meaning`
- `dalalah`
- `ifadah`
- `haqiqa_majaz`

### Syntactic (U₇+)
- `hukm`
- `i3rab_status`
- `case_marking`
- `mood_marking`

### Reference (U₅+)
- `resolved_reference`
- `referent`

### Quantity (U₅+)
- `quantity` (certified)
- `counted_entities`

### Verbal (U₅+)
- `tense`
- `voice`
- `valency`
- `aspect`

## Testing

See `tests/dal_core/test_u4_lafz_potentials.py` for:

1. **Prohibition tests** (6 tests)
   - Verify no forbidden fields
   - Verify hints are strings, not booleans

2. **Golden cases** (6 tests)
   - كَتَبَ
   - بِكِتَابٍ
   - وَبِكِتَابِهِمْ
   - فَسَيَكْتُبُونَهَا
   - كَاتِب
   - مَكْتَب

## Summary

**U₄-B Achievement:**

```
✅ Describes surface
✅ Opens guarded potentials
✅ Preserves trace/residuals
✅ No forbidden fields
✅ Hints, not certificates
✅ Ready for U₅
```

**Constitutional Compliance:**

```
U₄-B لا يحلل.
U₄-B لا يشهد.
U₄-B لا يقرر.
U₄-B يصف سطح اللفظ ويفتح إمكانات محروسة فقط.
```
