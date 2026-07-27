def calculate_seo_score(
    seo_result,
    heading_result,
    readability_result
):

    score = 0

    density = seo_result["density"]

    if 1 <= density <= 3:
        score += 40
    elif density > 0:
        score += 20

    if heading_result["h1_count"] == 1:
        score += 20

    if heading_result["h2_count"] > 0:
        score += 20

    if readability_result["reading_score"] >= 60:
        score += 20

    return score