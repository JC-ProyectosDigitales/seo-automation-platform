import requests
from bs4 import BeautifulSoup


def check_canonical(url: str):

    try:

        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True
        )

        if response.status_code != 200:

            return {
                "exists": False,
                "href": None,
                "status_code": response.status_code
            }

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        canonical = soup.find(
            "link",
            rel=lambda value: value and "canonical" in value
        )

        if canonical:

            return {
                "exists": True,
                "href": canonical.get("href"),
                "status_code": response.status_code
            }

        return {
            "exists": False,
            "href": None,
            "status_code": response.status_code
        }

    except requests.RequestException as error:

        return {
            "exists": False,
            "href": None,
            "status_code": None,
            "error": str(error)
        }
