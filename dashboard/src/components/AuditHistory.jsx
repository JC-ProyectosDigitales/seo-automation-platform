import {
    useEffect,
    useMemo,
    useState,
} from "react";

import { Link } from "react-router-dom";

import api from "../api/api";

function getStatusInformation(value) {
    const status = String(
        value || ""
    ).toLowerCase();

    const statuses = {
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
        statuses[status] || {
            label: value || "Desconocido",
            className: "status-unknown",
        }
    );
}

function formatDate(value) {
    if (!value) {
        return "Sin fecha";
    }

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return "Fecha no disponible";
    }

    return new Intl.DateTimeFormat(
        "es-MX",
        {
            dateStyle: "medium",
            timeStyle: "short",
        }
    ).format(date);
}

export default function AuditHistory() {
    const [audits, setAudits] = useState([]);
    const [search, setSearch] = useState("");
    const [statusFilter, setStatusFilter] =
        useState("all");

    const [loading, setLoading] =
        useState(true);
    const [error, setError] =
        useState("");

    useEffect(() => {
        loadAudits();
    }, []);

    async function loadAudits() {
        try {
            setLoading(true);
            setError("");

            const response =
                await api.get("/audits");

            setAudits(
                Array.isArray(
                    response.data?.audits
                )
                    ? response.data.audits
                    : []
            );
        } catch (requestError) {
            console.error(
                "Error loading audits:",
                requestError
            );

            setError(
                "No fue posible cargar el historial."
            );
        } finally {
            setLoading(false);
        }
    }

    const filteredAudits = useMemo(() => {
        const normalizedSearch =
            search.trim().toLowerCase();

        return audits.filter((audit) => {
            const matchesSearch =
                !normalizedSearch ||
                audit.audit_id
                    ?.toLowerCase()
                    .includes(
                        normalizedSearch
                    ) ||
                audit.website
                    ?.toLowerCase()
                    .includes(
                        normalizedSearch
                    ) ||
                audit.keyword
                    ?.toLowerCase()
                    .includes(
                        normalizedSearch
                    );

            const matchesStatus =
                statusFilter === "all" ||
                audit.status === statusFilter;

            return (
                matchesSearch &&
                matchesStatus
            );
        });
    }, [
        audits,
        search,
        statusFilter,
    ]);

    return (
        <section className="content-card history-card">
            <div className="history-toolbar">
                <div>
                    <span className="page-eyebrow">
                        Registro de análisis
                    </span>

                    <h2>
                        Historial de auditorías
                    </h2>

                    <p>
                        Consulta y filtra las
                        auditorías almacenadas por la
                        plataforma.
                    </p>
                </div>

                <Link
                    to="/new-audit"
                    className="primary-button"
                >
                    + Nueva auditoría
                </Link>
            </div>

            <div className="history-filters">
                <div className="history-search">
                    <span aria-hidden="true">
                        ⌕
                    </span>

                    <input
                        type="search"
                        placeholder="Buscar por ID, sitio o keyword"
                        value={search}
                        onChange={(event) =>
                            setSearch(
                                event.target.value
                            )
                        }
                    />
                </div>

                <select
                    value={statusFilter}
                    onChange={(event) =>
                        setStatusFilter(
                            event.target.value
                        )
                    }
                >
                    <option value="all">
                        Todos los estados
                    </option>

                    <option value="completed">
                        Completadas
                    </option>

                    <option value="pending">
                        Pendientes
                    </option>

                    <option value="running">
                        En proceso
                    </option>

                    <option value="failed">
                        Fallidas
                    </option>
                </select>

                <button
                    type="button"
                    className="secondary-button"
                    onClick={loadAudits}
                >
                    Actualizar
                </button>
            </div>

            {loading && (
                <div className="empty-state">
                    <div className="large-spinner" />

                    <p>
                        Cargando auditorías...
                    </p>
                </div>
            )}

            {!loading && error && (
                <div className="empty-state">
                    <div className="empty-state-icon">
                        !
                    </div>

                    <h3>
                        No se pudo cargar el
                        historial
                    </h3>

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

            {!loading &&
                !error &&
                filteredAudits.length === 0 && (
                    <div className="empty-state">
                        <div className="empty-state-icon">
                            ◎
                        </div>

                        <h3>
                            No hay resultados
                        </h3>

                        <p>
                            No se encontraron
                            auditorías con los filtros
                            seleccionados.
                        </p>
                    </div>
                )}

            {!loading &&
                !error &&
                filteredAudits.length > 0 && (
                    <div className="table-container">
                        <table className="data-table">
                            <thead>
                                <tr>
                                    <th>
                                        Auditoría
                                    </th>

                                    <th>
                                        Sitio web
                                    </th>

                                    <th>
                                        Keyword
                                    </th>

                                    <th>
                                        Estado
                                    </th>

                                    <th>
                                        Fecha
                                    </th>

                                    <th>
                                        Acción
                                    </th>
                                </tr>
                            </thead>

                            <tbody>
                                {filteredAudits.map(
                                    (audit) => {
                                        const status =
                                            getStatusInformation(
                                                audit.status
                                            );

                                        return (
                                            <tr
                                                key={
                                                    audit.audit_id
                                                }
                                            >
                                                <td>
                                                    <span className="audit-id">
                                                        {
                                                            audit.audit_id
                                                        }
                                                    </span>
                                                </td>

                                                <td>
                                                    <span className="website-cell">
                                                        {
                                                            audit.website
                                                        }
                                                    </span>
                                                </td>

                                                <td>
                                                    {audit.keyword ||
                                                        "—"}
                                                </td>

                                                <td>
                                                    <span
                                                        className={`status-badge ${status.className}`}
                                                    >
                                                        {
                                                            status.label
                                                        }
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
                                                    >
                                                        Ver resultado
                                                    </Link>
                                                </td>
                                            </tr>
                                        );
                                    }
                                )}
                            </tbody>
                        </table>
                    </div>
                )}
        </section>
    );
}
