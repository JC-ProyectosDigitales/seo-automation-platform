import { useEffect, useState } from "react";
import api from "../api/api";

export default function ModuleTable() {

    const [modules, setModules] = useState([]);

    useEffect(() => {

        loadModules();

    }, []);

    async function loadModules() {

        const response = await api.get("/modules");

        setModules(response.data.modules);

    }

    return (

        <div>

            <h2>Módulos</h2>

            <table border="1">

                <thead>

                    <tr>

                        <th>ID</th>

                        <th>Nombre</th>

                        <th>Activo</th>

                        <th>Prioridad</th>

                    </tr>

                </thead>

                <tbody>

                    {

                        modules.map(module => (

                            <tr key={module.id}>

                                <td>{module.id}</td>

                                <td>{module.name}</td>

                                <td>

                                    {module.active ? "Sí" : "No"}

                                </td>

                                <td>

                                    {module.priority}

                                </td>

                            </tr>

                        ))

                    }

                </tbody>

            </table>

        </div>

    );

}