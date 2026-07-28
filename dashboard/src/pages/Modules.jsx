import ModuleTable from "../components/ModuleTable";

export default function Modules() {
    return (
        <div className="modules-page">
            <section className="modules-page-heading">
                <div>
                    <span className="page-eyebrow">
                        Microservicios
                    </span>

                    <h2>
                        Módulos registrados
                    </h2>

                    <p>
                        Consulta los servicios conectados al
                        API Gateway y controla su estado.
                    </p>
                </div>
            </section>

            <section className="content-card">
                <ModuleTable />
            </section>
        </div>
    );
}
