import { useEffect, useRef, type CSSProperties, type MouseEvent as ReactMouseEvent, type ReactNode } from "react";
import { NodeViewWrapper } from "@tiptap/react";

export interface EmbedGeometry {
  x: number | null;
  y: number | null;
  width: number | null;
  height: number | null;
}

interface ResizableEmbedProps extends EmbedGeometry {
  className: string;
  lockAspect?: boolean;
  minWidth?: number;
  minHeight?: number;
  onChange: (patch: Partial<EmbedGeometry>) => void;
  children: ReactNode;
}

export function ResizableEmbed({
  className,
  x,
  y,
  width,
  height,
  lockAspect = false,
  minWidth = 60,
  minHeight = 60,
  onChange,
  children,
}: ResizableEmbedProps) {
  const ref = useRef<HTMLDivElement>(null);
  const shieldRef = useRef<HTMLDivElement>(null);
  // Se o node view desmontar no meio de um arrasto (nó excluído, troca de
  // página), essa ref cancela os listeners de window pendentes em vez de
  // deixá-los vazando e tentando atualizar um nó que não existe mais.
  const cancelDragRef = useRef<(() => void) | null>(null);

  useEffect(() => () => cancelDragRef.current?.(), []);

  // Iframes (PDF) capturam eventos de mouse — sem esse "escudo" por cima,
  // o arrasto engasga/perde o rastro quando o cursor passa sobre o PDF.
  function showShield() {
    if (shieldRef.current) shieldRef.current.style.display = "block";
  }
  function hideShield() {
    if (shieldRef.current) shieldRef.current.style.display = "none";
  }

  function startMove(e: ReactMouseEvent) {
    if (e.button !== 0) return;
    e.preventDefault();
    e.stopPropagation();
    const el = ref.current;
    if (!el) return;

    const startClientX = e.clientX;
    const startClientY = e.clientY;
    const originLeft = el.offsetLeft;
    const originTop = el.offsetTop;
    const originWidth = el.offsetWidth;

    el.style.position = "absolute";
    el.style.left = `${originLeft}px`;
    el.style.top = `${originTop}px`;
    el.style.width = `${originWidth}px`;
    showShield();

    function onMove(ev: globalThis.MouseEvent) {
      el!.style.left = `${originLeft + (ev.clientX - startClientX)}px`;
      el!.style.top = `${originTop + (ev.clientY - startClientY)}px`;
    }
    function cleanup() {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
      cancelDragRef.current = null;
      hideShield();
    }
    function onUp(ev: globalThis.MouseEvent) {
      cleanup();
      onChange({
        x: originLeft + (ev.clientX - startClientX),
        y: originTop + (ev.clientY - startClientY),
        width: originWidth,
      });
    }
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
    cancelDragRef.current = cleanup;
  }

  function startResize(e: ReactMouseEvent) {
    if (e.button !== 0) return;
    e.preventDefault();
    e.stopPropagation();
    const el = ref.current;
    if (!el) return;

    const startClientX = e.clientX;
    const startClientY = e.clientY;
    const startWidth = el.offsetWidth;
    const startHeight = el.offsetHeight;
    const ratio = startWidth / startHeight;
    showShield();

    function onMove(ev: globalThis.MouseEvent) {
      const newWidth = Math.max(minWidth, startWidth + (ev.clientX - startClientX));
      el!.style.width = `${newWidth}px`;
      if (lockAspect) {
        el!.style.height = `${newWidth / ratio}px`;
      } else {
        const newHeight = Math.max(minHeight, startHeight + (ev.clientY - startClientY));
        el!.style.height = `${newHeight}px`;
      }
    }
    function cleanup() {
      window.removeEventListener("mousemove", onMove);
      window.removeEventListener("mouseup", onUp);
      cancelDragRef.current = null;
      hideShield();
    }
    function onUp() {
      cleanup();
      onChange({
        width: el!.offsetWidth,
        height: lockAspect ? null : el!.offsetHeight,
      });
    }
    window.addEventListener("mousemove", onMove);
    window.addEventListener("mouseup", onUp);
    cancelDragRef.current = cleanup;
  }

  const style: CSSProperties = {};
  if (x !== null && y !== null) {
    style.position = "absolute";
    style.left = x;
    style.top = y;
  }
  if (width !== null) style.width = width;
  if (height !== null) style.height = height;

  return (
    <NodeViewWrapper as="div" ref={ref} className={className} style={style}>
      <button
        type="button"
        className="embed-move-handle"
        onMouseDown={startMove}
        title="Mover"
      >
        ⠿
      </button>
      {children}
      <div ref={shieldRef} className="embed-drag-shield" />
      <div className="embed-resize-handle" onMouseDown={startResize} title="Redimensionar" />
    </NodeViewWrapper>
  );
}
