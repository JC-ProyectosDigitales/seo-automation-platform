from typing import Any, Dict, List

import textstat


def analyze_readability(
    content: str,
) -> Dict[str, Any]:
    reading_score = textstat.flesch_reading_ease(
        content
    )

    sentence_count = textstat.sentence_count(
        content
    )

    word_count = textstat.lexicon_count(
        content,
        removepunct=True,
    )

    character_count = len(
        content
    )

    avg_sentence_length = 0.0

    if sentence_count > 0:
        avg_sentence_length = round(
            word_count / sentence_count,
            2,
        )

    recommendations: List[str] = []

    if word_count < 300:
        recommendations.append(
            "El contenido es corto; considera desarrollarlo con más información útil."
        )

    if reading_score >= 80:
        rating = "very_easy"

    elif reading_score >= 60:
        rating = "easy"

    elif reading_score >= 40:
        rating = "moderate"
        recommendations.append(
            "Simplifica algunas oraciones para mejorar la lectura."
        )

    else:
        rating = "difficult"
        recommendations.append(
            "Reduce la complejidad del contenido y utiliza frases más directas."
        )

    if avg_sentence_length > 25:
        recommendations.append(
            "Reduce la longitud promedio de las oraciones."
        )

    return {
        "reading_score": round(
            reading_score,
            2,
        ),
        "rating": rating,
        "sentence_count": sentence_count,
        "word_count": word_count,
        "character_count": character_count,
        "avg_sentence_length": avg_sentence_length,
        "recommendations": recommendations,
    }
