"""
NLPEngine — clasificador de intents con TF-IDF + cosine similarity.

Se entrena al instanciar con los ejemplos de intents.json del cliente.
Método principal: classify(text) → (intent | None, score float)
"""
from __future__ import annotations

import unicodedata

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class NLPEngine:
    def __init__(self, intents_data: dict) -> None:
        self._threshold: float = intents_data.get("confidence_threshold", 0.2)

        # Construimos dos listas paralelas: corpus de ejemplos e intent al que pertenecen.
        corpus: list[str] = []
        labels: list[str] = []
        self._intent_to_state: dict[str, str] = {}

        for intent_def in intents_data.get("intents", []):
            intent_name = intent_def["intent"]
            self._intent_to_state[intent_name] = intent_def["next_state"]
            for example in intent_def.get("examples", []):
                corpus.append(self._normalize(example))
                labels.append(intent_name)

        self._labels = labels

        # TF-IDF con bi-gramas para capturar frases cortas.
        self._vectorizer = TfidfVectorizer(
            analyzer="word",
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True,
        )
        self._matrix = self._vectorizer.fit_transform(corpus)

    # ------------------------------------------------------------------
    def _normalize(self, text: str) -> str:
        """Minúsculas + strip de acentos."""
        nfd = unicodedata.normalize("NFD", text.lower().strip())
        return "".join(c for c in nfd if not unicodedata.combining(c))

    def classify(self, text: str) -> tuple[str | None, float]:
        """
        Devuelve (intent, score).
        Si el score más alto cae bajo el threshold devuelve (None, score).
        """
        normalized = self._normalize(text)
        vec = self._vectorizer.transform([normalized])
        scores = cosine_similarity(vec, self._matrix).flatten()

        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])

        if best_score < self._threshold:
            return None, best_score

        return self._labels[best_idx], best_score

    def state_for_intent(self, intent: str) -> str | None:
        return self._intent_to_state.get(intent)
