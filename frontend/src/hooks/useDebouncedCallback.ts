import { useCallback, useEffect, useRef } from "react";

export function useDebouncedCallback<T extends (...args: never[]) => void>(
  fn: T,
  delay: number,
): T {
  const fnRef = useRef(fn);
  fnRef.current = fn;
  const timerRef = useRef<number>();

  const debounced = useCallback(
    (...args: never[]) => {
      if (timerRef.current) window.clearTimeout(timerRef.current);
      timerRef.current = window.setTimeout(() => fnRef.current(...args), delay);
    },
    [delay],
  );

  useEffect(
    () => () => {
      if (timerRef.current) window.clearTimeout(timerRef.current);
    },
    [],
  );

  return debounced as T;
}
