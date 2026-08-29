import { FormEvent, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Car, ClipboardList, Plus, Search } from "lucide-react";
import PageHeader from "../components/PageHeader";
import { useAuth } from "../auth";
import { apiFetch } from "../api";
import type { ServiceOrder, ServiceType } from "../types";

export default function Dashboard() {
  const { employee } = useAuth();
  const [plate, setPlate] = useState("");
  const [types, setTypes] = useState<ServiceType[]>([]);
  const [selected, setSelected] = useState<number[]>([]);
  const [lastOrder, setLastOrder] = useState<ServiceOrder | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    if (!employee || employee.is_admin) return;

    setLoading(true);
    Promise.all([
      apiFetch<ServiceType[]>("/service-types"),
      apiFetch<ServiceOrder[]>(`/service-orders/employee/${employee.id}`),
    ])
      .then(([serviceTypes, orders]) => {
        setTypes(serviceTypes.filter((type) => type.is_active));
        setLastOrder(orders[0] ?? null);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Não foi possível carregar os dados."))
      .finally(() => setLoading(false));
  }, [employee]);

  function toggleService(id: number) {
    setSelected((current) =>
      current.includes(id) ? current.filter((serviceId) => serviceId !== id) : [...current, id]
    );
  }

  async function registerServiceOrder(event: FormEvent) {
    event.preventDefault();
    setError("");
    setMessage("");

    if (!selected.length) {
      setError("Selecione pelo menos um serviço.");
      return;
    }

    try {
      const order = await apiFetch<ServiceOrder>("/service-orders", {
        method: "POST",
        body: JSON.stringify({
          plate: plate.trim().toUpperCase(),
          service_type_ids: selected,
        }),
      });
      setLastOrder(order);
      setPlate("");
      setSelected([]);
      setMessage("Atendimento registrado com sucesso.");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Não foi possível registrar o atendimento.");
    }
  }

  return (
    <>
      <PageHeader
        title={`Olá, ${employee?.name || employee?.username}!`}
        description={employee?.is_admin ? "Visão geral do Carwash Manager." : "Registre um serviço e acompanhe seu último veículo cadastrado."}
      />

      {employee?.is_admin ? (
        <>
          <div className="cards">
            <div className="stat-card">
              <div className="stat-icon"><Car /></div>
              <div><span>Atendimentos</span><strong>Consulte os registros</strong></div>
            </div>
            <div className="stat-card">
              <div className="stat-icon"><ClipboardList /></div>
              <div><span>Operação</span><strong>Sistema conectado à API</strong></div>
            </div>
          </div>
          <div className="quick-grid">
            <Link to="/service-orders/new" className="quick-card">
              <Plus /><strong>Novo atendimento</strong><span>Registrar uma lavagem</span>
            </Link>
            <Link to="/service-orders" className="quick-card">
              <Search /><strong>Consultar atendimentos</strong><span>Pesquisar por placa, funcionário ou data</span>
            </Link>
          </div>
        </>
      ) : (
        <div className="employee-dashboard">
          <form className="panel form-panel" onSubmit={registerServiceOrder}>
            <h2>Cadastrar veículo e atendimento</h2>
            <p className="panel-description">Informe a placa e os serviços realizados.</p>
            {error && <div className="alert error">{error}</div>}
            {message && <div className="alert success">{message}</div>}
            <label>Placa do veículo</label>
            <input value={plate} onChange={(event) => setPlate(event.target.value)} maxLength={10} placeholder="ABC1234" required />
            <label>Tipos de serviço</label>
            <div className="check-grid">
              {types.map((type) => (
                <label key={type.id} className={`check-card ${selected.includes(type.id) ? "selected" : ""}`}>
                  <input type="checkbox" checked={selected.includes(type.id)} onChange={() => toggleService(type.id)} />
                  <span>{type.name}</span>
                </label>
              ))}
            </div>
            <button className="primary" type="submit" disabled={loading}>Registrar atendimento</button>
          </form>

          <aside className="panel last-vehicle">
            <h2>Último veículo cadastrado</h2>
            {loading ? <p className="panel-description">Carregando...</p> : lastOrder ? (
              <>
                <strong>{lastOrder.plate}</strong>
                <span>Atendimento #{lastOrder.id}</span>
                <span>{new Date(lastOrder.created_at).toLocaleString("pt-BR")}</span>
              </>
            ) : <p className="panel-description">Você ainda não cadastrou nenhum veículo.</p>}
          </aside>
        </div>
      )}
    </>
  );
}