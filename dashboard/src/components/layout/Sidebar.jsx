import { NavLink } from "react-router-dom";

const navigationItems = [
    {
        path: "/",
        label: "Resumen",
        icon: "⌂",
        end: true,
    },
    {
        path: "/new-audit",
        label: "Nueva auditoría",
        icon: "+",
    },
    {
        path: "/history",
        label: "Historial",
        icon: "◷",
    },
    {
        path: "/modules",
        label: "Módulos",
        icon: "◇",
    },
];

export default function Sidebar({ isOpen, onClose }) {
    function getNavClass({ isActive }) {
        return isActive
            ? "sidebar-link sidebar-link-active"
            : "sidebar-link";
    }

    return (
        <>
            {isOpen && (
                <button
                    type="button"
                    className="sidebar-overlay"
                    aria-label="Cerrar menú"
                    onClick={onClose}
                />
            )}

            <aside
                className={
                    isOpen
                        ? "sidebar sidebar-open"
                        : "sidebar"
                }
            >
                <div className="sidebar-brand">
                    <div className="sidebar-logo">
                        SEO
                    </div>

                    <div>
                        <p className="sidebar-brand-title">
                            SEO Platform
                        </p>

                        <p className="sidebar-brand-subtitle">
                            Automation Suite
                        </p>
                    </div>
                </div>

                <nav className="sidebar-navigation">
                    <p className="sidebar-section-title">
                        Plataforma
                    </p>

                    {navigationItems.map((item) => (
                        <NavLink
                            key={item.path}
                            to={item.path}
                            end={item.end}
                            className={getNavClass}
                            onClick={onClose}
                        >
                            <span
                                className="sidebar-link-icon"
                                aria-hidden="true"
                            >
                                {item.icon}
                            </span>

                            <span>{item.label}</span>
                        </NavLink>
                    ))}
                </nav>

                <div className="sidebar-footer">
                    <div className="sidebar-status">
                        <span className="status-dot" />

                        <div>
                            <p className="sidebar-status-title">
                                Plataforma activa
                            </p>

                            <p className="sidebar-status-text">
                                Servicios conectados
                            </p>
                        </div>
                    </div>
                </div>
            </aside>
        </>
    );
}
