# Golden Dataset Coverage Report (PR #29)

**Generated**: 2026-05-20

```
================================================================================
GOLDEN DATASET COVERAGE REPORT (PR #29 - Phase 2)
================================================================================

Dataset Version: 1.0.0
Created: 2026-05-20
Purpose: Comprehensive validation of 10-layer coverage framework from PR #28
Cross-Reference: docs/MUFRAD_COVERAGE_MATRIX.md

DATASET STATISTICS
--------------------------------------------------------------------------------
Clear Cases:      10
Residual Cases:    6
Edge Cases:       11
TOTAL CASES:      27

10-LAYER COVERAGE ANALYSIS
--------------------------------------------------------------------------------
Layer    Name                                     Cases    Coverage  
--------------------------------------------------------------------------------
K.1      Orthography                              27       100.0% ✅
K.2      Phonology                                27       100.0% ✅
K.3      Origin-Segmentation                      27       100.0% ✅
K.4      Template Transformation                  27       100.0% ✅
K.5      Verb Health                              27       100.0% ✅
K.6      Word Type Taxonomy                       27       100.0% ✅
K.7      Surface Forces                           27       100.0% ✅
K.8      Gender-Number-Definiteness               27       100.0% ✅
K.9      Event-Aspect-Transitivity                27       100.0% ✅
K.10     Lexicon-Attestation                      27       100.0% ✅

ATTESTATION RANK DISTRIBUTION
--------------------------------------------------------------------------------
QIYAS             1 cases (  3.7%)
TAWATUR          23 cases ( 85.2%)
ZERO              3 cases ( 11.1%)

THEOREM VERIFICATION COVERAGE
--------------------------------------------------------------------------------
Total Theorems Verified: 7

  • Theorem 3: D_form ⊄ D_lugha (Form domain is not subset of language domain)
    Test cases: 3
    IDs: satarab_unattested, shams_metaphorical_gender, rijaal_broken_plural...

  • Theorem 5: No meaning fields (dal_core is pre-semantic)
    Test cases: 4
    IDs: kataba_verb, kitaab_noun, min_particle...

  • Rank Hierarchy: Qiyas ≠ Sama' (Analogy ≠ Attestation)
    Test cases: 3
    IDs: kataba_verb, satarab_unattested, rijaal_broken_plural...

  • K.1-K.10 Layer Separation
    Test cases: 3
    IDs: qala_weak_verb, hamza_irregular, shadda_gemination...

  • Surface Forces (K.7): Jamid vs Mushtaq, Mabni vs Murab
    Test cases: 4
    IDs: kaatib_active_participle, rajul_noun, min_particle...

  • No Direct Cross-Layer Promotion
    Test cases: 1
    IDs: qala_weak_verb...

  • Lexicon Required for Sama' (K.10)
    Test cases: 3
    IDs: shams_metaphorical_gender, rijaal_broken_plural, satarab_unattested...

LAYER-SPECIFIC CONCEPT COVERAGE
--------------------------------------------------------------------------------
K.10: 18 cases covering 8 concepts
  Concepts: TAWATUR rank, AHAD rank, ZERO rank, Attested, Unattested...

K.1: 15 cases covering 8 concepts
  Concepts: Standard IMLA, Hamza variants, Taa marbuta, Alif maqsura, Diacritics...

K.2: 15 cases covering 5 concepts
  Concepts: CV syllables, CVV long vowels, CVC closed syllables, Gemination, Syllable count...

K.3: 13 cases covering 7 concepts
  Concepts: Trilateral roots, Quadrilateral roots, Augmentation, Prefixes, Suffixes...

K.4: 12 cases covering 5 concepts
  Concepts: Deep vs Surface, I'lal transformation, Verb patterns, Noun patterns, Augmented patterns...

K.5: 8 cases covering 5 concepts
  Concepts: Sound (صحيح), Weak middle (أجوف), Weak final (ناقص), Hamzated (مهموز), Doubled (مضعف)...

K.6: 18 cases covering 11 concepts
  Concepts: ISM, FIIL, HARF, ISM_FAIL, ISM_MAFOOL...

K.7: 15 cases covering 5 concepts
  Concepts: JAMID, MUSHTAQ, MABNI, MURAB, Four orthogonal forces...

K.8: 14 cases covering 9 concepts
  Concepts: Masculine, Feminine, Singular, Dual, Plural sound...

K.9: 10 cases covering 7 concepts
  Concepts: Perfective, Transitive, Masdar, Agent, Place...

INTEGRATION WITH PR #28 (Coverage Matrix)
--------------------------------------------------------------------------------
✅ All 10 layers from MUFRAD_COVERAGE_MATRIX.md are covered
✅ Layer-specific matrices referenced in dataset
✅ Gap analysis from PR #28 addressed with test cases
✅ Forbidden claims validated (no meaning/semantic fields)

RECOMMENDATIONS FOR PHASE 3
--------------------------------------------------------------------------------
1. Expand dataset to 100-200 words (currently: 27)
2. Increase coverage for layers with <50% (K.4, K.5, K.9)
3. Add more quadrilateral root examples (K.3)
4. Implement missing contracts identified in gaps
5. Create layer-specific golden test suites

================================================================================
END OF REPORT
================================================================================
```
