import { useEffect, useState } from "react";

import { Link } from "react-router-dom";

import api from "../api/api";


function AuditHistory() {


    const [audits, setAudits] = useState([]);

    const [loading, setLoading] = useState(true);



    useEffect(() => {

        loadAudits();

    }, []);



    async function loadAudits() {


        try {

            const response = await api.get("/audits");

            setAudits(
                response.data.audits
            );


        } catch(error) {

            console.error(
                error
            );

        }
        finally {

            setLoading(false);

        }

    }



    if (loading) {

        return <p>Cargando auditorías...</p>;

    }



    return (

        <div>


            <h2>
                Historial de Auditorías
            </h2>


            <table>


                <thead>

                    <tr>

                        <th>
                            Audit ID
                        </th>

                        <th>
                            Sitio
                        </th>

                        <th>
                            Keyword
                        </th>

                        <th>
                            Estado
                        </th>

                        <th>
                            Fecha
                        </th>

                        <th>
                            Acción
                        </th>


                    </tr>


                </thead>



                <tbody>


                    {
                        audits.map((audit)=>(


                            <tr
                                key={audit.audit_id}
                            >


                                <td>
                                    {audit.audit_id}
                                </td>


                                <td>
                                    {audit.website}
                                </td>


                                <td>
                                    {audit.keyword}
                                </td>


                                <td>
                                    {audit.status}
                                </td>


                                <td>
                                    {
                                        new Date(
                                            audit.created_at
                                        )
                                        .toLocaleString()
                                    }
                                </td>


                                <td>

                                    <Link
                                        to={`/audit/${audit.audit_id}`}
                                    >

                                        Ver resultado

                                    </Link>


                                </td>


                            </tr>


                        ))
                    }


                </tbody>


            </table>


        </div>

    );


}


export default AuditHistory;