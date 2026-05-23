"""
FVAFK Adapters - Bridge to GFA/dal_core

This package provides thin adapters that connect FVAFK pipeline components
to the mature GFA governance and dal_core algebra infrastructure.

**Design Principle**: Adapters are pure translation layers (< 200 lines each).
They preserve all governance laws:
- Trace reversibility (DalTrace.is_reversible() = True)
- Evidence requirement (DalEvidence with span)
- No meaning field (Theorem 5)
- No direct cross-layer promotion
- No rank inflation

**Adapters**:
1. C2bToD3Adapter: FVAFK WordForm → dal_core DMufrad
2. FvafkToSyntaxInputAdapter: FVAFK tokens → syntax_theory SyntacticInput
3. SyntaxGraphToFvafkAdapter: syntax_theory SyntacticGraph → FVAFK output

**Usage**:
```python
from fvafk.adapters import C2bToD3Adapter, FvafkToSyntaxInputAdapter

# Morphology bridge
c2b_adapter = C2bToD3Adapter()
dmufrad, evidence, trace = c2b_adapter.adapt_word_form(word_form)

# Syntax bridge
syntax_adapter = FvafkToSyntaxInputAdapter()
syntactic_input = syntax_adapter.adapt_tokens(tokens, intent="declarative")
```

**See**: docs/FVAFK_GFA_INTEGRATION_MAP.md for full integration roadmap
"""

from .c2b_to_d3_adapter import C2bToD3Adapter
from .fvafk_to_syntax_input_adapter import FvafkToSyntaxInputAdapter
from .syntax_graph_to_fvafk_adapter import SyntaxGraphToFvafkAdapter

__all__ = [
    "C2bToD3Adapter",
    "FvafkToSyntaxInputAdapter",
    "SyntaxGraphToFvafkAdapter",
]
