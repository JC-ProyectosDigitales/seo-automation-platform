import { Link } from "react-router-dom";

const actions = [
    {
        title: "Nueva auditoría",
        description:
            "Analiza un sitio web utilizando los módulos SEO disponibles.",
        path: "/new-audit",
        icon: "+",
        className: "quick-action-primary",
        buttonText: "Iniciar análisis",
    },
    {
        title: "Consultar historial",
        description:
            "Revisa las auditorías ejecutadas y abre sus resultados.",
        path: "/history",
        icon: "◷",
        className: "quick-action-secondary",
        buttonText: "Ver historial",
    },
    {
        title: "Revisar módulos",
        description:
            "Consulta los servicios registrados en el API Gateway.",
        path: "/modules",
        icon: "◇",
        className: "quick-action-secondary",
        buttonText: "Ver módulos",
    },
];

export default function QuickActions() {
    return (
        <section>
            <div className="section-heading">
                <div>
                    <h2>Acciones rápidas</h2>

                    <p>
                        Accede a las funciones principales de la
                        plataforma.
                    </p>
                </div>
            </div>

            <div className="quick-actions-grid">
                {actions.map((action) => (
                    <article
                        key={action.path}
                        className={`quick-action-card ${action.className}`}
                    >
                        <div className="quick-action-icon">
                            {action.icon}
                        </div>

                        <div className="quick-action-content">
                            <h3>{action.title}</h3>

                            <p>{action.description}</p>
                        </div>

                        <Link
                            to={action.path}
                            className="quick-action-link"
                        >
                            {action.buttonText}

                            <span aria-hidden="true">→</span>
                        </Link>
                    </article>
                ))}
            </div>
        </section>
    );
}
