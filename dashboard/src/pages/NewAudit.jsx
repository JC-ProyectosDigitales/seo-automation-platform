import { useState } from "react";
import { Link } from "react-router-dom";

import AuditForm from "../components/AuditForm";
import AuditResult from "../components/AuditResult";

export default function NewAudit() {
    const [audit, setAudit] = useState(null);

    return (
        <div className="new-audit-page">
            <section className="audit-introduction">
                <div>
                    <span className="page-eyebrow">
                        Análisis SEO
                    </span>

                    <h2>
                        Ejecuta una auditoría completa de tu sitio
                    </h2>

                    <p>
                        La plataforma coordinará los módulos SEO
                        registrados para analizar el sitio web,
                        almacenar los resultados y generar
                        recomendaciones.
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
                    <AuditForm onCreated={setAudit} />
                </section>

                <aside className="audit-process-card">
                    <div className="section-heading">
                        <h2>Proceso de auditoría</h2>

                        <p>
                            La solicitud atravesará las siguientes
                            etapas.
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
                                    Se valida el dominio y la
                                    palabra clave ingresada.
                                </p>
                            </div>
                        </li>

                        <li className="process-item">
                            <span className="process-number">
                                2
                            </span>

                            <div>
                                <h3>API Gateway</h3>

                                <p>
                                    El Gateway registra la
                                    auditoría y coordina los
                                    servicios.
                                </p>
                            </div>
                        </li>

                        <li className="process-item">
                            <span className="process-number">
                                3
                            </span>

                            <div>
                                <h3>Módulos SEO</h3>

                                <p>
                                    Los módulos ejecutan sus
                                    comprobaciones especializadas.
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
                                    Los resultados quedan
                                    almacenados para su consulta.
                                </p>
                            </div>
                        </li>
                    </ol>

                    <div className="audit-module-summary">
                        <span className="status-dot" />

                        <div>
                            <strong>
                                Servicios disponibles
                            </strong>

                            <p>
                                Content, OnPage, Technical y
                                Monitor
                            </p>
                        </div>
                    </div>
                </aside>
            </div>

            {audit && (
    <section className="content-card audit-result-section">
        <div className="result-section-heading">
            <div>
                <span className="page-eyebrow">
                    Auditoría creada
                </span>

                <h2>Resultado de la solicitud</h2>
            </div>

            {audit.audit_id && (
                <Link
                    to={`/audit/${audit.audit_id}`}
                    className="primary-button"
                >
                    Ver detalle completo
                    <span aria-hidden="true">→</span>
                </Link>
            )}
        </div>

        <div className="audit-created-message">
            <div className="audit-created-icon">
                ✓
            </div>

            <div>
                <h3>
                    La auditoría fue registrada correctamente
                </h3>

                <p>
                    La solicitud fue enviada a los módulos SEO y
                    ya se encuentra disponible en el historial.
                </p>
            </div>
        </div>

        <AuditResult audit={audit} />
    </section>
)}
        </div>
    );
}
