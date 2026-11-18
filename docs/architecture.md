# ILIS architecture notes

## Core boundary

ILIS separates the surface form of language from the internal representation used
for later semantic and cognitive processing.

The first prototype implements only two small capabilities:

1. tokenization that preserves punctuation and source forms;
2. explicit lexical variation hints for a small set of Indonesian colloquial forms.

It does **not** yet infer sentence meaning, resolve ambiguity, reason, learn from
experience, or generate open-ended language.

## Planned layers

- **Language layer:** tokenization, morphology, syntax, spelling variation,
  register, slang, abbreviations, and typo handling.
- **Semantic layer:** compositional meaning representation, entities, events,
  roles, polarity, tense/aspect, modality, and uncertainty.
- **Knowledge layer:** concepts, relations, provenance, and confidence.
- **Cognition layer:** inference, planning, context tracking, and decision-making.
- **Learning layer:** updates from language and environment experience, with
  validation and contradiction handling.
- **Generation layer:** construct utterances from intended meaning, context,
  audience, and register.
- **Adapters:** chatbot and game-engine interfaces.

## Important design constraints

- Preserve the original input; normalization must not erase register or nuance.
- Do not treat spelling similarity as proof of semantic equivalence.
- Keep uncertain interpretations explicit rather than silently guessing.
- Record provenance for learned claims and distinguish observation from inference.
- Make every module testable in isolation.
- Do not describe the system as LLM-equivalent until rigorous evaluations support
  such a claim.

## First milestone

A user can submit Indonesian text and inspect token boundaries and known lexical
variation hints using the CLI. This establishes a small, testable foundation for
later parsing and semantic representation.
