import time
import requests


def check_response_time(url: str):

    try:

        start = time.perf_counter()

        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True
        )

        end = time.perf_counter()

        return {
            "response_time": round((end - start) * 1000, 2),
            "status_code": response.status_code
        }

    except Exception:

        return {
            "response_time": None,
            "status_code": None
        }
