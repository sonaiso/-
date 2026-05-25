#!/usr/bin/env python3
"""Quick test for مَكْتَب ordered trace fix."""

import sys
sys.path.insert(0, "/home/runner/work/-/-/src")

from dal_core.u0_unicode_carrier import text_to_unicode_layer
from dal_core.u1_grapheme_carrier import unicode_to_grapheme_layer
from dal_core.u2p_phonetic_projection import grapheme_to_phonetic_layer
from dal_core.u2s_syllable_carrier import phonetic_to_syllable_layer

text = "مَكْتَب"
print(f"Testing: {text}\n")

# U₀
u0 = text_to_unicode_layer(text)
print(f"U₀: {len(u0.layer_object.units)} units (type={type(u0.layer_object.units).__name__})")
for i, unit in enumerate(u0.layer_object.units):
    print(f"  {i}: {unit.char} (pos={unit.position})")

# U₁
u1 = unicode_to_grapheme_layer(u0.layer_object)
print(f"\nU₁: {len(u1.layer_object.clusters)} clusters (type={type(u1.layer_object.clusters).__name__})")
for i, cluster in enumerate(u1.layer_object.clusters):
    print(f"  {i}: base={cluster.base} marks={cluster.marks}")

# U₂p
u2p = grapheme_to_phonetic_layer(u1.layer_object)
print(f"\nU₂p: {len(u2p.layer_object.projections)} projections (type={type(u2p.layer_object.projections).__name__})")
for i, proj in enumerate(u2p.layer_object.projections):
    print(f"  {i}: C={proj.consonant_candidate}, V={proj.short_vowel_candidate}, closure={proj.closure_candidate}")

# U₂s
u2s = phonetic_to_syllable_layer(u2p.layer_object)
print(f"\nU₂s: valid={u2s.valid}")
if u2s.layer_object:
    syllables = list(u2s.layer_object.syllables)
    print(f"Syllables: {len(syllables)}")
    for i, syll in enumerate(syllables):
        print(f"  {i}: {syll.pattern.value} - {syll.ordered_surface}")

    print(f"\nResiduals: {len(u2s.layer_object.total_residuals)}")
    for i, res in enumerate(list(u2s.layer_object.total_residuals)[:5]):
        print(f"  {i}: {res.severity.value} - {res.message}")

if u2s.valid:
    print(f"\n✓ SUCCESS: مَكْتَب syllabified correctly!")
else:
    print(f"\n✗ FAILED: Check residuals above")
