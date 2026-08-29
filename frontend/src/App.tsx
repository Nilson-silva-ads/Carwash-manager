import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./auth";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import ServiceOrders from "./pages/ServiceOrders";
import NewServiceOrder from "./pages/NewServiceOrder";
import Employees from "./pages/Employees";
import ServiceTypes from "./pages/ServiceTypes";
import Reports from "./pages/Reports";

function Protected() {
  const { employee, loading } = useAuth();
  if (loading) return <div className="loading-screen">Carregando...</div>;
  if (!employee) return <Navigate to="/login" replace />;
  return <Layout />;
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route element={<Protected />}>
        <Route index element={<Navigate to="/dashboard" replace />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/service-orders" element={<ServiceOrders />} />
        <Route path="/service-orders/new" element={<NewServiceOrder />} />
        <Route path="/employees" element={<Employees />} />
        <Route path="/service-types" element={<ServiceTypes />} />
        <Route path="/reports" element={<Reports />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}