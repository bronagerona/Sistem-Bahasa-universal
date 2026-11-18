"""Game/NPC adapter for episodic events and cautious NPC responses."""

from __future__ import annotations

import re
from typing import Any

from ilis.interfaces.ilis_core import ILISCore
from ilis.persona import PersonaConfig, PersonaRenderer


class GameEngineAdapter:
    """Record game events and optionally render dialogue as a configured persona."""

    _FEAR_EVENT = re.compile(
        r"^\s*(?P<subject>naga)\s+takut\s+(?P<object>lonceng)\s*[.!?]?\s*$",
        re.IGNORECASE,
    )
    _BURN_EVENT = re.compile(
        r"^\s*(?P<source>api)\s+menyentuh\s+(?P<target>rumah)\s+(?P<material>kayu)\s*[.!?]?\s*$",
        re.IGNORECASE,
    )

    def __init__(
        self, core: ILISCore, *, persona_config: PersonaConfig | None = None
    ) -> None:
        if not isinstance(core, ILISCore):
            raise TypeError("core must be an ILISCore instance")
        self.core = core
        # A generic game adapter has no safe default character identity.
        # The host game opts in by passing a Mode B or Mode C configuration.
        self.persona_renderer = (
            PersonaRenderer(persona_config) if persona_config is not None else None
        )

    def handle_event(
        self, event: str, session_id: str, *, entities: list[str] | None = None,
        attributes: dict[str, Any] | None = None, event_type: str = "game_event",
        npc: str = "npc",
    ) -> dict[str, Any]:
        if not isinstance(event, str) or not event.strip():
            raise ValueError("event must be a non-empty string")
        episode = self.core.context_engine.record_event(
            session_id, event, event_type=event_type,
            entities=entities or self._entities_for(event),
            attributes=attributes,
        )
        context = self.core.context_engine.get_context(session_id)
        burn = self._BURN_EVENT.fullmatch(event)
        fear = self._FEAR_EVENT.fullmatch(event)
        if burn:
            reasoning = self.core.reasoning_engine.infer_burn_risk(
                burn.group("source").casefold(), burn.group("target").casefold()
            )
            meaning = None
        elif fear:
            subject, feared = fear.group("subject").casefold(), fear.group("object").casefold()
            reasoning = {
                "conclusion": f"Episode game mencatat bahwa {subject} takut pada {feared}.",
                "confidence_score": 0.48,
                "evidence": [episode["episode_id"]],
                "reasoning_type": "hypothetical_inference",
                "reasons": ["Interpretasi terbatas berasal langsung dari deskripsi episode game."],
                "uncertainty": "Ini adalah catatan/persepsi dalam sesi game, bukan fakta dunia yang diverifikasi.",
            }
            meaning = {
                "kind": "statement",
                "proposition": f"Catatan sesi menyebut {subject} takut pada {feared}",
            }
            reasoning["meaning"] = meaning
        else:
            reasoning = {
                "conclusion": "Belum cukup data untuk menarik kesimpulan dari peristiwa game ini.",
                "confidence_score": 0.0, "evidence": [episode["episode_id"]],
                "reasoning_type": "unknown",
                "reasons": ["Tidak ada aturan interpretasi adapter V1 yang cocok."],
                "uncertainty": "Episode tersimpan, tetapi belum ada aturan untuk menafsirkannya.",
            }
        generated = self.core.language_generator.generate(
            reasoning, context=context
        )
        raw_dialogue = generated["text"]
        dialogue = (
            self.persona_renderer.render(raw_dialogue)
            if self.persona_renderer is not None
            else raw_dialogue
        )
        return {
            "npc": npc,
            "dialogue": dialogue,
            "answer": dialogue,
            "metadata": {
                "session_id": session_id,
                "episode_id": episode["episode_id"],
                "confidence_score": generated["confidence_score"],
                "reasoning_type": generated["reasoning_type"],
                "evidence": generated["evidence"],
                "conflict_status": "conflicting" if reasoning["reasoning_type"] == "conflicting" else "clear",
                "interpretation_source": "episodic_rule" if fear else "reasoning_engine" if burn else "none",
            },
            "episode": episode,
            "context": context,
            "reasoning_result": reasoning,
            "generation": generated,
        }

    @staticmethod
    def _entities_for(event: str) -> list[str]:
        words = re.findall(r"[a-zA-ZÀ-ÿ-]+", event.casefold())
        return list(dict.fromkeys(words))
