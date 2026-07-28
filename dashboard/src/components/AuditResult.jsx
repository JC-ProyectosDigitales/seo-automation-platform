import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

function getFirstValue(source, keys, fallback = null) {
    if (!source || typeof source !== "object") {
        return fallback;
    }

    for (const key of keys) {
        if (
            Object.prototype.hasOwnProperty.call(source, key) &&
            source[key] !== null &&
            source[key] !== undefined &&
            source[key] !== ""
        ) {
            return source[key];
        }
    }

    return fallback;
}

function normalizeStatus(value) {
    const status = String(value || "completed").toLowerCase();

    const statuses = {
        completed: {
            label: "Completada",
            className: "audit-status-completed",
            icon: "✓",
        },
        success: {
            label: "Completada",
            className: "audit-status-completed",
            icon: "✓",
        },
        pending: {
            label: "Pendiente",
            className: "audit-status-pending",
            icon: "◷",
        },
        running: {
            label: "En proceso",
            className: "audit-status-running",
            icon: "◌",
        },
        processing: {
            label: "En proceso",
            className: "audit-status-running",
            icon: "◌",
        },
        failed: {
            label: "Fallida",
            className: "audit-status-failed",
            icon: "!",
        },
        error: {
            label: "Con errores",
            className: "audit-status-failed",
            icon: "!",
        },
        partial: {
            label: "Parcial",
            className: "audit-status-partial",
            icon: "!",
        },
    };

    return (
        statuses[status] || {
            label: value || "Registrada",
            className: "audit-status-unknown",
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

    return new Intl.DateTimeFormat("es-MX", {
        dateStyle: "medium",
        timeStyle: "short",
    }).format(date);
}

function normalizeModules(audit) {
    const possibleSources = [
        audit?.results,
        audit?.modules,
        audit?.module_results,
        audit?.audit_results,
        audit?.data?.results,
        audit?.data?.modules,
    ];

    const source = possibleSources.find(
        (value) =>
            value &&
            (Array.isArray(value) ||
                typeof value === "object")
    );

    if (!source) {
        return [];
    }

    if (Array.isArray(source)) {
        return source.map((item, index) => {
            if (typeof item === "string") {
                return {
                    name: item,
                    status: "completed",
                    data: null,
                };
            }

            return {
                name:
                    item.module ||
                    item.name ||
                    item.service ||
                    `Módulo ${index + 1}`,
                status:
                    item.status ||
                    (item.error ? "failed" : "completed"),
                data:
                    item.result ||
                    item.data ||
                    item.response ||
                    item,
                error:
                    item.error ||
                    item.detail ||
                    item.message ||
                    null,
            };
        });
    }

    return Object.entries(source).map(
        ([moduleName, moduleValue]) => {
            if (
                moduleValue === null ||
                moduleValue === undefined
            ) {
                return {
                    name: moduleName,
                    status: "unknown",
                    data: null,
                    error: null,
                };
            }

            if (typeof moduleValue !== "object") {
                return {
                    name: moduleName,
                    status: "completed",
                    data: moduleValue,
                    error: null,
                };
            }

            return {
                name:
                    moduleValue.module ||
                    moduleValue.name ||
                    moduleName,
                status:
                    moduleValue.status ||
                    (moduleValue.error
                        ? "failed"
                        : "completed"),
                data:
                    moduleValue.result ||
                    moduleValue.data ||
                    moduleValue.response ||
                    moduleValue,
                error:
                    moduleValue.error ||
                    moduleValue.detail ||
                    null,
            };
        }
    );
}

function ModuleResultCard({ module }) {
    const [expanded, setExpanded] = useState(false);
    const status = normalizeStatus(module.status);

    return (
        <article className="audit-module-card">
            <div className="audit-module-header">
                <div className="audit-module-title">
                    <div
                        className={`audit-module-status-icon ${status.className}`}
                    >
                        {status.icon}
                    </div>

                    <div>
                        <h4>{module.name}</h4>

                        <span
                            className={`audit-result-status ${status.className}`}
                        >
                            {status.label}
                        </span>
                    </div>
                </div>

                <button
                    type="button"
                    className="module-toggle-button"
                    onClick={() =>
                        setExpanded(
                            (currentValue) =>
                                !currentValue
                        )
                    }
                >
                    {expanded ? "Ocultar" : "Ver resultado"}
                </button>
            </div>

            {module.error && (
                <div className="module-error-message">
                    <strong>Error del módulo</strong>

                    <p>
                        {typeof module.error === "string"
                            ? module.error
                            : JSON.stringify(module.error)}
                    </p>
                </div>
            )}

            {expanded && (
                <pre className="module-json-result">
                    {JSON.stringify(module.data, null, 2)}
                </pre>
            )}
        </article>
    );
}

export default function AuditResult({ audit }) {
    const [showTechnicalResponse, setShowTechnicalResponse] =
        useState(false);

    const normalizedAudit = useMemo(() => {
        if (!audit || typeof audit !== "object") {
            return {};
        }

        return (
            audit.audit ||
            audit.data?.audit ||
            audit.result ||
            audit
        );
    }, [audit]);

    const auditId = getFirstValue(normalizedAudit, [
        "audit_id",
        "id",
        "uuid",
    ]);

    const website = getFirstValue(normalizedAudit, [
        "website",
        "url",
        "site",
        "domain",
    ]);

    const keyword = getFirstValue(normalizedAudit, [
        "keyword",
        "primary_keyword",
        "target_keyword",
    ]);

    const rawStatus = getFirstValue(
        normalizedAudit,
        ["status", "state"],
        "completed"
    );

    const createdAt = getFirstValue(normalizedAudit, [
        "created_at",
        "createdAt",
        "timestamp",
        "date",
    ]);

    const message = getFirstValue(normalizedAudit, [
        "message",
        "detail",
        "description",
    ]);

    const status = normalizeStatus(rawStatus);
    const modules = normalizeModules(normalizedAudit);

    if (!audit || typeof audit !== "object") {
        return (
            <div className="audit-result-empty">
                <div className="audit-result-empty-icon">
                    !
                </div>

                <h3>Resultado no disponible</h3>

                <p>
                    El API no devolvió información suficiente para
                    mostrar el resultado.
                </p>
            </div>
        );
    }

    return (
        <div className="audit-result">
            <div className="audit-result-overview">
                <div
                    className={`audit-result-main-status ${status.className}`}
                >
                    <span className="audit-result-main-icon">
                        {status.icon}
                    </span>

                    <div>
                        <span>Estado de la auditoría</span>
                        <strong>{status.label}</strong>
                    </div>
                </div>

                <div className="audit-result-summary-grid">
                    <article className="audit-summary-item">
                        <span>Identificador</span>

                        <strong className="audit-code-value">
                            {auditId || "No disponible"}
                        </strong>
                    </article>

                    <article className="audit-summary-item">
                        <span>Sitio web</span>

                        {website ? (
                            <a
                                href={website}
                                target="_blank"
                                rel="noreferrer"
                            >
                                {website}
                            </a>
                        ) : (
                            <strong>No disponible</strong>
                        )}
                    </article>

                    <article className="audit-summary-item">
                        <span>Palabra clave</span>

                        <strong>
                            {keyword || "No disponible"}
                        </strong>
                    </article>

                    <article className="audit-summary-item">
                        <span>Fecha de creación</span>

                        <strong>
                            {formatDate(createdAt)}
                        </strong>
                    </article>
                </div>
            </div>

            {message && (
                <div className="audit-result-message">
                    <div className="information-icon">
                        i
                    </div>

                    <p>
                        {typeof message === "string"
                            ? message
                            : JSON.stringify(message)}
                    </p>
                </div>
            )}

            <section className="audit-modules-result-section">
                <div className="audit-result-section-heading">
                    <div>
                        <h3>Resultados por módulo</h3>

                        <p>
                            Respuestas enviadas por los servicios
                            participantes.
                        </p>
                    </div>

                    <span className="module-count-badge">
                        {modules.length} módulos
                    </span>
                </div>

                {modules.length > 0 ? (
                    <div className="audit-modules-result-list">
                        {modules.map((module, index) => (
                            <ModuleResultCard
                                key={`${module.name}-${index}`}
                                module={module}
                            />
                        ))}
                    </div>
                ) : (
                    <div className="audit-modules-empty">
                        <div className="audit-modules-empty-icon">
                            ◇
                        </div>

                        <div>
                            <h4>
                                La auditoría fue registrada
                            </h4>

                            <p>
                                El Gateway no incluyó los resultados
                                de los módulos en la respuesta
                                inicial. Puedes consultarlos desde
                                el historial.
                            </p>
                        </div>
                    </div>
                )}
            </section>

            <div className="audit-technical-response">
                <button
                    type="button"
                    className="technical-response-toggle"
                    onClick={() =>
                        setShowTechnicalResponse(
                            (currentValue) =>
                                !currentValue
                        )
                    }
                >
                    <span>
                        Respuesta técnica del API
                    </span>

                    <span aria-hidden="true">
                        {showTechnicalResponse ? "−" : "+"}
                    </span>
                </button>

                {showTechnicalResponse && (
                    <pre className="technical-response-json">
                        {JSON.stringify(audit, null, 2)}
                    </pre>
                )}
            </div>

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
                    onClick={() => window.scrollTo(0, 0)}
                >
                    Nueva auditoría
                </Link>
            </div>
        </div>
    );
}
