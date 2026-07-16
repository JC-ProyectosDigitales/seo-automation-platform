import { useEffect, useState } from "react";
import api from "../api/api";

export default function AuditResult({ audit }) {

    const [result, setResult] = useState(null);

    useEffect(() => {

        if (!audit) return;

        const auditId = audit.audit_id;

        async function loadAudit() {

            try {

                const response = await api.get(`/audits/${auditId}`);

                setResult(response.data);

                if (response.data.status === "completed") {

                    clearInterval(interval);

                }

            } catch (error) {

                console.error(error);

            }

        }

        loadAudit();

        const interval = setInterval(loadAudit, 1000);

        return () => clearInterval(interval);

    }, [audit]);



    if (!result) return null;



    return (

        <div>

            <h2>Resultado de la Auditoría</h2>

            <p>

                <strong>Audit ID:</strong> {result.audit_id}

            </p>

            <p>

                <strong>Status:</strong> {result.status}

            </p>

            <p>

                <strong>Website:</strong> {result.website}

            </p>

            <p>

                <strong>Keyword:</strong> {result.keyword}

            </p>

            <hr />

            <h3>Resultados por módulo</h3>

            {

                Object.entries(result.results).map(

                    ([name, module]) => (

                        <div
                            key={name}
                            style={{
                                border: "1px solid #ccc",
                                padding: 15,
                                marginBottom: 15
                            }}
                        >

                            <h4>{name}</h4>

                            <p>

                                Prioridad: {module.priority}

                            </p>

                            <p>

                                Timeout: {module.timeout}s

                            </p>

                            <pre>

                                {JSON.stringify(module.result, null, 2)}

                            </pre>

                        </div>

                    )

                )

            }

        </div>

    );

}