import { Link, useNavigate } from "react-router-dom";

import AuditForm from "../components/AuditForm";

export default function NewAudit() {
    const navigate = useNavigate();

    function handleCreated(audit) {
        if (!audit?.audit_id) {
            return;
        }

        navigate(`/audit/${audit.audit_id}`);
    }

    return (
        <div className="new-audit-page">
            <section className="audit-introduction">
                <div>
                    <span className="page-eyebrow">
                        Análisis SEO
                    </span>

                    <h2>
                        Ejecuta una auditoría completa de tu
                        sitio
                    </h2>

                    <p>
                        Selecciona los módulos que participarán
                        en el análisis. El API Gateway
                        coordinará la ejecución y almacenará
                        todos los resultados.
                    </p>
                </div>

                <Link
                    to="/history"
                    className="secondary-button"
                >
                    Consultar historial
                </Link>
            </section>

            <div className="audit-workspace">
                <section className="content-card audit-form-card">
                    <AuditForm
                        onCreated={handleCreated}
                    />
                </section>

                <aside className="audit-process-card">
                    <div className="section-heading">
                        <h2>Proceso de auditoría</h2>

                        <p>
                            La solicitud atravesará las
                            siguientes etapas.
                        </p>
                    </div>

                    <ol className="process-list">
                        <li className="process-item">
                            <span className="process-number">
                                1
                            </span>

                            <div>
                                <h3>Validación</h3>

                                <p>
                                    Se valida el dominio, la
                                    keyword y los módulos.
                                </p>
                            </div>
                        </li>

                        <li className="process-item">
                            <span className="process-number">
                                2
                            </span>

                            <div>
                                <h3>Registro</h3>

                                <p>
                                    El Gateway crea un
                                    identificador único.
                                </p>
                            </div>
                        </li>

                        <li className="process-item">
                            <span className="process-number">
                                3
                            </span>

                            <div>
                                <h3>Ejecución</h3>

                                <p>
                                    Los microservicios analizan
                                    el sitio web.
                                </p>
                            </div>
                        </li>

                        <li className="process-item">
                            <span className="process-number">
                                4
                            </span>

                            <div>
                                <h3>Resultados</h3>

                                <p>
                                    El dashboard consulta y
                                    presenta la auditoría.
                                </p>
                            </div>
                        </li>
                    </ol>

                    <div className="audit-module-summary">
                        <span className="status-dot" />

                        <div>
                            <strong>
                                Arquitectura conectada
                            </strong>

                            <p>
                                Gateway y cuatro servicios SEO
                            </p>
                        </div>
                    </div>
                </aside>
            </div>
        </div>
    );
}
