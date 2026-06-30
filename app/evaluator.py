from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from data.reference_answers import REFERENCE_ANSWERS


def _length_fallback_score(answer):
    """
    Used only when a question has no reference answer yet in
    data/reference_answers.py. Keeps the app functional while you
    fill in reference answers incrementally.
    """

    score = 0

    if len(answer) > 20:
        score += 30

    if len(answer) > 50:
        score += 30

    if len(answer) > 100:
        score += 40

    return min(score, 100)


def _semantic_score(answer, reference):
    """
    Scores `answer` against `reference` using TF-IDF cosine similarity,
    blended with a coverage factor so short, low-effort answers can't
    score highly just by repeating a few matching keywords.
    """

    try:
        vectorizer = TfidfVectorizer(stop_words="english")
        vectors = vectorizer.fit_transform([reference, answer])

        # If neither text has any vocabulary left after stop-word
        # removal (e.g. a one or two word answer), fall back safely.
        if vectors.shape[1] == 0:
            raise ValueError("empty vocabulary")

        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]

    except ValueError:
        # TfidfVectorizer raises ValueError on empty vocabulary
        # (e.g. answer is empty, punctuation-only, or all stop words)
        similarity = 0.0

    # Raw TF-IDF cosine similarity tends to sit well below 1.0 even for
    # a genuinely excellent paraphrase (different wording = different
    # vocabulary), so we normalize against a realistic "ceiling" for a
    # strong answer rather than a literal 1.0 match. This keeps strong,
    # differently-worded answers from being unfairly capped low.
    SIMILARITY_CEILING = 0.6
    normalized_similarity = min(similarity / SIMILARITY_CEILING, 1.0)

    # Reward answers that are reasonably thorough relative to the
    # reference, but cap the benefit so padding with filler text
    # doesn't help once you've covered the key points.
    reference_len = max(len(reference.split()), 1)
    answer_len = len(answer.split())
    coverage = min(answer_len / reference_len, 1.0)

    # Weighted blend: semantic similarity matters most, coverage acts
    # as a sanity check against very short/sparse answers.
    raw_score = (normalized_similarity * 0.75 + coverage * 0.25) * 100

    # Small minimum-effort gate: a handful of words shouldn't be able
    # to score highly purely by keyword overlap.
    if answer_len < 5:
        raw_score = min(raw_score, 35)

    return round(min(max(raw_score, 0), 100))


def evaluate_answer(question, answer):

    if len(answer.strip()) == 0:
        return 0

    reference = REFERENCE_ANSWERS.get(question)

    if reference:
        return _semantic_score(answer.strip(), reference)

    # No reference answer written yet for this question — fall back
    # to the simple length heuristic so the app still works.
    return _length_fallback_score(answer)