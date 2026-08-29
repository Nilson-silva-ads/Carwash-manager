import { FormEvent, useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import { apiFetch } from "../api";
import type { ServiceType } from "../types";

export default function ServiceTypes() {
  const [types, setTypes] = useState<ServiceType[]>([]);
  const [name, setName] = useState("");
  const [error, setError] = useState("");

  async function load() {
    try { setTypes(await apiFetch<ServiceType[]>("/service-types")); }
    catch (err) { setError(err instanceof Error ? err.message : "Erro."); }
  }
  useEffect(() => { load(); }, []);

  async function create(event: FormEvent) {
    event.preventDefault();
    try {
      await apiFetch("/service-types", { method: "POST", body: JSON.stringify({ name }) });
      setName("");
      load();
    } catch (err) { setError(err instanceof Error ? err.message : "Erro."); }
  }

  async function toggle(type: ServiceType) {
    try {
      await apiFetch(`/service-types/${type.id}/${type.is_active ? "deactivate" : "activate"}`, { method: "PATCH" });
      load();
    } catch (err) { setError(err instanceof Error ? err.message : "Erro."); }
  }

  return (
    <>
      <PageHeader title="Tipos de serviço" description="Cadastre e controle os serviços disponíveis." />
      {error && <div className="alert error">{error}</div>}
      <div className="two-col">
        <form className="panel form-panel" onSubmit={create}>
          <h2>Novo serviço</h2>
          <label>Nome</label>
          <input value={name} onChange={(e) => setName(e.target.value)} required />
          <button className="primary">Cadastrar</button>
        </form>
        <div className="panel table-wrap">
          <table>
            <thead><tr><th>ID</th><th>Nome</th><th>Status</th><th>Ação</th></tr></thead>
            <tbody>
              {types.map((type) => (
                <tr key={type.id}>
                  <td>{type.id}</td><td>{type.name}</td>
                  <td><span className={`badge ${type.is_active ? "ok" : "off"}`}>{type.is_active ? "Ativo" : "Inativo"}</span></td>
                  <td><button className="small" onClick={() => toggle(type)}>{type.is_active ? "Desativar" : "Ativar"}</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}