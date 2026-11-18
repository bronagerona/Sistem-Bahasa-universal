from ilis.language.pipeline import inspect_text


def test_pipeline_preserves_surface_and_adds_hints():
    result = inspect_text("Gue nggak mau cabut, bro!")
    surfaces = [item["surface"] for item in result["tokens"]]
    hints = [item["variation_hint"] for item in result["tokens"]]

    assert surfaces == ["Gue", "nggak", "mau", "cabut", ",", "bro", "!"]
    assert hints[0] == "saya"
    assert hints[1] == "tidak"
    assert hints[3] == "pergi"
    assert result["input"] == "Gue nggak mau cabut, bro!"


def test_pipeline_discloses_current_limitations():
    result = inspect_text("Halo")
    assert result["limitations"]
