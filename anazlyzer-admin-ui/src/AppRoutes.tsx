import React from 'react';
import { Routes, Route, Navigate, Outlet } from 'react-router-dom';
import Dashboard from './components/pages/Dashboard';
import Home from './components/pages/Home';
import AlertSystem from './components/pages/AlertSystem';
import Monitoring from './components/pages/Monitoring';
import Settings from './components/pages/Settings';
import Article from './components/pages/configuration/Article';
import LoginPage from './components/security/LoginPage';
import { useAuth } from './components/security/auth/AuthContext';
import AppLayout from './components/Layout'; // ADD THIS
import Scheduler from './components/pages/configuration/Scheduler';

const PrivateRoute: React.FC = () => {
    const { user, loading } = useAuth();

    if (loading) return <div>Loading...</div>;
    return user ? <Outlet /> : <Navigate to="/login" replace />;
};

const AppRoutes: React.FC = () => {
    return (
        <Routes>
            <Route path="/login" element={<LoginPage />} />

            {/* PROTECTED ROUTES */}
            <Route element={<PrivateRoute />}>
                <Route element={<AppLayout />}>
                    {/* <Route path="/dashboard" element={<Dashboard />} /> */}
                    <Route path="/home" element={<Home />} />
                    <Route path="/alert-system" element={<AlertSystem />} />
                    <Route path="/configuration/article" element={<Article />} />
                    <Route path="/configuration/scheduler" element={<Scheduler />} />
                    <Route path="/monitoring" element={<Monitoring />} />
                    <Route path="/settings" element={<Settings />} />
                </Route>
            </Route>

            {/* Default route */}
            <Route path="*" element={<Navigate to="/home" replace />} />
        </Routes>
    );
};

export default AppRoutes;
