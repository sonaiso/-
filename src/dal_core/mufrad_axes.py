"""
Mufrad Axes (محاور المفرد قبل التركيب)

Typed, classified axes for the singular dal (لفظ مفرد) BEFORE composition.

This module is TYPES ONLY. It contains no judging logic, no registries,
no inference. It exists to give the rest of dal_core a stable, classified
vocabulary for two orthogonal judicial axes:

    1. Binaa / I'rab        (المحور الحُكمي الثالث)
    2. Ishtiqaq / Jamid     (المحور الحُكمي الرابع)

Plus an auxiliary axis that disambiguates the historically-overloaded
``NounInflectionClass.inflection_type`` string:

    3. Sarf Flexibility     (مصروف / ممنوع من الصرف)

Architectural invariants (must not be violated by any consumer):

* These axes are JUDGMENTS over a closed signifier. They are produced by
  judges in ``binaa_judge.py`` and ``ishtiqaq_judge.py`` using inputs from
  D3 (ORIGIN), D4 (TEMPLATE), and D5 (IDENTITY_AXIS).

* They MUST NOT be inferred from D1 (SYLLABIC). The number of syllables
  is descriptive, not judicial. Any code that maps ``syllable_count`` to
  ``BinaaJudgment`` is a hallucination guard violation.

* They MUST NOT carry syntactic case, syntax role, or semantic meaning.
  All three remain forbidden inside ``MufradProof``.

* The two judicial axes are orthogonal. Examples that MUST coexist:
    - هذا   : MABNI    + JAMID  (JAMID_FUNCTIONAL)
    - كاتب  : MUERAB   + MUSHTAQ (ISM_FAIL)
    - رجل   : MUERAB   + JAMID  (JAMID_DHAT)
    - الذين : MABNI    + JAMID  (JAMID_FUNCTIONAL)
    - مِنْ   : MABNI    + NOT_APPLICABLE (particle has no ishtiqaq axis)
"""

from enum import Enum


# =============================================================================
# Axis 3 — Binaa / I'rab (البناء / الإعراب)
# =============================================================================


class BinaaJudgment(Enum):
    """
    حُكم البناء/الإعراب

    A classified judgment over the singular dal as a whole. Distinct from
    ``CandidateStatus`` which only records certainty, not the value itself.
    """

    MABNI = "مبني"
    """The word is built (does not change for grammatical position)."""

    MUERAB = "معرب"
    """The word is inflectable (changes for raf'/nasb/jarr/jazm)."""

    UNRESOLVED = "غير محسوم"
    """Insufficient evidence to judge. A residual MUST be emitted."""

    NOT_APPLICABLE = "غير منطبق"
    """
    The axis does not apply to this signifier in the current scope.
    Reserved for special structural items where neither MABNI nor MUERAB
    is meaningful (rare; particles are MABNI, not NOT_APPLICABLE).
    """


class BinaaSubtype(Enum):
    """
    نوع البناء (للمبني فقط)

    Describes the LAST OBSERVED building shape on the surface. This is a
    surface description, NOT a syntactic case judgment. Even when an
    operator later assigns a case-effect, that judgment lives outside
    MufradProof; this subtype only records the visible building mark.
    """

    BINAA_SUKUN = "مبني على السكون"
    """e.g. اضْرِبْ، كَمْ، مَنْ."""

    BINAA_FATH = "مبني على الفتح"
    """e.g. ضَرَبَ، أَيْنَ."""

    BINAA_DAMM = "مبني على الضم"
    """e.g. نَحْنُ، حَيْثُ."""

    BINAA_KASR = "مبني على الكسر"
    """e.g. هؤلاءِ، أَمسِ."""

    INVARIANT_PROPER = "مبني بصورة ثابتة"
    """
    Built without an isolable end-mark (e.g. pronouns whose form is
    invariant as a whole: هو، هي، أنا، نحن in some descriptive accounts).
    Use when no single end-mark is the locus of building.
    """


# =============================================================================
# Axis 4 — Ishtiqaq / Jamid (الاشتقاق / الجمود)
# =============================================================================


class IshtiqaqJudgment(Enum):
    """
    حُكم الاشتقاق/الجمود

    Independent of BinaaJudgment. A word may be MUSHTAQ-and-MUERAB
    (كاتب), MUSHTAQ-and-MABNI (rare — e.g. some indeclinable derived
    nouns), JAMID-and-MUERAB (رجل), JAMID-and-MABNI (هذا), etc.
    """

    JAMID = "جامد"
    """The noun is non-derived (frozen). See JamidSubtype for category."""

    MUSHTAQ = "مشتق"
    """The noun is derived from a verbal root. See MushtaqSubtype."""

    UNRESOLVED = "غير محسوم"
    """Insufficient evidence to judge. A residual MUST be emitted."""

    NOT_APPLICABLE = "غير منطبق"
    """
    The axis does not apply. Used for:
      - All particles (harf): the jamid/mushtaq axis is nominal by origin.
      - All verbs: verbs are not classified jamid/mushtaq in this sense
        (their tense/voice/transitivity live in ``VerbFeatureProof``).
    """


class MushtaqSubtype(Enum):
    """
    أنواع المشتق (للأسماء المشتقة فقط)

    Closed set of classical derived-noun patterns. Each value corresponds
    to a recognizable morphological template (wazn). When a noun matches
    such a template AND is attested as derived, the judge emits one of
    these values.
    """

    ISM_FAIL = "اسم فاعل"
    """فاعل: doer (كاتب، قارئ، ضارب)."""

    ISM_MAFUL = "اسم مفعول"
    """مفعول: patient (مكتوب، مقروء، مضروب)."""

    SIFA_MUSHABBAHA = "صفة مشبهة"
    """Adjective resembling active participle (حَسَن، طَويل، كَريم)."""

    ISM_TAFDIL = "اسم تفضيل"
    """أفعل التفضيل (أفضل، أعظم، أكبر)."""

    ISM_ZAMAN = "اسم زمان"
    """Noun of time (مَوْعِد، مَوْقِف باعتبار الزمن)."""

    ISM_MAKAN = "اسم مكان"
    """Noun of place (مَكْتَب، مَدْرَسة، مَجْلِس)."""

    ISM_ALA = "اسم آلة"
    """Noun of instrument (مِفْتاح، مِنْشار، مِسْطَرَة)."""

    MASDAR_MIMI = "مصدر ميمي"
    """Mimic verbal noun (مَضْرَب بمعنى الضَّرْب)."""

    MASDAR_SINAII = "مصدر صناعي"
    """Coined verbal noun with -iyya suffix (إنسانية، حُرّية)."""


class JamidSubtype(Enum):
    """
    أنواع الجامد (للأسماء الجامدة فقط)

    Distinguishes the source-class of a frozen noun. This is essential
    because the four categories behave differently downstream:

    * JAMID_DHAT       : may be qualified, declined normally.
    * JAMID_MASDAR_ASLI: may act as a verbal noun in composition.
    * JAMID_PROPER_NAME: definite by itself, special case-sign behavior.
    * JAMID_FUNCTIONAL : closed-class structural item; usually MABNI too.
    """

    JAMID_DHAT = "جامد ذات"
    """Concrete frozen noun (رجل، حجر، شجرة، ماء)."""

    JAMID_MASDAR_ASLI = "مصدر أصلي"
    """Original (non-mimic, non-sinaii) verbal noun (ضَرْب، عِلْم، كِتاب)."""

    JAMID_PROPER_NAME = "علم"
    """Proper noun (محمد، مكة، فاطمة)."""

    JAMID_FUNCTIONAL = "جامد وظيفي"
    """
    Functional/structural frozen noun: pronoun, demonstrative, relative,
    interrogative, conditional, name-of-verb, indeclinable adverbs, and
    compound numbers. Typically MABNI on the other axis, but the axes
    remain logically independent.
    """


# =============================================================================
# Auxiliary axis — Sarf Flexibility (المصروفية)
# =============================================================================


class SarfFlexibility(Enum):
    """
    المصروفية (لأسماء معربة فقط)

    Disambiguates the historically overloaded
    ``NounInflectionClass.inflection_type`` string which mixed THREE
    different things:

      - ``"munassarif"``     ⇒ a value on the sarf-flexibility axis.
      - ``"mamnu_min_sarf"`` ⇒ a value on the sarf-flexibility axis.
      - ``"mabni"``          ⇒ a value on the binaa/i'rab axis (now removed
                               from this enum and moved to ``BinaaJudgment``).

    A word is MUNSARIF / MAMNU_MIN_SARF only if it is MUERAB on the binaa
    axis. Particles, verbs, and built nouns get NOT_APPLICABLE.
    """

    MUNSARIF = "مصروف"
    """Fully declinable noun, accepts tanwin and kasra in jarr."""

    MAMNU_MIN_SARF = "ممنوع من الصرف"
    """Diptote: no tanwin, fatha in jarr (mosques, foreign names, etc.)."""

    NOT_APPLICABLE = "غير منطبق"
    """For particles, verbs, and built (mabni) nouns."""


# =============================================================================
# Public API surface
# =============================================================================

__all__ = [
    "BinaaJudgment",
    "BinaaSubtype",
    "IshtiqaqJudgment",
    "MushtaqSubtype",
    "JamidSubtype",
    "SarfFlexibility",
]
