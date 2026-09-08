import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";

import { api } from "../../api/client";
import type { Notebook, SearchResult, Tag } from "../../api/types";
import { Button } from "../../components/Button";
import { Input } from "../../components/Input";
import ThemeToggle from "../../components/ThemeToggle";
import { useDebouncedCallback } from "../../hooks/useDebouncedCallback";
import { useAuth } from "../auth/AuthContext";
import ShareModal from "./ShareModal";

const ROLE_LABEL: Record<Notebook["role"], string> = {
  owner: "",
  editor: "compartilhado · pode editar",
  viewer: "compartilhado · só ver",
};

export default function NotebookListPage() {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const qc = useQueryClient();
  const [name, setName] = useState("");
  const [tagFilter, setTagFilter] = useState("");
  const [sharingNotebookId, setSharingNotebookId] = useState<number | null>(null);
  const [query, setQuery] = useState("");
  const [debouncedQuery, setDebouncedQuery] = useState("");
  const setDebouncedQueryLater = useDebouncedCallback(setDebouncedQuery, 300);

  const { data: notebooks = [], isLoading } = useQuery({
    queryKey: ["notebooks", tagFilter],
    queryFn: () =>
      api.get<Notebook[]>(`/api/v1/notebooks${tagFilter ? `?tag=${encodeURIComponent(tagFilter)}` : ""}`),
  });

  const { data: tags = [] } = useQuery({
    queryKey: ["tags"],
    queryFn: () => api.get<Tag[]>("/api/v1/tags"),
  });

  const { data: searchResults = [], isFetching: searching } = useQuery({
    queryKey: ["search", debouncedQuery],
    queryFn: () => api.get<SearchResult[]>(`/api/v1/search?q=${encodeURIComponent(debouncedQuery)}`),
    enabled: debouncedQuery.trim().length > 0,
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

  const setTags = useMutation({
    mutationFn: ({ id, newTags }: { id: number; newTags: string[] }) =>
      api.patch<Notebook>(`/api/v1/notebooks/${id}`, { tags: newTags }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["notebooks"] });
      qc.invalidateQueries({ queryKey: ["tags"] });
    },
  });

  const remove = useMutation({
    mutationFn: (id: number) => api.delete(`/api/v1/notebooks/${id}`),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notebooks"] }),
  });

  function handleRename(notebook: Notebook) {
    const newName = window.prompt("Novo nome:", notebook.name);
    if (newName && newName.trim()) rename.mutate({ id: notebook.id, newName: newName.trim() });
  }

  function handleEditTags(notebook: Notebook) {
    const raw = window.prompt("Tags (separadas por vírgula):", notebook.tags.join(", "));
    if (raw === null) return;
    const newTags = raw
      .split(",")
      .map((t) => t.trim())
      .filter(Boolean);
    setTags.mutate({ id: notebook.id, newTags });
  }

  function handleQueryChange(value: string) {
    setQuery(value);
    setDebouncedQueryLater(value);
  }

  const showSearch = debouncedQuery.trim().length > 0;

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

        <div className="search-row">
          <Input
            placeholder="Buscar em todos os cadernos..."
            value={query}
            onChange={(e) => handleQueryChange(e.target.value)}
          />
          {tags.length > 0 && (
            <select
              className="input tag-filter"
              value={tagFilter}
              onChange={(e) => setTagFilter(e.target.value)}
            >
              <option value="">Todas as tags</option>
              {tags.map((t) => (
                <option key={t.id} value={t.name}>
                  {t.name}
                </option>
              ))}
            </select>
          )}
        </div>

        {showSearch && (
          <div className="search-results">
            {searching && <p className="muted">Buscando...</p>}
            {!searching && searchResults.length === 0 && (
              <p className="muted">Nada encontrado para "{debouncedQuery}".</p>
            )}
            <ul className="notebook-list">
              {searchResults.map((r) => (
                <li key={r.page_id} className="notebook-item">
                  <button
                    className="notebook-open"
                    onClick={() => navigate(`/notebooks/${r.notebook_id}?page=${r.page_id}`)}
                  >
                    <span className="notebook-name">
                      {r.notebook_name} · {r.page_title}
                    </span>
                    <span className="muted">{r.snippet}</span>
                  </button>
                </li>
              ))}
            </ul>
          </div>
        )}

        {!showSearch && (
          <>
            {isLoading && <p className="muted">Carregando...</p>}

            <ul className="notebook-list">
              {notebooks.map((nb) => (
                <li key={nb.id} className="notebook-item">
                  <button className="notebook-open" onClick={() => navigate(`/notebooks/${nb.id}`)}>
                    <span className="notebook-name">{nb.name}</span>
                    <span className="muted">
                      {nb.page_mode === "fixed" ? "Páginas fixas" : "Rolagem contínua"}
                      {nb.role !== "owner" && ` · ${ROLE_LABEL[nb.role]}`}
                    </span>
                    {nb.tags.length > 0 && (
                      <span className="tag-chips">
                        {nb.tags.map((t) => (
                          <span key={t} className="tag-chip">
                            {t}
                          </span>
                        ))}
                      </span>
                    )}
                  </button>
                  {nb.role === "owner" && (
                    <>
                      <button
                        className="icon-btn"
                        onClick={() => setSharingNotebookId(nb.id)}
                        title="Compartilhar"
                      >
                        👥
                      </button>
                      <button className="icon-btn" onClick={() => handleEditTags(nb)} title="Editar tags">
                        🏷️
                      </button>
                      <button className="icon-btn" onClick={() => handleRename(nb)} title="Renomear">
                        ✏️
                      </button>
                      <button className="icon-btn" onClick={() => remove.mutate(nb.id)} title="Excluir">
                        🗑️
                      </button>
                    </>
                  )}
                </li>
              ))}
            </ul>

            {notebooks.length === 0 && !isLoading && (
              <p className="muted">Nenhum caderno ainda. Crie o primeiro!</p>
            )}
          </>
        )}
      </main>

      {sharingNotebookId !== null && (
        <ShareModal notebookId={sharingNotebookId} onClose={() => setSharingNotebookId(null)} />
      )}
    </div>
  );
}
