"""Deterministic rule-based reasoning over an ILIS KnowledgeEngine."""

from __future__ import annotations

from typing import Any

from ilis.cognition.inference_rules import (
    BURN_RISK_RULE,
    DRAGON_BELL_RULE,
    matching_burn_risk_premises,
    matching_rule_premises,
)
from ilis.cognition.knowledge_engine import KnowledgeEngine
from ilis.semantics.contract_validator import ContractValidationError, validate_output


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

    def infer_dragon_bell(self) -> dict[str, Any]:
        """Apply the V2 two-premise rule: bell -> loud sound -> scares dragon."""
        facts = self.knowledge_engine.fact_store.all()
        conflicts = [
            group for group in self.knowledge_engine.detect_conflicts()
            if any(f.get("subject") in {"naga", "lonceng"} or
                   f.get("object") in {"naga", "lonceng"} for f in group)
        ]
        if conflicts:
            return self._result(
                conclusion="Data tentang naga dan lonceng memiliki fakta yang saling bertentangan.",
                confidence_score=0.0,
                evidence=sorted({f["id"] for group in conflicts for f in group}),
                reasoning_type="conflicting",
                reasons=["Konflik fakta relevan menghentikan penerapan aturan naga-lonceng."],
                uncertainty="Tinjau fakta dan provenance yang bertentangan.",
            )
        premises = matching_rule_premises(facts, DRAGON_BELL_RULE)
        if premises is None:
            return self._result(
                conclusion="Belum cukup data untuk menentukan apakah lonceng dapat menakuti naga.",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=["Dibutuhkan fakta naga takut suara keras dan lonceng menghasilkan suara keras."],
                uncertainty="Premis yang tidak tersedia tidak dapat dianggap benar.",
            )
        fear_fact, sound_fact = premises
        evidence = [fear_fact["id"], sound_fact["id"]]
        records = [self.knowledge_engine.get_provenance(fid) for fid in evidence]
        if any(record is None for record in records):
            return self._result(
                conclusion="Provenance fakta aturan naga-lonceng tidak lengkap.",
                confidence_score=0.0, evidence=evidence, reasoning_type="unknown",
                reasons=["Satu atau lebih fakta pendukung tidak memiliki provenance."],
                uncertainty="Lengkapi provenance sebelum menggunakan kesimpulan.",
            )
        statuses = []
        for fact, record in zip((fear_fact, sound_fact), records):
            if fact.get("status") != record.get("status"):
                return self._result(
                    conclusion="Status fakta dan provenance tidak konsisten; inferensi dihentikan.",
                    confidence_score=0.0, evidence=evidence, reasoning_type="conflicting",
                    reasons=["Status pada FactStore berbeda dari ProvenanceStore."],
                    uncertainty="Selaraskan status fakta dan provenance.",
                )
            statuses.append(fact.get("status"))
        if "conflicting" in statuses:
            return self._result(
                conclusion="Premis aturan naga-lonceng berstatus conflicting.",
                confidence_score=0.0, evidence=evidence, reasoning_type="conflicting",
                reasons=["Setidaknya satu premis berstatus conflicting."],
                uncertainty="Selesaikan konflik sebelum menarik kesimpulan.",
            )
        verified = all(status == "verified" for status in statuses)
        return self._result(
            conclusion=DRAGON_BELL_RULE["conclusion"],
            confidence_score=0.72 if verified else 0.48,
            evidence=evidence,
            reasoning_type="verified_inference" if verified else "hypothetical_inference",
            reasons=[
                f"Fakta {fear_fact['id']}: naga fears suara_keras ({statuses[0]}).",
                f"Fakta {sound_fact['id']}: lonceng produces suara_keras ({statuses[1]}).",
                "Kedua premis berbagi objek suara_keras sehingga aturan naga_bell_fear_v2 dapat diterapkan.",
            ],
            uncertainty=DRAGON_BELL_RULE["uncertainty"] if verified else
                "Setidaknya satu premis masih berupa hipotesis; " + DRAGON_BELL_RULE["uncertainty"],
        )

    def infer_semantic(self, semantic_result: dict[str, Any]) -> dict[str, Any]:
        """Answer supported semantic questions; keep commands and assertions distinct.

        Accepts the SemanticEngine.analyze() result without changing either
        engine's contract. The returned reasoning result keeps the six V1 keys.
        """
        try:
            validated_result = validate_output(semantic_result)
        except (ContractValidationError, TypeError, ValueError):
            return self._result(
                conclusion="Kontrak semantik tidak valid sehingga inferensi dihentikan.",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=["Payload Semantic Engine gagal melewati contract_validator."],
                uncertainty="Kirim hasil Semantic Engine dengan wrapper dan tepat dua belas field yang valid.",
            )

        if validated_result["status"] != "supported":
            return self._result(
                conclusion="Input semantik belum didukung sehingga belum dapat dijawab.",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=[f"Semantic Engine memberikan status {validated_result['status']}."],
                uncertainty="Perjelas atau sederhanakan kalimat.",
            )
        semantics = validated_result["semantics"]
        intent = semantics.get("Intent")
        if intent != "question":
            label = "perintah" if intent == "command" else "pernyataan"
            return self._result(
                conclusion=f"Input dikenali sebagai {label}, bukan pertanyaan yang perlu dijawab.",
                confidence_score=0.0, evidence=[],
                reasoning_type="command" if intent == "command" else "assertion",
                reasons=[f"Semantic Engine mengklasifikasikan Intent sebagai {intent}."],
                uncertainty="Gunakan pertanyaan eksplisit untuk meminta kesimpulan.",
            )
        actor = semantics.get("Actor")
        predicate = semantics.get("Predicate")
        patient = semantics.get("Patient/Object")
        if not all(isinstance(value, str) and value.strip() for value in (actor, predicate, patient)):
            return self._result(
                conclusion="Pertanyaan belum memiliki subjek, predikat, dan objek yang cukup jelas.",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=["Komponen semantik untuk pencarian fakta tidak lengkap."],
                uncertainty="Pertanyaan dengan pola subjek-predikat-objek diperlukan.",
            )
        if semantics.get("Negation") != "none":
            return self._result(
                conclusion="Pertanyaan negatif belum didukung oleh aturan inferensi V2.",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=["Negasi tidak dipetakan menjadi relasi fakta positif."],
                uncertainty="Diperlukan aturan khusus untuk pertanyaan negatif.",
            )
        # The dragon/bell rule is exposed through the validated semantic question path.
        if (
            actor.casefold() == "lonceng"
            and predicate.casefold() in {"menakuti", "takut"}
            and patient.casefold() == "naga"
        ):
            return self.infer_dragon_bell()

        relation_aliases = {"membakar": "can_burn", "bakar": "can_burn"}
        relation = relation_aliases.get(predicate.casefold(), predicate.casefold())
        matches = [
            fact for fact in self.knowledge_engine.fact_store.all()
            if fact.get("subject") == actor.casefold()
            and fact.get("relation") == relation
            and fact.get("object") == patient.casefold()
        ]
        related = [
            fact for fact in self.knowledge_engine.fact_store.all()
            if fact.get("subject") == actor.casefold() and fact.get("relation") == relation
        ]
        if len({fact.get("object") for fact in related}) > 1 or any(
            fact.get("status") == "conflicting" for fact in matches
        ):
            evidence = sorted({fact["id"] for fact in related})
            return self._result(
                conclusion=f"Belum dapat dipastikan apakah {actor} {predicate} {patient}; fakta terkait saling bertentangan.",
                confidence_score=0.0, evidence=evidence, reasoning_type="conflicting",
                reasons=["Knowledge Engine menemukan klaim yang bertentangan untuk relasi yang ditanyakan."],
                uncertainty="Tinjau fakta dan provenance sebelum menjawab.",
            )
        if not matches:
            return self._result(
                conclusion=f"Belum ada bukti yang cukup untuk menjawab apakah {actor} {predicate} {patient}.",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=["Tidak ditemukan fakta dengan subjek, relasi, dan objek yang cocok."],
                uncertainty="Tidak adanya fakta bukan berarti jawabannya tidak.",
            )
        fact = matches[0]
        provenance = self.knowledge_engine.get_provenance(fact["id"])
        if provenance is None:
            return self._result(
                conclusion="Fakta ditemukan, tetapi provenance-nya tidak tersedia.",
                confidence_score=0.0, evidence=[fact["id"]], reasoning_type="unknown",
                reasons=["Fakta pendukung tidak memiliki catatan provenance."],
                uncertainty="Lengkapi provenance sebelum menarik jawaban.",
            )
        if fact.get("status") != provenance.get("status") or fact.get("status") == "conflicting":
            return self._result(
                conclusion="Status fakta tidak konsisten atau conflicting; jawaban ditahan.",
                confidence_score=0.0, evidence=[fact["id"]], reasoning_type="conflicting",
                reasons=["Status fakta dan provenance harus konsisten dan tidak conflicting."],
                uncertainty="Periksa kembali sumber fakta.",
            )
        verified = fact.get("status") == "verified"
        return self._result(
            conclusion=f"Ya, berdasarkan fakta yang tersimpan, {actor} dapat {predicate} {patient}." if verified
                else f"Ada indikasi bahwa {actor} dapat {predicate} {patient}, tetapi faktanya masih hipotesis.",
            confidence_score=0.72 if verified else 0.48,
            evidence=[fact["id"]],
            reasoning_type="verified_inference" if verified else "hypothetical_inference",
            reasons=[f"Fakta {fact['id']}: {actor} {relation} {patient} ({fact['status']}).",
                     "Jawaban diturunkan dari fakta yang cocok dengan pertanyaan semantik."],
            uncertainty="Kesimpulan berbasis aturan, bukan kepastian universal." if verified
                else "Premis masih berupa hipotesis dan belum diverifikasi.",
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
