import { getSchema, type JSONContent } from "@tiptap/core";
import { DOMSerializer, Node as ProseMirrorNode } from "@tiptap/pm/model";

import type { Notebook, Page } from "../../api/types";
import { editorExtensions } from "./extensions";

const EMPTY_PARAGRAPH: JSONContent = { type: "doc", content: [{ type: "paragraph" }] };

// Schema construído uma vez (mesmas extensões do editor ao vivo).
const schema = getSchema(editorExtensions);

/**
 * Serializa o `content_json` de uma página para HTML usando o DOM real do
 * navegador (via `DOMSerializer` do ProseMirror). Não usa `@tiptap/html`:
 * aquele pacote serializa num DOM headless (`zeed-dom`) que não sincroniza
 * `element.style.cssText` de volta pro atributo `style` — qualquer marca que
 * dependa de `style` (cor, fonte, tamanho, largura da imagem) sai sem
 * formatação nenhuma. Com o DOM real do navegador isso funciona certo.
 */
function pageHtml(page: Page): string {
  const doc =
    page.content_json && Object.keys(page.content_json).length > 0
      ? (page.content_json as JSONContent)
      : EMPTY_PARAGRAPH;
  try {
    const node = ProseMirrorNode.fromJSON(schema, doc);
    const fragment = DOMSerializer.fromSchema(schema).serializeFragment(node.content, { document });
    const wrapper = document.createElement("div");
    wrapper.appendChild(fragment);
    return wrapper.innerHTML;
  } catch {
    // Conteúdo corrompido/incompatível não deve travar a exportação inteira.
    return "<p></p>";
  }
}

/**
 * Monta uma view de impressão com todas as páginas do caderno (mesmas
 * classes/CSS do editor, então linhas/cores/fontes saem idênticas) e aciona
 * a impressão nativa do navegador. A view some sozinha após imprimir/cancelar.
 */
export function exportNotebookPdf(notebook: Notebook, pages: Page[]) {
  const sorted = [...pages].sort((a, b) => a.position - b.position);
  const paperClass =
    notebook.page_mode === "fixed" ? "paper paper--fixed" : "paper paper--continuous";

  const root = document.createElement("div");
  root.id = "print-root";

  for (const page of sorted) {
    const sheet = document.createElement("div");
    sheet.className = `print-sheet ${paperClass}`;
    sheet.style.setProperty("--line-spacing", `${notebook.line_spacing}px`);
    if (notebook.line_color) sheet.style.setProperty("--line-color", notebook.line_color);

    const lines = document.createElement("div");
    lines.className = "paper-lines";

    const prose = document.createElement("div");
    prose.className = "ProseMirror";
    prose.innerHTML = pageHtml(page);

    lines.appendChild(prose);
    sheet.appendChild(lines);
    root.appendChild(sheet);
  }

  document.body.appendChild(root);

  function cleanup() {
    root.remove();
    window.removeEventListener("afterprint", cleanup);
  }
  window.addEventListener("afterprint", cleanup);

  window.print();
}
