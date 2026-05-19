from dal_core import (
    LexicalType,
    Rank,
    SEED_LEXICON,
    analyze_dal_mufrad,
    atoms_from_text,
    attach_marks,
)


def test_unicode_is_not_letter():
    atoms = atoms_from_text("َ")
    assert atoms[0].kind.value == "short_vowel"
    assert atoms[0].kind.value != "letter"


def test_mark_without_base_is_blocker():
    atoms = atoms_from_text("َ")
    units = attach_marks(atoms)
    assert units
    assert any(r.code == "mark_without_base" for r in units[0].residuals)


def test_unvocalized_word_keeps_residual():
    result = analyze_dal_mufrad("كتب", SEED_LEXICON)
    codes = {r.code for r in result.residuals}
    assert "missing_visible_haraka" in codes
    assert "type_not_closed" in codes
    assert result.closed is False


def test_attested_word_closes_lugha():
    result = analyze_dal_mufrad("كَتَبَ", SEED_LEXICON)
    assert result.closed is True
    assert result.rank == Rank.AHAD
    assert result.d_type.lexical_type == LexicalType.VERB


def test_unknown_type_blocks_mufrad_certificate():
    result = analyze_dal_mufrad("غير", {})
    codes = {r.code for r in result.residuals}
    assert "mufrad_requires_closed_type" in codes
    assert result.closed is False


def test_no_semantic_field_in_dal_pipeline():
    result = analyze_dal_mufrad("كَتَبَ", SEED_LEXICON)
    payload = result.explain()
    assert "meaning" not in payload
    assert "semantic" not in payload
    assert "meaning" not in payload["trace"]
    assert "semantic" not in payload["trace"]
    assert "meaning" not in payload["trace"]["mufrad"]
    assert "semantic" not in payload["trace"]["mufrad"]
