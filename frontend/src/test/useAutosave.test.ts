import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { api } from "../api/client";
import { useAutosave } from "../hooks/useAutosave";

vi.mock("../api/client", () => ({
  api: { put: vi.fn() },
}));

const put = vi.mocked(api.put);

function setup(overrides: Partial<Parameters<typeof useAutosave>[0]> = {}) {
  const onRevision = vi.fn();
  const getJson = vi.fn(() => ({ type: "doc" }));
  const hook = renderHook(() =>
    useAutosave({
      pageId: 7,
      revision: 1,
      getJson,
      onRevision,
      delay: 1000,
      ...overrides,
    }),
  );
  return { hook, onRevision, getJson };
}

describe("useAutosave", () => {
  beforeEach(() => {
    vi.useFakeTimers();
    put.mockReset();
  });
  afterEach(() => vi.useRealTimers());

  it("salva após o debounce e atualiza a revision", async () => {
    put.mockResolvedValue({ revision: 2 });
    const { hook, onRevision, getJson } = setup();

    act(() => hook.result.current.schedule());
    expect(hook.result.current.status).toBe("unsaved");
    expect(put).not.toHaveBeenCalled();

    await act(async () => {
      vi.advanceTimersByTime(1000);
    });

    expect(put).toHaveBeenCalledWith("/api/v1/pages/7/content", {
      content_json: { type: "doc" },
      revision: 1,
    });
    expect(onRevision).toHaveBeenCalledWith(2);
    expect(getJson).toHaveBeenCalled();
    expect(hook.result.current.status).toBe("saved");
  });

  it("agrupa múltiplos schedules em um único save", async () => {
    put.mockResolvedValue({ revision: 2 });
    const { hook } = setup();

    act(() => hook.result.current.schedule());
    act(() => hook.result.current.schedule());
    act(() => hook.result.current.schedule());

    await act(async () => {
      vi.advanceTimersByTime(1000);
    });

    expect(put).toHaveBeenCalledTimes(1);
  });

  it("não chama a API quando não há mudanças pendentes", async () => {
    const { hook } = setup();

    await act(async () => {
      await hook.result.current.flush();
    });

    expect(put).not.toHaveBeenCalled();
    expect(hook.result.current.status).toBe("saved");
  });

  it("não salva enquanto não há página criada (id <= 0) e mantém pendente", async () => {
    const { hook } = setup({ pageId: 0 });

    act(() => hook.result.current.schedule());
    await act(async () => {
      vi.advanceTimersByTime(1000);
    });

    expect(put).not.toHaveBeenCalled();
    expect(hook.result.current.status).toBe("unsaved");
  });

  it("marca erro e permite retry na próxima edição", async () => {
    put.mockRejectedValueOnce(new Error("rede fora"));
    const { hook } = setup();

    act(() => hook.result.current.schedule());
    await act(async () => {
      vi.advanceTimersByTime(1000);
    });
    expect(hook.result.current.status).toBe("error");

    put.mockResolvedValueOnce({ revision: 2 });
    act(() => hook.result.current.schedule());
    await act(async () => {
      vi.advanceTimersByTime(1000);
    });
    expect(hook.result.current.status).toBe("saved");
    expect(put).toHaveBeenCalledTimes(2);
  });

  it("faz flush imediato no beforeunload", async () => {
    put.mockResolvedValue({ revision: 2 });
    const { hook } = setup();

    act(() => hook.result.current.schedule());
    await act(async () => {
      window.dispatchEvent(new Event("beforeunload"));
    });

    expect(put).toHaveBeenCalledTimes(1);
  });
});
