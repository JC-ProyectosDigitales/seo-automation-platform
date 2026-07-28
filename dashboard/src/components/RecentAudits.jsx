import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import api from "../api/api";

function getStatusInformation(status) {
    const normalizedStatus = String(status || "").toLowerCase();

    const statusMap = {
        completed: {
            label: "Completada",
            className: "status-completed",
        },
        pending: {
            label: "Pendiente",
            className: "status-pending",
        },
        running: {
            label: "En proceso",
            className: "status-running",
        },
        processing: {
            label: "En proceso",
            className: "status-running",
        },
        failed: {
            label: "Fallida",
            className: "status-failed",
        },
    };

    return (
        statusMap[normalizedStatus] || {
            label: status || "Desconocido",
            className: "status-unknown",
        }
    );
}

function formatDate(dateValue) {
    if (!dateValue) {
        return "Sin fecha";
    }

    const date = new Date(dateValue);

    if (Number.isNaN(date.getTime())) {
        return "Fecha no disponible";
    }

    return new Intl.DateTimeFormat("es-MX", {
        dateStyle: "medium",
        timeStyle: "short",
    }).format(date);
}

export default function RecentAudits() {
    const [audits, setAudits] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        loadAudits();
    }, []);

    async function loadAudits() {
        try {
            setError("");

            const response = await api.get("/audits");

            const responseAudits = Array.isArray(
                response.data.audits
            )
                ? response.data.audits
                : [];

            setAudits(responseAudits.slice(0, 5));
        } catch (requestError) {
            console.error(
                "Error loading recent audits:",
                requestError
            );

            setError(
                "No fue posible cargar las auditorías recientes."
            );
        } finally {
            setLoading(false);
        }
    }

    return (
        <section className="content-card recent-audits-card">
            <div className="section-heading section-heading-row">
                <div>
                    <h2>Auditorías recientes</h2>

                    <p>
                        Últimos análisis registrados en la plataforma.
                    </p>
                </div>

                <Link
                    to="/history"
                    className="text-link"
                >
                    Ver historial completo
                    <span aria-hidden="true">→</span>
                </Link>
            </div>

            {loading && (
                <div className="empty-state">
                    <div className="loading-spinner" />

                    <p>Cargando auditorías recientes...</p>
                </div>
            )}

            {!loading && error && (
                <div className="empty-state">
                    <div className="empty-state-icon">!</div>

                    <h3>No se pudieron cargar los datos</h3>

                    <p>{error}</p>

                    <button
                        type="button"
                        className="secondary-button"
                        onClick={loadAudits}
                    >
                        Reintentar
                    </button>
                </div>
            )}

            {!loading && !error && audits.length === 0 && (
                <div className="empty-state">
                    <div className="empty-state-icon">◎</div>

                    <h3>Todavía no hay auditorías</h3>

                    <p>
                        Ejecuta tu primera auditoría para comenzar a
                        visualizar resultados.
                    </p>

                    <Link
                        to="/new-audit"
                        className="primary-button"
                    >
                        Crear auditoría
                    </Link>
                </div>
            )}

            {!loading && !error && audits.length > 0 && (
                <div className="table-container">
                    <table className="data-table">
                        <thead>
                            <tr>
                                <th>Auditoría</th>
                                <th>Sitio web</th>
                                <th>Keyword</th>
                                <th>Estado</th>
                                <th>Fecha</th>
                                <th aria-label="Acciones" />
                            </tr>
                        </thead>

                        <tbody>
                            {audits.map((audit) => {
                                const status =
                                    getStatusInformation(
                                        audit.status
                                    );

                                return (
                                    <tr key={audit.audit_id}>
                                        <td>
                                            <span className="audit-id">
                                                {audit.audit_id}
                                            </span>
                                        </td>

                                        <td>
                                            <span className="website-cell">
                                                {audit.website ||
                                                    "Sin sitio"}
                                            </span>
                                        </td>

                                        <td>
                                            {audit.keyword || "—"}
                                        </td>

                                        <td>
                                            <span
                                                className={`status-badge ${status.className}`}
                                            >
                                                {status.label}
                                            </span>
                                        </td>

                                        <td>
                                            {formatDate(
                                                audit.created_at
                                            )}
                                        </td>

                                        <td>
                                            <Link
                                                to={`/audit/${audit.audit_id}`}
                                                className="table-action"
                                                aria-label={`Ver auditoría ${audit.audit_id}`}
                                            >
                                                Ver
                                            </Link>
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </div>
            )}
        </section>
    );
}
