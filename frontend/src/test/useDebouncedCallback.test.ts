import { act, renderHook } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { useDebouncedCallback } from "../hooks/useDebouncedCallback";

describe("useDebouncedCallback", () => {
  beforeEach(() => vi.useFakeTimers());
  afterEach(() => vi.useRealTimers());

  it("agrupa chamadas dentro do delay", () => {
    const fn = vi.fn();
    const { result } = renderHook(() => useDebouncedCallback(fn, 1000));

    act(() => result.current());
    act(() => result.current());
    expect(fn).not.toHaveBeenCalled();

    act(() => vi.advanceTimersByTime(1000));
    expect(fn).toHaveBeenCalledTimes(1);
  });
});
