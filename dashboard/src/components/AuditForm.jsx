import { useState } from "react";

import api from "../api/api";

function normalizeWebsite(value) {
    const trimmedValue = value.trim();

    if (!trimmedValue) {
        return "";
    }

    if (
        trimmedValue.startsWith("http://") ||
        trimmedValue.startsWith("https://")
    ) {
        return trimmedValue;
    }

    return `https://${trimmedValue}`;
}

function validateForm(website, keyword) {
    const errors = {};

    if (!website.trim()) {
        errors.website = "Ingresa la dirección del sitio web.";
    } else {
        try {
            const normalizedWebsite = normalizeWebsite(website);
            const parsedUrl = new URL(normalizedWebsite);

            if (!parsedUrl.hostname.includes(".")) {
                errors.website =
                    "Ingresa un dominio válido, por ejemplo: ejemplo.com";
            }
        } catch {
            errors.website =
                "Ingresa una dirección válida, por ejemplo: https://ejemplo.com";
        }
    }

    if (!keyword.trim()) {
        errors.keyword = "Ingresa la palabra clave principal.";
    } else if (keyword.trim().length < 2) {
        errors.keyword =
            "La palabra clave debe contener al menos dos caracteres.";
    }

    return errors;
}

function getRequestErrorMessage(error) {
    const apiDetail = error.response?.data?.detail;
    const apiMessage = error.response?.data?.message;

    if (typeof apiDetail === "string") {
        return apiDetail;
    }

    if (typeof apiMessage === "string") {
        return apiMessage;
    }

    if (error.code === "ECONNABORTED") {
        return "La solicitud superó el tiempo máximo de espera.";
    }

    if (!error.response) {
        return "No fue posible establecer conexión con el API Gateway.";
    }

    if (error.response.status >= 500) {
        return "El servidor presentó un error al procesar la auditoría.";
    }

    return "No fue posible crear la auditoría. Revisa los datos e inténtalo nuevamente.";
}

export default function AuditForm({ onCreated }) {
    const [website, setWebsite] = useState("");
    const [keyword, setKeyword] = useState("");
    const [errors, setErrors] = useState({});
    const [requestError, setRequestError] = useState("");
    const [loading, setLoading] = useState(false);

    function handleWebsiteChange(event) {
        setWebsite(event.target.value);

        if (errors.website) {
            setErrors((currentErrors) => ({
                ...currentErrors,
                website: "",
            }));
        }
    }

    function handleKeywordChange(event) {
        setKeyword(event.target.value);

        if (errors.keyword) {
            setErrors((currentErrors) => ({
                ...currentErrors,
                keyword: "",
            }));
        }
    }

    async function handleSubmit(event) {
        event.preventDefault();

        const validationErrors = validateForm(
            website,
            keyword
        );

        if (Object.keys(validationErrors).length > 0) {
            setErrors(validationErrors);
            return;
        }

        try {
            setLoading(true);
            setErrors({});
            setRequestError("");

            const payload = {
                website: normalizeWebsite(website),
                keyword: keyword.trim(),
            };

            const response = await api.post(
                "/audit",
                payload
            );
	    
            const responseData = response.data;

            const createdAudit =
                responseData?.audit ||
                responseData?.data?.audit ||
                responseData?.data ||
                responseData?.result ||
                responseData;

            if (
                createdAudit &&
                typeof createdAudit === "object" &&
                typeof onCreated === "function"
            ) {
                onCreated(createdAudit);
            }

            setWebsite(payload.website);
            setKeyword(payload.keyword);
        } catch (error) {
            console.error(
                "Error creating audit:",
                error
            );

            setRequestError(
                getRequestErrorMessage(error)
            );
        } finally {
            setLoading(false);
        }
    }

    function handleClear() {
        setWebsite("");
        setKeyword("");
        setErrors({});
        setRequestError("");

        if (typeof onCreated === "function") {
            onCreated(null);
        }
    }

    return (
        <form
            className="audit-form"
            onSubmit={handleSubmit}
            noValidate
        >
            <div className="audit-form-heading">
                <div className="audit-form-icon">
                    ◎
                </div>

                <div>
                    <h2>Configurar auditoría</h2>

                    <p>
                        Proporciona el sitio web y la palabra clave
                        que deseas analizar.
                    </p>
                </div>
            </div>

            {requestError && (
                <div
                    className="form-alert form-alert-error"
                    role="alert"
                >
                    <div className="form-alert-icon">
                        !
                    </div>

                    <div>
                        <strong>
                            No se pudo crear la auditoría
                        </strong>

                        <p>{requestError}</p>
                    </div>
                </div>
            )}

            <div className="form-field">
                <label htmlFor="audit-website">
                    Sitio web
                    <span aria-hidden="true">*</span>
                </label>

                <div
                    className={
                        errors.website
                            ? "input-wrapper input-wrapper-error"
                            : "input-wrapper"
                    }
                >
                    <span
                        className="input-prefix"
                        aria-hidden="true"
                    >
                        ↗
                    </span>

                    <input
                        id="audit-website"
                        name="website"
                        type="text"
                        inputMode="url"
                        autoComplete="url"
                        placeholder="https://ejemplo.com"
                        value={website}
                        disabled={loading}
                        aria-invalid={Boolean(errors.website)}
                        aria-describedby={
                            errors.website
                                ? "website-error"
                                : "website-help"
                        }
                        onChange={handleWebsiteChange}
                    />
                </div>

                {errors.website ? (
                    <p
                        id="website-error"
                        className="field-message field-message-error"
                    >
                        {errors.website}
                    </p>
                ) : (
                    <p
                        id="website-help"
                        className="field-message"
                    >
                        Puedes escribir el dominio con o sin
                        https://
                    </p>
                )}
            </div>

            <div className="form-field">
                <label htmlFor="audit-keyword">
                    Palabra clave principal
                    <span aria-hidden="true">*</span>
                </label>

                <div
                    className={
                        errors.keyword
                            ? "input-wrapper input-wrapper-error"
                            : "input-wrapper"
                    }
                >
                    <span
                        className="input-prefix"
                        aria-hidden="true"
                    >
                        #
                    </span>

                    <input
                        id="audit-keyword"
                        name="keyword"
                        type="text"
                        autoComplete="off"
                        placeholder="Ejemplo: marketing digital"
                        value={keyword}
                        disabled={loading}
                        aria-invalid={Boolean(errors.keyword)}
                        aria-describedby={
                            errors.keyword
                                ? "keyword-error"
                                : "keyword-help"
                        }
                        onChange={handleKeywordChange}
                    />
                </div>

                {errors.keyword ? (
                    <p
                        id="keyword-error"
                        className="field-message field-message-error"
                    >
                        {errors.keyword}
                    </p>
                ) : (
                    <p
                        id="keyword-help"
                        className="field-message"
                    >
                        Esta keyword será utilizada por los
                        módulos de análisis SEO.
                    </p>
                )}
            </div>

            <div className="audit-form-information">
                <div className="information-icon">
                    i
                </div>

                <p>
                    La plataforma enviará la auditoría a los
                    módulos registrados en el API Gateway y
                    almacenará sus resultados.
                </p>
            </div>

            <div className="audit-form-actions">
                <button
                    type="button"
                    className="secondary-button"
                    disabled={loading}
                    onClick={handleClear}
                >
                    Limpiar
                </button>

                <button
                    type="submit"
                    className="primary-button audit-submit-button"
                    disabled={loading}
                >
                    {loading ? (
                        <>
                            <span className="button-spinner" />
                            Ejecutando auditoría...
                        </>
                    ) : (
                        <>
                            <span aria-hidden="true">▶</span>
                            Iniciar auditoría
                        </>
                    )}
                </button>
            </div>
        </form>
    );
}
