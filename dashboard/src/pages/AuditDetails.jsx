import { useParams } from "react-router-dom";

import AuditResult from "../components/AuditResult";


export default function AuditDetails() {


    const { audit_id } = useParams();


    const audit = {

        audit_id: audit_id

    };


    return (

        <div style={{padding:"30px"}}>

            <h1>
                Detalle de Auditoría
            </h1>


            <AuditResult
                audit={audit}
            />


        </div>

    );

}