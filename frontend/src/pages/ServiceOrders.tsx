import { FormEvent, useState } from "react";
import PageHeader from "../components/PageHeader";
import { apiFetch } from "../api";
import type { ServiceOrder } from "../types";

export default function ServiceOrders() {
  const [plate, setPlate] = useState("");
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [orders, setOrders] = useState<ServiceOrder[]>([]);
  const [error, setError] = useState("");

  async function search(event?: FormEvent) {
    event?.preventDefault();
    setError("");

    const params = new URLSearchParams();
    if (plate) params.set("plate", plate.trim().toUpperCase());
    if (start) params.set("start_date", new Date(start).toISOString());
    if (end) params.set("end_date", new Date(end).toISOString());

    try {
      const data = await apiFetch<ServiceOrder[]>(`/service-orders?${params}`);
      setOrders(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro na consulta.");
    }
  }

  return (
    <>
      <PageHeader title="Atendimentos" description="Consulte os atendimentos registrados." />
      <form className="panel filters" onSubmit={search}>
        <div><label>Placa</label><input value={plate} onChange={(e) => setPlate(e.target.value)} placeholder="ABC1234" /></div>
        <div><label>Data inicial</label><input type="datetime-local" value={start} onChange={(e) => setStart(e.target.value)} /></div>
        <div><label>Data final</label><input type="datetime-local" value={end} onChange={(e) => setEnd(e.target.value)} /></div>
        <button className="primary" type="submit">Pesquisar</button>
      </form>

      {error && <div className="alert error">{error}</div>}

      <div className="panel table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Placa</th><th>Funcionário</th><th>Data</th></tr></thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>#{order.id}</td>
                <td><strong>{order.plate}</strong></td>
                <td>{order.employee?.name?? "Não informado"}</td>
                <td>{new Date(order.created_at).toLocaleString("pt-BR")}</td>
              </tr>
            ))}
            {!orders.length && <tr><td colSpan={4} className="empty">Nenhum atendimento encontrado.</td></tr>}
          </tbody>
        </table>
      </div>
    </>
  );
}