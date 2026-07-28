import { Link } from "react-router-dom";

import QuickActions from "../components/QuickActions";
import RecentAudits from "../components/RecentAudits";
import StatsCards from "../components/StatsCards";

export default function Dashboard() {
    return (
        <div className="dashboard-page">
            <section className="welcome-panel">
                <div className="welcome-content">
                    <div className="welcome-badge">
                        SEO Automation Platform
                    </div>

                    <h2>
                        Controla tus auditorías SEO desde un solo lugar
                    </h2>

                    <p>
                        Ejecuta análisis, revisa el estado de los
                        módulos y consulta los resultados almacenados
                        por la plataforma.
                    </p>

                    <div className="welcome-actions">
                        <Link
                            to="/new-audit"
                            className="primary-button"
                        >
                            <span aria-hidden="true">+</span>
                            Nueva auditoría
                        </Link>

                        <Link
                            to="/history"
                            className="secondary-button"
                        >
                            Ver historial
                        </Link>
                    </div>
                </div>

                <div
                    className="welcome-visual"
                    aria-hidden="true"
                >
                    <div className="visual-orbit visual-orbit-large" />
                    <div className="visual-orbit visual-orbit-small" />

                    <div className="visual-score">
                        <span>SEO</span>
                        <strong>100</strong>
                        <small>Objetivo</small>
                    </div>
                </div>
            </section>

            <section>
                <div className="section-heading">
                    <div>
                        <h2>Resumen general</h2>

                        <p>
                            Métricas actuales de la plataforma y sus
                            servicios.
                        </p>
                    </div>
                </div>

                <StatsCards />
            </section>

            <QuickActions />

            <RecentAudits />
        </div>
    );
}
