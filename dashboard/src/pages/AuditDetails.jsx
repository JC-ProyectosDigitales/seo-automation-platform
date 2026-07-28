import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import AuditResult from "../components/AuditResult";

export default function AuditDetails() {
  const { audit_id } = useParams();

  const [audit, setAudit] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;

    async function loadAudit() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(`/api/audits/${audit_id}`);

        if (!response.ok) {
          throw new Error(
            `No fue posible consultar la auditoría. Código HTTP: ${response.status}`
          );
        }

        const data = await response.json();

        if (!data.success) {
          throw new Error(
            data.message || "La API no devolvió una auditoría válida."
          );
        }

        if (!cancelled) {
          setAudit(data);
        }
      } catch (requestError) {
        if (!cancelled) {
          setError(
            requestError instanceof Error
              ? requestError.message
              : "Ocurrió un error al consultar la auditoría."
          );
        }
      } finally {
        if (!cancelled) {
          setLoading(false);
        }
      }
    }

    if (audit_id) {
      loadAudit();
    } else {
      setError("No se recibió un identificador de auditoría.");
      setLoading(false);
    }

    return () => {
      cancelled = true;
    };
  }, [audit_id]);

  if (loading) {
    return (
      <div style={{ padding: "30px" }}>
        <h1>Detalle de Auditoría</h1>
        <p>Cargando resultados de la auditoría...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: "30px" }}>
        <h1>Detalle de Auditoría</h1>

        <div
          style={{
            padding: "16px",
            border: "1px solid #EF4444",
            borderRadius: "10px"
          }}
        >
          <strong>No fue posible cargar la auditoría.</strong>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: "30px" }}>
      <h1>Detalle de Auditoría</h1>

      <AuditResult audit={audit} />
    </div>
  );
}
