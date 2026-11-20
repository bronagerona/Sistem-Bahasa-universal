"""Deterministic rule-based reasoning over an ILIS KnowledgeEngine."""

from __future__ import annotations

import re
from typing import Any

from ilis.cognition.inference_rules import (
    BURN_RISK_RULE,
    DRAGON_BELL_RULE,
    matching_burn_risk_premises,
    matching_rule_premises,
)
from ilis.cognition.knowledge_engine import KnowledgeEngine, MULTI_VALUED_RELATIONS
from ilis.concept_engine import (
    ConfidenceLevel,
    ConceptStore,
    InferenceEngine,
)
from ilis.language.pipeline import analyze_semantics
from ilis.semantics.contract_validator import ContractValidationError, validate_output


class ReasoningEngine:
    """Derive cautious, traceable conclusions from stored knowledge triples.

    No language model, statistical model, external service, or world simulation
    is used. V1 implements only the explicit burn-risk rule.
    """

    def __init__(
        self,
        knowledge_engine: KnowledgeEngine,
        *,
        concept_store: ConceptStore | None = None,
        inference_engine: InferenceEngine | None = None,
    ) -> None:
        if not isinstance(knowledge_engine, KnowledgeEngine):
            raise TypeError("knowledge_engine must be a KnowledgeEngine instance")
        if concept_store is not None and not isinstance(concept_store, ConceptStore):
            raise TypeError("concept_store must be a ConceptStore instance")
        if inference_engine is not None and not isinstance(inference_engine, InferenceEngine):
            raise TypeError("inference_engine must be an InferenceEngine instance")
        if concept_store is not None and inference_engine is not None:
            raise ValueError("provide concept_store or inference_engine, not both")
        self.knowledge_engine = knowledge_engine
        self.concept_store = concept_store if concept_store is not None else ConceptStore()
        self.inference_engine = (
            inference_engine if inference_engine is not None
            else InferenceEngine(self.concept_store)
        )

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

    def infer_semantic(
        self, semantic_result: dict[str, Any], *,
        context_snapshot: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Answer semantic questions, using prior turns only to resolve follow-ups.

        Conversation context is read-only and never becomes evidence. Every
        factual conclusion still requires a matching KnowledgeEngine fact.
        The Semantic 12-field and Reasoning six-key contracts remain unchanged.
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

        where_result = self._infer_where_dataset_question(validated_result)
        if where_result is not None:
            return where_result

        if validated_result["status"] != "supported":
            direct_result = self._infer_direct_dataset_question(validated_result)
            if direct_result is not None:
                return direct_result
            contextual_result = self._infer_mercury_followup(
                validated_result, context_snapshot=context_snapshot,
            )
            if contextual_result is not None:
                return contextual_result
            return self._result(
                conclusion="Input semantik belum didukung sehingga belum dapat dijawab.",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=[f"Semantic Engine memberikan status {validated_result['status']}."],
                uncertainty="Perjelas atau sederhanakan kalimat.",
            )
        # Work on a private interpretation copy. The Semantic 12-field result
        # returned to callers remains untouched by contextual resolution.
        semantics = dict(validated_result["semantics"])
        if semantics.get("Intent") == "greeting":
            return self._result(
                conclusion="Sapaan dikenali sebagai tindakan percakapan.",
                confidence_score=0.0,
                evidence=[],
                reasoning_type="greeting",
                reasons=[
                    "Semantic Engine mengklasifikasikan Intent sebagai greeting.",
                    "Sapaan tidak memerlukan inferensi fakta dari KnowledgeEngine.",
                ],
                uncertainty="Tidak ada klaim faktual yang sedang dinilai.",
            )
        context_note = None
        if context_snapshot is not None:
            if not isinstance(context_snapshot, dict):
                raise TypeError("context_snapshot must be a dictionary or None")
            turns = context_snapshot.get("turns", [])
            current_text = str(validated_result.get("original_text", ""))
            is_follow_up = bool(
                isinstance(turns, list) and turns
                and re.match(
                    r"^\s*(?:lalu|kemudian|terus|kalau\s+begitu|bagaimana\s+dengan)\b",
                    current_text, flags=re.IGNORECASE,
                )
            )
            if is_follow_up:
                previous_text = turns[-1].get("user_message") if isinstance(turns[-1], dict) else None
                if isinstance(previous_text, str) and previous_text.strip():
                    previous_semantic = analyze_semantics(previous_text)
                    previous_fields = (
                        previous_semantic.get("semantics", {})
                        if previous_semantic.get("status") == "supported" else {}
                    )
                    # Resolve only omitted actor/predicate. The current turn
                    # must still provide its own patient/object.
                    for field in ("Actor", "Predicate"):
                        current_value = semantics.get(field)
                        needs_context = not (
                            isinstance(current_value, str) and current_value.strip()
                        )
                        # The bounded Semantic parser can mistake a discourse
                        # particle in a follow-up ("Lalu ... juga ...") for the
                        # nominal actor. Treat these particles as omitted actors.
                        if field == "Actor" and isinstance(current_value, str):
                            needs_context = needs_context or current_value.casefold() in {
                                "lalu", "kemudian", "terus", "juga", "begitu",
                            }
                        if needs_context:
                            prior_value = previous_fields.get(field)
                            if isinstance(prior_value, str) and prior_value.strip():
                                semantics[field] = prior_value
                    context_note = (
                        "Penanda pertanyaan lanjutan ditafsirkan dengan membaca "
                        "giliran sebelumnya; riwayat hanya membantu memahami "
                        "kalimat dan bukan bukti faktual."
                    )
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
        if not all(
            isinstance(value, str) and value.strip()
            for value in (actor, predicate)
        ):
            return self._result(
                conclusion="Pertanyaan belum memiliki subjek dan predikat yang cukup jelas.",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=["Komponen semantik untuk pencarian fakta tidak lengkap."],
                uncertainty="Pertanyaan dengan subjek dan predikat yang jelas diperlukan.",
            )
        if patient is not None and (
            not isinstance(patient, str) or not patient.strip()
        ):
            patient = None
        if semantics.get("Negation") != "none":
            return self._result(
                conclusion="Pertanyaan negatif belum didukung oleh aturan inferensi V2.",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=["Negasi tidak dipetakan menjadi relasi fakta positif."],
                uncertainty="Diperlukan aturan khusus untuk pertanyaan negatif.",
            )
        # The dragon/bell rule is exposed through the validated semantic question path.
        if (
            (
                actor.casefold() == "lonceng"
                and predicate.casefold() == "menakuti"
                and patient.casefold() == "naga"
            )
            or (
                actor.casefold() == "naga"
                and predicate.casefold() == "takut"
                and patient.casefold() == "lonceng"
            )
        ):
            self._ensure_dragon_bell_core_facts()
            return self.infer_dragon_bell()

        relation_aliases = {"membakar": "can_burn", "bakar": "can_burn"}
        relation = relation_aliases.get(predicate.casefold(), predicate.casefold())
        matches = [
            fact for fact in self.knowledge_engine.fact_store.all()
            if patient is not None
            and fact.get("subject") == actor.casefold()
            and fact.get("relation") == relation
            and fact.get("object") == patient.casefold()
        ]
        dataset_fact_match = False
        if not matches:
            # Map only explicit, bounded predicate forms to dataset wording.
            if predicate.casefold() == "berotasi":
                relation_terms = ["rotasi"]
            elif predicate.casefold() == "mengorbit":
                relation_terms = ["orbit"]
                if patient:
                    relation_terms.extend(
                        token for token in patient.casefold().split()
                        if token not in {"mengelilingi", "mengitari"}
                    )
            elif predicate.casefold() == "memiliki" and patient:
                relation_terms = patient.casefold().split()
            else:
                relation_terms = []
            dataset_matches = self.knowledge_engine.search_dataset_facts(
                actor, relation_terms,
            )
            if len(dataset_matches) == 1:
                matches = dataset_matches
                relation = dataset_matches[0]["relation"]
                dataset_fact_match = True
            elif len(dataset_matches) > 1:
                return self._result(
                    conclusion=f"Beberapa fakta cocok untuk pertanyaan tentang {actor}; sistem tidak memilih salah satunya secara otomatis.",
                    confidence_score=0.0,
                    evidence=[],
                    reasoning_type="unknown",
                    reasons=[
                        "Pencarian KnowledgeEngine menemukan lebih dari satu fakta kandidat.",
                        "Diperlukan pertanyaan yang lebih spesifik agar tidak memilih fakta secara sewenang-wenang.",
                    ],
                    uncertainty="Kandidat fakta yang ambigu belum digunakan sebagai dasar jawaban.",
                )
        related = [
            fact for fact in self.knowledge_engine.fact_store.all()
            if fact.get("subject") == actor.casefold() and fact.get("relation") == relation
        ]
        relation_conflict = any(
            group[0].get("subject") == actor.casefold()
            and group[0].get("relation") == relation
            for group in self.knowledge_engine.detect_conflicts()
            if group
        )
        if relation_conflict or any(
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
            # Exact KnowledgeEngine lookup above always has priority. Only the
            # supported V3 burn-property rule may run as a fallback; legacy
            # conflicts and the dragon/bell path have already been handled.
            if relation == "can_burn":
                return self._infer_concept_fallback(
                    actor, patient, context_note=context_note,
                )
            return self._result(
                conclusion=f"Belum ada bukti yang cukup untuk menjawab pertanyaan tentang {actor} {predicate}" + (f" {patient}." if patient else "."),
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
        if dataset_fact_match:
            record = fact.get("dataset_record", {})
            original_subject = str(record.get("subject", fact["subject"]))
            original_relation = str(record.get("predicate", fact["relation"]))
            original_object = record.get("object", fact["object"])
            if isinstance(original_object, list):
                object_text = ", ".join(str(item) for item in original_object)
            else:
                object_text = str(original_object)
            conclusion = (
                f"{original_subject} {original_relation} {object_text}"
            )
            qualifiers = record.get("qualifiers", [])
            if isinstance(qualifiers, list) and qualifiers:
                conclusion += " Catatan: " + " ".join(
                    str(item) for item in qualifiers if isinstance(item, str)
                )
            reasons = [
                f"Fakta dataset {fact['id']} ditemukan melalui pencocokan subjek dan petunjuk predikat.",
                f"Status fakta: {fact['status']}; sumber: {fact.get('source', 'tidak tercatat')}.",
            ]
            if isinstance(qualifiers, list):
                reasons.extend(
                    f"Kualifikasi sumber: {item}"
                    for item in qualifiers if isinstance(item, str)
                )
            if context_note:
                reasons.append(context_note)
            return self._result(
                conclusion=conclusion,
                confidence_score=0.72 if verified else 0.48,
                evidence=[fact["id"]],
                reasoning_type="verified_inference" if verified else "hypothetical_inference",
                reasons=reasons,
                uncertainty=(
                    "Fakta dataset berstatus draft/hipotesis dan belum diverifikasi; "
                    "jawaban harus dipahami sebagai informasi sementara."
                    if not verified else
                    "Kesimpulan tetap dibatasi oleh cakupan dan kualifikasi sumber."
                ),
            )
        return self._result(
            conclusion=f"Ya, berdasarkan fakta yang tersimpan, {actor} dapat {predicate} {patient}." if verified
                else f"Ada indikasi bahwa {actor} dapat {predicate} {patient}, tetapi faktanya masih hipotesis.",
            confidence_score=0.72 if verified else 0.48,
            evidence=[fact["id"]],
            reasoning_type="verified_inference" if verified else "hypothetical_inference",
            reasons=[
                f"Fakta {fact['id']}: {actor} {relation} {patient} ({fact['status']}).",
                "Jawaban diturunkan dari fakta yang cocok dengan pertanyaan semantik.",
            ] + ([context_note] if context_note else []),
            uncertainty="Kesimpulan berbasis aturan, bukan kepastian universal." if verified
                else "Premis masih berupa hipotesis dan belum diverifikasi.",
        )


    def _infer_where_dataset_question(
        self, semantic_result: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Answer narrowly recognized Indonesian location questions from dataset facts.

        Only the exact dataset predicates below are eligible. The question
        wording selects a subject; the stored object is copied verbatim.
        No dataset schema, Semantic fields, or Reasoning keys are changed.
        """
        question = str(semantic_result.get("original_text", "")).casefold().strip()
        if not re.match(
            r"^(?:di\s+mana(?:kah)?|dimanakah|dari\s+mana)\b",
            question,
        ):
            return None

        facts = self.knowledge_engine.fact_store.all()
        subject_matches: list[tuple[str, dict[str, Any]]] = []
        for fact in facts:
            record = fact.get("dataset_record")
            if not isinstance(record, dict):
                continue
            subject = record.get("subject")
            if not isinstance(subject, str) or not subject.strip():
                continue
            normalized_subject = subject.casefold().strip()
            if normalized_subject in question:
                subject_matches.append((normalized_subject, fact))

        if not subject_matches:
            return self._result(
                conclusion="Saya belum memiliki informasi lokasi untuk itu",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=["Tidak ditemukan subjek yang cocok dengan pertanyaan lokasi."],
                uncertainty="Fakta lokasi yang relevan belum tersedia dalam basis pengetahuan.",
            )

        # Prefer the longest exact subject phrase to avoid matching a shorter
        # entity embedded inside a more specific subject (for example, Mars
        # inside 'orbit Mars dan Jupiter').
        longest_subject = max(len(subject) for subject, _ in subject_matches)
        selected_subjects = {
            subject for subject, _ in subject_matches if len(subject) == longest_subject
        }
        selected_facts = [
            fact for subject, fact in subject_matches if subject in selected_subjects
        ]
        eligible = []
        seen_ids = set()
        for fact in selected_facts:
            record = fact.get("dataset_record", {})
            predicate = record.get("predicate")
            normalized_predicate = (
                " ".join(predicate.casefold().split())
                if isinstance(predicate, str) else ""
            )
            # Prefer the more specific phrase first; substring matching then
            # naturally includes predicates such as "terletak di antara orbit".
            matches_location = (
                "terletak di antara" in normalized_predicate
                or "terletak di" in normalized_predicate
                or "berada di" in normalized_predicate
            )
            if matches_location and fact.get("id") not in seen_ids:
                eligible.append(fact)
                seen_ids.add(fact.get("id"))

        if not eligible:
            return self._result(
                conclusion="Saya belum memiliki informasi lokasi untuk itu",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=[
                    "Subjek ditemukan, tetapi predicate faktanya tidak termasuk whitelist lokasi P3c.",
                    "Predicate di luar whitelist sengaja tidak dipadankan atau ditafsirkan.",
                ],
                uncertainty="Diperlukan fakta dengan predicate berada di, terletak di, atau terletak di antara.",
            )

        if len(eligible) > 1:
            ids = sorted(str(fact["id"]) for fact in eligible)
            return self._result(
                conclusion="Ada beberapa fakta lokasi yang cocok untuk pertanyaan ini; saya tidak memilih salah satunya.",
                confidence_score=0.0, evidence=ids, reasoning_type="unknown",
                reasons=[
                    "Lebih dari satu fakta memakai predicate lokasi yang diizinkan untuk subjek yang sama.",
                    "Sistem menyebutkan ambiguitas dan tidak menggabungkan atau memilih fakta secara sepihak.",
                ],
                uncertainty="Perjelas lokasi atau hubungan yang dimaksud agar fakta dapat dibedakan.",
            )

        fact = eligible[0]
        provenance = self.knowledge_engine.get_provenance(fact["id"])
        if provenance is None:
            return self._result(
                conclusion="Fakta lokasi ditemukan, tetapi provenance-nya tidak tersedia.",
                confidence_score=0.0, evidence=[fact["id"]], reasoning_type="unknown",
                reasons=["Fakta pendukung tidak memiliki catatan provenance."],
                uncertainty="Lengkapi provenance sebelum menggunakan fakta lokasi.",
            )
        if (
            fact.get("status") != provenance.get("status")
            or fact.get("status") == "conflicting"
        ):
            return self._result(
                conclusion="Status fakta lokasi tidak konsisten atau saling bertentangan; jawaban ditahan.",
                confidence_score=0.0, evidence=[fact["id"]], reasoning_type="conflicting",
                reasons=["Status fakta dan provenance harus konsisten dan tidak conflicting."],
                uncertainty="Periksa kembali fakta dan provenance sebelum menjawab.",
            )

        record = fact["dataset_record"]
        subject = str(record["subject"])
        predicate = str(record["predicate"])
        object_value = record.get("object")
        object_text = (
            ", ".join(str(item) for item in object_value)
            if isinstance(object_value, list) else
            str(object_value).strip() if object_value is not None else ""
        )
        qualifiers = record.get("qualifiers", [])
        location_qualifiers = [
            item.strip() for item in qualifiers
            if isinstance(item, str)
            and any(
                marker in item.casefold()
                for marker in ("berada di", "terletak di")
            )
        ] if isinstance(qualifiers, list) else []
        qualifier_is_distinct_location = bool(
            location_qualifiers
            and object_text
            and not any(
                object_text.casefold() in item.casefold()
                for item in location_qualifiers
            )
        )

        if object_text and not qualifier_is_distinct_location:
            # A populated object is the primary answer. Keep it when an
            # explicit location qualifier merely repeats the same object.
            answer_text = object_text
            sentence = f"{subject} {predicate} {answer_text}."
        elif location_qualifiers:
            # The predicate has already passed the location whitelist. Use a
            # qualifier only when the object is empty or the qualifier states
            # a distinct explicit location not contained in the object.
            answer_text = " ".join(location_qualifiers)
            sentence = answer_text
        else:
            return self._result(
                conclusion="Saya belum memiliki informasi lokasi untuk itu",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=[
                    "Predicate termasuk whitelist lokasi, tetapi object tidak menyediakan lokasi dan tidak ada qualifier yang secara eksplisit menyatakan lokasi."
                ],
                uncertainty="Diperlukan nilai object atau qualifier lokasi yang eksplisit.",
            )
        verified = fact.get("status") == "verified"
        return self._result(
            conclusion=sentence,
            confidence_score=0.72 if verified else 0.48,
            evidence=[fact["id"]],
            reasoning_type="verified_inference" if verified else "hypothetical_inference",
            reasons=[
                f"Pertanyaan lokasi cocok dengan predicate whitelist pada fakta {fact['id']}.",
                (
                    f"Object disalin langsung dari record dataset: {object_text}."
                    if object_text and not qualifier_is_distinct_location else
                    "Qualifier lokasi eksplisit digunakan setelah predicate lolos whitelist karena object kosong atau tidak memuat lokasi tersebut."
                ),
                f"Status fakta: {fact['status']}; sumber: {fact.get('source', 'tidak tercatat')}.",
            ],
            uncertainty=(
                "Fakta dataset berstatus draft/hipotesis dan belum diverifikasi; jawaban bersifat sementara."
                if not verified else
                "Jawaban dibatasi oleh cakupan dan kualifikasi sumber."
            ),
        )

    def _infer_direct_dataset_question(
        self, semantic_result: dict[str, Any],
    ) -> dict[str, Any] | None:
        """Resolve a small, explicit set of direct WH questions from dataset facts.

        This fallback does not alter Semantic output. It uses lexical question
        cues only to select an exact-subject KnowledgeEngine lookup; context is
        never treated as factual evidence.
        """
        text = str(semantic_result.get("original_text", "")).casefold().strip()
        if not text.endswith("?") or "merkurius" not in text:
            return None

        if re.match(r"^(?:apa(?: itu)?|definisi)\b", text):
            if "rotasi" not in text:
                return None
            relation_terms = ["rotasi"]
            if "sideris" in text:
                relation_terms.append("sideris")
            question_kind = "definition"
        elif re.match(r"^berapa(?: lama| hari)?\b", text):
            if "hari" not in text and "lama" not in text:
                return None
            if "mengelilingi" not in text or "matahari" not in text:
                return None
            relation_terms = ["orbit", "mengelilingi", "matahari"]
            question_kind = "quantity"
        else:
            return None

        matches = self.knowledge_engine.search_dataset_facts(
            "merkurius", relation_terms,
        )
        if not matches:
            return self._result(
                conclusion="Saya belum memiliki informasi yang cocok untuk menjawab pertanyaan tentang Merkurius.",
                confidence_score=0.0, evidence=[], reasoning_type="unknown",
                reasons=["Tidak ditemukan fakta dataset dengan subjek dan petunjuk relasi yang diminta."],
                uncertainty="Pertanyaan perlu diperjelas atau fakta yang relevan belum tersedia.",
            )

        def relevance(fact: dict[str, Any]) -> int:
            record = fact.get("dataset_record", {})
            relation = str(record.get("predicate", fact.get("relation", ""))).casefold()
            qualifiers = record.get("qualifiers", [])
            qualifier_text = " ".join(
                item for item in qualifiers if isinstance(item, str)
            ).casefold() if isinstance(qualifiers, list) else ""
            return sum(term in relation for term in relation_terms) + sum(
                term in qualifier_text for term in relation_terms
            )

        best_score = max(relevance(fact) for fact in matches)
        best_matches = [fact for fact in matches if relevance(fact) == best_score]
        if len(best_matches) != 1:
            ids = sorted(fact["id"] for fact in best_matches)
            return self._result(
                conclusion="Ada beberapa fakta yang cocok untuk pertanyaan ini; mohon perjelas apakah yang dimaksud.",
                confidence_score=0.0, evidence=ids, reasoning_type="unknown",
                reasons=[
                    "Lebih dari satu fakta memiliki tingkat kecocokan tertinggi.",
                    "Sistem tidak menggabungkan fakta atau memilih kandidat yang seri secara sewenang-wenang.",
                ],
                uncertainty="Kandidat yang ambigu belum digunakan sebagai dasar jawaban.",
            )

        fact = best_matches[0]
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
                conclusion="Status fakta tidak konsisten atau saling bertentangan; jawaban ditahan.",
                confidence_score=0.0, evidence=[fact["id"]], reasoning_type="conflicting",
                reasons=["Status fakta dan provenance harus konsisten dan tidak conflicting."],
                uncertainty="Periksa kembali fakta dan provenance.",
            )

        record = fact.get("dataset_record", {})
        subject = str(record.get("subject", fact["subject"]))
        predicate = str(record.get("predicate", fact["relation"]))
        object_value = record.get("object", fact["object"])
        object_text = (
            ", ".join(str(item) for item in object_value)
            if isinstance(object_value, list) else str(object_value)
        )
        verified = fact.get("status") == "verified"
        sentence = f"{subject} {predicate} {object_text}."
        if not verified:
            sentence = "Ada kemungkinan bahwa " + sentence
        qualifiers = record.get("qualifiers", [])
        if isinstance(qualifiers, list):
            sentence += " " + " ".join(
                item for item in qualifiers if isinstance(item, str)
            )
        return self._result(
            conclusion=sentence,
            confidence_score=0.72 if verified else 0.48,
            evidence=[fact["id"]],
            reasoning_type="verified_inference" if verified else "hypothetical_inference",
            reasons=[
                f"Pertanyaan {question_kind} cocok dengan fakta dataset {fact['id']}.",
                f"Nilai diambil langsung dari object pada record: {object_text}.",
                f"Status fakta: {fact['status']}; sumber: {fact.get('source', 'tidak tercatat')}.",
            ],
            uncertainty=(
                "Fakta dataset berstatus draft/hipotesis dan belum diverifikasi; jawaban bersifat sementara."
                if not verified else
                "Jawaban dibatasi oleh cakupan dan kualifikasi sumber."
            ),
        )

    def _infer_mercury_followup(
        self,
        semantic_result: dict[str, Any],
        *,
        context_snapshot: dict[str, Any] | None,
    ) -> dict[str, Any] | None:
        """Resolve bounded Mercury follow-ups from a prior session assertion.

        The earlier user statement supplies entity context only. All factual
        values still come from dataset records with matching provenance, and
        draft records remain hypothetical rather than verified.
        """
        current_text = str(semantic_result.get("original_text", "")).casefold()
        if (
            context_snapshot is None
            or not isinstance(context_snapshot.get("turns"), list)
            or "?" not in current_text
            or (semantic_result.get("semantics") or {}).get("Negation", "none") != "none"
        ):
            return None

        prior_actor = None
        for turn in reversed(context_snapshot["turns"]):
            if not isinstance(turn, dict):
                continue
            prior_semantic = turn.get("semantic_result")
            if not isinstance(prior_semantic, dict):
                prior_text = turn.get("user_message")
                if not isinstance(prior_text, str) or not prior_text.strip():
                    continue
                prior_semantic = analyze_semantics(prior_text)
            if prior_semantic.get("status") != "supported":
                continue
            prior_fields = prior_semantic.get("semantics")
            if not isinstance(prior_fields, dict):
                continue
            actor = prior_fields.get("Actor")
            predicate = prior_fields.get("Predicate")
            if (
                prior_fields.get("Intent") == "assertion"
                and isinstance(actor, str)
                and actor.casefold() == "merkurius"
                and isinstance(predicate, str)
                and predicate.casefold() == "berotasi"
            ):
                prior_actor = actor.casefold()
                break
        if prior_actor is None:
            return None

        context_reason = (
            "Pernyataan sebelumnya digunakan hanya untuk mengidentifikasi "
            "Merkurius sebagai topik lanjutan; konteks percakapan bukan bukti faktual."
        )

        if "hari matahari" in current_text:
            rotation_matches = self.knowledge_engine.search_dataset_facts(
                prior_actor, ["rotasi", "sideris"],
            )
            solar_day_matches = []
            for fact in self.knowledge_engine.fact_store.all():
                record = fact.get("dataset_record")
                if not isinstance(record, dict):
                    continue
                subject = record.get("subject")
                qualifiers = record.get("qualifiers", [])
                if (
                    isinstance(subject, str)
                    and prior_actor in subject.casefold()
                    and isinstance(qualifiers, list)
                    and any(
                        isinstance(item, str)
                        and "hari matahari" in item.casefold()
                        and "176 hari bumi" in item.casefold()
                        for item in qualifiers
                    )
                ):
                    solar_day_matches.append(fact)
            if len(rotation_matches) != 1 or len(solar_day_matches) != 1:
                return None
            rotation_fact = rotation_matches[0]
            solar_day_fact = solar_day_matches[0]
            for fact in (rotation_fact, solar_day_fact):
                provenance = self.knowledge_engine.get_provenance(fact["id"])
                if (
                    provenance is None
                    or fact.get("status") != provenance.get("status")
                    or fact.get("status") == "conflicting"
                ):
                    return None
            rotation_record = rotation_fact["dataset_record"]
            solar_record = solar_day_fact["dataset_record"]
            rotation_value = rotation_record.get("object")
            qualifiers = solar_record.get("qualifiers", [])
            solar_qualifier = next(
                item for item in qualifiers
                if isinstance(item, str)
                and "hari matahari" in item.casefold()
                and "176 hari bumi" in item.casefold()
            )
            return self._result(
                conclusion=(
                    "Periode rotasi sideris Merkurius sekitar "
                    f"{rotation_value}, sedangkan {solar_qualifier[0].lower() + solar_qualifier[1:]}"
                ),
                confidence_score=0.48,
                evidence=[rotation_fact["id"], solar_day_fact["id"]],
                reasoning_type="hypothetical_inference",
                reasons=[
                    context_reason,
                    f"Fakta rotasi {rotation_fact['id']} berstatus {rotation_fact['status']}.",
                    f"Pembeda hari Matahari berasal dari kualifikasi fakta {solar_day_fact['id']} "
                    f"yang berstatus {solar_day_fact['status']}.",
                ],
                uncertainty=(
                    "Kedua fakta dataset masih berstatus draft/hipotesis dan belum "
                    "diverifikasi; jawaban bersifat sementara."
                ),
            )

        if re.search(r"\borbit(?:nya)?\b", current_text):
            matches = self.knowledge_engine.search_dataset_facts(
                prior_actor, ["orbit"],
            )
            if len(matches) != 1:
                return None
            fact = matches[0]
            provenance = self.knowledge_engine.get_provenance(fact["id"])
            if (
                provenance is None
                or fact.get("status") != provenance.get("status")
                or fact.get("status") == "conflicting"
            ):
                return None
            record = fact["dataset_record"]
            subject = str(record.get("subject", fact["subject"]))
            predicate = str(record.get("predicate", fact["relation"]))
            object_value = record.get("object", fact["object"])
            if isinstance(object_value, list):
                object_text = ", ".join(str(item) for item in object_value)
            else:
                object_text = str(object_value)
            qualifiers = record.get("qualifiers", [])
            conclusion = f"{subject} {predicate} {object_text}."
            if isinstance(qualifiers, list):
                conclusion += " " + " ".join(
                    item for item in qualifiers if isinstance(item, str)
                )
            verified = fact.get("status") == "verified"
            return self._result(
                conclusion=conclusion,
                confidence_score=0.72 if verified else 0.48,
                evidence=[fact["id"]],
                reasoning_type="verified_inference" if verified else "hypothetical_inference",
                reasons=[
                    context_reason,
                    f"Fakta dataset {fact['id']} ditemukan melalui petunjuk relasi orbit.",
                    f"Status fakta: {fact['status']}; sumber: {fact.get('source', 'tidak tercatat')}.",
                ],
                uncertainty=(
                    "Kesimpulan dibatasi oleh cakupan dan kualifikasi sumber."
                    if verified else
                    "Fakta dataset masih berstatus draft/hipotesis dan belum diverifikasi."
                ),
            )
        return None

    def _infer_concept_fallback(
        self,
        actor: str,
        patient: str,
        *,
        context_note: str | None = None,
    ) -> dict[str, Any]:
        """Map the standalone V3 inference result into the unchanged six-key API."""
        result = self.inference_engine.infer(
            actor,
            patient,
            relation_type="can_burn",
            required_property="mudah_terbakar",
        )
        status = result.status
        if status is ConfidenceLevel.KNOWN:
            confidence_score = 0.72
            reasoning_type = "concept_inference_known"
            conclusion = f"Tahu Pasti: {result.conclusion}"
        elif status is ConfidenceLevel.PARTIAL:
            confidence_score = 0.48
            reasoning_type = "concept_inference_partial"
            conclusion = f"Tahu Sebagian: {result.conclusion}"
        else:
            confidence_score = 0.0
            reasoning_type = "concept_inference_unknown"
            conclusion = f"Tidak Tahu: {result.conclusion}"

        reasons = list(result.reasons)
        reasons.insert(
            0,
            "KnowledgeEngine tidak menemukan fakta persis; jalur fallback Concept Engine V3 dijalankan.",
        )
        if context_note:
            reasons.append(context_note)
        uncertainty = " ".join(result.uncertainty) or (
            "Tidak ada ketidakpastian tambahan yang tercatat."
        )
        return self._result(
            conclusion=conclusion,
            confidence_score=confidence_score,
            evidence=list(result.evidence),
            reasoning_type=reasoning_type,
            reasons=reasons,
            uncertainty=uncertainty,
        )

    def _ensure_dragon_bell_core_facts(self) -> None:
        """Load built-in rule premises on demand without changing default seed counts."""
        if not self.knowledge_engine.seed_core_knowledge:
            return
        existing = {
            (fact["subject"], fact["relation"], fact["object"])
            for fact in self.knowledge_engine.fact_store.all()
        }
        premises = (
            ("naga", "fears", "suara_keras"),
            ("lonceng", "produces", "suara_keras"),
        )
        for subject, relation, object_ in premises:
            if (subject, relation, object_) not in existing:
                self.knowledge_engine.add_fact(
                    subject, relation, object_, "verified", "core_knowledge"
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
