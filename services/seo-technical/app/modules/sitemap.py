import xml.etree.ElementTree as ET

import requests


def check_sitemap(url: str):

    sitemap_url = url.rstrip("/") + "/sitemap.xml"

    try:

        response = requests.get(
            sitemap_url,
            timeout=5
        )

        if response.status_code != 200:

            return {
                "exists": False,
                "url": sitemap_url,
                "type": None,
                "valid_xml": False,
                "url_count": 0,
                "sitemap_count": 0,
                "status_code": response.status_code
            }

        try:

            root = ET.fromstring(response.content)

            root_tag = root.tag.split("}")[-1]

            namespace = {
                "sm": "http://www.sitemaps.org/schemas/sitemap/0.9"
            }

            if root_tag == "urlset":

                urls = root.findall("sm:url", namespace)

                return {
                    "exists": True,
                    "url": sitemap_url,
                    "type": "urlset",
                    "valid_xml": True,
                    "url_count": len(urls),
                    "sitemap_count": 0,
                    "status_code": response.status_code
                }

            if root_tag == "sitemapindex":

                sitemaps = root.findall("sm:sitemap", namespace)

                return {
                    "exists": True,
                    "url": sitemap_url,
                    "type": "sitemap_index",
                    "valid_xml": True,
                    "url_count": 0,
                    "sitemap_count": len(sitemaps),
                    "status_code": response.status_code
                }

            return {
                "exists": True,
                "url": sitemap_url,
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

    except requests.RequestException as error:

        return {
            "exists": False,
            "url": sitemap_url,
            "type": None,
            "valid_xml": False,
            "url_count": 0,
            "sitemap_count": 0,
            "status_code": None,
            "error": str(error)
        }
