"""Session context orchestration for ILIS language and cognition engines."""

from __future__ import annotations

from typing import Any

from ilis.cognition.knowledge_engine import KnowledgeEngine
from ilis.cognition.memory_store import MemoryStore
from ilis.cognition.reasoning_engine import ReasoningEngine
from ilis.language.pipeline import analyze_semantics


class ContextEngine:
    """Track speakers, conversation turns, episodes, and long-term knowledge.

    The engine coordinates existing ILIS components without changing their
    contracts. It uses deterministic Semantic, Knowledge, and Reasoning
    interfaces; no LLM or model AI is involved.
    """

    def __init__(
        self,
        knowledge_engine: KnowledgeEngine,
        memory_store: MemoryStore | None = None,
    ) -> None:
        if not isinstance(knowledge_engine, KnowledgeEngine):
            raise TypeError("knowledge_engine must be a KnowledgeEngine instance")
        if memory_store is not None and not isinstance(memory_store, MemoryStore):
            raise TypeError("memory_store must be a MemoryStore instance")
        self.knowledge_engine = knowledge_engine
        self.memory_store = memory_store or MemoryStore()

    def create_session(self, metadata: dict[str, Any] | None = None) -> str:
        """Create a unique session and return its session_id."""
        return self.memory_store.create_session(metadata)["session_id"]

    def close_session(
        self, session_id: str, *, clear_working: bool = True
    ) -> dict[str, Any]:
        """Close a session; working memory is cleared by default."""
        return self.memory_store.close_session(
            session_id, clear_working=clear_working
        )

    def add_message(
        self,
        session_id: str,
        speaker: str,
        text: str,
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Append a conversation turn and track its speaker."""
        return self.memory_store.add_message(
            session_id, speaker, text, metadata
        )

    def process_message(
        self,
        session_id: str,
        speaker: str,
        text: str,
        *,
        ingest_semantics: bool = False,
        source: str = "context_engine",
    ) -> dict[str, Any]:
        """Store a turn, run Semantic Engine, and optionally add its claim.

        Semantic analysis is performed by the existing pipeline adapter.
        Knowledge ingestion remains opt-in because parsed language is stored
        only as a hypothesis by KnowledgeEngine.
        """
        message = self.add_message(session_id, speaker, text)
        semantic_result = analyze_semantics(text)
        ingestion = None
        if ingest_semantics:
            ingestion = self.knowledge_engine.ingest_semantic_result(
                semantic_result, source=source
            )
        return {
            "message": message,
            "semantic_result": semantic_result,
            "knowledge_ingestion": ingestion,
        }

    def record_event(
        self,
        session_id: str,
        description: str,
        *,
        event_type: str = "event",
        entities: list[str] | None = None,
        attributes: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Record an event in Episodic Memory."""
        return self.memory_store.add_episode(
            session_id,
            description,
            event_type=event_type,
            entities=entities,
            attributes=attributes,
        )

    def get_context(self, session_id: str) -> dict[str, Any]:
        """Return a session snapshot plus a read-only view of long-term facts."""
        session = self.memory_store.get_session(session_id)
        if session is None:
            raise KeyError(f"unknown session_id: {session_id}")

        messages = self.memory_store.get_working_memory(session_id)
        episodes = self.memory_store.get_episodic_memory(session_id)
        participants = list(dict.fromkeys(
            message["speaker"] for message in messages
        ))
        facts = self.knowledge_engine.fact_store.all()
        fact_context = [
            {
                **fact,
                "provenance": self.knowledge_engine.get_provenance(fact["id"]),
            }
            for fact in facts
        ]
        return {
            "session_id": session_id,
            "session": session,
            "participants": participants,
            "conversation_history": messages,
            "episodic_memory": episodes,
            "long_term_memory": {
                "concepts": self.knowledge_engine.concept_store.all(),
                "relations": self.knowledge_engine.relation_store.all(),
                "facts": fact_context,
            },
        }

    def reason_from_context(
        self,
        session_id: str,
        source: str,
        target: str,
        reasoning_engine: ReasoningEngine | None = None,
    ) -> dict[str, Any]:
        """Pass session context to the existing Reasoning Engine and return both.

        The reasoner still evaluates Knowledge Engine facts; episodic context is
        included alongside its result so callers can inspect the triggering
        event. V1 does not silently convert an event description into a fact.
        """
        context = self.get_context(session_id)
        reasoner = reasoning_engine or ReasoningEngine(self.knowledge_engine)
        if not isinstance(reasoner, ReasoningEngine):
            raise TypeError("reasoning_engine must be a ReasoningEngine instance")
        if reasoner.knowledge_engine is not self.knowledge_engine:
            raise ValueError("reasoning_engine must use this ContextEngine's KnowledgeEngine")
        inference = reasoner.infer_burn_risk(source, target)
        return {
            "session_id": session_id,
            "context": context,
            "inference": inference,
        }
