import { useState, type FormEvent } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { ApiError, api } from "../../api/client";
import type { Share } from "../../api/types";
import { Button } from "../../components/Button";
import { Input } from "../../components/Input";

interface Props {
  notebookId: number;
  onClose: () => void;
}

export default function ShareModal({ notebookId, onClose }: Props) {
  const qc = useQueryClient();
  const [email, setEmail] = useState("");
  const [permission, setPermission] = useState<"viewer" | "editor">("viewer");
  const [error, setError] = useState<string | null>(null);

  const { data: shares = [], isPending } = useQuery({
    queryKey: ["shares", notebookId],
    queryFn: () => api.get<Share[]>(`/api/v1/notebooks/${notebookId}/shares`),
  });

  const create = useMutation({
    mutationFn: () =>
      api.post<Share>(`/api/v1/notebooks/${notebookId}/shares`, { email: email.trim(), permission }),
    onSuccess: () => {
      setEmail("");
      setError(null);
      void qc.invalidateQueries({ queryKey: ["shares", notebookId] });
    },
    onError: (err: unknown) => {
      setError(err instanceof ApiError ? err.message : "Não foi possível compartilhar.");
    },
  });

  const remove = useMutation({
    mutationFn: (shareId: number) => api.delete(`/api/v1/notebooks/${notebookId}/shares/${shareId}`),
    onSuccess: () => void qc.invalidateQueries({ queryKey: ["shares", notebookId] }),
  });

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    if (email.trim()) create.mutate();
  }

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
        <header className="modal-header">
          <h3>Compartilhar caderno</h3>
          <button className="icon-btn" onClick={onClose} title="Fechar">
            ✕
          </button>
        </header>

        <form className="share-form" onSubmit={handleSubmit}>
          <Input
            type="email"
            placeholder="e-mail da pessoa"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <select
            className="input"
            value={permission}
            onChange={(e) => setPermission(e.target.value as "viewer" | "editor")}
          >
            <option value="viewer">Pode ver</option>
            <option value="editor">Pode editar</option>
          </select>
          <Button type="submit" disabled={!email.trim() || create.isPending}>
            Compartilhar
          </Button>
        </form>
        {error && <p className="error">{error}</p>}

        {isPending && <p className="muted">Carregando...</p>}
        {!isPending && shares.length === 0 && (
          <p className="muted">Ainda não compartilhado com ninguém.</p>
        )}

        <ul className="share-list">
          {shares.map((s) => (
            <li key={s.id} className="share-item">
              <span>{s.email}</span>
              <span className="muted">{s.permission === "editor" ? "Pode editar" : "Pode ver"}</span>
              <button className="icon-btn" onClick={() => remove.mutate(s.id)} title="Revogar acesso">
                🗑️
              </button>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
