"""Experimental six-label Indonesian negation interpreter for BL-ILIS-002.

Intentionally isolated: this module is not wired into production runtime.
Source JSONL annotations are read-only inputs and are never written here.
"""
from __future__ import annotations
import re
from typing import Any

LABELS = frozenset({"none", "negative", "not_yet", "identity_negative", "prohibitive", "ambiguous"})
_WORD_RE = re.compile(r"[a-zA-ZÀ-ÿ]+", re.UNICODE)
_QUOTED_RE = re.compile(r"“[^”]*”|‘[^’]*’|\"[^\"]*\"|'[^']*'")
_CUE_RE = re.compile(r"\b(?:tidak|tak|enggak|nggak|gak|ga|ndak|bukan|belum|janganlah?|dilarang|tanpa)\b", re.IGNORECASE)
_NEGATIVE_WORDS = {"tidak", "tak", "enggak", "nggak", "gak", "ga", "ndak"}
_IDENTITY_NOUNS = {"orang","anak","kakak","adik","ayah","ibu","suami","istri","teman","guru","dokter","ketua","anggota","bagian","alasan","rumah","kendaraan","mobil","motor","laptop","komputer","aplikasi","dokumen","berkas","penelepon","pelaku","pemilik"}
_EPISTEMIC_BELUM = {"tentu", "pasti", "jelas"}

def _tokens(text: str) -> list[str]:
    return [m.group(0).casefold() for m in _WORD_RE.finditer(text)]

def _functional_text(text: str) -> tuple[str, list[str]]:
    quoted = _QUOTED_RE.findall(text)
    outside = _QUOTED_RE.sub(" ", text)
    quoted_cues = [m.group(0).casefold() for q in quoted for m in _CUE_RE.finditer(q)]
    return outside, quoted_cues

def map_negation(utterance: str, source_boolean: bool | None, context: list[str] | tuple[str, ...] | None = None) -> dict[str, Any]:
    """Return a six-label mapping plus a diagnostic trace; context is prior turns oldest first."""
    if not isinstance(utterance, str) or not utterance.strip():
        raise ValueError("utterance must be a non-empty string")
    if source_boolean is not None and type(source_boolean) is not bool:
        raise TypeError("source_boolean must be bool or None")
    if context is not None and not isinstance(context, (list, tuple)):
        raise TypeError("context must be a list/tuple of prior utterances")
    functional, quoted_cues = _functional_text(utterance)
    words = _tokens(functional)
    cues = [m.group(0).casefold() for m in _CUE_RE.finditer(functional)]
    prior_words = _tokens(" ".join(str(x) for x in (context or [])))
    label, confidence, scope = "none", 0.96, None
    if not cues:
        if source_boolean is True:
            label, confidence = "ambiguous", 0.30
            reason = "Boolean sumber true tetapi tidak ditemukan cue negasi fungsional."
        elif quoted_cues:
            reason = "Cue hanya disebut di dalam kutipan; bukan negasi fungsional."
        else:
            reason = "Tidak ditemukan cue negasi fungsional."
    else:
        scope = functional.strip()
        markers = [w for w in words if w in _NEGATIVE_WORDS or w in {"bukan","belum","jangan","janganlah","dilarang","tanpa"}]
        if len(markers) >= 2:
            if words[:2] == ["belum", "pernah"]:
                label, confidence, reason = "not_yet", 0.82, "Belum pernah menyatakan pengalaman yang belum terjadi sampai waktu acuan."
            elif words[:2] in (["tidak","pernah"], ["tak","pernah"]):
                label, confidence, reason = "negative", 0.86, "Tidak pernah menyangkal pengalaman/kebiasaan secara umum."
            elif words[:2] in (["tidak","boleh"], ["tak","boleh"]):
                label, confidence, reason = "prohibitive", 0.92, "Tidak boleh berfungsi sebagai larangan."
            else:
                label, confidence, reason = "ambiguous", 0.30, "Beberapa penanda negasi berinteraksi; scope belum tervalidasi."
        elif any(w in words for w in {"jangan","janganlah","dilarang"}):
            label, confidence, reason = "prohibitive", 0.94, "Konstruksi mengarahkan pelaku untuk tidak melakukan tindakan."
        elif ("tidak" in words or "tak" in words) and "boleh" in words:
            label, confidence, reason = "prohibitive", 0.92, "Tidak boleh menyatakan larangan normatif."
        elif "belum" in words:
            idx = words.index("belum")
            nxt = words[idx + 1] if idx + 1 < len(words) else None
            if nxt in _EPISTEMIC_BELUM:
                label, confidence, reason = "ambiguous", 0.42, "Belum tentu/pasti bersifat epistemik, bukan otomatis negasi temporal."
            elif nxt is not None or (prior_words and any(w in prior_words for w in {"sudah","telah","pernah","kirim","datang","selesai","makan"})):
                label, confidence, reason = "not_yet", 0.86, "Belum menandai peristiwa/keadaan yang belum terjadi atau tercapai."
            else:
                label, confidence, reason = "ambiguous", 0.40, "Jawaban belum eliptis tanpa konteks yang cukup."
        elif "bukan" in words:
            idx = words.index("bukan")
            following = words[idx + 1:]
            if following and following[0] in _IDENTITY_NOUNS:
                label, confidence, reason = "identity_negative", 0.90, "Bukan menyangkal identitas, kategori, atau relasi nominal."
            else:
                label, confidence, reason = "negative", 0.80, "Bukan menyangkal proposisi/unsur non-identitas."
        elif "tanpa" in words:
            label, confidence, reason = "negative", 0.86, "Tanpa meniadakan unsur atau keadaan dalam proposisi."
        elif any(w in words for w in _NEGATIVE_WORDS):
            if words[:2] in (["tidak","apa"], ["tak","apa"]):
                label, confidence, reason = "ambiguous", 0.45, "Ungkapan idiomatis tidak apa-apa memerlukan interpretasi pragmatis."
            elif "hanya" in words and "tetapi" in words:
                label, confidence, reason = "ambiguous", 0.40, "Konstruksi tidak hanya... tetapi juga memiliki scope khusus."
            else:
                label, confidence, reason = "negative", 0.88, "Penanda menyangkal proposisi atau keadaan biasa."
        else:
            label, confidence, reason = "ambiguous", 0.35, "Cue terdeteksi tetapi fungsi/konstruksinya belum tercakup."
    discrepancy = source_boolean is None or (source_boolean is False and label != "none") or (source_boolean is True and label == "none")
    if label == "ambiguous":
        confidence = min(confidence, 0.49)
    return {"source_boolean": source_boolean, "detected_cues": cues if cues else quoted_cues, "scope": scope, "mapping_label": label, "mapping_reason": reason, "confidence": round(confidence,3), "annotation_discrepancy": discrepancy}

def legacy_mapping(source_boolean: bool, utterance: str) -> str:
    """Reproduce the coarse PR #20 experiment-harness baseline."""
    if source_boolean is False:
        return "none"
    words = _tokens(utterance)
    if "belum" in words:
        return "not_yet"
    if "bukan" in words:
        return "identity_negative"
    if any(w in words for w in _NEGATIVE_WORDS | {"jangan","tanpa"}):
        return "negative"
    return "negative"
