from urllib.parse import urlparse

import requests

from app.modules.http_client import get_http_session


def check_redirect(url: str):
    parsed = urlparse(url)

    protocol = parsed.scheme or "https"
    host = parsed.netloc or parsed.path

    clean_host = host.removeprefix("www.")

    www_url = f"{protocol}://www.{clean_host}"
    non_www_url = f"{protocol}://{clean_host}"

    result = {
        "www_url": www_url,
        "www_status": None,
        "www_redirect": None,
        "non_www_url": non_www_url,
        "non_www_status": None,
        "non_www_redirect": None
    }

    with get_http_session() as session:
        try:
            response = session.get(
                www_url,
                allow_redirects=False,
                timeout=10
            )

            result["www_status"] = response.status_code
            result["www_redirect"] = response.headers.get("Location")

        except requests.RequestException as error:
            result["www_error"] = str(error)

        try:
            response = session.get(
                non_www_url,
                allow_redirects=False,
                timeout=10
            )

            result["non_www_status"] = response.status_code
            result["non_www_redirect"] = response.headers.get("Location")

        except requests.RequestException as error:
            result["non_www_error"] = str(error)

    return result
