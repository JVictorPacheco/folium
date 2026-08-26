import { useCallback, useEffect, useRef, useState, type CSSProperties } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { EditorContent, useEditor } from "@tiptap/react";
import type { JSONContent } from "@tiptap/core";
import { useNavigate, useParams } from "react-router-dom";

import { api } from "../../api/client";
import type { Notebook, Page } from "../../api/types";
import { useAutosave, type AutosaveStatus } from "../../hooks/useAutosave";
import { Button } from "../../components/Button";
import ThemeToggle from "../../components/ThemeToggle";
import { editorExtensions } from "./extensions";
import Toolbar from "./Toolbar";

const EMPTY_DOC: JSONContent = { type: "doc", content: [{ type: "paragraph" }] };
const DEFAULT_LINE_COLOR = "#D9CDB4";

const STATUS_LABEL: Record<AutosaveStatus, string> = {
  saved: "Salvo",
  unsaved: "Não salvo",
  saving: "Salvando...",
  error: "Erro ao salvar",
};

export default function EditorPage() {
  const { id } = useParams();
  const notebookId = Number(id);
  const navigate = useNavigate();
  const qc = useQueryClient();

  const { data: notebook } = useQuery({
    queryKey: ["notebook", notebookId],
    queryFn: () => api.get<Notebook>(`/api/v1/notebooks/${notebookId}`),
  });

  const { data: pages = [] } = useQuery({
    queryKey: ["pages", notebookId],
    queryFn: () => api.get<Page[]>(`/api/v1/notebooks/${notebookId}/pages`),
  });

  const [activeId, setActiveId] = useState<number | null>(null);
  const [revision, setRevision] = useState(1);

  const activeIdRef = useRef(activeId);
  activeIdRef.current = activeId;
  const revisionsRef = useRef<Record<number, number>>({});

  const handleRevision = useCallback((pageId: number, newRevision: number) => {
    revisionsRef.current[pageId] = newRevision;
    if (pageId === activeIdRef.current) setRevision(newRevision);
  }, []);

  const editor = useEditor({ extensions: editorExtensions, content: EMPTY_DOC });

  const getJson = (): Record<string, unknown> =>
    (editor?.getJSON() as Record<string, unknown>) ?? EMPTY_DOC;

  const { status, schedule, flush } = useAutosave({
    pageId: activeId ?? 0,
    revision,
    getJson,
    onRevision: handleRevision,
  });

  useEffect(() => {
    if (pages.length > 0 && activeId === null) setActiveId(pages[0].id);
  }, [pages, activeId]);

  const activePage = pages.find((p) => p.id === activeId) ?? null;

  useEffect(() => {
    if (editor && activePage) {
      if (skipNextContentReset.current) {
        skipNextContentReset.current = false;
        return;
      }
      const content =
        activePage.content_json && Object.keys(activePage.content_json).length > 0
          ? (activePage.content_json as JSONContent)
          : EMPTY_DOC;
      editor.commands.setContent(content, false);
      setRevision(revisionsRef.current[activePage.id] ?? activePage.revision);
    }
  }, [activePage?.id, editor]);

  useEffect(() => {
    if (!editor) return;
    const handler = () => schedule();
    editor.on("update", handler);
    return () => {
      editor.off("update", handler);
    };
  }, [editor, schedule]);

  const createPage = useMutation({
    mutationFn: () =>
      api.post<Page>(`/api/v1/notebooks/${notebookId}/pages`, { title: `Página ${pages.length + 1}` }),
    onSuccess: (page) => {
      qc.invalidateQueries({ queryKey: ["pages", notebookId] });
      setActiveId(page.id);
      setRevision(page.revision);
    },
  });

  // Caderno vazio → cria a 1ª página automaticamente (senão o autosave
  // tentaria salvar na página 0 e receberia 404 — conteúdo se perderia).
  // Ref guard: cria UMA vez por montagem (o refetch do onSuccess não
  // pode re-disparar a criação — causava páginas duplicadas).
  const createdFirstRef = useRef(false);
  const skipNextContentReset = useRef(false);
  useEffect(() => {
    if (createdFirstRef.current) return;
    if (pages.length === 0 && activeId === null && !createPage.isPending) {
      createdFirstRef.current = true;
      skipNextContentReset.current = true;
      createPage.mutate();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pages.length, activeId, createPage.isPending]);

  // Quando a 1ª página nasce (activeId vai de null → id), salva o que foi
  // digitado antes da criação.
  useEffect(() => {
    if (activeId !== null) void flush();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeId]);

  const removePage = useMutation({
    mutationFn: (pageId: number) => api.delete(`/api/v1/pages/${pageId}`),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["pages", notebookId] });
      setActiveId(null);
    },
  });

  const setLineColor = useMutation({
    mutationFn: (color: string) =>
      api.patch<Notebook>(`/api/v1/notebooks/${notebookId}`, { line_color: color }),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["notebook", notebookId] }),
  });

  function selectPage(pageId: number) {
    if (pageId === activeId) return;
    void flush();
    setActiveId(pageId);
  }

  function handleCreate() {
    void flush();
    createPage.mutate();
  }

  const lineSpacing = notebook?.line_spacing ?? 28;
  const customLineColor =
    notebook?.line_color && notebook.line_color.toLowerCase() !== DEFAULT_LINE_COLOR
      ? notebook.line_color
      : undefined;
  const paperStyle = {
    "--line-spacing": `${lineSpacing}px`,
    ...(customLineColor ? { "--line-color": customLineColor } : {}),
  } as CSSProperties;

  const paperClass =
    notebook?.page_mode === "fixed" ? "paper paper--fixed" : "paper paper--continuous";

  return (
    <div className="editor-page">
      <header className="topbar">
        <Button onClick={() => navigate("/")}>← Cadernos</Button>
        <h2 className="notebook-title">{notebook?.name ?? "..."}</h2>
        <label className="line-color" title="Cor da linha do caderno">
          Linha
          <input
            type="color"
            value={customLineColor ?? DEFAULT_LINE_COLOR}
            onChange={(e) => setLineColor.mutate(e.target.value)}
          />
        </label>
        <ThemeToggle />
        <span className={`save-status save-status--${status}`}>{STATUS_LABEL[status]}</span>
      </header>

      <aside className="page-sidebar">
        <Button className="full" onClick={handleCreate}>
          + Página
        </Button>
        {pages.map((p) => (
          <div
            key={p.id}
            className={`page-item${p.id === activeId ? " active" : ""}`}
            onClick={() => selectPage(p.id)}
          >
            <span>{p.title}</span>
            <button
              className="icon-btn"
              onClick={(e) => {
                e.stopPropagation();
                removePage.mutate(p.id);
              }}
              title="Excluir página"
            >
              🗑️
            </button>
          </div>
        ))}
      </aside>

      <main className="paper-area">
        <div className={paperClass} style={paperStyle}>
          {editor && <Toolbar editor={editor} />}
          <div className="paper-lines">
            <EditorContent editor={editor} />
          </div>
        </div>
      </main>
    </div>
  );
}
