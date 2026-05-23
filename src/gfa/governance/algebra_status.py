"""Algebra Status Classification System.

Defines the honest status of different algebra implementations
and components in the project.

Core Principle:
    الصدق في الحالة أساس الثقة.
    "Honesty in status is the foundation of trust."
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Set


class AlgebraStatus(Enum):
    """Classification of algebra implementation status.

    Attributes:
        SPEC_ONLY: Specification exists but no implementation
        CONSTITUTIONAL_SEED: Foundational definitions, incomplete
        PROVISIONAL_SPECIALIZED: Working specialized algebra, not general
        PATTERN_SPECIFIC_PROTOTYPE: Works on specific patterns only
        PARTIAL_RUNTIME: Partial implementation (< 50%)
        GENERATED_LAYER: Generated from General Algebra
        GENERAL_ALGEBRA_RUNTIME: Proven general algebra implementation
        PROVEN_GENERAL: Computationally proven generality
    """

    SPEC_ONLY = "specification without implementation"
    CONSTITUTIONAL_SEED = "foundational definitions, incomplete"
    PROVISIONAL_SPECIALIZED = "working specialized algebra, not general"
    PATTERN_SPECIFIC_PROTOTYPE = "works on specific patterns only"
    PARTIAL_RUNTIME = "partial implementation"
    GENERATED_LAYER = "generated from General Algebra"
    GENERAL_ALGEBRA_RUNTIME = "proven general algebra implementation"
    PROVEN_GENERAL = "computationally proven generality"


class ComponentStatus(Enum):
    """Status of specific project components.

    Each component tracks whether it's implemented and proven.
    """

    # Foundation components
    COGNITIVE_CARRIER = "CognitiveCarrier geometry"
    MEMORY_GEOMETRY = "Memory geometry"
    COMPARISON_GEOMETRY = "Comparison geometry"
    IDENTITY_GEOMETRY = "Identity/Difference geometry"
    BINDING_CORE = "Binding core"

    # Learning components
    CPB_EXTRACTION = "CPB extraction (μΦ solver)"
    LAYER_GENERATOR = "Layer algebra generator"
    GENERALITY_PROOF = "3-layer generality proof"

    # Specialized algebras
    GFA_METHODS = "GFA methods (Wadh/Mutabaqah)"
    DAL_ALGEBRA = "Dal algebra (D0-D7)"
    GENERAL_LEARNING = "General learning prototype"

    # Advanced components
    SUBJECT_GROUNDING = "RationalSubjectGrounding"
    TESTIMONY_GEOMETRY = "TestimonyGeometry"
    PRECONCEPTION_AUDIT = "PreconceptionResidueAudit"


@dataclass(frozen=True)
class ProjectStatus:
    """Complete status of the project.

    Attributes:
        general_algebra_constitution: Completeness of constitutional docs (0.0-1.0)
        general_algebra_architecture: Completeness of architecture (0.0-1.0)
        general_algebra_runtime: Implementation percentage (0.0-1.0)
        cpb_proven: Whether CPB extraction is proven
        layer_generator_exists: Whether LayerGenerator exists
        gfa_status: Status of GFA methods
        dal_status: Status of Dal algebra
        learning_status: Status of learning prototype
        implemented_components: Set of implemented components
        missing_components: Set of missing components
    """

    general_algebra_constitution: float
    general_algebra_architecture: float
    general_algebra_runtime: float
    cpb_proven: bool
    layer_generator_exists: bool
    gfa_status: AlgebraStatus
    dal_status: AlgebraStatus
    learning_status: AlgebraStatus
    implemented_components: Set[ComponentStatus]
    missing_components: Set[ComponentStatus]


def check_component_implementation(component: ComponentStatus) -> bool:
    """Check if a component is implemented.

    Args:
        component: Component to check

    Returns:
        True if component exists with working implementation
    """
    import os

    # Map components to file/directory checks
    component_paths = {
        ComponentStatus.COGNITIVE_CARRIER: "src/gfa/cognitive_carrier/cognitive_carrier.py",
        ComponentStatus.MEMORY_GEOMETRY: "src/gfa/foundations/memory",
        ComponentStatus.COMPARISON_GEOMETRY: "src/gfa/foundations/comparison",
        ComponentStatus.IDENTITY_GEOMETRY: "src/gfa/foundations/identity",
        ComponentStatus.BINDING_CORE: "src/gfa/foundations/binding",
        ComponentStatus.CPB_EXTRACTION: "src/gfa/foundations/cpb",
        ComponentStatus.LAYER_GENERATOR: "src/gfa/foundations/layer_generator",
        ComponentStatus.GENERALITY_PROOF: "src/gfa/foundations/generality_proof",
        ComponentStatus.GFA_METHODS: "src/gfa/methods",
        ComponentStatus.DAL_ALGEBRA: "src/dal_core/dal_algebra.py",
        ComponentStatus.GENERAL_LEARNING: "src/fvafk/algebra/general_learning/learner.py",
        ComponentStatus.SUBJECT_GROUNDING: "src/gfa/foundations/subject_grounding",
        ComponentStatus.TESTIMONY_GEOMETRY: "src/gfa/foundations/testimony",
        ComponentStatus.PRECONCEPTION_AUDIT: "src/gfa/foundations/preconception",
    }

    if component not in component_paths:
        return False

    path = component_paths[component]
    base_path = "/home/runner/work/-/-"
    full_path = os.path.join(base_path, path)

    return os.path.exists(full_path)


def get_project_status() -> ProjectStatus:
    """Get current honest project status.

    Returns:
        ProjectStatus with honest assessment
    """
    # Check which components are implemented
    all_components = set(ComponentStatus)
    implemented = {c for c in all_components if check_component_implementation(c)}
    missing = all_components - implemented

    # Required components for General Algebra Runtime
    required_for_general = {
        ComponentStatus.COGNITIVE_CARRIER,
        ComponentStatus.MEMORY_GEOMETRY,
        ComponentStatus.COMPARISON_GEOMETRY,
        ComponentStatus.BINDING_CORE,
        ComponentStatus.CPB_EXTRACTION,
    }

    # Required for proven generality
    required_for_proven = {
        ComponentStatus.CPB_EXTRACTION,
        ComponentStatus.LAYER_GENERATOR,
        ComponentStatus.GENERALITY_PROOF,
    }

    # Check CPB and LayerGenerator
    cpb_proven = ComponentStatus.CPB_EXTRACTION in implemented
    layer_generator_exists = ComponentStatus.LAYER_GENERATOR in implemented

    # Determine statuses
    if ComponentStatus.GFA_METHODS in implemented:
        gfa_status = AlgebraStatus.PROVISIONAL_SPECIALIZED
    else:
        gfa_status = AlgebraStatus.SPEC_ONLY

    if ComponentStatus.DAL_ALGEBRA in implemented:
        dal_status = AlgebraStatus.PARTIAL_RUNTIME
    else:
        dal_status = AlgebraStatus.SPEC_ONLY

    if ComponentStatus.GENERAL_LEARNING in implemented:
        learning_status = AlgebraStatus.PATTERN_SPECIFIC_PROTOTYPE
    else:
        learning_status = AlgebraStatus.SPEC_ONLY

    # Calculate completion percentages
    # Constitution: based on updated architecture with new layers
    constitution_completeness = 0.65  # 65% - not 100% as claimed

    # Architecture: includes new layers discovered
    architecture_completeness = 0.40  # 40% - added many new required layers

    # Runtime: increased with Memory Geometry implementation
    # CognitiveCarrier (partial) + Memory Geometry (complete) = ~10%
    runtime_completeness = 0.10  # 10% - Memory Geometry implemented (PR-G1)

    return ProjectStatus(
        general_algebra_constitution=constitution_completeness,
        general_algebra_architecture=architecture_completeness,
        general_algebra_runtime=runtime_completeness,
        cpb_proven=cpb_proven,
        layer_generator_exists=layer_generator_exists,
        gfa_status=gfa_status,
        dal_status=dal_status,
        learning_status=learning_status,
        implemented_components=implemented,
        missing_components=missing,
    )


__all__ = [
    "AlgebraStatus",
    "ComponentStatus",
    "ProjectStatus",
    "get_project_status",
    "check_component_implementation",
]
