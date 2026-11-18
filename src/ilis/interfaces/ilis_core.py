"""Single entry point that wires every deterministic ILIS V1 engine."""

from __future__ import annotations

from typing import Any

from ilis.cognition.context_engine import ContextEngine
from ilis.cognition.knowledge_engine import KnowledgeEngine
from ilis.cognition.reasoning_engine import ReasoningEngine
from ilis.generation.language_generator import LanguageGenerator
from ilis.learning.learning_engine import LearningEngine
from ilis.semantics.semantic_engine import SemanticEngine


class ILISCore:
    """Initialize and expose the complete ILIS engine stack."""

    def __init__(self, *, seed_core_knowledge: bool = True) -> None:
        self.semantic_engine = SemanticEngine()
        self.knowledge_engine = KnowledgeEngine(seed_core_knowledge=seed_core_knowledge)
        self.reasoning_engine = ReasoningEngine(self.knowledge_engine)
        self.context_engine = ContextEngine(self.knowledge_engine)
        self.learning_engine = LearningEngine(
            self.knowledge_engine, context_engine=self.context_engine
        )
        self.language_generator = LanguageGenerator(self.context_engine)

    def create_session(self, metadata: dict[str, Any] | None = None) -> str:
        return self.context_engine.create_session(metadata)

    def close_session(self, session_id: str, *, clear_working: bool = True) -> dict[str, Any]:
        return self.context_engine.close_session(session_id, clear_working=clear_working)

    def chatbot(self):
        from ilis.interfaces.chatbot_adapter import ChatbotAdapter
        return ChatbotAdapter(self)

    def game(self):
        from ilis.interfaces.game_adapter import GameEngineAdapter
        return GameEngineAdapter(self)
