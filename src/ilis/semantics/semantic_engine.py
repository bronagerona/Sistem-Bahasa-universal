"""Deterministic Indonesian Semantic Engine with additive V2 patterns.

The contract wrapper and its twelve semantic fields remain version 1.0.
"""

from __future__ import annotations

import re
from typing import Any

from ilis.semantics.constants import CONTRACT_VERSION
from ilis.semantics.contract_validator import validate_input, validate_output

_PRONOUNS = {
    "saya": ("saya", "formal"), "aku": ("aku", "informal"),
    "gue": ("saya", "slang"), "gw": ("saya", "slang"),
    "gua": ("saya", "slang"), "kamu": ("kamu", "informal"),
    "lu": ("kamu", "slang"), "lo": ("kamu", "slang"),
    "dia": ("dia", "unknown"), "kita": ("kita", "unknown"),
    "kami": ("kami", "unknown"), "mereka": ("mereka", "unknown"),
}
_VERBS = {
    "makan", "minum", "pergi", "berangkat", "datang", "tidur", "baca",
    "membaca", "menulis", "belajar", "bekerja", "main", "bermain",
    "melihat", "menakuti", "takut", "membeli", "membawa", "memberi", "memasak", "lari",
    "beli", "pulang", "membakar", "bakar", "bunyi", "bunyikan",
    "menyalakan", "matikan", "tutup", "buka", "ambil", "berikan",
    "panggil", "dengarkan", "lihat", "buat", "simpan", "hapus", "jawab",
}
_COMPLEX_MARKERS = {
    "dan", "tetapi", "namun", "karena", "sehingga", "ketika", "meskipun",
    "walaupun", "sedangkan", "sementara",
}
_INTERROGATIVE_MARKERS = {
    "apakah", "siapa", "apa", "mengapa", "kenapa", "bagaimana",
    "kapan", "dimana", "di mana", "mana",
}
_COMMAND_MARKERS = {"tolong", "silakan", "harap", "mohon"}
_IMPERATIVE_VERBS = {"bunyikan", "menyalakan", "matikan", "tutup", "buka", "ambil", "berikan", "panggil", "dengarkan", "simpan", "hapus", "jawab"}
_TIME_WORDS = {
    "sekarang", "tadi", "kemarin", "besok", "lusa", "nanti",
    "pagi", "siang", "sore", "malam", "subuh", "dinihari",
    "kemarin", "minggu", "senin", "selasa", "rabu", "kamis",
    "jumat", "sabtu", "ahad", "hari", "pekan", "bulan", "tahun",
    "pagian", "barusan", "nantimalam",
}
_TIME_PHRASES = (
    "pagi hari", "siang hari", "sore hari", "malam hari",
    "tengah malam", "dini hari", "akhir pekan", "setiap pagi",
    "setiap malam", "minggu depan", "minggu lalu", "bulan depan",
    "tahun depan",
)
_LOCATION_PREPOSITIONS = {"di", "ke", "dari", "menuju", "dalam", "luar"}
_ASPECT_MARKERS = {
    "progressive": {"lagi", "sedang"},
    "prospective": {"akan", "bakal"},
    "completed": {"sudah", "telah"},
    "habitual": {"biasanya", "sering", "selalu", "tiap", "setiap"},
}
_NEGATIONS = {"tidak", "tak", "gak", "ga", "nggak", "enggak", "ndak", "bukan", "belum", "jangan", "enggak"}
_MODALITY_MARKERS = {
    "ability": {"bisa", "dapat", "mampu"},
    "obligation": {"harus", "wajib"},
    "possibility": {"mungkin", "barangkali"},
    "desire": {"ingin", "mau", "pengen"},
    "permission": {"boleh"},
}


class SemanticEngine:
    """Parse a bounded set of Indonesian sentence patterns without an LLM."""

    def analyze(self, payload: dict[str, Any]) -> dict[str, Any]:
        validated = validate_input(payload)
        original = validated["original_text"]
        normalized = validated["ilve"]["normalized_text"]
        semantics, status = self._parse(
            original, normalized, validated["ilve"]["variation_hints"]
        )
        result = {
            "contract_version": CONTRACT_VERSION,
            "status": status,
            "semantics": semantics,
            "original_text": original,
            "ilve": validated["ilve"],
        }
        validate_output(result)
        return result

    def _parse(
        self, original: str, normalized: str, variation_hints: list[dict[str, str]]
    ) -> tuple[dict[str, Any] | None, str]:
        words = re.findall(r"[a-zA-ZÀ-ÿ]+", normalized.casefold())
        original_words = re.findall(r"[a-zA-ZÀ-ÿ]+", original.casefold())
        if not words:
            return None, "unsupported"
        if any(word in _COMPLEX_MARKERS for word in words):
            return None, "unsupported"

        is_question = "?" in original or words[0] in _INTERROGATIVE_MARKERS
        is_command = words[0] in _COMMAND_MARKERS
        if is_question and words[0] in _INTERROGATIVE_MARKERS:
            words = words[1:]
        if is_command:
            words = words[1:]
        if not words:
            return None, "unsupported"

        verb_positions = [i for i, word in enumerate(words) if word in _VERBS]
        if len(verb_positions) > 1:
            return None, "unsupported"

        # Imperative: predicate is commonly the first lexical token.
        if not is_question and not is_command and words[0] in _IMPERATIVE_VERBS:
            is_command = True
        if is_command:
            predicate_index = next((i for i, w in enumerate(words) if w in _VERBS), None)
            if predicate_index is None:
                return self._partial_semantics(intent="command"), "low_confidence"
            actor_index = None
            actor = None
            inferred_register = "unknown"
        else:
            actor_index = next((i for i, w in enumerate(words) if w in _PRONOUNS), None)
            predicate_index = next(
                (i for i, w in enumerate(words) if w in _VERBS and
                 (actor_index is None or i > actor_index)), None
            )
            if predicate_index is None:
                partial_predicate = words[verb_positions[0]] if verb_positions else None
                return self._partial_semantics(predicate=partial_predicate), "low_confidence"
            if actor_index is None:
                # A simple nominal subject before the predicate is accepted for
                # the bounded question pattern (e.g. "Apakah api bisa membakar kayu?").
                candidates = words[:predicate_index]
                candidates = [w for w in candidates if w not in _NEGATIONS and
                              not any(w in markers for markers in _MODALITY_MARKERS.values())]
                if not candidates:
                    return self._partial_semantics(predicate=words[predicate_index],
                                                   intent="question" if is_question else "assertion"), "low_confidence"
                actor = candidates[-1]
                inferred_register = "unknown"
                actor_word = actor
            else:
                actor_word = words[actor_index]
                actor, inferred_register = _PRONOUNS[actor_word]

        predicate = words[predicate_index]
        before_predicate = words[:predicate_index] if actor_index is None else words[actor_index + 1:predicate_index]
        after_predicate = words[predicate_index + 1:]
        aspect = "unspecified"
        for aspect_name, markers in _ASPECT_MARKERS.items():
            if any(word in markers for word in before_predicate):
                aspect = aspect_name
                break

        negation = "none"
        if "belum" in before_predicate:
            negation = "not_yet"
        elif "bukan" in before_predicate:
            negation = "identity_negative"
        elif any(word in _NEGATIONS or word == "jangan" for word in before_predicate):
            negation = "negative"

        modality = "none"
        for modality_name, markers in _MODALITY_MARKERS.items():
            if any(word in markers for word in before_predicate):
                modality = modality_name
                break

        time = None
        padded = " " + " ".join(words) + " "
        for phrase in _TIME_PHRASES:
            if " " + phrase + " " in padded:
                time = phrase
                break
        if time is None:
            if re.search(r"\bpagi[-\s]+pagian\b", original.casefold()):
                time = "pagi-pagian"
            else:
                time = next((w for w in words if w in _TIME_WORDS), None)

        location = None
        patient = None
        for i, word in enumerate(after_predicate):
            if word in _LOCATION_PREPOSITIONS and i + 1 < len(after_predicate):
                stop = next((j for j in range(i + 1, len(after_predicate))
                             if after_predicate[j] in _TIME_WORDS or
                             after_predicate[j] in _LOCATION_PREPOSITIONS or
                             after_predicate[j] in {"setiap", "tiap"}), len(after_predicate))
                location = " ".join(after_predicate[i + 1:stop]) or None
                break
        if location is None:
            patient_words = []
            for word in after_predicate:
                if word in _TIME_WORDS or word in _LOCATION_PREPOSITIONS:
                    break
                patient_words.append(word)
            patient = " ".join(patient_words) or None

        hint_surfaces = {hint["surface"].casefold() for hint in variation_hints}
        if any(w in {"gue", "gw", "gua", "lu", "lo"} for w in original_words) or hint_surfaces.intersection({"gue", "gw", "gua", "lu", "lo"}):
            register = "slang"
        elif inferred_register == "formal":
            register = "formal"
        elif inferred_register == "informal":
            register = "informal"
        else:
            register = inferred_register

        intent = "question" if is_question else ("command" if is_command else "assertion")
        confidence = 0.98 if predicate in {"makan", "pergi"} else 0.90
        semantics = {
            "Actor": actor, "Predicate": predicate, "Patient/Object": patient,
            "Recipient": None, "Location": location, "Time": time,
            "Aspect": aspect, "Negation": negation, "Modality": modality,
            "Intent": intent, "Register": register, "Confidence": confidence,
        }
        return semantics, "supported"

    @staticmethod
    def _partial_semantics(
        actor: str | None = None, predicate: str | None = None,
        register: str = "unknown", intent: str = "assertion",
    ) -> dict[str, Any]:
        return {
            "Actor": actor, "Predicate": predicate, "Patient/Object": None,
            "Recipient": None, "Location": None, "Time": None,
            "Aspect": "unspecified", "Negation": "none", "Modality": "none",
            "Intent": intent, "Register": register, "Confidence": 0.25,
        }
