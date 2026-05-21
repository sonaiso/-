"""Base adapter contract and utilities for FVAFK → Evidence translation.

All adapters must inherit from :class:`BaseAdapter` which enforces:

1. **Immutability**: ``__setattr__`` / ``__delattr__`` are locked after
   ``__init__`` completes; adapters cannot mutate state after
   construction.
2. **Read-only upstream access**: Adapters may read upstream objects
   but must never call mutating methods or set attributes.
3. **Evidence-only output**: All adapter public methods return
   ``Tuple[Evidence, ...]`` or ``Result[T]``; no bare values.
4. **Source citation**: Every Evidence must cite the upstream object
   via ``source`` field (format: ``"<module>:<type>:<id>"`` or
   ``"<module>:<type>:span=<start>-<end>"``).

The base class provides helper methods for constructing correctly-cited
Evidence and Residual atoms.
"""

from __future__ import annotations

from typing import Any, Protocol, Tuple
from dataclasses import dataclass, field

from fvafk.algebra import Domain, Evidence, Residual, Result, Trace


class AdapterContract(Protocol):
    """Protocol every FVAFK adapter must satisfy.

    Adapters translate upstream analysis objects into Evidence tuples.
    They are **stateless transformers** that never mutate inputs.
    """

    def adapt(self, obj: Any) -> Tuple[Evidence, ...]:
        """Convert upstream object to Evidence tuple.

        Args:
            obj: An analysis object from c1/c2a/c2b/syntax (e.g.
                RootExtractionResult, phonology trace, Link).

        Returns:
            Tuple of Evidence atoms, possibly empty if ``obj`` carries
            no admissible claim. Never returns bare ``None`` — use
            empty tuple ``()`` when no evidence can be extracted.

        Raises:
            TypeError: If ``obj`` is not a recognized upstream type.
        """
        ...


@dataclass
class BaseAdapter:
    """Base class for all FVAFK → Evidence adapters.

    Enforces immutability after construction and provides utility
    methods for Evidence construction with proper source citation.

    Attributes:
        source_module: Module identifier for Evidence.source (e.g.
            "c2b", "c2a", "syntax").
        strict: If ``True``, adapter raises ``TypeError`` on
            unrecognized object types; if ``False``, returns empty
            tuple ``()`` silently. Default: ``True``.
    """

    source_module: str
    strict: bool = True

    # Immutability lock: after __init__ completes, no attribute
    # assignment or deletion is allowed.
    _initialized: bool = field(default=False, init=False, repr=False)

    def __post_init__(self) -> None:
        # Mark as initialized to enable immutability lock
        object.__setattr__(self, "_initialized", True)

    def __setattr__(self, name: str, value: Any) -> None:
        # Allow setting during __init__, block after
        if hasattr(self, "_initialized") and self._initialized:
            raise AttributeError(
                f"BaseAdapter is immutable; cannot set attribute '{name}' "
                "after initialization (adapters are stateless transformers)."
            )
        object.__setattr__(self, name, value)

    def __delattr__(self, name: str) -> None:
        raise AttributeError(
            "BaseAdapter is immutable; attribute deletion is forbidden."
        )

    def make_evidence(
        self,
        *,
        kind: str,
        obj_type: str,
        obj_id: str | None = None,
        span: Tuple[int, int] | None = None,
        detail: str = "",
        weight: float = 1.0,
    ) -> Evidence:
        """Construct Evidence with proper source citation.

        Args:
            kind: Evidence kind (e.g. "root.candidate",
                "pattern.surface_match").
            obj_type: Upstream type name (e.g. "RootExtractionResult",
                "Link").
            obj_id: Optional stable identifier from upstream object.
            span: Optional source span tuple ``(start, end)``.
            detail: Human-readable detail string.
            weight: Evidence weight (default 1.0).

        Returns:
            Evidence with source formatted as
            ``"<module>:<type>:<id>"`` or
            ``"<module>:<type>:span=<start>-<end>"``.

        Raises:
            ValueError: If both ``obj_id`` and ``span`` are ``None``
                (source must be citable).
        """
        if obj_id is None and span is None:
            raise ValueError(
                "Evidence.source must be citable; provide either obj_id or span."
            )

        if obj_id is not None:
            source = f"{self.source_module}:{obj_type}:{obj_id}"
        else:
            assert span is not None
            source = f"{self.source_module}:{obj_type}:span={span[0]}-{span[1]}"

        return Evidence(kind=kind, source=source, detail=detail, weight=weight)

    def make_residual_for_missing_id(
        self, obj_type: str, description: str = ""
    ) -> Residual:
        """Construct Residual when upstream lacks stable id/span.

        When an upstream object cannot provide a stable identifier (no
        trace id, no unique key), emit a residual rather than
        inventing certainty.

        Args:
            obj_type: Upstream type name.
            description: Human-readable gap description (optional).

        Returns:
            Residual with kind ``"evidence.source_incomplete"``.
        """
        if not description:
            description = (
                f"{self.source_module}.{obj_type} lacks stable id/span; "
                "Evidence.source cannot be uniquely cited."
            )
        return Residual(kind="evidence.source_incomplete", description=description)


__all__ = ["AdapterContract", "BaseAdapter"]
