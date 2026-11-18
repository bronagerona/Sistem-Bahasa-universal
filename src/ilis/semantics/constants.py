"""Contract enums for the deterministic ILIS Semantic Engine V1."""

CONTRACT_VERSION = "1.0"

STATUSES = frozenset({"supported", "low_confidence", "unsupported"})
ASPECTS = frozenset({"progressive", "completed", "prospective", "habitual", "unspecified"})
NEGATIONS = frozenset({"none", "negative", "not_yet", "identity_negative"})
MODALITIES = frozenset({"none", "ability", "obligation", "possibility", "desire", "permission"})
INTENTS = frozenset({"assertion"})
REGISTERS = frozenset({"formal", "informal", "slang", "unknown"})

SEMANTIC_FIELDS = (
    "Actor",
    "Predicate",
    "Patient/Object",
    "Recipient",
    "Location",
    "Time",
    "Aspect",
    "Negation",
    "Modality",
    "Intent",
    "Register",
    "Confidence",
)
