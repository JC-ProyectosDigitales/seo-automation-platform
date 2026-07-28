import { useEffect, useMemo, useState } from "react";

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

function validateForm(website, keyword, selectedModules) {
    const errors = {};

    if (!website.trim()) {
        errors.website = "Ingresa la dirección del sitio web.";
    } else {
        try {
            const parsedUrl = new URL(
                normalizeWebsite(website)
            );

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
        errors.keyword =
            "Ingresa la palabra clave principal.";
    } else if (keyword.trim().length < 2) {
        errors.keyword =
            "La palabra clave debe contener al menos dos caracteres.";
    }

    if (selectedModules.length === 0) {
        errors.modules =
            "Selecciona al menos un módulo para ejecutar.";
    }

    return errors;
}

function getRequestErrorMessage(error) {
    const detail = error.response?.data?.detail;
    const message = error.response?.data?.message;
    const apiError = error.response?.data?.error;

    if (typeof detail === "string") {
        return detail;
    }

    if (typeof message === "string") {
        return message;
    }

    if (typeof apiError === "string") {
        return apiError;
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

function getCreatedAudit(responseData) {
    const auditId =
        responseData?.audit_id ||
        responseData?.data?.audit_id ||
        responseData?.audit?.audit_id ||
        responseData?.data?.audit?.audit_id;

    const status =
        responseData?.status ||
        responseData?.data?.status ||
        responseData?.audit?.status ||
        "pending";

    if (!auditId) {
        return null;
    }

    return {
        ...responseData,
        audit_id: auditId,
        status,
    };
}

export default function AuditForm({ onCreated }) {
    const [website, setWebsite] = useState("");
    const [keyword, setKeyword] = useState("");

    const [modules, setModules] = useState([]);
    const [selectedModules, setSelectedModules] =
        useState([]);

    const [errors, setErrors] = useState({});
    const [requestError, setRequestError] =
        useState("");

    const [loading, setLoading] = useState(false);
    const [loadingModules, setLoadingModules] =
        useState(true);
    const [modulesError, setModulesError] =
        useState("");

    useEffect(() => {
        loadModules();
    }, []);

    async function loadModules() {
        try {
            setLoadingModules(true);
            setModulesError("");

            const response = await api.get("/modules");

            const activeModules = Array.isArray(
                response.data?.modules
            )
                ? response.data.modules.filter(
                      (module) => module.active
                  )
                : [];

            setModules(activeModules);

            setSelectedModules(
                activeModules.map(
                    (module) => module.name
                )
            );
        } catch (error) {
            console.error(
                "Error loading modules:",
                error
            );

            setModulesError(
                "No fue posible cargar los módulos registrados."
            );
        } finally {
            setLoadingModules(false);
        }
    }

    const allModulesSelected = useMemo(() => {
        return (
            modules.length > 0 &&
            selectedModules.length === modules.length
        );
    }, [modules, selectedModules]);

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

    function toggleModule(moduleName) {
        setSelectedModules((currentModules) => {
            if (currentModules.includes(moduleName)) {
                return currentModules.filter(
                    (name) => name !== moduleName
                );
            }

            return [
                ...currentModules,
                moduleName,
            ];
        });

        if (errors.modules) {
            setErrors((currentErrors) => ({
                ...currentErrors,
                modules: "",
            }));
        }
    }

    function toggleAllModules() {
        if (allModulesSelected) {
            setSelectedModules([]);
            return;
        }

        setSelectedModules(
            modules.map((module) => module.name)
        );

        if (errors.modules) {
            setErrors((currentErrors) => ({
                ...currentErrors,
                modules: "",
            }));
        }
    }

    async function handleSubmit(event) {
        event.preventDefault();

        const validationErrors = validateForm(
            website,
            keyword,
            selectedModules
        );

        if (
            Object.keys(validationErrors).length > 0
        ) {
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
                modules: selectedModules,
            };

            const response = await api.post(
                "/audit",
                payload
            );

            const createdAudit = getCreatedAudit(
                response.data
            );

            if (!createdAudit) {
                throw new Error(
                    "El API Gateway no devolvió un audit_id."
                );
            }

            if (
                typeof onCreated === "function"
            ) {
                onCreated(createdAudit);
            }
        } catch (error) {
            console.error(
                "Error creating audit:",
                error
            );

            setRequestError(
                error.message ===
                    "El API Gateway no devolvió un audit_id."
                    ? error.message
                    : getRequestErrorMessage(error)
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

        setSelectedModules(
            modules.map((module) => module.name)
        );

        if (
            typeof onCreated === "function"
        ) {
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
                        Proporciona el sitio, la palabra
                        clave y los módulos que deseas
                        ejecutar.
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
                        aria-invalid={Boolean(
                            errors.website
                        )}
                        onChange={handleWebsiteChange}
                    />
                </div>

                <p
                    className={
                        errors.website
                            ? "field-message field-message-error"
                            : "field-message"
                    }
                >
                    {errors.website ||
                        "Puedes escribir el dominio con o sin https://"}
                </p>
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
                        aria-invalid={Boolean(
                            errors.keyword
                        )}
                        onChange={handleKeywordChange}
                    />
                </div>

                <p
                    className={
                        errors.keyword
                            ? "field-message field-message-error"
                            : "field-message"
                    }
                >
                    {errors.keyword ||
                        "La keyword será utilizada por los módulos de análisis."}
                </p>
            </div>

            <div className="form-field">
                <div className="module-selector-heading">
                    <div>
                        <label>
                            Módulos de análisis
                            <span aria-hidden="true">
                                *
                            </span>
                        </label>

                        <p className="field-message">
                            Selecciona los servicios que
                            participarán en la auditoría.
                        </p>
                    </div>

                    {!loadingModules &&
                        modules.length > 0 && (
                            <button
                                type="button"
                                className="text-action-button"
                                disabled={loading}
                                onClick={toggleAllModules}
                            >
                                {allModulesSelected
                                    ? "Deseleccionar todos"
                                    : "Seleccionar todos"}
                            </button>
                        )}
                </div>

                {loadingModules && (
                    <div className="module-selector-loading">
                        <span className="button-spinner" />
                        Cargando módulos...
                    </div>
                )}

                {!loadingModules &&
                    modulesError && (
                        <div className="inline-alert inline-alert-warning">
                            <span aria-hidden="true">
                                !
                            </span>

                            <p>{modulesError}</p>

                            <button
                                type="button"
                                onClick={loadModules}
                            >
                                Reintentar
                            </button>
                        </div>
                    )}

                {!loadingModules &&
                    !modulesError &&
                    modules.length === 0 && (
                        <div className="form-alert form-alert-error">
                            <div className="form-alert-icon">
                                !
                            </div>

                            <div>
                                <strong>
                                    No hay módulos activos
                                </strong>

                                <p>
                                    Registra o activa un
                                    módulo antes de ejecutar
                                    una auditoría.
                                </p>
                            </div>
                        </div>
                    )}

                {!loadingModules &&
                    modules.length > 0 && (
                        <div className="module-selector-grid">
                            {modules.map((module) => {
                                const selected =
                                    selectedModules.includes(
                                        module.name
                                    );

                                return (
                                    <button
                                        key={module.id}
                                        type="button"
                                        className={
                                            selected
                                                ? "module-selector-card module-selector-card-selected"
                                                : "module-selector-card"
                                        }
                                        disabled={loading}
                                        onClick={() =>
                                            toggleModule(
                                                module.name
                                            )
                                        }
                                    >
                                        <span className="module-selector-check">
                                            {selected
                                                ? "✓"
                                                : ""}
                                        </span>

                                        <span className="module-selector-content">
                                            <strong>
                                                {
                                                    module.name
                                                }
                                            </strong>

                                            <small>
                                                {module.description ||
                                                    "Módulo SEO registrado"}
                                            </small>
                                        </span>
                                    </button>
                                );
                            })}
                        </div>
                    )}

                {errors.modules && (
                    <p className="field-message field-message-error">
                        {errors.modules}
                    </p>
                )}
            </div>

            <div className="audit-form-information">
                <div className="information-icon">
                    i
                </div>

                <p>
                    El API Gateway registrará la auditoría
                    y ejecutará los módulos seleccionados
                    en segundo plano.
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
                    disabled={
                        loading ||
                        loadingModules ||
                        modules.length === 0
                    }
                >
                    {loading ? (
                        <>
                            <span className="button-spinner" />
                            Registrando auditoría...
                        </>
                    ) : (
                        <>
                            <span aria-hidden="true">
                                ▶
                            </span>
                            Iniciar auditoría
                        </>
                    )}
                </button>
            </div>
        </form>
    );
}
