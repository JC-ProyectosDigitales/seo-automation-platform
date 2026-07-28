import requests


def check_robots(url: str):

    robots_url = url.rstrip("/") + "/robots.txt"

    try:

        response = requests.get(
            robots_url,
            timeout=5
        )

        if response.status_code == 200:

            content = response.text

            return {
                "exists": True,
                "url": robots_url,
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
