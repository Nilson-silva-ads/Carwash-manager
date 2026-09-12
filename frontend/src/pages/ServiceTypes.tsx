import { FormEvent, useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import { apiFetch } from "../api";
import type { ServiceType } from "../types";
import LoadingSpinner from "../components/LoadingSpinner";

export default function ServiceTypes() {
  const [types, setTypes] = useState<ServiceType[]>([]);
  const [name, setName] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  async function load() {
    setLoading(true);
    try { setTypes(await apiFetch<ServiceType[]>("/service-types")); }
    catch (err) { setError(err instanceof Error ? err.message : "Erro."); }
    finally { setLoading(false); }
  }
  useEffect(() => { load(); }, []);

  async function create(event: FormEvent) {
    event.preventDefault();
    setSaving(true);
    try {
      await apiFetch("/service-types", { method: "POST", body: JSON.stringify({ name }) });
      setName("");
      load();
    } catch (err) { setError(err instanceof Error ? err.message : "Erro."); }
    finally { setSaving(false); }
  }

  async function toggle(type: ServiceType) {
    setSaving(true);
    try {
      await apiFetch(`/service-types/${type.id}/${type.is_active ? "deactivate" : "activate"}`, { method: "PATCH" });
      load();
    } catch (err) { setError(err instanceof Error ? err.message : "Erro."); }
    finally { setSaving(false); }
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
          <button className="primary" disabled={saving}>{saving ? <LoadingSpinner label="Salvando" /> : "Cadastrar"}</button>
        </form>
        <div className="panel table-wrap">
          <table>
            <thead><tr><th>Nome</th><th>Status</th><th>Ação</th></tr></thead>
            <tbody>
              {loading ? <tr><td colSpan={3} className="empty"><LoadingSpinner /></td></tr> : types.map((type) => (
                <tr key={type.id}>
                  <td>{type.name}</td>
                  <td><span className={`badge ${type.is_active ? "ok" : "off"}`}>{type.is_active ? "Ativo" : "Inativo"}</span></td>
                  <td><button className="small" disabled={saving} onClick={() => toggle(type)}>{saving ? <span className="spinner" /> : type.is_active ? "Desativar" : "Ativar"}</button></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}
