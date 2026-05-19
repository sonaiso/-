"""
Composition Readiness for MufradProof (جاهزية التركيب لبرهان المفرد)

Explicit states tracking whether MufradProof is ready for syntax composition.
"""

from enum import Enum


class CompositionReadiness(Enum):
    """
    جاهزية التركيب (Composition Readiness)

    Explicit readiness levels for syntax composition.

    Each level has specific requirements that must be met.
    """

    NOT_READY = "غير جاهز"
    """
    غير جاهز للتركيب

    Missing basic requirements:
    - Missing form/lugha/type
    - Blocker residuals present
    - Required feature slots empty
    """

    READY_AS_HYPOTHESIS = "جاهز كفرضية"
    """
    جاهز كفرضية فقط

    Basic proof exists but:
    - Some required morphological features unresolved
    - Some surface effects untraced
    - Rank insufficient for certificate
    - Can participate in composition but output will be hypothesis
    """

    READY_FOR_COMPOSITION = "جاهز للتركيب"
    """
    جاهز للتركيب العادي

    Sufficient features for syntax to consume:
    - Form/lugha/type present
    - No blocker residuals
    - Essential morph features resolved
    - But some competitors or residuals remain
    - Composition output will inherit limitations
    """

    READY_FOR_CERTIFICATE_COMPOSITION = "جاهز لتركيب موثق"
    """
    جاهز للتركيب الموثق

    Highest readiness:
    - No blockers
    - Required morph slots fully resolved
    - Surface effects fully traced
    - Competitors resolved or ranked
    - Rank sufficient (SAMA, AHAD, or TAWATUR)
    - Composition can issue certificate (if other constraints met)
    """

    def allows_composition(self) -> bool:
        """Check if any level of composition is allowed"""
        return self in {
            CompositionReadiness.READY_AS_HYPOTHESIS,
            CompositionReadiness.READY_FOR_COMPOSITION,
            CompositionReadiness.READY_FOR_CERTIFICATE_COMPOSITION,
        }

    def allows_certificate(self) -> bool:
        """Check if certificate-level composition is allowed"""
        return self == CompositionReadiness.READY_FOR_CERTIFICATE_COMPOSITION

    def __str__(self) -> str:
        return self.value
