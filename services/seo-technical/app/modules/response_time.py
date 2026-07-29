import time

import requests

from app.modules.http_client import get_http_session


def check_response_time(url: str):
    try:
        start = time.perf_counter()

        with get_http_session() as session:
            response = session.get(
                url,
                timeout=10,
                allow_redirects=True
            )

        end = time.perf_counter()

        return {
            "response_time": round((end - start) * 1000, 2),
            "status_code": response.status_code,
            "final_url": response.url
        }

    except requests.RequestException as error:
        return {
            "response_time": None,
            "status_code": None,
            "final_url": None,
            "error": str(error)
        }
