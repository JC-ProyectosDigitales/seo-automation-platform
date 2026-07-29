import requests

from app.modules.http_client import get_http_session


def check_http_status(url: str):
    try:
        with get_http_session() as session:
            response = session.get(
                url,
                timeout=10,
                allow_redirects=True
            )

        return {
            "status_code": response.status_code,
            "success": response.ok,
            "final_url": response.url
        }

    except requests.RequestException as error:
        return {
            "status_code": None,
            "success": False,
            "final_url": None,
            "error": str(error)
        }
