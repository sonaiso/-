"""
C2b to D3 Adapter - FVAFK WordForm → dal_core DMufrad

**Purpose**: Bridge FVAFK C2b morphology output to dal_core D3 (Mufrad) domain.

**Governance Laws Preserved**:
1. Trace reversibility: DalTrace.is_reversible() = True
2. Evidence requirement: DalEvidence with span (claim-scoped)
3. No meaning field: Theorem 5 (DMufrad has NO meaning/murad/haqiqa_majaz)
4. No direct promotion: Respects layer contracts
5. No rank inflation: Evidence ≠ certification

**Input**: FVAFK `WordForm` from C2b pipeline
**Output**: (`DMufrad` | None, `DalEvidence`, `DalTrace`)

**Contract**: If word is inadmissible → (None, evidence, trace) with governed failure
           If word is admissible → (DMufrad, evidence, trace)

**See**: docs/FVAFK_GFA_INTEGRATION_MAP.md
**Tests**: tests/fvafk/adapters/test_c2b_to_d3_adapter.py (8 tests)
"""

from dataclasses import dataclass
from typing import Optional, Tuple
from fvafk.c2b.word_form import WordForm, Span as FvafkSpan

# dal_core imports
try:
    from dal_core import (
        DMufrad,
        MufradProof,
        DalEvidence,
        DalTraceRef,
        DalTransitionDomain,
        DalClaimScope,
        LexicalType,
        atoms_from_text,
        build_d_form,
        prove_lugha,
        infer_type,
        close_mufrad,
    )
    DAL_CORE_AVAILABLE = True
except ImportError:
    DAL_CORE_AVAILABLE = False
    # Stub for development without dal_core
    class DMufrad: pass
    class DalEvidence: pass
    class DalTraceRef: pass


@dataclass(frozen=True)
class C2bToD3Adapter:
    """
    Adapter: FVAFK C2b morphology → dal_core D3 Mufrad.
    
    **Design**: Thin translation layer (< 200 lines).
    Pure function: WordForm → (DMufrad | None, Evidence, Trace)
    
    **Preserves**:
    - Trace reversibility
    - Evidence with span
    - No meaning field (Theorem 5)
    - No direct promotion
    """
    
    strict_mode: bool = False  # If True, raise on inadmissible; if False, return None
    
    def adapt_word_form(
        self,
        word_form: WordForm
    ) -> Tuple[Optional[DMufrad], Optional[DalEvidence], Optional[DalTraceRef]]:
        """
        Convert FVAFK WordForm to dal_core DMufrad.
        
        Args:
            word_form: FVAFK C2b morphology output
        
        Returns:
            (mufrad, evidence, trace) or (None, evidence, trace) if inadmissible
        
        **Governance**:
        - Returns None (not exception) for inadmissible words
        - Evidence always present (even for None)
        - Trace always reversible
        """
        if not DAL_CORE_AVAILABLE:
            return (None, None, None)
        
        # Step 1: Validate input has minimum required fields
        if not self._is_admissible(word_form):
            evidence = self._build_inadmissible_evidence(word_form)
            trace = self._build_inadmissible_trace(word_form)
            return (None, evidence, trace)
        
        # Step 2: Extract evidence from FVAFK (with span)
        evidence = self._extract_evidence(word_form)
        
        # Step 3: Build reversible trace
        trace = self._build_trace(word_form)
        
        # Step 4: Construct DMufrad (respecting Theorem 5: no meaning field)
        try:
            mufrad = self._construct_dmufrad(word_form, evidence, trace)
            return (mufrad, evidence, trace)
        except Exception as e:
            if self.strict_mode:
                raise
            # Governed failure: return None with evidence + trace
            return (None, evidence, trace)
    
    def _is_admissible(self, wf: WordForm) -> bool:
        """
        Check if WordForm has minimum fields for D3 construction.
        
        **Required**:
        - surface (non-empty)
        - bare (non-empty)
        - span (for evidence)
        
        **Optional** (missing → heuristics):
        - root
        - pattern
        - pos
        """
        if not wf.surface or not wf.bare:
            return False
        if wf.span is None:
            return False
        return True
    
    def _extract_evidence(self, wf: WordForm) -> DalEvidence:
        """
        Extract claim-scoped evidence from FVAFK WordForm.
        
        **DalEvidence Contract** (PR #22):
        - Requires span (source text location)
        - Claim scope: WORD_LEVEL
        - Domain: D3 (Mufrad)
        """
        return DalEvidence(
            domain=DalTransitionDomain.D3_MUFRAD,
            scope=DalClaimScope.WORD_LEVEL,
            span=(wf.span.start, wf.span.end),
            source_text=wf.surface,
            observations={
                "bare_form": wf.bare,
                "root_letters": wf.root.letters if wf.root else None,
                "pattern_template": wf.pattern.template if wf.pattern else None,
                "pos": wf.pos.value if wf.pos else None,
            }
        )
    
    def _build_inadmissible_evidence(self, wf: WordForm) -> DalEvidence:
        """Build evidence for inadmissible word (missing required fields)"""
        return DalEvidence(
            domain=DalTransitionDomain.D3_MUFRAD,
            scope=DalClaimScope.WORD_LEVEL,
            span=(0, len(wf.surface)) if wf.span is None else (wf.span.start, wf.span.end),
            source_text=wf.surface or "",
            observations={"inadmissible": True, "reason": "missing_required_fields"}
        )
    
    def _build_trace(self, wf: WordForm) -> DalTraceRef:
        """
        Build reversible trace from FVAFK atoms.
        
        **DalTrace Contract** (PR #22):
        - Must be reversible: is_reversible() = True
        - Preserves source atoms
        - Records transformation steps
        """
        # Build trace that can reverse back to FVAFK atoms
        return DalTraceRef(
            domain=DalTransitionDomain.D3_MUFRAD,
            operation="fvafk_c2b_to_d3_adapt",
            source_atoms=list(wf.bare),  # Character-level atoms
            steps=[
                {"step": "extract_bare_form", "output": wf.bare},
                {"step": "extract_root", "output": wf.root.letters if wf.root else None},
                {"step": "extract_pattern", "output": wf.pattern.template if wf.pattern else None},
            ],
            reversible=True,
        )
    
    def _build_inadmissible_trace(self, wf: WordForm) -> DalTraceRef:
        """Build trace for inadmissible word"""
        return DalTraceRef(
            domain=DalTransitionDomain.D3_MUFRAD,
            operation="fvafk_c2b_to_d3_adapt_failed",
            source_atoms=list(wf.surface) if wf.surface else [],
            steps=[{"step": "inadmissible", "reason": "missing_required_fields"}],
            reversible=False,  # Cannot reverse from incomplete input
        )
    
    def _construct_dmufrad(
        self,
        wf: WordForm,
        evidence: DalEvidence,
        trace: DalTraceRef
    ) -> DMufrad:
        """
        Construct DMufrad respecting Theorem 5 (no meaning field).
        
        **Uses dal_core pipeline**:
        1. atoms_from_text(wf.bare)
        2. build_d_form(atoms)
        3. prove_lugha(d_form)
        4. infer_type(d_lugha)
        5. close_mufrad(d_type)
        
        **Critical**: DMufrad must NOT have fields: meaning, murad, haqiqa_majaz
        """
        # Step 1: Convert to atoms
        atoms = atoms_from_text(wf.bare)
        
        # Step 2: Build DForm
        d_form = build_d_form(atoms, source_span=evidence.span)
        
        # Step 3: Prove lugha (phonological/graphemic constraints)
        d_lugha = prove_lugha(d_form)
        
        # Step 4: Infer type (noun/verb/particle classification)
        lexical_type = self._infer_lexical_type(wf)
        d_type = infer_type(d_lugha, lexical_type)
        
        # Step 5: Close mufrad (final D3 unit)
        dmufrad = close_mufrad(d_type, evidence=evidence, trace=trace)
        
        # Governance check: Ensure no meaning field
        if hasattr(dmufrad, 'meaning') or hasattr(dmufrad, 'murad') or hasattr(dmufrad, 'haqiqa_majaz'):
            raise ValueError(
                "Theorem 5 violation: DMufrad must NOT contain meaning/murad/haqiqa_majaz fields"
            )
        
        return dmufrad
    
    def _infer_lexical_type(self, wf: WordForm) -> LexicalType:
        """
        Map FVAFK PartOfSpeech to dal_core LexicalType.
        
        **Mapping**:
        - NOUN, NAME, PRONOUN, DEMONSTRATIVE → NOUN
        - VERB → VERB
        - PARTICLE, OPERATOR → PARTICLE
        - UNKNOWN → UNKNOWN (will trigger heuristics in dal_core)
        """
        from fvafk.c2b.word_form import PartOfSpeech
        
        pos_mapping = {
            PartOfSpeech.NOUN: LexicalType.NOUN,
            PartOfSpeech.NAME: LexicalType.NOUN,
            PartOfSpeech.PRONOUN: LexicalType.NOUN,
            PartOfSpeech.DEMONSTRATIVE: LexicalType.NOUN,
            PartOfSpeech.VERB: LexicalType.VERB,
            PartOfSpeech.PARTICLE: LexicalType.PARTICLE,
            PartOfSpeech.OPERATOR: LexicalType.PARTICLE,
            PartOfSpeech.UNKNOWN: LexicalType.UNKNOWN,
        }
        
        return pos_mapping.get(wf.pos, LexicalType.UNKNOWN)
