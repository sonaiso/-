"""
DomainSpec - مواصفة المجال

Every thinking style operates within a specific domain.
No style can operate outside its domain boundary.

Nabhani Core Principle:
    المجال يحدد نطاق التفكير
    The domain determines the scope of thinking.

Critical Laws:
    1. Every domain has specific boundaries
    2. No domain jump without bridge
    3. Domain determines evidence requirements
    4. Domain determines allowed operations
    5. Domain determines residual handling

Domains (Initial Declaration):
    MATERIAL_EXPERIMENTAL - Physical reality, experiments, measurements
    FORMAL_LOGICAL - Abstract logic, formal systems, proofs
    LAFZI_DALALI - Linguistic meaning, دال/مدلول, وضع/استعمال
    TEXTUAL_NORMATIVE - Textual sources, نصوص, أحكام شرعية
    PROGRAMMING_EXECUTION - Code, algorithms, computational execution
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ThinkingDomain(Enum):
    """
    Domains of rational thinking - مجالات التفكير العقلي

    Each domain represents a distinct realm of reality with
    its own evidence requirements, operations, and constraints.
    """

    # Material domain - المجال المادي
    MATERIAL_EXPERIMENTAL = "material_experimental"

    # Formal domain - المجال الصوري
    FORMAL_LOGICAL = "formal_logical"

    # Linguistic domain - المجال اللفظي الدلالي
    LAFZI_DALALI = "lafzi_dalali"

    # Textual/normative domain - المجال النصي الشرعي
    TEXTUAL_NORMATIVE = "textual_normative"

    # Programming/execution domain - المجال البرمجي التنفيذي
    PROGRAMMING_EXECUTION = "programming_execution"


class EvidenceKind(Enum):
    """
    Types of evidence valid in different domains.

    Evidence requirements vary by domain.
    """

    # Sensory evidence (material domain)
    SENSORY = "sensory"
    MEASUREMENT = "measurement"
    OBSERVATION = "observation"

    # Formal evidence (logical domain)
    AXIOM = "axiom"
    PROOF = "proof"
    DERIVATION = "derivation"

    # Linguistic evidence (lafzi domain)
    WADH = "wadh"  # وضع لغوي
    ISTIMAL = "istimal"  # استعمال
    QARYNAH = "qarynah"  # قرينة

    # Textual evidence (normative domain)
    NASS = "nass"  # نص
    IJMA = "ijma"  # إجماع
    QIYAS = "qiyas"  # قياس

    # Computational evidence (programming domain)
    EXECUTION = "execution"
    TYPE_CHECK = "type_check"
    ASSERTION = "assertion"


@dataclass(frozen=True)
class DomainBoundary:
    """
    Defines the boundary conditions for a domain.

    Boundaries prevent unauthorized domain jumps.
    """
    domain: ThinkingDomain
    description: str

    # Evidence requirements
    required_evidence_kinds: frozenset[EvidenceKind]

    # Forbidden evidence (evidence from other domains not valid here)
    forbidden_evidence_kinds: frozenset[EvidenceKind]

    def allows_evidence(self, evidence_kind: EvidenceKind) -> bool:
        """Check if this evidence kind is allowed in this domain."""
        return (
            evidence_kind in self.required_evidence_kinds
            and evidence_kind not in self.forbidden_evidence_kinds
        )

    def blocks_evidence(self, evidence_kind: EvidenceKind) -> bool:
        """Check if this evidence kind is blocked in this domain."""
        return evidence_kind in self.forbidden_evidence_kinds


@dataclass(frozen=True)
class DomainSpec:
    """
    Complete specification of a thinking domain.

    DomainSpec is declaration only - it does not execute reasoning.
    DomainSpec defines constraints, not operations.

    Critical Laws:
        - DomainSpec does NOT implement ScientificMethod
        - DomainSpec does NOT implement LogicalStyle
        - DomainSpec does NOT implement LafziMadlul
        - DomainSpec does NOT issue judgment
        - DomainSpec does NOT certify claims
        - DomainSpec only declares boundaries and requirements
    """
    domain: ThinkingDomain
    name_ar: str  # Arabic name
    name_en: str  # English name
    boundary: DomainBoundary
    description: str

    # Domain cannot operate without these
    requires_reality: bool = True
    requires_sensory_transfer: bool = True
    requires_cognitive_carrier: bool = True
    requires_prior_information: bool = True

    def __post_init__(self):
        """Validate domain spec construction."""
        if self.boundary.domain != self.domain:
            raise ValueError(
                f"DomainSpec domain {self.domain} does not match "
                f"boundary domain {self.boundary.domain}"
            )

    def is_compatible_with(self, other: DomainSpec) -> bool:
        """
        Check if two domains can coexist in same reasoning chain.

        Different domains can coexist if bridged properly.
        This only checks compatibility, not actual bridge existence.
        """
        # Same domain always compatible
        if self.domain == other.domain:
            return True

        # Different domains need bridge (not implemented here)
        # This is declaration only
        return False

    def blocks_domain_jump_to(self, target: ThinkingDomain) -> bool:
        """
        Check if jumping to target domain is blocked.

        Without bridge, all domain jumps are blocked.
        """
        return self.domain != target


# Domain Registry (Declaration Only)
# These are the initially declared domains
# Implementation is NOT part of this PR

def make_material_experimental_domain() -> DomainSpec:
    """Create Material/Experimental domain specification."""
    boundary = DomainBoundary(
        domain=ThinkingDomain.MATERIAL_EXPERIMENTAL,
        description="Physical reality requiring sensory evidence",
        required_evidence_kinds=frozenset([
            EvidenceKind.SENSORY,
            EvidenceKind.MEASUREMENT,
            EvidenceKind.OBSERVATION,
        ]),
        forbidden_evidence_kinds=frozenset([
            EvidenceKind.AXIOM,  # Cannot use pure logic in physical domain
            EvidenceKind.NASS,   # Cannot use textual evidence for physical claims
        ])
    )

    return DomainSpec(
        domain=ThinkingDomain.MATERIAL_EXPERIMENTAL,
        name_ar="المجال المادي التجريبي",
        name_en="Material Experimental Domain",
        boundary=boundary,
        description="Domain of physical reality, experiments, and measurements",
        requires_reality=True,
        requires_sensory_transfer=True,
        requires_cognitive_carrier=True,
        requires_prior_information=True,
    )


def make_formal_logical_domain() -> DomainSpec:
    """Create Formal/Logical domain specification."""
    boundary = DomainBoundary(
        domain=ThinkingDomain.FORMAL_LOGICAL,
        description="Abstract logic requiring formal proofs",
        required_evidence_kinds=frozenset([
            EvidenceKind.AXIOM,
            EvidenceKind.PROOF,
            EvidenceKind.DERIVATION,
        ]),
        forbidden_evidence_kinds=frozenset([
            EvidenceKind.MEASUREMENT,  # Cannot measure abstract entities
            EvidenceKind.NASS,  # Textual evidence not valid for logic
        ])
    )

    return DomainSpec(
        domain=ThinkingDomain.FORMAL_LOGICAL,
        name_ar="المجال الصوري المنطقي",
        name_en="Formal Logical Domain",
        boundary=boundary,
        description="Domain of abstract logic, formal systems, and proofs",
        requires_reality=False,  # Logic doesn't require physical reality
        requires_sensory_transfer=False,  # Logic doesn't require senses
        requires_cognitive_carrier=True,
        requires_prior_information=True,
    )


def make_lafzi_dalali_domain() -> DomainSpec:
    """
    Create Lafzi/Dalali domain specification.

    This is DECLARATION ONLY.
    Implementation of LafziMadlul is NOT part of this PR.
    """
    boundary = DomainBoundary(
        domain=ThinkingDomain.LAFZI_DALALI,
        description="Linguistic meaning through وضع and استعمال",
        required_evidence_kinds=frozenset([
            EvidenceKind.WADH,
            EvidenceKind.ISTIMAL,
            EvidenceKind.QARYNAH,
        ]),
        forbidden_evidence_kinds=frozenset([
            EvidenceKind.MEASUREMENT,  # Cannot measure meaning
            EvidenceKind.PROOF,  # Meaning is not formal proof
        ])
    )

    return DomainSpec(
        domain=ThinkingDomain.LAFZI_DALALI,
        name_ar="المجال اللفظي الدلالي",
        name_en="Lafzi Dalali Domain",
        boundary=boundary,
        description="Domain of linguistic meaning, دال/مدلول, وضع/استعمال",
        requires_reality=True,  # Language refers to reality
        requires_sensory_transfer=True,  # Language requires hearing/seeing
        requires_cognitive_carrier=True,
        requires_prior_information=True,
    )


def make_textual_normative_domain() -> DomainSpec:
    """Create Textual/Normative domain specification."""
    boundary = DomainBoundary(
        domain=ThinkingDomain.TEXTUAL_NORMATIVE,
        description="Textual sources and شرعي rulings",
        required_evidence_kinds=frozenset([
            EvidenceKind.NASS,
            EvidenceKind.IJMA,
            EvidenceKind.QIYAS,
        ]),
        forbidden_evidence_kinds=frozenset([
            EvidenceKind.MEASUREMENT,  # Rulings not measured
            EvidenceKind.EXECUTION,  # Rulings not executed like code
        ])
    )

    return DomainSpec(
        domain=ThinkingDomain.TEXTUAL_NORMATIVE,
        name_ar="المجال النصي الشرعي",
        name_en="Textual Normative Domain",
        boundary=boundary,
        description="Domain of textual sources, نصوص, أحكام شرعية",
        requires_reality=True,
        requires_sensory_transfer=True,
        requires_cognitive_carrier=True,
        requires_prior_information=True,
    )


def make_programming_execution_domain() -> DomainSpec:
    """Create Programming/Execution domain specification."""
    boundary = DomainBoundary(
        domain=ThinkingDomain.PROGRAMMING_EXECUTION,
        description="Code execution and computational verification",
        required_evidence_kinds=frozenset([
            EvidenceKind.EXECUTION,
            EvidenceKind.TYPE_CHECK,
            EvidenceKind.ASSERTION,
        ]),
        forbidden_evidence_kinds=frozenset([
            EvidenceKind.NASS,  # Code not validated by text
            EvidenceKind.IJMA,  # Code not validated by consensus
        ])
    )

    return DomainSpec(
        domain=ThinkingDomain.PROGRAMMING_EXECUTION,
        name_ar="المجال البرمجي التنفيذي",
        name_en="Programming Execution Domain",
        boundary=boundary,
        description="Domain of code, algorithms, and computational execution",
        requires_reality=True,  # Code executes in real systems
        requires_sensory_transfer=True,  # Results observed through I/O
        requires_cognitive_carrier=True,
        requires_prior_information=True,
    )
