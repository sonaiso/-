"""C2A (phonological gates) adapter → Evidence.

This adapter translates C2A phonological gate outputs (phonology traces,
syllable structures) into Evidence atoms for PHONEME and SYLLABLE
domains.

Key contracts:

1. **Domain coverage**: C2A adapter emits Evidence in domains
   ``PHONEME`` and ``SYLLABLE``.
2. **Gate evidence**: When phonological gates fire (sukun repair,
   shadda expansion, etc.), adapter emits Evidence with kind
   ``"phonology.gate_fired"`` or ``"syllable.structure_detected"``.
3. **No semantic jump**: C2A adapter never emits SEMANTICS or HUKM
   evidence kinds.
4. **CPB compliance**: All Evidence must pass CPB validation for
   bridges ``PHONEME → SYLLABLE`` or ``SYLLABLE → MORPH_SURFACE``.

Since C2A gate structures may vary, this adapter provides flexibility
for dict-like and trace-like objects.

Example usage::

    from fvafk.algebra.adapters import C2aAdapter

    adapter = C2aAdapter()

    # Adapt a phonology trace (if C2A returns structured trace objects)
    trace = {"gate": "sukun_repair", "input": "...", "output": "..."}
    evidence = adapter.adapt(trace)

    # Or adapt syllable structure
    syllable = {"pattern": "CVC", "span": (0, 3)}
    evidence = adapter.adapt(syllable)
"""

from __future__ import annotations

from typing import Any, Tuple

from fvafk.algebra import Evidence

from .common import BaseAdapter


class C2aAdapter(BaseAdapter):
    """Adapter for C2A (phonological gates) → Evidence.

    Translates phonological gate traces and syllable structures into
    Evidence tuples supporting PHONEME and SYLLABLE domain claims.
    """

    def __init__(self, *, strict: bool = False):
        """Initialize C2A adapter.

        Args:
            strict: If ``True``, raise ``TypeError`` on unrecognized
                object types; if ``False``, return empty tuple silently.
                Default ``False`` for flexibility with varying C2A
                output structures.
        """
        super().__init__(source_module="c2a", strict=strict)

    def adapt(self, obj: Any) -> Tuple[Evidence, ...]:
        """Convert C2A output to Evidence tuple.

        Args:
            obj: A dict-like object representing a phonology trace or
                syllable structure. Expected keys vary by object type:
                - Phonology trace: ``"gate"``, ``"input"``, ``"output"``
                - Syllable: ``"pattern"``, ``"span"``

        Returns:
            Tuple of Evidence atoms.

        Raises:
            TypeError: If ``obj`` is not dict-like and ``strict=True``.
        """
        if not isinstance(obj, dict):
            if self.strict:
                raise TypeError(
                    f"C2aAdapter.adapt() expects dict, got {type(obj).__name__}"
                )
            return ()

        evidence_list = []

        # Check if this is a phonology gate trace
        if "gate" in obj:
            evidence_list.append(self._make_gate_evidence(obj))

        # Check if this is a syllable structure
        if "pattern" in obj and "span" in obj:
            evidence_list.append(self._make_syllable_evidence(obj))

        return tuple(evidence_list)

    def adapt_gate_trace(
        self, gate_name: str, input_text: str, output_text: str
    ) -> Tuple[Evidence, ...]:
        """Convenience method for adapting gate traces.

        Args:
            gate_name: Name of the phonological gate (e.g. "sukun_repair").
            input_text: Input to the gate.
            output_text: Output from the gate.

        Returns:
            Tuple containing single Evidence for gate firing.
        """
        trace = {"gate": gate_name, "input": input_text, "output": output_text}
        return (self._make_gate_evidence(trace),)

    def _make_gate_evidence(self, trace: dict) -> Evidence:
        """Construct Evidence for phonological gate firing.

        Args:
            trace: Dict with keys "gate", "input", "output".

        Returns:
            Evidence with kind "phonology.gate_fired".
        """
        gate_name = trace.get("gate", "unknown")
        input_text = trace.get("input", "")
        output_text = trace.get("output", "")

        detail = f"gate='{gate_name}' applied"
        if input_text != output_text:
            detail += f": '{input_text}' → '{output_text}'"

        # Use input_text as obj_id for citation
        obj_id = input_text or "unknown"

        return self.make_evidence(
            kind="phonology.gate_fired",
            obj_type="PhonologyTrace",
            obj_id=obj_id,
            detail=detail,
            weight=0.8,
        )

    def _make_syllable_evidence(self, syllable: dict) -> Evidence:
        """Construct Evidence for syllable structure detection.

        Args:
            syllable: Dict with keys "pattern" and "span".

        Returns:
            Evidence with kind "syllable.structure_detected".
        """
        pattern = syllable.get("pattern", "")
        span = syllable.get("span", (0, 0))

        detail = f"syllable pattern '{pattern}' at span {span}"

        return self.make_evidence(
            kind="syllable.structure_detected",
            obj_type="Syllable",
            span=tuple(span),  # Use span for citation
            detail=detail,
            weight=0.7,
        )


__all__ = ["C2aAdapter"]
