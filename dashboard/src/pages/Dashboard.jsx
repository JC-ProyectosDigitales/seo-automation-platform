import { useState } from "react";

import AuditForm from "../components/AuditForm";
import AuditResult from "../components/AuditResult";
import ModuleTable from "../components/ModuleTable";
import StatsCards from "../components/StatsCards";

export default function Dashboard() {

    const [audit, setAudit] = useState(null);

    return (

        <div style={{padding:"30px"}}>

            <h1>

                SEO Automation Platform

            </h1>

            <StatsCards />


            <AuditForm

                onCreated={setAudit}

            />

            <hr />

            <AuditResult audit={audit} />

            <hr />

            <ModuleTable />

        </div>

    );

}