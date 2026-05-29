"""
Tests for Governed T5 Integration Skeleton (PR #150)

Constitutional Testing Laws:
    1. Test that skeleton declares dependencies, does NOT load models
    2. Test that skeleton defines boundaries, does NOT execute inference
    3. Test that skeleton validates contracts, does NOT train models
    4. Test constitutional guards prevent forbidden operations
    5. Test preflight checks detect execution markers
    6. Test immutability of all data structures
    7. Test no rank upgrade, no residual resolution, no ifādah closure
"""

import pytest

from dal_core.governed_t5_integration_skeleton import (
    GovernedT5IntegrationConfig,
    ModelDependencyDeclaration,
    AdapterBoundaryPlan,
    NoExecutionIntegrationReport,
    IntegrationPreflightCheck,
    IntegrationPreflightReport,
    GovernedT5IntegrationSkeleton,
    ModelFamily,
    AdapterBoundaryType,
    IntegrationCheckType,
    IntegrationCheckStatus,
    FORBIDDEN_EXECUTION_MARKERS,
    INTEGRATION_CONSTITUTIONAL_CONSTRAINTS,
)
from dal_core.training_pipeline_skeleton import (
    TrainingPipelineConfig,
    TrainingPlanCandidate,
    ConstitutionalPreflightReport,
    PreflightCheckResult,
    PreflightCheckType,
    PreflightCheckStatus,
    TrainingRunPlan,
    TrainingMode,
    ModelArchitecture,
)
from dal_core.algorithm_trace_payload import TraceConsumerOperation


# ============================================================================
# Helper Functions
# ============================================================================

def make_training_run_plan(
    run_plan_id: str = "run_plan_test123",
    ready_for_execution: bool = True,
) -> TrainingRunPlan:
    """Create test TrainingRunPlan."""
    from pathlib import Path

    config = TrainingPipelineConfig(
        config_id="config_test123",
        training_examples_path="/tmp/test_examples.jsonl",
        model_architecture=ModelArchitecture.T5_BASE,
        training_mode=TrainingMode.EXPLANATION_GENERATION,
        max_input_length=512,
        max_target_length=128,
        batch_size=8,
        learning_rate=5e-5,
        num_epochs=3,
        output_dir="/tmp/output",
        allowed_operations=frozenset({TraceConsumerOperation.EXPLAIN_TRACE}),
    )

    plan_candidate = TrainingPlanCandidate(
        plan_id="plan_test123",
        config_id=config.config_id,
        config=config,
        total_examples=100,
        estimated_steps=100,
        estimated_duration_minutes=10,
        requires_preflight_check=True,
    )

    # Create preflight report
    checks = (
        PreflightCheckResult(
            check_type=PreflightCheckType.CONFIG_VALIDATION,
            status=PreflightCheckStatus.PASSED,
            message="Config valid",
        ),
    )

    preflight_report = ConstitutionalPreflightReport(
        report_id="preflight_test123",
        plan_id=plan_candidate.plan_id,
        checks=checks,
        passed=ready_for_execution,
        failed_checks_count=0 if ready_for_execution else 1,
        warning_checks_count=0,
    )

    return TrainingRunPlan(
        run_plan_id=run_plan_id,
        plan_id=plan_candidate.plan_id,
        plan_candidate=plan_candidate,
        preflight_report=preflight_report,
        ready_for_execution=ready_for_execution,
        constitutional_constraints=frozenset({
            "Training pipeline does NOT execute",
            "Training pipeline does NOT load models",
        }),
    )


def make_dependency_declaration(
    dependency_id: str = "dep_test123",
    model_family: ModelFamily = ModelFamily.T5_BASE,
) -> ModelDependencyDeclaration:
    """Create test ModelDependencyDeclaration."""
    return ModelDependencyDeclaration(
        dependency_id=dependency_id,
        model_family=model_family,
        required_transformers_version=">=4.30.0",
        required_torch_version=">=2.0.0",
        checkpoint_path=None,
        additional_requirements=(),
    )


def make_adapter_boundary(
    boundary_id: str = "boundary_test123",
    boundary_type: AdapterBoundaryType = AdapterBoundaryType.INPUT_ADAPTER,
) -> AdapterBoundaryPlan:
    """Create test AdapterBoundaryPlan."""
    return AdapterBoundaryPlan(
        boundary_id=boundary_id,
        boundary_type=boundary_type,
        input_contract_description="Input: TrainingRunPlan data",
        output_contract_description="Output: Model input format specification",
        constitutional_constraints=(
            "Preserve source_trace_id bindings",
            "Prevent authority claims",
            "Prevent rank upgrades",
        ),
        preserves_source_bindings=True,
        prevents_authority_claims=True,
        prevents_rank_upgrade=True,
    )


def make_integration_config(
    integration_id: str = "integration_test123",
    training_run_plan_id: str = "plan_test123",
) -> GovernedT5IntegrationConfig:
    """Create test GovernedT5IntegrationConfig."""
    return GovernedT5IntegrationConfig(
        integration_id=integration_id,
        training_run_plan_id=training_run_plan_id,
        dependency_declaration=make_dependency_declaration(),
        input_adapter_boundary=make_adapter_boundary(
            boundary_id="input_boundary",
            boundary_type=AdapterBoundaryType.INPUT_ADAPTER,
        ),
        output_adapter_boundary=make_adapter_boundary(
            boundary_id="output_boundary",
            boundary_type=AdapterBoundaryType.OUTPUT_ADAPTER,
        ),
        validation_adapter_boundary=make_adapter_boundary(
            boundary_id="validation_boundary",
            boundary_type=AdapterBoundaryType.VALIDATION_ADAPTER,
        ),
        constitutional_constraints=INTEGRATION_CONSTITUTIONAL_CONSTRAINTS,
    )


# ============================================================================
# ModelDependencyDeclaration Tests
# ============================================================================

class TestModelDependencyDeclaration:
    """Test ModelDependencyDeclaration immutable container."""

    def test_valid_dependency_creation(self):
        """Test creating valid ModelDependencyDeclaration."""
        dep = make_dependency_declaration()

        assert dep.dependency_id == "dep_test123"
        assert dep.model_family == ModelFamily.T5_BASE
        assert dep.required_transformers_version == ">=4.30.0"
        assert dep.required_torch_version == ">=2.0.0"

    def test_dependency_immutable(self):
        """Test ModelDependencyDeclaration is immutable."""
        dep = make_dependency_declaration()

        with pytest.raises(Exception):  # FrozenInstanceError or AttributeError
            dep.dependency_id = "modified"

    def test_dependency_requires_id(self):
        """Test ModelDependencyDeclaration requires dependency_id."""
        with pytest.raises(ValueError, match="requires dependency_id"):
            ModelDependencyDeclaration(
                dependency_id="",
                model_family=ModelFamily.T5_BASE,
                required_transformers_version=">=4.30.0",
            )

    def test_dependency_requires_transformers_version(self):
        """Test ModelDependencyDeclaration requires transformers version."""
        with pytest.raises(ValueError, match="requires required_transformers_version"):
            ModelDependencyDeclaration(
                dependency_id="dep_test",
                model_family=ModelFamily.T5_BASE,
                required_transformers_version="",
            )

    def test_dependency_is_data_not_import(self):
        """Test dependency declaration is data, NOT actual import."""
        dep = make_dependency_declaration()

        # Verify these are strings/enums, NOT imported modules
        assert isinstance(dep.model_family, ModelFamily)
        assert isinstance(dep.required_transformers_version, str)
        assert dep.model_family.value == "t5-base"  # String value, not module


# ============================================================================
# AdapterBoundaryPlan Tests
# ============================================================================

class TestAdapterBoundaryPlan:
    """Test AdapterBoundaryPlan immutable container."""

    def test_valid_boundary_creation(self):
        """Test creating valid AdapterBoundaryPlan."""
        boundary = make_adapter_boundary()

        assert boundary.boundary_id == "boundary_test123"
        assert boundary.boundary_type == AdapterBoundaryType.INPUT_ADAPTER
        assert boundary.preserves_source_bindings is True
        assert boundary.prevents_authority_claims is True
        assert boundary.prevents_rank_upgrade is True

    def test_boundary_immutable(self):
        """Test AdapterBoundaryPlan is immutable."""
        boundary = make_adapter_boundary()

        with pytest.raises(Exception):
            boundary.boundary_id = "modified"

    def test_boundary_requires_id(self):
        """Test AdapterBoundaryPlan requires boundary_id."""
        with pytest.raises(ValueError, match="requires boundary_id"):
            AdapterBoundaryPlan(
                boundary_id="",
                boundary_type=AdapterBoundaryType.INPUT_ADAPTER,
                input_contract_description="Input",
                output_contract_description="Output",
                constitutional_constraints=("constraint",),
                preserves_source_bindings=True,
                prevents_authority_claims=True,
                prevents_rank_upgrade=True,
            )

    def test_boundary_must_preserve_source_bindings(self):
        """Test AdapterBoundaryPlan must preserve source bindings."""
        with pytest.raises(ValueError, match="must preserve_source_bindings"):
            AdapterBoundaryPlan(
                boundary_id="boundary_test",
                boundary_type=AdapterBoundaryType.INPUT_ADAPTER,
                input_contract_description="Input",
                output_contract_description="Output",
                constitutional_constraints=("constraint",),
                preserves_source_bindings=False,  # Violation
                prevents_authority_claims=True,
                prevents_rank_upgrade=True,
            )

    def test_boundary_must_prevent_authority_claims(self):
        """Test AdapterBoundaryPlan must prevent authority claims."""
        with pytest.raises(ValueError, match="must prevent_authority_claims"):
            AdapterBoundaryPlan(
                boundary_id="boundary_test",
                boundary_type=AdapterBoundaryType.INPUT_ADAPTER,
                input_contract_description="Input",
                output_contract_description="Output",
                constitutional_constraints=("constraint",),
                preserves_source_bindings=True,
                prevents_authority_claims=False,  # Violation
                prevents_rank_upgrade=True,
            )

    def test_boundary_must_prevent_rank_upgrade(self):
        """Test AdapterBoundaryPlan must prevent rank upgrades."""
        with pytest.raises(ValueError, match="must prevent_rank_upgrade"):
            AdapterBoundaryPlan(
                boundary_id="boundary_test",
                boundary_type=AdapterBoundaryType.INPUT_ADAPTER,
                input_contract_description="Input",
                output_contract_description="Output",
                constitutional_constraints=("constraint",),
                preserves_source_bindings=True,
                prevents_authority_claims=True,
                prevents_rank_upgrade=False,  # Violation
            )


# ============================================================================
# GovernedT5IntegrationConfig Tests
# ============================================================================

class TestGovernedT5IntegrationConfig:
    """Test GovernedT5IntegrationConfig immutable container."""

    def test_valid_config_creation(self):
        """Test creating valid GovernedT5IntegrationConfig."""
        config = make_integration_config()

        assert config.integration_id == "integration_test123"
        assert config.training_run_plan_id == "plan_test123"
        assert config.dependency_declaration is not None
        assert config.input_adapter_boundary is not None
        assert config.output_adapter_boundary is not None
        assert config.validation_adapter_boundary is not None

    def test_config_immutable(self):
        """Test GovernedT5IntegrationConfig is immutable."""
        config = make_integration_config()

        with pytest.raises(Exception):
            config.integration_id = "modified"

    def test_config_requires_integration_id(self):
        """Test GovernedT5IntegrationConfig requires integration_id."""
        with pytest.raises(ValueError, match="requires integration_id"):
            GovernedT5IntegrationConfig(
                integration_id="",
                training_run_plan_id="plan_test",
                dependency_declaration=make_dependency_declaration(),
                input_adapter_boundary=make_adapter_boundary(
                    boundary_type=AdapterBoundaryType.INPUT_ADAPTER
                ),
                output_adapter_boundary=make_adapter_boundary(
                    boundary_type=AdapterBoundaryType.OUTPUT_ADAPTER
                ),
                validation_adapter_boundary=make_adapter_boundary(
                    boundary_type=AdapterBoundaryType.VALIDATION_ADAPTER
                ),
                constitutional_constraints=("constraint",),
            )

    def test_config_validates_adapter_types(self):
        """Test GovernedT5IntegrationConfig validates adapter types."""
        with pytest.raises(ValueError, match="must be INPUT_ADAPTER type"):
            GovernedT5IntegrationConfig(
                integration_id="integration_test",
                training_run_plan_id="plan_test",
                dependency_declaration=make_dependency_declaration(),
                input_adapter_boundary=make_adapter_boundary(
                    boundary_type=AdapterBoundaryType.OUTPUT_ADAPTER  # Wrong type
                ),
                output_adapter_boundary=make_adapter_boundary(
                    boundary_type=AdapterBoundaryType.OUTPUT_ADAPTER
                ),
                validation_adapter_boundary=make_adapter_boundary(
                    boundary_type=AdapterBoundaryType.VALIDATION_ADAPTER
                ),
                constitutional_constraints=("constraint",),
            )

    def test_config_has_no_forbidden_fields(self):
        """Test config has NO forbidden execution fields."""
        config = make_integration_config()

        # Verify these forbidden fields do NOT exist
        assert not hasattr(config, 'loaded_model')
        assert not hasattr(config, 'tokenizer')
        assert not hasattr(config, 'trainer')
        assert not hasattr(config, 'inference_results')
        assert not hasattr(config, 'training_metrics')
        assert not hasattr(config, 'upgraded_rank')
        assert not hasattr(config, 'produced_hukm')


# ============================================================================
# Integration Preflight Tests
# ============================================================================

class TestIntegrationPreflight:
    """Test integration preflight validation."""

    def test_scan_detects_forbidden_import_transformers(self):
        """Test scanner detects 'import transformers'."""
        text = "import transformers\nfrom transformers import T5"
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(text)

        assert "import transformers" in detected
        assert "from transformers import" in detected

    def test_scan_detects_forbidden_import_torch(self):
        """Test scanner detects 'import torch'."""
        text = "import torch\ntorch.cuda.is_available()"
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(text)

        assert "import torch" in detected
        assert "torch.cuda" in detected

    def test_scan_detects_from_pretrained(self):
        """Test scanner detects '.from_pretrained('."""
        text = "model = T5ForConditionalGeneration.from_pretrained('t5-base')"
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(text)

        assert ".from_pretrained(" in detected

    def test_scan_detects_generate(self):
        """Test scanner detects '.generate('."""
        text = "outputs = model.generate(inputs)"
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(text)

        assert ".generate(" in detected

    def test_scan_detects_trainer(self):
        """Test scanner detects 'Trainer('."""
        text = "trainer = Trainer(model=model, args=training_args)"
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(text)

        assert "Trainer(" in detected

    def test_scan_passes_for_declaration_only(self):
        """Test scanner passes for declaration-only code."""
        text = """
        model_name = "t5-base"
        required_version = ">=4.30.0"
        checkpoint_path = "/path/to/checkpoint"
        """
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(text)

        assert len(detected) == 0

    def test_scan_case_insensitive_import_transformers(self):
        """Test scanner detects case variations of 'import transformers'."""
        text = "IMPORT TRANSFORMERS"
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(text)

        assert "import transformers" in detected

    def test_scan_case_insensitive_import_torch(self):
        """Test scanner detects case variations of 'import torch'."""
        text = "Import Torch"
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(text)

        assert "import torch" in detected

    def test_scan_case_insensitive_from_pretrained(self):
        """Test scanner detects case variations of '.from_pretrained('."""
        text = "model = T5.FROM_PRETRAINED('t5-base')"
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(text)

        assert ".from_pretrained(" in detected

    def test_scan_case_insensitive_trainer(self):
        """Test scanner detects case variations of 'Trainer('."""
        text = "trainer = TRAINER(model=model)"
        detected = GovernedT5IntegrationSkeleton.scan_for_execution_markers(text)

        assert "Trainer(" in detected

    def test_preflight_passes_for_valid_config(self):
        """Test preflight passes for valid integration config."""
        config = make_integration_config()
        report = GovernedT5IntegrationSkeleton.run_preflight_checks(config)

        assert report.all_checks_passed is True
        assert len(report.critical_violations) == 0

    def test_preflight_fails_for_forbidden_markers(self):
        """Test preflight fails when forbidden markers detected."""
        config = make_integration_config()
        scan_text = "import transformers\nmodel.from_pretrained('t5-base')"

        report = GovernedT5IntegrationSkeleton.run_preflight_checks(
            config, scan_text=scan_text
        )

        assert report.all_checks_passed is False
        assert len(report.critical_violations) > 0
        assert "import transformers" in report.critical_violations

    def test_preflight_checks_all_types(self):
        """Test preflight runs all check types (with scan_text)."""
        config = make_integration_config()
        scan_text = "# Clean code with no violations"
        report = GovernedT5IntegrationSkeleton.run_preflight_checks(config, scan_text=scan_text)

        check_types = {check.check_type for check in report.checks}
        # Should have all 7 check types when scan_text is provided
        assert IntegrationCheckType.DEPENDENCY_DECLARATION in check_types
        assert IntegrationCheckType.NO_FORBIDDEN_IMPORTS in check_types
        assert IntegrationCheckType.NO_MODEL_LOADING in check_types
        assert IntegrationCheckType.NO_INFERENCE_EXECUTION in check_types
        assert IntegrationCheckType.NO_TRAINING_EXECUTION in check_types
        assert IntegrationCheckType.ADAPTER_BOUNDARY_VALID in check_types
        assert IntegrationCheckType.CONSTITUTIONAL_CONSTRAINTS in check_types
        assert len(check_types) == 7

    def test_preflight_checks_all_types_without_scan_text(self):
        """Test preflight runs all check types even without scan_text."""
        config = make_integration_config()
        report = GovernedT5IntegrationSkeleton.run_preflight_checks(config, scan_text=None)

        check_types = {check.check_type for check in report.checks}
        # Should have all 7 check types even without scan_text
        assert IntegrationCheckType.DEPENDENCY_DECLARATION in check_types
        assert IntegrationCheckType.NO_FORBIDDEN_IMPORTS in check_types
        assert IntegrationCheckType.NO_MODEL_LOADING in check_types
        assert IntegrationCheckType.NO_INFERENCE_EXECUTION in check_types
        assert IntegrationCheckType.NO_TRAINING_EXECUTION in check_types
        assert IntegrationCheckType.ADAPTER_BOUNDARY_VALID in check_types
        assert IntegrationCheckType.CONSTITUTIONAL_CONSTRAINTS in check_types
        assert len(check_types) == 7

        # Execution-scan checks should be PASSED with declaration-only message
        for check in report.checks:
            if check.check_type in (
                IntegrationCheckType.NO_FORBIDDEN_IMPORTS,
                IntegrationCheckType.NO_MODEL_LOADING,
                IntegrationCheckType.NO_INFERENCE_EXECUTION,
                IntegrationCheckType.NO_TRAINING_EXECUTION,
            ):
                assert check.status == IntegrationCheckStatus.PASSED
                assert "declaration-only preflight" in check.message


# ============================================================================
# NoExecutionIntegrationReport Tests
# ============================================================================

class TestNoExecutionIntegrationReport:
    """Test NoExecutionIntegrationReport."""

    def test_valid_report_creation(self):
        """Test creating valid NoExecutionIntegrationReport."""
        config = make_integration_config()
        preflight = GovernedT5IntegrationSkeleton.run_preflight_checks(config)
        report = GovernedT5IntegrationSkeleton.create_integration_report(
            config, preflight
        )

        assert report.integration_config_id == config.integration_id
        assert report.dependencies_declared_not_loaded is True
        assert report.boundaries_defined_not_implemented is True
        assert report.no_model_loading_detected is True
        assert report.no_training_execution_detected is True
        assert report.no_inference_execution_detected is True

    def test_report_immutable(self):
        """Test NoExecutionIntegrationReport is immutable."""
        config = make_integration_config()
        preflight = GovernedT5IntegrationSkeleton.run_preflight_checks(config)
        report = GovernedT5IntegrationSkeleton.create_integration_report(
            config, preflight
        )

        with pytest.raises(Exception):
            report.report_id = "modified"

    def test_report_requires_no_execution_confirmations(self):
        """Test report requires all no-execution confirmations."""
        config = make_integration_config()
        preflight = GovernedT5IntegrationSkeleton.run_preflight_checks(config)

        with pytest.raises(ValueError, match="Must confirm dependencies_declared_not_loaded"):
            NoExecutionIntegrationReport(
                report_id="report_test",
                integration_config_id=config.integration_id,
                preflight_report=preflight,
                dependencies_declared_not_loaded=False,  # Violation
                boundaries_defined_not_implemented=True,
                no_model_loading_detected=True,
                no_training_execution_detected=True,
                no_inference_execution_detected=True,
                integration_contract_valid=True,
            )

    def test_report_has_no_forbidden_fields(self):
        """Test report has NO forbidden execution fields."""
        config = make_integration_config()
        preflight = GovernedT5IntegrationSkeleton.run_preflight_checks(config)
        report = GovernedT5IntegrationSkeleton.create_integration_report(
            config, preflight
        )

        # Verify these forbidden fields do NOT exist
        assert not hasattr(report, 'model_loaded')
        assert not hasattr(report, 'training_executed')
        assert not hasattr(report, 'inference_executed')
        assert not hasattr(report, 'metrics_computed')
        assert not hasattr(report, 'rank_upgraded')
        assert not hasattr(report, 'hukm_produced')


# ============================================================================
# GovernedT5IntegrationSkeleton Tests
# ============================================================================

class TestGovernedT5IntegrationSkeleton:
    """Test GovernedT5IntegrationSkeleton validation logic."""

    def test_validate_valid_config(self):
        """Test validating valid integration config."""
        config = make_integration_config()
        is_valid, violations = GovernedT5IntegrationSkeleton.validate_integration_config(
            config
        )

        assert is_valid is True
        assert len(violations) == 0


# ============================================================================
# Constitutional Constraints Tests
# ============================================================================

class TestConstitutionalConstraints:
    """Test constitutional constraints and boundaries."""

    def test_integration_has_constitutional_constraints(self):
        """Test integration config has constitutional constraints."""
        config = make_integration_config()

        assert len(config.constitutional_constraints) > 0
        assert any("does NOT load models" in c for c in config.constitutional_constraints)
        assert any("does NOT execute inference" in c for c in config.constitutional_constraints)

    def test_forbidden_markers_defined(self):
        """Test forbidden execution markers are defined."""
        assert len(FORBIDDEN_EXECUTION_MARKERS) > 0
        assert "import transformers" in FORBIDDEN_EXECUTION_MARKERS
        assert "import torch" in FORBIDDEN_EXECUTION_MARKERS
        assert ".from_pretrained(" in FORBIDDEN_EXECUTION_MARKERS
        assert ".generate(" in FORBIDDEN_EXECUTION_MARKERS

    def test_no_rank_upgrade_methods(self):
        """Test integration skeleton has NO rank upgrade methods."""
        skeleton = GovernedT5IntegrationSkeleton()

        assert not hasattr(skeleton, 'upgrade_rank')
        assert not hasattr(skeleton, 'promote_rank')
        assert not hasattr(skeleton, 'increase_rank')

    def test_no_residual_resolution_methods(self):
        """Test integration skeleton has NO residual resolution methods."""
        skeleton = GovernedT5IntegrationSkeleton()

        assert not hasattr(skeleton, 'resolve_residuals')
        assert not hasattr(skeleton, 'delete_residuals')
        assert not hasattr(skeleton, 'discharge_residuals')

    def test_no_ifadah_closure_methods(self):
        """Test integration skeleton has NO ifādah closure methods."""
        skeleton = GovernedT5IntegrationSkeleton()

        assert not hasattr(skeleton, 'close_ifadah')
        assert not hasattr(skeleton, 'complete_ifadah')
        assert not hasattr(skeleton, 'finalize_ifadah')

    def test_no_hukm_production_methods(self):
        """Test integration skeleton has NO hukm production methods."""
        skeleton = GovernedT5IntegrationSkeleton()

        assert not hasattr(skeleton, 'produce_hukm')
        assert not hasattr(skeleton, 'create_hukm')
        assert not hasattr(skeleton, 'generate_hukm')

    def test_no_reality_production_methods(self):
        """Test integration skeleton has NO reality production methods."""
        skeleton = GovernedT5IntegrationSkeleton()

        assert not hasattr(skeleton, 'produce_reality')
        assert not hasattr(skeleton, 'create_reality')
        assert not hasattr(skeleton, 'establish_reality')


# ============================================================================
# Integration Flow Tests
# ============================================================================

class TestIntegrationFlow:
    """Test complete integration flow."""

    def test_complete_integration_flow(self):
        """Test complete integration validation flow."""
        # Step 1: Create integration config
        config = make_integration_config()
        assert config is not None

        # Step 2: Run preflight checks
        preflight = GovernedT5IntegrationSkeleton.run_preflight_checks(config)
        assert preflight.all_checks_passed is True

        # Step 3: Create integration report
        report = GovernedT5IntegrationSkeleton.create_integration_report(
            config, preflight
        )
        assert report.integration_contract_valid is True
        assert report.no_model_loading_detected is True
        assert report.no_training_execution_detected is True
        assert report.no_inference_execution_detected is True

    def test_integration_flow_with_violations(self):
        """Test integration flow detects violations."""
        # Step 1: Create config
        config = make_integration_config()

        # Step 2: Run preflight with forbidden code
        scan_text = "import transformers\nmodel = T5.from_pretrained('t5-base')"
        preflight = GovernedT5IntegrationSkeleton.run_preflight_checks(
            config, scan_text=scan_text
        )

        assert preflight.all_checks_passed is False
        assert len(preflight.critical_violations) > 0

        # Step 3: Create report (still validates contract structure)
        report = GovernedT5IntegrationSkeleton.create_integration_report(
            config, preflight
        )

        # Report confirms no execution (because we only scanned text, didn't execute)
        # But detection flags now correctly reflect that markers WERE found
        assert report.no_model_loading_detected is False  # Markers were detected
        assert report.no_training_execution_detected is True  # No training markers

        # Contract is invalid due to preflight failures
        assert report.integration_contract_valid is False

    def test_integration_report_reflects_model_loading_detection(self):
        """Test integration report correctly sets no_model_loading_detected=False when markers found."""
        config = make_integration_config()
        scan_text = "model = T5.from_pretrained('t5-base')"
        preflight = GovernedT5IntegrationSkeleton.run_preflight_checks(
            config, scan_text=scan_text
        )
        report = GovernedT5IntegrationSkeleton.create_integration_report(
            config, preflight
        )

        # Model loading markers were detected
        assert report.no_model_loading_detected is False
        assert report.integration_contract_valid is False

    def test_integration_report_reflects_training_detection(self):
        """Test integration report correctly sets no_training_execution_detected=False when markers found."""
        config = make_integration_config()
        scan_text = "trainer = Trainer(model=model, args=args)"
        preflight = GovernedT5IntegrationSkeleton.run_preflight_checks(
            config, scan_text=scan_text
        )
        report = GovernedT5IntegrationSkeleton.create_integration_report(
            config, preflight
        )

        # Training markers were detected
        assert report.no_training_execution_detected is False
        assert report.integration_contract_valid is False

    def test_integration_report_reflects_inference_detection(self):
        """Test integration report correctly sets no_inference_execution_detected=False when markers found."""
        config = make_integration_config()
        scan_text = "outputs = model.generate(inputs)"
        preflight = GovernedT5IntegrationSkeleton.run_preflight_checks(
            config, scan_text=scan_text
        )
        report = GovernedT5IntegrationSkeleton.create_integration_report(
            config, preflight
        )

        # Inference markers were detected
        assert report.no_inference_execution_detected is False
        assert report.integration_contract_valid is False


# ============================================================================
# Factory Method Tests
# ============================================================================

class TestFactoryMethod:
    """Test create_integration_config_from_run_plan factory method."""

    def test_factory_creates_valid_config_from_run_plan(self):
        """Test factory creates valid config from ready TrainingRunPlan."""
        run_plan = make_training_run_plan(ready_for_execution=True)
        dependency_declaration = make_dependency_declaration()
        input_boundary = make_adapter_boundary(
            boundary_id="input_boundary",
            boundary_type=AdapterBoundaryType.INPUT_ADAPTER,
        )
        output_boundary = make_adapter_boundary(
            boundary_id="output_boundary",
            boundary_type=AdapterBoundaryType.OUTPUT_ADAPTER,
        )
        validation_boundary = make_adapter_boundary(
            boundary_id="validation_boundary",
            boundary_type=AdapterBoundaryType.VALIDATION_ADAPTER,
        )

        config = GovernedT5IntegrationSkeleton.create_integration_config_from_run_plan(
            run_plan=run_plan,
            dependency_declaration=dependency_declaration,
            input_adapter_boundary=input_boundary,
            output_adapter_boundary=output_boundary,
            validation_adapter_boundary=validation_boundary,
        )

        assert config.training_run_plan_id == run_plan.run_plan_id
        assert config.integration_id == f"integration_{run_plan.run_plan_id}"
        assert config.dependency_declaration == dependency_declaration

    def test_factory_rejects_not_ready_run_plan(self):
        """Test factory rejects TrainingRunPlan not ready for execution."""
        run_plan = make_training_run_plan(ready_for_execution=False)
        dependency_declaration = make_dependency_declaration()
        input_boundary = make_adapter_boundary(
            boundary_type=AdapterBoundaryType.INPUT_ADAPTER
        )
        output_boundary = make_adapter_boundary(
            boundary_type=AdapterBoundaryType.OUTPUT_ADAPTER
        )
        validation_boundary = make_adapter_boundary(
            boundary_type=AdapterBoundaryType.VALIDATION_ADAPTER
        )

        with pytest.raises(ValueError, match="is not ready_for_execution"):
            GovernedT5IntegrationSkeleton.create_integration_config_from_run_plan(
                run_plan=run_plan,
                dependency_declaration=dependency_declaration,
                input_adapter_boundary=input_boundary,
                output_adapter_boundary=output_boundary,
                validation_adapter_boundary=validation_boundary,
            )

    def test_factory_preserves_run_plan_id(self):
        """Test factory preserves run_plan_id in training_run_plan_id."""
        custom_id = "custom_run_plan_xyz"
        run_plan = make_training_run_plan(
            run_plan_id=custom_id,
            ready_for_execution=True,
        )
        dependency_declaration = make_dependency_declaration()

        config = GovernedT5IntegrationSkeleton.create_integration_config_from_run_plan(
            run_plan=run_plan,
            dependency_declaration=dependency_declaration,
            input_adapter_boundary=make_adapter_boundary(
                boundary_type=AdapterBoundaryType.INPUT_ADAPTER
            ),
            output_adapter_boundary=make_adapter_boundary(
                boundary_type=AdapterBoundaryType.OUTPUT_ADAPTER
            ),
            validation_adapter_boundary=make_adapter_boundary(
                boundary_type=AdapterBoundaryType.VALIDATION_ADAPTER
            ),
        )

        assert config.training_run_plan_id == custom_id
        assert config.integration_id == f"integration_{custom_id}"

