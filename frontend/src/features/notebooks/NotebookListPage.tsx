import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";

import { api } from "../../api/client";
import type { Notebook } from "../../api/types";
import { Button } from "../../components/Button";
import { Input } from "../../components/Input";
import ThemeToggle from "../../components/ThemeToggle";
import { useAuth } from "../auth/AuthContext";

export default function NotebookListPage() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const [name, setName] = useState("");

  const { data: notebooks = [], isLoading } = useQuery({
    queryKey: ["notebooks"],
    queryFn: () => api.get<Notebook[]>("/api/v1/notebooks"),
  });

  const create = useMutation({
    mutationFn: () => api.post<Notebook>("/api/v1/notebooks", { name }),
    onSuccess: () => {
      setName("");
      qc.invalidateQueries({ queryKey: ["notebooks"] });
    },
  });

  const rename = useMutation({
    mutationFn: ({ id, newName }: { id: number; newName: string }) =>
      api.patch<Notebook>(`/api/v1/notebooks/${id}`, { name: newName }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notebooks"] }),
  });

  const remove = useMutation({
    mutationFn: (id: number) => api.delete(`/api/v1/notebooks/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notebooks"] }),
  });

  function handleRename(notebook: Notebook) {
    const newName = window.prompt("Novo nome:", notebook.name);
    if (newName && newName.trim()) rename.mutate({ id: notebook.id, newName: newName.trim() });
  }

  return (
    <div className="notebooks-page">
      <header className="topbar">
        <h1 className="notebook-title">Folium</h1>
        <ThemeToggle />
        <Button onClick={logout}>Sair</Button>
      </header>

      <main className="container">
        <form
          className="create-row"
          onSubmit={(e) => {
            e.preventDefault();
            if (name.trim()) create.mutate();
          }}
        >
          <Input
            placeholder="Nome do caderno"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />
          <Button type="submit" disabled={!name.trim() || create.isPending}>
            Criar
          </Button>
        </form>

        {isLoading && <p className="muted">Carregando...</p>}

        <ul className="notebook-list">
          {notebooks.map((nb) => (
            <li key={nb.id} className="notebook-item">
              <button className="notebook-open" onClick={() => navigate(`/notebooks/${nb.id}`)}>
                <span className="notebook-name">{nb.name}</span>
                <span className="muted">{nb.page_mode === "fixed" ? "Páginas fixas" : "Rolagem contínua"}</span>
              </button>
              <button className="icon-btn" onClick={() => handleRename(nb)} title="Renomear">
                ✏️
              </button>
              <button className="icon-btn" onClick={() => remove.mutate(nb.id)} title="Excluir">
                🗑️
              </button>
            </li>
          ))}
        </ul>

        {notebooks.length === 0 && !isLoading && (
          <p className="muted">Nenhum caderno ainda. Crie o primeiro!</p>
        )}
      </main>
    </div>
  );
}
