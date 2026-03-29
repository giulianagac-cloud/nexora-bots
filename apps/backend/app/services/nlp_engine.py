"""
NLPEngine — clasificador de intents con TF-IDF + cosine similarity.

Se entrena al instanciar con los ejemplos de intents.json del cliente.
Métodos:
  classify(text) → (intent | None, score float)
  scores(text)   → dict[intent, float]  ← scores crudos por intent
"""
from __future__ import annotations

import unicodedata

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class NLPEngine:
    def __init__(self, intents_data: dict) -> None:
        self._threshold: float = intents_data.get("confidence_threshold", 0.2)

        corpus: list[str] = []
        labels: list[str] = []
        self._intent_to_state: dict[str, str] = {}
        self._intents: list[str] = []

        for intent_def in intents_data.get("intents", []):
            intent_name = intent_def["intent"]
            self._intent_to_state[intent_name] = intent_def["next_state"]
            if intent_name not in self._intents:
                self._intents.append(intent_name)
            for example in intent_def.get("examples", []):
                corpus.append(self._normalize(example))
                labels.append(intent_name)

        self._labels = labels

        self._vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True,
        )
        self._matrix = self._vectorizer.fit_transform(corpus)

    def _normalize(self, text: str) -> str:
        nfd = unicodedata.normalize("NFD", text.lower().strip())
        return "".join(c for c in nfd if not unicodedata.combining(c))

    def scores(self, text: str) -> dict[str, float]:
        """Devuelve el score máximo por intent (sin aplicar threshold)."""
        normalized = self._normalize(text)
        vec = self._vectorizer.transform([normalized])
        raw = cosine_similarity(vec, self._matrix).flatten()

        result: dict[str, float] = {intent: 0.0 for intent in self._intents}
        for idx, score in enumerate(raw):
            intent = self._labels[idx]
            if score > result[intent]:
                result[intent] = float(score)
        return result

    def classify(self, text: str) -> tuple[str | None, float]:
        """
        Devuelve (intent, score).
        Si el score más alto cae bajo el threshold devuelve (None, score).
        """
        intent_scores = self.scores(text)
        if not intent_scores:
            return None, 0.0

        best_intent = max(intent_scores, key=lambda k: intent_scores[k])
        best_score = intent_scores[best_intent]

        if best_score < self._threshold:
            return None, best_score

        return best_intent, best_score

    def state_for_intent(self, intent: str) -> str | None:
        return self._intent_to_state.get(intent)
