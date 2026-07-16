import { useState } from "react";
import api from "../api/api";

export default function AuditForm({ onCreated }) {

    const [website, setWebsite] = useState("");
    const [keyword, setKeyword] = useState("");

    async function handleSubmit(e) {

        e.preventDefault();

        const response = await api.post(
            "/audit",
            {
                website,
                keyword
            }
        );

        onCreated(response.data);

    }

    return (

        <form onSubmit={handleSubmit}>

            <h2>Nueva Auditoría</h2>

            <input
                type="text"
                placeholder="Website"
                value={website}
                onChange={(e)=>setWebsite(e.target.value)}
            />

            <br /><br />

            <input
                type="text"
                placeholder="Keyword"
                value={keyword}
                onChange={(e)=>setKeyword(e.target.value)}
            />

            <br /><br />

            <button>

                Ejecutar Auditoría

            </button>

        </form>

    );

}