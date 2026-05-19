"""
Sentence Frame Proof (برهان إطار الجملة)

Typed frame candidates built from PreSyntaxMufradVector list.

CRITICAL ARCHITECTURE:
This layer transforms list[PreSyntaxMufradVector] → SentenceFrameCandidate.

It does NOT:
- Work on raw tokens (operators already forbidden from that)
- Apply operators (operators come AFTER frame identification)
- Assign CaseEffect (still at potential/candidate level)
- Determine final syntax roles (faail, mafool... come with operators)
- Infer meaning/semantic (dal-only architecture)
- Elevate rank (rank ≤ min(constituent ranks))

It DOES:
- Identify structural frame types (nominal, verbal, particle-led, fragment, unresolved)
- Inherit ALL residuals from constituent mufrad proofs
- Preserve rank ceiling theorem
- Provide typed interface for future operator consumption
- Enable governed composition without hallucination

Mathematical Foundation:
```
list[PreSyntaxMufradVector] → FrameIdentifier → SentenceFrameCandidate
```

NOT:
```
list[Token] → DirectParser → SyntaxTree  (FORBIDDEN!)
```
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum

from dal_core.presyntax_vector import PreSyntaxMufradVector
from dal_core.ranks import LughaRank
from dal_core.residuals import Residual
from dal_core.type_ids import NounTypeID, VerbTypeID, ParticleTypeID


class FrameType(Enum):
    """
    Frame type classification (تصنيف نوع الإطار)

    These are structural candidates, NOT semantic judgments.
    """
    NOMINAL = "nominal"           # جملة اسمية مرشحة
    VERBAL = "verbal"             # جملة فعلية مرشحة
    PARTICLE_LED = "particle_led" # جملة بحرف مرشح
    FRAGMENT = "fragment"         # شبه جملة / مفرد مرشح
    UNRESOLVED = "unresolved"     # إطار غير محسوم


@dataclass(frozen=True)
class SentenceFrameCandidate:
    """
    Base class for sentence frame candidates.

    A frame is a CANDIDATE structural pattern, not a definitive parse.

    All frames must:
    1. Preserve rank ceiling: rank ≤ min(constituent_ranks)
    2. Inherit ALL residuals from constituents
    3. Have NO semantic/meaning fields
    4. Have NO final syntax roles (faail, mafool...)
    5. Have NO case effects (marfoo_by, mansub_by...)
    """

    frame_id: str
    """Unique identifier for this frame candidate"""

    frame_type: FrameType
    """Type of frame candidate"""

    constituents: tuple[PreSyntaxMufradVector, ...]
    """Constituent mufrad vectors (must preserve order)"""

    frame_rank: LughaRank
    """Frame rank: MUST be ≤ min(constituent ranks)"""

    inherited_residuals: tuple[Residual, ...]
    """ALL residuals from constituents (union)"""

    frame_specific_residuals: tuple[Residual, ...]
    """New residuals specific to frame composition"""

    trace_id: str
    """Trace identifier linking to constituent proofs"""

    def __post_init__(self):
        """Validate frame construction rules"""
        # Forbidden fields check
        forbidden_fields = [
            'meaning', 'semantic', 'madlul', 'murad',
            'haqiqa', 'majaz',
            'faail', 'mafool', 'mubtada', 'khabar',
            'case_effect', 'marfoo_by', 'mansub_by', 'majroor_by',
            'governed_by_operator', 'operator_id',
        ]

        field_names = {f.name for f in self.__dataclass_fields__.values()}
        violations = field_names.intersection(forbidden_fields)
        if violations:
            raise ValueError(
                f"SentenceFrameCandidate contains forbidden fields: {violations}"
            )

        # Verify rank ceiling theorem
        if self.constituents:
            min_constituent_rank = min(c.final_rank for c in self.constituents)
            if self.frame_rank.value > min_constituent_rank.value:
                raise ValueError(
                    f"Rank ceiling violated: frame_rank ({self.frame_rank.value}) > "
                    f"min_constituent_rank ({min_constituent_rank.value})"
                )

    def get_all_residuals(self) -> tuple[Residual, ...]:
        """Get combined residuals (inherited + frame-specific)"""
        return self.inherited_residuals + self.frame_specific_residuals

    def allows_operator_application(self) -> bool:
        """
        Check if frame is ready for operator application.

        Base implementation: all constituents must allow consumption.
        Subclasses may add frame-specific checks.
        """
        return all(c.allows_operator_consumption() for c in self.constituents)


@dataclass(frozen=True)
class NominalFrameCandidate(SentenceFrameCandidate):
    """
    Nominal sentence frame candidate (جملة اسمية مرشحة)

    Pattern: ISM + ... (potential mubtada + khabar pattern)

    This identifies a CANDIDATE nominal structure.
    It does NOT assign mubtada/khabar roles (operators do that).

    Example: "الكتابُ جديدٌ" → NominalFrameCandidate
    - constituents[0]: الكتابُ (ISM with DAMMA potential)
    - constituents[1]: جديدٌ (ISM with TANWIN potential)

    Operators will later decide:
    - Is constituents[0] actually mubtada? (needs absence of operator)
    - Is constituents[1] actually khabar? (needs agreement check)
    """

    lead_noun_index: int
    """Index of leading noun in constituents (potential mubtada)"""

    def __post_init__(self):
        super().__post_init__()

        # Verify frame_type
        object.__setattr__(self, 'frame_type', FrameType.NOMINAL)

        # Verify lead noun exists and is ISM
        if not (0 <= self.lead_noun_index < len(self.constituents)):
            raise ValueError(
                f"lead_noun_index {self.lead_noun_index} out of range for "
                f"{len(self.constituents)} constituents"
            )

        lead = self.constituents[self.lead_noun_index]
        if not isinstance(lead.type_id, NounTypeID):
            raise ValueError(
                f"Lead constituent at index {self.lead_noun_index} must be ISM, "
                f"got {lead.type_value}"
            )


@dataclass(frozen=True)
class VerbalFrameCandidate(SentenceFrameCandidate):
    """
    Verbal sentence frame candidate (جملة فعلية مرشحة)

    Pattern: FIIL + ... (potential verb + subject + objects pattern)

    This identifies a CANDIDATE verbal structure.
    It does NOT assign faail/mafool roles (operators do that).

    Example: "كَتَبَ الطالبُ الدرسَ" → VerbalFrameCandidate
    - constituents[0]: كَتَبَ (FIIL_MADI with verb features)
    - constituents[1]: الطالبُ (ISM with DAMMA potential)
    - constituents[2]: الدرسَ (ISM with FATHA potential)

    Operators will later decide:
    - Is constituents[1] actually faail? (needs verb-subject agreement)
    - Is constituents[2] actually mafool? (needs verb valency check)
    """

    verb_index: int
    """Index of verb in constituents"""

    def __post_init__(self):
        super().__post_init__()

        # Verify frame_type
        object.__setattr__(self, 'frame_type', FrameType.VERBAL)

        # Verify verb exists and is FIIL
        if not (0 <= self.verb_index < len(self.constituents)):
            raise ValueError(
                f"verb_index {self.verb_index} out of range for "
                f"{len(self.constituents)} constituents"
            )

        verb = self.constituents[self.verb_index]
        if not isinstance(verb.type_id, VerbTypeID):
            raise ValueError(
                f"Verb constituent at index {self.verb_index} must be FIIL, "
                f"got {verb.type_value}"
            )


@dataclass(frozen=True)
class ParticleLedFrameCandidate(SentenceFrameCandidate):
    """
    Particle-led frame candidate (جملة بحرف مرشح)

    Pattern: HARF + ... (particle + governed structure)

    This identifies a CANDIDATE particle-led structure.
    It does NOT apply operator governance (operators do that).

    Example: "إنَّ الكتابَ جديدٌ" → ParticleLedFrameCandidate
    - constituents[0]: إنَّ (HARF_NASIKH_INNA)
    - constituents[1]: الكتابَ (ISM with FATHA potential)
    - constituents[2]: جديدٌ (ISM with TANWIN potential)

    Operators will later decide:
    - Does إنَّ govern constituents[1] as ism-inna?
    - Does إنَّ affect case of constituents[1]?
    - Is constituents[2] khabar-inna?
    """

    particle_index: int
    """Index of leading particle in constituents"""

    particle_operator_potential: Optional[str]
    """Operator potential from particle (if any)"""

    def __post_init__(self):
        super().__post_init__()

        # Verify frame_type
        object.__setattr__(self, 'frame_type', FrameType.PARTICLE_LED)

        # Verify particle exists and is HARF
        if not (0 <= self.particle_index < len(self.constituents)):
            raise ValueError(
                f"particle_index {self.particle_index} out of range for "
                f"{len(self.constituents)} constituents"
            )

        particle = self.constituents[self.particle_index]
        if not isinstance(particle.type_id, ParticleTypeID):
            raise ValueError(
                f"Particle constituent at index {self.particle_index} must be HARF, "
                f"got {particle.type_value}"
            )


@dataclass(frozen=True)
class FragmentFrameCandidate(SentenceFrameCandidate):
    """
    Fragment frame candidate (شبه جملة / مفرد مرشح)

    A fragment is a structure that doesn't form a complete sentence.
    Examples:
    - Prepositional phrase: "في البيتِ"
    - Adverbial: "أمسِ"
    - Single noun: "الكتابُ" (without predicate)
    - Incomplete verbal: "كَتَبَ" (without required arguments)

    Fragments may:
    - Be part of larger sentence (prepositional phrase modifying noun)
    - Require additional context to become complete
    - Have unresolved structural dependencies
    """

    fragment_reason: str
    """Why this is classified as fragment (missing_predicate, prepositional_phrase, etc.)"""

    def __post_init__(self):
        super().__post_init__()

        # Verify frame_type
        object.__setattr__(self, 'frame_type', FrameType.FRAGMENT)


@dataclass(frozen=True)
class UnresolvedFrameCandidate(SentenceFrameCandidate):
    """
    Unresolved frame candidate (إطار غير محسوم)

    When frame type cannot be confidently determined due to:
    - Ambiguous constituent types
    - Multiple competing frame interpretations
    - Insufficient morphological resolution
    - Blocking residuals in constituents

    This is NOT an error - it's a honest admission of uncertainty.
    Operators may still attempt to work with unresolved frames,
    or may reject them based on confidence thresholds.
    """

    competing_frame_types: tuple[FrameType, ...]
    """Competing frame type hypotheses"""

    unresolved_reason: str
    """Why frame type is unresolved"""

    def __post_init__(self):
        super().__post_init__()

        # Verify frame_type
        object.__setattr__(self, 'frame_type', FrameType.UNRESOLVED)

        # Verify competing types are provided
        if not self.competing_frame_types:
            raise ValueError(
                "UnresolvedFrameCandidate must have at least one competing frame type"
            )


def calculate_frame_rank(constituents: tuple[PreSyntaxMufradVector, ...]) -> LughaRank:
    """
    Calculate frame rank applying rank ceiling theorem.

    Frame rank = min(constituent ranks)

    This enforces Theorem 5: Composition cannot raise constituent rank.
    """
    if not constituents:
        return LughaRank.QIYAS  # Lowest rank for empty frame

    return min(c.final_rank for c in constituents)


def collect_inherited_residuals(
    constituents: tuple[PreSyntaxMufradVector, ...]
) -> tuple[Residual, ...]:
    """
    Collect all residuals from constituents.

    This enforces Theorem 6: Residual inheritance.
    All constituent residuals MUST be inherited by frame.
    """
    all_residuals = []
    for constituent in constituents:
        all_residuals.extend(constituent.residuals)

    return tuple(all_residuals)
