import { BrowserRouter, Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import Modules from "./pages/Modules";
import History from "./pages/History";
import AuditDetails from "./pages/AuditDetails";


function App() {

    return (

        <BrowserRouter>

            <Routes>


                <Route
                    path="/"
                    element={<Dashboard />}
                />


                <Route
                    path="/modules"
                    element={<Modules />}
                />


                <Route
                    path="/history"
                    element={<History />}
                />


                <Route
                    path="/audit/:audit_id"
                    element={<AuditDetails />}
                />


            </Routes>

        </BrowserRouter>

    );

}


export default App;