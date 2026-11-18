"""Rule-based, explainable Semantic Engine for simple Indonesian assertions.

No LLM, embedding model, or external AI service is used. This V1 parser deliberately
supports a small, explicit set of sentence patterns and declines complex input.
"""

from __future__ import annotations

import re
from typing import Any

from ilis.semantics.constants import CONTRACT_VERSION
from ilis.semantics.contract_validator import (
    ContractValidationError,
    validate_input,
    validate_output,
)


_PRONOUNS = {
    "saya": ("saya", "formal"),
    "aku": ("aku", "informal"),
    "gue": ("saya", "slang"),
    "gw": ("saya", "slang"),
    "gua": ("saya", "slang"),
    "kamu": ("kamu", "informal"),
    "lu": ("kamu", "slang"),
    "lo": ("kamu", "slang"),
}
_VERBS = {
    "makan", "minum", "pergi", "berangkat", "datang", "tidur", "baca",
    "membaca", "menulis", "belajar", "bekerja", "main", "bermain",
    "melihat", "membeli", "membawa", "memberi", "memasak", "lari",
}
_COMPLEX_MARKERS = {
    "dan", "tetapi", "namun", "karena", "sehingga", "ketika", "meskipun",
    "walaupun", "sedangkan", "sementara",
}
_TIME_WORDS = {
    "sekarang", "tadi", "kemarin", "besok", "nanti", "pagi", "siang",
    "sore", "malam", "hari",
}
_LOCATION_PREPOSITIONS = {"di", "ke", "dari", "menuju"}


class SemanticEngine:
    """Parse simple Indonesian declarative sentences using deterministic rules."""

    def analyze(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Validate an ILVE input and return a contract-1.0 semantic result.

        The original text and validated ILVE payload are retained in the result
        for traceability. They are not replaced by normalized text.
        """
        validated = validate_input(payload)
        original = validated["original_text"]
        normalized = validated["ilve"]["normalized_text"]
        semantics, status = self._parse(original, normalized, validated["ilve"]["variation_hints"])
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
        # A second known predicate is a conservative signal of multiple clauses.
        verb_positions = [i for i, word in enumerate(words) if word in _VERBS]
        if len(verb_positions) > 1:
            return None, "unsupported"

        if len(words) < 2:
            return None, "unsupported"

        actor_index = next((i for i, word in enumerate(words) if word in _PRONOUNS), None)
        if actor_index is None:
            # Do not invent an omitted subject. Return a complete, explicitly partial
            # structure so downstream consumers can distinguish uncertainty.
            predicate = words[verb_positions[0]] if verb_positions else None
            return self._partial_semantics(predicate=predicate), "low_confidence"

        actor_word = words[actor_index]
        actor, inferred_register = _PRONOUNS[actor_word]
        predicate_index = next(
            (i for i, word in enumerate(words) if word in _VERBS and i > actor_index),
            None,
        )
        if predicate_index is None:
            partial = self._partial_semantics(actor=actor, register=inferred_register)
            return partial, "low_confidence"
        predicate = words[predicate_index]

        before_predicate = words[actor_index + 1:predicate_index]
        after_predicate = words[predicate_index + 1:]
        aspect = "unspecified"
        negation = "none"
        modality = "none"

        if any(word in {"lagi", "sedang"} for word in before_predicate):
            aspect = "progressive"
        elif any(word in {"akan", "bakal"} for word in before_predicate):
            aspect = "prospective"
        elif any(word in {"sudah", "telah"} for word in before_predicate):
            aspect = "completed"
        elif any(word in {"biasanya", "sering", "selalu"} for word in before_predicate):
            aspect = "habitual"

        if "belum" in before_predicate:
            negation = "not_yet"
        elif any(word in {"tidak", "tak", "gak", "ga", "nggak", "enggak"} for word in before_predicate):
            negation = "negative"
        elif "bukan" in before_predicate:
            negation = "identity_negative"

        if any(word in {"bisa", "dapat", "mampu"} for word in before_predicate):
            modality = "ability"
        elif any(word in {"harus", "wajib"} for word in before_predicate):
            modality = "obligation"
        elif any(word in {"mungkin", "barangkali"} for word in before_predicate):
            modality = "possibility"
        elif any(word in {"ingin", "mau", "pengen"} for word in before_predicate):
            modality = "desire"
        elif "boleh" in before_predicate:
            modality = "permission"

        location = None
        time = next((word for word in words if word in _TIME_WORDS), None)
        patient = None
        if after_predicate:
            for i, word in enumerate(after_predicate):
                if word in _LOCATION_PREPOSITIONS and i + 1 < len(after_predicate):
                    location = after_predicate[i + 1]
                    break
            if location is None:
                candidate = next(
                    (word for word in after_predicate if word not in _TIME_WORDS),
                    None,
                )
                patient = candidate

        # ILVE hints preserve surface/register evidence even when normalized_text
        # contains only canonical lexical forms.
        hint_surfaces = {hint["surface"].casefold() for hint in variation_hints}
        if any(word in {"gue", "gw", "gua", "lu", "lo"} for word in original_words) or hint_surfaces.intersection({"gue", "gw", "gua", "lu", "lo"}):
            register = "slang"
        elif actor_word == "aku":
            register = "informal"
        elif actor_word == "saya":
            register = "formal"
        else:
            register = inferred_register

        # A simple assertion with a recognized actor and predicate is high confidence.
        confidence = 0.98 if predicate in {"makan", "pergi"} else 0.93
        semantics = {
            "Actor": actor,
            "Predicate": predicate,
            "Patient/Object": patient,
            "Recipient": None,
            "Location": location,
            "Time": time,
            "Aspect": aspect,
            "Negation": negation,
            "Modality": modality,
            "Intent": "assertion",
            "Register": register,
            "Confidence": confidence,
        }
        return semantics, "supported"

    @staticmethod
    def _partial_semantics(
        actor: str | None = None,
        predicate: str | None = None,
        register: str = "unknown",
    ) -> dict[str, Any]:
        """Build a contract-complete partial result without guessing missing roles."""
        return {
            "Actor": actor,
            "Predicate": predicate,
            "Patient/Object": None,
            "Recipient": None,
            "Location": None,
            "Time": None,
            "Aspect": "unspecified",
            "Negation": "none",
            "Modality": "none",
            "Intent": "assertion",
            "Register": register,
            "Confidence": 0.25,
        }
