import { useState, type FormEvent } from "react";
import { Link, useSearchParams } from "react-router-dom";

import { api } from "../../api/client";
import { Button } from "../../components/Button";
import { PasswordInput } from "../../components/PasswordInput";
import ThemeToggle from "../../components/ThemeToggle";

export default function ResetPasswordPage() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get("token") ?? "";

  const [password, setPassword] = useState("");
  const [done, setDone] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError(null);
    if (password.length < 8) {
      setError("A senha deve ter ao menos 8 caracteres");
      return;
    }
    setLoading(true);
    try {
      await api.post("/api/v1/auth/reset-password", { token, new_password: password });
      setDone(true);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Falha ao redefinir a senha");
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
        <h1>Nova senha</h1>
        {done ? (
          <>
            <p className="muted">Senha atualizada com sucesso.</p>
            <Link to="/login">Fazer login</Link>
          </>
        ) : (
          <>
            <p className="muted">Defina uma nova senha (mín. 8 caracteres).</p>
            <PasswordInput
              placeholder="Nova senha"
              autoComplete="new-password"
              autoFocus
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
            {error && <p className="error">{error}</p>}
            <Button type="submit" disabled={loading || !token}>
              {loading ? "Salvando..." : "Salvar senha"}
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
