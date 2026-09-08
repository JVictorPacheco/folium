import { useState } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { api } from "../../api/client";
import type { Page, PageVersion, PageVersionDetail } from "../../api/types";
import { Button } from "../../components/Button";
import { contentToHtml } from "./exportPdf";

interface Props {
  pageId: number;
  canRestore?: boolean;
  onClose: () => void;
  onRestored: (page: Page) => void;
}

function formatDate(iso: string): string {
  return new Date(iso).toLocaleString("pt-BR", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

export default function VersionHistoryModal({ pageId, canRestore = true, onClose, onRestored }: Props) {
  const qc = useQueryClient();
  const [previewId, setPreviewId] = useState<number | null>(null);

  const { data: versions = [], isPending } = useQuery({
    queryKey: ["page-versions", pageId],
    queryFn: () => api.get<PageVersion[]>(`/api/v1/pages/${pageId}/versions`),
  });

  const { data: preview, isPending: previewLoading } = useQuery({
    queryKey: ["page-version-detail", pageId, previewId],
    queryFn: () => api.get<PageVersionDetail>(`/api/v1/pages/${pageId}/versions/${previewId}`),
    enabled: previewId !== null,
  });

  const restore = useMutation({
    mutationFn: (versionId: number) =>
      api.post<Page>(`/api/v1/pages/${pageId}/versions/${versionId}/restore`),
    onSuccess: (page) => {
      void qc.invalidateQueries({ queryKey: ["page-versions", pageId] });
      onRestored(page);
      onClose();
    },
  });

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal" onClick={(e) => e.stopPropagation()} role="dialog" aria-modal="true">
        <header className="modal-header">
          <h3>Histórico de versões</h3>
          <button className="icon-btn" onClick={onClose} title="Fechar">
            ✕
          </button>
        </header>

        {isPending && <p className="muted">Carregando...</p>}
        {!isPending && versions.length === 0 && (
          <p className="muted">
            Ainda não há versões salvas desta página. Snapshots aparecem conforme você edita.
          </p>
        )}

        {versions.length > 0 && (
          <div className="version-body">
            <ul className="version-list">
              {versions.map((v) => (
                <li key={v.id} className={`version-item${v.id === previewId ? " active" : ""}`}>
                  <button className="version-select" onClick={() => setPreviewId(v.id)}>
                    {formatDate(v.created_at)}
                  </button>
                  {canRestore && (
                    <Button onClick={() => restore.mutate(v.id)} disabled={restore.isPending}>
                      Restaurar
                    </Button>
                  )}
                </li>
              ))}
            </ul>

            <div className="version-preview">
              {previewId === null && (
                <p className="muted">Selecione uma versão para ver a prévia.</p>
              )}
              {previewId !== null && previewLoading && <p className="muted">Carregando prévia...</p>}
              {previewId !== null && preview && (
                <div
                  className="ProseMirror"
                  dangerouslySetInnerHTML={{ __html: contentToHtml(preview.content_json) }}
                />
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
