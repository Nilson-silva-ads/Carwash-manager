import "./LoadingSpinner.css";

type LoadingSpinnerProps = { label?: string };

export default function LoadingSpinner({ label = "Carregando" }: LoadingSpinnerProps) {
  return <span className="loading-state"><span className="spinner" aria-hidden="true" />{label}</span>;
}
