import xml.etree.ElementTree as ET
from urllib.parse import urljoin, urlparse

import requests

from app.modules.http_client import get_http_session


def parse_sitemap(response: requests.Response, sitemap_url: str):
    try:
        root = ET.fromstring(response.content)
        root_tag = root.tag.split("}")[-1].lower()

        if root_tag == "urlset":
            urls = [
                element
                for element in root.iter()
                if element.tag.split("}")[-1].lower() == "url"
            ]

            return {
                "exists": True,
                "url": response.url,
                "type": "urlset",
                "valid_xml": True,
                "url_count": len(urls),
                "sitemap_count": 0,
                "status_code": response.status_code
            }

        if root_tag == "sitemapindex":
            sitemaps = [
                element
                for element in root.iter()
                if element.tag.split("}")[-1].lower() == "sitemap"
            ]

            return {
                "exists": True,
                "url": response.url,
                "type": "sitemap_index",
                "valid_xml": True,
                "url_count": 0,
                "sitemap_count": len(sitemaps),
                "status_code": response.status_code
            }

        return {
            "exists": True,
            "url": response.url,
            "type": "unknown",
            "valid_xml": True,
            "url_count": 0,
            "sitemap_count": 0,
            "status_code": response.status_code
        }

    except ET.ParseError:
        return {
            "exists": True,
            "url": sitemap_url,
            "type": None,
            "valid_xml": False,
            "url_count": 0,
            "sitemap_count": 0,
            "status_code": response.status_code
        }


def check_sitemap(url: str):
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"

    sitemap_candidates = [
        urljoin(base_url, "/sitemap.xml"),
        urljoin(base_url, "/sitemap_index.xml"),
        urljoin(base_url, "/wp-sitemap.xml")
    ]

    last_status_code = None

    try:
        with get_http_session() as session:
            for sitemap_url in sitemap_candidates:
                response = session.get(
                    sitemap_url,
                    timeout=10,
                    allow_redirects=True
                )

                last_status_code = response.status_code

                if response.status_code != 200:
                    continue

                content_type = response.headers.get(
                    "Content-Type",
                    ""
                ).lower()

                content_start = response.text.lstrip()[:100].lower()

                looks_like_xml = (
                    "xml" in content_type
                    or content_start.startswith("<?xml")
                    or "<urlset" in content_start
                    or "<sitemapindex" in content_start
                )

                if not looks_like_xml:
                    continue

                return parse_sitemap(
                    response,
                    sitemap_url
                )

        return {
            "exists": False,
            "url": sitemap_candidates[0],
            "checked_urls": sitemap_candidates,
            "type": None,
            "valid_xml": False,
            "url_count": 0,
            "sitemap_count": 0,
            "status_code": last_status_code
        }

    except requests.RequestException as error:
        return {
            "exists": False,
            "url": sitemap_candidates[0],
            "checked_urls": sitemap_candidates,
            "type": None,
            "valid_xml": False,
            "url_count": 0,
            "sitemap_count": 0,
            "status_code": None,
            "error": str(error)
        }
