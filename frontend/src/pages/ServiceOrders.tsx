import { FormEvent, useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import { apiFetch } from "../api";
import { useAuth } from "../auth";
import type { ServiceOrder, ServiceType } from "../types";

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
  const [serviceTypes, setServiceTypes] = useState<ServiceType[]>([]);
  const [editing, setEditing] = useState<ServiceOrder | null>(null);
  const [editPlate, setEditPlate] = useState("");
  const [editServiceIds, setEditServiceIds] = useState<number[]>([]);
  const { employee } = useAuth();

  useEffect(() => {
    if (employee?.is_admin) apiFetch<ServiceType[]>("/service-types").then(setServiceTypes).catch(() => undefined);
  }, [employee?.is_admin]);

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

  function startEdit(order: ServiceOrder) {
    setEditing(order);
    setEditPlate(order.plate);
    setEditServiceIds(order.items?.map((item) => item.service_type_id ?? item.service_type.id) ?? []);
    setError("");
  }

  async function saveEdit(event: FormEvent) {
    event.preventDefault();
    if (!editing) return;
    try {
      await apiFetch(`/service-orders/${editing.id}`, {
        method: "PUT",
        body: JSON.stringify({ plate: editPlate, service_type_ids: editServiceIds }),
      });
      setEditing(null);
      await search();
    } catch (err) { setError(err instanceof Error ? err.message : "Erro ao atualizar atendimento."); }
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
          <thead><tr><th>ID</th><th>Placa</th><th>Funcionário</th><th>Serviços</th><th>Data</th>{employee?.is_admin && <th className="actions-column">Ações</th>}</tr></thead>
          <tbody>
            {orders.map((order) => (
              <tr key={order.id}>
                <td>#{order.id}</td>
                <td><strong>{order.plate}</strong></td>
                <td>{order.employee?.name?? "Não informado"}</td>
                <td> {order.items?.length? order.items.map((item) => item.service_type.name).join(", "): "Nenhum serviço" } </td>
                <td>{new Date(order.created_at).toLocaleString("pt-BR", { timeZone: "America/Recife" })}</td>
                {employee?.is_admin && <td className="actions-column"><button className="edit-button" type="button" onClick={() => startEdit(order)}>Editar</button></td>}
              </tr>
            ))}
            {!orders.length && <tr><td colSpan={employee?.is_admin ? 6 : 5} className="empty">Nenhum atendimento encontrado.</td></tr>}
          </tbody>
        </table>
      </div>
      {editing && <div className="panel form-panel">
        <h2>Editar atendimento #{editing.id}</h2>
        <form onSubmit={saveEdit}>
          <label>Placa</label>
          <input value={editPlate} onChange={(e) => setEditPlate(e.target.value)} maxLength={10} required />
          <label>Serviços</label>
          <div>{serviceTypes.map((type) => <label key={type.id}><input type="checkbox" checked={editServiceIds.includes(type.id)} onChange={(e) => setEditServiceIds((ids) => e.target.checked ? [...ids, type.id] : ids.filter((id) => id !== type.id))} /> {type.name}</label>)}</div>
          <button className="primary" type="submit">Salvar alterações</button>
          <button type="button" onClick={() => setEditing(null)}>Cancelar</button>
        </form>
      </div>}
    </>
  );
}
