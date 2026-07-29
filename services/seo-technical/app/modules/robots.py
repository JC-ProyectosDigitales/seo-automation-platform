from urllib.parse import urljoin, urlparse

import requests

from app.modules.http_client import get_http_session


def check_robots(url: str):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    robots_url = urljoin(base_url, "/robots.txt")

    try:
        with get_http_session() as session:
            response = session.get(
                robots_url,
                timeout=10,
                allow_redirects=True
            )

        if response.status_code == 200:
            content = response.text

            return {
                "exists": True,
                "url": response.url,
                "has_sitemap": "sitemap:" in content.lower(),
                "has_user_agent": "user-agent:" in content.lower(),
                "status_code": response.status_code
            }

        return {
            "exists": False,
            "url": robots_url,
            "has_sitemap": False,
            "has_user_agent": False,
            "status_code": response.status_code
        }

    except requests.RequestException as error:
        return {
            "exists": False,
            "url": robots_url,
            "has_sitemap": False,
            "has_user_agent": False,
            "status_code": None,
            "error": str(error)
        }
