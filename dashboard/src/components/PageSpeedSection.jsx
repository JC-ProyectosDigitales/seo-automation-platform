const SCORE_INFORMATION = {
    performance: {
        label: "Rendimiento",
        abbreviation: "PERF",
    },
    accessibility: {
        label: "Accesibilidad",
        abbreviation: "A11Y",
    },
    best_practices: {
        label: "Mejores prácticas",
        abbreviation: "BP",
    },
    seo: {
        label: "SEO",
        abbreviation: "SEO",
    },
};

const METRIC_INFORMATION = {
    first_contentful_paint: {
        abbreviation: "FCP",
        label: "First Contentful Paint",
        missingReason:
            "Lighthouse no pudo determinar cuándo apareció el primer contenido visible.",
    },
    largest_contentful_paint: {
        abbreviation: "LCP",
        label: "Largest Contentful Paint",
        missingReason:
            "Lighthouse no pudo medir el elemento de contenido principal.",
    },
    cumulative_layout_shift: {
        abbreviation: "CLS",
        label: "Cumulative Layout Shift",
        missingReason:
            "No se obtuvo información suficiente sobre los cambios de diseño.",
    },
    interaction_to_next_paint: {
        abbreviation: "INP",
        label: "Interaction to Next Paint",
        missingReason:
            "No existen suficientes datos reales de usuarios para calcular esta métrica.",
    },
    total_blocking_time: {
        abbreviation: "TBT",
        label: "Total Blocking Time",
        missingReason:
            "Lighthouse no pudo calcular el tiempo total de bloqueo.",
    },
    speed_index: {
        abbreviation: "SI",
        label: "Speed Index",
        missingReason:
            "Lighthouse no pudo calcular la velocidad visual de carga.",
    },
};

const DIAGNOSTIC_LABELS = {
    total_byte_weight:
        "Peso total de la página",
    dom_size:
        "Tamaño del DOM",
    main_thread_work:
        "Trabajo del hilo principal",
    bootup_time:
        "Ejecución de JavaScript",
    unused_javascript:
        "JavaScript sin utilizar",
    unused_css:
        "CSS sin utilizar",
    render_blocking_resources:
        "Recursos que bloquean el renderizado",
    uses_optimized_images:
        "Optimización de imágenes",
    uses_webp_images:
        "Formatos modernos de imagen",
    server_response_time:
        "Respuesta inicial del servidor",
};

const OPTIONAL_SCORE_NAMES = [
    "accessibility",
    "best_practices",
    "seo",
];

function isMissingValue(value) {
    return (
        value === null ||
        value === undefined ||
        value === ""
    );
}

function getScoreInformation(score) {
    if (isMissingValue(score)) {
        return {
            className:
                "pagespeed-score-unknown",
            status: "No evaluado",
        };
    }

    if (score >= 90) {
        return {
            className:
                "pagespeed-score-good",
            status: "Bueno",
        };
    }

    if (score >= 50) {
        return {
            className:
                "pagespeed-score-medium",
            status: "Mejorable",
        };
    }

    return {
        className:
            "pagespeed-score-low",
        status: "Deficiente",
    };
}

function getRatingInformation(rating) {
    const ratings = {
        good: {
            label: "Bueno",
            className:
                "pagespeed-rating-good",
        },
        needs_improvement: {
            label: "Mejorable",
            className:
                "pagespeed-rating-medium",
        },
        poor: {
            label: "Deficiente",
            className:
                "pagespeed-rating-poor",
        },
        unknown: {
            label: "Sin datos",
            className:
                "pagespeed-rating-unknown",
        },
    };

    return (
        ratings[rating] ||
        ratings.unknown
    );
}

function formatBytes(value) {
    if (
        value === null ||
        value === undefined ||
        Number.isNaN(Number(value))
    ) {
        return null;
    }

    const bytes = Number(value);

    if (bytes >= 1024 * 1024) {
        return `${(
            bytes /
            (1024 * 1024)
        ).toFixed(2)} MB`;
    }

    if (bytes >= 1024) {
        return `${(
            bytes / 1024
        ).toFixed(2)} KB`;
    }

    return `${Math.round(bytes)} B`;
}

function getGeneralErrorTitle(error) {
    const code = String(
        error?.code || ""
    ).toUpperCase();

    const statusCode =
        error?.status_code;

    if (statusCode === 429) {
        return "Cuota de PageSpeed agotada";
    }

    if (code.includes("TIMEOUT")) {
        return "El análisis excedió el tiempo de espera";
    }

    if (
        statusCode === 401 ||
        statusCode === 403
    ) {
        return "La solicitud no pudo autenticarse";
    }

    if (statusCode === 404) {
        return "La página no pudo encontrarse";
    }

    if (
        statusCode &&
        statusCode >= 500
    ) {
        return "PageSpeed presentó un error temporal";
    }

    if (
        code.includes(
            "ERRORED_DOCUMENT_REQUEST"
        )
    ) {
        return "La página no pudo cargarse";
    }

    if (code.includes("NO_FCP")) {
        return "La página no mostró contenido visible";
    }

    if (code.includes("PAGE_HUNG")) {
        return "La página dejó de responder";
    }

    return "No fue posible completar el análisis";
}

function getGeneralErrorExplanation(
    error
) {
    const code = String(
        error?.code || ""
    ).toUpperCase();

    const statusCode =
        error?.status_code;

    if (statusCode === 429) {
        return (
            "Se alcanzó el límite permitido por la API de Google. " +
            "Las demás comprobaciones del sitio pueden continuar, " +
            "pero las métricas de Lighthouse no estarán disponibles."
        );
    }

    if (code.includes("TIMEOUT")) {
        return (
            "Google comenzó el análisis, pero no devolvió el resultado " +
            "dentro del tiempo configurado. Puede ocurrir en páginas " +
            "pesadas, lentas o con muchos recursos externos."
        );
    }

    if (
        statusCode === 401 ||
        statusCode === 403
    ) {
        return (
            "La clave de la API puede ser inválida, estar restringida " +
            "o no tener habilitado PageSpeed Insights."
        );
    }

    if (statusCode === 404) {
        return (
            "La URL respondió como página inexistente o Google no pudo localizarla."
        );
    }

    if (
        statusCode &&
        statusCode >= 500
    ) {
        return (
            "Google Lighthouse presentó una falla temporal. " +
            "La auditoría puede volver a intentarse más tarde."
        );
    }

    if (
        code.includes(
            "ERRORED_DOCUMENT_REQUEST"
        )
    ) {
        return (
            "Lighthouse no pudo descargar el documento principal. " +
            "El sitio pudo bloquear la solicitud o interrumpir la conexión."
        );
    }

    if (code.includes("NO_FCP")) {
        return (
            "No apareció contenido visible durante el tiempo esperado, " +
            "por lo que Lighthouse no pudo calcular las métricas visuales."
        );
    }

    if (code.includes("PAGE_HUNG")) {
        return (
            "La página dejó de responder mientras Lighthouse ejecutaba la prueba."
        );
    }

    return (
        error?.message ||
        "Google PageSpeed Insights no devolvió información suficiente."
    );
}

function PageSpeedUnavailable({
    pagespeed,
}) {
    const error =
        pagespeed?.error || {};

    return (
        <section className="pagespeed-section">
            <header className="pagespeed-main-header">
                <div className="pagespeed-main-title">
                    <span className="pagespeed-google-label">
                        Google Lighthouse
                    </span>

                    <h4>
                        PageSpeed Insights
                    </h4>
                </div>

                <span className="pagespeed-status pagespeed-status-failed">
                    No disponible
                </span>
            </header>

            <div className="pagespeed-error-card">
                <div className="pagespeed-error-icon">
                    !
                </div>

                <div className="pagespeed-error-content">
                    <strong>
                        {getGeneralErrorTitle(
                            error
                        )}
                    </strong>

                    <p>
                        {getGeneralErrorExplanation(
                            error
                        )}
                    </p>

                    {error.message && (
                        <details className="pagespeed-error-details">
                            <summary>
                                Ver respuesta técnica
                            </summary>

                            <p>
                                {error.message}
                            </p>
                        </details>
                    )}

                    <div className="pagespeed-error-meta">
                        {error.code && (
                            <span>
                                Código:{" "}
                                {error.code}
                            </span>
                        )}

                        {error.status_code && (
                            <span>
                                HTTP:{" "}
                                {
                                    error.status_code
                                }
                            </span>
                        )}

                        {pagespeed?.strategy && (
                            <span>
                                Estrategia:{" "}
                                {
                                    pagespeed.strategy
                                }
                            </span>
                        )}
                    </div>
                </div>
            </div>
        </section>
    );
}

function getMissingDataMessages(
    pagespeed
) {
    const messages = [];

    const scores =
        pagespeed?.scores || {};

    const missingOptionalScores =
        OPTIONAL_SCORE_NAMES.filter(
            (scoreName) =>
                isMissingValue(
                    scores[scoreName]
                )
        );

    if (
        missingOptionalScores.length ===
        OPTIONAL_SCORE_NAMES.length
    ) {
        messages.push(
            "Accesibilidad, Mejores prácticas y SEO no fueron ejecutadas porque la auditoría está configurada únicamente para Rendimiento."
        );
    } else if (
        missingOptionalScores.length > 0
    ) {
        const labels =
            missingOptionalScores.map(
                (scoreName) =>
                    SCORE_INFORMATION[
                        scoreName
                    ]?.label ||
                    scoreName
            );

        messages.push(
            `No se obtuvo puntuación para: ${labels.join(
                ", "
            )}.`
        );
    }

    const metrics =
        pagespeed?.metrics || {};

    const inp =
        metrics.interaction_to_next_paint;

    if (
        !inp ||
        isMissingValue(
            inp.display_value
        )
    ) {
        messages.push(
            "INP no está disponible porque Google no cuenta con suficientes datos reales de usuarios para esta página."
        );
    }

    const warnings =
        pagespeed?.warnings;

    if (Array.isArray(warnings)) {
        warnings.forEach(
            (warning) => {
                if (
                    typeof warning ===
                        "string" &&
                    warning.trim()
                ) {
                    messages.push(
                        warning.trim()
                    );
                }
            }
        );
    }

    return [
        ...new Set(messages),
    ];
}

function PageSpeedDataNotice({
    pagespeed,
}) {
    const messages =
        getMissingDataMessages(
            pagespeed
        );

    if (messages.length === 0) {
        return null;
    }

    return (
        <aside className="pagespeed-data-notice">
            <div className="pagespeed-data-notice-icon">
                i
            </div>

            <div className="pagespeed-data-notice-content">
                <div className="pagespeed-data-notice-heading">
                    <strong>
                        Información parcial
                    </strong>

                    <span>
                        Algunos datos fueron omitidos
                    </span>
                </div>

                <ul>
                    {messages.map(
                        (
                            message,
                            index
                        ) => (
                            <li
                                key={`${index}-${message}`}
                            >
                                {message}
                            </li>
                        )
                    )}
                </ul>
            </div>
        </aside>
    );
}

function PageSpeedScores({
    scores,
}) {
    return (
        <section className="pagespeed-content-block">
            <header className="pagespeed-block-heading">
                <div>
                    <span className="pagespeed-eyebrow">
                        Lighthouse
                    </span>

                    <h5>
                        Puntuaciones
                    </h5>
                </div>

                <span className="pagespeed-scale">
                    Escala de 0 a 100
                </span>
            </header>

            <div className="pagespeed-score-grid">
                {Object.entries(
                    SCORE_INFORMATION
                ).map(
                    ([
                        scoreName,
                        information,
                    ]) => {
                        const score =
                            scores?.[
                                scoreName
                            ];

                        const missing =
                            isMissingValue(
                                score
                            );

                        const scoreInfo =
                            getScoreInformation(
                                score
                            );

                        return (
                            <article
                                key={
                                    scoreName
                                }
                                className={`pagespeed-score-card ${scoreInfo.className}`}
                            >
                                <div className="pagespeed-score-visual">
                                    {missing ? (
                                        <div className="pagespeed-score-placeholder">
                                            —
                                        </div>
                                    ) : (
                                        <div className="pagespeed-score-circle">
                                            <strong>
                                                {
                                                    score
                                                }
                                            </strong>
                                        </div>
                                    )}
                                </div>

                                <div className="pagespeed-score-content">
                                    <div className="pagespeed-score-title-row">
                                        <strong>
                                            {
                                                information.label
                                            }
                                        </strong>

                                        <span>
                                            {
                                                scoreInfo.status
                                            }
                                        </span>
                                    </div>

                                    <small>
                                        {missing
                                            ? "Esta categoría no se incluyó en la ejecución actual."
                                            : `Puntuación obtenida: ${score}/100`}
                                    </small>
                                </div>
                            </article>
                        );
                    }
                )}
            </div>
        </section>
    );
}

function PageSpeedMetrics({
    metrics,
}) {
    return (
        <section className="pagespeed-content-block">
            <header className="pagespeed-block-heading">
                <div>
                    <span className="pagespeed-eyebrow">
                        Rendimiento
                    </span>

                    <h5>
                        Métricas de laboratorio
                    </h5>
                </div>
            </header>

            <div className="pagespeed-metrics-grid">
                {Object.entries(
                    METRIC_INFORMATION
                ).map(
                    ([
                        metricName,
                        information,
                    ]) => {
                        const metric =
                            metrics?.[
                                metricName
                            ] || {};

                        const missing =
                            isMissingValue(
                                metric.display_value
                            );

                        const rating =
                            getRatingInformation(
                                metric.rating
                            );

                        return (
                            <article
                                key={
                                    metricName
                                }
                                className={`pagespeed-metric-card ${
                                    missing
                                        ? "pagespeed-metric-card-missing"
                                        : ""
                                }`}
                            >
                                <header className="pagespeed-metric-header">
                                    <div className="pagespeed-metric-name">
                                        <strong>
                                            {
                                                information.abbreviation
                                            }
                                        </strong>

                                        <span>
                                            {
                                                information.label
                                            }
                                        </span>
                                    </div>

                                    <span
                                        className={`pagespeed-rating ${rating.className}`}
                                    >
                                        {
                                            rating.label
                                        }
                                    </span>
                                </header>

                                <div className="pagespeed-metric-result">
                                    <strong>
                                        {missing
                                            ? "No disponible"
                                            : metric.display_value}
                                    </strong>

                                    {!missing &&
                                        metric.numeric_unit && (
                                            <small>
                                                Medición de laboratorio
                                            </small>
                                        )}
                                </div>

                                {missing && (
                                    <p className="pagespeed-metric-reason">
                                        {
                                            information.missingReason
                                        }
                                    </p>
                                )}
                            </article>
                        );
                    }
                )}
            </div>
        </section>
    );
}

function PageSpeedOpportunities({
    opportunities,
}) {
    if (
        !Array.isArray(
            opportunities
        ) ||
        opportunities.length === 0
    ) {
        return null;
    }

    return (
        <section className="pagespeed-content-block">
            <header className="pagespeed-block-heading">
                <div>
                    <span className="pagespeed-eyebrow">
                        Optimización
                    </span>

                    <h5>
                        Principales oportunidades
                    </h5>
                </div>

                <span className="pagespeed-scale">
                    {Math.min(
                        opportunities.length,
                        5
                    )}{" "}
                    resultados
                </span>
            </header>

            <div className="pagespeed-opportunity-list">
                {opportunities
                    .slice(0, 5)
                    .map(
                        (
                            opportunity,
                            index
                        ) => (
                            <article
                                key={
                                    opportunity.id ||
                                    index
                                }
                                className="pagespeed-opportunity"
                            >
                                <div className="pagespeed-opportunity-number">
                                    {index + 1}
                                </div>

                                <div className="pagespeed-opportunity-content">
                                    <strong>
                                        {opportunity.title ||
                                            opportunity.id ||
                                            "Oportunidad de mejora"}
                                    </strong>

                                    {opportunity.display_value && (
                                        <p>
                                            {
                                                opportunity.display_value
                                            }
                                        </p>
                                    )}

                                    <div className="pagespeed-opportunity-meta">
                                        {opportunity.savings_ms !==
                                            null &&
                                            opportunity.savings_ms !==
                                                undefined && (
                                                <span>
                                                    Ahorro:{" "}
                                                    {
                                                        opportunity.savings_ms
                                                    }{" "}
                                                    ms
                                                </span>
                                            )}

                                        {opportunity.savings_bytes !==
                                            null &&
                                            opportunity.savings_bytes !==
                                                undefined && (
                                                <span>
                                                    Transferencia:{" "}
                                                    {formatBytes(
                                                        opportunity.savings_bytes
                                                    )}
                                                </span>
                                            )}
                                    </div>
                                </div>
                            </article>
                        )
                    )}
            </div>
        </section>
    );
}

function PageSpeedDiagnostics({
    diagnostics,
}) {
    const availableDiagnostics =
        Object.entries(
            diagnostics || {}
        ).filter(
            ([, diagnostic]) =>
                diagnostic &&
                typeof diagnostic ===
                    "object" &&
                !isMissingValue(
                    diagnostic.display_value
                )
        );

    if (
        availableDiagnostics.length ===
        0
    ) {
        return null;
    }

    return (
        <section className="pagespeed-content-block">
            <header className="pagespeed-block-heading">
                <div>
                    <span className="pagespeed-eyebrow">
                        Lighthouse
                    </span>

                    <h5>
                        Diagnósticos
                    </h5>
                </div>
            </header>

            <div className="pagespeed-diagnostics-grid">
                {availableDiagnostics.map(
                    ([
                        diagnosticName,
                        diagnostic,
                    ]) => (
                        <article
                            key={
                                diagnosticName
                            }
                            className="pagespeed-diagnostic-card"
                        >
                            <span>
                                {DIAGNOSTIC_LABELS[
                                    diagnosticName
                                ] ||
                                    diagnostic.title ||
                                    diagnosticName}
                            </span>

                            <strong>
                                {
                                    diagnostic.display_value
                                }
                            </strong>

                            {typeof diagnostic.score ===
                                "number" && (
                                <small>
                                    Score:{" "}
                                    {
                                        diagnostic.score
                                    }
                                    /100
                                </small>
                            )}
                        </article>
                    )
                )}
            </div>
        </section>
    );
}

export default function PageSpeedSection({
    pagespeed,
}) {
    if (!pagespeed) {
        return null;
    }

    if (!pagespeed.available) {
        return (
            <PageSpeedUnavailable
                pagespeed={pagespeed}
            />
        );
    }

    return (
        <section className="pagespeed-section">
            <header className="pagespeed-main-header">
                <div className="pagespeed-main-title">
                    <span className="pagespeed-google-label">
                        Google Lighthouse
                    </span>

                    <h4>
                        PageSpeed Insights
                    </h4>

                    <p>
                        Medición realizada con
                        estrategia{" "}
                        <strong>
                            {pagespeed.strategy ||
                                "mobile"}
                        </strong>
                        .
                    </p>
                </div>

                <span className="pagespeed-status pagespeed-status-success">
                    Disponible
                </span>
            </header>

            <PageSpeedDataNotice
                pagespeed={pagespeed}
            />

            <PageSpeedScores
                scores={
                    pagespeed.scores
                }
            />

            <PageSpeedMetrics
                metrics={
                    pagespeed.metrics
                }
            />

            <PageSpeedOpportunities
                opportunities={
                    pagespeed.opportunities
                }
            />

            <PageSpeedDiagnostics
                diagnostics={
                    pagespeed.diagnostics
                }
            />

            <footer className="pagespeed-footer">
                <span>
                    Lighthouse{" "}
                    {pagespeed.lighthouse_version ||
                        "versión no disponible"}
                </span>

                <span>
                    {pagespeed.fetch_time
                        ? new Date(
                              pagespeed.fetch_time
                          ).toLocaleString(
                              "es-MX"
                          )
                        : "Fecha no disponible"}
                </span>
            </footer>
        </section>
    );
}
