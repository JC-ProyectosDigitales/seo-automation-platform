import requests
from bs4 import BeautifulSoup


def extract_content(url):

    response = requests.get(
        url,
        timeout=15,
        headers={
            "User-Agent": "SEO-Optimizer/1.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()

    text = soup.get_text(separator=" ")

    text = " ".join(text.split())

    return text