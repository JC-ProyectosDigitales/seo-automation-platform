from app.modules.https_checker import check_https
from app.modules.http_status import check_http_status
from app.modules.response_time import check_response_time
from app.modules.robots import check_robots
from app.modules.sitemap import check_sitemap
from app.modules.redirect import check_redirect
from app.modules.canonical import check_canonical
from app.modules.meta_robots import check_meta_robots
from app.modules.score import calculate_score
from app.modules.issues import generate_issues


def analyze_site(url: str):

    https = check_https(url)

    http_status = check_http_status(url)

    response_time = check_response_time(url)

    robots = check_robots(url)

    sitemap = check_sitemap(url)

    redirect = check_redirect(url)

    canonical = check_canonical(url)

    meta_robots = check_meta_robots(url)

    score, recommendations = calculate_score(
        https,
        http_status,
        response_time,
        robots,
        sitemap,
        redirect,
        canonical,
        meta_robots
    )

    result = {
        "url": url,
        "https": https,
        "http_status": http_status,
        "response_time": response_time,
        "robots": robots,
        "sitemap": sitemap,
        "redirect": redirect,
        "canonical": canonical,
        "meta_robots": meta_robots,
        "score": score,
        "recommendations": recommendations
    }

    result["issues"] = generate_issues(result)

    return result
