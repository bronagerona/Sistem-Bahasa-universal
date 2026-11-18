"""Game/NPC adapter for episodic events and adapter-owned dialogue history."""

from __future__ import annotations

import re
from typing import Any

from ilis.interfaces.ilis_core import ILISCore
from ilis.interfaces.session_manager import SessionManager
from ilis.persona import PersonaConfig, PersonaRenderer


class GameEngineAdapter:
    """Record game events while keeping dialogue turns outside Core memory."""

    _FEAR_EVENT = re.compile(
        r"^\s*(?P<subject>naga)\s+takut\s+(?P<object>lonceng)\s*[.!?]?\s*$",
        re.IGNORECASE,
    )
    _BURN_EVENT = re.compile(
        r"^\s*(?P<source>api)\s+menyentuh\s+(?P<target>rumah)\s+(?P<material>kayu)\s*[.!?]?\s*$",
        re.IGNORECASE,
    )
    _RESET_COMMAND = re.compile(
        r"^\s*(?:reset\s+percakapan|hapus\s+riwayat(?:\s+percakapan)?)\s*[.!?]*\s*$",
        re.IGNORECASE,
    )

    def __init__(
        self, core: ILISCore, *, persona_config: PersonaConfig | None = None,
        session_manager: SessionManager | None = None,
    ) -> None:
        if not isinstance(core, ILISCore):
            raise TypeError("core must be an ILISCore instance")
        if session_manager is not None and not isinstance(session_manager, SessionManager):
            raise TypeError("session_manager must be a SessionManager instance")
        self.core = core
        self.session_manager = session_manager if session_manager is not None else SessionManager()
        self.persona_renderer = (
            PersonaRenderer(persona_config) if persona_config is not None else None
        )

    def create_session(self, metadata: dict[str, Any] | None = None) -> str:
        """Create a conversation session and a separate episodic scope."""
        episodic_session_id = self.core.create_session(metadata=metadata)
        session_metadata = dict(metadata or {})
        session_metadata["_episodic_session_id"] = episodic_session_id
        return self.session_manager.create_session(metadata=session_metadata)

    def handle_event(
        self, event: str, session_id: str | None = None, *, entities: list[str] | None = None,
        attributes: dict[str, Any] | None = None, event_type: str = "game_event",
        npc: str = "npc", conversation_session_id: str | None = None,
        context_snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if not isinstance(event, str) or not event.strip():
            raise ValueError("event must be a non-empty string")
        if session_id is None:
            conversation_id = conversation_session_id
            if conversation_id is None:
                conversation_id = self.create_session()
            elif self.session_manager.get_session(conversation_id) is None:
                episodic_id = self.core.create_session()
                self.session_manager.ensure_session(
                    conversation_id, metadata={"_episodic_session_id": episodic_id}
                )
            session = self.session_manager.require_session(conversation_id)
            episodic_session_id = session.metadata.get("_episodic_session_id")
        elif self.session_manager.get_session(session_id) is not None:
            conversation_id = conversation_session_id or session_id
            session = self.session_manager.require_session(conversation_id)
            episodic_session_id = session.metadata.get("_episodic_session_id") or session_id
        else:
            # Backward-compatible path: the old positional session_id is an
            # existing ContextEngine episodic scope, not a transcript store.
            legacy_context = self.core.context_engine.get_context(session_id)
            conversation_id = conversation_session_id or session_id
            metadata = dict(legacy_context.get("session", {}).get("metadata", {}))
            metadata["_episodic_session_id"] = session_id
            self.session_manager.ensure_session(conversation_id, metadata=metadata)
            session = self.session_manager.require_session(conversation_id)
            episodic_session_id = session_id

        if not isinstance(episodic_session_id, str) or not episodic_session_id:
            raise ValueError("game conversation has no episodic memory scope")

        if self._RESET_COMMAND.fullmatch(event):
            reset = self.session_manager.reset_session(conversation_id)
            dialogue = "Riwayat percakapan sesi ini sudah direset. Kita mulai dari awal, ya."
            return {
                "npc": npc, "dialogue": dialogue, "answer": dialogue,
                "metadata": {
                    "session_id": conversation_id, "response_type": "session_reset",
                    "deleted_turns": reset["deleted_turns"],
                },
                "episode": None, "context": None,
                "conversation_context": self.session_manager.get_context_snapshot(conversation_id),
                "reasoning_result": None, "generation": None,
            }

        managed_snapshot = self.session_manager.get_context_snapshot(conversation_id)
        if context_snapshot is not None:
            if not isinstance(context_snapshot, dict):
                raise TypeError("context_snapshot must be a dictionary or None")
            if context_snapshot.get("session_id", conversation_id) != conversation_id:
                raise ValueError("context_snapshot session_id does not match conversation_session_id")
            snapshot = dict(managed_snapshot)
            snapshot["additional_context"] = dict(context_snapshot)
        else:
            snapshot = managed_snapshot

        episode = self.core.context_engine.record_event(
            episodic_session_id, event, event_type=event_type,
            entities=entities or self._entities_for(event),
            attributes=attributes,
        )
        core_context = self.core.context_engine.get_context(episodic_session_id)
        burn = self._BURN_EVENT.fullmatch(event)
        fear = self._FEAR_EVENT.fullmatch(event)
        if burn:
            reasoning = self.core.reasoning_engine.infer_burn_risk(
                burn.group("source").casefold(), burn.group("target").casefold()
            )
        elif fear:
            subject, feared = fear.group("subject").casefold(), fear.group("object").casefold()
            reasoning = {
                "conclusion": f"Episode game mencatat bahwa {subject} takut pada {feared}.",
                "confidence_score": 0.48, "evidence": [episode["episode_id"]],
                "reasoning_type": "hypothetical_inference",
                "reasons": ["Interpretasi terbatas berasal langsung dari deskripsi episode game."],
                "uncertainty": "Ini adalah catatan/persepsi dalam sesi game, bukan fakta dunia yang diverifikasi.",
            }
            reasoning["meaning"] = {
                "kind": "statement",
                "proposition": f"Catatan sesi menyebut {subject} takut pada {feared}",
            }
        else:
            reasoning = {
                "conclusion": "Belum cukup data untuk menarik kesimpulan dari peristiwa game ini.",
                "confidence_score": 0.0, "evidence": [episode["episode_id"]],
                "reasoning_type": "unknown",
                "reasons": ["Tidak ada aturan interpretasi adapter V1 yang cocok."],
                "uncertainty": "Episode tersimpan, tetapi belum ada aturan untuk menafsirkannya.",
            }
        core_session_metadata = core_context.get("session", {}).get("metadata", {})
        default_register = core_session_metadata.get("register") if isinstance(core_session_metadata, dict) else None
        generated = self.core.language_generator.generate(
            reasoning, register=default_register, context=snapshot
        )
        raw_dialogue = generated["text"]
        dialogue = self.persona_renderer.render(raw_dialogue) if self.persona_renderer else raw_dialogue
        self.session_manager.add_turn(conversation_id, event, dialogue, metadata={
            "npc": npc, "event_type": event_type,
        })
        return {
            "npc": npc, "dialogue": dialogue, "answer": dialogue,
            "metadata": {
                "session_id": conversation_id, "episode_id": episode["episode_id"],
                "confidence_score": generated["confidence_score"],
                "reasoning_type": generated["reasoning_type"],
                "evidence": generated["evidence"],
                "conflict_status": "conflicting" if reasoning["reasoning_type"] == "conflicting" else "clear",
                "interpretation_source": "episodic_rule" if fear else "reasoning_engine" if burn else "none",
                "context_turns_used": len(snapshot.get("turns", [])),
            },
            "episode": episode, "context": core_context,
            "conversation_context": snapshot,
            "reasoning_result": reasoning, "generation": generated,
        }

    @staticmethod
    def _entities_for(event: str) -> list[str]:
        words = re.findall(r"[a-zA-ZÀ-ÿ-]+", event.casefold())
        return list(dict.fromkeys(words))
