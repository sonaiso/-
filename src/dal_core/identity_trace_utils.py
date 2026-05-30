"""
Identity vs Trace Utilities (هوية ضد الأثر)

PR #163: Identity/trace separation enforcement utilities.

CONSTITUTIONAL LAWS:
1. identity_ids ∩ trace_ids = ∅ (disjoint sets)
2. Identity IDs MUST be stable across runs (NO UUIDs)
3. Trace IDs MUST NOT leak into identity_ids
4. Linguistic identities MUST be preserved across layers

Created: 2026-05-30
"""

from __future__ import annotations

import re
from enum import Enum
from typing import Protocol


# ---------------------------------------------------------------------------
# Identity Makers (Stable Linguistic Identities)
# ---------------------------------------------------------------------------


def make_operator_identity(
    display_name_ar: str,
    source: Enum,  # OperatorSource
    school: Enum,  # NahwSchool
) -> str:
    """
    Create stable linguistic identity for operator.

    Args:
        display_name_ar: Arabic display name (e.g., "إن", "كان")
        source: OperatorSource enum (e.g., KITAB_SIBAWAYH)
        school: NahwSchool enum (e.g., BASRI)

    Returns:
        Stable identity string: "op_identity:{name}|{source}|{school}"

    Example:
        >>> make_operator_identity("إن", OperatorSource.KITAB_SIBAWAYH, NahwSchool.BASRI)
        "op_identity:إن|KITAB_SIBAWAYH|BASRI"

    Constitutional Law:
        Operator identity is the linguistic triple (name, source, school),
        NOT the generated registry_entry_id UUID.
    """
    if not display_name_ar:
        raise ValueError("make_operator_identity requires non-empty display_name_ar")
    if not isinstance(source, Enum):
        raise TypeError(f"source must be Enum; got {type(source).__name__}")
    if not isinstance(school, Enum):
        raise TypeError(f"school must be Enum; got {type(school).__name__}")

    return f"op_identity:{display_name_ar}|{source.value}|{school.value}"


def make_mufrad_identity(
    raw_text: str,
    type_value: str,
) -> str:
    """
    Create stable linguistic identity for mufrad (single word unit).

    Args:
        raw_text: The raw Arabic text (e.g., "الكتاب")
        type_value: Type identifier (e.g., "ISM_COMMON")

    Returns:
        Stable identity string: "mufrad_identity:{text}|{type}"

    Example:
        >>> make_mufrad_identity("الكتاب", "ISM_COMMON")
        "mufrad_identity:الكتاب|ISM_COMMON"

    Constitutional Law:
        Mufrad identity is the linguistic pair (text, type),
        NOT the generated mufrad_id UUID.
    """
    if not raw_text:
        raise ValueError("make_mufrad_identity requires non-empty raw_text")
    if not type_value:
        raise ValueError("make_mufrad_identity requires non-empty type_value")

    return f"mufrad_identity:{raw_text}|{type_value}"


def make_lexical_identity(
    lexeme: str,
    lemma: str,
) -> str:
    """
    Create stable linguistic identity for lexical entry.

    Args:
        lexeme: The lexeme form (e.g., "كَتَبَ")
        lemma: The lemma/dictionary form (e.g., "ك ت ب")

    Returns:
        Stable identity string: "lexical_identity:{lexeme}|{lemma}"

    Example:
        >>> make_lexical_identity("كَتَبَ", "ك ت ب")
        "lexical_identity:كَتَبَ|ك ت ب"

    Constitutional Law:
        Lexical identity is the linguistic pair (lexeme, lemma),
        NOT any generated entry_id UUID.
    """
    if not lexeme:
        raise ValueError("make_lexical_identity requires non-empty lexeme")
    if not lemma:
        raise ValueError("make_lexical_identity requires non-empty lemma")

    return f"lexical_identity:{lexeme}|{lemma}"


# ---------------------------------------------------------------------------
# Validation Functions
# ---------------------------------------------------------------------------


def is_uuid_pattern(value: str) -> bool:
    """
    Check if value matches UUID pattern.

    Args:
        value: String to check

    Returns:
        True if value appears to be a UUID

    UUID patterns detected:
    - Pure hex string ≥8 chars: "abc123def456"
    - UUID format: "550e8400-e29b-41d4-a716-446655440000"
    """
    if not value:
        return False

    # Check for hex-only string ≥8 chars
    if re.match(r'^[a-f0-9]{8,}$', value, re.IGNORECASE):
        return True

    # Check for standard UUID format
    if re.match(
        r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$',
        value,
        re.IGNORECASE,
    ):
        return True

    return False


def has_trace_prefix(value: str) -> bool:
    """
    Check if value starts with trace-indicating prefix.

    Args:
        value: String to check

    Returns:
        True if value starts with trace prefix

    Trace prefixes:
    - trace-
    - candidate-
    - op- (when followed by hex)
    - mufrad- (when followed by hex)
    - row-
    - trigger-
    - frame-
    - matrix-
    - equation-
    - case-effect-
    """
    if not value:
        return False

    trace_prefixes = (
        "trace-",
        "candidate-",
        "row-",
        "trigger-",
        "frame-",
        "matrix-",
        "equation-",
        "case-effect-",
    )

    if value.startswith(trace_prefixes):
        return True

    # Check for op-{hex} or mufrad-{hex} (generated IDs)
    if re.match(r'^(op|mufrad)-[a-f0-9]+$', value, re.IGNORECASE):
        return True

    return False


def is_stable_identity(value: str) -> bool:
    """
    Check if value is a stable linguistic identity.

    Args:
        value: String to check

    Returns:
        True if value is stable (not UUID, not trace)

    Stable identities:
    - Start with identity marker: "op_identity:", "mufrad_identity:", "lexical_identity:"
    - Do NOT match UUID pattern
    - Do NOT have trace prefix

    Non-stable (traces):
    - UUID patterns
    - Trace prefixes (trace-, candidate-, op-{hex}, etc.)
    """
    if not value:
        return False

    # Check for identity markers
    identity_markers = (
        "op_identity:",
        "mufrad_identity:",
        "lexical_identity:",
        "factor_identity:",
        "relation_identity:",
    )

    if value.startswith(identity_markers):
        return True

    # Reject UUIDs
    if is_uuid_pattern(value):
        return False

    # Reject trace prefixes
    if has_trace_prefix(value):
        return False

    # If none of the above, assume stable (e.g., enum value, name)
    return True


def validate_identity_trace_separation(
    identity_ids: tuple[str, ...],
    trace_ids: tuple[str, ...],
) -> None:
    """
    Validate constitutional law: identity_ids ∩ trace_ids = ∅

    Args:
        identity_ids: Tuple of identity IDs
        trace_ids: Tuple of trace IDs

    Raises:
        ValueError: If identity_ids and trace_ids overlap
        ValueError: If identity_ids contain generated UUIDs
        ValueError: If identity_ids contain trace prefixes

    Constitutional Laws Enforced:
    1. Identity and trace sets must be disjoint
    2. Identity IDs must be stable (no UUIDs)
    3. Trace IDs must not leak into identity IDs

    Example:
        >>> validate_identity_trace_separation(
        ...     identity_ids=("op_identity:إن|KITAB_SIBAWAYH|BASRI",),
        ...     trace_ids=("trace-001", "candidate-abc123"),
        ... )
        # Passes

        >>> validate_identity_trace_separation(
        ...     identity_ids=("op-abc123",),  # UUID pattern
        ...     trace_ids=(),
        ... )
        # Raises ValueError: identity_id 'op-abc123' appears to be UUID
    """
    if not isinstance(identity_ids, tuple):
        raise TypeError("identity_ids must be tuple")
    if not isinstance(trace_ids, tuple):
        raise TypeError("trace_ids must be tuple")

    # Law 1: Disjoint sets
    overlap = set(identity_ids) & set(trace_ids)
    if overlap:
        raise ValueError(
            f"CONSTITUTIONAL VIOLATION: identity_ids and trace_ids overlap: {overlap}. "
            f"Identity IDs and trace IDs must be disjoint sets. "
            f"An ID cannot be both identity and trace."
        )

    # Law 2: Stability requirement for identities
    for iid in identity_ids:
        # Check for UUID patterns
        if is_uuid_pattern(iid):
            raise ValueError(
                f"CONSTITUTIONAL VIOLATION: identity_id '{iid}' appears to be a UUID. "
                f"Generated UUIDs cannot be linguistic identities. "
                f"Use make_operator_identity() or make_mufrad_identity() to create "
                f"stable linguistic identities."
            )

        # Check for trace prefixes (unless it's an identity marker)
        if has_trace_prefix(iid) and not iid.startswith(
            ("op_identity:", "mufrad_identity:", "lexical_identity:")
        ):
            raise ValueError(
                f"CONSTITUTIONAL VIOLATION: identity_id '{iid}' starts with trace prefix. "
                f"Trace IDs cannot be linguistic identities. "
                f"Trace prefixes (trace-, candidate-, op-hex, mufrad-hex, row-, etc.) "
                f"indicate computational provenance, not linguistic identity."
            )


def validate_identity_preservation(
    input_identity_ids: tuple[str, ...],
    output_identity_ids: tuple[str, ...],
) -> None:
    """
    Validate that linguistic identities are preserved across transformation.

    Args:
        input_identity_ids: Identity IDs from input
        output_identity_ids: Identity IDs from output

    Raises:
        ValueError: If input identities are not preserved in output

    Constitutional Law:
        If input carries identity_ids, output MUST preserve them.
        Layers may ADD identities, but must NEVER DROP them.

    Example:
        >>> validate_identity_preservation(
        ...     input_identity_ids=("op_identity:إن|KITAB_SIBAWAYH|BASRI",),
        ...     output_identity_ids=("op_identity:إن|KITAB_SIBAWAYH|BASRI", "mufrad_identity:الكتاب|ISM_COMMON"),
        ... )
        # Passes (output preserves input and adds new identity)

        >>> validate_identity_preservation(
        ...     input_identity_ids=("op_identity:إن|KITAB_SIBAWAYH|BASRI",),
        ...     output_identity_ids=("mufrad_identity:الكتاب|ISM_COMMON",),
        ... )
        # Raises ValueError: Input identity 'op_identity:إن...' not preserved
    """
    if not isinstance(input_identity_ids, tuple):
        raise TypeError("input_identity_ids must be tuple")
    if not isinstance(output_identity_ids, tuple):
        raise TypeError("output_identity_ids must be tuple")

    input_set = set(input_identity_ids)
    output_set = set(output_identity_ids)

    # Check preservation: input ⊆ output
    if not input_set.issubset(output_set):
        missing = input_set - output_set
        raise ValueError(
            f"IDENTITY LOSS: Input identities {missing} not preserved in output. "
            f"Constitutional law requires all input identities to be preserved. "
            f"Input identities: {sorted(input_set)} "
            f"Output identities: {sorted(output_set)}"
        )


# ---------------------------------------------------------------------------
# Diagnostic Functions
# ---------------------------------------------------------------------------


def diagnose_identity_ids(identity_ids: tuple[str, ...]) -> dict[str, list[str]]:
    """
    Diagnose identity IDs for stability issues.

    Args:
        identity_ids: Tuple of identity IDs to diagnose

    Returns:
        Dictionary with categories:
        - "stable": Stable identities (✅ correct)
        - "uuid_pattern": UUIDs (❌ violation)
        - "trace_prefix": Trace prefixes (❌ violation)
        - "empty": Empty strings (❌ violation)

    Example:
        >>> diagnose_identity_ids((
        ...     "op_identity:إن|KITAB_SIBAWAYH|BASRI",
        ...     "op-abc123",
        ...     "trace-001",
        ...     "",
        ... ))
        {
            "stable": ["op_identity:إن|KITAB_SIBAWAYH|BASRI"],
            "uuid_pattern": ["op-abc123"],
            "trace_prefix": ["trace-001"],
            "empty": [""],
        }
    """
    result = {
        "stable": [],
        "uuid_pattern": [],
        "trace_prefix": [],
        "empty": [],
    }

    for iid in identity_ids:
        if not iid:
            result["empty"].append(iid)
        elif is_uuid_pattern(iid):
            result["uuid_pattern"].append(iid)
        elif has_trace_prefix(iid):
            result["trace_prefix"].append(iid)
        else:
            result["stable"].append(iid)

    return result


def format_diagnosis_report(diagnosis: dict[str, list[str]]) -> str:
    """
    Format diagnosis results as human-readable report.

    Args:
        diagnosis: Output from diagnose_identity_ids()

    Returns:
        Formatted report string

    Example:
        >>> report = format_diagnosis_report(diagnose_identity_ids(ids))
        >>> print(report)
        Identity IDs Diagnosis Report
        ==============================
        ✅ Stable Identities (1):
          - op_identity:إن|KITAB_SIBAWAYH|BASRI

        ❌ UUID Patterns (1):
          - op-abc123

        ❌ Trace Prefixes (1):
          - trace-001

        ❌ Empty Strings (1):
          - (empty)
    """
    lines = ["Identity IDs Diagnosis Report", "=" * 30]

    # Stable
    stable = diagnosis["stable"]
    lines.append(f"\n✅ Stable Identities ({len(stable)}):")
    if stable:
        for iid in stable:
            lines.append(f"  - {iid}")
    else:
        lines.append("  (none)")

    # UUID patterns
    uuid_pattern = diagnosis["uuid_pattern"]
    lines.append(f"\n❌ UUID Patterns ({len(uuid_pattern)}):")
    if uuid_pattern:
        for iid in uuid_pattern:
            lines.append(f"  - {iid}")
    else:
        lines.append("  (none)")

    # Trace prefixes
    trace_prefix = diagnosis["trace_prefix"]
    lines.append(f"\n❌ Trace Prefixes ({len(trace_prefix)}):")
    if trace_prefix:
        for iid in trace_prefix:
            lines.append(f"  - {iid}")
    else:
        lines.append("  (none)")

    # Empty
    empty = diagnosis["empty"]
    lines.append(f"\n❌ Empty Strings ({len(empty)}):")
    if empty:
        lines.append(f"  - (empty) × {len(empty)}")
    else:
        lines.append("  (none)")

    return "\n".join(lines)
