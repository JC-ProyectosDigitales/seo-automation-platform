import { useLocation } from "react-router-dom";

const pageInformation = {
    "/": {
        title: "Resumen",
        description: "Estado general de la plataforma SEO",
    },
    "/new-audit": {
        title: "Nueva auditoría",
        description: "Analiza un sitio web y consulta sus resultados",
    },
    "/history": {
        title: "Historial",
        description: "Consulta las auditorías realizadas",
    },
    "/modules": {
        title: "Módulos",
        description: "Revisa los servicios conectados al API Gateway",
    },
};

function getPageInformation(pathname) {
    if (pathname.startsWith("/audit/")) {
        return {
            title: "Detalle de auditoría",
            description: "Resultados completos del análisis SEO",
        };
    }

    return (
        pageInformation[pathname] || {
            title: "SEO Automation Platform",
            description: "Panel de administración",
        }
    );
}

export default function Topbar({ onMenuClick }) {
    const location = useLocation();
    const page = getPageInformation(location.pathname);

    return (
        <header className="topbar">
            <div className="topbar-left">
                <button
                    type="button"
                    className="menu-button"
                    aria-label="Abrir menú"
                    onClick={onMenuClick}
                >
                    ☰
                </button>

                <div>
                    <h1 className="topbar-title">
                        {page.title}
                    </h1>

                    <p className="topbar-description">
                        {page.description}
                    </p>
                </div>
            </div>

            <div className="topbar-right">
                <div className="environment-badge">
                    <span className="status-dot" />
                    Producción
                </div>

                <div
                    className="user-avatar"
                    aria-label="Usuario"
                    title="Administrador"
                >
                    Z
                </div>
            </div>
        </header>
    );
}
