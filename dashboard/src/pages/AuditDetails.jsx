import { useEffect, useState } from "react";
import {
  useNavigate,
  useParams
} from "react-router-dom";

import AuditResult from "../components/AuditResult";

const PROCESSING_STATUSES = [
  "pending",
  "running",
  "processing"
];

const POLLING_INTERVAL = 2000;

function isAuditProcessing(status) {
  return PROCESSING_STATUSES.includes(
    String(status || "").toLowerCase()
  );
}

export default function AuditDetails() {
  const { audit_id } = useParams();
  const navigate = useNavigate();

  const [audit, setAudit] = useState(null);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(false);
  const [downloading, setDownloading] =
    useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    let cancelled = false;
    let pollingTimeout = null;

    async function loadAudit(
      isInitialRequest = false
    ) {
      try {
        if (isInitialRequest) {
          setLoading(true);
        }

        setError("");

        const response = await fetch(
          `/api/audits/${audit_id}`,
          {
            method: "GET",
            headers: {
              Accept: "application/json"
            },
            cache: "no-store"
          }
        );

        if (!response.ok) {
          throw new Error(
            `No fue posible consultar la auditoría. Código HTTP: ${response.status}`
          );
        }

        const data = await response.json();

        if (!data.success) {
          throw new Error(
            data.message ||
              "La API no devolvió una auditoría válida."
          );
        }

        if (cancelled) {
          return;
        }

        setAudit(data);

        if (isAuditProcessing(data.status)) {
          pollingTimeout = window.setTimeout(
            () => loadAudit(false),
            POLLING_INTERVAL
          );
        }
      } catch (requestError) {
        if (cancelled) {
          return;
        }

        setError(
          requestError instanceof Error
            ? requestError.message
            : "Ocurrió un error al consultar la auditoría."
        );
      } finally {
        if (!cancelled && isInitialRequest) {
          setLoading(false);
        }
      }
    }

    if (audit_id) {
      loadAudit(true);
    } else {
      setError(
        "No se recibió un identificador de auditoría."
      );
      setLoading(false);
    }

    return () => {
      cancelled = true;

      if (pollingTimeout) {
        window.clearTimeout(
          pollingTimeout
        );
      }
    };
  }, [audit_id]);

  async function handleDownloadReport() {
    try {
      setDownloading(true);
      setError("");

      const response = await fetch(
        `/api/audits/${audit_id}/report`,
        {
          method: "GET",
          headers: {
            Accept: "application/pdf"
          },
          cache: "no-store"
        }
      );

      if (!response.ok) {
        let message =
          `No fue posible generar el reporte. Código HTTP: ${response.status}`;

        const contentType =
          response.headers.get(
            "content-type"
          ) || "";

        if (
          contentType.includes(
            "application/json"
          )
        ) {
          const data =
            await response.json();

          message =
            data.detail ||
            data.message ||
            message;
        }

        throw new Error(message);
      }

      const blob = await response.blob();

      const objectUrl =
        window.URL.createObjectURL(
          blob
        );

      const link =
        document.createElement("a");

      link.href = objectUrl;
      link.download =
        `reporte-${audit_id}.pdf`;

      document.body.appendChild(link);

      link.click();
      link.remove();

      window.URL.revokeObjectURL(
        objectUrl
      );
    } catch (downloadError) {
      setError(
        downloadError instanceof Error
          ? downloadError.message
          : "Ocurrió un error al descargar el reporte."
      );
    } finally {
      setDownloading(false);
    }
  }

  async function handleDeleteAudit() {
    const confirmed = window.confirm(
      `¿Deseas eliminar la auditoría ${audit_id}?\n\nEsta acción no se puede deshacer.`
    );

    if (!confirmed) {
      return;
    }

    try {
      setDeleting(true);
      setError("");

      const response = await fetch(
        `/api/audits/${audit_id}`,
        {
          method: "DELETE",
          headers: {
            Accept: "application/json"
          }
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.message ||
            `No fue posible eliminar la auditoría. Código HTTP: ${response.status}`
        );
      }

      if (!data.success) {
        throw new Error(
          data.message ||
            "La API no confirmó la eliminación."
        );
      }

      navigate("/history", {
        replace: true
      });
    } catch (deleteError) {
      setError(
        deleteError instanceof Error
          ? deleteError.message
          : "Ocurrió un error al eliminar la auditoría."
      );
    } finally {
      setDeleting(false);
    }
  }

  if (loading) {
    return (
      <div style={{ padding: "30px" }}>
        <h1>Detalle de Auditoría</h1>

        <p>
          Cargando resultados de la
          auditoría...
        </p>
      </div>
    );
  }

  if (error && !audit) {
    return (
      <div style={{ padding: "30px" }}>
        <h1>Detalle de Auditoría</h1>

        <div
          style={{
            padding: "16px",
            border:
              "1px solid #EF4444",
            borderRadius: "10px"
          }}
        >
          <strong>
            No fue posible cargar la
            auditoría.
          </strong>

          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div style={{ padding: "30px" }}>
      <div
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent:
            "space-between",
          flexWrap: "wrap",
          gap: "16px",
          marginBottom: "24px"
        }}
      >
        <h1 style={{ margin: 0 }}>
          Detalle de Auditoría
        </h1>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            flexWrap: "wrap",
            gap: "10px"
          }}
        >
          <button
            type="button"
            onClick={
              handleDownloadReport
            }
            disabled={
              downloading ||
              isAuditProcessing(
                audit?.status
              )
            }
            style={{
              padding: "10px 16px",
              border:
                "1px solid #3B82F6",
              borderRadius: "8px",
              background: downloading
                ? "#1E3A8A"
                : "#3B82F6",
              color: "#FFFFFF",
              fontWeight: "600",
              cursor:
                downloading ||
                isAuditProcessing(
                  audit?.status
                )
                  ? "not-allowed"
                  : "pointer",
              opacity:
                downloading ||
                isAuditProcessing(
                  audit?.status
                )
                  ? 0.7
                  : 1
            }}
          >
            {downloading
              ? "Generando reporte..."
              : "Descargar reporte PDF"}
          </button>

          <button
            type="button"
            onClick={
              handleDeleteAudit
            }
            disabled={
              deleting ||
              downloading
            }
            style={{
              padding: "10px 16px",
              border:
                "1px solid #EF4444",
              borderRadius: "8px",
              background: deleting
                ? "#7F1D1D"
                : "#EF4444",
              color: "#FFFFFF",
              fontWeight: "600",
              cursor:
                deleting ||
                downloading
                  ? "not-allowed"
                  : "pointer",
              opacity:
                deleting ||
                downloading
                  ? 0.7
                  : 1
            }}
          >
            {deleting
              ? "Eliminando..."
              : "Eliminar auditoría"}
          </button>
        </div>
      </div>

      {isAuditProcessing(
        audit?.status
      ) && (
        <div
          style={{
            marginBottom: "16px",
            padding: "12px 16px",
            border:
              "1px solid #FACC15",
            borderRadius: "10px",
            background:
              "rgba(250, 204, 21, 0.08)"
          }}
        >
          <strong>
            La auditoría continúa en
            proceso.
          </strong>

          <p style={{ marginBottom: 0 }}>
            El reporte PDF estará
            disponible cuando todos los
            módulos terminen.
          </p>
        </div>
      )}

      {error && (
        <div
          style={{
            marginBottom: "16px",
            padding: "12px 16px",
            border:
              "1px solid #EF4444",
            borderRadius: "10px"
          }}
        >
          <strong>
            No fue posible completar la
            operación.
          </strong>

          <p>{error}</p>
        </div>
      )}

      <AuditResult audit={audit} />
    </div>
  );
}
