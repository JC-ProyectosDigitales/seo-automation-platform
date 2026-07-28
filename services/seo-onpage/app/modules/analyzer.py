from typing import Any, Dict

from bs4 import BeautifulSoup

from app.modules.canonical import analyze_canonical
from app.modules.headings import analyze_headings
from app.modules.images import analyze_images
from app.modules.issues import build_issues_and_recommendations
from app.modules.links import analyze_links
from app.modules.meta_description import analyze_meta_description
from app.modules.open_graph import analyze_open_graph
from app.modules.page_fetcher import fetch_page
from app.modules.score import calculate_score
from app.modules.title import analyze_title


async def analyze_page(
    website: str,
    keyword: str | None = None,
) -> Dict[str, Any]:
    page = await fetch_page(
        website,
    )

    if not page["success"]:
        return {
            "success": False,
            "score": 0,
            "analysis": {
                "website": website,
                "page": {
                    "requested_url": page["requested_url"],
                    "final_url": page["final_url"],
                    "status_code": page["status_code"],
                    "content_type": page["content_type"],
                },
            },
            "issues": [
                {
                    "type": "error",
                    "code": "PAGE_FETCH_FAILED",
                    "message": (
                        "No fue posible descargar la página para analizarla."
                    ),
                }
            ],
            "recommendations": [
                "Verifica que la URL esté disponible y acepte solicitudes HTTP."
            ],
            "errors": [
                page["error"]
                or "La página devolvió una respuesta HTTP no válida."
            ],
        }

    content_type = page["content_type"] or ""

    if "html" not in content_type:
        return {
            "success": False,
            "score": 0,
            "analysis": {
                "website": website,
                "page": {
                    "requested_url": page["requested_url"],
                    "final_url": page["final_url"],
                    "status_code": page["status_code"],
                    "content_type": content_type,
                },
            },
            "issues": [
                {
                    "type": "error",
                    "code": "INVALID_CONTENT_TYPE",
                    "message": (
                        "La URL no devolvió contenido HTML."
                    ),
                }
            ],
            "recommendations": [
                "Utiliza una URL que apunte a una página HTML."
            ],
            "errors": [],
        }

    soup = BeautifulSoup(
        page["html"],
        "html.parser",
    )

    final_url = page["final_url"] or website

    analysis = {
        "website": website,
        "keyword": keyword,
        "page": {
            "requested_url": page["requested_url"],
            "final_url": final_url,
            "status_code": page["status_code"],
            "content_type": page["content_type"],
        },
        "title": analyze_title(
            soup,
            keyword,
        ),
        "meta_description": analyze_meta_description(
            soup,
            keyword,
        ),
        "headings": analyze_headings(
            soup,
            keyword,
        ),
        "images": analyze_images(
            soup,
        ),
        "links": analyze_links(
            soup,
            final_url,
        ),
        "canonical": analyze_canonical(
            soup,
            final_url,
        ),
        "open_graph": analyze_open_graph(
            soup,
        ),
    }

    score = calculate_score(
        analysis,
    )

    issues, recommendations = (
        build_issues_and_recommendations(
            analysis,
        )
    )

    return {
        "success": True,
        "score": score,
        "analysis": analysis,
        "issues": issues,
        "recommendations": recommendations,
        "errors": [],
    }
