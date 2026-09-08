import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

import ShareModal from "./ShareModal";

const SHARES = [{ id: 1, notebook_id: 1, email: "colega@example.com", permission: "viewer" as const, created_at: "2026-09-08T00:00:00Z" }];

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

function renderModal(onClose = vi.fn()) {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  render(
    <QueryClientProvider client={qc}>
      <ShareModal notebookId={1} onClose={onClose} />
    </QueryClientProvider>,
  );
  return { onClose };
}

describe("ShareModal", () => {
  afterEach(() => vi.restoreAllMocks());

  it("lista compartilhamentos existentes e permite revogar", async () => {
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (url.endsWith("/api/v1/notebooks/1/shares") && (!init || init.method === "GET" || init.method === undefined))
        return Promise.resolve(jsonResponse(SHARES));
      if (url.endsWith("/api/v1/notebooks/1/shares/1") && init?.method === "DELETE")
        return Promise.resolve(new Response(null, { status: 204 }));
      return Promise.reject(new Error(`unexpected fetch: ${url} ${init?.method}`));
    });
    vi.stubGlobal("fetch", fetchMock);

    renderModal();

    await screen.findByText("colega@example.com");
    fireEvent.click(screen.getByTitle("Revogar acesso"));

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining("/api/v1/notebooks/1/shares/1"),
        expect.objectContaining({ method: "DELETE" }),
      ),
    );
  });

  it("cria um novo compartilhamento com e-mail e permissão escolhidos", async () => {
    const newShare = { id: 2, notebook_id: 1, email: "novo@example.com", permission: "editor", created_at: "2026-09-08T01:00:00Z" };
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (url.endsWith("/api/v1/notebooks/1/shares") && (!init || init.method === "GET" || init.method === undefined))
        return Promise.resolve(jsonResponse([]));
      if (url.endsWith("/api/v1/notebooks/1/shares") && init?.method === "POST")
        return Promise.resolve(jsonResponse(newShare, 201));
      return Promise.reject(new Error(`unexpected fetch: ${url} ${init?.method}`));
    });
    vi.stubGlobal("fetch", fetchMock);

    renderModal();
    await screen.findByText(/Ainda não compartilhado/);

    fireEvent.change(screen.getByPlaceholderText("e-mail da pessoa"), {
      target: { value: "novo@example.com" },
    });
    fireEvent.change(screen.getByRole("combobox"), { target: { value: "editor" } });
    fireEvent.click(screen.getByText("Compartilhar"));

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining("/api/v1/notebooks/1/shares"),
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({ email: "novo@example.com", permission: "editor" }),
        }),
      ),
    );
  });

  it("mostra erro do backend quando o e-mail não tem conta", async () => {
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (url.endsWith("/api/v1/notebooks/1/shares") && (!init || init.method === "GET" || init.method === undefined))
        return Promise.resolve(jsonResponse([]));
      if (url.endsWith("/api/v1/notebooks/1/shares") && init?.method === "POST")
        return Promise.resolve(
          jsonResponse({ detail: "Não existe usuário cadastrado com esse e-mail" }, 404),
        );
      return Promise.reject(new Error(`unexpected fetch: ${url} ${init?.method}`));
    });
    vi.stubGlobal("fetch", fetchMock);

    renderModal();
    await screen.findByText(/Ainda não compartilhado/);

    fireEvent.change(screen.getByPlaceholderText("e-mail da pessoa"), {
      target: { value: "fantasma@example.com" },
    });
    fireEvent.click(screen.getByText("Compartilhar"));

    await screen.findByText("Não existe usuário cadastrado com esse e-mail");
  });
});
