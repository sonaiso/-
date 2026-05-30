"""
Tests for K9 Storage Governance Contract

Tests the five-dimensional K9 constitutional law implementation:
1. StorageKind taxonomy
2. DerivationRank classification
3. ProofSource validation
4. ResidualState handling
5. RegenerationPolicy enforcement

Test Coverage:
    - K9 core violations (primitive storage of derivable items)
    - MODEL_OUTPUT proof source rejection
    - Artifact constitutional binding requirements
    - Derivation rank thresholds
    - Residual blocking logic
    - Edge cases and boundary conditions
"""

import pytest
from dal_core.k9_storage_governance import (
    StorageKind,
    DerivationRank,
    ProofSource,
    ResidualState,
    RegenerationPolicy,
    K9Item,
    verify_k9,
)


# ============================================================================
# Test: K9 Core Violation - Primitive Storage of Derivable Items
# ============================================================================

class TestK9CoreViolation:
    """Test core K9 violation: storing derivable items as primitives"""

    def test_primitive_storage_of_derivable_item_is_violation(self):
        """K9 Law 1: PRIMITIVE + derivable + sufficient rank + no blocking residuals = violation"""
        item = K9Item(
            item_id="test_001",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,  # Sufficient rank
            required_replacement_rank=DerivationRank.QIYAS,  # Equal to derivation rank
            proof_source=ProofSource.RULE,
            residual_state=ResidualState.NONE,  # No blocking residuals
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        assert reason == "primitive_storage_of_derivable_item"

    def test_primitive_storage_allowed_when_derivation_rank_insufficient(self):
        """Primitive allowed when derivation rank < required replacement rank"""
        item = K9Item(
            item_id="test_002",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=True,
            derivation_rank=DerivationRank.FORM,  # Low rank
            required_replacement_rank=DerivationRank.SAMA,  # Requires higher rank
            proof_source=ProofSource.RULE,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert is_valid  # Allowed because rank insufficient
        assert reason == "k9_ok"

    def test_primitive_storage_allowed_when_blocking_residuals_exist(self):
        """Primitive allowed when blocking residuals prevent replacement"""
        item = K9Item(
            item_id="test_003",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,
            required_replacement_rank=DerivationRank.QIYAS,
            proof_source=ProofSource.RULE,
            residual_state=ResidualState.BLOCKING,  # Blocking residuals
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert is_valid  # Allowed due to blocking residuals
        assert reason == "k9_ok"

    def test_primitive_storage_allowed_when_defer_residuals_exist(self):
        """Primitive allowed when deferred residuals prevent replacement"""
        item = K9Item(
            item_id="test_004",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=True,
            derivation_rank=DerivationRank.CERTIFIED,
            required_replacement_rank=DerivationRank.QIYAS,
            proof_source=ProofSource.GOVERNANCE,
            residual_state=ResidualState.DEFER,  # Deferred residuals
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert is_valid  # Allowed due to deferred residuals
        assert reason == "k9_ok"

    def test_primitive_storage_allowed_when_unknown_residuals(self):
        """Primitive allowed when residual state unknown (epistemologically honest)"""
        item = K9Item(
            item_id="test_005",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,
            required_replacement_rank=DerivationRank.QIYAS,
            proof_source=ProofSource.TRACE,
            residual_state=ResidualState.UNKNOWN,  # Unknown residuals
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert is_valid  # Allowed due to unknown residuals
        assert reason == "k9_ok"

    def test_primitive_storage_allowed_when_not_derivable(self):
        """Primitive storage of non-derivable item is allowed"""
        item = K9Item(
            item_id="test_006",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=False,  # Not derivable
            derivation_rank=DerivationRank.NOT_DERIVABLE,
            required_replacement_rank=DerivationRank.NOT_DERIVABLE,
            proof_source=ProofSource.LEXICAL,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert is_valid
        assert reason == "k9_ok"


# ============================================================================
# Test: MODEL_OUTPUT Proof Source Rejection
# ============================================================================

class TestModelOutputProofSourceRejection:
    """Test that MODEL_OUTPUT cannot be used as proof source for derivability"""

    def test_model_output_proof_source_rejected(self):
        """K9 Law 2: MODEL_OUTPUT cannot prove derivability"""
        item = K9Item(
            item_id="test_007",
            storage_kind=StorageKind.DERIVED_ARTIFACT,
            derivable=True,
            derivation_rank=DerivationRank.FORM,
            required_replacement_rank=DerivationRank.FORM,
            proof_source=ProofSource.MODEL_OUTPUT,  # FORBIDDEN
            residual_state=ResidualState.NONE,
            regeneration_policy=RegenerationPolicy.ON_MODEL_VERSION,
            source_trace_id="trace_123",
            derivation_rule_id="rule_456",
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        assert reason == "model_output_cannot_prove_derivability"

    def test_model_output_rejected_even_for_primitive(self):
        """MODEL_OUTPUT rejected regardless of storage kind"""
        item = K9Item(
            item_id="test_008",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=False,
            derivation_rank=DerivationRank.NOT_DERIVABLE,
            required_replacement_rank=DerivationRank.NOT_DERIVABLE,
            proof_source=ProofSource.MODEL_OUTPUT,  # FORBIDDEN
            residual_state=ResidualState.NONE,
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        assert reason == "model_output_cannot_prove_derivability"

    def test_valid_proof_sources_accepted(self):
        """Valid proof sources are accepted"""
        valid_proof_sources = [
            ProofSource.RULE,
            ProofSource.TRACE,
            ProofSource.TEST,
            ProofSource.TABLE,
            ProofSource.LEXICAL,
            ProofSource.GOVERNANCE,
        ]

        for proof_source in valid_proof_sources:
            item = K9Item(
                item_id=f"test_{proof_source.value}",
                storage_kind=StorageKind.PRIMITIVE,
                derivable=False,
                derivation_rank=DerivationRank.NOT_DERIVABLE,
                required_replacement_rank=DerivationRank.NOT_DERIVABLE,
                proof_source=proof_source,
                residual_state=ResidualState.NONE,
                regeneration_policy=None,
            )

            is_valid, reason = verify_k9(item)

            assert is_valid, f"{proof_source.value} should be accepted"
            assert reason == "k9_ok"


# ============================================================================
# Test: Artifact Constitutional Binding Requirements
# ============================================================================

class TestArtifactConstitutionalBindings:
    """Test that artifacts require source_trace_id, derivation_rule_id, regeneration_policy"""

    def test_derived_artifact_missing_source_trace_id(self):
        """K9 Law 3: DERIVED_ARTIFACT requires source_trace_id"""
        item = K9Item(
            item_id="test_009",
            storage_kind=StorageKind.DERIVED_ARTIFACT,
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,
            required_replacement_rank=DerivationRank.FORM,
            proof_source=ProofSource.TRACE,
            residual_state=ResidualState.NONE,
            regeneration_policy=RegenerationPolicy.ON_TRACE_CHANGE,
            source_trace_id=None,  # MISSING
            derivation_rule_id="rule_789",
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        assert reason == "derived_storage_missing_source_trace"

    def test_derived_artifact_missing_derivation_rule_id(self):
        """K9 Law 3: DERIVED_ARTIFACT requires derivation_rule_id"""
        item = K9Item(
            item_id="test_010",
            storage_kind=StorageKind.DERIVED_ARTIFACT,
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,
            required_replacement_rank=DerivationRank.FORM,
            proof_source=ProofSource.RULE,
            residual_state=ResidualState.NONE,
            regeneration_policy=RegenerationPolicy.ON_RULE_CHANGE,
            source_trace_id="trace_456",
            derivation_rule_id=None,  # MISSING
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        assert reason == "derived_storage_missing_rule"

    def test_derived_artifact_missing_regeneration_policy(self):
        """K9 Law 3: DERIVED_ARTIFACT requires regeneration_policy"""
        item = K9Item(
            item_id="test_011",
            storage_kind=StorageKind.DERIVED_ARTIFACT,
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,
            required_replacement_rank=DerivationRank.FORM,
            proof_source=ProofSource.GOVERNANCE,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,  # MISSING
            source_trace_id="trace_789",
            derivation_rule_id="rule_012",
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        assert reason == "derived_storage_missing_regeneration_policy"

    def test_cache_missing_bindings(self):
        """CACHE requires same bindings as DERIVED_ARTIFACT"""
        item = K9Item(
            item_id="test_012",
            storage_kind=StorageKind.CACHE,
            derivable=True,
            derivation_rank=DerivationRank.FORM,
            required_replacement_rank=DerivationRank.NOT_DERIVABLE,
            proof_source=ProofSource.RULE,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,  # MISSING
            source_trace_id=None,  # MISSING
            derivation_rule_id=None,  # MISSING
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        # First violation detected wins
        assert reason in {
            "derived_storage_missing_source_trace",
            "derived_storage_missing_rule",
            "derived_storage_missing_regeneration_policy",
        }

    def test_index_missing_bindings(self):
        """INDEX requires same bindings as DERIVED_ARTIFACT"""
        item = K9Item(
            item_id="test_013",
            storage_kind=StorageKind.INDEX,
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,
            required_replacement_rank=DerivationRank.FORM,
            proof_source=ProofSource.TABLE,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,  # MISSING
            source_trace_id="trace_345",
            derivation_rule_id="rule_678",
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        assert reason == "derived_storage_missing_regeneration_policy"

    def test_valid_derived_artifact_with_all_bindings(self):
        """Valid DERIVED_ARTIFACT with all required bindings"""
        item = K9Item(
            item_id="test_014",
            storage_kind=StorageKind.DERIVED_ARTIFACT,
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,
            required_replacement_rank=DerivationRank.FORM,
            proof_source=ProofSource.GOVERNANCE,
            residual_state=ResidualState.NON_BLOCKING,
            regeneration_policy=RegenerationPolicy.ON_SOURCE_CHANGE,
            source_trace_id="trace_valid",
            derivation_rule_id="rule_valid",
        )

        is_valid, reason = verify_k9(item)

        assert is_valid
        assert reason == "k9_ok"


# ============================================================================
# Test: Storage Kind Not Requiring Bindings
# ============================================================================

class TestStorageKindNotRequiringBindings:
    """Test that PRIMITIVE, TRACE_LOG, EXCEPTION_OVERRIDE don't require artifact bindings"""

    def test_primitive_does_not_require_bindings(self):
        """PRIMITIVE storage doesn't require artifact bindings"""
        item = K9Item(
            item_id="test_015",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=False,
            derivation_rank=DerivationRank.NOT_DERIVABLE,
            required_replacement_rank=DerivationRank.NOT_DERIVABLE,
            proof_source=ProofSource.LEXICAL,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,  # Not required for primitive
            source_trace_id=None,  # Not required for primitive
            derivation_rule_id=None,  # Not required for primitive
        )

        is_valid, reason = verify_k9(item)

        assert is_valid
        assert reason == "k9_ok"

    def test_trace_log_does_not_require_bindings(self):
        """TRACE_LOG storage doesn't require artifact bindings"""
        item = K9Item(
            item_id="test_016",
            storage_kind=StorageKind.TRACE_LOG,
            derivable=False,
            derivation_rank=DerivationRank.NOT_DERIVABLE,
            required_replacement_rank=DerivationRank.NOT_DERIVABLE,
            proof_source=ProofSource.TRACE,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,  # Not required for trace log
            source_trace_id=None,  # Not required for trace log
            derivation_rule_id=None,  # Not required for trace log
        )

        is_valid, reason = verify_k9(item)

        assert is_valid
        assert reason == "k9_ok"

    def test_exception_override_does_not_require_bindings(self):
        """EXCEPTION_OVERRIDE storage doesn't require artifact bindings"""
        item = K9Item(
            item_id="test_017",
            storage_kind=StorageKind.EXCEPTION_OVERRIDE,
            derivable=False,
            derivation_rank=DerivationRank.NOT_DERIVABLE,
            required_replacement_rank=DerivationRank.NOT_DERIVABLE,
            proof_source=ProofSource.LEXICAL,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,  # Not required for exception
            source_trace_id=None,  # Not required for exception
            derivation_rule_id=None,  # Not required for exception
        )

        is_valid, reason = verify_k9(item)

        assert is_valid
        assert reason == "k9_ok"


# ============================================================================
# Test: Derivation Rank Boundary Cases
# ============================================================================

class TestDerivationRankBoundaries:
    """Test derivation rank threshold logic"""

    def test_derivation_rank_equal_to_required_triggers_violation(self):
        """derivation_rank == required_replacement_rank triggers K9 violation"""
        item = K9Item(
            item_id="test_018",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,  # 2
            required_replacement_rank=DerivationRank.QIYAS,  # 2 (equal)
            proof_source=ProofSource.RULE,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        assert reason == "primitive_storage_of_derivable_item"

    def test_derivation_rank_greater_than_required_triggers_violation(self):
        """derivation_rank > required_replacement_rank triggers K9 violation"""
        item = K9Item(
            item_id="test_019",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=True,
            derivation_rank=DerivationRank.CERTIFIED,  # 4
            required_replacement_rank=DerivationRank.FORM,  # 1 (much lower)
            proof_source=ProofSource.GOVERNANCE,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        assert reason == "primitive_storage_of_derivable_item"

    def test_derivation_rank_less_than_required_allows_primitive(self):
        """derivation_rank < required_replacement_rank allows primitive storage"""
        item = K9Item(
            item_id="test_020",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=True,
            derivation_rank=DerivationRank.FORM,  # 1
            required_replacement_rank=DerivationRank.CERTIFIED,  # 4 (much higher)
            proof_source=ProofSource.RULE,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert is_valid
        assert reason == "k9_ok"


# ============================================================================
# Test: Real-World Scenarios
# ============================================================================

class TestRealWorldScenarios:
    """Test real-world K9 scenarios"""

    def test_training_example_as_derived_artifact(self):
        """TrainingExample stored as DERIVED_ARTIFACT with proper bindings"""
        item = K9Item(
            item_id="training_example_001",
            storage_kind=StorageKind.DERIVED_ARTIFACT,  # NOT primitive
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,
            required_replacement_rank=DerivationRank.FORM,
            proof_source=ProofSource.TRACE,  # Derived from trace
            residual_state=ResidualState.NON_BLOCKING,
            regeneration_policy=RegenerationPolicy.ON_TRACE_CHANGE,
            source_trace_id="algorithm_trace_payload_789",
            derivation_rule_id="TraceExplanationDatasetGenerator",
        )

        is_valid, reason = verify_k9(item)

        assert is_valid  # Compliant
        assert reason == "k9_ok"

    def test_training_example_as_primitive_violation(self):
        """TrainingExample stored as PRIMITIVE is K9 violation"""
        item = K9Item(
            item_id="training_example_002",
            storage_kind=StorageKind.PRIMITIVE,  # VIOLATION
            derivable=True,
            derivation_rank=DerivationRank.QIYAS,
            required_replacement_rank=DerivationRank.FORM,
            proof_source=ProofSource.TRACE,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert not is_valid
        assert reason == "primitive_storage_of_derivable_item"

    def test_lexical_entry_as_primitive_allowed(self):
        """Lexical entry (NOT derivable) stored as PRIMITIVE is allowed"""
        item = K9Item(
            item_id="lexical_entry_طاهر",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=False,  # Lexical, not derivable
            derivation_rank=DerivationRank.NOT_DERIVABLE,
            required_replacement_rank=DerivationRank.NOT_DERIVABLE,
            proof_source=ProofSource.LEXICAL,
            residual_state=ResidualState.NONE,
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert is_valid
        assert reason == "k9_ok"

    def test_augmented_verb_with_blocking_residuals(self):
        """Augmented verb derivable BUT blocking residuals prevent primitive deletion"""
        item = K9Item(
            item_id="verb_augmented_سمع",
            storage_kind=StorageKind.PRIMITIVE,
            derivable=True,  # Can derive تعدية generally
            derivation_rank=DerivationRank.QIYAS,
            required_replacement_rank=DerivationRank.QIYAS,
            proof_source=ProofSource.RULE,
            residual_state=ResidualState.BLOCKING,  # سماع contradicts قياس
            regeneration_policy=None,
        )

        is_valid, reason = verify_k9(item)

        assert is_valid  # Allowed due to blocking residuals
        assert reason == "k9_ok"

    def test_model_output_jsonl_as_artifact(self):
        """Model output JSONL stored as DERIVED_ARTIFACT with regeneration"""
        item = K9Item(
            item_id="model_output_jsonl_001",
            storage_kind=StorageKind.DERIVED_ARTIFACT,
            derivable=True,
            derivation_rank=DerivationRank.FORM,
            required_replacement_rank=DerivationRank.NOT_DERIVABLE,
            proof_source=ProofSource.TRACE,  # NOT MODEL_OUTPUT
            residual_state=ResidualState.NON_BLOCKING,
            regeneration_policy=RegenerationPolicy.ON_MODEL_VERSION,
            source_trace_id="training_run_trace_456",
            derivation_rule_id="T5AdapterPipeline",
        )

        is_valid, reason = verify_k9(item)

        assert is_valid
        assert reason == "k9_ok"


# ============================================================================
# Test: Enum Completeness
# ============================================================================

class TestEnumCompleteness:
    """Verify all enums are properly defined"""

    def test_storage_kind_enum_values(self):
        """Verify StorageKind enum has all required values"""
        expected_values = {
            "primitive",
            "derived_artifact",
            "cache",
            "index",
            "trace_log",
            "exception_override",
        }
        actual_values = {kind.value for kind in StorageKind}
        assert actual_values == expected_values

    def test_derivation_rank_enum_ordering(self):
        """Verify DerivationRank enum values are properly ordered"""
        assert DerivationRank.NOT_DERIVABLE.value == 0
        assert DerivationRank.FORM.value == 1
        assert DerivationRank.QIYAS.value == 2
        assert DerivationRank.SAMA.value == 3
        assert DerivationRank.CERTIFIED.value == 4

    def test_proof_source_enum_values(self):
        """Verify ProofSource enum has all required values"""
        expected_values = {
            "rule",
            "trace",
            "test",
            "table",
            "lexical",
            "governance",
            "model_output",
        }
        actual_values = {source.value for source in ProofSource}
        assert actual_values == expected_values

    def test_residual_state_enum_values(self):
        """Verify ResidualState enum has all required values"""
        expected_values = {"none", "non_blocking", "defer", "blocking", "unknown"}
        actual_values = {state.value for state in ResidualState}
        assert actual_values == expected_values

    def test_regeneration_policy_enum_values(self):
        """Verify RegenerationPolicy enum has all required values"""
        expected_values = {
            "never",
            "on_source_change",
            "on_rule_change",
            "on_trace_change",
            "on_schema_change",
            "on_model_version",
            "ttl_cache",
            "manual_review",
        }
        actual_values = {policy.value for policy in RegenerationPolicy}
        assert actual_values == expected_values
