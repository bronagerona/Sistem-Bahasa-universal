"""Single entry point wiring the deterministic ILIS engines."""

from __future__ import annotations

from typing import Any

from ilis.cognition.context_engine import ContextEngine
from ilis.cognition.knowledge_engine import KnowledgeEngine
from ilis.cognition.reasoning_engine import ReasoningEngine
from ilis.generation.language_generator import LanguageGenerator
from ilis.learning.learning_engine import LearningEngine
from ilis.semantics.semantic_engine import SemanticEngine
from ilis.language.pipeline import analyze_semantics


class ILISCore:
    """Initialize and expose the complete ILIS engine stack.

    Conversation transcript is owned by adapters. Core accepts an optional
    immutable context snapshot per call but never stores conversation state.
    Default storage='memory' preserves V1 behavior. Use storage='sqlite' to
    persist knowledge and episodic memory across process restarts.
    """

    def __init__(
        self, *, seed_core_knowledge: bool = True,
        storage: str = "memory", db_path: str = "./ilis_v2.db",
    ) -> None:
        if storage not in {"memory", "sqlite"}:
            raise ValueError("storage must be 'memory' or 'sqlite'")
        self.storage_provider = None
        if storage == "sqlite":
            from ilis.storage import SQLiteStorageProvider
            self.storage_provider = SQLiteStorageProvider(db_path)

        self.semantic_engine = SemanticEngine()
        self.knowledge_engine = KnowledgeEngine(
            seed_core_knowledge=seed_core_knowledge,
            storage_provider=self.storage_provider,
        )
        self.reasoning_engine = ReasoningEngine(self.knowledge_engine)
        self.context_engine = ContextEngine(
            self.knowledge_engine, storage_provider=self.storage_provider
        )
        self.learning_engine = LearningEngine(
            self.knowledge_engine, context_engine=self.context_engine
        )
        self.language_generator = LanguageGenerator(self.context_engine)

    def analyze_text(
        self, text: str, *,
        context_snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Analyze one utterance; context is an external, per-call input only.

        The snapshot is deliberately not inserted into the Semantic payload:
        Semantic's stable 12-field contract only describes the current text.
        The adapter may pass the same snapshot separately to LanguageGenerator.
        """
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text must be a non-empty string")
        if context_snapshot is not None and not isinstance(context_snapshot, dict):
            raise TypeError("context_snapshot must be a dictionary or None")
        return analyze_semantics(text)

    def create_session(self, metadata: dict[str, Any] | None = None) -> str:
        """Legacy ContextEngine session API for knowledge/episodic integrations."""
        return self.context_engine.create_session(metadata)

    def close_session(
        self, session_id: str, *, clear_working: bool = True
    ) -> dict[str, Any]:
        return self.context_engine.close_session(session_id, clear_working=clear_working)

    def close(self) -> None:
        if self.storage_provider is not None:
            self.storage_provider.close()

    def chatbot(self):
        from ilis.interfaces.chatbot_adapter import ChatbotAdapter
        return ChatbotAdapter(self)

    def game(self):
        from ilis.interfaces.game_adapter import GameEngineAdapter
        return GameEngineAdapter(self)
