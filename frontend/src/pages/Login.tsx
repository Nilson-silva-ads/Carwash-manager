import { FormEvent, useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import { Droplets } from "lucide-react";
import { useAuth } from "../auth";

export default function Login() {
  const { employee, signIn } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  if (employee) return <Navigate to="/dashboard" replace />;

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setBusy(true);
    try {
      await signIn(username, password);
      navigate("/dashboard");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha no login.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-page">
      <form className="login-card" onSubmit={submit}>
        <div className="login-logo"><Droplets size={30} /></div>
        <h1>Carwash Manager</h1>
        <p>Acesse o sistema</p>

        {error && <div className="alert error">{error}</div>}

        <label>Usuário</label>
        <input value={username} onChange={(e) => setUsername(e.target.value)} required />

        <label>Senha</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />

        <button className="primary full" disabled={busy}>
          {busy ? "Entrando..." : "Entrar"}
        </button>
      </form>
    </div>
  );
}