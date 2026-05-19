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
from .case_signs import (
    CaseSignFamily,
    CaseSignValue,
    CaseSignPotential,
    CaseSignResidualType,
)
from .type_ids import (
    NounTypeID,
    VerbTypeID,
    ParticleTypeID,
    CompositeTypeID,
)
from .presyntax_vector import PreSyntaxMufradVector
from .sentence_frame import (
    FrameType,
    SentenceFrameCandidate,
    NominalFrameCandidate,
    VerbalFrameCandidate,
    ParticleLedFrameCandidate,
    FragmentFrameCandidate,
    UnresolvedFrameCandidate,
    calculate_frame_rank,
    collect_inherited_residuals,
)
from .frame_builder import (
    FrameBuilder,
    build_sentence_frames,
)
from .case_sign_matrix import (
    CaseCompatibilityFamily,
    SurfaceSignObservation,
    CaseSignMatrixRow,
    CaseSignMatrixTrace,
    CaseSignMatrix,
    CaseSignMatrixBuilder,
    build_case_sign_matrix,
)
from .operator_trigger import (
    OperatorTriggerFamily,
    TriggerSource,
    OperatorTriggerTrace,
    OperatorTriggerPotential,
    OperatorTriggerPotentialBuilder,
    build_operator_trigger_potential,
)

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
    # Case signs and type IDs
    "CaseSignFamily",
    "CaseSignValue",
    "CaseSignPotential",
    "CaseSignResidualType",
    "NounTypeID",
    "VerbTypeID",
    "ParticleTypeID",
    "CompositeTypeID",
    "PreSyntaxMufradVector",
    # Sentence frames
    "FrameType",
    "SentenceFrameCandidate",
    "NominalFrameCandidate",
    "VerbalFrameCandidate",
    "ParticleLedFrameCandidate",
    "FragmentFrameCandidate",
    "UnresolvedFrameCandidate",
    "calculate_frame_rank",
    "collect_inherited_residuals",
    "FrameBuilder",
    "build_sentence_frames",
    # CaseSignMatrix (PR #13)
    "CaseCompatibilityFamily",
    "SurfaceSignObservation",
    "CaseSignMatrixRow",
    "CaseSignMatrixTrace",
    "CaseSignMatrix",
    "CaseSignMatrixBuilder",
    "build_case_sign_matrix",
    # OperatorTriggerPotential (PR #14)
    "OperatorTriggerFamily",
    "TriggerSource",
    "OperatorTriggerTrace",
    "OperatorTriggerPotential",
    "OperatorTriggerPotentialBuilder",
    "build_operator_trigger_potential",
]
