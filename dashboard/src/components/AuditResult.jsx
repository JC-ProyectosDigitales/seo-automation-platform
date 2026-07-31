import { useMemo, useState } from "react";
import { Link } from "react-router-dom";
import PageSpeedSection from "./PageSpeedSection";

const MODULE_INFORMATION = {
    "seo-content": {
        title: "SEO Content",
        description:
            "Contenido, keyword, legibilidad y optimización.",
        icon: "C",
    },
    "seo-onpage": {
        title: "SEO OnPage",
        description:
            "Elementos HTML, metadatos, enlaces e imágenes.",
        icon: "O",
    },
    "seo-technical": {
        title: "SEO Technical",
        description:
            "Indexación, HTTPS, sitemap y robots.",
        icon: "T",
    },
    "seo-monitor": {
        title: "SEO Monitor",
        description:
            "Disponibilidad, SSL, rendimiento y PageSpeed Insights.",
        icon: "M",
    },
};

function getStatusInformation(value) {
    const status = String(
        value || "unknown"
    ).toLowerCase();

    const statuses = {
        completed: {
            label: "Completada",
            className: "status-completed",
            icon: "✓",
        },
        success: {
            label: "Completada",
            className: "status-completed",
            icon: "✓",
        },
        pending: {
            label: "Pendiente",
            className: "status-pending",
            icon: "◷",
        },
        running: {
            label: "En proceso",
            className: "status-running",
            icon: "◌",
        },
        processing: {
            label: "En proceso",
            className: "status-running",
            icon: "◌",
        },
        failed: {
            label: "Fallida",
            className: "status-failed",
            icon: "!",
        },
        error: {
            label: "Con errores",
            className: "status-failed",
            icon: "!",
        },
        partial: {
            label: "Parcial",
            className: "status-partial",
            icon: "!",
        },
    };

    return (
        statuses[status] || {
            label: value || "Desconocido",
            className: "status-unknown",
            icon: "•",
        }
    );
}

function formatDate(value) {
    if (!value) {
        return "No disponible";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return String(value);
    }

    return new Intl.DateTimeFormat(
        "es-MX",
        {
            dateStyle: "medium",
            timeStyle: "short",
        }
    ).format(date);
}

function normalizeModuleResults(results) {
    if (
        !results ||
        typeof results !== "object"
    ) {
        return [];
    }

    return Object.entries(results).map(
        ([moduleName, wrapper]) => {
            const result =
                wrapper?.result ||
                wrapper?.data ||
                wrapper ||
                {};

            const moduleInfo =
                MODULE_INFORMATION[moduleName] || {
                    title: moduleName,
                    description:
                        "Servicio de análisis SEO.",
                    icon: "S",
                };

            return {
                key: moduleName,
                name:
                    result.module ||
                    moduleName,
                title: moduleInfo.title,
                description:
                    moduleInfo.description,
                icon: moduleInfo.icon,
                priority:
                    wrapper?.priority ?? null,
                timeout:
                    wrapper?.timeout ?? null,
                success:
                    result.success !== false,
                status:
                    result.status ||
                    (result.success === false
                        ? "failed"
                        : "completed"),
                score:
                    typeof result.score ===
                    "number"
                        ? result.score
                        : null,
                analysis:
                    result.analysis || {},
                issues: Array.isArray(
                    result.issues
                )
                    ? result.issues
                    : [],
                recommendations: Array.isArray(
                    result.recommendations
                )
                    ? result.recommendations
                    : [],
                errors: Array.isArray(
                    result.errors
                )
                    ? result.errors
                    : [],
                raw: result,
            };
        }
    );
}

function getScoreClass(score) {
    if (
        score === null ||
        score === undefined
    ) {
        return "score-neutral";
    }

    if (score >= 80) {
        return "score-good";
    }

    if (score >= 50) {
        return "score-medium";
    }

    return "score-low";
}

function calculateOverallScore(modules) {
    const validScores = modules
        .map((module) => module.score)
        .filter(
            (score) =>
                typeof score === "number"
        );

    if (validScores.length === 0) {
        return null;
    }

    const total = validScores.reduce(
        (sum, score) => sum + score,
        0
    );

    return Math.round(
        total / validScores.length
    );
}

function Metric({
    label,
    value,
    suffix = "",
}) {
    return (
        <article className="module-metric">
            <span>{label}</span>

            <strong>
                {value === null ||
                value === undefined ||
                value === ""
                    ? "No disponible"
                    : `${value}${suffix}`}
            </strong>
        </article>
    );
}

function BooleanMetric({
    label,
    value,
}) {
    return (
        <article className="module-metric">
            <span>{label}</span>

            <strong
                className={
                    value
                        ? "metric-boolean-success"
                        : "metric-boolean-failed"
                }
            >
                {value ? "✓ Correcto" : "✕ Pendiente"}
            </strong>
        </article>
    );
}

function ContentMetrics({ analysis }) {
    return (
        <div className="module-metrics-grid">
            <Metric
                label="Densidad keyword"
                value={
                    analysis.keyword?.density
                }
                suffix="%"
            />

            <Metric
                label="Palabras"
                value={
                    analysis.keyword
                        ?.total_words ??
                    analysis.readability
                        ?.word_count
                }
            />

            <Metric
                label="Encabezados H1"
                value={
                    analysis.headings?.h1
                        ?.count
                }
            />

            <Metric
                label="Encabezados H2"
                value={
                    analysis.headings?.h2
                        ?.count
                }
            />

            <Metric
                label="Legibilidad"
                value={
                    analysis.readability
                        ?.reading_score
                }
            />

            <BooleanMetric
                label="Meta Description"
                value={
                    analysis.meta
                        ?.description?.exists
                }
            />
        </div>
    );
}

function OnPageMetrics({ analysis }) {
    return (
        <div className="module-metrics-grid">
            <BooleanMetric
                label="Title"
                value={
                    analysis.title?.exists
                }
            />

            <BooleanMetric
                label="Meta Description"
                value={
                    analysis.meta_description
                        ?.exists
                }
            />

            <BooleanMetric
                label="Canonical"
                value={
                    analysis.canonical?.exists
                }
            />

            <BooleanMetric
                label="Open Graph"
                value={
                    analysis.open_graph
                        ?.complete
                }
            />

            <Metric
                label="Enlaces internos"
                value={
                    analysis.links?.internal
                        ?.count
                }
            />

            <Metric
                label="Imágenes optimizadas"
                value={
                    analysis.images
                        ?.optimized_percentage
                }
                suffix="%"
            />
        </div>
    );
}

function TechnicalMetrics({ analysis }) {
    return (
        <div className="module-metrics-grid">
            <BooleanMetric
                label="HTTPS"
                value={
                    analysis.https?.secure
                }
            />

            <BooleanMetric
                label="Estado HTTP"
                value={
                    analysis.http_status
                        ?.success
                }
            />

            <BooleanMetric
                label="robots.txt"
                value={
                    analysis.robots?.exists
                }
            />

            <BooleanMetric
                label="sitemap.xml"
                value={
                    analysis.sitemap?.exists
                }
            />

            <BooleanMetric
                label="Canonical"
                value={
                    analysis.canonical?.exists
                }
            />

            <Metric
                label="Respuesta"
                value={
                    analysis.response_time
                        ?.response_time
                }
                suffix=" ms"
            />
        </div>
    );
}

function MonitorMetrics({ analysis }) {
    return (
        <div className="module-metrics-grid">
            <BooleanMetric
                label="Disponible"
                value={
                    analysis.availability
                        ?.available
                }
            />

            <Metric
                label="Estado HTTP"
                value={
                    analysis.availability
                        ?.status_code
                }
            />

            <Metric
                label="Respuesta"
                value={
                    analysis.response_time
                        ?.response_time_ms
                }
                suffix=" ms"
            />

            <BooleanMetric
                label="SSL válido"
                value={
                    analysis.ssl?.valid
                }
            />

            <Metric
                label="Días SSL"
                value={
                    analysis.ssl
                        ?.days_remaining
                }
            />

            <Metric
                label="Redirecciones"
                value={
                    analysis.redirects
                        ?.count
                }
            />
        </div>
    );
}

function ModuleMetrics({ module }) {
    switch (module.key) {
        case "seo-content":
            return (
                <ContentMetrics
                    analysis={module.analysis}
                />
            );

        case "seo-onpage":
            return (
                <OnPageMetrics
                    analysis={module.analysis}
                />
            );

        case "seo-technical":
            return (
                <TechnicalMetrics
                    analysis={module.analysis}
                />
            );

        case "seo-monitor":
            return (
                <MonitorMetrics
                    analysis={module.analysis}
                />
            );

        default:
            return null;
    }
}

function IssueList({ issues }) {
    if (issues.length === 0) {
        return (
            <div className="module-success-message">
                <span>✓</span>

                <p>
                    No se detectaron problemas en este
                    módulo.
                </p>
            </div>
        );
    }

    return (
        <div className="module-issues-list">
            {issues.map((issue, index) => (
                <article
                    key={`${issue.code}-${index}`}
                    className={`module-issue module-issue-${issue.type || "info"}`}
                >
                    <span className="module-issue-type">
                        {issue.type || "info"}
                    </span>

                    <div>
                        <strong>
                            {issue.code ||
                                "SEO_ISSUE"}
                        </strong>

                        <p>
                            {issue.message ||
                                "Problema detectado"}
                        </p>
                    </div>
                </article>
            ))}
        </div>
    );
}

function ModuleCard({ module }) {
    const [expanded, setExpanded] =
        useState(false);

    const status = getStatusInformation(
        module.status
    );

    return (
        <article className="visual-module-card">
            <div className="visual-module-header">
                <div className="visual-module-title">
                    <div className="visual-module-icon">
                        {module.icon}
                    </div>

                    <div>
                        <h3>{module.title}</h3>

                        <p>
                            {module.description}
                        </p>
                    </div>
                </div>

                <div className="visual-module-summary">
                    <span
                        className={`status-badge ${status.className}`}
                    >
                        {status.icon}{" "}
                        {status.label}
                    </span>

                    <div
                        className={`module-score ${getScoreClass(
                            module.score
                        )}`}
                    >
                        <strong>
                            {module.score ?? "—"}
                        </strong>

                        <span>/100</span>
                    </div>
                </div>
            </div>

            <ModuleMetrics module={module} />
	    
            {module.key === "seo-monitor" && (
		<PageSpeedSection
		    pagespeed={
			module.analysis?.pagespeed
		    }
		/>
	    )}

            <div className="module-count-summary">
                <div>
                    <span>Problemas</span>
                    <strong>
                        {module.issues.length}
                    </strong>
                </div>

                <div>
                    <span>Recomendaciones</span>
                    <strong>
                        {
                            module.recommendations
                                .length
                        }
                    </strong>
                </div>

                <div>
                    <span>Errores</span>
                    <strong>
                        {module.errors.length}
                    </strong>
                </div>
            </div>

            <div className="module-detail-actions">
                <button
                    type="button"
                    className="module-toggle-button"
                    onClick={() =>
                        setExpanded(
                            (current) => !current
                        )
                    }
                >
                    {expanded
                        ? "Ocultar detalles"
                        : "Ver problemas y recomendaciones"}
                </button>
            </div>

            {expanded && (
                <div className="module-expanded-content">
                    <section>
                        <div className="module-subheading">
                            <h4>
                                Problemas detectados
                            </h4>

                            <span>
                                {
                                    module.issues
                                        .length
                                }
                            </span>
                        </div>

                        <IssueList
                            issues={module.issues}
                        />
                    </section>

                    <section>
                        <div className="module-subheading">
                            <h4>
                                Recomendaciones
                            </h4>

                            <span>
                                {
                                    module
                                        .recommendations
                                        .length
                                }
                            </span>
                        </div>

                        {module.recommendations
                            .length > 0 ? (
                            <ol className="recommendation-list">
                                {module.recommendations.map(
                                    (
                                        recommendation,
                                        index
                                    ) => (
                                        <li
                                            key={`${recommendation}-${index}`}
                                        >
                                            <span>
                                                {index +
                                                    1}
                                            </span>

                                            <p>
                                                {
                                                    recommendation
                                                }
                                            </p>
                                        </li>
                                    )
                                )}
                            </ol>
                        ) : (
                            <div className="module-success-message">
                                <span>✓</span>

                                <p>
                                    Este módulo no
                                    generó
                                    recomendaciones.
                                </p>
                            </div>
                        )}
                    </section>

                    {module.errors.length > 0 && (
                        <section>
                            <div className="module-subheading">
                                <h4>
                                    Errores técnicos
                                </h4>

                                <span>
                                    {
                                        module.errors
                                            .length
                                    }
                                </span>
                            </div>

                            <pre className="technical-response-json">
                                {JSON.stringify(
                                    module.errors,
                                    null,
                                    2
                                )}
                            </pre>
                        </section>
                    )}
                </div>
            )}
        </article>
    );
}

export default function AuditResult({ audit }) {
    const [showTechnicalResponse, setShowTechnicalResponse] =
        useState(false);

    const modules = useMemo(
        () =>
            normalizeModuleResults(
                audit?.results
            ),
        [audit]
    );

    const overallScore = useMemo(
        () => calculateOverallScore(modules),
        [modules]
    );

    const totalIssues = modules.reduce(
        (total, module) =>
            total + module.issues.length,
        0
    );

    const totalRecommendations =
        modules.reduce(
            (total, module) =>
                total +
                module.recommendations.length,
            0
        );

    const status = getStatusInformation(
        audit?.status
    );

    const isProcessing = [
        "pending",
        "running",
        "processing",
    ].includes(
        String(
            audit?.status || ""
        ).toLowerCase()
    );

    if (!audit) {
        return (
            <div className="audit-result-empty">
                <div className="audit-result-empty-icon">
                    !
                </div>

                <h3>
                    Resultado no disponible
                </h3>
            </div>
        );
    }

    return (
        <div className="audit-result">
            <section className="audit-overview-panel">
                <div className="overall-score-column">
                    <span>
                        Score general
                    </span>

                    <div
                        className={`overall-score ${getScoreClass(
                            overallScore
                        )}`}
                    >
                        <strong>
                            {overallScore ?? "—"}
                        </strong>

                        <small>/100</small>
                    </div>

                    <span
                        className={`status-badge ${status.className}`}
                    >
                        {status.icon}{" "}
                        {status.label}
                    </span>
                </div>

                <div className="audit-overview-information">
                    <div className="audit-overview-title">
                        <div>
                            <span className="page-eyebrow">
                                {audit.audit_id}
                            </span>

                            <h2>
                                {audit.website}
                            </h2>

                            <p>
                                Keyword principal:{" "}
                                <strong>
                                    {audit.keyword}
                                </strong>
                            </p>
                        </div>
                    </div>

                    <div className="audit-overview-metrics">
                        <article>
                            <span>Módulos</span>
                            <strong>
                                {modules.length}
                            </strong>
                        </article>

                        <article>
                            <span>Problemas</span>
                            <strong>
                                {totalIssues}
                            </strong>
                        </article>

                        <article>
                            <span>
                                Recomendaciones
                            </span>
                            <strong>
                                {
                                    totalRecommendations
                                }
                            </strong>
                        </article>

                        <article>
                            <span>Fecha</span>
                            <strong>
                                {formatDate(
                                    audit.created_at
                                )}
                            </strong>
                        </article>
                    </div>
                </div>
            </section>

            {isProcessing && (
                <div className="audit-processing-banner">
                    <span className="large-spinner" />

                    <div>
                        <strong>
                            Auditoría en proceso
                        </strong>

                        <p>
                            Los resultados se
                            actualizarán automáticamente.
                        </p>
                    </div>
                </div>
            )}

            {modules.length > 0 ? (
                <section className="visual-module-list">
                    {modules.map((module) => (
                        <ModuleCard
                            key={module.key}
                            module={module}
                        />
                    ))}
                </section>
            ) : (
                <div className="audit-modules-empty">
                    <div className="audit-modules-empty-icon">
                        ◇
                    </div>

                    <div>
                        <h4>
                            Resultados todavía no
                            disponibles
                        </h4>

                        <p>
                            Los módulos continúan
                            ejecutando la auditoría.
                        </p>
                    </div>
                </div>
            )}

            <section className="audit-technical-response">
                <button
                    type="button"
                    className="technical-response-toggle"
                    onClick={() =>
                        setShowTechnicalResponse(
                            (current) => !current
                        )
                    }
                >
                    <span>
                        Respuesta técnica completa
                    </span>

                    <span aria-hidden="true">
                        {showTechnicalResponse
                            ? "−"
                            : "+"}
                    </span>
                </button>

                {showTechnicalResponse && (
                    <pre className="technical-response-json">
                        {JSON.stringify(
                            audit,
                            null,
                            2
                        )}
                    </pre>
                )}
            </section>

            <div className="audit-result-footer">
                <Link
                    to="/history"
                    className="secondary-button"
                >
                    Consultar historial
                </Link>

                <Link
                    to="/new-audit"
                    className="primary-button"
                >
                    Nueva auditoría
                </Link>
            </div>
        </div>
    );
}
