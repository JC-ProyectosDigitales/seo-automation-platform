from typing import Any, Dict, List, Optional

import httpx

from app.config import (
    PAGESPEED_API_KEY,
    PAGESPEED_API_URL,
    PAGESPEED_STRATEGY,
    PAGESPEED_TIMEOUT,
)


PAGESPEED_CATEGORIES = (
    "performance",
    "accessibility",
    "best-practices",
    "seo",
)


METRIC_AUDITS = {
    "first_contentful_paint": (
        "first-contentful-paint"
    ),
    "largest_contentful_paint": (
        "largest-contentful-paint"
    ),
    "cumulative_layout_shift": (
        "cumulative-layout-shift"
    ),
    "total_blocking_time": (
        "total-blocking-time"
    ),
    "speed_index": "speed-index",
    "interaction_to_next_paint": (
        "interaction-to-next-paint"
    ),
}


def _empty_metric() -> Dict[str, Any]:
    return {
        "score": None,
        "numeric_value": None,
        "numeric_unit": None,
        "display_value": None,
        "rating": "unknown",
    }


def _score_to_percentage(
    score: Any,
) -> Optional[int]:
    if not isinstance(
        score,
        (int, float),
    ):
        return None

    percentage = round(
        float(score) * 100
    )

    return max(
        0,
        min(percentage, 100),
    )


def _metric_rating(
    audit_id: str,
    numeric_value: Any,
) -> str:
    if not isinstance(
        numeric_value,
        (int, float),
    ):
        return "unknown"

    value = float(numeric_value)

    thresholds = {
        "first-contentful-paint": (
            1800,
            3000,
        ),
        "largest-contentful-paint": (
            2500,
            4000,
        ),
        "cumulative-layout-shift": (
            0.1,
            0.25,
        ),
        "total-blocking-time": (
            200,
            600,
        ),
        "speed-index": (
            3400,
            5800,
        ),
        "interaction-to-next-paint": (
            200,
            500,
        ),
    }

    threshold = thresholds.get(
        audit_id
    )

    if threshold is None:
        return "unknown"

    good_limit, poor_limit = threshold

    if value <= good_limit:
        return "good"

    if value <= poor_limit:
        return "needs_improvement"

    return "poor"


def _extract_metric(
    audits: Dict[str, Any],
    audit_id: str,
) -> Dict[str, Any]:
    audit = audits.get(
        audit_id,
        {},
    )

    if not isinstance(
        audit,
        dict,
    ):
        return _empty_metric()

    numeric_value = audit.get(
        "numericValue"
    )

    return {
        "score": _score_to_percentage(
            audit.get("score")
        ),
        "numeric_value": numeric_value,
        "numeric_unit": audit.get(
            "numericUnit"
        ),
        "display_value": audit.get(
            "displayValue"
        ),
        "rating": _metric_rating(
            audit_id,
            numeric_value,
        ),
    }


def _extract_category_score(
    categories: Dict[str, Any],
    category_name: str,
) -> Optional[int]:
    category = categories.get(
        category_name,
        {},
    )

    if not isinstance(
        category,
        dict,
    ):
        return None

    return _score_to_percentage(
        category.get("score")
    )


def _extract_opportunities(
    audits: Dict[str, Any],
) -> List[Dict[str, Any]]:
    opportunities: List[
        Dict[str, Any]
    ] = []

    for audit_id, audit in audits.items():
        if not isinstance(
            audit,
            dict,
        ):
            continue

        details = audit.get(
            "details",
            {},
        )

        if not isinstance(
            details,
            dict,
        ):
            continue

        details_type = details.get(
            "type"
        )

        if details_type != "opportunity":
            continue

        score = audit.get("score")

        if (
            isinstance(score, (int, float))
            and score >= 1
        ):
            continue

        savings_ms = details.get(
            "overallSavingsMs"
        )

        savings_bytes = details.get(
            "overallSavingsBytes"
        )

        opportunities.append(
            {
                "id": audit_id,
                "title": audit.get(
                    "title"
                ),
                "description": audit.get(
                    "description"
                ),
                "display_value": audit.get(
                    "displayValue"
                ),
                "score": (
                    _score_to_percentage(
                        score
                    )
                ),
                "savings_ms": (
                    round(
                        float(savings_ms),
                        2,
                    )
                    if isinstance(
                        savings_ms,
                        (int, float),
                    )
                    else None
                ),
                "savings_bytes": (
                    int(savings_bytes)
                    if isinstance(
                        savings_bytes,
                        (int, float),
                    )
                    else None
                ),
            }
        )

    opportunities.sort(
        key=lambda item: (
            item["savings_ms"] or 0
        ),
        reverse=True,
    )

    return opportunities[:10]


def _extract_diagnostics(
    audits: Dict[str, Any],
) -> Dict[str, Any]:
    diagnostic_ids = {
        "total_byte_weight": (
            "total-byte-weight"
        ),
        "dom_size": "dom-size",
        "main_thread_work": (
            "mainthread-work-breakdown"
        ),
        "bootup_time": (
            "bootup-time"
        ),
        "unused_javascript": (
            "unused-javascript"
        ),
        "unused_css": (
            "unused-css-rules"
        ),
        "render_blocking_resources": (
            "render-blocking-resources"
        ),
        "uses_optimized_images": (
            "uses-optimized-images"
        ),
        "uses_webp_images": (
            "uses-webp-images"
        ),
        "server_response_time": (
            "server-response-time"
        ),
    }

    diagnostics: Dict[
        str,
        Any,
    ] = {}

    for key, audit_id in (
        diagnostic_ids.items()
    ):
        audit = audits.get(
            audit_id,
            {},
        )

        if not isinstance(
            audit,
            dict,
        ):
            diagnostics[key] = None
            continue

        diagnostics[key] = {
            "id": audit_id,
            "title": audit.get(
                "title"
            ),
            "score": (
                _score_to_percentage(
                    audit.get("score")
                )
            ),
            "numeric_value": audit.get(
                "numericValue"
            ),
            "numeric_unit": audit.get(
                "numericUnit"
            ),
            "display_value": audit.get(
                "displayValue"
            ),
        }

    return diagnostics


def _build_error_result(
    code: str,
    message: str,
    *,
    status_code: Optional[int] = None,
    details: Optional[str] = None,
) -> Dict[str, Any]:
    return {
        "available": False,
        "status": "failed",
        "strategy": PAGESPEED_STRATEGY,
        "requested_url": None,
        "final_url": None,
        "fetch_time": None,
        "lighthouse_version": None,
        "scores": {
            "performance": None,
            "accessibility": None,
            "best_practices": None,
            "seo": None,
        },
        "metrics": {
            metric_name: _empty_metric()
            for metric_name in METRIC_AUDITS
        },
        "opportunities": [],
        "diagnostics": {},
        "error": {
            "code": code,
            "message": message,
            "status_code": status_code,
            "details": details,
        },
    }


def _google_error_message(
    payload: Any,
) -> Optional[str]:
    if not isinstance(
        payload,
        dict,
    ):
        return None

    error = payload.get(
        "error"
    )

    if not isinstance(
        error,
        dict,
    ):
        return None

    message = error.get(
        "message"
    )

    if isinstance(
        message,
        str,
    ):
        return message

    return None


async def analyze_pagespeed(
    website: str,
) -> Dict[str, Any]:
    params: List[
        tuple[str, str]
    ] = [
        (
            "url",
            website,
        ),
        (
            "strategy",
            PAGESPEED_STRATEGY,
        ),
        (
            "locale",
            "es",
        ),
    ]

    for category in (
        PAGESPEED_CATEGORIES
    ):
        params.append(
            (
                "category",
                category,
            )
        )

    if PAGESPEED_API_KEY:
        params.append(
            (
                "key",
                PAGESPEED_API_KEY,
            )
        )

    timeout = httpx.Timeout(
        timeout=PAGESPEED_TIMEOUT,
        connect=15.0,
    )

    try:
        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
        ) as client:
            response = await client.get(
                PAGESPEED_API_URL,
                params=params,
            )

    except httpx.TimeoutException:
        return _build_error_result(
            code="PAGESPEED_TIMEOUT",
            message=(
                "PageSpeed Insights excedió "
                "el tiempo máximo de espera."
            ),
        )

    except httpx.RequestError as exc:
        return _build_error_result(
            code="PAGESPEED_REQUEST_FAILED",
            message=(
                "No fue posible conectar con "
                "PageSpeed Insights."
            ),
            details=str(exc),
        )

    try:
        payload = response.json()
    except ValueError:
        return _build_error_result(
            code="PAGESPEED_INVALID_RESPONSE",
            message=(
                "PageSpeed Insights devolvió "
                "una respuesta no válida."
            ),
            status_code=response.status_code,
        )

    if response.status_code >= 400:
        return _build_error_result(
            code="PAGESPEED_HTTP_ERROR",
            message=(
                _google_error_message(payload)
                or (
                    "PageSpeed Insights devolvió "
                    "un error HTTP."
                )
            ),
            status_code=response.status_code,
        )

    if not isinstance(
        payload,
        dict,
    ):
        return _build_error_result(
            code="PAGESPEED_INVALID_PAYLOAD",
            message=(
                "La respuesta de PageSpeed "
                "no tiene el formato esperado."
            ),
            status_code=response.status_code,
        )

    lighthouse = payload.get(
        "lighthouseResult"
    )

    if not isinstance(
        lighthouse,
        dict,
    ):
        return _build_error_result(
            code="PAGESPEED_LIGHTHOUSE_MISSING",
            message=(
                "La respuesta no contiene "
                "resultados de Lighthouse."
            ),
            status_code=response.status_code,
        )

    categories = lighthouse.get(
        "categories",
        {},
    )

    audits = lighthouse.get(
        "audits",
        {},
    )

    if not isinstance(
        categories,
        dict,
    ):
        categories = {}

    if not isinstance(
        audits,
        dict,
    ):
        audits = {}

    scores = {
        "performance": (
            _extract_category_score(
                categories,
                "performance",
            )
        ),
        "accessibility": (
            _extract_category_score(
                categories,
                "accessibility",
            )
        ),
        "best_practices": (
            _extract_category_score(
                categories,
                "best-practices",
            )
        ),
        "seo": (
            _extract_category_score(
                categories,
                "seo",
            )
        ),
    }

    metrics = {
        metric_name: _extract_metric(
            audits,
            audit_id,
        )
        for (
            metric_name,
            audit_id,
        ) in METRIC_AUDITS.items()
    }

    runtime_error = lighthouse.get(
        "runtimeError"
    )

    if isinstance(
        runtime_error,
        dict,
    ):
        runtime_code = runtime_error.get(
            "code"
        )

        if runtime_code:
            return _build_error_result(
                code=(
                    "PAGESPEED_"
                    f"{runtime_code}"
                ),
                message=(
                    runtime_error.get(
                        "message"
                    )
                    or (
                        "Lighthouse no pudo "
                        "completar el análisis."
                    )
                ),
                status_code=response.status_code,
            )

    return {
        "available": True,
        "status": "completed",
        "strategy": PAGESPEED_STRATEGY,
        "requested_url": website,
        "final_url": lighthouse.get(
            "finalDisplayedUrl"
        )
        or lighthouse.get(
            "finalUrl"
        ),
        "fetch_time": lighthouse.get(
            "fetchTime"
        ),
        "lighthouse_version": (
            lighthouse.get(
                "lighthouseVersion"
            )
        ),
        "scores": scores,
        "metrics": metrics,
        "opportunities": (
            _extract_opportunities(
                audits
            )
        ),
        "diagnostics": (
            _extract_diagnostics(
                audits
            )
        ),
        "error": None,
    }
