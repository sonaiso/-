"""Anti-promotion tests for D1 (SYLLABIC domain).

Critical tests to prevent cross-layer leakage.

D1 must NOT contain or claim:
- Root (D3 domain)
- Wazn/Pattern (D4 domain)
- Ism/Fi'l/Harf classification (D5 domain)
- Meaning/Murad (semantic layer)
- Any morphological judgment

These tests enforce the architectural law:
"No algebra may claim outputs of later algebra"
"""

import pytest
from dal_core.syllable_candidate import (
    SyllableCandidate,
    generate_syllable_candidates
)
from dal_core.atoms import ArabicAtom, classify_carrier
from dal_core.carriers import make_carrier
from dal_core.dal_algebra import DalTransitionDomain


class TestD1AntiPromotion:
    """Test that D1 doesn't promote to higher layers."""

    def test_syllable_candidate_does_not_claim_root(self):
        """D1 must NOT claim root (D3 domain).

        Root extraction is D3 (ORIGIN) domain responsibility.
        D1 deals only with syllable structure.
        """
        candidate = SyllableCandidate()

        # Verify no root field
        assert not hasattr(candidate, 'root'), \
            "D1 SyllableCandidate must NOT have 'root' field (D3 domain)"

        assert not hasattr(candidate, 'jidhr'), \
            "D1 SyllableCandidate must NOT have 'jidhr' field (root in Arabic)"

        assert not hasattr(candidate, 'radicals'), \
            "D1 SyllableCandidate must NOT have 'radicals' field"

    def test_syllable_candidate_does_not_claim_wazn(self):
        """D1 must NOT claim wazn/pattern (D4 domain).

        Pattern matching is D4 (TEMPLATE) domain responsibility.
        D1 deals only with syllable patterns (CV, CVC), not morphological patterns.
        """
        candidate = SyllableCandidate()

        # Verify no wazn field
        assert not hasattr(candidate, 'wazn'), \
            "D1 SyllableCandidate must NOT have 'wazn' field (D4 domain)"

        assert not hasattr(candidate, 'pattern'), \
            "D1 SyllableCandidate must NOT have morphological 'pattern' field (D4 domain)"

        assert not hasattr(candidate, 'template'), \
            "D1 SyllableCandidate must NOT have 'template' field (D4 domain)"

        assert not hasattr(candidate, 'mold'), \
            "D1 SyllableCandidate must NOT have 'mold' field"

    def test_syllable_candidate_does_not_claim_meaning(self):
        """D1 must NOT claim semantic meaning.

        Meaning is semantic layer responsibility (beyond dal_algebra).
        D1 is pure form analysis.
        """
        candidate = SyllableCandidate()

        # Verify no meaning fields
        assert not hasattr(candidate, 'meaning'), \
            "D1 SyllableCandidate must NOT have 'meaning' field"

        assert not hasattr(candidate, 'murad'), \
            "D1 SyllableCandidate must NOT have 'murad' field (intended meaning)"

        assert not hasattr(candidate, 'haqiqa_majaz'), \
            "D1 SyllableCandidate must NOT have 'haqiqa_majaz' field (literal/metaphorical)"

        assert not hasattr(candidate, 'semantics'), \
            "D1 SyllableCandidate must NOT have 'semantics' field"

    def test_syllable_candidate_does_not_claim_identity_axis(self):
        """D1 must NOT claim Ism/Fi'l/Harf classification (D5 domain).

        Identity axis determination is D5 (IDENTITY_AXIS) domain responsibility.
        D1 cannot determine if syllable belongs to noun/verb/particle.
        """
        candidate = SyllableCandidate()

        # Verify no identity axis fields
        assert not hasattr(candidate, 'ism'), \
            "D1 SyllableCandidate must NOT have 'ism' field (D5 domain)"

        assert not hasattr(candidate, 'fil'), \
            "D1 SyllableCandidate must NOT have 'fil' field (D5 domain)"

        assert not hasattr(candidate, 'harf'), \
            "D1 SyllableCandidate must NOT have 'harf' field (D5 domain)"

        assert not hasattr(candidate, 'word_class'), \
            "D1 SyllableCandidate must NOT have 'word_class' field (D5 domain)"

        assert not hasattr(candidate, 'pos'), \
            "D1 SyllableCandidate must NOT have 'pos' (part-of-speech) field (D5 domain)"

    def test_syllable_candidate_does_not_promote_to_premorph(self):
        """D1 must NOT skip to D2 (PRE_MORPH) domain.

        D2 requires explicit transition from D1.
        No direct syllable → morpheme promotion.
        """
        candidate = SyllableCandidate()

        # Verify domain is exactly SYLLABIC
        assert candidate.domain == DalTransitionDomain.SYLLABIC, \
            "D1 candidate must have SYLLABIC domain, not PRE_MORPH or higher"

        # Verify no pre-morph fields
        assert not hasattr(candidate, 'morpheme'), \
            "D1 SyllableCandidate must NOT have 'morpheme' field (D2 domain)"

        assert not hasattr(candidate, 'affix'), \
            "D1 SyllableCandidate must NOT have 'affix' field (D2 domain)"

        assert not hasattr(candidate, 'stem'), \
            "D1 SyllableCandidate must NOT have 'stem' field (D2 domain)"

    def test_syllable_candidate_does_not_skip_layers(self):
        """D1 must not bypass intermediate layers.

        Architectural law: Each layer jump requires intermediate contract.
        """
        candidate = SyllableCandidate()

        # Verify domain is SYLLABIC (D1), not higher
        assert candidate.domain == DalTransitionDomain.SYLLABIC

        # Cannot jump to D3 (ORIGIN)
        assert candidate.domain != DalTransitionDomain.ORIGIN

        # Cannot jump to D4 (TEMPLATE)
        assert candidate.domain != DalTransitionDomain.TEMPLATE

        # Cannot jump to D5 (IDENTITY_AXIS)
        assert candidate.domain != DalTransitionDomain.IDENTITY_AXIS

        # Cannot jump to D6 (DIRECTIONAL_ANALYSIS)
        assert candidate.domain != DalTransitionDomain.DIRECTIONAL_ANALYSIS

        # Cannot jump to D7 (JUDGMENT)
        assert candidate.domain != DalTransitionDomain.JUDGMENT

    def test_generated_candidates_do_not_claim_root(self):
        """Generated candidates must not contain root information.

        Test actual generation flow, not just candidate class.
        """
        # Generate candidates for كَتَبَ (kataba)
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a1, _ = make_carrier('\u064E', 1)  # fatha
        atom_a1, _ = classify_carrier(carrier_a1)

        carrier_t, _ = make_carrier('ت', 2)
        atom_t, _ = classify_carrier(carrier_t)

        carrier_a2, _ = make_carrier('\u064E', 3)  # fatha
        atom_a2, _ = classify_carrier(carrier_a2)

        carrier_b, _ = make_carrier('ب', 4)
        atom_b, _ = classify_carrier(carrier_b)

        carrier_a3, _ = make_carrier('\u064E', 5)  # fatha
        atom_a3, _ = classify_carrier(carrier_a3)

        atoms = [atom_k, atom_a1, atom_t, atom_a2, atom_b, atom_a3]

        candidate_set = generate_syllable_candidates(atoms)

        # Every candidate must not have root
        for candidate in candidate_set.candidates:
            assert not hasattr(candidate, 'root'), \
                "Generated candidate must NOT have 'root' field"

            # Root is ك-ت-ب, but D1 must NOT extract it
            assert not hasattr(candidate, 'ktb'), \
                "D1 must not extract or store root radicals"

    def test_generated_candidates_do_not_claim_wazn(self):
        """Generated candidates must not contain pattern information.

        Test that generation doesn't leak morphological patterns.
        """
        # Generate candidates for كَاتِب (kaatib) - active participle
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a1, _ = make_carrier('\u064E', 1)  # fatha
        atom_a1, _ = classify_carrier(carrier_a1)

        carrier_alif, _ = make_carrier('ا', 2)
        atom_alif, _ = classify_carrier(carrier_alif)

        carrier_t, _ = make_carrier('ت', 3)
        atom_t, _ = classify_carrier(carrier_t)

        carrier_i, _ = make_carrier('\u0650', 4)  # kasra
        atom_i, _ = classify_carrier(carrier_i)

        carrier_b, _ = make_carrier('ب', 5)
        atom_b, _ = classify_carrier(carrier_b)

        atoms = [atom_k, atom_a1, atom_alif, atom_t, atom_i, atom_b]

        candidate_set = generate_syllable_candidates(atoms)

        # Every candidate must not have wazn
        for candidate in candidate_set.candidates:
            assert not hasattr(candidate, 'wazn'), \
                "Generated candidate must NOT have 'wazn' field"

            # Pattern is فاعل (faa'il), but D1 must NOT extract it
            assert not hasattr(candidate, 'faa_il'), \
                "D1 must not extract or store morphological pattern"

    def test_evidence_does_not_claim_higher_layers(self):
        """Evidence attached to D1 candidate must not claim higher-layer facts.

        Evidence scope must be SYLLABLE_STRUCTURE_VALID only.
        """
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]

        candidate_set = generate_syllable_candidates(atoms)

        for candidate in candidate_set.candidates:
            for evidence in candidate.evidence:
                # Check claim scope
                from dal_core.dal_algebra import DalClaimScope

                # Allowed scopes for D1
                allowed_scopes = {
                    DalClaimScope.SYLLABLE_STRUCTURE_VALID,
                    DalClaimScope.ATOM_SEQUENCE_VALID
                }

                # Forbidden scopes
                forbidden_scopes = {
                    DalClaimScope.ORIGIN_CLASSIFIED,
                    DalClaimScope.TEMPLATE_MATCHED,
                    DalClaimScope.IDENTITY_DETERMINED,
                    DalClaimScope.JUDGMENT_ISSUED
                }

                assert evidence.claim_scope not in forbidden_scopes, \
                    f"D1 evidence must not claim {evidence.claim_scope.name}"


class TestD1DomainBoundaries:
    """Test that D1 respects domain boundaries."""

    def test_syllable_candidate_stays_in_d1_domain(self):
        """Syllable candidate must stay in D1 (SYLLABIC) domain."""
        candidate = SyllableCandidate()

        assert candidate.domain == DalTransitionDomain.SYLLABIC, \
            "SyllableCandidate must be in SYLLABIC domain"

        # Not in D0 (too low)
        assert candidate.domain != DalTransitionDomain.GRAPHOPHONEMIC

        # Not in D2+ (too high)
        assert candidate.domain != DalTransitionDomain.PRE_MORPH
        assert candidate.domain != DalTransitionDomain.ORIGIN
        assert candidate.domain != DalTransitionDomain.TEMPLATE

    def test_trace_source_is_d0(self):
        """Trace source must be D0 (GRAPHOPHONEMIC)."""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]

        candidate_set = generate_syllable_candidates(atoms)

        for candidate in candidate_set.candidates:
            if candidate.trace:
                assert candidate.trace.source_domain == DalTransitionDomain.GRAPHOPHONEMIC, \
                    "D1 trace must originate from D0 (GRAPHOPHONEMIC)"

                assert candidate.trace.target_domain == DalTransitionDomain.SYLLABIC, \
                    "D1 trace must target D1 (SYLLABIC)"

    def test_no_backward_leakage_to_d0(self):
        """D1 must not leak back to D0 responsibilities.

        D1 works with syllables, not carriers or graphemes.
        """
        candidate = SyllableCandidate()

        # D1 uses atoms (D0 output), not carriers (D0 input)
        assert not hasattr(candidate, 'carriers'), \
            "D1 should not store raw carriers"

        assert not hasattr(candidate, 'graphemes'), \
            "D1 should not store raw graphemes"

        # D1 should store atoms (D0 output)
        assert hasattr(candidate, 'source_atoms'), \
            "D1 should store source atoms (D0 → D1 transition)"


class TestD1ForbiddenOperations:
    """Test that D1 doesn't perform forbidden operations."""

    def test_syllable_does_not_extract_root(self):
        """Syllabification must not extract root.

        Root extraction is D3 responsibility.
        """
        # Word: كَتَبَ (kataba) with known root ك-ت-ب
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a1, _ = make_carrier('\u064E', 1)
        atom_a1, _ = classify_carrier(carrier_a1)

        carrier_t, _ = make_carrier('ت', 2)
        atom_t, _ = classify_carrier(carrier_t)

        carrier_a2, _ = make_carrier('\u064E', 3)
        atom_a2, _ = classify_carrier(carrier_a2)

        carrier_b, _ = make_carrier('ب', 4)
        atom_b, _ = classify_carrier(carrier_b)

        atoms = [atom_k, atom_a1, atom_t, atom_a2, atom_b]

        candidate_set = generate_syllable_candidates(atoms)

        # Candidates generated, but NO root extraction
        assert len(candidate_set.candidates) > 0, "Should generate syllable candidates"

        for candidate in candidate_set.candidates:
            # No root field
            assert not hasattr(candidate, 'root')

            # Evidence should not mention root
            for evidence in candidate.evidence:
                assert 'root' not in str(evidence.details).lower(), \
                    "Evidence must not mention root extraction"

    def test_syllable_does_not_match_pattern(self):
        """Syllabification must not match morphological patterns.

        Pattern matching is D4 responsibility.
        """
        # Word: كَاتِب (kaatib) with known pattern فَاعِل (faa'il)
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        carrier_alif, _ = make_carrier('ا', 2)
        atom_alif, _ = classify_carrier(carrier_alif)

        carrier_t, _ = make_carrier('ت', 3)
        atom_t, _ = classify_carrier(carrier_t)

        carrier_i, _ = make_carrier('\u0650', 4)
        atom_i, _ = classify_carrier(carrier_i)

        carrier_b, _ = make_carrier('ب', 5)
        atom_b, _ = classify_carrier(carrier_b)

        atoms = [atom_k, atom_a, atom_alif, atom_t, atom_i, atom_b]

        candidate_set = generate_syllable_candidates(atoms)

        # Candidates generated, but NO pattern matching
        for candidate in candidate_set.candidates:
            # No wazn field
            assert not hasattr(candidate, 'wazn')
            assert not hasattr(candidate, 'pattern')

            # Evidence should not mention morphological pattern
            for evidence in candidate.evidence:
                assert 'faa_il' not in str(evidence.details).lower()
                assert 'active_participle' not in str(evidence.details).lower()

    def test_syllable_does_not_classify_word_class(self):
        """Syllabification must not classify word class.

        Word class (Ism/Fi'l/Harf) is D5 responsibility.
        """
        # Particle: فِي (fii) - known to be harf (particle)
        carrier_f, _ = make_carrier('ف', 0)
        atom_f, _ = classify_carrier(carrier_f)

        carrier_i, _ = make_carrier('\u0650', 1)  # kasra
        atom_i, _ = classify_carrier(carrier_i)

        carrier_y, _ = make_carrier('ي', 2)
        atom_y, _ = classify_carrier(carrier_y)

        atoms = [atom_f, atom_i, atom_y]

        candidate_set = generate_syllable_candidates(atoms)

        # Candidates generated, but NO word class determination
        for candidate in candidate_set.candidates:
            # No identity axis fields
            assert not hasattr(candidate, 'harf')
            assert not hasattr(candidate, 'particle')
            assert not hasattr(candidate, 'word_class')

            # Evidence should not mention word class
            for evidence in candidate.evidence:
                assert 'harf' not in str(evidence.details).lower()
                assert 'particle' not in str(evidence.details).lower()
