import requests


def check_http_status(url: str):

    try:

        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True
        )

        return {
            "status_code": response.status_code,
            "success": response.ok
        }

    except Exception:

        return {
            "status_code": None,
            "success": False
        }
