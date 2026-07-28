import {
    useEffect,
    useState,
} from "react";

import api from "../api/api";

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

export default function ModuleTable() {
    const [modules, setModules] =
        useState([]);

    const [loading, setLoading] =
        useState(true);

    const [error, setError] =
        useState("");

    const [updatingModule, setUpdatingModule] =
        useState(null);

    useEffect(() => {
        loadModules();
    }, []);

    async function loadModules() {
        try {
            setLoading(true);
            setError("");

            const response =
                await api.get("/modules");

            setModules(
                Array.isArray(
                    response.data?.modules
                )
                    ? response.data.modules
                    : []
            );
        } catch (requestError) {
            console.error(
                "Error loading modules:",
                requestError
            );

            setError(
                "No fue posible cargar los módulos."
            );
        } finally {
            setLoading(false);
        }
    }

    async function toggleModule(module) {
        try {
            setUpdatingModule(module.id);
            setError("");

            const response = await api.patch(
                `/modules/${module.id}/activate`,
                {
                    active: !module.active,
                }
            );

            setModules((currentModules) =>
                currentModules.map(
                    (currentModule) =>
                        currentModule.id ===
                        module.id
                            ? {
                                  ...currentModule,
                                  active:
                                      response
                                          .data
                                          ?.module
                                          ?.active ??
                                      !module.active,
                              }
                            : currentModule
                )
            );
        } catch (requestError) {
            console.error(
                "Error updating module:",
                requestError
            );

            setError(
                "No fue posible actualizar el estado del módulo."
            );
        } finally {
            setUpdatingModule(null);
        }
    }

    if (loading) {
        return (
            <div className="empty-state">
                <div className="large-spinner" />

                <p>Cargando módulos...</p>
            </div>
        );
    }

    return (
        <div className="module-management">
            {error && (
                <div className="inline-alert inline-alert-warning">
                    <span aria-hidden="true">
                        !
                    </span>

                    <p>{error}</p>

                    <button
                        type="button"
                        onClick={loadModules}
                    >
                        Reintentar
                    </button>
                </div>
            )}

            <div className="module-management-grid">
                {modules.map((module) => (
                    <article
                        key={module.id}
                        className="module-management-card"
                    >
                        <div className="module-management-header">
                            <div className="module-service-icon">
                                {module.name
                                    ?.replace(
                                        "seo-",
                                        ""
                                    )
                                    ?.charAt(0)
                                    ?.toUpperCase() ||
                                    "S"}
                            </div>

                            <div className="module-management-title">
                                <h3>
                                    {module.name}
                                </h3>

                                <span
                                    className={
                                        module.active
                                            ? "status-badge status-completed"
                                            : "status-badge status-failed"
                                    }
                                >
                                    {module.active
                                        ? "Activo"
                                        : "Inactivo"}
                                </span>
                            </div>
                        </div>

                        <p className="module-management-description">
                            {module.description ||
                                "Servicio de análisis SEO registrado en el API Gateway."}
                        </p>

                        <dl className="module-details-list">
                            <div>
                                <dt>Prioridad</dt>
                                <dd>
                                    {
                                        module.priority
                                    }
                                </dd>
                            </div>

                            <div>
                                <dt>Timeout</dt>
                                <dd>
                                    {module.timeout} s
                                </dd>
                            </div>

                            <div>
                                <dt>Identificador</dt>
                                <dd>
                                    #{module.id}
                                </dd>
                            </div>

                            <div>
                                <dt>Actualizado</dt>
                                <dd>
                                    {formatDate(
                                        module.updated_at
                                    )}
                                </dd>
                            </div>
                        </dl>

                        <div className="module-url-box">
                            <span>
                                Endpoint interno
                            </span>

                            <code>
                                {module.url}
                            </code>
                        </div>

                        <button
                            type="button"
                            className={
                                module.active
                                    ? "secondary-button module-state-button"
                                    : "primary-button module-state-button"
                            }
                            disabled={
                                updatingModule ===
                                module.id
                            }
                            onClick={() =>
                                toggleModule(
                                    module
                                )
                            }
                        >
                            {updatingModule ===
                            module.id
                                ? "Actualizando..."
                                : module.active
                                  ? "Desactivar módulo"
                                  : "Activar módulo"}
                        </button>
                    </article>
                ))}
            </div>
        </div>
    );
}
