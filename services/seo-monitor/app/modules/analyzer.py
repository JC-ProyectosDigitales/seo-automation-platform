from typing import Any, Dict

from app.modules.availability import (
    analyze_availability,
)
from app.modules.http_monitor import monitor_http
from app.modules.issues import (
    build_issues_and_recommendations,
)
from app.modules.redirects import analyze_redirects
from app.modules.response_time import (
    analyze_response_time,
)
from app.modules.score import calculate_score
from app.modules.ssl_checker import check_ssl


async def analyze_monitoring(
    website: str,
) -> Dict[str, Any]:
    http_result = await monitor_http(
        website
    )

    ssl_result = await check_ssl(
        http_result.get("final_url")
        or website
    )

    analysis = {
        "website": website,
        "availability": analyze_availability(
            http_result
        ),
        "response_time": analyze_response_time(
            http_result.get(
                "response_time_ms"
            )
        ),
        "redirects": analyze_redirects(
            redirect_count=http_result.get(
                "redirect_count",
                0,
            ),
            redirect_history=http_result.get(
                "redirect_history",
                [],
            ),
            requested_url=http_result.get(
                "requested_url",
                website,
            ),
            final_url=http_result.get(
                "final_url"
            ),
        ),
        "http": {
            "status_code": http_result.get(
                "status_code"
            ),
            "content_type": http_result.get(
                "content_type"
            ),
            "content_length": http_result.get(
                "content_length"
            ),
            "server": http_result.get(
                "server"
            ),
        },
        "ssl": ssl_result,
    }

    score = calculate_score(
        analysis
    )

    issues, recommendations = (
        build_issues_and_recommendations(
            analysis
        )
    )

    errors = []

    if http_result.get("error"):
        errors.append(
            http_result["error"]
        )

    if ssl_result.get("error"):
        errors.append(
            ssl_result["error"]
        )

    success = (
        http_result.get("success", False)
        and analysis["availability"]["available"]
    )

    return {
        "success": success,
        "score": score,
        "analysis": analysis,
        "issues": issues,
        "recommendations": recommendations,
        "errors": errors,
    }
