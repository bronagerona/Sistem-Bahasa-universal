"""Contract enums for the ILIS Semantic Engine, compatible with contract 1.0."""

CONTRACT_VERSION = "1.0"

STATUSES = frozenset({"supported", "unsupported", "low_confidence"})
ASPECTS = frozenset({"progressive", "completed", "prospective", "habitual", "unspecified"})
NEGATIONS = frozenset({"none", "negative", "not_yet", "identity_negative"})
MODALITIES = frozenset({"none", "ability", "obligation", "possibility", "desire", "permission"})
INTENTS = frozenset({"assertion", "question", "command", "greeting"})
REGISTERS = frozenset({"formal", "informal", "slang", "unknown"})

SEMANTIC_FIELDS = (
    "Actor", "Predicate", "Patient/Object", "Recipient", "Location", "Time",
    "Aspect", "Negation", "Modality", "Intent", "Register", "Confidence",
)
