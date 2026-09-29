import { FormEvent, useEffect, useState } from "react";
import { Download, FileBarChart2, UsersRound, Wrench } from "lucide-react";
import PageHeader from "../components/PageHeader";
import { apiFetch } from "../api";
import type { DashboardReport, Employee, EmployeeMonthlyReport, MonthlyReport, ServiceOrderReport, ServiceType } from "../types";

const months = ["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"];

function escapeCell(value: string | number) {
  return String(value).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/\"/g, "&quot;");
}

function downloadExcel(title: string, columns: string[], rows: Array<Array<string | number>>, filename: string) {
  const header = columns.map((column) => `<th>${escapeCell(column)}</th>`).join("");
  const body = rows.map((row) => `<tr>${row.map((cell) => `<td>${escapeCell(cell)}</td>`).join("")}</tr>`).join("");
  const html = `<!DOCTYPE html><html><head><meta charset="UTF-8"><meta name="ProgId" content="Excel.Sheet"><style>table{border-collapse:collapse}th{background:#1d4ed8;color:#fff}th,td{border:1px solid #cbd5e1;padding:8px;text-align:left}</style></head><body><table><caption>${escapeCell(title)}</caption><thead><tr>${header}</tr></thead><tbody>${body}</tbody></table></body></html>`;
  const blob = new Blob([html], { type: "application/vnd.ms-excel;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `${filename}.xls`;
  document.body.appendChild(link);
  link.click();
  link.remove();
  URL.revokeObjectURL(url);
}

export default function Reports() {
  const [start, setStart] = useState("");
  const [end, setEnd] = useState("");
  const [employeeId, setEmployeeId] = useState("");
  const [serviceTypeId, setServiceTypeId] = useState("");
  const [employees, setEmployees] = useState<Employee[]>([]);
  const [serviceTypes, setServiceTypes] = useState<ServiceType[]>([]);
  const [dashboard, setDashboard] = useState<DashboardReport | null>(null);
  const [period, setPeriod] = useState<ServiceOrderReport | null>(null);
  const [loadingPeriod, setLoadingPeriod] = useState(false);
  const [annualYear, setAnnualYear] = useState(new Date().getFullYear());
  const [monthly, setMonthly] = useState<MonthlyReport[]>([]);
  const [loadingAnnual, setLoadingAnnual] = useState(false);
  const [employeeYear, setEmployeeYear] = useState(new Date().getFullYear());
  const [month, setMonth] = useState(new Date().getMonth() + 1);
  const [employeeMonth, setEmployeeMonth] = useState<EmployeeMonthlyReport | null>(null);
  const [loadingEmployee, setLoadingEmployee] = useState(false);
  const [error, setError] = useState("");
  const maxMonthlyOrders = Math.max(...monthly.map((item) => item.total_service_orders), 1);

  useEffect(() => {
    Promise.all([apiFetch<DashboardReport>("/reports/dashboard"), apiFetch<Employee[]>("/employees"), apiFetch<ServiceType[]>("/service-types")])
      .then(([dashboardData, employeeData, typeData]) => {
        setDashboard(dashboardData);
        setEmployees(employeeData.filter((employee) => employee.is_active));
        setServiceTypes(typeData);
      })
      .catch((err) => setError(err instanceof Error ? err.message : "Não foi possível carregar o resumo dos relatórios."));
  }, []);

  async function periodReport(event: FormEvent) {
    event.preventDefault();
    setError("");
    if (new Date(start) > new Date(end)) {
      setError("A data inicial não pode ser maior que a data final.");
      return;
    }
    setLoadingPeriod(true);
    try {
      const params = new URLSearchParams({ start_date: `${start}T00:00:00`, end_date: `${end}T23:59:59` });
      if (employeeId) params.set("employee_id", employeeId);
      if (serviceTypeId) params.set("service_type_id", serviceTypeId);
      setPeriod(await apiFetch<ServiceOrderReport>(`/reports/service-orders?${params}`));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro ao carregar relatório por período.");
    } finally {
      setLoadingPeriod(false);
    }
  }

  async function annualReport() {
    setError("");
    setLoadingAnnual(true);
    try { setMonthly(await apiFetch<MonthlyReport[]>(`/reports/monthly?year=${annualYear}`)); }
    catch (err) { setError(err instanceof Error ? err.message : "Erro ao carregar relatório anual."); }
    finally { setLoadingAnnual(false); }
  }

  async function employeeMonthlyReport() {
    setError("");
    setLoadingEmployee(true);
    try { setEmployeeMonth(await apiFetch<EmployeeMonthlyReport>(`/reports/monthly/employee?year=${employeeYear}&month=${month}`)); }
    catch (err) { setError(err instanceof Error ? err.message : "Erro ao carregar produtividade mensal."); }
    finally { setLoadingEmployee(false); }
  }

  return (
    <div className="reports-page">
      <PageHeader title="Relatórios" description="Acompanhe os resultados e exporte seus dados para o Excel." />
      {error && <div className="alert error">{error}</div>}
      <section className="report-summary" aria-label="Resumo de atendimentos">
        {[{ label: "Hoje", value: dashboard?.today, icon: FileBarChart2 }, { label: "Este mês", value: dashboard?.month, icon: Wrench }, { label: "Total", value: dashboard?.total, icon: UsersRound }].map(({ label, value, icon: Icon }) => (
          <article className="report-summary-card" key={label}><span className="report-summary-icon"><Icon size={21} /></span><div><span>{label}</span><strong>{value ?? "—"}</strong><small>atendimentos</small></div></article>
        ))}
      </section>
      <div className="reports-layout">
        <form className="panel report-panel" onSubmit={periodReport}>
          <div className="report-panel-heading"><div><h2>Por período</h2><p>Filtre os atendimentos para uma análise detalhada.</p></div></div>
          <div className="report-filter-grid">
            <label>Data inicial<input type="date" value={start} onChange={(event) => setStart(event.target.value)} required /></label>
            <label>Data final<input type="date" value={end} onChange={(event) => setEnd(event.target.value)} required /></label>
            <label>Funcionário<select value={employeeId} onChange={(event) => setEmployeeId(event.target.value)}><option value="">Todos</option>{employees.map((employee) => <option key={employee.id} value={employee.id}>{employee.name}</option>)}</select></label>
            <label>Tipo de serviço<select value={serviceTypeId} onChange={(event) => setServiceTypeId(event.target.value)}><option value="">Todos</option>{serviceTypes.map((type) => <option key={type.id} value={type.id}>{type.name}</option>)}</select></label>
          </div>
          <div className="report-actions"><button className="primary" type="submit" disabled={loadingPeriod}>{loadingPeriod ? "Consultando..." : "Consultar relatório"}</button>{period && <button className="secondary" type="button" onClick={() => downloadExcel("Relatório por período", ["Serviço", "Quantidade"], [["Atendimentos", period.total_service_orders], ...period.services.map((service) => [service.name, service.total])], "relatorio-por-periodo")}><Download size={17} /> Baixar Excel</button>}</div>
          {period && <div className="report-result report-data"><strong>{period.total_service_orders}</strong><span>atendimentos encontrados</span>{period.services.length ? period.services.map((service) => <div className="report-line" key={service.service_type_id}><span>{service.name}</span><b>{service.total}</b></div>) : <p>Nenhum serviço registrado com estes filtros.</p>}</div>}
        </form>
        <div className="panel report-panel">
          <div className="report-panel-heading"><div><h2>Relatório anual</h2><p>Volume de atendimentos por mês.</p></div></div>
          <label>Ano<input type="number" value={annualYear} onChange={(event) => setAnnualYear(Number(event.target.value))} /></label>
          <div className="report-actions"><button className="primary" type="button" onClick={annualReport} disabled={loadingAnnual}>{loadingAnnual ? "Consultando..." : "Consultar relatório"}</button>{monthly.length > 0 && <button className="secondary" type="button" onClick={() => downloadExcel(`Relatório anual ${annualYear}`, ["Mês", "Atendimentos"], monthly.map((item) => [months[item.month - 1], item.total_service_orders]), `relatorio-anual-${annualYear}`)}><Download size={17} /> Baixar Excel</button>}</div>
          <div className="monthly">{monthly.map((item) => <div className="month-row" key={item.month}><span>{months[item.month - 1]}</span><div className="bar"><i style={{ width: `${(item.total_service_orders / maxMonthlyOrders) * 100}%` }} /></div><strong>{item.total_service_orders}</strong></div>)}</div>
        </div>
        <div className="panel report-panel productivity-panel">
          <div className="report-panel-heading"><div><h2>Produtividade mensal</h2><p>Resultados por funcionário e tipo de serviço.</p></div></div>
          <div className="report-filter-grid compact"><label>Ano<input type="number" value={employeeYear} onChange={(event) => setEmployeeYear(Number(event.target.value))} /></label><label>Mês<select value={month} onChange={(event) => setMonth(Number(event.target.value))}>{months.map((name, index) => <option key={name} value={index + 1}>{name}</option>)}</select></label></div>
          <div className="report-actions"><button className="primary" type="button" onClick={employeeMonthlyReport} disabled={loadingEmployee}>{loadingEmployee ? "Consultando..." : "Consultar relatório"}</button>{employeeMonth && <button className="secondary" type="button" onClick={() => downloadExcel(`Produtividade ${months[month - 1]} ${employeeYear}`, ["Funcionário", "Atendimentos", "Serviços", "Média por atendimento"], employeeMonth.employees.map((employee) => [employee.employee_name, employee.total, employee.total_services, employee.average_services_per_order]), `produtividade-${employeeYear}-${month}`)}><Download size={17} /> Baixar Excel</button>}</div>
          {employeeMonth && <div className="report-result report-data"><strong>{employeeMonth.total_service_orders}</strong><span>atendimentos no mês</span>{employeeMonth.employees.length ? employeeMonth.employees.map((employee) => <article key={employee.employee_id} className="employee-report"><div className="employee-report-title"><h3>{employee.employee_name}</h3><b>{employee.total} atend.</b></div><div className="employee-report-metrics"><span>{employee.total_services} serviços</span><span>média {employee.average_services_per_order.toLocaleString("pt-BR")} por atendimento</span></div>{employee.services.map((service) => <div className="report-line" key={service.service_type_id}><span>{service.name}</span><b>{service.total}</b></div>)}</article>) : <p>Nenhum dado de funcionário encontrado.</p>}</div>}
        </div>
      </div>
    </div>
  );
}
