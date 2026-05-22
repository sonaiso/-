"""
EmbodiedObserver - The Observer is Part of Reality

Critical principle: The observer is NOT external to reality.
The observer is an embodied entity within reality.

The embodied human is the first reality:
- Body (physical substrate)
- Sensation (sensory capability)
- Pain (suffering, discomfort)
- Need (hunger, thirst, warmth, safety)
- Action (movement, interaction)

Critical laws:
- Observer is part of SelfReality
- Observer has body state (alive, functioning, limited)
- Observer has needs (biological requirements)
- Observer actions affect reality
- Observer cannot escape embodiment
- Observer limitations are reality constraints
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, FrozenSet, Set
from uuid import UUID, uuid4


class BodyState(Enum):
    """State of the embodied observer's body."""
    FUNCTIONAL = auto()      # Body is functional
    IMPAIRED = auto()        # Body has impairments
    DAMAGED = auto()         # Body is damaged
    RECOVERING = auto()      # Body is recovering
    DEGRADING = auto()       # Body is degrading


class NeedState(Enum):
    """State of biological needs."""
    SATISFIED = auto()       # Needs are satisfied
    EMERGING = auto()        # Needs are emerging
    URGENT = auto()          # Needs are urgent
    CRITICAL = auto()        # Needs are critical
    UNMET = auto()           # Needs are unmet (dangerous)


@dataclass(frozen=True)
class EmbodiedObserver:
    """
    The embodied observer - part of reality, not external to it.

    This represents the observer as an embodied entity with:
    - Physical body (substrate)
    - Sensory capabilities (channels)
    - Biological needs (requirements)
    - Action capabilities (effects on reality)
    - Limitations (constraints)

    CRITICAL: Observer is in SelfReality domain.
    """

    # Observer identity
    observer_id: str

    # Body state
    body_state: BodyState

    # Need state
    need_state: NeedState

    # Sensory capabilities (what channels are available)
    available_sensory_channels: FrozenSet[str]

    # Action capabilities (what actions are possible)
    available_actions: FrozenSet[str]

    # Biological needs (what is required for survival/function)
    biological_needs: FrozenSet[str]

    # Fields with defaults (must come last)
    trace_id: UUID = field(default_factory=uuid4)
    known_limitations: Optional[FrozenSet[str]] = None
    impairments: Optional[FrozenSet[str]] = None
    current_context: Optional[str] = None

    def __post_init__(self):
        # Validate observer_id
        if not self.observer_id or not self.observer_id.strip():
            raise ValueError("observer_id cannot be empty")

        # Validate sensory channels
        if not self.available_sensory_channels:
            raise ValueError("available_sensory_channels cannot be empty")

        # Validate actions
        if not self.available_actions:
            raise ValueError("available_actions cannot be empty")

        # Validate biological needs
        if not self.biological_needs:
            raise ValueError("biological_needs cannot be empty")

        # Convert sets to frozensets for immutability
        if not isinstance(self.available_sensory_channels, frozenset):
            object.__setattr__(
                self,
                'available_sensory_channels',
                frozenset(self.available_sensory_channels)
            )

        if not isinstance(self.available_actions, frozenset):
            object.__setattr__(
                self,
                'available_actions',
                frozenset(self.available_actions)
            )

        if not isinstance(self.biological_needs, frozenset):
            object.__setattr__(
                self,
                'biological_needs',
                frozenset(self.biological_needs)
            )

        if self.known_limitations and not isinstance(self.known_limitations, frozenset):
            object.__setattr__(
                self,
                'known_limitations',
                frozenset(self.known_limitations)
            )

        if self.impairments and not isinstance(self.impairments, frozenset):
            object.__setattr__(
                self,
                'impairments',
                frozenset(self.impairments)
            )

    @property
    def is_functional(self) -> bool:
        """Check if observer body is functional."""
        return self.body_state == BodyState.FUNCTIONAL

    @property
    def has_impairments(self) -> bool:
        """Check if observer has impairments."""
        return self.body_state == BodyState.IMPAIRED or bool(self.impairments)

    @property
    def needs_are_critical(self) -> bool:
        """Check if biological needs are in critical state."""
        return self.need_state in {NeedState.CRITICAL, NeedState.UNMET}

    @property
    def can_observe(self) -> bool:
        """
        Can this observer perform observations?

        Requires: functional body and available sensory channels.
        """
        return self.is_functional and bool(self.available_sensory_channels)

    @property
    def can_act(self) -> bool:
        """
        Can this observer perform actions?

        Requires: functional body and available actions.
        """
        return self.is_functional and bool(self.available_actions)

    def has_sensory_channel(self, channel: str) -> bool:
        """Check if observer has specific sensory channel."""
        return channel in self.available_sensory_channels

    def can_perform_action(self, action: str) -> bool:
        """Check if observer can perform specific action."""
        return action in self.available_actions and self.can_act

    def is_external_to_reality(self) -> bool:
        """
        Is this observer external to reality?

        CRITICAL LAW: NO. Observer is part of reality.
        """
        return False

    def can_escape_embodiment(self) -> bool:
        """
        Can this observer escape embodiment?

        CRITICAL LAW: NO. Observer cannot escape embodiment.
        """
        return False

    def __str__(self) -> str:
        return (
            f"EmbodiedObserver("
            f"id={self.observer_id}, "
            f"body={self.body_state.name}, "
            f"needs={self.need_state.name})"
        )
