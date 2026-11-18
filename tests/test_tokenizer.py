from ilis.language.tokenizer import tokenize


def test_tokenize_words_and_punctuation():
    assert tokenize("Aku makan nasi.") == ["Aku", "makan", "nasi", "."]


def test_tokenize_contractions_and_hyphenated_words():
    assert tokenize("anak-anak 'kan?") == ["anak", "-", "anak", "'", "kan", "?"]


def test_tokenize_empty_string():
    assert tokenize("") == []
