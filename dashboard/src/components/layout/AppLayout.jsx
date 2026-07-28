import { useState } from "react";
import { Outlet } from "react-router-dom";

import Sidebar from "./Sidebar";
import Topbar from "./Topbar";

export default function AppLayout() {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    function openSidebar() {
        setIsSidebarOpen(true);
    }

    function closeSidebar() {
        setIsSidebarOpen(false);
    }

    return (
        <div className="app-shell">
            <Sidebar
                isOpen={isSidebarOpen}
                onClose={closeSidebar}
            />

            <div className="app-main">
                <Topbar onMenuClick={openSidebar} />

                <main className="page-content">
                    <Outlet />
                </main>
            </div>
        </div>
    );
}
