"""
Type ID Registry (سجل أكواد الأنواع)

Operational type identifiers for PreSyntax interface.

CRITICAL PRINCIPLE:
type_id ≠ meaning
type_id = operational key for operator entry

These are NOT semantic categories. They are typed identifiers that:
1. Enable operator contracts to check input signatures
2. Prevent operators from working on wrong types
3. Provide numerical foundation for composition

Before any operator works, each MufradProof must have a stable type_id.
"""

from enum import Enum


class NounTypeID(Enum):
    """
    أكواد أنواع الأسماء (Noun Type Identifiers)

    Operational noun subtypes for operator matching.
    These are NOT meanings - they are entry keys.
    """
    # Common nouns
    ISM_COMMON = "اسم_جنس"
    """Common noun (كتاب، رجل، بيت)"""

    ISM_PROPER = "اسم_علم"
    """Proper noun/name (محمد، مكة)"""

    # Pronouns
    ISM_PRONOUN_SEPARATE = "ضمير_منفصل"
    """Separate pronoun (أنا، أنت، هو)"""

    ISM_PRONOUN_ATTACHED = "ضمير_متصل"
    """Attached pronoun (ـه، ـك، ـي)"""

    ISM_PRONOUN_HIDDEN = "ضمير_مستتر"
    """Hidden pronoun (estimated)"""

    # Demonstratives
    ISM_DEMONSTRATIVE_NEAR = "اسم_إشارة_قريب"
    """Near demonstrative (هذا، هذه)"""

    ISM_DEMONSTRATIVE_FAR = "اسم_إشارة_بعيد"
    """Far demonstrative (ذلك، تلك)"""

    # Relatives
    ISM_RELATIVE = "اسم_موصول"
    """Relative pronoun (الذي، التي، مَن)"""

    # Interrogatives
    ISM_INTERROGATIVE = "اسم_استفهام"
    """Interrogative noun (مَن، ما، أين، متى)"""

    # Conditionals
    ISM_CONDITIONAL = "اسم_شرط"
    """Conditional noun (مَن، ما في الشرط)"""

    # Numerals
    ISM_NUMERAL_CARDINAL = "عدد_أصلي"
    """Cardinal number (واحد، اثنان، ثلاثة)"""

    ISM_NUMERAL_ORDINAL = "عدد_ترتيبي"
    """Ordinal number (أول، ثاني، ثالث)"""

    # Derived nouns
    ISM_DERIVED_ACTIVE_PARTICIPLE = "اسم_فاعل"
    """Active participle (كاتب، قارئ)"""

    ISM_DERIVED_PASSIVE_PARTICIPLE = "اسم_مفعول"
    """Passive participle (مكتوب، مقروء)"""

    ISM_DERIVED_EXAGGERATION = "صيغة_مبالغة"
    """Exaggeration form (فعّال، مفعال)"""

    ISM_DERIVED_ADJECTIVE = "صفة_مشبهة"
    """Resembling adjective (حسَن، كريم)"""

    ISM_DERIVED_COMPARATIVE = "اسم_تفضيل"
    """Comparative/superlative (أفضل، أكبر)"""

    ISM_DERIVED_INSTRUMENT = "اسم_آلة"
    """Instrument noun (مفتاح، منشار)"""

    ISM_DERIVED_TIME_PLACE = "اسم_زمان_مكان"
    """Time/place noun (مكتب، موعد)"""

    ISM_DERIVED_VERBAL_NOUN = "مصدر"
    """Verbal noun/masdar (كتابة، قراءة)"""

    # Special categories
    ISM_FIVE_NOUNS = "من_الأسماء_الخمسة"
    """One of five nouns (أب، أخ، حم، فو، ذو)"""

    ISM_DEFECTIVE = "اسم_منقوص"
    """Defective noun ending in ya (القاضي)"""

    ISM_SHORTENED = "اسم_مقصور"
    """Shortened noun ending in alif (الفتى)"""

    ISM_EXTENDED = "اسم_ممدود"
    """Extended noun with hamza (صحراء)"""

    ISM_INVARIANT_FORM = "اسم_مبني"
    """Invariant/built noun (not inflected)"""

    ISM_INFLECTABLE = "اسم_معرب"
    """Inflectable noun"""

    ISM_UNRESOLVED = "اسم_غير_محسوم"
    """Noun type unresolved (competition remains)"""


class VerbTypeID(Enum):
    """
    أكواد أنواع الأفعال (Verb Type Identifiers)

    Operational verb subtypes for operator matching.
    """
    # Tense/mood
    FIIL_MADI = "فعل_ماضٍ"
    """Past tense verb"""

    FIIL_MUDARI = "فعل_مضارع"
    """Present/future tense verb"""

    FIIL_AMR = "فعل_أمر"
    """Imperative verb"""

    # Valency types
    FIIL_LAZIM = "فعل_لازم"
    """Intransitive verb"""

    FIIL_MUTADI_ONE = "فعل_متعدٍّ_لمفعول_واحد"
    """Transitive to one object"""

    FIIL_MUTADI_TWO = "فعل_متعدٍّ_لمفعولين"
    """Transitive to two objects"""

    FIIL_MUTADI_THREE = "فعل_متعدٍّ_لثلاثة_مفاعيل"
    """Transitive to three objects"""

    # Voice
    FIIL_MABNI_MALUM = "فعل_مبني_للمعلوم"
    """Active voice"""

    FIIL_MABNI_MAJHUL = "فعل_مبني_للمجهول"
    """Passive voice"""

    # Soundness categories
    FIIL_SAHIH = "فعل_صحيح"
    """Sound verb (no weak letters)"""

    FIIL_MUTAL = "فعل_معتل"
    """Weak verb (contains و، ي، ا)"""

    FIIL_MITHAL = "فعل_مثال"
    """Assimilated verb (first radical weak)"""

    FIIL_AJWAF = "فعل_أجوف"
    """Hollow verb (middle radical weak)"""

    FIIL_NAQIS = "فعل_ناقص"
    """Defective verb (final radical weak)"""

    # Gemination
    FIIL_MUDAAF = "فعل_مضاعف"
    """Geminated verb (doubled consonant)"""

    # Hamza verbs
    FIIL_MAHMUZ = "فعل_مهموز"
    """Hamzated verb"""

    # Five verbs (الأفعال الخمسة)
    FIIL_FIVE_VERBS = "من_الأفعال_الخمسة"
    """One of five verb patterns (with و، ا، ي subject markers)"""

    FIIL_UNRESOLVED = "فعل_غير_محسوم"
    """Verb type unresolved"""


class ParticleTypeID(Enum):
    """
    أكواد أنواع الحروف (Particle Type Identifiers)

    Operational particle subtypes for operator matching.
    """
    # Prepositions
    HARF_JARR = "حرف_جر"
    """Preposition (من، إلى، في، على، عن، ...)"""

    # Nasb particles
    HARF_NASB = "حرف_نصب"
    """Nasb particle for verbs (أن، لن، كي، ...)"""

    # Jazm particles
    HARF_JAZM = "حرف_جزم"
    """Jazm particle for verbs (لم، لما، لام الأمر، لا الناهية، ...)"""

    # Interrogatives
    HARF_ISTIFHAM = "حرف_استفهام"
    """Interrogative particle (هل، أ)"""

    # Conjunction
    HARF_ATF = "حرف_عطف"
    """Conjunction (و، ف، ثم، أو، ...)"""

    # Negation
    HARF_NAFI = "حرف_نفي"
    """Negation particle (لا، ما، لم، ...)"""

    # Exception
    HARF_ISTITHNA = "حرف_استثناء"
    """Exception particle (إلا، غير، سوى، ...)"""

    # Emphasis
    HARF_TAWKID = "حرف_توكيد"
    """Emphasis particle (إن، أن، لكن، ...)"""

    # Vocative
    HARF_NIDA = "حرف_نداء"
    """Vocative particle (يا، أيا، هيا، ...)"""

    # Initiation
    HARF_IBTIDA = "حرف_ابتداء"
    """Sentence-initial particle (ألا، أما، ...)"""

    # Response
    HARF_JAWAB = "حرف_جواب"
    """Response particle (نعم، بلى، لا في الجواب، ...)"""

    # Comparison
    HARF_TASHBIH = "حرف_تشبيه"
    """Comparison particle (ك in كأن، كأنّ)"""

    # Future
    HARF_ISTIQBAL = "حرف_استقبال"
    """Future particle (س، سوف)"""

    # Explanation
    HARF_TAFSIR = "حرف_تفسير"
    """Explanation particle (أي، أنّ)"""

    # Causative operators (inna and sisters)
    HARF_NASIKH_INNA = "حرف_ناسخ_إن_وأخواتها"
    """Inna and sisters (إن، أن، كأن، لكن، ليت، لعل)"""

    # Exception from nasikh
    HARF_NASIKH_LA_NAFI_LILJINS = "لا_النافية_للجنس"
    """La negating the genus"""

    HARF_UNRESOLVED = "حرف_غير_محسوم"
    """Particle type unresolved"""


class CompositeTypeID(Enum):
    """
    أكواد التراكيب المركبة (Composite Type Identifiers)

    For multi-word constructs that behave as single units.
    """
    COMPOSITE_MUDAF_MUDAF_ILAYH = "مركب_إضافي"
    """Possessive construct (إضافة)"""

    COMPOSITE_NAAT_MANUT = "مركب_نعتي"
    """Adjectival construct"""

    COMPOSITE_BADAL = "مركب_بدلي"
    """Appositive construct"""

    COMPOSITE_TAWKID = "مركب_توكيدي"
    """Emphatic construct"""

    COMPOSITE_ATF = "مركب_عطفي"
    """Conjunctive construct"""

    COMPOSITE_PREPOSITIONAL_PHRASE = "شبه_جملة_جر_ومجرور"
    """Prepositional phrase"""

    COMPOSITE_ADVERBIAL_PHRASE = "شبه_جملة_ظرفية"
    """Adverbial phrase"""

    COMPOSITE_UNRESOLVED = "مركب_غير_محسوم"
    """Composite type unresolved"""
