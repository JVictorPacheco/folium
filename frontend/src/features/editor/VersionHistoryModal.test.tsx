import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import VersionHistoryModal from "./VersionHistoryModal";

const VERSIONS = [
  { id: 2, page_id: 1, revision: 3, created_at: "2026-09-05T10:00:00Z" },
  { id: 1, page_id: 1, revision: 1, created_at: "2026-09-05T09:00:00Z" },
];

const DETAIL = {
  id: 1,
  page_id: 1,
  revision: 1,
  created_at: "2026-09-05T09:00:00Z",
  content_json: { type: "doc", content: [{ type: "paragraph", content: [{ type: "text", text: "antigo" }] }] },
};

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

function renderModal(onRestored = vi.fn(), onClose = vi.fn()) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  render(
    <QueryClientProvider client={qc}>
      <VersionHistoryModal pageId={1} onClose={onClose} onRestored={onRestored} />
    </QueryClientProvider>,
  );
  return { onRestored, onClose };
}

describe("VersionHistoryModal", () => {
  afterEach(() => vi.restoreAllMocks());

  it("lista as versões e mostra prévia ao selecionar", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string) => {
        if (url.endsWith("/api/v1/pages/1/versions")) return Promise.resolve(jsonResponse(VERSIONS));
        if (url.endsWith("/api/v1/pages/1/versions/1")) return Promise.resolve(jsonResponse(DETAIL));
        return Promise.reject(new Error(`unexpected fetch: ${url}`));
      }),
    );

    renderModal();

    const items = await screen.findAllByRole("listitem");
    expect(items).toHaveLength(2);

    const [selectBtn] = within(items[1]).getAllByRole("button");
    fireEvent.click(selectBtn);

    await waitFor(() => expect(screen.getByText("antigo")).toBeInTheDocument());
  });

  it("restaura uma versão e chama onRestored/onClose", async () => {
    const restoredPage = { id: 1, notebook_id: 1, title: "Notas", position: 1, content_json: {}, revision: 4 };
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string) => {
        if (url.endsWith("/api/v1/pages/1/versions")) return Promise.resolve(jsonResponse(VERSIONS));
        if (url.endsWith("/api/v1/pages/1/versions/1/restore")) return Promise.resolve(jsonResponse(restoredPage));
        return Promise.reject(new Error(`unexpected fetch: ${url}`));
      }),
    );

    const { onRestored, onClose } = renderModal();

    const items = await screen.findAllByRole("listitem");
    const [, restoreBtn] = within(items[1]).getAllByRole("button");
    fireEvent.click(restoreBtn);

    await waitFor(() => expect(onRestored).toHaveBeenCalledWith(restoredPage));
    expect(onClose).toHaveBeenCalled();
  });

  it("mostra mensagem quando não há versões", async () => {
    vi.stubGlobal("fetch", vi.fn(() => Promise.resolve(jsonResponse([]))));

    renderModal();

    await screen.findByText(/Ainda não há versões salvas/);
  });
});
