"""Contract-governed dal-mufrad pipeline.

This package models lexical sign closure only (الدال المفرد),
without semantic meaning inference.
"""

from .pipeline import (
    Rank,
    Severity,
    Evidence,
    Residual,
    LexicalType,
    LexiconRecord,
    DForm,
    DLugha,
    DType,
    DMufrad,
    SEED_LEXICON,
    analyze_dal_mufrad,
    build_d_form,
    prove_lugha,
    infer_type,
    close_mufrad,
    atoms_from_text,
    attach_marks,
)

from .mufrad_proof import MufradProof
from .morph_features import (
    CandidateStatus,
    SegmentationProof,
    StemProof,
    CliticProof,
    RootCandidate,
    WaznCandidate,
    VerbFeatureProof,
    NounInflectionClass,
    ParticleOperatorPotential,
)
from .surface_effects import (
    SurfaceEffect,
    SurfaceEffectType,
    SurfaceEffectVisibility,
)
from .composition_readiness import CompositionReadiness
from .operator_contract import OperatorContract

__all__ = [
    "Rank",
    "Severity",
    "Evidence",
    "Residual",
    "LexicalType",
    "LexiconRecord",
    "DForm",
    "DLugha",
    "DType",
    "DMufrad",
    "SEED_LEXICON",
    "analyze_dal_mufrad",
    "build_d_form",
    "prove_lugha",
    "infer_type",
    "close_mufrad",
    "atoms_from_text",
    "attach_marks",
    # MufradProof and supporting types
    "MufradProof",
    "CandidateStatus",
    "SegmentationProof",
    "StemProof",
    "CliticProof",
    "RootCandidate",
    "WaznCandidate",
    "VerbFeatureProof",
    "NounInflectionClass",
    "ParticleOperatorPotential",
    "SurfaceEffect",
    "SurfaceEffectType",
    "SurfaceEffectVisibility",
    "CompositionReadiness",
    "OperatorContract",
]
