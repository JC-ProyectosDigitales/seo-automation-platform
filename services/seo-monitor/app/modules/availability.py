from typing import Any, Dict


def analyze_availability(
    http_result: Dict[str, Any],
) -> Dict[str, Any]:
    status_code = http_result.get(
        "status_code"
    )

    available = http_result.get(
        "available",
        False,
    )

    status = "unavailable"

    if available:
        if status_code and 200 <= status_code < 300:
            status = "available"

        elif status_code and 300 <= status_code < 400:
            status = "redirected"

        elif status_code and 400 <= status_code < 500:
            status = "client_error"

        elif status_code and status_code >= 500:
            status = "server_error"

    return {
        "available": available,
        "status": status,
        "status_code": status_code,
        "requested_url": http_result.get(
            "requested_url"
        ),
        "final_url": http_result.get(
            "final_url"
        ),
    }
