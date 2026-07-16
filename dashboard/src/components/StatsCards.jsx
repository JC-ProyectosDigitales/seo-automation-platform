import { useEffect, useState } from "react";

import api from "../api/api";


export default function StatsCards() {


    const [stats, setStats] = useState(null);



    useEffect(() => {

        loadStats();

    }, []);



    async function loadStats() {

        try {

            const response = await api.get("/stats");

            setStats(
                response.data.stats
            );


        } catch(error) {

            console.error(
                "Error loading stats:",
                error
            );

        }

    }



    if (!stats) {

        return (

            <p>
                Cargando métricas...
            </p>

        );

    }



    return (

        <div
            style={{
                display: "flex",
                gap: "20px",
                justifyContent: "center",
                marginBottom: "30px"
            }}
        >


            <div>

                <h3>
                    Auditorías
                </h3>

                <p>
                    {stats.total_audits}
                </p>

            </div>



            <div>

                <h3>
                    Completadas
                </h3>

                <p>
                    {stats.completed_audits}
                </p>

            </div>



            <div>

                <h3>
                    Pendientes
                </h3>

                <p>
                    {stats.pending_audits}
                </p>

            </div>



            <div>

                <h3>
                    Módulos activos
                </h3>

                <p>
                    {stats.active_modules}
                </p>

            </div>



        </div>

    );

}