"""Rule-based Learning Engine V1; no LLM or model AI is used."""

from __future__ import annotations

import re
from typing import Any

from ilis.cognition.context_engine import ContextEngine
from ilis.cognition.knowledge_engine import KnowledgeEngine
from ilis.learning.hypothesis_tracker import HypothesisTracker


class LearningEngine:
    """Convert supported context inputs into hypotheses and flag disagreements.

    The engine never promotes a fact automatically. Confirmation is a separate,
    explicit operation and conflicting candidates remain pending review.
    """

    def __init__(
        self,
        knowledge_engine: KnowledgeEngine,
        context_engine: ContextEngine | None = None,
        hypothesis_tracker: HypothesisTracker | None = None,
    ) -> None:
        if not isinstance(knowledge_engine, KnowledgeEngine):
            raise TypeError("knowledge_engine must be a KnowledgeEngine instance")
        if context_engine is not None and not isinstance(context_engine, ContextEngine):
            raise TypeError("context_engine must be a ContextEngine instance")
        if context_engine is not None and context_engine.knowledge_engine is not knowledge_engine:
            raise ValueError("context_engine must use the same KnowledgeEngine instance")
        if hypothesis_tracker is not None and not isinstance(hypothesis_tracker, HypothesisTracker):
            raise TypeError("hypothesis_tracker must be a HypothesisTracker instance")
        self.knowledge_engine = knowledge_engine
        self.context_engine = context_engine
        self.hypothesis_tracker = hypothesis_tracker or HypothesisTracker()

    def learn_from_semantics(
        self, semantic_result: dict[str, Any], *, source: str = "semantic_engine"
    ) -> dict[str, Any]:
        """Accept a Context/Semantic result and store a representable assertion."""
        if not isinstance(semantic_result, dict) or semantic_result.get("status") != "supported":
            return self._report(
                candidate={}, fact=None, origin="semantic", source_ref=None,
                reason="semantic_result_not_supported",
            )
        semantics = semantic_result.get("semantics")
        if not isinstance(semantics, dict):
            return self._report(
                candidate={}, fact=None, origin="semantic", source_ref=None,
                reason="missing_semantics",
            )
        if semantics.get("Intent") != "assertion" or semantics.get("Negation", "none") != "none" or semantics.get("Modality", "none") != "none":
            return self._report(
                candidate={}, fact=None, origin="semantic", source_ref=None,
                reason="assertion_negated_or_modal_not_representable",
            )
        subject = semantics.get("Actor")
        relation = semantics.get("Predicate")
        object_ = semantics.get("Patient/Object")
        if not all(isinstance(value, str) and value.strip() for value in (subject, relation, object_)):
            return self._report(
                candidate={}, fact=None, origin="semantic", source_ref=None,
                reason="incomplete_subject_relation_object",
            )
        return self._learn_candidate(
            {"subject": subject, "relation": relation, "object": object_},
            origin="semantic", source=source, source_ref=None,
        )

    def learn_from_context_message(
        self,
        session_id: str,
        speaker: str,
        text: str,
        *,
        source: str = "context_semantic",
    ) -> dict[str, Any]:
        """Store a user turn through ContextEngine, then learn its semantic result.

        A narrow deterministic fallback handles explicit 'X tidak bisa dibakar'
        statements because Semantic Engine V1 does not yet parse that sentence
        pattern. It does not attempt open-ended language understanding.
        """
        context = self._require_context()
        processed = context.process_message(session_id, speaker, text)
        semantic_result = processed["semantic_result"]
        result = self.learn_from_semantics(semantic_result, source=source)
        if result["reason"] != "semantic_result_not_supported" and result["reason"] != "incomplete_subject_relation_object":
            result["context_message"] = processed["message"]
            result["semantic_result"] = semantic_result
            return result

        candidate = self._parse_burnability_statement(text)
        if candidate is None:
            result["context_message"] = processed["message"]
            result["semantic_result"] = semantic_result
            return result
        learned = self._learn_candidate(
            candidate, origin="context_rule_fallback", source=source,
            source_ref=processed["message"]["message_id"],
        )
        learned["context_message"] = processed["message"]
        learned["semantic_result"] = semantic_result
        return learned

    def learn_from_episode(
        self, session_id: str, episode_id: str, *, source: str = "episodic_memory"
    ) -> dict[str, Any]:
        """Learn a hypothesis from one ContextEngine episodic record.

        Explicit subject/relation/object attributes are preferred. Otherwise the
        recorded event is represented as an experience hypothesis, not as a
        verified real-world fact.
        """
        context = self._require_context()
        snapshot = context.get_context(session_id)
        episode = next(
            (item for item in snapshot["episodic_memory"] if item["episode_id"] == episode_id),
            None,
        )
        if episode is None:
            raise KeyError(f"unknown episode_id: {episode_id}")
        attributes = episode.get("attributes", {})
        if all(isinstance(attributes.get(key), str) and attributes[key].strip()
               for key in ("subject", "relation", "object")):
            candidate = {
                "subject": attributes["subject"],
                "relation": attributes["relation"],
                "object": attributes["object"],
            }
        else:
            entities = episode.get("entities", [])
            candidate = {
                "subject": entities[0] if entities else "session_event",
                "relation": f"experienced_event_{episode['event_type']}",
                "object": episode["description"],
            }
        return self._learn_candidate(
            candidate, origin="episodic", source=source, source_ref=episode_id,
        )

    def confirm_hypothesis(
        self, hypothesis_id: str, *, confirmed_by: str
    ) -> dict[str, Any]:
        """Explicitly promote a non-conflicting hypothesis to verified."""
        if not isinstance(confirmed_by, str) or not confirmed_by.strip():
            raise ValueError("confirmed_by must be a non-empty explicit confirmer")
        item = self.hypothesis_tracker.get(hypothesis_id)
        if item is None:
            raise KeyError(f"unknown hypothesis_id: {hypothesis_id}")
        if item["conflict"] or item["status"] == "conflicting":
            raise ValueError("conflicting hypotheses require conflict review before verification")
        fact_id = item["fact_id"]
        if fact_id is None:
            raise ValueError("hypothesis has no KnowledgeEngine fact to verify")
        fact = self.knowledge_engine.fact_store.get(fact_id)
        if fact is None:
            raise KeyError(f"unknown fact_id: {fact_id}")
        if fact["status"] == "conflicting":
            raise ValueError("conflicting KnowledgeEngine facts cannot be verified")
        self.knowledge_engine.fact_store.update_status(fact_id, "verified")
        self.knowledge_engine.provenance.update_status(fact_id, "verified")
        return self.hypothesis_tracker.update_review(
            hypothesis_id, status="verified", knowledge_status="verified"
        ) | {"confirmed_by": confirmed_by.strip(), "fact": self.knowledge_engine.fact_store.get(fact_id)}

    def get_hypotheses(self) -> list[dict[str, Any]]:
        return self.hypothesis_tracker.all()

    def _learn_candidate(
        self,
        candidate: dict[str, str],
        *,
        origin: str,
        source: str,
        source_ref: str | None,
    ) -> dict[str, Any]:
        subject = candidate["subject"]
        relation = candidate["relation"]
        object_ = candidate["object"]
        normalized = (
            " ".join(subject.casefold().split()),
            " ".join(relation.casefold().split()),
            " ".join(object_.casefold().split()),
        )
        matching = [
            fact for fact in self.knowledge_engine.fact_store.all()
            if fact["subject"] == normalized[0] and fact["relation"] == normalized[1]
        ]
        conflict = any(fact["object"] != normalized[2] for fact in matching)
        # KnowledgeEngine owns conflict/provenance semantics. Its add_fact method
        # flags every conflicting member and updates provenance consistently.
        fact = self.knowledge_engine.add_fact(
            subject, relation, object_, status="hypothesis", source=source
        )
        if conflict or fact["status"] == "conflicting":
            status = "conflicting"
            reason = "conflict_detected_confirmation_required"
        else:
            status = "hipotesis_baru"
            reason = "stored_as_hypothesis_not_verified"
        tracker_item = self.hypothesis_tracker.track(
            origin=origin, candidate=candidate, fact=fact, status=status,
            conflict=conflict or fact["status"] == "conflicting",
            requires_confirmation=status == "conflicting",
            source_ref=source_ref, reason=reason,
        )
        return {
            "laporan": status,
            "hipotesis_baru": tracker_item,
            "konflik_ditemukan": tracker_item["conflict"],
            "aman": not tracker_item["conflict"],
            "fact": fact,
            "reason": reason,
        }

    def _report(
        self, *, candidate: dict[str, str], fact: dict[str, Any] | None,
        origin: str, source_ref: str | None, reason: str,
    ) -> dict[str, Any]:
        item = self.hypothesis_tracker.track(
            origin=origin, candidate=candidate, fact=fact,
            status="not_learned", conflict=False, requires_confirmation=False,
            source_ref=source_ref, reason=reason,
        )
        return {
            "laporan": "tidak_dipelajari",
            "hipotesis_baru": item,
            "konflik_ditemukan": False,
            "aman": False,
            "fact": None,
            "reason": reason,
        }

    def _require_context(self) -> ContextEngine:
        if self.context_engine is None:
            raise ValueError("ContextEngine is required for context input")
        return self.context_engine

    @staticmethod
    def _parse_burnability_statement(text: str) -> dict[str, str] | None:
        match = re.fullmatch(
            r"\s*(?P<subject>[\w-]+)\s+(?P<negation>tidak|tak|nggak|enggak|gak|ga)?\s*"
            r"(?:(?:bisa|dapat|mampu)\s+)?dibakar\s*[.!?]?\s*",
            text, flags=re.IGNORECASE,
        )
        if not match:
            return None
        negative = bool(match.group("negation"))
        return {
            "subject": match.group("subject").casefold(),
            "relation": "can_burn",
            "object": "false" if negative else "true",
        }
