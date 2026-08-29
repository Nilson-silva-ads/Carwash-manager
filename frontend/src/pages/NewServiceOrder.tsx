import { FormEvent, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import PageHeader from "../components/PageHeader";
import { apiFetch } from "../api";
import type { ServiceType } from "../types";

export default function NewServiceOrder() {
  const navigate = useNavigate();
  const [plate, setPlate] = useState("");
  const [types, setTypes] = useState<ServiceType[]>([]);
  const [selected, setSelected] = useState<number[]>([]);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    apiFetch<ServiceType[]>("/service-types")
      .then(setTypes)
      .catch((err) => setError(err.message));
  }, []);

  function toggle(id: number) {
    setSelected((current) =>
      current.includes(id) ? current.filter((x) => x !== id) : [...current, id]
    );
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setMessage("");

    if (!selected.length) {
      setError("Selecione pelo menos um serviço.");
      return;
    }

    try {
      await apiFetch("/service-orders", {
        method: "POST",
        body: JSON.stringify({
          plate: plate.trim().toUpperCase(),
          service_type_ids: selected,
        }),
      });
      setMessage("Atendimento criado com sucesso.");
      setPlate("");
      setSelected([]);
      setTimeout(() => navigate("/service-orders"), 700);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao criar atendimento.");
    }
  }

  return (
    <>
      <PageHeader title="Novo atendimento" description="Registre os serviços realizados no veículo." />
      <form className="panel form-panel" onSubmit={submit}>
        {error && <div className="alert error">{error}</div>}
        {message && <div className="alert success">{message}</div>}

        <label>Placa</label>
        <input
          value={plate}
          onChange={(e) => setPlate(e.target.value)}
          maxLength={10}
          placeholder="ABC1234"
          required
        />

        <label>Tipos de serviço</label>
        <div className="check-grid">
          {types.filter((type) => type.is_active).map((type) => (
            <label key={type.id} className={`check-card ${selected.includes(type.id) ? "selected" : ""}`}>
              <input
                type="checkbox"
                checked={selected.includes(type.id)}
                onChange={() => toggle(type.id)}
              />
              <span>{type.name}</span>
            </label>
          ))}
        </div>

        <button className="primary" type="submit">Registrar atendimento</button>
      </form>
    </>
  );
}