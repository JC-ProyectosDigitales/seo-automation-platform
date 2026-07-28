import requests
from bs4 import BeautifulSoup


def check_meta_robots(url: str):

    try:

        response = requests.get(
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
                    and value.lower() == "robots"
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
        ).lower()

        return {
            "exists": True,
            "content": content,
            "index": "noindex" not in content,
            "follow": "nofollow" not in content,
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
