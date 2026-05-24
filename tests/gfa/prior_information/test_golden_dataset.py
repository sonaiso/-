"""
Parametrized Tests Using Golden Dataset for Name Reality Cases

This test file loads the golden dataset from JSON and runs parametrized tests.

Critical Law:
- Golden dataset must be the source of truth, not manual test cases
- All cases in golden dataset must pass
- Failures must update golden dataset, not bypass it
"""

import pytest
import json
from pathlib import Path

from gfa.prior_information import (
    NameRealitySubGate,
    RealityType,
)


# Load golden dataset
GOLDEN_DATASET_PATH = Path(__file__).parent.parent.parent / "golden" / "prior_information" / "name_reality_cases.json"


def load_golden_dataset():
    """Load golden dataset from JSON file."""
    if not GOLDEN_DATASET_PATH.exists():
        return []  # Return empty list if not found (will skip tests)

    with open(GOLDEN_DATASET_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    return data.get("name_reality_cases", [])


class TestNameRealityGoldenDataset:
    """Test NameRealitySubGate against golden dataset."""

    @pytest.fixture
    def gate(self):
        """Provide NameRealitySubGate instance."""
        return NameRealitySubGate()

    @pytest.mark.parametrize(
        "case",
        load_golden_dataset(),
        ids=lambda case: case.get("case_id", "unknown")
    )
    def test_golden_case(self, gate, case):
        """
        Test NameRealitySubGate against golden dataset case.

        Each case specifies:
        - name: The Arabic name
        - referent_candidate: Proposed referent
        - existence_type: Type of existence
        - domain: Domain (may be null)
        - referent_evidence: Evidence (may be null)
        - expected_status: ADMITTED or BLOCKED
        - expected_rank: Expected rank
        - reason: Human-readable explanation
        """
        # Extract case parameters
        name = case["name"]
        referent_candidate = case.get("referent_candidate")
        existence_type_str = case.get("existence_type")
        domain = case.get("domain")
        referent_evidence = case.get("referent_evidence")
        expected_status = case["expected_status"]
        expected_rank = case["expected_rank"]
        reason = case.get("reason", "")

        # Map string to RealityType enum
        existence_type = None
        if existence_type_str:
            try:
                existence_type = RealityType[existence_type_str]
            except KeyError:
                pytest.fail(f"Unknown existence type in golden dataset: {existence_type_str}")

        # Run admission
        result = gate.admit_named_reality(
            name=name,
            referent_candidate=referent_candidate,
            existence_type=existence_type,
            domain=domain,
            referent_evidence=referent_evidence,
        )

        # Validate status
        if expected_status == "ADMITTED":
            assert result.is_admitted(), \
                f"Case {case['case_id']}: Expected ADMITTED but got {result.status}. " \
                f"Reason: {reason}. Failure: {result.failure}"
        elif expected_status == "BLOCKED":
            assert result.is_blocked(), \
                f"Case {case['case_id']}: Expected BLOCKED but got {result.status}. " \
                f"Reason: {reason}"
        else:
            pytest.fail(f"Unknown expected_status in golden dataset: {expected_status}")

        # Validate rank
        assert result.rank == expected_rank, \
            f"Case {case['case_id']}: Expected rank {expected_rank} but got {result.rank}. " \
            f"Reason: {reason}"

    def test_golden_dataset_exists(self):
        """Ensure golden dataset file exists."""
        assert GOLDEN_DATASET_PATH.exists(), \
            f"Golden dataset missing: {GOLDEN_DATASET_PATH}"

    def test_golden_dataset_non_empty(self):
        """Ensure golden dataset has cases."""
        cases = load_golden_dataset()
        assert len(cases) > 0, "Golden dataset is empty"

    def test_golden_dataset_valid_structure(self):
        """Validate golden dataset structure."""
        cases = load_golden_dataset()

        required_fields = [
            "case_id",
            "name",
            "expected_status",
            "expected_rank",
        ]

        for i, case in enumerate(cases):
            for field in required_fields:
                assert field in case, \
                    f"Case {i}: Missing required field '{field}'"

            # Validate expected_status
            assert case["expected_status"] in ["ADMITTED", "BLOCKED"], \
                f"Case {i}: Invalid expected_status: {case['expected_status']}"

            # Validate expected_rank
            assert case["expected_rank"] in ["CANDIDATE", "LICENSED", "CERTIFIED", "BLOCKED"], \
                f"Case {i}: Invalid expected_rank: {case['expected_rank']}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
