"""Notes processing and summarization utilities.

This module uses basic NLP techniques (via NLTK) to summarize notes and extract
key points. It is intentionally simple and designed for educational usage.
"""

from __future__ import annotations

import heapq
import re
from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


# Ensure required NLTK data is downloaded at least once.
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


def _clean_text(text: str) -> str:
    """Basic text cleanup (remove extra whitespace)."""

    return re.sub(r"\s+", " ", text.strip())


def summarize_notes(text: str, max_sentences: int = 3) -> str:
    """Return a short summary containing the most important sentences."""

    text = _clean_text(text)
    if not text:
        return ""

    sentences = sent_tokenize(text)
    if len(sentences) <= max_sentences:
        return text

    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))

    word_frequencies = {}
    for word in words:
        if word.isalpha() and word not in stop_words:
            word_frequencies[word] = word_frequencies.get(word, 0) + 1

    if not word_frequencies:
        return " " .join(sentences[:max_sentences])

    max_freq = max(word_frequencies.values())
    for word in word_frequencies:
        word_frequencies[word] /= max_freq

    sentence_scores = {}
    for sentence in sentences:
        sentence_words = word_tokenize(sentence.lower())
        for word in sentence_words:
            if word in word_frequencies:
                sentence_scores[sentence] = sentence_scores.get(sentence, 0) + word_frequencies[word]

    best_sentences = heapq.nlargest(max_sentences, sentence_scores, key=sentence_scores.get)
    return " ".join(best_sentences)


def extract_key_points(text: str, max_points: int = 5) -> List[str]:
    """Extract key points (most frequent terms) from notes."""

    text = _clean_text(text)
    if not text:
        return []

    words = word_tokenize(text.lower())
    stop_words = set(stopwords.words("english"))

    freq = {}
    for word in words:
        if word.isalpha() and word not in stop_words:
            freq[word] = freq.get(word, 0) + 1

    most_common = heapq.nlargest(max_points, freq.items(), key=lambda kv: kv[1])
    return [word for word, _ in most_common]
