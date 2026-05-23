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

        # SyntacticInput uses L, T, I, B notation
        return SyntacticInput(L=atoms, I=constraints)
    
    def _to_lexical_atom(self, token: WordForm) -> LexicalAtom:
        """
        Map FVAFK token to syntax_theory LexicalAtom.

        Maps:
        - WordForm.pos → LexicalAtom.atom_type
        - WordForm.root → LexicalAtom.raw_material
        - WordForm.features → LexicalAtom attributes
        """
        from syntax_theory.structures import LexicalType, VerbValency

        # Map POS to LexicalType
        pos_map = {
            "noun": LexicalType.N,
            "verb": LexicalType.V,
            "particle": LexicalType.Part,
            "pronoun": LexicalType.Pron,
            "adjective": LexicalType.Adj,
            "adverb": LexicalType.Adv,
        }
        atom_type = pos_map.get(token.kind, LexicalType.N)

        # Extract raw material (root if available, else surface form)
        raw_material = token.root.formatted if token.root else token.bare

        # Extract valency for verbs
        valency = None
        if token.kind == "verb" and token.features:
            valency_num = token.features.get("valency", 1)
            if valency_num == 0:
                valency = VerbValency.INTRANSITIVE
            elif valency_num == 1:
                valency = VerbValency.INTRANSITIVE
            elif valency_num == 2:
                valency = VerbValency.TRANSITIVE
            elif valency_num >= 3:
                valency = VerbValency.DITRANSITIVE

        # Check if declinable (murab vs mabni)
        # Particles are typically mabni (not declinable)
        requires_case = token.kind not in ("particle", "pronoun")
        is_built = token.kind in ("particle", "pronoun")

        return LexicalAtom(
            atom_type=atom_type,
            raw_material=raw_material,
            valency=valency,
            requires_case=requires_case,
            is_built=is_built
        )

    def _extract_intent_constraints(self, intent: str) -> List:
        """
        Map intent to IntentConstraint (interrogative/imperative/...).

        Intents:
        - "declarative" → no constraints (default)
        - "interrogative" → REQUIRES_QUESTION
        - "imperative" → REQUIRES_COMMAND
        - "prohibitive" → REQUIRES_PROHIBITION
        """
        # For now, return empty list (no constraints for declarative)
        # Phase 2 will expand this with IntentConstraint objects
        return []
