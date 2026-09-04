import { FormEvent, useState } from "react";
import PageHeader from "../components/PageHeader";
import { apiFetch } from "../api";
import type { ServiceOrder } from "../types";

function toDateBoundary(date: string, boundary: "start" | "end") {
  const time = boundary === "start" ? "00:00:00" : "23:59:59";
  return `${date}T${time}`;
}

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
    if (start) params.set("start_date", toDateBoundary(start, "start"));
    if (end) params.set("end_date", toDateBoundary(end, "end"));

    try {
      const data = await apiFetch<ServiceOrder[]>(`/service-orders?${params}`);
      setOrders(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro na consulta.");
    }
  }

  return (
    <>
      <PageHeader title="Atendimentos" description="Consulte os veiculos registrados." />
      <form className="panel filters" onSubmit={search}>
        <div><label>Placa</label><input value={plate} onChange={(e) => setPlate(e.target.value)} placeholder="ABC1234" /></div>
        <div><label>Data inicial</label><input type="date" value={start} onChange={(e) => setStart(e.target.value)} /></div>
        <div><label>Data final</label><input type="date" value={end} onChange={(e) => setEnd(e.target.value)} /></div>
        <button className="primary" type="submit">Pesquisar</button>
      </form>

      {error && <div className="alert error">{error}</div>}

      <div className="panel table-wrap">
        <table>
          <thead><tr><th>ID</th><th>Placa</th><th>Funcionário</th><th>Serviços</th><th>Data</th></tr></thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>#{order.id}</td>
                <td><strong>{order.plate}</strong></td>
                <td>{order.employee?.name?? "Não informado"}</td>
                <td> {order.items?.length? order.items.map((item) => item.service_type.name).join(", "): "Nenhum serviço" } </td>
                <td>{new Date(order.created_at).toLocaleString("pt-BR", { timeZone: "America/Recife" })}</td>
              </tr>
            ))}
            {!orders.length && <tr><td colSpan={5} className="empty">Nenhum atendimento encontrado.</td></tr>}
          </tbody>
        </table>
      </div>
    </>
  );
}
