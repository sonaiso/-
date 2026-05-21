"""Read-only adapters for FVAFK pipeline outputs → Evidence.

This module implements Phase 2: thin adapters that translate existing
FVAFK analysis objects (from c1, c2a, c2b, syntax) into Evidence atoms
for the algebra layer. **No FVAFK pipeline code is modified**; adapters
are pure read-only translators.

Key design principles:

1. **Read-only**: Adapters never mutate upstream objects.
2. **Evidence-only output**: Adapters produce Evidence, never final
   judgments or Rank promotions.
3. **Source citation**: Every Evidence.source cites the original
   analysis object (type, id, or span).
4. **Residuals for gaps**: When upstream lacks stable id/span, emit
   residual (e.g. ``evidence.source_incomplete``) rather than
   inventing certainty.
5. **CPB validation**: Any adapter Evidence must still pass CPB
   validation if used in a bridge.
6. **No semantic/hukm jump**: RootExtractor evidence supports ROOT
   claims, not SEMANTICS or HUKM; syntax evidence supports SYNTAX, not
   SEMANTICS/HUKM.

Adapters:

- :class:`C1Adapter` — encoding/normalization → GRAPHEME/PHONEME Evidence
- :class:`C2aAdapter` — phonological gates → PHONEME/SYLLABLE Evidence
- :class:`C2bAdapter` — RootExtractor → ROOT Evidence (primary use case)
- :class:`SyntaxAdapter` — syntactic links → SYNTAX Evidence

All adapters inherit from :class:`BaseAdapter` which enforces the
read-only contract and provides utility methods for Evidence
construction.
"""

from __future__ import annotations

from .common import BaseAdapter, AdapterContract
from .c1_adapter import C1Adapter
from .c2a_adapter import C2aAdapter
from .c2b_adapter import C2bAdapter
from .syntax_adapter import SyntaxAdapter

__all__ = [
    "BaseAdapter",
    "AdapterContract",
    "C1Adapter",
    "C2aAdapter",
    "C2bAdapter",
    "SyntaxAdapter",
]
