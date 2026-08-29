import { FormEvent, useState } from "react";
import PageHeader from "../components/PageHeader";
import { apiFetch } from "../api";
import type { MonthlyReport, ServiceOrderReport } from "../types";

const months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];

export default function Reports() {
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [year, setYear] = useState(new Date().getFullYear());
  const [period, setPeriod] = useState<ServiceOrderReport | null>(null);
  const [monthly, setMonthly] = useState<MonthlyReport[]>([]);
  const [error, setError] = useState("");

  async function periodReport(event: FormEvent) {
    event.preventDefault();
    setError("");
    try {
      const params = new URLSearchParams({
        start_date: new Date(start).toISOString(),
        end_date: new Date(end).toISOString(),
      });
      setPeriod(await apiFetch<ServiceOrderReport>(`/reports/service-orders?${params}`));
    } catch (err) { setError(err instanceof Error ? err.message : "Erro."); }
  }

  async function monthlyReport() {
    setError("");
    try {
      setMonthly(await apiFetch<MonthlyReport[]>(`/reports/monthly?year=${year}`));
    } catch (err) { setError(err instanceof Error ? err.message : "Erro."); }
  }

  return (
    <>
      <PageHeader title="Relatórios" description="Indicadores de atendimentos e serviços." />
      {error && <div className="alert error">{error}</div>}

      <div className="report-grid">
        <form className="panel form-panel" onSubmit={periodReport}>
          <h2>Por período</h2>
          <label>Data inicial</label><input type="datetime-local" value={start} onChange={(e) => setStart(e.target.value)} required />
          <label>Data final</label><input type="datetime-local" value={end} onChange={(e) => setEnd(e.target.value)} required />
          <button className="primary">Gerar</button>
          {period && (
            <div className="report-result">
              <strong>{period.total_service_orders}</strong>
              <span>atendimentos</span>
              {period.services.map((s) => <div key={s.service_type_id}>{s.name}: <b>{s.total}</b></div>)}
            </div>
          )}
        </form>

        <div className="panel form-panel">
          <h2>Mensal</h2>
          <label>Ano</label><input type="number" value={year} onChange={(e) => setYear(Number(e.target.value))} />
          <button className="primary" onClick={monthlyReport}>Gerar relatório</button>
          <div className="monthly">
            {monthly.map((item) => (
              <div className="month-row" key={item.month}>
                <span>{months[item.month - 1]}</span>
                <div className="bar"><i style={{width: `${Math.min(item.total_service_orders * 12, 100)}%`}} /></div>
                <strong>{item.total_service_orders}</strong>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}