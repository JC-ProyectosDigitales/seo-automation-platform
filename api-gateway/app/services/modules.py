import os


MODULES = {

    "seo-content": os.getenv(
        "SEO_CONTENT_URL"
    ),

    "seo-onpage": os.getenv(
        "SEO_ONPAGE_URL"
    ),

    "seo-technical": os.getenv(
        "SEO_TECHNICAL_URL"
    )
}