"""Public ILIS interface adapters."""

from ilis.interfaces.ilis_core import ILISCore
from ilis.interfaces.chatbot_adapter import ChatbotAdapter
from ilis.interfaces.game_adapter import GameEngineAdapter

__all__ = ["ILISCore", "ChatbotAdapter", "GameEngineAdapter"]
