"""
Observer - The biological or cognitive observer receiving the sensory transfer

For biological perception, the observer matters:
- Attention state
- Prior expectations
- Perceptual biases
- Cognitive load
"""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Observer:
    """
    The observer (biological or cognitive) receiving the sensory transfer.

    CRITICAL: Observers are not neutral receivers.
    They bring attention, expectations, and biases.
    """

    observer_id: str  # Identifier for the observer

    # Observer state (optional)
    attention_state: Optional[str] = None  # e.g., "focused", "distracted", "unconscious"
    prior_expectations: Optional[str] = None
    observer_description: Optional[str] = None

    def __post_init__(self):
        if not self.observer_id or not self.observer_id.strip():
            raise ValueError("Observer requires observer_id")

    def __str__(self) -> str:
        return f"Observer({self.observer_id})"
