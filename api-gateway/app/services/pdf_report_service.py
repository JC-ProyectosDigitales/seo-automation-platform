from io import BytesIO
from typing import Any, Dict, Iterable, List
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
    ParagraphStyle,
    getSampleStyleSheet,
)
from reportlab.lib.units import mm
from reportlab.platypus import (
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


PAGE_WIDTH, PAGE_HEIGHT = A4


BACKGROUND = colors.HexColor("#0F172A")
DARK = colors.HexColor("#020617")
CARD = colors.HexColor("#1E293B")
BORDER = colors.HexColor("#CBD5E1")
PRIMARY = colors.HexColor("#2563EB")
TEXT = colors.HexColor("#0F172A")
SECONDARY_TEXT = colors.HexColor("#475569")
LIGHT_BACKGROUND = colors.HexColor("#F8FAFC")
SUCCESS = colors.HexColor("#16A34A")
WARNING = colors.HexColor("#CA8A04")
ERROR = colors.HexColor("#DC2626")
INFO = colors.HexColor("#0891B2")


MODULE_NAMES = {
    "seo-content": "SEO Content",
    "seo-onpage": "SEO On-Page",
    "seo-technical": "SEO Technical",
    "seo-monitor": "SEO Monitor",
}


def safe_text(value: Any) -> str:
    if value is None:
        return "No disponible"

    if isinstance(value, bool):
        return "Sí" if value else "No"

    text = str(value)

    return (
        text.replace("\u00a0", " ")
        .replace("\u2013", "-")
        .replace("\u2014", "-")
        .strip()
    )


def paragraph_text(value: Any) -> str:
    return escape(safe_text(value))


def format_number(
    value: Any,
    decimals: int = 2,
) -> str:
    if not isinstance(value, (int, float)):
        return safe_text(value)

    if isinstance(value, int):
        return f"{value:,}".replace(",", " ")

    return (
        f"{value:,.{decimals}f}"
        .replace(",", " ")
    )


def format_percent(value: Any) -> str:
    if not isinstance(value, (int, float)):
        return safe_text(value)

    percentage = value

    if 0 <= value <= 1:
        percentage = value * 100

    return f"{percentage:.2f} %"


def format_datetime(value: Any) -> str:
    if value is None:
        return "No disponible"

    if hasattr(value, "strftime"):
        return value.strftime(
            "%d/%m/%Y %H:%M:%S"
        )

    text = safe_text(value)

    return (
        text.replace("T", " ")
        .replace("+00:00", " UTC")
    )


def get_result(
    wrapper: Any,
) -> Dict[str, Any]:
    if not isinstance(wrapper, dict):
        return {}

    result = wrapper.get("result")

    if isinstance(result, dict):
        return result

    return wrapper


def get_styles() -> Dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=sample["Title"],
            fontName="Helvetica-Bold",
            fontSize=21,
            leading=25,
            textColor=colors.white,
            alignment=TA_LEFT,
            spaceAfter=6,
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#CBD5E1"),
        ),
        "section": ParagraphStyle(
            "ReportSection",
            parent=sample["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=14,
            leading=18,
            textColor=TEXT,
            spaceBefore=8,
            spaceAfter=9,
        ),
        "subsection": ParagraphStyle(
            "ReportSubsection",
            parent=sample["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=TEXT,
            spaceBefore=6,
            spaceAfter=6,
        ),
        "normal": ParagraphStyle(
            "ReportNormal",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=12,
            textColor=TEXT,
        ),
        "small": ParagraphStyle(
            "ReportSmall",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=7.5,
            leading=10,
            textColor=SECONDARY_TEXT,
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8,
            leading=10,
            textColor=colors.white,
            alignment=TA_LEFT,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=7.8,
            leading=10,
            textColor=TEXT,
        ),
        "score": ParagraphStyle(
            "Score",
            parent=sample["Normal"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=24,
            textColor=PRIMARY,
            alignment=TA_CENTER,
        ),
        "center": ParagraphStyle(
            "Center",
            parent=sample["Normal"],
            fontName="Helvetica",
            fontSize=8,
            leading=10,
            textColor=TEXT,
            alignment=TA_CENTER,
        ),
    }


def create_table(
    rows: Iterable[Iterable[Any]],
    styles: Dict[str, ParagraphStyle],
    *,
    widths: List[float] | None = None,
    header: bool = False,
) -> Table:
    processed_rows = []

    for row_index, row in enumerate(rows):
        processed_row = []

        for cell in row:
            style = (
                styles["table_header"]
                if header and row_index == 0
                else styles["table_cell"]
            )

            if isinstance(cell, Paragraph):
                processed_row.append(cell)
            else:
                processed_row.append(
                    Paragraph(
                        paragraph_text(cell),
                        style,
                    )
                )

        processed_rows.append(processed_row)

    table = Table(
        processed_rows,
        colWidths=widths,
        repeatRows=1 if header else 0,
        hAlign="LEFT",
    )

    table_style = [
        (
            "VALIGN",
            (0, 0),
            (-1, -1),
            "TOP",
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.4,
            BORDER,
        ),
        (
            "LEFTPADDING",
            (0, 0),
            (-1, -1),
            7,
        ),
        (
            "RIGHTPADDING",
            (0, 0),
            (-1, -1),
            7,
        ),
        (
            "TOPPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
        (
            "BOTTOMPADDING",
            (0, 0),
            (-1, -1),
            6,
        ),
        (
            "BACKGROUND",
            (0, 0),
            (-1, -1),
            LIGHT_BACKGROUND,
        ),
    ]

    if header:
        table_style.extend(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    BACKGROUND,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
            ]
        )

    table.setStyle(
        TableStyle(table_style)
    )

    return table


def calculate_overall_score(
    results: Dict[str, Any],
) -> int | None:
    scores = []

    for wrapper in results.values():
        result = get_result(wrapper)
        score = result.get("score")

        if isinstance(score, (int, float)):
            scores.append(float(score))

    if not scores:
        return None

    return round(
        sum(scores) / len(scores)
    )


def build_summary_section(
    audit: Any,
    results: Dict[str, Any],
    styles: Dict[str, ParagraphStyle],
) -> List[Any]:
    overall_score = calculate_overall_score(
        results
    )

    score_text = (
        str(overall_score)
        if overall_score is not None
        else "-"
    )

    summary = Table(
        [
            [
                Paragraph(
                    score_text,
                    styles["score"],
                ),
                Paragraph(
                    "<b>Score general</b><br/>"
                    "Promedio de los módulos ejecutados.",
                    styles["normal"],
                ),
            ]
        ],
        colWidths=[
            35 * mm,
            125 * mm,
        ],
    )

    summary.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    colors.HexColor("#EFF6FF"),
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.8,
                    colors.HexColor("#93C5FD"),
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
            ]
        )
    )

    details = create_table(
        [
            ["Dato", "Valor"],
            ["ID de auditoría", audit.audit_id],
            ["Sitio web", audit.website],
            ["Keyword", audit.keyword],
            ["Estado", audit.status],
            [
                "Fecha de creación",
                format_datetime(audit.created_at),
            ],
            [
                "Inicio",
                format_datetime(audit.started_at),
            ],
            [
                "Finalización",
                format_datetime(audit.completed_at),
            ],
            [
                "Tiempo de ejecución",
                (
                    f"{audit.execution_time:.2f} s"
                    if isinstance(
                        audit.execution_time,
                        (int, float),
                    )
                    else "No disponible"
                ),
            ],
        ],
        styles,
        widths=[
            48 * mm,
            112 * mm,
        ],
        header=True,
    )

    return [
        Paragraph(
            "Resumen de la auditoría",
            styles["section"],
        ),
        summary,
        Spacer(1, 5 * mm),
        details,
    ]


def build_module_summary(
    results: Dict[str, Any],
    styles: Dict[str, ParagraphStyle],
) -> List[Any]:
    rows = [
        [
            "Módulo",
            "Estado",
            "Score",
            "Problemas",
            "Recomendaciones",
        ]
    ]

    ordered_modules = sorted(
        results.items(),
        key=lambda item: (
            item[1].get("priority", 999)
            if isinstance(item[1], dict)
            else 999
        ),
    )

    for module_name, wrapper in ordered_modules:
        result = get_result(wrapper)

        rows.append(
            [
                MODULE_NAMES.get(
                    module_name,
                    module_name,
                ),
                result.get(
                    "status",
                    "No disponible",
                ),
                result.get(
                    "score",
                    "No disponible",
                ),
                len(
                    result.get("issues", [])
                    if isinstance(
                        result.get("issues"),
                        list,
                    )
                    else []
                ),
                len(
                    result.get(
                        "recommendations",
                        [],
                    )
                    if isinstance(
                        result.get(
                            "recommendations"
                        ),
                        list,
                    )
                    else []
                ),
            ]
        )

    return [
        Paragraph(
            "Resultados por módulo",
            styles["section"],
        ),
        create_table(
            rows,
            styles,
            widths=[
                48 * mm,
                28 * mm,
                20 * mm,
                30 * mm,
                34 * mm,
            ],
            header=True,
        ),
    ]


def build_content_metrics(
    analysis: Dict[str, Any],
    styles: Dict[str, ParagraphStyle],
) -> List[Any]:
    keyword = analysis.get("keyword", {})
    readability = analysis.get(
        "readability",
        {},
    )
    headings = analysis.get("headings", {})
    meta = analysis.get("meta", {})

    rows = [
        ["Métrica", "Resultado"],
        [
            "Cantidad de palabras",
            readability.get("word_count"),
        ],
        [
            "Densidad de keyword",
            (
                f"{keyword.get('density')} %"
                if keyword.get("density")
                is not None
                else None
            ),
        ],
        [
            "Apariciones de keyword",
            keyword.get("keyword_count"),
        ],
        [
            "Legibilidad",
            readability.get(
                "reading_score"
            ),
        ],
        [
            "Encabezados H1",
            (
                headings.get("h1", {})
                .get("count")
            ),
        ],
        [
            "Encabezados H2",
            (
                headings.get("h2", {})
                .get("count")
            ),
        ],
        [
            "Encabezados H3",
            (
                headings.get("h3", {})
                .get("count")
            ),
        ],
        [
            "Título SEO",
            (
                meta.get("title", {})
                .get("text")
            ),
        ],
        [
            "Meta Description",
            (
                meta.get("description", {})
                .get("text")
            ),
        ],
    ]

    return [
        create_table(
            rows,
            styles,
            widths=[
                60 * mm,
                100 * mm,
            ],
            header=True,
        )
    ]


def build_onpage_metrics(
    analysis: Dict[str, Any],
    styles: Dict[str, ParagraphStyle],
) -> List[Any]:
    title = analysis.get("title", {})
    description = analysis.get(
        "meta_description",
        {},
    )
    headings = analysis.get("headings", {})
    images = analysis.get("images", {})
    links = analysis.get("links", {})
    canonical = analysis.get(
        "canonical",
        {},
    )
    open_graph = analysis.get(
        "open_graph",
        {},
    )

    rows = [
        ["Métrica", "Resultado"],
        ["Título", title.get("text")],
        [
            "Longitud del título",
            title.get("length"),
        ],
        [
            "Meta Description",
            description.get("content"),
        ],
        [
            "Longitud de descripción",
            description.get("length"),
        ],
        [
            "Cantidad de H1",
            (
                headings.get("h1", {})
                .get("count")
            ),
        ],
        [
            "Imágenes totales",
            images.get("total"),
        ],
        [
            "Imágenes sin ALT",
            images.get("missing_alt"),
        ],
        [
            "Enlaces internos",
            (
                links.get("internal", {})
                .get("count")
            ),
        ],
        [
            "Enlaces externos",
            (
                links.get("external", {})
                .get("count")
            ),
        ],
        [
            "Canonical",
            canonical.get("href"),
        ],
        [
            "Open Graph completo",
            open_graph.get("complete"),
        ],
    ]

    return [
        create_table(
            rows,
            styles,
            widths=[
                60 * mm,
                100 * mm,
            ],
            header=True,
        )
    ]


def build_technical_metrics(
    analysis: Dict[str, Any],
    styles: Dict[str, ParagraphStyle],
) -> List[Any]:
    https_result = analysis.get("https", {})
    http_status = analysis.get(
        "http_status",
        {},
    )
    response_time = analysis.get(
        "response_time",
        {},
    )
    robots = analysis.get("robots", {})
    sitemap = analysis.get("sitemap", {})
    canonical = analysis.get(
        "canonical",
        {},
    )
    meta_robots = analysis.get(
        "meta_robots",
        {},
    )

    rows = [
        ["Métrica", "Resultado"],
        [
            "HTTPS seguro",
            https_result.get("secure"),
        ],
        [
            "Código HTTP",
            http_status.get("status_code"),
        ],
        [
            "Tiempo de respuesta",
            (
                f"{response_time.get('response_time')} ms"
                if response_time.get(
                    "response_time"
                )
                is not None
                else None
            ),
        ],
        [
            "robots.txt",
            robots.get("exists"),
        ],
        [
            "Sitemap en robots.txt",
            robots.get("has_sitemap"),
        ],
        [
            "sitemap.xml",
            sitemap.get("exists"),
        ],
        [
            "Tipo de sitemap",
            sitemap.get("type"),
        ],
        [
            "URLs en sitemap",
            sitemap.get("url_count"),
        ],
        [
            "Sitemaps registrados",
            sitemap.get("sitemap_count"),
        ],
        [
            "Canonical",
            canonical.get("href"),
        ],
        [
            "Meta robots",
            meta_robots.get("content"),
        ],
    ]

    return [
        create_table(
            rows,
            styles,
            widths=[
                60 * mm,
                100 * mm,
            ],
            header=True,
        )
    ]


def build_monitor_metrics(
    analysis: Dict[str, Any],
    styles: Dict[str, ParagraphStyle],
) -> List[Any]:
    availability = analysis.get(
        "availability",
        {},
    )
    response_time = analysis.get(
        "response_time",
        {},
    )
    redirects = analysis.get(
        "redirects",
        {},
    )
    ssl_result = analysis.get("ssl", {})
    pagespeed = analysis.get(
        "pagespeed",
        {},
    )

    rows = [
        ["Métrica", "Resultado"],
        [
            "Sitio disponible",
            availability.get("available"),
        ],
        [
            "Código HTTP",
            availability.get("status_code"),
        ],
        [
            "Tiempo de respuesta",
            (
                f"{response_time.get('response_time_ms')} ms"
                if response_time.get(
                    "response_time_ms"
                )
                is not None
                else None
            ),
        ],
        [
            "Redirecciones",
            redirects.get("count"),
        ],
        [
            "SSL válido",
            ssl_result.get("valid"),
        ],
        [
            "Protocolo TLS",
            ssl_result.get("protocol"),
        ],
        [
            "Días restantes SSL",
            ssl_result.get(
                "days_remaining"
            ),
        ],
        [
            "PageSpeed disponible",
            pagespeed.get("available"),
        ],
        [
            "Estrategia PageSpeed",
            pagespeed.get("strategy"),
        ],
        [
            "Performance",
            pagespeed.get(
                "performance_score"
            ),
        ],
        ["FCP", pagespeed.get("fcp")],
        ["LCP", pagespeed.get("lcp")],
        ["CLS", pagespeed.get("cls")],
        [
            "Speed Index",
            pagespeed.get("speed_index"),
        ],
        [
            "TBT",
            (
                pagespeed.get("metrics", {})
                .get(
                    "total_blocking_time",
                    {},
                )
                .get("display_value")
            ),
        ],
        [
            "Versión de Lighthouse",
            pagespeed.get(
                "lighthouse_version"
            ),
        ],
    ]

    elements: List[Any] = [
        create_table(
            rows,
            styles,
            widths=[
                60 * mm,
                100 * mm,
            ],
            header=True,
        )
    ]

    opportunities = pagespeed.get(
        "opportunities",
        [],
    )

    if isinstance(opportunities, list) and opportunities:
        opportunity_rows = [
            [
                "Oportunidad",
                "Ahorro estimado",
            ]
        ]

        for opportunity in opportunities[:10]:
            if not isinstance(
                opportunity,
                dict,
            ):
                continue

            opportunity_rows.append(
                [
                    opportunity.get(
                        "title"
                    ),
                    opportunity.get(
                        "display_value"
                    ),
                ]
            )

        elements.extend(
            [
                Spacer(1, 4 * mm),
                Paragraph(
                    "Oportunidades PageSpeed",
                    styles["subsection"],
                ),
                create_table(
                    opportunity_rows,
                    styles,
                    widths=[
                        105 * mm,
                        55 * mm,
                    ],
                    header=True,
                ),
            ]
        )

    return elements


def build_issues_section(
    issues: Any,
    styles: Dict[str, ParagraphStyle],
) -> List[Any]:
    if not isinstance(issues, list) or not issues:
        return [
            Paragraph(
                "No se detectaron incidencias.",
                styles["normal"],
            )
        ]

    rows = [
        ["Tipo", "Código", "Descripción"]
    ]

    for issue in issues:
        if not isinstance(issue, dict):
            continue

        rows.append(
            [
                issue.get("type"),
                issue.get("code"),
                issue.get("message"),
            ]
        )

    return [
        create_table(
            rows,
            styles,
            widths=[
                24 * mm,
                48 * mm,
                88 * mm,
            ],
            header=True,
        )
    ]


def build_recommendations_section(
    recommendations: Any,
    styles: Dict[str, ParagraphStyle],
) -> List[Any]:
    if (
        not isinstance(
            recommendations,
            list,
        )
        or not recommendations
    ):
        return [
            Paragraph(
                "No hay recomendaciones adicionales.",
                styles["normal"],
            )
        ]

    elements: List[Any] = []

    for index, recommendation in enumerate(
        recommendations,
        start=1,
    ):
        elements.append(
            Paragraph(
                (
                    f"<b>{index}.</b> "
                    f"{paragraph_text(recommendation)}"
                ),
                styles["normal"],
            )
        )
        elements.append(
            Spacer(1, 1.5 * mm)
        )

    return elements


def build_module_section(
    module_name: str,
    wrapper: Dict[str, Any],
    styles: Dict[str, ParagraphStyle],
) -> List[Any]:
    result = get_result(wrapper)
    analysis = result.get("analysis", {})

    if not isinstance(analysis, dict):
        analysis = {}

    title = MODULE_NAMES.get(
        module_name,
        module_name,
    )

    elements: List[Any] = [
        Paragraph(
            title,
            styles["section"],
        ),
        create_table(
            [
                ["Dato", "Valor"],
                [
                    "Estado",
                    result.get("status"),
                ],
                [
                    "Éxito",
                    result.get("success"),
                ],
                [
                    "Score",
                    result.get("score"),
                ],
                [
                    "Prioridad",
                    wrapper.get("priority"),
                ],
                [
                    "Timeout",
                    (
                        f"{wrapper.get('timeout')} s"
                        if wrapper.get(
                            "timeout"
                        )
                        is not None
                        else None
                    ),
                ],
            ],
            styles,
            widths=[
                48 * mm,
                112 * mm,
            ],
            header=True,
        ),
        Spacer(1, 4 * mm),
        Paragraph(
            "Métricas principales",
            styles["subsection"],
        ),
    ]

    metric_builders = {
        "seo-content": build_content_metrics,
        "seo-onpage": build_onpage_metrics,
        "seo-technical": (
            build_technical_metrics
        ),
        "seo-monitor": build_monitor_metrics,
    }

    builder = metric_builders.get(
        module_name
    )

    if builder:
        elements.extend(
            builder(
                analysis,
                styles,
            )
        )
    else:
        elements.append(
            Paragraph(
                "No existe una plantilla específica para este módulo.",
                styles["normal"],
            )
        )

    elements.extend(
        [
            Spacer(1, 5 * mm),
            Paragraph(
                "Problemas detectados",
                styles["subsection"],
            ),
        ]
    )

    elements.extend(
        build_issues_section(
            result.get("issues"),
            styles,
        )
    )

    elements.extend(
        [
            Spacer(1, 5 * mm),
            Paragraph(
                "Recomendaciones",
                styles["subsection"],
            ),
        ]
    )

    elements.extend(
        build_recommendations_section(
            result.get(
                "recommendations"
            ),
            styles,
        )
    )

    errors = result.get("errors")

    if isinstance(errors, list) and errors:
        elements.extend(
            [
                Spacer(1, 5 * mm),
                Paragraph(
                    "Errores técnicos",
                    styles["subsection"],
                ),
                build_issues_section(
                    [
                        {
                            "type": "error",
                            "code": (
                                error.get("code")
                                if isinstance(
                                    error,
                                    dict,
                                )
                                else "ERROR"
                            ),
                            "message": (
                                error.get("message")
                                if isinstance(
                                    error,
                                    dict,
                                )
                                else error
                            ),
                        }
                        for error in errors
                    ],
                    styles,
                )[0],
            ]
        )

    return elements


def draw_page(
    canvas,
    document,
    audit_id: str,
) -> None:
    canvas.saveState()

    canvas.setFillColor(
        BACKGROUND
    )
    canvas.rect(
        0,
        PAGE_HEIGHT - 22 * mm,
        PAGE_WIDTH,
        22 * mm,
        fill=1,
        stroke=0,
    )

    canvas.setFont(
        "Helvetica-Bold",
        9,
    )
    canvas.setFillColor(
        colors.white
    )
    canvas.drawString(
        18 * mm,
        PAGE_HEIGHT - 13 * mm,
        "SEO Automation Platform",
    )

    canvas.setFont(
        "Helvetica",
        7,
    )
    canvas.setFillColor(
        colors.HexColor("#CBD5E1")
    )
    canvas.drawRightString(
        PAGE_WIDTH - 18 * mm,
        PAGE_HEIGHT - 13 * mm,
        safe_text(audit_id),
    )

    canvas.setStrokeColor(
        BORDER
    )
    canvas.line(
        18 * mm,
        15 * mm,
        PAGE_WIDTH - 18 * mm,
        15 * mm,
    )

    canvas.setFillColor(
        SECONDARY_TEXT
    )
    canvas.setFont(
        "Helvetica",
        7,
    )

    canvas.drawString(
        18 * mm,
        9 * mm,
        "Reporte generado automáticamente.",
    )

    canvas.drawRightString(
        PAGE_WIDTH - 18 * mm,
        9 * mm,
        f"Página {document.page}",
    )

    canvas.restoreState()


def build_audit_pdf(
    audit: Any,
) -> BytesIO:
    buffer = BytesIO()
    styles = get_styles()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=30 * mm,
        bottomMargin=22 * mm,
        title=(
            f"Reporte de auditoría "
            f"{audit.audit_id}"
        ),
        author="SEO Automation Platform",
        subject="Reporte de auditoría SEO",
    )

    results = (
        audit.results
        if isinstance(audit.results, dict)
        else {}
    )

    story: List[Any] = []

    title_card = Table(
        [
            [
                Paragraph(
                    "Reporte de auditoría SEO",
                    styles["title"],
                )
            ],
            [
                Paragraph(
                    (
                        f"Sitio: "
                        f"{paragraph_text(audit.website)}"
                        "<br/>"
                        f"Auditoría: "
                        f"{paragraph_text(audit.audit_id)}"
                    ),
                    styles["subtitle"],
                )
            ],
        ],
        colWidths=[160 * mm],
    )

    title_card.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    BACKGROUND,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0,
                    BACKGROUND,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    14,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    14,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, 0),
                    13,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 1),
                    (-1, -1),
                    13,
                ),
            ]
        )
    )

    story.extend(
        [
            title_card,
            Spacer(1, 6 * mm),
        ]
    )

    story.extend(
        build_summary_section(
            audit,
            results,
            styles,
        )
    )

    story.extend(
        [
            Spacer(1, 7 * mm),
            *build_module_summary(
                results,
                styles,
            ),
        ]
    )

    ordered_modules = sorted(
        results.items(),
        key=lambda item: (
            item[1].get("priority", 999)
            if isinstance(item[1], dict)
            else 999
        ),
    )

    for module_name, wrapper in ordered_modules:
        if not isinstance(wrapper, dict):
            continue

        story.append(PageBreak())

        story.extend(
            build_module_section(
                module_name,
                wrapper,
                styles,
            )
        )

    if not ordered_modules:
        story.extend(
            [
                Spacer(1, 8 * mm),
                Paragraph(
                    "La auditoría todavía no contiene resultados de módulos.",
                    styles["normal"],
                ),
            ]
        )

    document.build(
        story,
        onFirstPage=lambda canvas, doc: draw_page(
            canvas,
            doc,
            audit.audit_id,
        ),
        onLaterPages=lambda canvas, doc: draw_page(
            canvas,
            doc,
            audit.audit_id,
        ),
    )

    buffer.seek(0)

    return buffer
