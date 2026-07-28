import { useEffect, useState } from "react";

import api from "../api/api";

const defaultStats = {
    total_audits: 0,
    completed_audits: 0,
    pending_audits: 0,
    active_modules: 0,
};

const metricDefinitions = [
    {
        key: "total_audits",
        label: "Auditorías totales",
        description: "Análisis registrados",
        icon: "◎",
        className: "metric-blue",
    },
    {
        key: "completed_audits",
        label: "Completadas",
        description: "Auditorías finalizadas",
        icon: "✓",
        className: "metric-green",
    },
    {
        key: "pending_audits",
        label: "Pendientes",
        description: "Procesos en ejecución",
        icon: "◷",
        className: "metric-yellow",
    },
    {
        key: "active_modules",
        label: "Módulos activos",
        description: "Servicios disponibles",
        icon: "◇",
        className: "metric-purple",
    },
];

export default function StatsCards() {
    const [stats, setStats] = useState(defaultStats);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState("");

    useEffect(() => {
        loadStats();
    }, []);

    async function loadStats() {
        try {
            setError("");

            const response = await api.get("/stats");

            setStats({
                ...defaultStats,
                ...response.data.stats,
            });
        } catch (requestError) {
            console.error("Error loading stats:", requestError);

            setError(
                "No fue posible cargar las métricas de la plataforma."
            );
        } finally {
            setLoading(false);
        }
    }

    if (loading) {
        return (
            <div className="metrics-grid">
                {metricDefinitions.map((metric) => (
                    <div
                        key={metric.key}
                        className="metric-card metric-card-loading"
                    >
                        <div className="skeleton skeleton-icon" />

                        <div className="metric-content">
                            <div className="skeleton skeleton-title" />
                            <div className="skeleton skeleton-value" />
                            <div className="skeleton skeleton-text" />
                        </div>
                    </div>
                ))}
            </div>
        );
    }

    return (
        <div>
            {error && (
                <div className="inline-alert inline-alert-warning">
                    <span aria-hidden="true">!</span>

                    <p>{error}</p>

                    <button
                        type="button"
                        onClick={loadStats}
                    >
                        Reintentar
                    </button>
                </div>
            )}

            <div className="metrics-grid">
                {metricDefinitions.map((metric) => (
                    <article
                        key={metric.key}
                        className={`metric-card ${metric.className}`}
                    >
                        <div className="metric-icon">
                            {metric.icon}
                        </div>

                        <div className="metric-content">
                            <p className="metric-label">
                                {metric.label}
                            </p>

                            <p className="metric-value">
                                {stats[metric.key]}
                            </p>

                            <p className="metric-description">
                                {metric.description}
                            </p>
                        </div>
                    </article>
                ))}
            </div>
        </div>
    );
}
