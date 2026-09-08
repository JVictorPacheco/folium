import { useCallback, useEffect, useRef, useState, type CSSProperties } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { EditorContent, useEditor } from "@tiptap/react";
import type { JSONContent } from "@tiptap/core";
import { useNavigate, useParams, useSearchParams } from "react-router-dom";

import { ApiError, api, uploadAsset } from "../../api/client";
import type { Notebook, Page } from "../../api/types";
import { useAutosave, type AutosaveStatus } from "../../hooks/useAutosave";
import { Button } from "../../components/Button";
import ThemeToggle from "../../components/ThemeToggle";
import { editorExtensions } from "./extensions";
import { exportNotebookPdf } from "./exportPdf";
import Toolbar from "./Toolbar";
import VersionHistoryModal from "./VersionHistoryModal";

const EMPTY_DOC: JSONContent = { type: "doc", content: [{ type: "paragraph" }] };
const DEFAULT_LINE_COLOR = "#D9CDB4";
const AUTO_LINE_COLORS = new Set(["#9db3c8", "#d9cdb4"]);

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
  const [searchParams, setSearchParams] = useSearchParams();
  const requestedPageId = searchParams.get("page") ? Number(searchParams.get("page")) : null;

  const { data: notebook } = useQuery({
    queryKey: ["notebook", notebookId],
    queryFn: () => api.get<Notebook>(`/api/v1/notebooks/${notebookId}`),
  });

  const { data: pages = [], isPending: pagesLoading } = useQuery({
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

  const role = notebook?.role ?? "owner";
  const isOwner = role === "owner";
  const canEdit = role !== "viewer";
  const canEditRef = useRef(canEdit);
  canEditRef.current = canEdit;

  async function insertPastedImage(file: File) {
    if (!editorRef.current) return;
    try {
      const asset = await uploadAsset(file, "image");
      // Insere a imagem seguida de um parágrafo vazio, ambos numa mesma
      // chamada — depois de inserir só a imagem, a seleção fica em cima do
      // nó dela (é um átomo), então uma segunda imagem colada/arrastada em
      // seguida substituiria a primeira em vez de ficar ao lado. Com o
      // parágrafo, o cursor termina num texto de verdade.
      editorRef.current
        .chain()
        .focus()
        .insertContent([{ type: "image", attrs: { src: asset.url } }, { type: "paragraph" }])
        .run();
    } catch (err) {
      window.alert(err instanceof ApiError ? err.message : "Não foi possível colar a imagem.");
    }
  }

  // Processa um arquivo de cada vez (aguarda upload + inserção completarem
  // antes do próximo) — inserir em paralelo faz o segundo substituir o
  // primeiro, porque a seleção fica em cima do nó recém-inserido.
  async function insertPastedImages(files: File[]) {
    for (const file of files) {
      await insertPastedImage(file);
    }
  }

  const editor = useEditor({
    extensions: editorExtensions,
    content: EMPTY_DOC,
    editable: canEdit,
    editorProps: {
      handlePaste: (_view, event) => {
        if (!canEditRef.current) return false;
        const items = Array.from(event.clipboardData?.items ?? []);
        const imageItem = items.find((item) => item.type.startsWith("image/"));
        const file = imageItem?.getAsFile();
        if (!file) return false;
        event.preventDefault();
        void insertPastedImage(file);
        return true;
      },
      handleDrop: (_view, event) => {
        if (!canEditRef.current) return false;
        const files = Array.from(event.dataTransfer?.files ?? []).filter((f) =>
          f.type.startsWith("image/"),
        );
        if (files.length === 0) return false;
        event.preventDefault();
        void insertPastedImages(files);
        return true;
      },
    },
  });
  const editorRef = useRef(editor);
  editorRef.current = editor;

  useEffect(() => {
    // `emitUpdate: false` — trocar editable não é uma edição de conteúdo;
    // sem isso o TipTap dispara "update" nessa troca, o que agendava um
    // autosave (e um 404 pra quem não pode editar) só por causa do próprio
    // ajuste de permissão, não de algo que o usuário digitou.
    editor?.setEditable(canEdit, false);
  }, [editor, canEdit]);

  const getJson = (): Record<string, unknown> =>
    (editor?.getJSON() as Record<string, unknown>) ?? EMPTY_DOC;

  const { status, schedule, flush } = useAutosave({
    pageId: activeId ?? 0,
    revision,
    getJson,
    onRevision: handleRevision,
  });

  useEffect(() => {
    if (pages.length === 0 || activeId !== null) return;
    const requested = requestedPageId !== null && pages.some((p) => p.id === requestedPageId);
    setActiveId(requested ? requestedPageId : pages[0].id);
    if (requestedPageId !== null) {
      searchParams.delete("page");
      setSearchParams(searchParams, { replace: true });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
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
    if (!editor || !canEdit) return;
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
  // Só cria quando a listagem já terminou de carregar (pagesLoading), para
  // não criar página duplicada no reload de um caderno que já tem páginas.
  const createdFirstRef = useRef(false);
  const skipNextContentReset = useRef(false);
  useEffect(() => {
    if (createdFirstRef.current) return;
    if (pagesLoading || pages.length > 0 || activeId !== null || createPage.isPending) return;
    createdFirstRef.current = true;
    skipNextContentReset.current = true;
    createPage.mutate();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pagesLoading, pages.length, activeId, createPage.isPending]);

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

  const [exporting, setExporting] = useState(false);

  async function handleExportPdf() {
    if (!notebook || exporting) return;
    setExporting(true);
    try {
      await flush();
      // `pages` (cache do React Query) só é atualizado na criação/exclusão
      // de página, não a cada autosave — busca direto do servidor (sem
      // passar pelo cache/`qc`, pra não notificar o `useQuery` de `pages`
      // no meio da mesma renderização) pra não exportar conteúdo
      // desatualizado de páginas editadas antes na mesma sessão.
      const freshPages = await api.get<Page[]>(`/api/v1/notebooks/${notebookId}/pages`);
      exportNotebookPdf(notebook, freshPages);
    } finally {
      setExporting(false);
    }
  }

  const [showHistory, setShowHistory] = useState(false);

  function handleRestored(page: Page) {
    revisionsRef.current[page.id] = page.revision;
    qc.invalidateQueries({ queryKey: ["pages", notebookId] });
    if (page.id !== activeId || !editor) return;
    setRevision(page.revision);
    const content =
      page.content_json && Object.keys(page.content_json).length > 0
        ? (page.content_json as JSONContent)
        : EMPTY_DOC;
    editor.commands.setContent(content, false);
  }

  const lineSpacing = notebook?.line_spacing ?? 28;
  const [lineColorDraft, setLineColorDraft] = useState<string | null>(null);
  const customLineColor =
    notebook?.line_color && !AUTO_LINE_COLORS.has(notebook.line_color.toLowerCase())
      ? notebook.line_color
      : undefined;
  const effectiveLineColor = lineColorDraft ?? customLineColor ?? DEFAULT_LINE_COLOR;
  const paperStyle = {
    "--line-spacing": `${lineSpacing}px`,
    ...(effectiveLineColor !== DEFAULT_LINE_COLOR ? { "--line-color": effectiveLineColor } : {}),
  } as CSSProperties;

  const paperClass =
    notebook?.page_mode === "fixed" ? "paper paper--fixed" : "paper paper--continuous";

  return (
    <div className="editor-page">
      <header className="topbar">
        <Button onClick={() => navigate("/")}>← Cadernos</Button>
        <h2 className="notebook-title">
          {notebook?.name ?? "..."}
          {!isOwner && <span className="role-badge">{role === "editor" ? "pode editar" : "só ver"}</span>}
        </h2>
        {isOwner && (
          <label className="line-color" title="Cor da linha do caderno">
            Linha
            <input
              type="color"
              value={effectiveLineColor}
              onChange={(e) => {
                setLineColorDraft(e.target.value);
                setLineColor.mutate(e.target.value);
              }}
            />
          </label>
        )}
        <Button onClick={handleExportPdf} disabled={exporting}>
          {exporting ? "Exportando..." : "Exportar PDF"}
        </Button>
        <Button onClick={() => setShowHistory(true)} disabled={!activeId}>
          Histórico
        </Button>
        <ThemeToggle />
        <span className={`save-status save-status--${status}`}>{STATUS_LABEL[status]}</span>
      </header>

      <aside className="page-sidebar">
        {canEdit && (
          <Button className="full" onClick={handleCreate}>
            + Página
          </Button>
        )}
        {pages.map((p) => (
          <div
            key={p.id}
            className={`page-item${p.id === activeId ? " active" : ""}`}
            onClick={() => selectPage(p.id)}
          >
            <span>{p.title}</span>
            {canEdit && (
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
            )}
          </div>
        ))}
      </aside>

      <main className="paper-area">
        <div className={paperClass} style={paperStyle}>
          {editor && canEdit && <Toolbar editor={editor} />}
          <div className="paper-lines">
            <EditorContent editor={editor} />
          </div>
        </div>
      </main>

      {showHistory && activeId && (
        <VersionHistoryModal
          pageId={activeId}
          canRestore={canEdit}
          onClose={() => setShowHistory(false)}
          onRestored={handleRestored}
        />
      )}
    </div>
  );
}
