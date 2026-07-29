import requests
from bs4 import BeautifulSoup

from app.modules.http_client import get_http_session


def check_meta_robots(url: str):
    try:
        with get_http_session() as session:
            response = session.get(
                url,
                timeout=10,
                allow_redirects=True
            )

        if response.status_code != 200:
            return {
                "exists": False,
                "content": None,
                "index": None,
                "follow": None,
                "status_code": response.status_code
            }

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        meta = soup.find(
            "meta",
            attrs={
                "name": lambda value: (
                    value
                    and value.strip().lower() == "robots"
                )
            }
        )

        if not meta:
            return {
                "exists": False,
                "content": None,
                "index": None,
                "follow": None,
                "status_code": response.status_code
            }

        content = meta.get(
            "content",
            ""
        ).strip().lower()

        directives = {
            directive.strip()
            for directive in content.split(",")
            if directive.strip()
        }

        return {
            "exists": True,
            "content": content,
            "index": "noindex" not in directives,
            "follow": "nofollow" not in directives,
            "status_code": response.status_code
        }

    except requests.RequestException as error:
        return {
            "exists": False,
            "content": None,
            "index": None,
            "follow": None,
            "status_code": None,
            "error": str(error)
        }
