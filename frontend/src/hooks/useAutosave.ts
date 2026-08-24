import { useCallback, useEffect, useRef, useState } from "react";

import { api } from "../api/client";

export type AutosaveStatus = "saved" | "unsaved" | "saving" | "error";

interface AutosaveArgs {
  pageId: number;
  revision: number;
  getJson: () => Record<string, unknown>;
  onRevision: (revision: number) => void;
  delay?: number;
}

export function useAutosave({ pageId, revision, getJson, onRevision, delay = 1000 }: AutosaveArgs) {
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

  const flush = useCallback(async () => {
    if (!dirtyRef.current) return;
    dirtyRef.current = false;
    setStatus("saving");
    try {
      const res = await api.put<{ revision: number }>(
        `/api/v1/pages/${pageIdRef.current}/content`,
        { content_json: getJsonRef.current(), revision: revisionRef.current },
      );
      onRevisionRef.current(res.revision);
      setStatus("saved");
    } catch {
      dirtyRef.current = true;
      setStatus("error");
    }
  }, []);

  const schedule = useCallback(() => {
    dirtyRef.current = true;
    setStatus("unsaved");
    if (timerRef.current) window.clearTimeout(timerRef.current);
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
    };
  }, [flush]);

  return { status, schedule, flush };
}
