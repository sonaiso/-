from __future__ import annotations

# TEMPORARY ADAPTER NOTE:
# This pipeline module still exposes local Rank/Evidence/Residual names for
# legacy DAL callers. See docs/ALGEBRA_KERNEL_CONSTITUTION.md; these are
# temporary adapter surfaces and should migrate to fvafk.algebra.

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
import unicodedata


# ============================================================================
# MIGRATION NOTICE: This Rank definition is DEPRECATED and awaiting migration.
#
# CONSTITUTIONAL AUTHORITY: docs/ALGEBRA_KERNEL_CONSTITUTION.md Article 2
# TARGET: Migrate to fvafk.algebra.Rank (src/fvafk/algebra/core.py:36)
# TIMELINE: Remove after dal_core pipeline refactoring
# ISSUE: To be tracked in future PR
#
# CRITICAL LAW: Do NOT extend this enum. Use fvafk.algebra.Rank for new code.
#
# This parallel Rank exists temporarily for dal_core pipeline compatibility.
# The canonical epistemic rank system is fvafk.algebra.Rank with values:
#   UNRESOLVED, CANDIDATE, LICENSED, CERTIFIED, REFUTED
#
# Migration path:
#   1. Map dal_core ranks to fvafk.algebra.Rank:
#      ZERO → UNRESOLVED
#      FORM → CANDIDATE
#      QIYAS/AHAD/TAWATUR → LICENSED (with evidence differentiation)
#      CERT → CERTIFIED
#   2. Update pipeline to use fvafk.algebra.Rank
#   3. Remove this definition
# ============================================================================
class Rank(Enum):
    """DEPRECATED: Legacy dal_core rank. See migration notice above."""
    ZERO = 0
    FORM = 1
    QIYAS = 2
    AHAD = 3
    TAWATUR = 4
    CERT = 5


class Severity(Enum):
    INFO = "info"
    WARNING = "warning"
    BLOCKER = "blocker"


@dataclass(frozen=True)
class Evidence:
    source: str
    description: str
    rank: Rank


@dataclass(frozen=True)
class Residual:
    code: str
    message: str
    severity: Severity = Severity.WARNING


def has_blocking_residuals(residuals: List[Residual]) -> bool:
    return any(r.severity == Severity.BLOCKER for r in residuals)


def min_rank(a: Rank, b: Rank) -> Rank:
    return a if a.value <= b.value else b


def rank_from_residuals(residuals: List[Residual]) -> Rank:
    if has_blocking_residuals(residuals):
        return Rank.ZERO
    if residuals:
        return Rank.FORM
    return Rank.CERT


@dataclass(frozen=True)
class Carrier:
    char: str
    codepoint: str
    index: int
    unicode_name: str
    normalized_form: str = "NFC"


def normalize_text(text: str) -> str:
    return unicodedata.normalize("NFC", text)


def to_carriers(text: str) -> List[Carrier]:
    normalized = normalize_text(text)
    return [
        Carrier(
            char=ch,
            codepoint=f"U+{ord(ch):04X}",
            index=i,
            unicode_name=unicodedata.name(ch, "UNKNOWN"),
        )
        for i, ch in enumerate(normalized)
    ]


class AtomKind(Enum):
    LETTER = "letter"
    SHORT_VOWEL = "short_vowel"
    MARK = "mark"
    TATWEEL = "tatweel"
    PUNCTUATION = "punctuation"
    SPACE = "space"
    UNKNOWN = "unknown"


# Seed letter inventory for dal-form carrier classification.
# This table is intentionally scoped to core Arabic letters used by the seed pipeline.
ARABIC_LETTERS = set("ابتثجحخدذرزسشصضطظعغفقكلمنهويءآأؤإئاةى")
SHORT_VOWELS = {"\u064e": "fatha", "\u064f": "damma", "\u0650": "kasra"}
SHORT_VOWEL_NAMES = tuple(SHORT_VOWELS.values())
MARKS = {
    "\u0652": "sukun",
    "\u0651": "shadda",
    "\u064b": "tanwin_fath",
    "\u064c": "tanwin_damm",
    "\u064d": "tanwin_kasr",
    "\u0653": "maddah",
    "\u0670": "dagger_alif",
}
PUNCTUATION = set("،؛؟.!?:")


@dataclass
class ArabicAtom:
    carrier: Carrier
    kind: AtomKind
    features: Dict[str, Any]
    evidence: Evidence
    rank: Rank
    residuals: List[Residual] = field(default_factory=list)

    @property
    def char(self) -> str:
        return self.carrier.char


def classify_atom(carrier: Carrier) -> ArabicAtom:
    ch = carrier.char
    if ch in ARABIC_LETTERS:
        return ArabicAtom(
            carrier=carrier,
            kind=AtomKind.LETTER,
            features={"script": "arabic", "is_base_letter": True},
            evidence=Evidence("arabic_alphabet_table", "Arabic letter carrier", Rank.CERT),
            rank=Rank.CERT,
        )
    if ch in SHORT_VOWELS:
        return ArabicAtom(
            carrier=carrier,
            kind=AtomKind.SHORT_VOWEL,
            features={"script": "arabic", "vowel_name": SHORT_VOWELS[ch], "is_diacritic": True},
            evidence=Evidence("unicode_diacritic_table", "Arabic short vowel", Rank.CERT),
            rank=Rank.CERT,
        )
    if ch in MARKS:
        return ArabicAtom(
            carrier=carrier,
            kind=AtomKind.MARK,
            features={"script": "arabic", "mark_name": MARKS[ch], "is_diacritic": True},
            evidence=Evidence("unicode_mark_table", "Arabic operational mark", Rank.CERT),
            rank=Rank.CERT,
        )
    if ch == "\u0640":
        return ArabicAtom(
            carrier=carrier,
            kind=AtomKind.TATWEEL,
            features={"decorative": True},
            evidence=Evidence("unicode_table", "Tatweel decorative carrier", Rank.CERT),
            rank=Rank.CERT,
            residuals=[Residual("decorative_tatweel", "Tatweel excluded from dal fold", Severity.INFO)],
        )
    if ch.isspace():
        return ArabicAtom(
            carrier=carrier,
            kind=AtomKind.SPACE,
            features={"separator": True},
            evidence=Evidence("unicode_category", "Space separator", Rank.CERT),
            rank=Rank.CERT,
        )
    if ch in PUNCTUATION:
        return ArabicAtom(
            carrier=carrier,
            kind=AtomKind.PUNCTUATION,
            features={"punctuation": True},
            evidence=Evidence("punctuation_table", "Punctuation symbol", Rank.CERT),
            rank=Rank.CERT,
        )
    return ArabicAtom(
        carrier=carrier,
        kind=AtomKind.UNKNOWN,
        features={},
        evidence=Evidence("classifier", "Unknown carrier", Rank.ZERO),
        rank=Rank.ZERO,
        residuals=[Residual("unknown_carrier", f"Unknown carrier: {carrier.char}", Severity.BLOCKER)],
    )


def atoms_from_text(text: str) -> List[ArabicAtom]:
    return [classify_atom(c) for c in to_carriers(text)]


@dataclass
class OperativeUnit:
    base: ArabicAtom
    marks: List[ArabicAtom]
    evidence: Evidence
    rank: Rank
    residuals: List[Residual] = field(default_factory=list)

    def text(self) -> str:
        return self.base.char + "".join(m.char for m in self.marks)

    def mark_names(self) -> List[str]:
        names: List[str] = []
        for m in self.marks:
            if m.kind == AtomKind.SHORT_VOWEL:
                names.append(m.features["vowel_name"])
            elif m.kind == AtomKind.MARK:
                names.append(m.features["mark_name"])
        return names

    def has_mark(self, name: str) -> bool:
        return name in self.mark_names()


def attach_marks(atoms: List[ArabicAtom]) -> List[OperativeUnit]:
    units: List[OperativeUnit] = []
    current: Optional[OperativeUnit] = None
    for atom in atoms:
        if atom.kind == AtomKind.LETTER:
            current = OperativeUnit(
                base=atom,
                marks=[],
                evidence=Evidence("attach_marks_contract", "Base letter opens operative unit", Rank.CERT),
                rank=Rank.CERT,
            )
            units.append(current)
        elif atom.kind in {AtomKind.SHORT_VOWEL, AtomKind.MARK}:
            if current is None:
                units.append(
                    OperativeUnit(
                        base=atom,
                        marks=[],
                        evidence=Evidence("attach_marks_contract", "Mark without base letter", Rank.ZERO),
                        rank=Rank.ZERO,
                        residuals=[Residual("mark_without_base", "Mark appears without base letter", Severity.BLOCKER)],
                    )
                )
            else:
                current.marks.append(atom)
        elif atom.kind in {AtomKind.SPACE, AtomKind.PUNCTUATION, AtomKind.TATWEEL}:
            continue
        elif current is not None:
            current.residuals.extend(atom.residuals)
    return units


@dataclass
class ContextUnit:
    prev: Optional[OperativeUnit]
    current: OperativeUnit
    next: Optional[OperativeUnit]
    position: str
    boundary: str
    residuals: List[Residual] = field(default_factory=list)

    def explain(self) -> Dict[str, Any]:
        return {
            "prev": self.prev.text() if self.prev else None,
            "current": self.current.text(),
            "next": self.next.text() if self.next else None,
            "position": self.position,
            "boundary": self.boundary,
            "residuals": [r.code for r in self.residuals],
        }


def build_context(units: List[OperativeUnit]) -> List[ContextUnit]:
    def determine_position(index: int, total: int) -> str:
        if index == 0:
            return "start"
        if index == total - 1:
            return "end"
        return "middle"

    def determine_boundary(position: str) -> str:
        if position == "start":
            return "entry_gate"
        if position == "end":
            return "judgment_gate"
        return "internal"

    result: List[ContextUnit] = []
    n = len(units)
    for i, unit in enumerate(units):
        pos = determine_position(i, n)
        boundary = determine_boundary(pos)
        residuals = []
        if not unit.marks:
            residuals.append(
                Residual(
                    "missing_visible_haraka",
                    "No visible haraka; candidate requires further ranking",
                    Severity.WARNING,
                )
            )
        result.append(
            ContextUnit(
                prev=units[i - 1] if i > 0 else None,
                current=unit,
                next=units[i + 1] if i + 1 < n else None,
                position=pos,
                boundary=boundary,
                residuals=residuals,
            )
        )
    return result


@dataclass
class Syllable:
    units: List[OperativeUnit]
    pattern: str
    evidence: Evidence
    rank: Rank
    residuals: List[Residual] = field(default_factory=list)

    def text(self) -> str:
        return "".join(u.text() for u in self.units)


def fold_syllables(units: List[OperativeUnit]) -> List[Syllable]:
    syllables: List[Syllable] = []
    n = len(units)
    i = 0
    while i < n:
        unit = units[i]
        names = unit.mark_names()
        if "sukun" in names and not syllables:
            syllables.append(
                Syllable(
                    units=[unit],
                    pattern="Cْ",
                    evidence=Evidence("syllable_contract", "Initial sukun witness", Rank.ZERO),
                    rank=Rank.ZERO,
                    residuals=[Residual("initial_sukun", "Initial sukun needs prior context", Severity.BLOCKER)],
                )
            )
            i += 1
            continue

        has_short_vowel = any(v in names for v in SHORT_VOWEL_NAMES)
        if has_short_vowel:
            if i + 1 < n and units[i + 1].has_mark("sukun"):
                syllables.append(
                    Syllable(
                        units=[unit, units[i + 1]],
                        pattern="CVC",
                        evidence=Evidence("syllable_contract", "CV followed by sukun folded as CVC", Rank.CERT),
                        rank=Rank.CERT,
                    )
                )
                i += 2
            else:
                syllables.append(
                    Syllable(
                        units=[unit],
                        pattern="CV",
                        evidence=Evidence("syllable_contract", "Short vowel folded as CV", Rank.CERT),
                        rank=Rank.CERT,
                    )
                )
                i += 1
        else:
            syllables.append(
                Syllable(
                    units=[unit],
                    pattern="C?",
                    evidence=Evidence("syllable_contract", "Missing vowel keeps form-level candidate", Rank.FORM),
                    rank=Rank.FORM,
                    residuals=[Residual("undetermined_vowel", "Vowel is undetermined", Severity.WARNING)],
                )
            )
            i += 1
    return syllables


@dataclass
class DForm:
    candidate: str
    raw_text: str
    units: List[OperativeUnit]
    contexts: List[ContextUnit]
    syllables: List[Syllable]
    evidence: List[Evidence]
    rank: Rank
    residuals: List[Residual]
    trace: Dict[str, Any]

    @property
    def normalized_text(self) -> str:
        return self.candidate


def build_d_form(text: str) -> DForm:
    atoms = atoms_from_text(text)
    units = attach_marks(atoms)
    contexts = build_context(units)
    syllables = fold_syllables(units)

    residuals: List[Residual] = []
    for atom in atoms:
        residuals.extend(atom.residuals)
    for unit in units:
        residuals.extend(unit.residuals)
    for ctx in contexts:
        residuals.extend(ctx.residuals)
    for syll in syllables:
        residuals.extend(syll.residuals)

    rank = rank_from_residuals(residuals)

    candidate = "".join(u.text() for u in units)
    return DForm(
        candidate=candidate,
        raw_text=text,
        units=units,
        contexts=contexts,
        syllables=syllables,
        evidence=[Evidence("d_form_contract", "Formal dal closure stage", rank)],
        rank=rank,
        residuals=residuals,
        trace={
            "atoms": [
                {
                    "char": a.char,
                    "kind": a.kind.value,
                    "rank": a.rank.name,
                    "residuals": [r.code for r in a.residuals],
                }
                for a in atoms
            ],
            "contexts": [c.explain() for c in contexts],
            "syllables": [
                {
                    "text": s.text(),
                    "pattern": s.pattern,
                    "rank": s.rank.name,
                    "residuals": [r.code for r in s.residuals],
                }
                for s in syllables
            ],
        },
    )


class LexicalType(Enum):
    NOUN = "ism"
    VERB = "fiil"
    PARTICLE = "harf"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class LexiconRecord:
    form: str
    lexical_type: LexicalType
    evidence: Evidence
    notes: str = ""


@dataclass
class DLugha:
    candidate: str
    form: DForm
    record: Optional[LexiconRecord]
    evidence: List[Evidence]
    rank: Rank
    residuals: List[Residual]
    trace: Dict[str, Any]


def prove_lugha(d_form: DForm, lexicon: Dict[str, LexiconRecord]) -> DLugha:
    key = d_form.normalized_text
    if key in lexicon:
        record = lexicon[key]
        trace = dict(d_form.trace)
        trace["lugha"] = {
            "status": "attested",
            "source": record.evidence.source,
            "rank": record.evidence.rank.name,
        }
        return DLugha(
            candidate=key,
            form=d_form,
            record=record,
            evidence=[record.evidence],
            rank=record.evidence.rank,
            residuals=list(d_form.residuals),
            trace=trace,
        )

    residuals = list(d_form.residuals)
    residuals.append(
        Residual(
            "not_attested_in_seed_lexicon",
            "Candidate is not attested in seed lexicon",
            Severity.WARNING,
        )
    )
    trace = dict(d_form.trace)
    trace["lugha"] = {"status": "unattested_in_seed_lexicon", "rank": "FORM"}
    return DLugha(
        candidate=key,
        form=d_form,
        record=None,
        evidence=[Evidence("seed_lexicon_lookup", "No attestation found", Rank.FORM)],
        rank=min_rank(d_form.rank, Rank.FORM),
        residuals=residuals,
        trace=trace,
    )


@dataclass
class DType:
    candidate: str
    lugha: DLugha
    lexical_type: LexicalType
    evidence: List[Evidence]
    rank: Rank
    residuals: List[Residual]
    trace: Dict[str, Any]


def infer_type(d_lugha: DLugha) -> DType:
    residuals = list(d_lugha.residuals)
    if d_lugha.record is not None:
        lexical_type = d_lugha.record.lexical_type
        rank = d_lugha.rank
        evidence = [Evidence("type_from_linguistic_record", "Type inferred from attested record", rank)]
        status = "from_linguistic_record"
    else:
        lexical_type = LexicalType.UNKNOWN
        rank = min_rank(d_lugha.rank, Rank.FORM)
        evidence = [Evidence("type_unclosed", "Type remains open without linguistic attestation", Rank.FORM)]
        status = "unknown_type"
        residuals.append(
            Residual(
                "type_not_closed",
                "Type is not closed without lexical attestation",
                Severity.WARNING,
            )
        )
    return DType(
        candidate=d_lugha.candidate,
        lugha=d_lugha,
        lexical_type=lexical_type,
        evidence=evidence,
        rank=rank,
        residuals=residuals,
        trace={
            **d_lugha.trace,
            "type": {"status": status, "lexical_type": lexical_type.value, "rank": rank.name},
        },
    )


@dataclass
class DMufrad:
    candidate: str
    text: str
    d_form: DForm
    d_lugha: DLugha
    d_type: DType
    evidence: List[Evidence]
    closed: bool
    rank: Rank
    residuals: List[Residual]
    trace: Dict[str, Any]

    def explain(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "candidate": self.candidate,
            "closed": self.closed,
            "rank": self.rank.name,
            "lexical_type": self.d_type.lexical_type.value,
            "residuals": [
                {"code": r.code, "message": r.message, "severity": r.severity.value} for r in self.residuals
            ],
            "trace": self.trace,
        }


def close_mufrad(d_type: DType) -> DMufrad:
    """Close dal-mufrad contract.

    Required conditions:
    1) no blocker residuals, 2) lexical type closed, 3) linguistic rank >= AHAD.
    """

    residuals = list(d_type.residuals)
    if d_type.lexical_type == LexicalType.UNKNOWN:
        residuals.append(
            Residual("mufrad_requires_closed_type", "Dal mufrad requires closed lexical type", Severity.WARNING)
        )
    if d_type.lugha.rank.value < Rank.AHAD.value:
        residuals.append(
            Residual("mufrad_requires_lugha_rank", "Dal mufrad requires linguistic attestation rank", Severity.WARNING)
        )

    closed = (
        not has_blocking_residuals(residuals)
        and d_type.lexical_type != LexicalType.UNKNOWN
        and d_type.rank.value >= Rank.AHAD.value
    )
    rank = d_type.rank if closed else min_rank(d_type.rank, Rank.FORM)
    return DMufrad(
        candidate=d_type.candidate,
        text=d_type.lugha.form.normalized_text,
        d_form=d_type.lugha.form,
        d_lugha=d_type.lugha,
        d_type=d_type,
        evidence=[Evidence("d_mufrad_contract", "Dal closure only, without semantics", rank)],
        closed=closed,
        rank=rank,
        residuals=residuals,
        trace={
            **d_type.trace,
            "mufrad": {"closed": closed, "rank": rank.name, "note": "dal only; no meaning/model intent"},
        },
    )


def analyze_dal_mufrad(text: str, lexicon: Dict[str, LexiconRecord]) -> DMufrad:
    d_form = build_d_form(text)
    d_lugha = prove_lugha(d_form, lexicon)
    d_type = infer_type(d_lugha)
    return close_mufrad(d_type)


SEED_LEXICON: Dict[str, LexiconRecord] = {
    "كَتَبَ": LexiconRecord(
        form="كَتَبَ",
        lexical_type=LexicalType.VERB,
        evidence=Evidence("seed_attestation", "Seed attested Arabic verb", Rank.AHAD),
    ),
    "كِتَاب": LexiconRecord(
        form="كِتَاب",
        lexical_type=LexicalType.NOUN,
        evidence=Evidence("seed_attestation", "Seed attested Arabic noun", Rank.AHAD),
    ),
    "مِنْ": LexiconRecord(
        form="مِنْ",
        lexical_type=LexicalType.PARTICLE,
        evidence=Evidence("seed_attestation", "Seed attested Arabic particle", Rank.AHAD),
    ),
}
