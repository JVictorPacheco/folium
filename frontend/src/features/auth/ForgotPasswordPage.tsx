import { useState, type FormEvent } from "react";
import { Link } from "react-router-dom";

import { api } from "../../api/client";
import { Button } from "../../components/Button";
import { Input } from "../../components/Input";
import ThemeToggle from "../../components/ThemeToggle";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      await api.post("/api/v1/auth/forgot-password", { email });
      setSent(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao enviar");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-theme-toggle">
        <ThemeToggle />
      </div>
      <form className="card" onSubmit={handleSubmit}>
        <h1>Recuperar senha</h1>
        {sent ? (
          <>
            <p className="muted">Se o e-mail existir, enviaremos um link de recuperação.</p>
            <Link to="/login">Voltar para o login</Link>
          </>
        ) : (
          <>
            <p className="muted">Informe seu e-mail para receber o link de recuperação.</p>
            <Input
              type="email"
              placeholder="E-mail"
              autoComplete="email"
              autoFocus
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            {error && <p className="error">{error}</p>}
            <Button type="submit" disabled={loading}>
              {loading ? "Enviando..." : "Enviar link"}
            </Button>
            <p>
              <Link to="/login">Voltar para o login</Link>
            </p>
          </>
        )}
      </form>
    </div>
  );
}
