"""
Tests for Training Pipeline Skeleton (PR #148)

Constitutional Testing Laws:
    1. Test that skeleton plans training, does NOT train
    2. Test that skeleton validates conditions, does NOT execute models
    3. Test that skeleton produces plans, does NOT create authority
    4. Test constitutional guards prevent forbidden operations
    5. Test preflight checks detect violations
"""

import pytest
from pathlib import Path
from tempfile import TemporaryDirectory

from dal_core.training_pipeline_skeleton import (
    TrainingPipelineConfig,
    TrainingPlanCandidate,
    ConstitutionalPreflightReport,
    TrainingRunPlan,
    TrainingPipelineSkeleton,
    TrainingMode,
    ModelArchitecture,
    PreflightCheckType,
    PreflightCheckStatus,
    CONSTITUTIONAL_CONSTRAINTS,
)
from dal_core.training_example import TrainingExample
from dal_core.algorithm_trace_payload import TraceConsumerOperation
from dal_core.trace_explanation_dataset_generator import (
    OutputType,
    ValidationStatus,
)


# ============================================================================
# Helper Functions
# ============================================================================

def make_training_example(
    example_id: str = "training_example_test123",
    source_trace_id: str = "trace_abc123",
    source_dataset_row_id: str = "dataset_row_xyz789",
    operation: TraceConsumerOperation = TraceConsumerOperation.EXPLAIN_TRACE,
    input_text: str = "Explain candidate_abc123",
    target_text: str = "The candidate represents nominal structure",
) -> TrainingExample:
    """Create test TrainingExample."""
    return TrainingExample(
        training_example_id=example_id,
        source_dataset_row_id=source_dataset_row_id,
        source_trace_id=source_trace_id,
        source_algorithm="test_algorithm",
        operation=operation,
        input_text=input_text,
        target_text=target_text,
        referenced_candidate_ids=("candidate_abc123",),
        referenced_residual_ids=(),
        referenced_gate_ids=(),
        referenced_rank_values=(),
        output_type=OutputType.EXPLANATION,
        requires_algorithm_rerun=False,
        validation_status=ValidationStatus.VALID,
    )


def make_training_config(
    config_id: str = "config_test123",
    training_examples_path: str = "/tmp/test_examples.jsonl",
    output_dir: str = "/tmp/test_output",
) -> TrainingPipelineConfig:
    """Create test TrainingPipelineConfig."""
    return TrainingPipelineConfig(
        config_id=config_id,
        training_examples_path=training_examples_path,
        model_architecture=ModelArchitecture.T5_BASE,
        training_mode=TrainingMode.EXPLANATION_GENERATION,
        max_input_length=512,
        max_target_length=256,
        batch_size=8,
        num_epochs=3,
        learning_rate=5e-5,
        output_dir=output_dir,
        allowed_operations=frozenset([
            TraceConsumerOperation.EXPLAIN_TRACE,
            TraceConsumerOperation.SUMMARIZE_CANDIDATES,
        ]),
    )


# ============================================================================
# TrainingPipelineConfig Tests
# ============================================================================

class TestTrainingPipelineConfig:
    """Test TrainingPipelineConfig immutable container."""

    def test_valid_config_creation(self):
        """Test creating valid TrainingPipelineConfig."""
        config = make_training_config()

        assert config.config_id == "config_test123"
        assert config.model_architecture == ModelArchitecture.T5_BASE
        assert config.training_mode == TrainingMode.EXPLANATION_GENERATION
        assert config.max_input_length == 512
        assert config.batch_size == 8
        assert config.num_epochs == 3
        assert config.learning_rate == 5e-5

    def test_config_is_immutable(self):
        """Test that TrainingPipelineConfig is immutable."""
        config = make_training_config()

        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            config.batch_size = 16

    def test_config_requires_config_id(self):
        """Test that config_id is required."""
        with pytest.raises(ValueError, match="requires config_id"):
            TrainingPipelineConfig(
                config_id="",  # Invalid: empty
                training_examples_path="/tmp/test.jsonl",
                model_architecture=ModelArchitecture.T5_BASE,
                training_mode=TrainingMode.EXPLANATION_GENERATION,
                max_input_length=512,
                max_target_length=256,
                batch_size=8,
                num_epochs=3,
                learning_rate=5e-5,
                output_dir="/tmp/output",
                allowed_operations=frozenset([TraceConsumerOperation.EXPLAIN_TRACE]),
            )

    def test_config_requires_positive_max_input_length(self):
        """Test that max_input_length must be positive."""
        with pytest.raises(ValueError, match="max_input_length must be positive"):
            TrainingPipelineConfig(
                config_id="test",
                training_examples_path="/tmp/test.jsonl",
                model_architecture=ModelArchitecture.T5_BASE,
                training_mode=TrainingMode.EXPLANATION_GENERATION,
                max_input_length=0,  # Invalid
                max_target_length=256,
                batch_size=8,
                num_epochs=3,
                learning_rate=5e-5,
                output_dir="/tmp/output",
                allowed_operations=frozenset([TraceConsumerOperation.EXPLAIN_TRACE]),
            )

    def test_config_requires_positive_batch_size(self):
        """Test that batch_size must be positive."""
        with pytest.raises(ValueError, match="batch_size must be positive"):
            TrainingPipelineConfig(
                config_id="test",
                training_examples_path="/tmp/test.jsonl",
                model_architecture=ModelArchitecture.T5_BASE,
                training_mode=TrainingMode.EXPLANATION_GENERATION,
                max_input_length=512,
                max_target_length=256,
                batch_size=-1,  # Invalid
                num_epochs=3,
                learning_rate=5e-5,
                output_dir="/tmp/output",
                allowed_operations=frozenset([TraceConsumerOperation.EXPLAIN_TRACE]),
            )

    def test_config_requires_allowed_operations(self):
        """Test that allowed_operations cannot be empty."""
        with pytest.raises(ValueError, match="requires allowed_operations"):
            TrainingPipelineConfig(
                config_id="test",
                training_examples_path="/tmp/test.jsonl",
                model_architecture=ModelArchitecture.T5_BASE,
                training_mode=TrainingMode.EXPLANATION_GENERATION,
                max_input_length=512,
                max_target_length=256,
                batch_size=8,
                num_epochs=3,
                learning_rate=5e-5,
                output_dir="/tmp/output",
                allowed_operations=frozenset(),  # Invalid: empty
            )


# ============================================================================
# TrainingPlanCandidate Tests
# ============================================================================

class TestTrainingPlanCandidate:
    """Test TrainingPlanCandidate plan representation."""

    def test_create_training_plan(self):
        """Test creating training plan from config and examples."""
        config = make_training_config()
        examples = tuple(make_training_example(f"ex_{i}") for i in range(100))

        plan = TrainingPipelineSkeleton.create_training_plan(config, examples)

        assert plan.config_id == config.config_id
        assert plan.total_examples == 100
        assert plan.estimated_steps > 0
        assert plan.estimated_duration_minutes > 0
        assert plan.requires_preflight_check is True

    def test_plan_estimates_steps_correctly(self):
        """Test that plan estimates training steps correctly."""
        config = make_training_config()
        examples = tuple(make_training_example(f"ex_{i}") for i in range(100))

        plan = TrainingPipelineSkeleton.create_training_plan(config, examples)

        # 100 examples, batch_size=8, num_epochs=3
        # Steps per epoch = ceil(100/8) = 13
        # Total steps = 13 * 3 = 39
        expected_steps_per_epoch = (100 + 8 - 1) // 8  # 13
        expected_total_steps = expected_steps_per_epoch * 3  # 39

        assert plan.estimated_steps == expected_total_steps

    def test_plan_is_immutable(self):
        """Test that TrainingPlanCandidate is immutable."""
        config = make_training_config()
        examples = tuple(make_training_example(f"ex_{i}") for i in range(10))
        plan = TrainingPipelineSkeleton.create_training_plan(config, examples)

        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            plan.total_examples = 999

    def test_plan_requires_non_empty_examples(self):
        """Test that creating plan requires non-empty examples."""
        config = make_training_config()
        examples = ()  # Empty

        with pytest.raises(ValueError, match="Cannot create training plan with zero examples"):
            TrainingPipelineSkeleton.create_training_plan(config, examples)

    def test_plan_validates_config_id_match(self):
        """Test that plan config_id matches config."""
        config = make_training_config(config_id="config_123")
        examples = tuple(make_training_example(f"ex_{i}") for i in range(10))
        plan = TrainingPipelineSkeleton.create_training_plan(config, examples)

        # Manually create plan with mismatched config_id (bypass factory method)
        with pytest.raises(ValueError, match="config_id mismatch"):
            TrainingPlanCandidate(
                plan_id="plan_test",
                config_id="different_config",  # Mismatch
                config=config,
                total_examples=10,
                estimated_steps=100,
                estimated_duration_minutes=2,
                requires_preflight_check=True,
            )


# ============================================================================
# Preflight Check Tests
# ============================================================================

class TestConstitutionalPreflightCheck:
    """Test constitutional preflight checks."""

    def test_preflight_all_checks_pass(self):
        """Test preflight when all checks pass."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")  # Create empty file
            output_dir = tmpdir_path / "output"

            config = make_training_config(
                training_examples_path=str(training_file),
                output_dir=str(output_dir),
            )
            examples = tuple(make_training_example(f"ex_{i}") for i in range(10))
            plan = TrainingPipelineSkeleton.create_training_plan(config, examples)

            preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)

            assert preflight.plan_id == plan.plan_id
            assert preflight.passed is True
            assert preflight.failed_checks_count == 0
            assert len(preflight.checks) >= 7  # At least 7 check types

    def test_preflight_detects_missing_training_file(self):
        """Test preflight detects missing training examples file."""
        config = make_training_config(
            training_examples_path="/nonexistent/path/examples.jsonl",
        )
        examples = tuple(make_training_example(f"ex_{i}") for i in range(10))
        plan = TrainingPipelineSkeleton.create_training_plan(config, examples)

        preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)

        assert preflight.passed is False
        assert preflight.failed_checks_count >= 1

        # Check for TRAINING_EXAMPLES_EXIST failure
        training_file_check = [
            c for c in preflight.checks
            if c.check_type == PreflightCheckType.TRAINING_EXAMPLES_EXIST
        ]
        assert len(training_file_check) == 1
        assert training_file_check[0].status == PreflightCheckStatus.FAILED

    def test_preflight_detects_empty_examples(self):
        """Test preflight detects when no examples provided."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")

            config = make_training_config(
                training_examples_path=str(training_file),
            )
            examples = ()  # Empty tuple

            # Cannot create plan with empty examples
            with pytest.raises(ValueError, match="Cannot create training plan with zero examples"):
                TrainingPipelineSkeleton.create_training_plan(config, examples)

    def test_preflight_detects_disallowed_operations(self):
        """Test preflight detects disallowed operations."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")

            config = make_training_config(
                training_examples_path=str(training_file),
                output_dir=str(tmpdir_path / "output"),
            )
            # Config only allows EXPLAIN_TRACE and SUMMARIZE_CANDIDATES

            # Create example with disallowed operation
            examples = (
                make_training_example(operation=TraceConsumerOperation.SUGGEST_REPAIR),
            )
            plan = TrainingPipelineSkeleton.create_training_plan(config, examples)

            preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)

            assert preflight.passed is False
            assert preflight.failed_checks_count >= 1

            # Check for OPERATION_PERMITTED failure
            operation_check = [
                c for c in preflight.checks
                if c.check_type == PreflightCheckType.OPERATION_PERMITTED
            ]
            assert len(operation_check) == 1
            assert operation_check[0].status == PreflightCheckStatus.FAILED

    def test_preflight_detects_missing_source_bindings(self):
        """Test preflight detects examples with missing source bindings."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")

            config = make_training_config(
                training_examples_path=str(training_file),
                output_dir=str(tmpdir_path / "output"),
            )

            # Create example with missing source_trace_id
            example_bad = TrainingExample(
                training_example_id="ex_bad",
                source_dataset_row_id="dataset_row_123",
                source_trace_id="",  # Missing
                source_algorithm="test",
                operation=TraceConsumerOperation.EXPLAIN_TRACE,
                input_text="test input",
                target_text="test target",
                referenced_candidate_ids=(),
                referenced_residual_ids=(),
                referenced_gate_ids=(),
                referenced_rank_values=(),
                output_type=OutputType.EXPLANATION,
                requires_algorithm_rerun=False,
                validation_status=ValidationStatus.VALID,
            )

            examples = (example_bad,)
            plan = TrainingPipelineSkeleton.create_training_plan(config, examples)

            preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)

            assert preflight.passed is False
            assert preflight.failed_checks_count >= 1

            # Check for SOURCE_BINDINGS_PRESERVED failure
            binding_check = [
                c for c in preflight.checks
                if c.check_type == PreflightCheckType.SOURCE_BINDINGS_PRESERVED
            ]
            assert len(binding_check) == 1
            assert binding_check[0].status == PreflightCheckStatus.FAILED

    def test_preflight_warns_about_forbidden_phrases(self):
        """Test preflight warns about forbidden authority phrases."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")

            config = make_training_config(
                training_examples_path=str(training_file),
                output_dir=str(tmpdir_path / "output"),
            )

            # Create example with forbidden phrase
            example_bad = make_training_example(
                target_text="The final_answer is that the structure is correct"
            )

            examples = (example_bad,)
            plan = TrainingPipelineSkeleton.create_training_plan(config, examples)

            preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)

            # Should have warning (not failure) since this is sample check
            assert preflight.warning_checks_count >= 1

            # Check for NO_FORBIDDEN_PHRASES warning
            phrase_check = [
                c for c in preflight.checks
                if c.check_type == PreflightCheckType.NO_FORBIDDEN_PHRASES
            ]
            assert len(phrase_check) == 1
            assert phrase_check[0].status == PreflightCheckStatus.WARNING


# ============================================================================
# TrainingRunPlan Tests
# ============================================================================

class TestTrainingRunPlan:
    """Test TrainingRunPlan governed plan."""

    def test_create_training_run_plan(self):
        """Test creating training run plan from validated plan and preflight."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")

            config = make_training_config(
                training_examples_path=str(training_file),
                output_dir=str(tmpdir_path / "output"),
            )
            examples = tuple(make_training_example(f"ex_{i}") for i in range(10))
            plan = TrainingPipelineSkeleton.create_training_plan(config, examples)
            preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)

            run_plan = TrainingPipelineSkeleton.create_training_run_plan(plan, preflight)

            assert run_plan.plan_id == plan.plan_id
            assert run_plan.plan_candidate == plan
            assert run_plan.preflight_report == preflight
            assert run_plan.ready_for_execution == preflight.passed
            assert run_plan.constitutional_constraints == CONSTITUTIONAL_CONSTRAINTS

    def test_run_plan_is_immutable(self):
        """Test that TrainingRunPlan is immutable."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")

            config = make_training_config(
                training_examples_path=str(training_file),
                output_dir=str(tmpdir_path / "output"),
            )
            examples = tuple(make_training_example(f"ex_{i}") for i in range(10))
            plan = TrainingPipelineSkeleton.create_training_plan(config, examples)
            preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)
            run_plan = TrainingPipelineSkeleton.create_training_run_plan(plan, preflight)

            with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
                run_plan.ready_for_execution = False

    def test_run_plan_validates_plan_id_match(self):
        """Test that run_plan validates plan_id matches between plan and preflight."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")

            config = make_training_config(
                training_examples_path=str(training_file),
                output_dir=str(tmpdir_path / "output"),
            )
            examples = tuple(make_training_example(f"ex_{i}") for i in range(10))
            plan = TrainingPipelineSkeleton.create_training_plan(config, examples)
            preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)

            # Create different plan with different ID
            plan2 = TrainingPipelineSkeleton.create_training_plan(config, examples)

            # Try to create run_plan with mismatched IDs
            with pytest.raises(ValueError, match="plan_id mismatch"):
                TrainingPipelineSkeleton.create_training_run_plan(plan2, preflight)

    def test_run_plan_rejects_ready_with_failed_preflight(self):
        """Test that run_plan rejects ready_for_execution=True with failed preflight."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")

            config = make_training_config(
                training_examples_path=str(training_file),
                output_dir=str(tmpdir_path / "output"),
            )

            # Create example with disallowed operation (will fail preflight)
            examples = (
                make_training_example(operation=TraceConsumerOperation.SUGGEST_REPAIR),
            )
            plan = TrainingPipelineSkeleton.create_training_plan(config, examples)
            preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)

            # Preflight should have failed
            assert preflight.passed is False

            # Create run_plan (should have ready_for_execution=False)
            run_plan = TrainingPipelineSkeleton.create_training_run_plan(plan, preflight)
            assert run_plan.ready_for_execution is False

            # Manually try to create run_plan with ready=True despite failed preflight
            with pytest.raises(ValueError, match="Constitutional violation"):
                TrainingRunPlan(
                    run_plan_id="run_plan_test",
                    plan_id=plan.plan_id,
                    plan_candidate=plan,
                    preflight_report=preflight,
                    ready_for_execution=True,  # Invalid: preflight failed
                    constitutional_constraints=CONSTITUTIONAL_CONSTRAINTS,
                )

    def test_run_plan_requires_constitutional_constraints(self):
        """Test that run_plan requires constitutional_constraints."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")

            config = make_training_config(
                training_examples_path=str(training_file),
                output_dir=str(tmpdir_path / "output"),
            )
            examples = tuple(make_training_example(f"ex_{i}") for i in range(10))
            plan = TrainingPipelineSkeleton.create_training_plan(config, examples)
            preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)

            with pytest.raises(ValueError, match="must declare constitutional_constraints"):
                TrainingRunPlan(
                    run_plan_id="run_plan_test",
                    plan_id=plan.plan_id,
                    plan_candidate=plan,
                    preflight_report=preflight,
                    ready_for_execution=False,
                    constitutional_constraints=frozenset(),  # Invalid: empty
                )


# ============================================================================
# Constitutional Constraints Tests
# ============================================================================

class TestConstitutionalConstraints:
    """Test constitutional constraints are enforced."""

    def test_constitutional_constraints_present(self):
        """Test that CONSTITUTIONAL_CONSTRAINTS is non-empty."""
        assert len(CONSTITUTIONAL_CONSTRAINTS) > 0

    def test_constitutional_constraints_forbid_training(self):
        """Test that constraints forbid training execution."""
        assert "NO_TRAINING_EXECUTION" in CONSTITUTIONAL_CONSTRAINTS

    def test_constitutional_constraints_forbid_model_loading(self):
        """Test that constraints forbid model loading."""
        assert "NO_MODEL_LOADING" in CONSTITUTIONAL_CONSTRAINTS

    def test_constitutional_constraints_forbid_inference(self):
        """Test that constraints forbid inference execution."""
        assert "NO_INFERENCE_EXECUTION" in CONSTITUTIONAL_CONSTRAINTS

    def test_constitutional_constraints_forbid_rank_upgrade(self):
        """Test that constraints forbid rank upgrade."""
        assert "NO_RANK_UPGRADE" in CONSTITUTIONAL_CONSTRAINTS

    def test_constitutional_constraints_forbid_hukm_production(self):
        """Test that constraints forbid hukm production."""
        assert "NO_HUKM_PRODUCTION" in CONSTITUTIONAL_CONSTRAINTS

    def test_constitutional_constraints_enforce_plan_only(self):
        """Test that constraints enforce plan-only, not authority."""
        assert "PLAN_ONLY_NOT_AUTHORITY" in CONSTITUTIONAL_CONSTRAINTS

    def test_run_plan_preserves_all_constraints(self):
        """Test that TrainingRunPlan preserves all constitutional constraints."""
        with TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            training_file = tmpdir_path / "examples.jsonl"
            training_file.write_text("", encoding="utf-8")

            config = make_training_config(
                training_examples_path=str(training_file),
                output_dir=str(tmpdir_path / "output"),
            )
            examples = tuple(make_training_example(f"ex_{i}") for i in range(10))
            plan = TrainingPipelineSkeleton.create_training_plan(config, examples)
            preflight = TrainingPipelineSkeleton.run_preflight_checks(plan, examples)
            run_plan = TrainingPipelineSkeleton.create_training_run_plan(plan, preflight)

            # Verify all constraints preserved
            assert run_plan.constitutional_constraints == CONSTITUTIONAL_CONSTRAINTS
            assert "NO_TRAINING_EXECUTION" in run_plan.constitutional_constraints
            assert "NO_MODEL_LOADING" in run_plan.constitutional_constraints
            assert "PLAN_ONLY_NOT_AUTHORITY" in run_plan.constitutional_constraints
