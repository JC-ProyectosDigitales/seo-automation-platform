from time import perf_counter
from typing import Any, Dict

import requests
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 "
        "(compatible; SEOAutomationPlatformContent/2.0)"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,*/*;q=0.8"
    ),
}


def extract_content(
    url: str,
    supplied_content: str | None = None,
    timeout: float = 15.0,
) -> Dict[str, Any]:
    if supplied_content and supplied_content.strip():
        html = supplied_content.strip()
        final_url = url
        status_code = None
        content_type = "text/html"
        response_time_ms = None
        source = "supplied"

    else:
        started_at = perf_counter()

        response = requests.get(
            url,
            timeout=timeout,
            headers=DEFAULT_HEADERS,
            allow_redirects=True,
        )

        response.raise_for_status()

        response_time_ms = round(
            (perf_counter() - started_at) * 1000,
            2,
        )

        html = response.text
        final_url = response.url
        status_code = response.status_code
        content_type = response.headers.get(
            "content-type",
        )
        source = "website"

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    for tag in soup(
        [
            "script",
            "style",
            "noscript",
            "svg",
            "template",
        ]
    ):
        tag.decompose()

    text = soup.get_text(
        separator=" ",
        strip=True,
    )

    text = " ".join(
        text.split()
    )

    return {
        "requested_url": url,
        "final_url": final_url,
        "status_code": status_code,
        "content_type": content_type,
        "response_time_ms": response_time_ms,
        "source": source,
        "html": html,
        "text": text,
    }
