import textstat

def analyze_readability(content):

    reading_score = textstat.flesch_reading_ease(content)

    sentence_count = textstat.sentence_count(content)

    word_count = textstat.lexicon_count(content)

    avg_sentence_length = 0

    if sentence_count > 0:
        avg_sentence_length = round(word_count / sentence_count, 2)

    recommendations = []

    # Evaluación SEO conversacional
    if reading_score >= 80:
        recommendations.append("El contenido es muy fácil de leer.")
    elif reading_score >= 60:
        recommendations.append("La legibilidad del contenido es adecuada.")
    elif reading_score >= 40:
        recommendations.append("El contenido es algo difícil de leer.")
    else:
        recommendations.append("El contenido es difícil de leer para usuarios generales.")

    if avg_sentence_length > 25:
        recommendations.append("Las oraciones son demasiado largas.")
    else:
        recommendations.append("La longitud de oraciones es adecuada.")

    return {
        "reading_score": round(reading_score, 2),
        "sentence_count": sentence_count,
        "word_count": word_count,
        "avg_sentence_length": avg_sentence_length,
        "recommendations": recommendations
    }