import { FormEvent, useEffect, useState } from "react";
import PageHeader from "../components/PageHeader";
import { apiFetch } from "../api";
import type { Employee } from "../types";

export default function Employees() {
  const [employees, setEmployees] = useState<Employee[]>([]);

  const [form, setForm] = useState({
    name: "",
    username: "",
    password: "",
    is_admin: false,
  });

  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  async function load() {
    try {
      setEmployees(await apiFetch<Employee[]>("/employees"));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro.");
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function create(event: FormEvent) {
    event.preventDefault();
    setError("");
    setMessage("");

    try {
      await apiFetch("/employees", {
        method: "POST",
        body: JSON.stringify(form),
      });

      setForm({
        name: "",
        username: "",
        password: "",
        is_admin: false,
      });

      setMessage("Funcionário criado.");
      load();
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Erro ao criar funcionário."
      );
    }
  }

  async function activate(id: number, active: boolean) {
    try {
      await apiFetch(
        `/employees/${id}/${active ? "deactivate" : "activate"}`,
        { method: "PATCH" }
      );

      load();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro.");
    }
  }

  return (
    <>
      <PageHeader
        title="Funcionários"
        description="Gerencie os usuários do sistema."
      />

      <div className="two-col">
        <form className="panel form-panel" onSubmit={create}>
          <h2>Novo funcionário</h2>

          {message && (
            <div className="alert success">{message}</div>
          )}

          {error && (
            <div className="alert error">{error}</div>
          )}

          <label>Nome</label>
          <input
            value={form.name}
            onChange={(e) =>
              setForm({ ...form, name: e.target.value })
            }
            required
          />

          <label>Username</label>
          <input
            value={form.username}
            onChange={(e) =>
              setForm({ ...form, username: e.target.value })
            }
            required
          />

          <label>Senha</label>
          <input
            type="password"
            value={form.password}
            onChange={(e) =>
              setForm({ ...form, password: e.target.value })
            }
            required
          />

          <label className="checkbox-label">
            <input
              type="checkbox"
              checked={form.is_admin}
              onChange={(e) =>
                setForm({
                  ...form,
                  is_admin: e.target.checked,
                })
              }
            />
            Administrador
          </label>

          <button className="primary" type="submit">
            Cadastrar
          </button>
        </form>

        <div className="panel table-wrap">
          <table>
            <thead>
              <tr>
                <th>Nome</th>
                <th>Username</th>
                <th>Perfil</th>
                <th>Status</th>
                <th>Ação</th>
              </tr>
            </thead>

            <tbody>
              {employees.map((employee) => (
                <tr key={employee.id}>
                  <td>{employee.name}</td>

                  <td>{employee.username}</td>

                  <td>
                    <span
                      className={`badge ${
                        employee.is_admin ? "ok" : "off"
                      }`}
                    >
                      {employee.is_admin ? "ADM" : "Funcionário"}
                    </span>
                  </td>

                  <td>
                    <span
                      className={`badge ${
                        employee.is_active ? "ok" : "off"
                      }`}
                    >
                      {employee.is_active ? "Ativo" : "Inativo"}
                    </span>
                  </td>

                  <td>
                    <button
                      className="small"
                      onClick={() =>
                        activate(employee.id, employee.is_active)
                      }
                    >
                      {employee.is_active
                        ? "Desativar"
                        : "Ativar"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </>
  );
}