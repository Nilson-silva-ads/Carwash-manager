import { createContext, useContext, useEffect, useState } from "react";
import { apiFetch, clearToken, getToken, login } from "./api";
import type { Employee } from "./types";

type AuthContextValue = {
  employee: Employee | null;
  loading: boolean;
  signIn: (username: string, password: string) => Promise<void>;
  signOut: () => void;
};

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [employee, setEmployee] = useState<Employee | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!getToken()) {
      setLoading(false);
      return;
    }

    apiFetch<Employee>("/employees/me")
      .then(setEmployee)
      .catch(() => {
        clearToken();
        setEmployee(null);
      })
      .finally(() => setLoading(false));
  }, []);

  async function signIn(username: string, password: string) {
    const data = await login(username, password);
    localStorage.setItem("carwash_token", data.access_token);

    // O backend atual pode não possuir /employees/me.
    // Nesse caso, o usuário continua autenticado e o dashboard funciona.
    try {
      const current = await apiFetch<Employee>("/employees/me");
      setEmployee(current);
    } catch {
      setEmployee({
        id: 0,
        name: username,
        username,
        is_admin: false,
        is_active: true,
      });
    }
  }

  function signOut() {
    clearToken();
    setEmployee(null);
  }

  return (
    <AuthContext.Provider value={{ employee, loading, signIn, signOut }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth deve ser usado dentro de AuthProvider");
  return context;
}