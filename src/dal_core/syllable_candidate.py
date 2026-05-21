"""
Syllable Candidate Layer (D1) - PR #30

Domain: SYLLABIC (D1)
Transition: Atom sequence → Syllable candidates
Purpose: Generate syllable structure candidates with boundaries

Implements PR #30 deliverables:
- SyllableCandidate class following DalCandidateProtocol
- Syllable candidate generator (atom → syllable transitions)
- Syllable boundary detection
- Evidence-based syllable validation
"""

from dataclasses import dataclass, field
from typing import List, Optional
from uuid import uuid4

from dal_core.atoms import ArabicAtom, AtomKind
from dal_core.syllables import (
    Syllable,
    SyllableType,
    handle_shadda,
    handle_tanwin,
    handle_sukun,
    handle_madd,
    is_long_vowel_sequence,
    validate_syllable_pattern
)
from dal_core.dal_algebra import (
    DalTransitionDomain,
    DalClaimScope,
    DalEvidence,
    DalCounterEvidence,
    DalTraceRef
)
from dal_core.residuals import Residual, make_blocker, make_warning, ResidualType


@dataclass
class SyllableCandidate:
    """
    Syllable Candidate (D1 Domain)

    Follows DalCandidateProtocol for typed transition algebra.

    Each candidate represents one possible syllabification of an atom sequence.
    Multiple candidates may exist for ambiguous sequences.
    """
    # Required by DalCandidateProtocol
    candidate_id: str = field(default_factory=lambda: f"syl-{uuid4().hex[:8]}")
    domain: DalTransitionDomain = DalTransitionDomain.SYLLABIC
    evidence: List[DalEvidence] = field(default_factory=list)
    counter_evidence: List[DalCounterEvidence] = field(default_factory=list)

    # Syllable-specific fields
    syllable: Syllable = field(default_factory=lambda: Syllable(type=SyllableType.CV))
    source_atoms: List[ArabicAtom] = field(default_factory=list)
    span: tuple[int, int] = (0, 0)  # Position in source atom sequence

    # Transition metadata
    trace: Optional[DalTraceRef] = None
    residuals: List[Residual] = field(default_factory=list)
    confidence: float = 1.0  # [0.0, 1.0]

    def __post_init__(self):
        """Validate candidate invariants."""
        if not (0.0 <= self.confidence <= 1.0):
            raise ValueError(f"Confidence must be in [0.0, 1.0], got {self.confidence}")
        if self.span[0] > self.span[1]:
            raise ValueError(f"Invalid span: start > end ({self.span})")
        if self.span[0] < 0:
            raise ValueError(f"Invalid span: negative start ({self.span})")

    def is_valid(self) -> bool:
        """Check if this candidate has no blocking residuals."""
        return not any(r.is_blocker() for r in self.residuals)

    def has_blocker(self) -> bool:
        """Check if this candidate has blocking residuals."""
        return any(r.is_blocker() for r in self.residuals)


@dataclass
class SyllableCandidateSet:
    """
    Set of syllable candidates for a word.

    Bounded candidate set (|candidates| < ∞).
    Preserves competitors for ambiguous syllabifications.
    """
    candidates: List[SyllableCandidate] = field(default_factory=list)
    source_atoms: List[ArabicAtom] = field(default_factory=list)
    global_residuals: List[Residual] = field(default_factory=list)

    def __len__(self) -> int:
        return len(self.candidates)

    def valid_candidates(self) -> List[SyllableCandidate]:
        """Return candidates without blockers."""
        return [c for c in self.candidates if c.is_valid()]

    def best_candidate(self) -> Optional[SyllableCandidate]:
        """Return highest confidence valid candidate, if any."""
        valid = self.valid_candidates()
        if not valid:
            return None
        return max(valid, key=lambda c: c.confidence)


def detect_syllable_boundaries(atoms: List[ArabicAtom]) -> List[tuple[int, int]]:
    """
    Detect syllable boundaries in atom sequence.

    Returns: List of (start, end) spans for each syllable.

    Arabic syllable patterns:
    - CV: consonant + short vowel
    - CVC: consonant + short vowel + consonant
    - CVV: consonant + long vowel
    - CVVC: consonant + long vowel + consonant
    - CVCC: consonant + short vowel + consonant + consonant
    """
    boundaries = []
    i = 0

    while i < len(atoms):
        # Skip non-structural atoms (marks, spaces, etc.)
        if atoms[i].kind in {AtomKind.SPACE, AtomKind.PUNCT}:
            i += 1
            continue

        # Syllable must start with consonant (onset)
        if atoms[i].kind != AtomKind.LETTER:
            # Invalid: syllable without onset
            # Skip and continue
            i += 1
            continue

        start = i
        onset_end = i + 1  # Single consonant onset

        # Check for nucleus (required)
        nucleus_start = onset_end
        nucleus_end = nucleus_start

        # Look for vowel
        if nucleus_start < len(atoms):
            # Check for long vowel sequence (CV + madd letter)
            if is_long_vowel_sequence(atoms, nucleus_start):
                nucleus_end = nucleus_start + 2  # vowel + letter
            elif atoms[nucleus_start].kind == AtomKind.VOWEL:
                nucleus_end = nucleus_start + 1
            elif atoms[nucleus_start].kind == AtomKind.SUKUN:
                # Sukun as nucleus (rare, word-final only)
                nucleus_end = nucleus_start + 1

        # Check for coda (optional)
        coda_start = nucleus_end
        coda_end = coda_start

        if coda_start < len(atoms):
            # Single consonant coda
            if atoms[coda_start].kind == AtomKind.LETTER:
                coda_end = coda_start + 1

                # Check for double consonant coda (CVCC)
                if coda_end < len(atoms) and atoms[coda_end].kind == AtomKind.LETTER:
                    # Check if next is also coda or starts new syllable
                    # For now, treat as single coda
                    pass

        # Create boundary
        end = max(nucleus_end, coda_end, onset_end)
        if end > start:
            boundaries.append((start, end))

        i = end

    return boundaries


def classify_syllable_type(
    onset: List[ArabicAtom],
    nucleus: List[ArabicAtom],
    coda: List[ArabicAtom]
) -> SyllableType:
    """
    Classify syllable based on structure.

    Returns: SyllableType enum value
    """
    has_long_nucleus = len(nucleus) > 1
    has_coda = len(coda) > 0
    has_double_coda = len(coda) > 1

    if has_double_coda:
        return SyllableType.CVCC
    elif has_long_nucleus and has_coda:
        return SyllableType.CVVC
    elif has_long_nucleus and not has_coda:
        return SyllableType.CVV
    elif not has_long_nucleus and has_coda:
        return SyllableType.CVC
    else:
        return SyllableType.CV


def generate_syllable_candidate(
    atoms: List[ArabicAtom],
    span: tuple[int, int],
    candidate_id: Optional[str] = None
) -> SyllableCandidate:
    """
    Generate a single syllable candidate from atom sequence.

    Args:
        atoms: Full atom sequence
        span: (start, end) indices for this syllable
        candidate_id: Optional explicit ID

    Returns: SyllableCandidate
    """
    start, end = span
    syllable_atoms = atoms[start:end]

    # Separate onset, nucleus, coda
    onset = []
    nucleus = []
    coda = []
    residuals = []

    i = 0
    # Extract onset (consonant)
    while i < len(syllable_atoms) and syllable_atoms[i].kind == AtomKind.LETTER:
        onset.append(syllable_atoms[i])
        i += 1
        break  # Single consonant onset for now

    # Extract nucleus (vowel or long vowel)
    if i < len(syllable_atoms):
        if is_long_vowel_sequence(syllable_atoms, i):
            nucleus = [syllable_atoms[i], syllable_atoms[i + 1]]
            i += 2
        elif syllable_atoms[i].kind in {AtomKind.VOWEL, AtomKind.SUKUN}:
            nucleus.append(syllable_atoms[i])
            i += 1

    # Extract coda (consonant(s))
    while i < len(syllable_atoms) and syllable_atoms[i].kind == AtomKind.LETTER:
        coda.append(syllable_atoms[i])
        i += 1

    # Handle special atoms (shadda, tanwin)
    for atom in syllable_atoms:
        if atom.kind == AtomKind.SUKUN:
            sukun_residuals = handle_sukun(atom, 'coda' if coda else 'onset')
            residuals.extend(sukun_residuals)

    # Classify syllable type
    syll_type = classify_syllable_type(onset, nucleus, coda)

    # Create syllable
    syllable = Syllable(
        type=syll_type,
        onset=onset,
        nucleus=nucleus,
        coda=coda,
        trace={
            'span': span,
            'atom_count': len(syllable_atoms),
            'method': 'boundary_detection'
        }
    )

    # Validate syllable
    validation_residuals = validate_syllable_pattern(syllable)
    residuals.extend(validation_residuals)

    # Create evidence
    evidence = [
        DalEvidence(
            source="syllable_boundary_detection",
            claim_scope=DalClaimScope.SYLLABLE_STRUCTURE_VALID,
            span=span,
            confidence=0.9,
            details={
                'type': syll_type.value,
                'onset_count': len(onset),
                'nucleus_count': len(nucleus),
                'coda_count': len(coda)
            }
        )
    ]

    # Create trace
    trace = DalTraceRef(
        transition_id="d0-to-d1-syllabification",
        source_domain=DalTransitionDomain.GRAPHOPHONEMIC,
        target_domain=DalTransitionDomain.SYLLABIC,
        timestamp="",  # Would be filled by orchestrator
        reversible=True,
        metadata={
            'atoms_consumed': len(syllable_atoms),
            'syllable_type': syll_type.value
        }
    )

    # Compute confidence
    confidence = 0.9 if not validation_residuals else 0.5

    return SyllableCandidate(
        candidate_id=candidate_id or f"syl-{uuid4().hex[:8]}",
        domain=DalTransitionDomain.SYLLABIC,
        evidence=evidence,
        counter_evidence=[],
        syllable=syllable,
        source_atoms=syllable_atoms,
        span=span,
        trace=trace,
        residuals=residuals,
        confidence=confidence
    )


def generate_syllable_candidates(atoms: List[ArabicAtom]) -> SyllableCandidateSet:
    """
    Generate syllable candidates for entire atom sequence.

    This is the main D0 → D1 transition function.

    Args:
        atoms: Atom sequence from D0 (GRAPHOPHONEMIC domain)

    Returns: SyllableCandidateSet with all candidates
    """
    candidates = []
    global_residuals = []

    # Detect boundaries
    boundaries = detect_syllable_boundaries(atoms)

    if not boundaries:
        # No syllables detected - add warning
        global_residuals.append(make_warning(
            ResidualType.INVALID_SYLLABLE,
            "No syllable boundaries detected in atom sequence",
            location="syllabification"
        ))
        return SyllableCandidateSet(
            candidates=[],
            source_atoms=atoms,
            global_residuals=global_residuals
        )

    # Generate candidate for each boundary
    for i, span in enumerate(boundaries):
        candidate = generate_syllable_candidate(
            atoms=atoms,
            span=span,
            candidate_id=f"syl-{i:03d}"
        )
        candidates.append(candidate)

    return SyllableCandidateSet(
        candidates=candidates,
        source_atoms=atoms,
        global_residuals=global_residuals
    )


# Convenience function for single-word syllabification
def syllabify_word(atoms: List[ArabicAtom]) -> List[SyllableCandidate]:
    """
    Syllabify a word (atom sequence) into syllable candidates.

    Returns: List of valid syllable candidates
    """
    candidate_set = generate_syllable_candidates(atoms)
    return candidate_set.valid_candidates()
