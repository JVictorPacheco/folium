import { describe, expect, it } from "vitest";

import { resolveAssetUrl } from "./client";

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
