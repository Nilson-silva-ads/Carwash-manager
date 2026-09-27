import { FormEvent, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import {
  Armchair,
  Car,
  CarFront,
  Camera,
  ChevronRight,
  CircleDot,
  Droplets,
  Gift,
  Server,
  Sparkles,
  Store,
  Wrench,
} from "lucide-react";
import PageHeader from "../components/PageHeader";
import { useAuth } from "../auth";
import { apiFetch } from "../api";
import type { ServiceOrder, ServiceType } from "../types";

function normalizeText(value: string) {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function getServiceIcon(name: string) {
  const normalized = normalizeText(name);

  if (normalized.includes("lavagem simples")) {
    return <Droplets size={28} strokeWidth={2} />;
  }

  if (normalized.includes("kit")) {
    return <Gift size={28} strokeWidth={2} />;
  }

  if (
    normalized.includes("carro zero") ||
    normalized.includes("carros zero")
  ) {
    return <CarFront size={28} strokeWidth={2} />;
  }

  if (
    normalized.includes("funilaria") ||
    normalized.includes("funilar")
  ) {
    return <Wrench size={28} strokeWidth={2} />;
  }

  if (
    normalized.includes("test drive") ||
    normalized.includes("testdrive") ||
    normalized.includes("testes driving")
  ) {
    return <CircleDot size={28} strokeWidth={2} />;
  }

  if (normalized.includes("showroom")) {
    return <Store size={28} strokeWidth={2} />;
  }

  if (normalized.includes("higienizacao")) {
    return <Sparkles size={28} strokeWidth={2} />;
  }

  if (
    normalized.includes("banco") ||
    normalized.includes("lavagem de banco")
  ) {
    return <Armchair size={28} strokeWidth={2} />;
  }

  if (
    normalized.includes("coating") ||
    normalized.includes("vidro") ||
    normalized.includes("vidros")
  ) {
    return <Sparkles size={28} strokeWidth={2} />;
  }

  return <Car size={28} strokeWidth={2} />;
}

function isWashingType(name: string) {
  const normalized = normalizeText(name);

  return (
    normalized.includes("lavagem simples") ||
    normalized.includes("kit") ||
    normalized.includes("carro zero") ||
    normalized.includes("carros zero") ||
    normalized.includes("funilaria") ||
    normalized.includes("test drive") ||
    normalized.includes("testdrive") ||
    normalized.includes("testes driving") ||
    normalized.includes("showroom")
  );
}

type DashboardService = {
  service_type_id: number;
  name: string;
  total: number;
};

type DashboardReport = {
  today: number;
  month: number;
  services: DashboardService[];
};

export default function Dashboard() {
  const { employee } = useAuth();

  const [plate, setPlate] = useState("");
  const [types, setTypes] = useState<ServiceType[]>([]);
  const [selected, setSelected] = useState<number[]>([]);
  const [lastOrder, setLastOrder] = useState<ServiceOrder | null>(null);

  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const [adminTodayTotal, setAdminTodayTotal] = useState<number | null>(
    null
  );

  const [adminServices, setAdminServices] = useState<DashboardService[]>(
    []
  );

  const [apiStatus, setApiStatus] = useState<
    "loading" | "connected" | "offline"
  >("loading");

  const [adminStatsLoading, setAdminStatsLoading] = useState(false);

  /*
   * ============================================================
   * DASHBOARD DO FUNCIONÁRIO
   * ============================================================
   */

  useEffect(() => {
    if (!employee || employee.is_admin) return;

    setLoading(true);
    setError("");

    Promise.all([
      apiFetch<ServiceType[]>("/service-types"),
      apiFetch<ServiceOrder[]>(
        `/service-orders/employee/${employee.id}`
      ),
    ])
      .then(([serviceTypes, orders]) => {
        setTypes(
          serviceTypes.filter((type) => type.is_active)
        );

        setLastOrder(orders[0] ?? null);
      })
      .catch((err) => {
        setError(
          err instanceof Error
            ? err.message
            : "Não foi possível carregar os dados."
        );
      })
      .finally(() => {
        setLoading(false);
      });
  }, [employee]);

  /*
   * ============================================================
   * DASHBOARD DO ADMINISTRADOR
   * ============================================================
   */

  useEffect(() => {
    if (!employee?.is_admin) return;

    let cancelled = false;

    async function loadAdminDashboard() {
      setAdminStatsLoading(true);
      setApiStatus("loading");
      setAdminServices([]);

      try {
        const dashboard = await apiFetch<DashboardReport>(
          "/reports/dashboard"
        );

        if (cancelled) return;

        setAdminTodayTotal(dashboard.today);
        setAdminServices(dashboard.services ?? []);
        setApiStatus("connected");
      } catch (err) {
        if (cancelled) return;

        setAdminTodayTotal(null);
        setAdminServices([]);
        setApiStatus("offline");

        console.error(
          "Erro ao carregar dashboard administrativo:",
          err
        );
      } finally {
        if (!cancelled) {
          setAdminStatsLoading(false);
        }
      }
    }

    loadAdminDashboard();

    return () => {
      cancelled = true;
    };
  }, [employee]);

  function toggleService(id: number) {
    setSelected((current) =>
      current.includes(id)
        ? current.filter((serviceId) => serviceId !== id)
        : [...current, id]
    );
  }

  function cancelForm() {
    setPlate("");
    setSelected([]);
    setError("");
    setMessage("");
  }

  async function registerServiceOrder(event: FormEvent) {
    event.preventDefault();

    if (submitting) return;

    setError("");
    setMessage("");

    const normalizedPlate = plate
      .replace(/\s/g, "")
      .toUpperCase();

    if (!normalizedPlate) {
      setError("Informe a placa do veículo.");
      return;
    }

    if (!selected.length) {
      setError("Selecione pelo menos um serviço.");
      return;
    }

    setSubmitting(true);

    try {
      const order = await apiFetch<ServiceOrder>(
        "/service-orders",
        {
          method: "POST",
          body: JSON.stringify({
            plate: normalizedPlate,
            service_type_ids: selected,
          }),
        }
      );

      setLastOrder(order);

      setPlate("");
      setSelected([]);

      setMessage(
        `Veículo ${order.plate} registrado com sucesso.`
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Não foi possível registrar o atendimento."
      );
    } finally {
      setSubmitting(false);
    }
  }

  const washingTypes = types.filter((type) =>
    isWashingType(type.name)
  );

  const serviceTypes = types.filter(
    (type) => !isWashingType(type.name)
  );

  /*
   * ============================================================
   * RENDER
   * ============================================================
   */

  return (
    <>
      {employee?.is_admin ? (
        /*
         * ======================================================
         * ADMINISTRADOR
         * ======================================================
         */
        <div className="admin-dashboard">
          <PageHeader
            title={`Olá, ${employee?.name || employee?.username}!`}
            description="Visão geral do Carwash Manager."
          />

          <div className="admin-stat-list">
            {/* ATENDIMENTOS DE HOJE */}
            <Link
              to="/service-orders"
              className="admin-stat-card"
            >
              <div className="admin-stat-icon">
                <Car size={30} strokeWidth={2} />
              </div>

              <div className="admin-stat-content">
                <span>Atendimentos hoje</span>

                <strong>
                  {adminStatsLoading
                    ? "..."
                    : adminTodayTotal !== null
                      ? adminTodayTotal
                      : "--"}
                </strong>
              </div>

              <ChevronRight
                className="admin-stat-arrow"
                size={28}
              />
            </Link>

            {/* STATUS DA API */}
            <div className="admin-stat-card">
              <div className="admin-stat-icon">
                <Server size={30} strokeWidth={2} />
              </div>

              <div className="admin-stat-content">
                <span>Operação</span>

                <strong>
                  Sistema conectado à API
                </strong>

                <div
                  className={`api-status ${
                    apiStatus === "connected"
                      ? "connected"
                      : apiStatus === "offline"
                        ? "offline"
                        : "checking"
                  }`}
                >
                  <span className="api-status-dot" />

                  {apiStatus === "connected"
                    ? "Conectado"
                    : apiStatus === "offline"
                      ? "Sem conexão"
                      : "Verificando..."}
                </div>
              </div>
            </div>
          </div>

          {/* SERVIÇOS REALIZADOS HOJE */}
          <section className="admin-services-summary">
            <div className="admin-services-header">
              <div>
                <h2>Serviços realizados hoje</h2>
                <p>
                  Quantidade por tipo de serviço
                </p>
              </div>
            </div>

            {adminStatsLoading ? (
              <div className="admin-services-loading">
                <span className="loading-spinner" />
                <span>Carregando serviços...</span>
              </div>
            ) : adminServices.length > 0 ? (
              <div className="admin-services-list">
                {adminServices.map((service) => (
                  <div
                    key={service.service_type_id}
                    className="admin-service-row"
                  >
                    <div className="admin-service-info">
                      <span className="admin-service-icon">
                        {getServiceIcon(service.name)}
                      </span>

                      <span className="admin-service-name">
                        {service.name}
                      </span>
                    </div>

                    <strong className="admin-service-total">
                      {service.total}
                    </strong>
                  </div>
                ))}
              </div>
            ) : (
              <div className="admin-services-empty">
                <span>Nenhum serviço realizado hoje.</span>
              </div>
            )}
          </section>
        </div>
      ) : (
        /*
         * ======================================================
         * FUNCIONÁRIO
         * ======================================================
         */
        <div className="mobile-service-page">
          <div className="service-page-top">
            <div className="service-page-header">
              <h1>Cadastrar veículo e atendimento</h1>
              <p>
                Informe a placa e os serviços realizados
              </p>
            </div>

            {/* ÚLTIMO VEÍCULO CADASTRADO */}
            <section className="last-vehicle-card">
              <div className="last-vehicle-header">
                <div>
                  <h2>Último veículo cadastrado</h2>
                  <p>Seu atendimento mais recente</p>
                </div>

                <div className="last-vehicle-icon">
                  <Car size={22} />
                </div>
              </div>

              {loading ? (
                <div className="last-vehicle-loading">
                  <span className="last-vehicle-spinner"></span>
                  <span>Carregando...</span>
                </div>
              ) : lastOrder ? (
                <div className="last-vehicle-info">
                  <strong>{lastOrder.plate}</strong>

                  <div className="last-vehicle-details">
                    <span>
                      Atendimento #{lastOrder.id}
                    </span>

                    <span>
                      {new Date(
                        lastOrder.created_at
                      ).toLocaleString("pt-BR")}
                    </span>
                  </div>
                </div>
              ) : (
                <p className="last-vehicle-empty">
                  Você ainda não cadastrou nenhum veículo.
                </p>
              )}
            </section>
          </div>

          <form
            className="service-registration-card"
            onSubmit={registerServiceOrder}
          >
            {error && (
              <div className="alert error">
                {error}
              </div>
            )}

            {message && (
              <div className="alert success">
                {message}
              </div>
            )}

            <div className="plate-field">
              <div className="plate-label">
                <label htmlFor="plate">
                  Placa do veículo
                </label>

                <span
                  className="plate-info"
                  title="Informe a placa do veículo"
                >
                  i
                </span>
              </div>

              <div className="plate-input-wrapper">
                <input
                  id="plate"
                  value={plate}
                  onChange={(event) =>
                    setPlate(
                      event.target.value
                        .replace(/\s/g, "")
                        .toUpperCase()
                    )
                  }
                  maxLength={10}
                  placeholder="ABC1234"
                  autoCapitalize="characters"
                  autoComplete="off"
                  required
                />

                <button
                  type="button"
                  className="plate-camera"
                  aria-label="Câmera"
                  onClick={() =>
                    document
                      .getElementById("plate")
                      ?.focus()
                  }
                >
                  <Camera size={27} />
                </button>
              </div>
            </div>

            <div className="services-section">
              <h2>Serviços Prestados</h2>

              {washingTypes.length > 0 && (
                <>
                  <h3>Tipos de Lavagem</h3>

                  <div className="service-card-grid">
                    {washingTypes.map((type) => {
                      const isSelected =
                        selected.includes(type.id);

                      return (
                        <button
                          key={type.id}
                          type="button"
                          className={`service-option ${
                            isSelected
                              ? "selected"
                              : ""
                          }`}
                          onClick={() =>
                            toggleService(type.id)
                          }
                        >
                          <span className="service-icon">
                            {getServiceIcon(type.name)}
                          </span>

                          <span className="service-name">
                            {type.name}
                          </span>

                          <span className="service-plus">
                            {isSelected ? "✓" : "+"}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                </>
              )}

              {serviceTypes.length > 0 && (
                <>
                  <h3>Tipos de Serviços</h3>

                  <div className="service-card-list">
                    {serviceTypes.map((type) => {
                      const isSelected =
                        selected.includes(type.id);

                      return (
                        <button
                          key={type.id}
                          type="button"
                          className={`service-option service-option-single ${
                            isSelected
                              ? "selected"
                              : ""
                          }`}
                          onClick={() =>
                            toggleService(type.id)
                          }
                        >
                          <span className="service-icon">
                            {getServiceIcon(type.name)}
                          </span>

                          <span className="service-name">
                            {type.name}
                          </span>

                          <span className="service-plus">
                            {isSelected ? "✓" : "+"}
                          </span>
                        </button>
                      );
                    })}
                  </div>
                </>
              )}

              {!loading && types.length === 0 && (
                <p className="service-empty">
                  Nenhum serviço disponível no momento.
                </p>
              )}
            </div>

            <button
              className="register-service-button"
              type="submit"
              disabled={loading || submitting}
            >
              <span>
                {submitting
                  ? "Cadastrando..."
                  : "Registrar atendimento"}
              </span>

              <span className="register-arrow">
                ›
              </span>
            </button>

            <button
              type="button"
              className="cancel-service-button"
              onClick={cancelForm}
              disabled={submitting}
            >
              Cancelar
            </button>
          </form>
        </div>
      )}
    </>
  );
}