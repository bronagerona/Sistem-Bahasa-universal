from ilis.language.variation import variation_hint


def test_common_colloquial_variants():
    assert variation_hint("gue") == "saya"
    assert variation_hint("GAK") == "tidak"
    assert variation_hint("udh") == "sudah"


def test_unknown_word_has_no_guess():
    assert variation_hint("xylophone") is None


def test_surface_forms_are_not_overwritten():
    original = "Gue"
    assert variation_hint(original) == "saya"
    assert original == "Gue"
