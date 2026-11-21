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

DRAGON_BELL_RULE: dict[str, Any] = {
    "id": "dragon_bell_fear_v2",
    "name": "dragon_fears_loud_sound",
    "premises": (
        ("naga", "fears", "suara_keras"),
        ("lonceng", "produces", "suara_keras"),
    ),
    "conclusion_relation": "may_scare",
    "conclusion": "Lonceng dapat menakuti naga karena menghasilkan suara keras yang ditakuti naga.",
    "uncertainty": "Kesimpulan bergantung pada fakta yang tersimpan dan bukan simulasi respons semua naga.",
}

INFERENCE_RULES: tuple[dict[str, Any], ...] = (BURN_RISK_RULE, DRAGON_BELL_RULE)


def matching_rule_premises(
    facts: list[dict[str, Any]], rule: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any]] | None:
    """Match the two explicit triples declared by a rule, sharing its variable."""
    first, second = rule["premises"]
    first_matches = [f for f in facts if
        f.get("subject") == first[0] and f.get("relation") == first[1]]
    second_matches = [f for f in facts if
        f.get("subject") == second[0] and f.get("relation") == second[1]]
    for left in first_matches:
        for right in second_matches:
            if left.get("object") == first[2] and right.get("object") == second[2]:
                return left, right
    return None


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
