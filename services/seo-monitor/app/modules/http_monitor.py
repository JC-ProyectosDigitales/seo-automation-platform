from time import perf_counter
from typing import Any, Dict, List

import httpx


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; SEOAutomationPlatformMonitor/1.0)"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,*/*;q=0.8"
    ),
}


async def monitor_http(
    url: str,
    timeout: float = 15.0,
) -> Dict[str, Any]:
    started_at = perf_counter()

    try:
        async with httpx.AsyncClient(
            headers=DEFAULT_HEADERS,
            timeout=timeout,
            follow_redirects=True,
        ) as client:
            response = await client.get(url)

        elapsed_ms = round(
            (perf_counter() - started_at) * 1000,
            2,
        )

        redirect_history: List[Dict[str, Any]] = []

        for previous_response in response.history:
            redirect_history.append(
                {
                    "url": str(previous_response.url),
                    "status_code": previous_response.status_code,
                    "location": previous_response.headers.get(
                        "location"
                    ),
                }
            )

        content_length = response.headers.get(
            "content-length"
        )

        return {
            "success": True,
            "available": response.status_code < 500,
            "requested_url": url,
            "final_url": str(response.url),
            "status_code": response.status_code,
            "response_time_ms": elapsed_ms,
            "content_type": response.headers.get(
                "content-type"
            ),
            "content_length": (
                int(content_length)
                if content_length
                and content_length.isdigit()
                else len(response.content)
            ),
            "server": response.headers.get("server"),
            "redirect_count": len(response.history),
            "redirect_history": redirect_history,
            "error": None,
        }

    except httpx.TimeoutException:
        elapsed_ms = round(
            (perf_counter() - started_at) * 1000,
            2,
        )

        return {
            "success": False,
            "available": False,
            "requested_url": url,
            "final_url": None,
            "status_code": None,
            "response_time_ms": elapsed_ms,
            "content_type": None,
            "content_length": None,
            "server": None,
            "redirect_count": 0,
            "redirect_history": [],
            "error": (
                "La solicitud excedió el tiempo límite "
                f"de {timeout} segundos."
            ),
        }

    except httpx.RequestError as error:
        elapsed_ms = round(
            (perf_counter() - started_at) * 1000,
            2,
        )

        return {
            "success": False,
            "available": False,
            "requested_url": url,
            "final_url": None,
            "status_code": None,
            "response_time_ms": elapsed_ms,
            "content_type": None,
            "content_length": None,
            "server": None,
            "redirect_count": 0,
            "redirect_history": [],
            "error": str(error),
        }
