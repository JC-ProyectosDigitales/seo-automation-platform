const SCORE_LABELS = {
    performance: "Rendimiento",
    accessibility: "Accesibilidad",
    best_practices: "Mejores prácticas",
    seo: "SEO",
};

const METRIC_INFORMATION = {
    first_contentful_paint: {
        abbreviation: "FCP",
        label: "First Contentful Paint",
    },
    largest_contentful_paint: {
        abbreviation: "LCP",
        label: "Largest Contentful Paint",
    },
    cumulative_layout_shift: {
        abbreviation: "CLS",
        label: "Cumulative Layout Shift",
    },
    interaction_to_next_paint: {
        abbreviation: "INP",
        label: "Interaction to Next Paint",
    },
    total_blocking_time: {
        abbreviation: "TBT",
        label: "Total Blocking Time",
    },
    speed_index: {
        abbreviation: "SI",
        label: "Speed Index",
    },
};

const DIAGNOSTIC_LABELS = {
    total_byte_weight: "Peso total de la página",
    dom_size: "Tamaño del DOM",
    main_thread_work: "Trabajo del hilo principal",
    bootup_time: "Tiempo de ejecución de JavaScript",
    unused_javascript: "JavaScript sin utilizar",
    unused_css: "CSS sin utilizar",
    render_blocking_resources:
        "Recursos que bloquean el renderizado",
    uses_optimized_images:
        "Optimización de imágenes",
    uses_webp_images:
        "Formatos modernos de imagen",
    server_response_time:
        "Tiempo de respuesta del servidor",
};

function getScoreClass(score) {
    if (
        score === null ||
        score === undefined
    ) {
        return "pagespeed-score-unknown";
    }

    if (score >= 90) {
        return "pagespeed-score-good";
    }

    if (score >= 50) {
        return "pagespeed-score-medium";
    }

    return "pagespeed-score-low";
}

function getRatingInformation(rating) {
    const ratings = {
        good: {
            label: "Bueno",
            className: "pagespeed-rating-good",
        },
        needs_improvement: {
            label: "Mejorable",
            className:
                "pagespeed-rating-medium",
        },
        poor: {
            label: "Deficiente",
            className: "pagespeed-rating-poor",
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

function PageSpeedUnavailable({
    pagespeed,
}) {
    const error = pagespeed?.error || {};

    const isQuotaError =
        error.status_code === 429;

    return (
        <section className="pagespeed-section">
            <div className="pagespeed-section-heading">
                <div>
                    <span className="pagespeed-eyebrow">
                        Google Lighthouse
                    </span>

                    <h4>
                        PageSpeed Insights
                    </h4>
                </div>

                <span className="pagespeed-status pagespeed-status-failed">
                    No disponible
                </span>
            </div>

            <div className="pagespeed-error-card">
                <div className="pagespeed-error-icon">
                    !
                </div>

                <div>
                    <strong>
                        {isQuotaError
                            ? "Cuota de PageSpeed agotada"
                            : "No fue posible completar el análisis"}
                    </strong>

                    <p>
                        {error.message ||
                            "Google PageSpeed Insights no devolvió resultados."}
                    </p>

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

function PageSpeedScores({ scores }) {
    return (
        <section className="pagespeed-content-block">
            <div className="pagespeed-block-heading">
                <div>
                    <span className="pagespeed-eyebrow">
                        Lighthouse
                    </span>

                    <h5>
                        Puntuaciones
                    </h5>
                </div>

                <span>
                    Escala de 0 a 100
                </span>
            </div>

            <div className="pagespeed-score-grid">
                {Object.entries(
                    SCORE_LABELS
                ).map(
                    ([
                        scoreName,
                        label,
                    ]) => {
                        const score =
                            scores?.[
                                scoreName
                            ];

                        return (
                            <article
                                key={
                                    scoreName
                                }
                                className={`pagespeed-score-card ${getScoreClass(
                                    score
                                )}`}
                            >
                                <div className="pagespeed-score-circle">
                                    <strong>
                                        {score ??
                                            "—"}
                                    </strong>
                                </div>

                                <span>
                                    {label}
                                </span>
                            </article>
                        );
                    }
                )}
            </div>
        </section>
    );
}

function PageSpeedMetrics({ metrics }) {
    return (
        <section className="pagespeed-content-block">
            <div className="pagespeed-block-heading">
                <div>
                    <span className="pagespeed-eyebrow">
                        Rendimiento
                    </span>

                    <h5>
                        Métricas de laboratorio
                    </h5>
                </div>
            </div>

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

                        const rating =
                            getRatingInformation(
                                metric.rating
                            );

                        return (
                            <article
                                key={
                                    metricName
                                }
                                className="pagespeed-metric-card"
                            >
                                <div className="pagespeed-metric-header">
                                    <strong>
                                        {
                                            information.abbreviation
                                        }
                                    </strong>

                                    <span
                                        className={`pagespeed-rating ${rating.className}`}
                                    >
                                        {
                                            rating.label
                                        }
                                    </span>
                                </div>

                                <span className="pagespeed-metric-label">
                                    {
                                        information.label
                                    }
                                </span>

                                <strong className="pagespeed-metric-value">
                                    {metric.display_value ||
                                        "No disponible"}
                                </strong>
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
        !Array.isArray(opportunities) ||
        opportunities.length === 0
    ) {
        return null;
    }

    return (
        <section className="pagespeed-content-block">
            <div className="pagespeed-block-heading">
                <div>
                    <span className="pagespeed-eyebrow">
                        Optimización
                    </span>

                    <h5>
                        Principales oportunidades
                    </h5>
                </div>

                <span>
                    Primeras{" "}
                    {Math.min(
                        opportunities.length,
                        5
                    )}
                </span>
            </div>

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
                    "object"
        );

    if (
        availableDiagnostics.length ===
        0
    ) {
        return null;
    }

    return (
        <section className="pagespeed-content-block">
            <div className="pagespeed-block-heading">
                <div>
                    <span className="pagespeed-eyebrow">
                        Lighthouse
                    </span>

                    <h5>
                        Diagnósticos
                    </h5>
                </div>
            </div>

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
                                {diagnostic.display_value ||
                                    "No disponible"}
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
            <div className="pagespeed-section-heading">
                <div>
                    <span className="pagespeed-eyebrow">
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
            </div>

            <PageSpeedScores
                scores={pagespeed.scores}
            />

            <PageSpeedMetrics
                metrics={pagespeed.metrics}
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
                    Fecha:{" "}
                    {pagespeed.fetch_time
                        ? new Date(
                              pagespeed.fetch_time
                          ).toLocaleString(
                              "es-MX"
                          )
                        : "No disponible"}
                </span>
            </footer>
        </section>
    );
}
