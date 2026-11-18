"""Deterministic V1 inference rules for ILIS cognition.

Rules operate on explicit subject-relation-object triples. They describe
limited rule-based possibilities, not universal laws or guaranteed outcomes.
"""

from __future__ import annotations

from typing import Any


BURN_RISK_RULE: dict[str, Any] = {
    "id": "material_burn_risk_v1",
    "name": "combustible_material_exposure",
    "premises": (
        ("source", "can_burn", "material"),
        ("target", "made_of", "material"),
    ),
    "conclusion_relation": "may_burn",
    "conclusion_template": (
        "{source} yang menyambar {target} berbahan {material} "
        "berpotensi menyebabkan {target} terbakar."
    ),
    "uncertainty": (
        "Ini adalah kesimpulan berbasis aturan, bukan kepastian. "
        "Hasil nyata bergantung pada kondisi seperti intensitas dan durasi api, "
        "kadar air, perlakuan bahan, serta faktor lingkungan."
    ),
}

INFERENCE_RULES: tuple[dict[str, Any], ...] = (BURN_RISK_RULE,)


def matching_burn_risk_premises(
    facts: list[dict[str, Any]], source: str, target: str
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Return the two exact triples needed by the V1 burn-risk rule."""
    source = " ".join(source.casefold().split())
    target = " ".join(target.casefold().split())

    burn_facts = [
        fact for fact in facts
        if fact.get("subject") == source and fact.get("relation") == "can_burn"
    ]
    material_facts = [
        fact for fact in facts
        if fact.get("subject") == target and fact.get("relation") == "made_of"
    ]

    for burn_fact in burn_facts:
        for material_fact in material_facts:
            if burn_fact.get("object") == material_fact.get("object"):
                return burn_fact, material_fact
    return None
