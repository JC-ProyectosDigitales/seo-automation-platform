from typing import Any, Dict

import httpx


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; SEOAutomationPlatform/1.0; "
        "+https://example.com)"
    ),
    "Accept": "text/html,application/xhtml+xml",
}


async def fetch_page(
    url: str,
    timeout: float = 15.0,
) -> Dict[str, Any]:
    try:
        async with httpx.AsyncClient(
            follow_redirects=True,
            timeout=timeout,
            headers=DEFAULT_HEADERS,
        ) as client:
            response = await client.get(url)

        content_type = response.headers.get(
            "content-type",
            "",
        ).lower()

        return {
            "success": response.status_code < 400,
            "requested_url": url,
            "final_url": str(response.url),
            "status_code": response.status_code,
            "content_type": content_type,
            "html": response.text,
            "error": None,
        }

    except httpx.TimeoutException:
        return {
            "success": False,
            "requested_url": url,
            "final_url": None,
            "status_code": None,
            "content_type": None,
            "html": "",
            "error": "La solicitud excedió el tiempo límite.",
        }

    except httpx.RequestError as error:
        return {
            "success": False,
            "requested_url": url,
            "final_url": None,
            "status_code": None,
            "content_type": None,
            "html": "",
            "error": str(error),
        }
