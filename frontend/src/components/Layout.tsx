import { NavLink, Outlet } from "react-router-dom";
import {
  BarChart3,
  Car,
  ClipboardList,
  Droplets,
  LogOut,
  Menu,
  Settings,
  Users,
  X,
} from "lucide-react";
import { useState } from "react";
import { useAuth } from "../auth";

export default function Layout() {
  const { employee, signOut } = useAuth();
  const [open, setOpen] = useState(false);

  const links = [
    { to: "/dashboard", label: "Dashboard", icon: BarChart3 },
    { to: "/service-orders", label: "Atendimentos", icon: ClipboardList },
    { to: "/service-orders/new", label: "Novo atendimento", icon: Car },
    ...(employee?.is_admin
      ? [
          { to: "/employees", label: "Funcionários", icon: Users },
          { to: "/service-types", label: "Tipos de serviço", icon: Settings },
          { to: "/reports", label: "Relatórios", icon: BarChart3 },
        ]
      : []),
  ];

  return (
    <div className="app-shell">
      <aside className={`sidebar ${open ? "sidebar-open" : ""}`}>
        <div className="brand">
          <Droplets size={24} />
          <span>Carwash Manager</span>
          <button className="mobile-close" onClick={() => setOpen(false)}>
            <X />
          </button>
        </div>

        <nav>
          {links.map(({ to, label, icon: Icon }) => (
            <NavLink
              key={to}
              to={to}
              onClick={() => setOpen(false)}
              className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}
            >
              <Icon size={19} />
              {label}
            </NavLink>
          ))}
        </nav>

        <button className="logout" onClick={signOut}>
          <LogOut size={18} />
          Sair
        </button>
      </aside>

      <main className="main">
        <header className="topbar">
          <button className="mobile-menu" onClick={() => setOpen(true)}>
            <Menu />
          </button>
          <div>
            <strong>{employee?.name || employee?.username}</strong>
            <span>{employee?.is_admin ? "Administrador" : "Funcionário"}</span>
          </div>
        </header>
        <section className="content">
          <Outlet />
        </section>
      </main>
    </div>
  );
}