from urllib.parse import urlparse


def check_https(url: str):

    parsed = urlparse(url)

    return {
        "protocol": parsed.scheme,
        "secure": parsed.scheme == "https"
    }
