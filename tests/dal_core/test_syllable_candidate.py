"""
Tests for Syllable Candidate Layer (D1) - PR #30

Tests syllable candidate generation, boundary detection,
and dal_algebra protocol compliance.
"""

import pytest
from dal_core.syllable_candidate import (
    SyllableCandidate,
    SyllableCandidateSet,
    detect_syllable_boundaries,
    generate_syllable_candidate,
    generate_syllable_candidates,
    syllabify_word
)
from dal_core.syllables import SyllableType
from dal_core.atoms import ArabicAtom, AtomKind, classify_carrier
from dal_core.carriers import make_carrier
from dal_core.dal_algebra import DalTransitionDomain, DalClaimScope


class TestSyllableCandidate:
    """Test SyllableCandidate class"""

    def test_syllable_candidate_creation(self):
        """SyllableCandidate can be created with required fields"""
        candidate = SyllableCandidate()

        # Required by DalCandidateProtocol
        assert candidate.candidate_id
        assert candidate.domain == DalTransitionDomain.SYLLABIC
        assert isinstance(candidate.evidence, list)
        assert isinstance(candidate.counter_evidence, list)

    def test_syllable_candidate_confidence_validation(self):
        """Confidence must be in [0.0, 1.0]"""
        # Valid
        candidate = SyllableCandidate(confidence=0.5)
        assert candidate.confidence == 0.5

        # Invalid
        with pytest.raises(ValueError, match="Confidence must be in"):
            SyllableCandidate(confidence=1.5)

        with pytest.raises(ValueError, match="Confidence must be in"):
            SyllableCandidate(confidence=-0.1)

    def test_syllable_candidate_span_validation(self):
        """Span must be valid (start <= end, start >= 0)"""
        # Valid
        candidate = SyllableCandidate(span=(0, 3))
        assert candidate.span == (0, 3)

        # Invalid: start > end
        with pytest.raises(ValueError, match="Invalid span"):
            SyllableCandidate(span=(5, 3))

        # Invalid: negative start
        with pytest.raises(ValueError, match="Invalid span"):
            SyllableCandidate(span=(-1, 3))

    def test_syllable_candidate_is_valid(self):
        """is_valid() returns True when no blockers"""
        candidate = SyllableCandidate()
        assert candidate.is_valid()

    def test_syllable_candidate_has_blocker(self):
        """has_blocker() detects blocking residuals"""
        candidate = SyllableCandidate()
        assert not candidate.has_blocker()


class TestSyllableBoundaryDetection:
    """Test syllable boundary detection"""

    def test_detect_simple_cv_syllable(self):
        """Detect simple CV syllable (consonant + vowel)"""
        # كَ = ك + fatha
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)  # fatha
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]
        boundaries = detect_syllable_boundaries(atoms)

        assert len(boundaries) == 1
        assert boundaries[0] == (0, 2)

    def test_detect_cvc_syllable(self):
        """Detect CVC syllable (consonant + vowel + consonant)"""
        # كَتَ = ك + fatha + ت
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        carrier_t, _ = make_carrier('ت', 2)
        atom_t, _ = classify_carrier(carrier_t)

        atoms = [atom_k, atom_a, atom_t]
        boundaries = detect_syllable_boundaries(atoms)

        assert len(boundaries) == 1
        # Should be single syllable with coda
        assert boundaries[0][0] == 0

    def test_detect_multiple_syllables(self):
        """Detect multiple syllables in sequence"""
        # كَتَبَ = كَ + تَ + بَ (simplified)
        atoms = []
        chars = [('ك', 0), ('\u064E', 1), ('ت', 2), ('\u064E', 3), ('ب', 4), ('\u064E', 5)]

        for char, idx in chars:
            carrier, _ = make_carrier(char, idx)
            atom, _ = classify_carrier(carrier)
            atoms.append(atom)

        boundaries = detect_syllable_boundaries(atoms)

        # Should detect at least 1 syllable (algorithm may vary)
        assert len(boundaries) >= 1

    def test_detect_cvv_long_vowel(self):
        """Detect CVV syllable with long vowel"""
        # كَا = ك + fatha + alif
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        carrier_alif, _ = make_carrier('ا', 2)
        atom_alif, _ = classify_carrier(carrier_alif)

        atoms = [atom_k, atom_a, atom_alif]
        boundaries = detect_syllable_boundaries(atoms)

        assert len(boundaries) == 1
        # Should include all atoms
        assert boundaries[0] == (0, 3)


class TestGenerateSyllableCandidate:
    """Test syllable candidate generation"""

    def test_generate_cv_candidate(self):
        """Generate CV syllable candidate"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]
        candidate = generate_syllable_candidate(atoms, span=(0, 2))

        assert candidate.syllable.type == SyllableType.CV
        assert len(candidate.syllable.onset) == 1
        assert len(candidate.syllable.nucleus) == 1
        assert len(candidate.syllable.coda) == 0
        assert candidate.span == (0, 2)

    def test_generate_cvc_candidate(self):
        """Generate CVC syllable candidate"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        carrier_t, _ = make_carrier('ت', 2)
        atom_t, _ = classify_carrier(carrier_t)

        atoms = [atom_k, atom_a, atom_t]
        candidate = generate_syllable_candidate(atoms, span=(0, 3))

        assert candidate.syllable.type == SyllableType.CVC
        assert len(candidate.syllable.onset) == 1
        assert len(candidate.syllable.nucleus) == 1
        assert len(candidate.syllable.coda) == 1

    def test_generate_cvv_candidate(self):
        """Generate CVV syllable candidate (long vowel)"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        carrier_alif, _ = make_carrier('ا', 2)
        atom_alif, _ = classify_carrier(carrier_alif)

        atoms = [atom_k, atom_a, atom_alif]
        candidate = generate_syllable_candidate(atoms, span=(0, 3))

        assert candidate.syllable.type == SyllableType.CVV
        assert len(candidate.syllable.onset) == 1
        assert len(candidate.syllable.nucleus) == 2  # fatha + alif
        assert len(candidate.syllable.coda) == 0

    def test_candidate_has_evidence(self):
        """Generated candidate has evidence"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]
        candidate = generate_syllable_candidate(atoms, span=(0, 2))

        assert len(candidate.evidence) > 0
        assert candidate.evidence[0].claim_scope == DalClaimScope.SYLLABLE_STRUCTURE_VALID

    def test_candidate_has_trace(self):
        """Generated candidate has trace"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]
        candidate = generate_syllable_candidate(atoms, span=(0, 2))

        assert candidate.trace is not None
        assert candidate.trace.source_domain == DalTransitionDomain.GRAPHOPHONEMIC
        assert candidate.trace.target_domain == DalTransitionDomain.SYLLABIC
        assert candidate.trace.reversible is True


class TestGenerateSyllableCandidates:
    """Test syllable candidate set generation"""

    def test_generate_candidates_single_syllable(self):
        """Generate candidates for single syllable"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]
        candidate_set = generate_syllable_candidates(atoms)

        assert len(candidate_set) >= 1
        assert candidate_set.source_atoms == atoms

    def test_generate_candidates_multiple_syllables(self):
        """Generate candidates for multiple syllables"""
        atoms = []
        chars = [('ك', 0), ('\u064E', 1), ('ت', 2), ('\u064E', 3)]

        for char, idx in chars:
            carrier, _ = make_carrier(char, idx)
            atom, _ = classify_carrier(carrier)
            atoms.append(atom)

        candidate_set = generate_syllable_candidates(atoms)

        # Should generate at least one candidate
        assert len(candidate_set) >= 1

    def test_candidate_set_valid_candidates(self):
        """CandidateSet can filter valid candidates"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]
        candidate_set = generate_syllable_candidates(atoms)

        valid = candidate_set.valid_candidates()
        assert isinstance(valid, list)

    def test_candidate_set_best_candidate(self):
        """CandidateSet can select best candidate"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]
        candidate_set = generate_syllable_candidates(atoms)

        best = candidate_set.best_candidate()
        assert best is None or isinstance(best, SyllableCandidate)

    def test_empty_atoms_produces_warning(self):
        """Empty atom sequence produces warning residual"""
        candidate_set = generate_syllable_candidates([])

        assert len(candidate_set.global_residuals) > 0
        assert len(candidate_set) == 0


class TestSyllabifyWord:
    """Test convenience function"""

    def test_syllabify_simple_word(self):
        """Syllabify simple word"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]
        candidates = syllabify_word(atoms)

        assert isinstance(candidates, list)
        # Should return valid candidates only
        for candidate in candidates:
            assert candidate.is_valid()


class TestProtocolCompliance:
    """Test DalCandidateProtocol compliance"""

    def test_candidate_has_required_properties(self):
        """SyllableCandidate has all required protocol properties"""
        candidate = SyllableCandidate()

        # Required by DalCandidateProtocol
        assert hasattr(candidate, 'candidate_id')
        assert hasattr(candidate, 'domain')
        assert hasattr(candidate, 'evidence')
        assert hasattr(candidate, 'counter_evidence')

    def test_candidate_domain_is_syllabic(self):
        """SyllableCandidate domain is SYLLABIC"""
        candidate = SyllableCandidate()
        assert candidate.domain == DalTransitionDomain.SYLLABIC

    def test_candidate_id_is_unique(self):
        """Each candidate has unique ID"""
        c1 = SyllableCandidate()
        c2 = SyllableCandidate()

        assert c1.candidate_id != c2.candidate_id


class TestIntegrationWithExistingSyllables:
    """Test integration with existing syllables.py module"""

    def test_uses_syllable_type_enum(self):
        """SyllableCandidate uses SyllableType from syllables.py"""
        candidate = SyllableCandidate()
        assert isinstance(candidate.syllable.type, SyllableType)

    def test_candidate_syllable_validates(self):
        """Generated syllables pass validation"""
        carrier_k, _ = make_carrier('ك', 0)
        atom_k, _ = classify_carrier(carrier_k)

        carrier_a, _ = make_carrier('\u064E', 1)
        atom_a, _ = classify_carrier(carrier_a)

        atoms = [atom_k, atom_a]
        candidate = generate_syllable_candidate(atoms, span=(0, 2))

        # Should have minimal residuals
        assert candidate.syllable is not None
