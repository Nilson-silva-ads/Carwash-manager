import { FormEvent, useState } from "react";
import PageHeader from "../components/PageHeader";
import { apiFetch } from "../api";
import type { EmployeeMonthlyReport, MonthlyReport, ServiceOrderReport } from "../types";

const months = [
  "Jan",
  "Fev",
  "Mar",
  "Abr",
  "Mai",
  "Jun",
  "Jul",
  "Ago",
  "Set",
  "Out",
  "Nov",
  "Dez",
];

export default function Reports() {
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [year, setYear] = useState(new Date().getFullYear());
  const [period, setPeriod] = useState<ServiceOrderReport | null>(null);
  const [monthly, setMonthly] = useState<MonthlyReport[]>([]);
  const [employeeMonth, setEmployeeMonth] = useState<EmployeeMonthlyReport | null>(null);
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [error, setError] = useState("");

  async function periodReport(event: FormEvent) {
    event.preventDefault();
    setError("");

    try {
      const params = new URLSearchParams({
        start_date: `${start}T00:00:00`,
        end_date: `${end}T23:59:59`,
      });

      setPeriod(
        await apiFetch<ServiceOrderReport>(
          `/reports/service-orders?${params}`
        )
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro.");
    }
  }

  async function annualReport() {
    setError("");

    try {
      setMonthly(
        await apiFetch<MonthlyReport[]>(
          `/reports/monthly?year=${year}`
        )
      );
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro.");
    }
  }

  async function employeeMonthlyReport() {
    setError("");
    try {
      setEmployeeMonth(await apiFetch<EmployeeMonthlyReport>(`/reports/monthly/employee?year=${year}&month=${month}`));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro.");
    }
  }

  return (
    <>
      <PageHeader
        title="Relatórios"
        description="Indicadores de atendimentos e serviços."
      />

      {error && <div className="alert error">{error}</div>}

      <div className="report-grid">
        <form className="panel form-panel" onSubmit={periodReport}>
          <h2>Por período</h2>

          <label>Data inicial</label>
          <input
            type="date"
            value={start}
            onChange={(e) => setStart(e.target.value)}
            required
          />

          <label>Data final</label>
          <input
            type="date"
            value={end}
            onChange={(e) => setEnd(e.target.value)}
            required
          />

          <button className="primary" type="submit">
            Gerar
          </button>

          {period && (
            <div className="report-result">
              <strong>{period.total_service_orders}</strong>
              <span>atendimentos</span>

              {period.services.map((s) => (
                <div key={s.service_type_id}>
                  {s.name}: <b>{s.total}</b>
                </div>
              ))}
            </div>
          )}
        </form>

        <div className="panel form-panel">
          <h2>Relatório Anual</h2>

          <label>Ano</label>
          <input
            type="number"
            value={year}
            onChange={(e) => setYear(Number(e.target.value))}
          />

          <button
            className="primary"
            type="button"
            onClick={annualReport}
          >
            Gerar relatório
          </button>

          <div className="monthly">
            {monthly.map((item) => (
              <div className="month-row" key={item.month}>
                <span>{months[item.month - 1]}</span>

                <div className="bar">
                  <i
                    style={{
                      width: `${Math.min(
                        item.total_service_orders * 12,
                        100
                      )}%`,
                    }}
                  />
                </div>

                <strong>{item.total_service_orders}</strong>
              </div>
            ))}
          </div>
        </div>

        <div className="panel form-panel">
          <h2>Produtividade mensal</h2>
          <label>Ano</label>
          <input type="number" value={year} onChange={(e) => setYear(Number(e.target.value))} />
          <label>Mês</label>
          <select value={month} onChange={(e) => setMonth(Number(e.target.value))}>
            {months.map((name, index) => <option key={index + 1} value={index + 1}>{name}</option>)}
          </select>
          <button className="primary" type="button" onClick={employeeMonthlyReport}>Gerar relatório</button>
          {employeeMonth && <div className="report-result">
            <strong>{employeeMonth.total_service_orders}</strong><span>atendimentos</span>
            {employeeMonth.employees.map((employee) => <div key={employee.employee_id} className="employee-report">
              <h3>{employee.employee_name} — {employee.total} carros</h3>
              {employee.services.map((service) => <div key={service.service_type_id}>{service.name}: <b>{service.total}</b></div>)}
            </div>)}
          </div>}
        </div>
      </div>
    </>
  );
}
