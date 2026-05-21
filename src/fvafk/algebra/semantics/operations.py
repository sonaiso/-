"""
Phase 5 Semantic Operations

Implements the 11 governed operations across semantic layers (Phase 5A-5I).

These operations bridge syntax (Phase 4) to semantic completion (ifādah)
while enforcing hard boundaries against premature HUKM.

Operation Categories:
    Phase 5A: DalCandidateOperation
    Phase 5B: MadlulCandidateOperation
    Phase 5C: WadhBindingOperation
    Phase 5D: MutabaqahGate, TadammunGate, IltizamGate
    Phase 5E: NisbahSemanticOperation
    Phase 5F: ReferenceResolutionOperation
    Phase 5G: SpeechForceOperation
    Phase 5H: IfadahClosureOperation
    Phase 5I: BoundaryGuardOperation
"""

from typing import Tuple
from ..core import Result, Rank, Evidence, Residual, Failure, Carrier, Domain
from ..cpb import validate_cpb, ALLOWED_BRIDGES
from .residual_taxonomy import (
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


# =============================================================================
# Phase 5A: Dāl Candidate Operation
# =============================================================================

class DalCandidateOperation:
    """
    Represent dāl (signifier) alone as governed candidate.

    Law: الدال وحده ليس معنى (Dāl alone is not meaning)

    Bridge: SYNTAX → SEMANTICS (identity, no interpretation)
    Input: Signifier form
    Output: Result with polysemy residuals
    Rank: CANDIDATE (never CERTIFIED without binding)
    """

    def run(self, carrier: Carrier, evidence: Tuple[Evidence, ...] = ()) -> Result:
        """
        Process dāl candidate with polysemy residuals.

        Args:
            carrier: Signifier carrier
            evidence: Optional evidence for attestation

        Returns:
            Result with CANDIDATE rank and polysemy residuals
        """
        # Verify domain
        if carrier.domain not in (Domain.SYNTAX, Domain.SEMANTICS):
            return Result(
                value=carrier.value,
                rank=Rank.REFUTED,
                evidence=(),
                residuals=(),
                failures=(Failure(
                    kind="domain.mismatch",
                    detail=f"expected SYNTAX/SEMANTICS, got {carrier.domain}",
                    fatal=True
                ),),
                replay=""
            )

        # Dāl alone creates polysemy residual
        residuals = (make_polysemy_possible(str(carrier.value)),)

        # Evidence may support but never removes polysemy without binding
        rank = Rank.LICENSED if evidence else Rank.CANDIDATE

        return Result(
            value=carrier.value,
            rank=rank,
            evidence=evidence,
            residuals=residuals,
            failures=(),
            replay=f"dal_candidate({carrier.value})"
        )


def governed_dal_candidate(value: str, evidence: Tuple[Evidence, ...] = ()) -> Result:
    """
    Convenience wrapper for dāl candidate operation.

    Args:
        value: Signifier value
        evidence: Optional evidence

    Returns:
        Result with dāl candidate
    """
    op = DalCandidateOperation()
    carrier = Carrier(domain=Domain.SEMANTICS, value=value)
    return op.run(carrier, evidence)


# =============================================================================
# Phase 5B: Madlūl Candidate Operation
# =============================================================================

class MadlulCandidateOperation:
    """
    Represent madlūl (signified) alone as governed candidate.

    Law: المدلول وحده ليس دلالة (Madlūl alone is not dalālah)

    Bridge: None (madlūl exists in semantic space)
    Input: Signified candidate
    Output: Result with dal_binding.absent residual
    Rank: CANDIDATE (never CERTIFIED without dāl binding)
    """

    def run(self, carrier: Carrier, evidence: Tuple[Evidence, ...] = ()) -> Result:
        """
        Process madlūl candidate with binding residuals.

        Args:
            carrier: Signified carrier
            evidence: Optional evidence

        Returns:
            Result with CANDIDATE rank and binding residuals
        """
        # Madlūl requires SEMANTICS domain
        if carrier.domain != Domain.SEMANTICS:
            return Result(
                value=carrier.value,
                rank=Rank.REFUTED,
                evidence=(),
                residuals=(),
                failures=(Failure(
                    kind="domain.mismatch",
                    detail=f"expected SEMANTICS, got {carrier.domain}",
                    fatal=True
                ),),
                replay=""
            )

        # Madlūl alone creates binding residual
        residuals = (make_dal_binding_absent(str(carrier.value)),)

        # Evidence may support but never removes binding requirement
        rank = Rank.LICENSED if evidence else Rank.CANDIDATE

        return Result(
            value=carrier.value,
            rank=rank,
            evidence=evidence,
            residuals=residuals,
            failures=(),
            replay=f"madlul_candidate({carrier.value})"
        )


def governed_madlul_candidate(value: str, evidence: Tuple[Evidence, ...] = ()) -> Result:
    """
    Convenience wrapper for madlūl candidate operation.

    Args:
        value: Signified value
        evidence: Optional evidence

    Returns:
        Result with madlūl candidate
    """
    op = MadlulCandidateOperation()
    carrier = Carrier(domain=Domain.SEMANTICS, value=value)
    return op.run(carrier, evidence)


# =============================================================================
# Phase 5C: Wadh' Binding Operation
# =============================================================================

class WadhBindingOperation:
    """
    Bind dāl to madlūl through wadh'/usage/context.

    Law: لا دلالة بلا ربط (No dalālah without binding)

    Bridge: SEMANTICS → SEMANTICS (binds two semantic candidates)
    Input: Dāl + Madlūl + Evidence
    Output: Result with binding or dalalah_gate.required residual
    Rank: LICENSED with evidence, CANDIDATE without
    """

    def run(self, dal: str, madlul: str, evidence: Tuple[Evidence, ...] = ()) -> Result:
        """
        Bind dāl to madlūl.

        Args:
            dal: Signifier
            madlul: Signified
            evidence: Binding evidence (wadh', usage, context)

        Returns:
            Result with binding (LICENSED if evidence, else CANDIDATE)
        """
        # Binding requires evidence
        if not evidence:
            residuals = (make_dalalah_gate_required("wadh"),)
            rank = Rank.CANDIDATE
        else:
            # Evidence present → LICENSED binding
            residuals = ()
            rank = Rank.LICENSED

        return Result(
            value=f"{dal}→{madlul}",
            rank=rank,
            evidence=evidence,
            residuals=residuals,
            failures=(),
            replay=f"wadh_binding({dal}, {madlul})"
        )


def governed_wadh_binding(dal: str, madlul: str, evidence: Tuple[Evidence, ...] = ()) -> Result:
    """
    Convenience wrapper for wadh' binding operation.

    Args:
        dal: Signifier
        madlul: Signified
        evidence: Binding evidence

    Returns:
        Result with binding
    """
    op = WadhBindingOperation()
    return op.run(dal, madlul, evidence)


# =============================================================================
# Phase 5D: Dalālah Gates (Mutābaqah, Taḍammun, Iltizām)
# =============================================================================

class MutabaqahGate:
    """
    Mutābaqah (direct correspondence) gate.

    Law: المطابقة لا تصبح إفادة وحدها (Mutābaqah does not become ifādah alone)

    This is a **pre-ifādah condition**, not ifādah itself.

    Bridge: SEMANTICS → SEMANTICS (identity)
    Input: Dāl/madlūl binding
    Output: Result with mutabaqah.insufficient residual
    Rank: LICENSED (never CERTIFIED without nisbah)
    """

    def run(self, binding: str, evidence: Tuple[Evidence, ...] = ()) -> Result:
        """
        Process mutābaqah relation.

        Args:
            binding: Dāl→madlūl binding
            evidence: Optional evidence

        Returns:
            Result with mutābaqah residual (pre-ifādah condition)
        """
        # Mutābaqah alone is insufficient for ifādah
        residuals = (make_mutabaqah_insufficient(),)

        rank = Rank.LICENSED if evidence else Rank.CANDIDATE

        return Result(
            value=f"mutabaqah:{binding}",
            rank=rank,
            evidence=evidence,
            residuals=residuals,
            failures=(),
            replay=f"mutabaqah({binding})"
        )


def governed_mutabaqah(binding: str, evidence: Tuple[Evidence, ...] = ()) -> Result:
    """Convenience wrapper for mutābaqah gate."""
    gate = MutabaqahGate()
    return gate.run(binding, evidence)


class TadammunGate:
    """
    Taḍammun (partial inclusion) gate.

    Law: التضمن لا يصبح إفادة وحده (Taḍammun does not become ifādah alone)

    This is a **pre-ifādah condition**, not ifādah itself.

    Bridge: SEMANTICS → SEMANTICS (identity)
    Input: Dāl/madlūl binding
    Output: Result with tadammun.insufficient residual
    Rank: LICENSED (never CERTIFIED without nisbah)
    """

    def run(self, binding: str, part: str, evidence: Tuple[Evidence, ...] = ()) -> Result:
        """
        Process taḍammun relation.

        Args:
            binding: Dāl→madlūl binding
            part: Part of meaning included
            evidence: Optional evidence

        Returns:
            Result with taḍammun residual (pre-ifādah condition)
        """
        # Taḍammun alone is insufficient for ifādah
        residuals = (make_tadammun_insufficient(),)

        rank = Rank.LICENSED if evidence else Rank.CANDIDATE

        return Result(
            value=f"tadammun:{binding}→{part}",
            rank=rank,
            evidence=evidence,
            residuals=residuals,
            failures=(),
            replay=f"tadammun({binding}, {part})"
        )


def governed_tadammun(binding: str, part: str, evidence: Tuple[Evidence, ...] = ()) -> Result:
    """Convenience wrapper for taḍammun gate."""
    gate = TadammunGate()
    return gate.run(binding, part, evidence)


class IltizamGate:
    """
    Iltizām (entailment) gate.

    Law: الالتزام ليس تلقائياً (Iltizām is not automatic)

    Iltizām requires EXPLICIT gate (logical, conventional, shariah, contextual).

    Bridge: SEMANTICS → SEMANTICS (identity)
    Input: Dāl/madlūl binding + gate type
    Output: Result with iltizam.gate_missing if no gate, else LICENSED
    Rank: LICENSED only with explicit gate evidence
    """

    def run(self, binding: str, consequence: str, gate_type: str = "",
            evidence: Tuple[Evidence, ...] = ()) -> Result:
        """
        Process iltizām relation.

        Args:
            binding: Dāl→madlūl binding
            consequence: Entailed consequence
            gate_type: Gate type (logical, conventional, shariah, contextual)
            evidence: Gate evidence (REQUIRED)

        Returns:
            Result with iltizām (LICENSED if gate, else CANDIDATE with residual)
        """
        # Iltizām requires explicit gate
        if not gate_type or not evidence:
            residuals = (make_iltizam_gate_missing(gate_type),)
            rank = Rank.CANDIDATE
        else:
            # Gate present → LICENSED (but still pre-ifādah)
            residuals = ()
            rank = Rank.LICENSED

        return Result(
            value=f"iltizam:{binding}→{consequence}",
            rank=rank,
            evidence=evidence,
            residuals=residuals,
            failures=(),
            replay=f"iltizam({binding}, {consequence}, {gate_type})"
        )


def governed_iltizam(binding: str, consequence: str, gate_type: str = "",
                     evidence: Tuple[Evidence, ...] = ()) -> Result:
    """Convenience wrapper for iltizām gate."""
    gate = IltizamGate()
    return gate.run(binding, consequence, gate_type, evidence)


# =============================================================================
# Phase 5E: Nisbah Semantic Operation
# =============================================================================

class NisbahSemanticOperation:
    """
    Compositional semantics from syntactic nisbah.

    Laws:
        - النسبة الإضافية لا تصبح إفادة (Iḍāfah does not become ifādah)
        - الشرط بلا جواب لا يصبح إفادة (Conditional without jawāb ≠ ifādah)

    Bridge: SYNTAX → SEMANTICS
    Input: Nisbah type from Phase 4
    Output: Result with ifādah candidate or insufficiency residual
    Rank: Depends on nisbah type (ISNADI may lead to ifādah, IDAFAH does not)
    """

    def run(self, nisbah_type: str, parties: str, evidence: Tuple[Evidence, ...] = ()) -> Result:
        """
        Process nisbah semantic composition.

        Args:
            nisbah_type: ISN, TADMN, TAQYID, IDAFA, etc.
            parties: Parties in relation
            evidence: Optional evidence

        Returns:
            Result with semantic composition
        """
        # Iḍāfah alone does not become ifādah
        if nisbah_type == "IDAFA":
            residuals = (make_idafah_not_ifadah(parties),)
            rank = Rank.LICENSED if evidence else Rank.CANDIDATE

        # Taqyīd incomplete without predication
        elif nisbah_type == "TAQYID":
            residuals = (make_taqyid_incomplete(parties),)
            rank = Rank.LICENSED if evidence else Rank.CANDIDATE

        # Conditional requires jawāb (checked externally)
        elif nisbah_type == "SHART":
            residuals = (make_conditional_jawab_missing(),)
            rank = Rank.CANDIDATE

        # Isnadi may lead to ifādah (Phase 5H will verify)
        elif nisbah_type == "ISN":
            residuals = ()
            rank = Rank.LICENSED if evidence else Rank.CANDIDATE

        else:
            residuals = ()
            rank = Rank.LICENSED if evidence else Rank.CANDIDATE

        return Result(
            value=f"nisbah_semantic:{nisbah_type}({parties})",
            rank=rank,
            evidence=evidence,
            residuals=residuals,
            failures=(),
            replay=f"nisbah_semantic({nisbah_type}, {parties})"
        )


def governed_nisbah_semantic(nisbah_type: str, parties: str,
                             evidence: Tuple[Evidence, ...] = ()) -> Result:
    """Convenience wrapper for nisbah semantic operation."""
    op = NisbahSemanticOperation()
    return op.run(nisbah_type, parties, evidence)


# =============================================================================
# Phase 5F: Reference Resolution Operation
# =============================================================================

class ReferenceResolutionOperation:
    """
    Resolve pronouns, demonstratives, ellipsis, jawāb.

    Law: الضمير بلا مرجع لا يصبح إفادة معتمدة
         (Pronoun without referent cannot become CERTIFIED ifādah)

    Bridge: SEMANTICS → SEMANTICS
    Input: Reference element + referent
    Output: Result with resolution or pronoun.referent_missing residual
    Rank: LICENSED if resolved, CANDIDATE if missing
    """

    def run(self, reference: str, referent: str = "", evidence: Tuple[Evidence, ...] = ()) -> Result:
        """
        Resolve reference element.

        Args:
            reference: Pronoun/demonstrative/ellipsis
            referent: Resolved referent (empty if unresolved)
            evidence: Resolution evidence

        Returns:
            Result with resolution status
        """
        # Reference without referent creates residual
        if not referent:
            residuals = (make_pronoun_referent_missing(reference),)
            rank = Rank.CANDIDATE
        else:
            # Referent present → LICENSED
            residuals = ()
            rank = Rank.LICENSED if evidence else Rank.CANDIDATE

        return Result(
            value=f"reference:{reference}→{referent}" if referent else f"reference:{reference}",
            rank=rank,
            evidence=evidence,
            residuals=residuals,
            failures=(),
            replay=f"reference_resolution({reference}, {referent})"
        )


def governed_reference_resolution(reference: str, referent: str = "",
                                  evidence: Tuple[Evidence, ...] = ()) -> Result:
    """Convenience wrapper for reference resolution."""
    op = ReferenceResolutionOperation()
    return op.run(reference, referent, evidence)


# =============================================================================
# Phase 5G: Speech Force Operation
# =============================================================================

class SpeechForceOperation:
    """
    Detect speech force (illocutionary act type).

    Laws:
        - Khabar does NOT become HUKM
        - Inshā does NOT become legal judgment
        - Amr does NOT become obligation at Phase 5
        - Nahy does NOT become prohibition at Phase 5

    Bridge: SEMANTICS → SEMANTICS (identity)
    Input: Utterance + markers
    Output: Result with speech force type
    Rank: LICENSED if determined, CANDIDATE if uncertain
    """

    FORCE_TYPES = (
        "khabar", "insha", "amr", "nahy", "istifham", "shart",
        "nida", "tamanni", "tarjji", "taajjub"
    )

    def run(self, utterance: str, force: str = "", evidence: Tuple[Evidence, ...] = ()) -> Result:
        """
        Detect speech force.

        Args:
            utterance: Utterance to analyze
            force: Detected force type (empty if uncertain)
            evidence: Force markers/evidence

        Returns:
            Result with speech force
        """
        # Force uncertain creates residual
        if not force or force not in self.FORCE_TYPES:
            residuals = (make_speech_force_uncertain(force),)
            rank = Rank.CANDIDATE
        else:
            # Force determined → LICENSED (but still not HUKM)
            residuals = ()
            rank = Rank.LICENSED if evidence else Rank.CANDIDATE

        return Result(
            value=f"speech_force:{force}({utterance})" if force else f"speech_force:uncertain({utterance})",
            rank=rank,
            evidence=evidence,
            residuals=residuals,
            failures=(),
            replay=f"speech_force({utterance}, {force})"
        )


def governed_speech_force(utterance: str, force: str = "",
                          evidence: Tuple[Evidence, ...] = ()) -> Result:
    """Convenience wrapper for speech force operation."""
    op = SpeechForceOperation()
    return op.run(utterance, force, evidence)


# =============================================================================
# Phase 5H: Ifādah Closure Operation
# =============================================================================

class IfadahClosureOperation:
    """
    Close semantic completion (ifādah) with full residual accounting.

    Ifādah requires ALL of:
        1. Licensed parties
        2. Licensed dāl/madlūl binding
        3. Licensed dalālah (mutābaqah/taḍammun/iltizām)
        4. Licensed nisbah
        5. Complete structure
        6. Resolved references or residuals
        7. Known speech force or residual
        8. Full residual accounting

    Rank Rules:
        - Ifādah with residuals → LICENSED only
        - Ifādah without residuals + full evidence → CERTIFIED
        - Incomplete ifādah → CANDIDATE

    Bridge: SEMANTICS → SEMANTICS (closure)
    """

    def run(self, components: dict, evidence: Tuple[Evidence, ...] = ()) -> Result:
        """
        Close ifādah.

        Args:
            components: Dict with keys: parties, binding, dalalah, nisbah,
                       structure, references, speech_force
            evidence: Ifādah evidence

        Returns:
            Result with ifādah closure
        """
        missing = []

        # Check all 8 requirements
        if not components.get("parties"):
            missing.append("parties")
        if not components.get("binding"):
            missing.append("binding")
        if not components.get("dalalah"):
            missing.append("dalalah")
        if not components.get("nisbah"):
            missing.append("nisbah")
        if not components.get("structure"):
            missing.append("structure")
        if not components.get("references"):
            missing.append("references")
        if not components.get("speech_force"):
            missing.append("speech_force")

        # Incomplete ifādah
        if missing:
            residuals = (make_ifadah_incomplete(",".join(missing)),)
            rank = Rank.CANDIDATE
        else:
            # Complete ifādah → LICENSED (CERTIFIED requires no residuals)
            residuals = ()
            rank = Rank.CERTIFIED if evidence else Rank.LICENSED

        return Result(
            value=f"ifadah:{components.get('nisbah', 'unknown')}",
            rank=rank,
            evidence=evidence,
            residuals=residuals,
            failures=(),
            replay=f"ifadah_closure({components})"
        )


def governed_ifadah_closure(components: dict, evidence: Tuple[Evidence, ...] = ()) -> Result:
    """Convenience wrapper for ifādah closure."""
    op = IfadahClosureOperation()
    return op.run(components, evidence)


# =============================================================================
# Phase 5I: Boundary Guard Operation
# =============================================================================

class BoundaryGuardOperation:
    """
    Prevent SEMANTICS → HUKM or IFADAH → HUKM jump.

    Hard Laws:
        - SEMANTICS cannot jump to HUKM
        - IFADAH cannot issue HUKM
        - HUKM is Phase 6 (future, separate algebra)

    Bridge: None (guard operation)
    Input: Attempted transition
    Output: REFUTED if violation detected
    """

    def run(self, source: Domain, target: Domain, value: str) -> Result:
        """
        Guard against forbidden boundary crossing.

        Args:
            source: Source domain
            target: Target domain
            value: Value being transitioned

        Returns:
            REFUTED if violation, else CANDIDATE
        """
        # Detect SEMANTICS → HUKM jump
        if source == Domain.SEMANTICS and target == Domain.HUKM:
            return Result(
                value=value,
                rank=Rank.REFUTED,
                evidence=(),
                residuals=(make_hukm_boundary_violation(f"{source}→{target}"),),
                failures=(Failure(
                    kind="boundary.violation",
                    detail=f"SEMANTICS→HUKM jump forbidden",
                    fatal=True
                ),),
                replay=f"boundary_guard({source}, {target}, {value})"
            )

        # All other transitions pass (may be invalid for other reasons)
        return Result(
            value=value,
            rank=Rank.CANDIDATE,
            evidence=(),
            residuals=(),
            failures=(),
            replay=f"boundary_guard({source}, {target}, {value})"
        )


def governed_boundary_guard(source: Domain, target: Domain, value: str) -> Result:
    """Convenience wrapper for boundary guard."""
    op = BoundaryGuardOperation()
    return op.run(source, target, value)
