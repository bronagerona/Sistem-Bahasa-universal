# ILIS Interface V1 — Developer Guide

## Overview

ILIS Interface V1 is a deterministic integration layer. It wires the existing
Semantic, Knowledge, Reasoning, Context, Learning, and Language Generator
engines without changing their contracts. No LLM, machine-learning model, or
external AI service is used.

## Installation

From the repository root:

```bash
python -m pip install -e ".[dev]"
```

## Initialize ILIS once

```python
from ilis.interfaces import ILISCore

ilis = ILISCore()
session_id = ilis.create_session(metadata={"register": "formal"})
chatbot = ilis.chatbot()
game = ilis.game()
```

ILISCore exposes `semantic_engine`, `knowledge_engine`, `reasoning_engine`,
`context_engine`, `learning_engine`, and `language_generator`. Sessions
are owned by ContextEngine and should be closed when the conversation/game
session ends.

## Chatbot adapter

```python
result = chatbot.respond("Api menyentuh rumah kayu", session_id)
print(result["answer"])
print(result["metadata"])
```

The adapter stores the user's message and calls Semantic analysis through
ContextEngine, then invokes supported deterministic reasoning and generates
register-aware Indonesian. Pass `register="formal"`, `"informal"`, or
`"slang"` to override the session/semantic register.

V1 includes a narrow explicit fallback for the acceptance phrase
"Api menyentuh rumah kayu": it maps to the existing seeded burn-risk facts.
Semantic Engine V1 does not yet parse that subject/predicate pattern, so the
semantic status is returned transparently rather than being fabricated as
supported. Unsupported sentences receive a cautious unknown response.

The result contains `answer` / `text` and `metadata` including
`confidence_score`, `conflict_status`, `reasoning_type`, evidence,
register, semantic status, and session ID.

## Game/NPC adapter

```python
result = game.handle_event(
    "Naga takut lonceng",
    session_id,
    entities=["naga", "lonceng"],
    npc="penjaga_gua",
)
print(result["dialogue"])
```

Each event is stored in Episodic Memory before interpretation. The V1 adapter
has a narrow explicit event rule for "Naga takut lonceng"; it produces a
low-confidence, episode-backed NPC statement. This is an interpretation of
the game event, not a verified world fact and not a new general-purpose
Reasoning Engine rule. The existing core Reasoning Engine V1 currently only
implements the burn-risk rule. Other events remain stored and receive an
unknown/cautious response unless a supported adapter rule is added.

Game results include the episode, context snapshot, reasoning trace, generated
dialogue, and metadata with confidence, evidence, conflict status, and
interpretation source.

## Session lifecycle and limitations

```python
ilis.close_session(session_id)  # clears Working Memory by default
```

Episodic Memory is retained according to MemoryStore's existing lifecycle.
The adapters do not automatically turn arbitrary event text into verified
knowledge. LearningEngine remains available through `ilis.learning_engine`
for explicit hypothesis workflows; Interface V1 does not auto-confirm facts.

This release is a narrow deterministic adapter, not open-domain language
understanding. New domains/game mechanics should be added as explicit,
tested rules or supplied as structured meaning to the generator.
