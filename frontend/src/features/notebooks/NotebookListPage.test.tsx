import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { MemoryRouter } from "react-router-dom";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("../auth/AuthContext", () => ({
  useAuth: () => ({ logout: vi.fn() }),
}));

import NotebookListPage from "./NotebookListPage";
import { ThemeProvider } from "../theme/ThemeContext";

const NOTEBOOKS = [
  {
    id: 1,
    name: "Receitas",
    page_mode: "continuous",
    line_color: "#D9CDB4",
    line_spacing: 28,
    tags: ["cozinha"],
    created_at: "2026-09-01T00:00:00Z",
    updated_at: "2026-09-01T00:00:00Z",
  },
];

const TAGS = [{ id: 1, name: "cozinha" }];

function jsonResponse(body: unknown, status = 200) {
  return new Response(JSON.stringify(body), { status, headers: { "Content-Type": "application/json" } });
}

function renderPage() {
  const qc = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  render(
    <QueryClientProvider client={qc}>
      <MemoryRouter>
        <ThemeProvider>
          <NotebookListPage />
        </ThemeProvider>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("NotebookListPage — busca e tags", () => {
  afterEach(() => vi.restoreAllMocks());

  it("lista cadernos com chips de tag", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn((url: string) => {
        if (url.includes("/api/v1/notebooks")) return Promise.resolve(jsonResponse(NOTEBOOKS));
        if (url.endsWith("/api/v1/tags")) return Promise.resolve(jsonResponse(TAGS));
        return Promise.reject(new Error(`unexpected fetch: ${url}`));
      }),
    );

    renderPage();

    await screen.findByText("Receitas");
    expect(screen.getByText("cozinha", { selector: ".tag-chip" })).toBeInTheDocument();
  });

  it("busca dispara /api/v1/search com debounce e mostra resultados", async () => {
    const searchResults = [
      {
        notebook_id: 1,
        notebook_name: "Receitas",
        page_id: 5,
        page_title: "Bolo",
        snippet: "…bolo de cenoura…",
      },
    ];
    const fetchMock = vi.fn((url: string) => {
      if (url.includes("/api/v1/search")) return Promise.resolve(jsonResponse(searchResults));
      if (url.includes("/api/v1/notebooks")) return Promise.resolve(jsonResponse(NOTEBOOKS));
      if (url.endsWith("/api/v1/tags")) return Promise.resolve(jsonResponse(TAGS));
      return Promise.reject(new Error(`unexpected fetch: ${url}`));
    });
    vi.stubGlobal("fetch", fetchMock);

    renderPage();
    await screen.findByText("Receitas");

    fireEvent.change(screen.getByPlaceholderText("Buscar em todos os cadernos..."), {
      target: { value: "cenoura" },
    });

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringContaining("/api/v1/search?q=cenoura"),
        expect.anything(),
      ),
    );
    await screen.findByText(/bolo de cenoura/);
  });

  it("editar tags chama PATCH com a lista digitada no prompt", async () => {
    const fetchMock = vi.fn((url: string, init?: RequestInit) => {
      if (url.includes("/api/v1/notebooks") && (!init || init.method === "GET" || init.method === undefined))
        return Promise.resolve(jsonResponse(NOTEBOOKS));
      if (url.endsWith("/api/v1/tags")) return Promise.resolve(jsonResponse(TAGS));
      if (url.match(/\/api\/v1\/notebooks\/1$/) && init?.method === "PATCH")
        return Promise.resolve(jsonResponse({ ...NOTEBOOKS[0], tags: ["cozinha", "familia"] }));
      return Promise.reject(new Error(`unexpected fetch: ${url} ${init?.method}`));
    });
    vi.stubGlobal("fetch", fetchMock);
    vi.spyOn(window, "prompt").mockReturnValue("cozinha, familia");

    renderPage();
    await screen.findByText("Receitas");

    fireEvent.click(screen.getByTitle("Editar tags"));

    await waitFor(() =>
      expect(fetchMock).toHaveBeenCalledWith(
        expect.stringMatching(/\/api\/v1\/notebooks\/1$/),
        expect.objectContaining({ method: "PATCH" }),
      ),
    );
  });
});
