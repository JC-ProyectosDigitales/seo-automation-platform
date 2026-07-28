import {
    BrowserRouter,
    Navigate,
    Route,
    Routes,
} from "react-router-dom";

import AppLayout from "./components/layout/AppLayout";

import AuditDetails from "./pages/AuditDetails";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import Modules from "./pages/Modules";
import NewAudit from "./pages/NewAudit";

function App() {
    return (
        <BrowserRouter>
            <Routes>
                <Route element={<AppLayout />}>
                    <Route
                        path="/"
                        element={<Dashboard />}
                    />

                    <Route
                        path="/new-audit"
                        element={<NewAudit />}
                    />

                    <Route
                        path="/history"
                        element={<History />}
                    />

                    <Route
                        path="/modules"
                        element={<Modules />}
                    />

                    <Route
                        path="/audit/:audit_id"
                        element={<AuditDetails />}
                    />
                </Route>

                <Route
                    path="*"
                    element={<Navigate to="/" replace />}
                />
            </Routes>
        </BrowserRouter>
    );
}

export default App;
