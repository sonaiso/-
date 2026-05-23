"""
FVAFK to SyntaxInput Adapter - FVAFK tokens → syntax_theory SyntacticInput

**Purpose**: Convert FVAFK token stream to syntax_theory SyntacticInput for graph-based parsing.

**Input**: List[WordForm] + intent (declarative/interrogative/imperative/...)
**Output**: syntax_theory.SyntacticInput

**See**: docs/FVAFK_GFA_INTEGRATION_MAP.md
**Tests**: tests/fvafk/adapters/test_fvafk_to_syntax_input_adapter.py (6 tests)
"""

from dataclasses import dataclass
from typing import List
from fvafk.c2b.word_form import WordForm

# syntax_theory imports (placeholder - to be implemented in Phase 2)
try:
    from syntax_theory.structures import SyntacticInput, LexicalAtom, IntentConstraint
    SYNTAX_THEORY_AVAILABLE = True
except ImportError:
    SYNTAX_THEORY_AVAILABLE = False
    class SyntacticInput: pass
    class LexicalAtom: pass


@dataclass(frozen=True)
class FvafkToSyntaxInputAdapter:
    """
    Adapter: FVAFK tokens → syntax_theory SyntacticInput.
    
    **Preserves**:
    - Lexical type classification
    - Verb valency extraction
    - Intent constraints
    """
    
    def adapt_tokens(self, tokens: List[WordForm], intent: str = "declarative") -> SyntacticInput:
        """
        Build SyntacticInput for syntax_theory graph construction.
        
        Args:
            tokens: FVAFK WordForm list from C2b
            intent: Sentence intent (declarative/interrogative/imperative/...)
        
        Returns:
            SyntacticInput ready for CanonicalConstructor
        """
        if not SYNTAX_THEORY_AVAILABLE:
            raise NotImplementedError("syntax_theory not available - Phase 2 implementation pending")
        
        atoms = [self._to_lexical_atom(t) for t in tokens]
        constraints = self._extract_intent_constraints(intent)
        return SyntacticInput(atoms=atoms, constraints=constraints)
    
    def _to_lexical_atom(self, token: WordForm) -> LexicalAtom:
        """Map FVAFK token to syntax_theory LexicalAtom"""
        # TODO: Phase 2 implementation
        raise NotImplementedError("Phase 2: Map WordForm to LexicalAtom")
    
    def _extract_intent_constraints(self, intent: str) -> List:
        """Map intent to IntentConstraint (interrogative/imperative/...)"""
        # TODO: Phase 2 implementation
        raise NotImplementedError("Phase 2: Extract intent constraints")
