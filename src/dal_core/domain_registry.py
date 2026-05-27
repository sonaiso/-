"""
Domain Registry (سجل المجالات)

AlgebraicDecisionCore Component: Domain classification and boundary enforcement.

Purpose:
    Define and enforce domain boundaries for all Arabic linguistic operations.
    Every decision, judgment, or classification must occur within a defined domain.

Architecture Position:
    AlgebraicDecisionCore
        └── DomainRegistry (this module)

Governing Law:
    لا حكم خارج مجاله
    No judgment outside its domain.

Critical Distinctions:
    صيغة فاعل (WeightDomain) ≠ الفاعل النحوي (SyntaxDomain) ≠ معنى الفاعلية (SemanticsDomain)

    Weight pattern "فاعل" is a morphological form.
    Syntactic "فاعل" is a functional relation (agent of verb).
    Semantic "فاعل" is the meaning (who performs the action).

    These are THREE DIFFERENT domains and must NOT be conflated.

Forbidden Cross-Domain Leaps:
    - No meaning determination in morphological domain
    - No syntactic judgment in phonological domain
    - No root extraction in semantic domain
    - No i'rab assignment in weight domain

PR: ALGEBRAIC-DECISION-CORE
Created: 2026-05-26
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import FrozenSet, Optional, Tuple, Dict
from types import MappingProxyType


# ============================================================================
# Domain Type Classification
# ============================================================================

class DomainType(Enum):
    """
    Complete classification of domains in Arabic linguistic analysis.

    Each domain has clear boundaries and specific competencies.
    Cross-domain judgments are forbidden.
    """
    # Surface and Script Domains (U₀-U₁)
    SCRIPT_DOMAIN = auto()                      # مجال الخط
    SOUND_DOMAIN = auto()                       # مجال الصوت

    # Phonological Domains (U₂)
    SYLLABLE_DOMAIN = auto()                    # مجال المقطع
    BOUNDARY_DOMAIN = auto()                    # مجال الحد

    # Lexical Unit Domain (U₄)
    LAFZ_DOMAIN = auto()                        # مجال اللفظ

    # Surface Protection Domains (U₇)
    MARKER_PROTECTION_DOMAIN = auto()           # مجال حماية العلامات
    CLAUSE_AGREEMENT_DOMAIN = auto()            # مجال الاتفاق الجملي

    # Morphological Domains (U₈-U₉)
    ROOT_STEM_DOMAIN = auto()                   # مجال الجذر والجذع
    WEIGHT_DOMAIN = auto()                      # مجال الوزن

    # Identity Domain (U₅-U₆)
    IDENTITY_DOMAIN = auto()                    # مجال محور الهوية (Ism/Fi'l/Harf)

    # Derivational Domains (U₁₀+)
    SOURCE_FORM_DOMAIN = auto()                 # مجال صيغة المصدر
    ATTRIBUTE_FORM_DOMAIN = auto()              # مجال صيغة الصفة
    FUNCTIONAL_FORM_DOMAIN = auto()             # مجال الصيغة الوظيفية
    WORDFORM_DOMAIN = auto()                    # مجال صورة الكلمة المرشحة

    # Syntactic Domains (U₁₃+)
    AMIL_RELATION_DOMAIN = auto()               # مجال علاقة العامل
    I3RAB_SURFACE_DOMAIN = auto()               # مجال سطح الإعراب
    SYNTAX_DOMAIN = auto()                      # مجال النحو

    # Semantic Domains (U₁₄-U₁₅)
    SEMANTICS_DOMAIN = auto()                   # مجال الدلالة
    PRAGMATICS_DOMAIN = auto()                  # مجال التداول

    # Meta-Domains
    EVIDENCE_DOMAIN = auto()                    # مجال الدليل
    JUDGMENT_DOMAIN = auto()                    # مجال الحكم


class DomainLayer(Enum):
    """Layer assignment for domains (parallel to execution layers)."""
    SCRIPT_LAYER = 0
    SOUND_LAYER = 2
    BOUNDARY_LAYER = 3
    LAFZ_LAYER = 4
    PROTECTION_LAYER = 7
    MORPHOLOGY_LAYER = 8
    DERIVATION_LAYER = 10
    SYNTAX_LAYER = 13
    SEMANTICS_LAYER = 14
    JUDGMENT_LAYER = 15


@dataclass(frozen=True)
class DomainSpec:
    """
    Specification for one domain.

    Attributes:
        domain_type: The domain classification
        arabic_name: Arabic name
        layer: Primary layer where this domain operates
        competencies: What this domain can determine
        prohibitions: What this domain CANNOT determine
        requires_domains: Domains that must be completed before this one
        allows_transition_to: Domains this can transition to
    """
    domain_type: DomainType
    arabic_name: str
    layer: DomainLayer
    competencies: FrozenSet[str] = frozenset()
    prohibitions: FrozenSet[str] = frozenset()
    requires_domains: FrozenSet[DomainType] = frozenset()
    allows_transition_to: FrozenSet[DomainType] = frozenset()

    def can_determine(self, competency: str) -> bool:
        """Check if this domain has competency to make a determination."""
        return competency in self.competencies

    def is_prohibited(self, determination: str) -> bool:
        """Check if a determination is prohibited in this domain."""
        return determination in self.prohibitions


# ============================================================================
# Domain Registry - Immutable Catalog
# ============================================================================

class DomainRegistry:
    """
    Immutable registry of all domains in the Arabic linguistic pipeline.

    Provides:
        - Domain specifications and boundaries
        - Competency checking (what can be determined in each domain)
        - Prohibition enforcement (what CANNOT be determined)
        - Cross-domain validation

    Immutability:
        - Backed by MappingProxyType
        - No runtime additions
        - All specs are frozen dataclasses

    Usage:
        registry = DomainRegistry()
        spec = registry.get_spec(DomainType.WEIGHT_DOMAIN)
        can_determine = spec.can_determine("root_pattern")
        is_forbidden = spec.is_prohibited("meaning")
    """

    def __init__(self):
        """Initialize domain registry with all domain specifications."""
        self._specs: Dict[DomainType, DomainSpec] = {}
        self._build_registry()
        self._specs = MappingProxyType(self._specs)

    def _build_registry(self) -> None:
        """Build complete domain registry with specifications."""

        # Script Domain (U₀)
        self._add_spec(DomainSpec(
            domain_type=DomainType.SCRIPT_DOMAIN,
            arabic_name="مجال الخط",
            layer=DomainLayer.SCRIPT_LAYER,
            competencies=frozenset({
                "unicode_validation",
                "character_classification",
                "combining_marks"
            }),
            prohibitions=frozenset({
                "phonetic_value",
                "syllable_structure",
                "morphological_analysis",
                "syntactic_role",
                "meaning",
                "i3rab"
            }),
            allows_transition_to=frozenset({DomainType.SOUND_DOMAIN})
        ))

        # Sound Domain (U₂)
        self._add_spec(DomainSpec(
            domain_type=DomainType.SOUND_DOMAIN,
            arabic_name="مجال الصوت",
            layer=DomainLayer.SOUND_LAYER,
            competencies=frozenset({
                "phoneme_classification",
                "phonetic_feature",
                "consonant_vowel"
            }),
            prohibitions=frozenset({
                "morphological_analysis",
                "syntactic_role",
                "meaning",
                "i3rab",
                "root",
                "weight"
            }),
            requires_domains=frozenset({DomainType.SCRIPT_DOMAIN}),
            allows_transition_to=frozenset({DomainType.SYLLABLE_DOMAIN})
        ))

        # Syllable Domain (U₂s)
        self._add_spec(DomainSpec(
            domain_type=DomainType.SYLLABLE_DOMAIN,
            arabic_name="مجال المقطع",
            layer=DomainLayer.SOUND_LAYER,
            competencies=frozenset({
                "syllable_structure",
                "cv_pattern",
                "onset_nucleus_coda"
            }),
            prohibitions=frozenset({
                "word_boundary",
                "morphological_analysis",
                "syntactic_role",
                "meaning",
                "i3rab",
                "root",
                "weight"
            }),
            requires_domains=frozenset({DomainType.SOUND_DOMAIN}),
            allows_transition_to=frozenset({DomainType.BOUNDARY_DOMAIN})
        ))

        # Boundary Domain (U₃)
        self._add_spec(DomainSpec(
            domain_type=DomainType.BOUNDARY_DOMAIN,
            arabic_name="مجال الحد",
            layer=DomainLayer.BOUNDARY_LAYER,
            competencies=frozenset({
                "word_boundary_detection",
                "clitic_attachment",
                "prefix_suffix_identification"
            }),
            prohibitions=frozenset({
                "morphological_analysis",
                "syntactic_role",
                "meaning",
                "i3rab",
                "root",
                "weight",
                "functional_role"
            }),
            requires_domains=frozenset({DomainType.SYLLABLE_DOMAIN}),
            allows_transition_to=frozenset({DomainType.LAFZ_DOMAIN})
        ))

        # Lafz Domain (U₄)
        self._add_spec(DomainSpec(
            domain_type=DomainType.LAFZ_DOMAIN,
            arabic_name="مجال اللفظ",
            layer=DomainLayer.LAFZ_LAYER,
            competencies=frozenset({
                "word_unit_identity",
                "true_singular_lafz",
                "surface_potential",
                "definiteness_hint",
                "quantity_hint"
            }),
            prohibitions=frozenset({
                "root_extraction",
                "weight_assignment",
                "syntactic_role",
                "meaning",
                "i3rab",
                "functional_relation"
            }),
            requires_domains=frozenset({DomainType.BOUNDARY_DOMAIN}),
            allows_transition_to=frozenset({
                DomainType.MARKER_PROTECTION_DOMAIN,
                DomainType.CLAUSE_AGREEMENT_DOMAIN
            })
        ))

        # Marker Protection Domain (U₇-B)
        self._add_spec(DomainSpec(
            domain_type=DomainType.MARKER_PROTECTION_DOMAIN,
            arabic_name="مجال حماية العلامات",
            layer=DomainLayer.PROTECTION_LAYER,
            competencies=frozenset({
                "marker_identification",
                "marker_protection",
                "tanwin_detection",
                "alif_lam_detection",
                "pronoun_suffix_detection"
            }),
            prohibitions=frozenset({
                "root_extraction",
                "weight_assignment",
                "syntactic_role",
                "meaning",
                "i3rab_judgment"  # Marker ≠ i3rab judgment
            }),
            requires_domains=frozenset({DomainType.LAFZ_DOMAIN}),
            allows_transition_to=frozenset({
                DomainType.CLAUSE_AGREEMENT_DOMAIN
            })
        ))

        # Clause Agreement Domain (U₇-C)
        self._add_spec(DomainSpec(
            domain_type=DomainType.CLAUSE_AGREEMENT_DOMAIN,
            arabic_name="مجال الاتفاق الجملي",
            layer=DomainLayer.PROTECTION_LAYER,
            competencies=frozenset({
                "agreement_detection",
                "gender_contract",
                "number_contract",
                "rationality_contract",
                "broken_plural_guard"
            }),
            prohibitions=frozenset({
                "root_extraction",  # Agreement ≠ root
                "weight_assignment",  # Agreement ≠ weight
                "syntactic_role",  # Agreement ≠ function
                "meaning",  # Agreement ≠ semantics
                "i3rab_judgment"  # Agreement ≠ i3rab
            }),
            requires_domains=frozenset({
                DomainType.MARKER_PROTECTION_DOMAIN
            }),
            allows_transition_to=frozenset({
                DomainType.ROOT_STEM_DOMAIN
            })
        ))

        # Root/Stem Domain (U₈)
        self._add_spec(DomainSpec(
            domain_type=DomainType.ROOT_STEM_DOMAIN,
            arabic_name="مجال الجذر والجذع",
            layer=DomainLayer.MORPHOLOGY_LAYER,
            competencies=frozenset({
                "root_candidate_extraction",
                "stem_candidate_extraction",
                "radical_count",
                "weak_radical_detection"
            }),
            prohibitions=frozenset({
                "root_certification",  # U₈ gives CANDIDATES not CERTIFICATES
                "weight_assignment",  # Weight comes after root
                "syntactic_role",
                "meaning",
                "i3rab"
            }),
            requires_domains=frozenset({
                DomainType.CLAUSE_AGREEMENT_DOMAIN
            }),
            allows_transition_to=frozenset({
                DomainType.WEIGHT_DOMAIN
            })
        ))

        # Weight Domain (U₉)
        self._add_spec(DomainSpec(
            domain_type=DomainType.WEIGHT_DOMAIN,
            arabic_name="مجال الوزن",
            layer=DomainLayer.MORPHOLOGY_LAYER,
            competencies=frozenset({
                "weight_pattern",
                "morphological_template",
                "faa_ayn_lam_mapping"
            }),
            prohibitions=frozenset({
                "syntactic_role",  # فاعل weight ≠ فاعل syntax
                "meaning",  # Weight ≠ meaning
                "i3rab",
                "functional_relation"
            }),
            requires_domains=frozenset({
                DomainType.ROOT_STEM_DOMAIN
            }),
            allows_transition_to=frozenset({
                DomainType.IDENTITY_DOMAIN,
                DomainType.SOURCE_FORM_DOMAIN,
                DomainType.ATTRIBUTE_FORM_DOMAIN,
                DomainType.FUNCTIONAL_FORM_DOMAIN
            })
        ))

        # Identity Domain (U₅-U₆) - محور الهوية
        # PR-127: Path-aware prerequisites
        # Arabic identity determination has multiple paths:
        # 1. Weight path: WEIGHT_DOMAIN → IDENTITY_DOMAIN (derived forms: فاعل، مفعول...)
        # 2. Mabni path: LAFZ_DOMAIN → IDENTITY_DOMAIN (closed-class: ما، هل، إن...)
        # 3. Tool path: LAFZ_DOMAIN → IDENTITY_DOMAIN (particles: في، على، من...)
        # 4. Pronoun path: LAFZ_DOMAIN → IDENTITY_DOMAIN (pronouns: هو، أنت...)
        # 5. Jāmid path: LAFZ_DOMAIN → IDENTITY_DOMAIN (frozen nouns, non-weighted)
        #
        # Constitutional law: No Identity from weight alone for all paths.
        # Remove unconditional WEIGHT_DOMAIN requirement.
        self._add_spec(DomainSpec(
            domain_type=DomainType.IDENTITY_DOMAIN,
            arabic_name="مجال محور الهوية",
            layer=DomainLayer.DERIVATION_LAYER,
            competencies=frozenset({
                "ism_fil_harf_classification",  # اسم/فعل/حرف
                "functional_role_determination",  # U₅
                "mabni_closed_class_determination",  # U₆
                "word_category_classification"
            }),
            prohibitions=frozenset({
                "syntactic_role",  # Identity ≠ syntactic function
                "meaning",  # Identity ≠ meaning
                "i3rab",  # Identity ≠ i3rab judgment
                "case_assignment",
                "semantic_interpretation"
            }),
            requires_domains=frozenset(),  # Path-aware: validated at transition time
            allows_transition_to=frozenset({
                DomainType.WORDFORM_DOMAIN
            })
        ))

        # Source Form Domain (مصدر)
        self._add_spec(DomainSpec(
            domain_type=DomainType.SOURCE_FORM_DOMAIN,
            arabic_name="مجال صيغة المصدر",
            layer=DomainLayer.DERIVATION_LAYER,
            competencies=frozenset({
                "source_form_pattern",
                "qiyasi_masdar",
                "samaa_i_masdar",
                "ism_masdar"
            }),
            prohibitions=frozenset({
                "mafool_mutlaq_relation",  # Form ≠ syntactic relation
                "meaning",  # Form ≠ meaning
                "syntactic_role"
            }),
            requires_domains=frozenset({DomainType.WEIGHT_DOMAIN}),
            allows_transition_to=frozenset({
                DomainType.SYNTAX_DOMAIN
            })
        ))

        # Attribute Form Domain (صفة)
        self._add_spec(DomainSpec(
            domain_type=DomainType.ATTRIBUTE_FORM_DOMAIN,
            arabic_name="مجال صيغة الصفة",
            layer=DomainLayer.DERIVATION_LAYER,
            competencies=frozenset({
                "ism_faa_il_form",
                "ism_maf_ool_form",
                "sifa_mushabbaha_form",
                "sighat_mubaalagha_form"
            }),
            prohibitions=frozenset({
                "wasf_relation",  # صفة form ≠ نعت relation
                "agent_meaning",  # Form ≠ meaning
                "syntactic_role"
            }),
            requires_domains=frozenset({DomainType.WEIGHT_DOMAIN}),
            allows_transition_to=frozenset({
                DomainType.SYNTAX_DOMAIN
            })
        ))

        # Functional Form Domain
        self._add_spec(DomainSpec(
            domain_type=DomainType.FUNCTIONAL_FORM_DOMAIN,
            arabic_name="مجال الصيغة الوظيفية",
            layer=DomainLayer.DERIVATION_LAYER,
            competencies=frozenset({
                "form_classification",
                "derivational_pattern"
            }),
            prohibitions=frozenset({
                "syntactic_role",
                "meaning",
                "i3rab"
            }),
            requires_domains=frozenset({DomainType.WEIGHT_DOMAIN}),
            allows_transition_to=frozenset({
                DomainType.WORDFORM_DOMAIN
            })
        ))

        # WordForm Domain (U₁₀) - صورة الكلمة المرشحة
        self._add_spec(DomainSpec(
            domain_type=DomainType.WORDFORM_DOMAIN,
            arabic_name="مجال صورة الكلمة المرشحة",
            layer=DomainLayer.DERIVATION_LAYER,
            competencies=frozenset({
                "word_form_candidate",
                "lexical_form_closed",
                "word_contract_holder",
                "jamid_mushtaq_classification",  # جامد/مشتق
                "mabni_murab_classification"  # مبني/معرب
            }),
            prohibitions=frozenset({
                "syntactic_role",  # WordForm ≠ syntactic function
                "meaning",  # WordForm ≠ meaning (no isolated word→meaning)
                "i3rab_judgment",  # WordForm ≠ i3rab judgment
                "compositional_relation",  # WordForm ≠ composition
                "ifadah",  # WordForm ≠ ifādah (no تمام الإفادة)
                "hukm"  # WordForm ≠ hukm (judgment)
            }),
            requires_domains=frozenset({
                DomainType.IDENTITY_DOMAIN
            }),
            allows_transition_to=frozenset({
                DomainType.SYNTAX_DOMAIN  # U₁₀ → U₁₁ (composition)
            })
        ))

        # Amil Relation Domain
        self._add_spec(DomainSpec(
            domain_type=DomainType.AMIL_RELATION_DOMAIN,
            arabic_name="مجال علاقة العامل",
            layer=DomainLayer.SYNTAX_LAYER,
            competencies=frozenset({
                "amil_identification",
                "maamul_identification",
                "expected_effect"
            }),
            prohibitions=frozenset({
                "meaning",  # Amil relation ≠ meaning
                "i3rab_certificate",  # Relation ≠ i3rab judgment
                "semantic_interpretation"
            }),
            requires_domains=frozenset({
                DomainType.FUNCTIONAL_FORM_DOMAIN
            }),
            allows_transition_to=frozenset({
                DomainType.I3RAB_SURFACE_DOMAIN
            })
        ))

        # I3rab Surface Domain
        self._add_spec(DomainSpec(
            domain_type=DomainType.I3RAB_SURFACE_DOMAIN,
            arabic_name="مجال سطح الإعراب",
            layer=DomainLayer.SYNTAX_LAYER,
            competencies=frozenset({
                "i3rab_marker_observation",
                "case_sign_potential",
                "expected_vs_observed"
            }),
            prohibitions=frozenset({
                "i3rab_judgment",  # Surface ≠ judgment
                "meaning",
                "semantic_interpretation"
            }),
            requires_domains=frozenset({
                DomainType.AMIL_RELATION_DOMAIN
            }),
            allows_transition_to=frozenset({
                DomainType.SYNTAX_DOMAIN
            })
        ))

        # Syntax Domain
        self._add_spec(DomainSpec(
            domain_type=DomainType.SYNTAX_DOMAIN,
            arabic_name="مجال النحو",
            layer=DomainLayer.SYNTAX_LAYER,
            competencies=frozenset({
                "syntactic_relation",
                "faa_il_maf_ool",  # NOW allowed (syntactic فاعل)
                "mubtada_khabar",
                "naat_badal_tawkid"
            }),
            prohibitions=frozenset({
                "meaning",  # Syntax ≠ meaning (CRITICAL)
                "semantic_interpretation",
                "pragmatic_interpretation",
                "intent",
                "reference_resolution"
            }),
            requires_domains=frozenset({
                DomainType.I3RAB_SURFACE_DOMAIN
            }),
            allows_transition_to=frozenset({
                DomainType.SEMANTICS_DOMAIN
            })
        ))

        # Semantics Domain
        self._add_spec(DomainSpec(
            domain_type=DomainType.SEMANTICS_DOMAIN,
            arabic_name="مجال الدلالة",
            layer=DomainLayer.SEMANTICS_LAYER,
            competencies=frozenset({
                "semantic_interpretation",
                "meaning_determination",
                "reference_resolution",
                "literal_metaphorical",
                "univocal_equivocal"
            }),
            prohibitions=frozenset({
                "pragmatic_interpretation",  # Semantics ≠ pragmatics
                "speaker_intent",
                "context_dependent_meaning"
            }),
            requires_domains=frozenset({
                DomainType.SYNTAX_DOMAIN
            }),
            allows_transition_to=frozenset({
                DomainType.PRAGMATICS_DOMAIN,
                DomainType.JUDGMENT_DOMAIN
            })
        ))

        # Pragmatics Domain
        self._add_spec(DomainSpec(
            domain_type=DomainType.PRAGMATICS_DOMAIN,
            arabic_name="مجال التداول",
            layer=DomainLayer.SEMANTICS_LAYER,
            competencies=frozenset({
                "pragmatic_interpretation",
                "context_dependent_meaning",
                "speech_act",
                "implicature"
            }),
            prohibitions=frozenset({
                "grammatical_judgment",  # Pragmatics ≠ grammar
                "morphological_analysis"
            }),
            requires_domains=frozenset({
                DomainType.SEMANTICS_DOMAIN
            }),
            allows_transition_to=frozenset({
                DomainType.JUDGMENT_DOMAIN
            })
        ))

        # Evidence Domain (meta-domain)
        self._add_spec(DomainSpec(
            domain_type=DomainType.EVIDENCE_DOMAIN,
            arabic_name="مجال الدليل",
            layer=DomainLayer.JUDGMENT_LAYER,
            competencies=frozenset({
                "evidence_collection",
                "evidence_validation",
                "proof_construction"
            }),
            prohibitions=frozenset({
                "judgment_without_evidence"
            }),
            requires_domains=frozenset(),
            allows_transition_to=frozenset({
                DomainType.JUDGMENT_DOMAIN
            })
        ))

        # Judgment Domain (terminal)
        self._add_spec(DomainSpec(
            domain_type=DomainType.JUDGMENT_DOMAIN,
            arabic_name="مجال الحكم",
            layer=DomainLayer.JUDGMENT_LAYER,
            competencies=frozenset({
                "final_judgment",
                "certification",
                "hukm_determination"
            }),
            prohibitions=frozenset(),  # Terminal domain
            requires_domains=frozenset({
                DomainType.EVIDENCE_DOMAIN
            }),
            allows_transition_to=frozenset()  # Terminal
        ))

    def _add_spec(self, spec: DomainSpec) -> None:
        """Add domain specification (internal use only)."""
        self._specs[spec.domain_type] = spec

    def get_spec(self, domain_type: DomainType) -> DomainSpec:
        """Get specification for a domain type."""
        return self._specs[domain_type]

    def can_determine_in_domain(
        self,
        domain_type: DomainType,
        competency: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Check if a competency can be determined in a domain.

        Args:
            domain_type: Domain to check
            competency: Competency/determination to validate

        Returns:
            (is_allowed, reason) tuple
        """
        spec = self.get_spec(domain_type)

        if spec.is_prohibited(competency):
            return False, f"{competency} is prohibited in {spec.arabic_name}"

        if spec.can_determine(competency):
            return True, None

        return False, f"{competency} not in competencies of {spec.arabic_name}"

    def validate_domain_transition(
        self,
        from_domain: DomainType,
        to_domain: DomainType
    ) -> Tuple[bool, Optional[str]]:
        """
        Validate transition from one domain to another.

        Args:
            from_domain: Source domain
            to_domain: Target domain

        Returns:
            (is_allowed, reason) tuple
        """
        from_spec = self.get_spec(from_domain)
        to_spec = self.get_spec(to_domain)

        # Check if transition is allowed
        if to_domain not in from_spec.allows_transition_to:
            return False, f"Transition from {from_spec.arabic_name} to {to_spec.arabic_name} not allowed"

        # Check if required domains are satisfied (would need context for full validation)
        # For now, just check the direct transition
        return True, None

    def get_layer(self, domain_type: DomainType) -> DomainLayer:
        """Get the layer where this domain operates."""
        return self.get_spec(domain_type).layer

    def get_prohibitions(self, domain_type: DomainType) -> FrozenSet[str]:
        """Get all prohibitions for a domain."""
        return self.get_spec(domain_type).prohibitions

    def get_competencies(self, domain_type: DomainType) -> FrozenSet[str]:
        """Get all competencies for a domain."""
        return self.get_spec(domain_type).competencies


# ============================================================================
# Guard Functions
# ============================================================================

def verify_domain_boundary(
    domain_type: DomainType,
    attempted_determination: str,
    registry: DomainRegistry
) -> Tuple[bool, Optional[str]]:
    """
    Verify that a determination respects domain boundaries.

    Args:
        domain_type: Domain where determination is attempted
        attempted_determination: What is being determined
        registry: Domain registry

    Returns:
        (is_valid, reason) tuple
    """
    spec = registry.get_spec(domain_type)

    # Check if explicitly prohibited
    if spec.is_prohibited(attempted_determination):
        return False, f"{attempted_determination} is forbidden in {spec.arabic_name}"

    # Check if in competencies
    if spec.can_determine(attempted_determination):
        return True, None

    # Not in competencies and not explicitly allowed
    return False, f"{attempted_determination} exceeds competency of {spec.arabic_name}"


__all__ = [
    "DomainType",
    "DomainLayer",
    "DomainSpec",
    "DomainRegistry",
    "verify_domain_boundary",
]
