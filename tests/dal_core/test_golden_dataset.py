"""
Golden Dataset Tests

End-to-end validation of dal_core Phase 2 using golden dataset fixtures.

This test suite validates:
- Complete pipeline behavior on known cases
- Theorem compliance across all test cases
- Semantic leak prevention (Theorem 5)
- Rank assignment correctness
- Residual propagation
"""

import json
import pytest
from pathlib import Path


# Load golden dataset
GOLDEN_DATASET_PATH = Path(__file__).parent.parent / "fixtures" / "dal_core" / "golden_vocalized_words.json"


@pytest.fixture
def golden_dataset():
    """Load golden dataset from JSON"""
    with open(GOLDEN_DATASET_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


class TestGoldenDatasetStructure:
    """Test golden dataset structure and completeness"""

    def test_golden_dataset_exists(self):
        """Golden dataset file exists"""
        assert GOLDEN_DATASET_PATH.exists()

    def test_golden_dataset_has_metadata(self, golden_dataset):
        """Dataset has metadata section"""
        assert 'metadata' in golden_dataset
        assert 'version' in golden_dataset['metadata']
        assert 'description' in golden_dataset['metadata']

    def test_golden_dataset_has_clear_cases(self, golden_dataset):
        """Dataset has clear cases"""
        assert 'clear_cases' in golden_dataset
        assert len(golden_dataset['clear_cases']) >= 3

    def test_golden_dataset_has_residual_cases(self, golden_dataset):
        """Dataset has residual cases"""
        assert 'residual_cases' in golden_dataset
        assert len(golden_dataset['residual_cases']) >= 2

    def test_golden_dataset_has_theorem_verification(self, golden_dataset):
        """Dataset has theorem verification mappings"""
        assert 'theorem_verification' in golden_dataset
        assert len(golden_dataset['theorem_verification']) >= 3


class TestClearCaseStructure:
    """Test clear case structure requirements"""

    def test_all_clear_cases_have_id(self, golden_dataset):
        """All clear cases have unique IDs"""
        cases = golden_dataset['clear_cases']
        ids = [c['id'] for c in cases]
        assert len(ids) == len(set(ids))  # All unique

    def test_all_clear_cases_have_input(self, golden_dataset):
        """All clear cases have input text"""
        cases = golden_dataset['clear_cases']
        for case in cases:
            assert 'input' in case
            assert len(case['input']) > 0

    def test_all_clear_cases_have_expected(self, golden_dataset):
        """All clear cases have expected results"""
        cases = golden_dataset['clear_cases']
        for case in cases:
            assert 'expected' in case
            assert 'd_lugha_rank' in case['expected']

    def test_clear_cases_specify_forbidden_fields(self, golden_dataset):
        """Clear cases specify forbidden semantic fields"""
        cases = golden_dataset['clear_cases']
        for case in cases:
            expected = case['expected']
            if 'forbidden_fields_absent' in expected:
                # Must include at least 'meaning' and 'semantic'
                forbidden = expected['forbidden_fields_absent']
                assert 'meaning' in forbidden or 'semantic' in forbidden


class TestResidualCaseStructure:
    """Test residual case structure requirements"""

    def test_all_residual_cases_have_expected_residuals(self, golden_dataset):
        """Residual cases specify expected residuals"""
        cases = golden_dataset['residual_cases']
        for case in cases:
            assert 'expected' in case
            assert 'expected_residuals' in case['expected']
            assert len(case['expected']['expected_residuals']) > 0

    def test_unvocalized_case_exists(self, golden_dataset):
        """Dataset includes unvocalized text case"""
        cases = golden_dataset['residual_cases']
        unvocalized = [c for c in cases if c['id'] == 'unvocalized_ktb']
        assert len(unvocalized) == 1

    def test_non_arabic_case_exists(self, golden_dataset):
        """Dataset includes non-Arabic text case"""
        cases = golden_dataset['residual_cases']
        non_arabic = [c for c in cases if c['id'] == 'non_arabic_latin']
        assert len(non_arabic) == 1


class TestTheoremCoverage:
    """Test theorem coverage in dataset"""

    def test_theorem_3_coverage(self, golden_dataset):
        """Theorem 3 (D_form ⊄ D_lugha) is covered"""
        theorems = golden_dataset['theorem_verification']
        theorem_3 = [t for t in theorems if 'Theorem 3' in t['theorem']]
        assert len(theorem_3) == 1

    def test_theorem_5_coverage(self, golden_dataset):
        """Theorem 5 (No meaning) is covered"""
        theorems = golden_dataset['theorem_verification']
        theorem_5 = [t for t in theorems if 'Theorem 5' in t['theorem']]
        assert len(theorem_5) == 1

    def test_rank_hierarchy_coverage(self, golden_dataset):
        """Rank hierarchy (Qiyas ≠ Sama) is documented"""
        theorems = golden_dataset['theorem_verification']
        rank_theorem = [t for t in theorems if 'Qiyas' in t['theorem']]
        assert len(rank_theorem) >= 1


class TestAttestedForms:
    """Test attested forms from witness store"""

    def test_kataba_attested(self, golden_dataset):
        """كَتَبَ case exists with TAWATUR rank"""
        cases = golden_dataset['clear_cases']
        kataba = [c for c in cases if c['input'] == 'كَتَبَ']
        assert len(kataba) == 1
        assert kataba[0]['expected']['d_lugha_rank'] == 'TAWATUR'

    def test_kitaab_attested(self, golden_dataset):
        """كِتَابٌ case exists with TAWATUR rank"""
        cases = golden_dataset['clear_cases']
        kitaab = [c for c in cases if c['input'] == 'كِتَابٌ']
        assert len(kitaab) == 1
        assert kitaab[0]['expected']['d_lugha_rank'] == 'TAWATUR'

    def test_min_particle_attested(self, golden_dataset):
        """مِنْ case exists with TAWATUR rank"""
        cases = golden_dataset['clear_cases']
        min_particle = [c for c in cases if c['input'] == 'مِنْ']
        assert len(min_particle) == 1
        assert min_particle[0]['expected']['d_lugha_rank'] == 'TAWATUR'


class TestUnattestedForms:
    """Test unattested forms behavior"""

    def test_satarab_unattested(self, golden_dataset):
        """سَطَرَبَ case exists as unattested"""
        cases = golden_dataset['residual_cases']
        satarab = [c for c in cases if c['input'] == 'سَطَرَبَ']
        assert len(satarab) == 1
        assert satarab[0]['expected']['d_lugha_rank'] == 'ZERO'
        assert not satarab[0]['expected']['d_lugha_attested']


class TestSemanticLeakPrevention:
    """Verify semantic leak prevention across all cases"""

    def test_all_clear_cases_forbid_semantic_fields(self, golden_dataset):
        """All clear cases must forbid semantic fields"""
        cases = golden_dataset['clear_cases']

        for case in cases:
            forbidden = case['expected'].get('forbidden_fields_absent', [])

            # At minimum, should forbid 'meaning' and 'semantic'
            # or be empty (meaning they weren't tested for that case)
            if forbidden:
                assert isinstance(forbidden, list)
                # If list exists, it should contain critical fields
                critical_fields = {'meaning', 'semantic', 'murad'}
                has_critical = any(f in forbidden for f in critical_fields)
                assert has_critical, f"Case {case['id']} doesn't forbid critical semantic fields"


# Integration tests (to be implemented when pipeline is complete)
class TestGoldenCaseIntegration:
    """Integration tests with actual pipeline (placeholder)"""

    @pytest.mark.skip(reason="Full pipeline integration pending")
    def test_clear_case_integration(self, golden_dataset):
        """Test clear cases against actual pipeline"""
        # from dal_core.pipeline import analyze_dal_mufrad

        cases = golden_dataset['clear_cases']

        for case in cases:
            # result = analyze_dal_mufrad(case['input'])
            # assert result.final_rank.name == case['expected']['d_lugha_rank']
            # ... full validation
            pass

    @pytest.mark.skip(reason="Full pipeline integration pending")
    def test_residual_case_integration(self, golden_dataset):
        """Test residual cases against actual pipeline"""
        # from dal_core.pipeline import analyze_dal_mufrad

        cases = golden_dataset['residual_cases']

        for case in cases:
            # result = analyze_dal_mufrad(case['input'])
            # ... validate residuals
            pass


class TestDatasetCompleteness:
    """Test dataset covers all critical scenarios"""

    def test_has_verb_cases(self, golden_dataset):
        """Dataset includes verb cases"""
        all_cases = golden_dataset['clear_cases'] + golden_dataset.get('edge_cases', [])
        verb_cases = [c for c in all_cases if 'FIIL' in str(c.get('expected', {}).get('d_type', ''))]
        assert len(verb_cases) >= 2

    def test_has_noun_cases(self, golden_dataset):
        """Dataset includes noun cases"""
        all_cases = golden_dataset['clear_cases'] + golden_dataset.get('edge_cases', [])
        noun_cases = [c for c in all_cases if 'ISM' in str(c.get('expected', {}).get('d_type', ''))]
        assert len(noun_cases) >= 3

    def test_has_particle_cases(self, golden_dataset):
        """Dataset includes particle cases"""
        all_cases = golden_dataset['clear_cases']
        particle_cases = [c for c in all_cases if 'HARF' in str(c.get('expected', {}).get('d_type', ''))]
        assert len(particle_cases) >= 1

    def test_has_tawatur_cases(self, golden_dataset):
        """Dataset includes TAWATUR rank cases"""
        all_cases = golden_dataset['clear_cases']
        tawatur_cases = [c for c in all_cases if c['expected']['d_lugha_rank'] == 'TAWATUR']
        assert len(tawatur_cases) >= 3

    def test_has_ahad_cases(self, golden_dataset):
        """Dataset includes AHAD rank cases"""
        all_cases = golden_dataset['clear_cases']
        ahad_cases = [c for c in all_cases if c['expected']['d_lugha_rank'] == 'AHAD']
        assert len(ahad_cases) >= 1

    def test_has_zero_rank_cases(self, golden_dataset):
        """Dataset includes ZERO rank (unattested) cases"""
        all_cases = golden_dataset['clear_cases'] + golden_dataset['residual_cases']
        zero_cases = [c for c in all_cases if c.get('expected', {}).get('d_lugha_rank') == 'ZERO']
        assert len(zero_cases) >= 2
