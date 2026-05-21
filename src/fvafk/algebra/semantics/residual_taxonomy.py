"""
Phase 5 Semantic Residual Taxonomy

Defines the canonical set of residuals for the semantic layers (Phase 5A-5I).

These residuals capture incompleteness, ambiguity, and missing evidence
across the dāl → madlūl → dalālah → ifādah chain.

Residual Categories:
    - Dāl/Madlūl separation (5A-5C)
    - Dalālah insufficiency (5D)
    - Nisbah incompleteness (5E)
    - Reference missing (5F)
    - Speech force uncertainty (5G)
    - Ifādah incompleteness (5H)
    - Boundary violations (5I)
"""

from typing import Tuple, Optional
from ..core import Residual


# =============================================================================
# Canonical Residual Set (13 kinds)
# =============================================================================

SEMANTICS_RESIDUAL_KINDS: Tuple[str, ...] = (
    # Phase 5A-5C: Dāl/Madlūl/Binding
    "semantics.polysemy.possible",          # Dāl has multiple possible madlūl
    "semantics.dal_binding.absent",         # Madlūl not bound to dāl yet
    "semantics.dalalah_gate.required",      # Binding requires evidence

    # Phase 5D: Dalālah Gates
    "semantics.mutabaqah.insufficient",     # Mutābaqah alone ≠ ifādah
    "semantics.tadammun.insufficient",      # Taḍammun alone ≠ ifādah
    "semantics.iltizam.gate_missing",       # Iltizām requires explicit gate

    # Phase 5E: Nisbah Semantic
    "semantics.idafah.not_ifadah",          # Iḍāfah alone ≠ ifādah
    "semantics.taqyid.incomplete",          # Taqyīd incomplete without predication
    "semantics.conditional.jawab_missing",  # Conditional requires jawāb

    # Phase 5F: Reference Resolution
    "semantics.pronoun.referent_missing",   # Pronoun without referent

    # Phase 5G: Speech Force
    "semantics.speech_force.uncertain",     # Speech act type unclear

    # Phase 5H: Ifādah Closure
    "semantics.ifadah.incomplete",          # Ifādah requirements not met

    # Phase 5I: Boundary Guard
    "semantics.hukm_boundary.violation",    # Attempted SEMANTICS → HUKM jump
)


# =============================================================================
# Phase 5A-5C: Dāl/Madlūl/Binding Residuals
# =============================================================================

def make_polysemy_possible(term: str = "") -> Residual:
    """
    Dāl has multiple possible madlūl candidates.

    Law: الدال وحده ليس معنى (Dāl alone is not meaning)

    Args:
        term: The dāl (signifier) that has polysemy

    Returns:
        Residual indicating polysemy
    """
    return Residual(
        kind="semantics.polysemy.possible",
        detail=f"polysemy:{term}" if term else "polysemy:unspecified"
    )


def make_dal_binding_absent(madlul: str = "") -> Residual:
    """
    Madlūl candidate not bound to dāl yet.

    Law: المدلول وحده ليس دلالة (Madlūl alone is not dalālah)

    Args:
        madlul: The madlūl (signified) candidate

    Returns:
        Residual indicating missing binding
    """
    return Residual(
        kind="semantics.dal_binding.absent",
        detail=f"madlul:{madlul}" if madlul else "madlul:unbound"
    )


def make_dalalah_gate_required(evidence_type: str = "") -> Residual:
    """
    Dāl/madlūl binding requires evidence (wadh'/usage/context).

    Law: لا دلالة بلا ربط (No dalālah without binding)

    Args:
        evidence_type: Type of evidence required (wadh, usage, context)

    Returns:
        Residual indicating evidence requirement
    """
    return Residual(
        kind="semantics.dalalah_gate.required",
        detail=f"evidence:{evidence_type}" if evidence_type else "evidence:required"
    )


# =============================================================================
# Phase 5D: Dalālah Gate Residuals
# =============================================================================

def make_mutabaqah_insufficient() -> Residual:
    """
    Mutābaqah (direct correspondence) alone does not produce ifādah.

    Law: المطابقة لا تصبح إفادة وحدها (Mutābaqah does not become ifādah alone)

    Returns:
        Residual indicating mutābaqah insufficiency
    """
    return Residual(
        kind="semantics.mutabaqah.insufficient",
        detail="mutabaqah:pre_ifadah_condition"
    )


def make_tadammun_insufficient() -> Residual:
    """
    Taḍammun (partial inclusion) alone does not produce ifādah.

    Law: التضمن لا يصبح إفادة وحده (Taḍammun does not become ifādah alone)

    Returns:
        Residual indicating taḍammun insufficiency
    """
    return Residual(
        kind="semantics.tadammun.insufficient",
        detail="tadammun:pre_ifadah_condition"
    )


def make_iltizam_gate_missing(iltizam_type: str = "") -> Residual:
    """
    Iltizām (entailment) requires explicit gate, not automatic.

    Law: الالتزام ليس تلقائياً (Iltizām is not automatic)

    Args:
        iltizam_type: Type of entailment (logical, conventional, shariah, contextual)

    Returns:
        Residual indicating missing iltizām gate
    """
    return Residual(
        kind="semantics.iltizam.gate_missing",
        detail=f"iltizam:{iltizam_type}" if iltizam_type else "iltizam:gate_required"
    )


# =============================================================================
# Phase 5E: Nisbah Semantic Residuals
# =============================================================================

def make_idafah_not_ifadah(terms: str = "") -> Residual:
    """
    Iḍāfah relation alone does not become ifādah.

    Law: النسبة الإضافية لا تصبح إفادة (Iḍāfah relation does not become ifādah)

    Args:
        terms: The iḍāfah construction

    Returns:
        Residual indicating iḍāfah insufficiency
    """
    return Residual(
        kind="semantics.idafah.not_ifadah",
        detail=f"idafah:{terms}" if terms else "idafah:requires_predication"
    )


def make_taqyid_incomplete(modifier: str = "") -> Residual:
    """
    Taqyīd (modifier) incomplete without complete predication.

    Law: التقييد لا يصبح إفادة حتى يكمل الإسناد
    (Taqyīd does not become ifādah until predication completes)

    Args:
        modifier: The taqyīd element

    Returns:
        Residual indicating incomplete taqyīd
    """
    return Residual(
        kind="semantics.taqyid.incomplete",
        detail=f"taqyid:{modifier}" if modifier else "taqyid:awaits_predication"
    )


def make_conditional_jawab_missing() -> Residual:
    """
    Conditional without jawāb does not become ifādah.

    Law: الشرط بلا جواب لا يصبح إفادة
    (Conditional without jawāb does not become ifādah)

    Returns:
        Residual indicating missing jawāb
    """
    return Residual(
        kind="semantics.conditional.jawab_missing",
        detail="conditional:requires_jawab"
    )


# =============================================================================
# Phase 5F: Reference Resolution Residuals
# =============================================================================

def make_pronoun_referent_missing(pronoun: str = "") -> Residual:
    """
    Pronoun without referent cannot produce CERTIFIED ifādah.

    Law: الضمير بلا مرجع لا يصبح إفادة معتمدة
    (Pronoun without referent cannot become CERTIFIED ifādah)

    Args:
        pronoun: The pronoun

    Returns:
        Residual indicating missing referent
    """
    return Residual(
        kind="semantics.pronoun.referent_missing",
        detail=f"pronoun:{pronoun}" if pronoun else "pronoun:requires_referent"
    )


# =============================================================================
# Phase 5G: Speech Force Residuals
# =============================================================================

def make_speech_force_uncertain(candidates: str = "") -> Residual:
    """
    Speech force (khabar/inshā/amr/etc.) uncertain or ambiguous.

    Note: Even when determined, speech force does NOT become HUKM.

    Args:
        candidates: Possible speech force types

    Returns:
        Residual indicating uncertain speech force
    """
    return Residual(
        kind="semantics.speech_force.uncertain",
        detail=f"force:{candidates}" if candidates else "force:undetermined"
    )


# =============================================================================
# Phase 5H: Ifādah Closure Residuals
# =============================================================================

def make_ifadah_incomplete(missing_requirements: str = "") -> Residual:
    """
    Ifādah closure requirements not met.

    Ifādah requires ALL of:
        1. Licensed parties
        2. Licensed dāl/madlūl binding
        3. Licensed dalālah (mutābaqah/taḍammun/iltizām)
        4. Licensed nisbah
        5. Complete structure
        6. Resolved references or residuals
        7. Known speech force or residual
        8. Full residual accounting

    Args:
        missing_requirements: Which requirements are missing

    Returns:
        Residual indicating incomplete ifādah
    """
    return Residual(
        kind="semantics.ifadah.incomplete",
        detail=f"missing:{missing_requirements}" if missing_requirements else "ifadah:requirements_unmet"
    )


# =============================================================================
# Phase 5I: Boundary Guard Residuals
# =============================================================================

def make_hukm_boundary_violation(attempted_jump: str = "") -> Residual:
    """
    Attempted SEMANTICS → HUKM or IFADAH → HUKM jump.

    Hard Law: SEMANTICS cannot jump to HUKM.
              IFADAH cannot issue HUKM.
              HUKM is Phase 6 (future, separate algebra).

    Args:
        attempted_jump: Description of attempted violation

    Returns:
        Residual indicating boundary violation
    """
    return Residual(
        kind="semantics.hukm_boundary.violation",
        detail=f"violation:{attempted_jump}" if attempted_jump else "hukm:boundary_crossed"
    )
