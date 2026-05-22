"""
Existence Types, Domains, and Channels

These define the fundamental categories of existence that can enter FirstPriorUnit.

Key Principle:
- Different existence types CANNOT imply each other without explicit bridge
- Textual/Symbolic/Acoustic existence does NOT imply Physical existence
- Hypothetical existence CANNOT be CERTIFIED

ExistenceType: The mode of existence of an entity or effect
Domain: The realm/field in which the entity/effect exists
Channel: The access pathway through which the entity/effect is observed
"""

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class ExistenceType(Enum):
    """
    The mode of existence.

    Critical distinctions:
    - PHYSICAL: Measurable physical entity/effect
    - CONCEPTUAL: Mental construct/abstraction
    - LINGUISTIC: Textual/symbolic/acoustic form
    - HYPOTHETICAL: Proposed but unverified
    - RELATIONAL: Exists as relation between other entities
    - PROCESSUAL: Exists as ongoing process
    - POTENTIAL: Possible but not actualized
    """

    PHYSICAL = auto()
    CONCEPTUAL = auto()
    LINGUISTIC = auto()
    HYPOTHETICAL = auto()
    RELATIONAL = auto()
    PROCESSUAL = auto()
    POTENTIAL = auto()

    def can_imply(self, other: "ExistenceType") -> bool:
        """
        Check if this existence type can imply another without explicit bridge.

        Critical law: LINGUISTIC/HYPOTHETICAL/CONCEPTUAL cannot imply PHYSICAL.
        """
        # Same type can imply itself
        if self == other:
            return True

        # Physical can imply relational/processual
        if self == ExistenceType.PHYSICAL:
            return other in {ExistenceType.RELATIONAL, ExistenceType.PROCESSUAL}

        # Conceptual can imply relational
        if self == ExistenceType.CONCEPTUAL:
            return other == ExistenceType.RELATIONAL

        # No other implications allowed without explicit bridge
        return False


@dataclass(frozen=True)
class Domain:
    """
    The realm or field in which an entity/effect exists.

    Examples:
    - Physical: "3D space", "electromagnetic field"
    - Conceptual: "mathematical structures", "logical propositions"
    - Linguistic: "Arabic lexicon", "phonological space"
    """

    name: str
    description: Optional[str] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Domain name cannot be empty")


@dataclass(frozen=True)
class Channel:
    """
    The access pathway through which an entity/effect is observed.

    Examples:
    - "visual perception"
    - "auditory perception"
    - "measurement instrument"
    - "logical inference"
    - "textual notation"
    - "memory recall"
    """

    name: str
    description: Optional[str] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Channel name cannot be empty")
