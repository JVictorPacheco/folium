import { afterEach, describe, expect, it, vi } from "vitest";

import { ApiError, api, resolveAssetUrl } from "./client";

describe("resolveAssetUrl", () => {
  it("mantém URLs absolutas como estão", () => {
    expect(resolveAssetUrl("http://cdn.example.com/x.png")).toBe("http://cdn.example.com/x.png");
    expect(resolveAssetUrl("https://cdn.example.com/x.png")).toBe("https://cdn.example.com/x.png");
  });

  it("prefixa o BASE_URL em URLs relativas (com barra)", () => {
    expect(resolveAssetUrl("/media/1/image/x.png")).toBe("http://localhost:8000/media/1/image/x.png");
  });

  it("prefixa o BASE_URL em URLs relativas (sem barra)", () => {
    expect(resolveAssetUrl("media/1/image/x.png")).toBe("http://localhost:8000/media/1/image/x.png");
  });
});

describe("api (tratamento de erro)", () => {
  afterEach(() => vi.restoreAllMocks());

  it("extrai o campo detail do corpo JSON de erro", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(
        new Response(JSON.stringify({ detail: "Credenciais inválidas" }), {
          status: 401,
          headers: { "Content-Type": "application/json" },
        }),
      ),
    );

    await expect(api.post("/api/v1/auth/login", {})).rejects.toEqual(
      new ApiError(401, "Credenciais inválidas"),
    );
  });

  it("mantém o texto cru quando o corpo de erro não é JSON", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue(new Response("erro interno", { status: 500 })),
    );

    await expect(api.get("/api/v1/notebooks")).rejects.toEqual(new ApiError(500, "erro interno"));
  });
});
