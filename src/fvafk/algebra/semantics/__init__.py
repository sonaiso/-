"""
Phase 5: Dāl/Madlūl/Dalālah/Ifādah Algebra

This module implements the semantic layers between syntax (Phase 4) and
judgment (Phase 6).

Core Principle:
    الإفادة لا تبدأ من النحو مباشرة ولا من المعجم مباشرة
    (Ifādah does not begin directly from syntax or directly from lexicon.)

Architecture (9 subphases):
    5A: Dāl Algebra — Signifier candidates (dāl alone is not meaning)
    5B: Madlūl Algebra — Signified candidates (madlūl alone is not dalālah)
    5C: Wadh' Binding — Dāl/madlūl linking (no dalālah without binding)
    5D: Dalālah Gates — Mutābaqah, taḍammun, iltizām (pre-ifādah conditions)
    5E: Nisbah Semantic — Compositional semantics (iḍāfah ≠ ifādah)
    5F: Reference Resolution — Pronouns, ellipsis, jawāb
    5G: Speech Force — Khabar, inshā, amr, etc. (not HUKM)
    5H: Ifādah Closure — Semantic completion with residuals
    5I: Boundary Guards — Prevent SEMANTICS → HUKM jump

Hard Boundaries:
    - Dāl alone is NOT meaning
    - Madlūl alone is NOT dalālah
    - Mutābaqah/taḍammun/iltizām are NOT ifādah
    - Iḍāfah alone is NOT ifādah
    - Khabar is NOT hukm
    - Ifādah with residuals cannot be CERTIFIED
    - SEMANTICS cannot jump to HUKM
    - IFADAH cannot issue HUKM

Maps to Architecture Layers:
    A5: Wadh' Algebra
    A6: Madlul Algebra
    A7: Dalalah Algebra
    A8: Usage Algebra (partial)
    A9: Murad Algebra (partial)
"""

from .residual_taxonomy import (
    SEMANTICS_RESIDUAL_KINDS,
    make_polysemy_possible,
    make_dal_binding_absent,
    make_dalalah_gate_required,
    make_mutabaqah_insufficient,
    make_tadammun_insufficient,
    make_iltizam_gate_missing,
    make_idafah_not_ifadah,
    make_taqyid_incomplete,
    make_conditional_jawab_missing,
    make_pronoun_referent_missing,
    make_speech_force_uncertain,
    make_ifadah_incomplete,
    make_hukm_boundary_violation,
)

from .operations import (
    DalCandidateOperation,
    MadlulCandidateOperation,
    WadhBindingOperation,
    MutabaqahGate,
    TadammunGate,
    IltizamGate,
    NisbahSemanticOperation,
    ReferenceResolutionOperation,
    SpeechForceOperation,
    IfadahClosureOperation,
    BoundaryGuardOperation,
    # Convenience wrappers
    governed_dal_candidate,
    governed_madlul_candidate,
    governed_wadh_binding,
    governed_mutabaqah,
    governed_tadammun,
    governed_iltizam,
    governed_nisbah_semantic,
    governed_reference_resolution,
    governed_speech_force,
    governed_ifadah_closure,
    governed_boundary_guard,
)

__all__ = [
    # Residual kinds
    "SEMANTICS_RESIDUAL_KINDS",
    "make_polysemy_possible",
    "make_dal_binding_absent",
    "make_dalalah_gate_required",
    "make_mutabaqah_insufficient",
    "make_tadammun_insufficient",
    "make_iltizam_gate_missing",
    "make_idafah_not_ifadah",
    "make_taqyid_incomplete",
    "make_conditional_jawab_missing",
    "make_pronoun_referent_missing",
    "make_speech_force_uncertain",
    "make_ifadah_incomplete",
    "make_hukm_boundary_violation",
    # Operations
    "DalCandidateOperation",
    "MadlulCandidateOperation",
    "WadhBindingOperation",
    "MutabaqahGate",
    "TadammunGate",
    "IltizamGate",
    "NisbahSemanticOperation",
    "ReferenceResolutionOperation",
    "SpeechForceOperation",
    "IfadahClosureOperation",
    "BoundaryGuardOperation",
    # Convenience wrappers
    "governed_dal_candidate",
    "governed_madlul_candidate",
    "governed_wadh_binding",
    "governed_mutabaqah",
    "governed_tadammun",
    "governed_iltizam",
    "governed_nisbah_semantic",
    "governed_reference_resolution",
    "governed_speech_force",
    "governed_ifadah_closure",
    "governed_boundary_guard",
]
