"""Contract-governed dal-mufrad pipeline.

This package models lexical sign closure only (الدال المفرد),
without semantic meaning inference.
"""

from .pipeline import (
    Rank,
    Severity,
    Evidence,
    Residual,
    LexicalType,
    LexiconRecord,
    DForm,
    DLugha,
    DType,
    DMufrad,
    SEED_LEXICON,
    analyze_dal_mufrad,
    build_d_form,
    prove_lugha,
    infer_type,
    close_mufrad,
    atoms_from_text,
    attach_marks,
)

__all__ = [
    "Rank",
    "Severity",
    "Evidence",
    "Residual",
    "LexicalType",
    "LexiconRecord",
    "DForm",
    "DLugha",
    "DType",
    "DMufrad",
    "SEED_LEXICON",
    "analyze_dal_mufrad",
    "build_d_form",
    "prove_lugha",
    "infer_type",
    "close_mufrad",
    "atoms_from_text",
    "attach_marks",
]
