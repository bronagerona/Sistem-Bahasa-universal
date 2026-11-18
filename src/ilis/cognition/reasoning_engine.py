"""Deterministic rule-based reasoning over an ILIS KnowledgeEngine."""

from __future__ import annotations

from typing import Any

from ilis.cognition.inference_rules import (
    BURN_RISK_RULE,
    matching_burn_risk_premises,
)
from ilis.cognition.knowledge_engine import KnowledgeEngine


class ReasoningEngine:
    """Derive cautious, traceable conclusions from stored knowledge triples.

    No language model, statistical model, external service, or world simulation
    is used. V1 implements only the explicit burn-risk rule.
    """

    def __init__(self, knowledge_engine: KnowledgeEngine) -> None:
        if not isinstance(knowledge_engine, KnowledgeEngine):
            raise TypeError("knowledge_engine must be a KnowledgeEngine instance")
        self.knowledge_engine = knowledge_engine

    def infer_burn_risk(self, source: str, target: str) -> dict[str, Any]:
        """Assess whether a source may cause a target to burn.

        The rule requires:
        - source --can_burn--> material
        - target --made_of--> material

        Fact and provenance statuses are both checked. Conflicting relevant
        knowledge blocks inference; missing premises/provenance yield unknown.
        """
        source_key = self._normalize(source, "source")
        target_key = self._normalize(target, "target")
        facts = self.knowledge_engine.fact_store.all()
        conflicts = self._relevant_conflicts(source_key, target_key)

        if conflicts:
            evidence = sorted({
                fact["id"] for group in conflicts for fact in group
            })
            return self._result(
                conclusion=(
                    f"Data tentang kemungkinan {target_key} terbakar oleh "
                    f"{source_key} memiliki fakta yang saling bertentangan."
                ),
                confidence_score=0.0,
                evidence=evidence,
                reasoning_type="conflicting",
                reasons=[
                    "Knowledge Engine mendeteksi konflik pada fakta yang relevan.",
                    "Inferensi dihentikan agar tidak memilih salah satu klaim secara sewenang-wenang.",
                ],
                uncertainty="Selesaikan konflik dan tinjau provenance sebelum menarik kesimpulan.",
            )

        premises = matching_burn_risk_premises(facts, source_key, target_key)
        if premises is None:
            return self._result(
                conclusion=f"Belum cukup data untuk menentukan apakah {target_key} dapat terbakar oleh {source_key}.",
                confidence_score=0.0,
                evidence=[],
                reasoning_type="unknown",
                reasons=[
                    "Aturan V1 membutuhkan fakta source --can_burn--> material.",
                    "Aturan V1 juga membutuhkan fakta target --made_of--> material dengan material yang sama.",
                    "Pasangan fakta pendukung yang lengkap tidak ditemukan.",
                ],
                uncertainty="Data tidak tersedia bukan berarti peristiwa tersebut mustahil terjadi.",
            )

        burn_fact, material_fact = premises
        evidence = [burn_fact["id"], material_fact["id"]]
        provenance = [
            self.knowledge_engine.get_provenance(fact_id)
            for fact_id in evidence
        ]

        if any(item is None for item in provenance):
            return self._result(
                conclusion=f"Data provenance untuk menilai risiko {target_key} terbakar tidak lengkap.",
                confidence_score=0.0,
                evidence=evidence,
                reasoning_type="unknown",
                reasons=["Satu atau lebih fakta pendukung tidak memiliki catatan provenance."],
                uncertainty="Sumber dan status fakta harus tersedia sebelum inferensi dapat dipercaya.",
            )

        statuses = []
        for fact, record in zip((burn_fact, material_fact), provenance):
            if fact.get("status") != record.get("status"):
                return self._result(
                    conclusion="Status fakta dan provenance tidak konsisten; inferensi dihentikan.",
                    confidence_score=0.0,
                    evidence=evidence,
                    reasoning_type="conflicting",
                    reasons=["Status pada FactStore berbeda dari status pada ProvenanceStore."],
                    uncertainty="Periksa dan selaraskan catatan fakta serta provenance.",
                )
            statuses.append(fact.get("status"))

        if "conflicting" in statuses:
            return self._result(
                conclusion="Fakta pendukung berstatus conflicting; kesimpulan tidak dapat ditarik.",
                confidence_score=0.0,
                evidence=evidence,
                reasoning_type="conflicting",
                reasons=["Setidaknya satu premis berstatus conflicting."],
                uncertainty="Tinjau konflik fakta terlebih dahulu.",
            )

        material = burn_fact["object"]
        conclusion = BURN_RISK_RULE["conclusion_template"].format(
            source=source_key, target=target_key, material=material
        )
        reasons = [
            f"Fakta {burn_fact['id']}: {source_key} can_burn {material} ({statuses[0]}).",
            f"Fakta {material_fact['id']}: {target_key} made_of {material} ({statuses[1]}).",
            "Aturan material_combustible_exposure menghubungkan kedua premis karena materialnya sama.",
            "Aturan hanya mendukung kemungkinan terbakar, bukan kepastian kejadian.",
        ]

        if all(status == "verified" for status in statuses):
            return self._result(
                conclusion=conclusion,
                confidence_score=0.72,
                evidence=evidence,
                reasoning_type="verified_inference",
                reasons=reasons,
                uncertainty=BURN_RISK_RULE["uncertainty"],
            )

        return self._result(
            conclusion=conclusion,
            confidence_score=0.48,
            evidence=evidence,
            reasoning_type="hypothetical_inference",
            reasons=reasons + ["Setidaknya satu premis masih berupa hipotesis."],
            uncertainty=(
                "Kesimpulan bergantung pada hipotesis yang belum diverifikasi. "
                + BURN_RISK_RULE["uncertainty"]
            ),
        )

    def infer(self, source: str, target: str) -> dict[str, Any]:
        """Alias for the V1 burn-risk inference entry point."""
        return self.infer_burn_risk(source, target)

    def _relevant_conflicts(
        self, source: str, target: str
    ) -> list[list[dict[str, Any]]]:
        """Find conflicts touching either queried concept or V1 rule relation."""
        return [
            group for group in self.knowledge_engine.detect_conflicts()
            if any(
                fact.get("subject") in {source, target}
                or fact.get("object") in {source, target}
                for fact in group
            )
        ]

    @staticmethod
    def _normalize(value: str, field: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{field} must be a non-empty string")
        return " ".join(value.casefold().split())

    @staticmethod
    def _result(
        *,
        conclusion: str,
        confidence_score: float,
        evidence: list[str],
        reasoning_type: str,
        reasons: list[str],
        uncertainty: str,
    ) -> dict[str, Any]:
        return {
            "conclusion": conclusion,
            "confidence_score": confidence_score,
            "evidence": evidence,
            "reasoning_type": reasoning_type,
            "reasons": reasons,
            "uncertainty": uncertainty,
        }
