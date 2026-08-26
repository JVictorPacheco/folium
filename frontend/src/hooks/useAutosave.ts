import { useCallback, useEffect, useRef, useState } from "react";

import { api } from "../api/client";

export type AutosaveStatus = "saved" | "unsaved" | "saving" | "error";

interface AutosaveArgs {
  pageId: number;
  revision: number;
  getJson: () => Record<string, unknown>;
  onRevision: (revision: number) => void;
  delay?: number;
  maxRetries?: number;
}

export function useAutosave({
  pageId,
  revision,
  getJson,
  onRevision,
  delay = 1000,
  maxRetries = 5,
}: AutosaveArgs) {
  const [status, setStatus] = useState<AutosaveStatus>("saved");

  const pageIdRef = useRef(pageId);
  pageIdRef.current = pageId;
  const revisionRef = useRef(revision);
  revisionRef.current = revision;
  const onRevisionRef = useRef(onRevision);
  onRevisionRef.current = onRevision;
  const getJsonRef = useRef(getJson);
  getJsonRef.current = getJson;

  const dirtyRef = useRef(false);
  const timerRef = useRef<number>();
  const retryTimerRef = useRef<number>();
  const attemptsRef = useRef(0);

  const flush = useCallback(async () => {
    if (!dirtyRef.current) return;
    if (pageIdRef.current <= 0) return;

    const savingPageId = pageIdRef.current;
    dirtyRef.current = false;
    setStatus("saving");

    try {
      const res = await api.put<{ revision: number }>(
        `/api/v1/pages/${savingPageId}/content`,
        { content_json: getJsonRef.current(), revision: revisionRef.current },
      );
      if (pageIdRef.current !== savingPageId) return;
      attemptsRef.current = 0;
      onRevisionRef.current(res.revision);
      setStatus("saved");
    } catch {
      if (pageIdRef.current !== savingPageId) return;
      dirtyRef.current = true;
      setStatus("error");
      if (attemptsRef.current < maxRetries) {
        attemptsRef.current += 1;
        if (retryTimerRef.current) window.clearTimeout(retryTimerRef.current);
        retryTimerRef.current = window.setTimeout(() => void flush(), 2500);
      }
    }
  }, [maxRetries]);

  const schedule = useCallback(() => {
    attemptsRef.current = 0;
    dirtyRef.current = true;
    setStatus("unsaved");
    if (timerRef.current) window.clearTimeout(timerRef.current);
    if (retryTimerRef.current) window.clearTimeout(retryTimerRef.current);
    timerRef.current = window.setTimeout(() => void flush(), delay);
  }, [flush, delay]);

  useEffect(() => {
    const onUnload = () => {
      if (dirtyRef.current) void flush();
    };
    window.addEventListener("beforeunload", onUnload);
    return () => {
      window.removeEventListener("beforeunload", onUnload);
      if (timerRef.current) window.clearTimeout(timerRef.current);
      if (retryTimerRef.current) window.clearTimeout(retryTimerRef.current);
    };
  }, [flush]);

  return { status, schedule, flush };
}
