import { Node, mergeAttributes } from "@tiptap/core";
import { type NodeViewProps, ReactNodeViewRenderer } from "@tiptap/react";

import { ResizableEmbed } from "./ResizableEmbed";

function PdfEmbedView({ node, updateAttributes, deleteNode }: NodeViewProps) {
  const { src, title, width, height, x, y } = node.attrs as {
    src: string;
    title: string;
    width: number | null;
    height: number | null;
    x: number | null;
    y: number | null;
  };
  return (
    <ResizableEmbed
      className="pdf-embed"
      x={x}
      y={y}
      width={width}
      height={height}
      minWidth={120}
      minHeight={120}
      onChange={(patch) => updateAttributes(patch)}
    >
      <iframe src={src} title={title} />
      <button className="asset-remove" type="button" onClick={deleteNode} title="Remover PDF">
        ✕
      </button>
    </ResizableEmbed>
  );
}

export const PdfEmbed = Node.create({
  name: "pdfEmbed",
  group: "block",
  atom: true,

  addAttributes() {
    return {
      src: { default: null },
      title: { default: "PDF" },
      width: {
        default: null,
        renderHTML: (attributes) => {
          if (attributes.width == null) return {};
          return { style: `width: ${attributes.width}px` };
        },
      },
      height: {
        default: null,
        renderHTML: (attributes) => {
          if (attributes.height == null) return {};
          return { style: `height: ${attributes.height}px` };
        },
      },
      // Posição flutuante (Fase 15) é só para a edição ao vivo — a
      // exportação em PDF sempre segue o fluxo normal do documento (FR-28).
      x: { default: null, renderHTML: () => ({}) },
      y: { default: null, renderHTML: () => ({}) },
    };
  },

  parseHTML() {
    return [{ tag: "div[data-pdf-embed]" }];
  },

  // Usado só fora da edição ao vivo (o NodeView React cobre o editor) —
  // é o que aparece na exportação em PDF. Embutir o iframe de fato numa
  // impressão é frágil entre navegadores, então mostra um "cartão" com
  // nome do arquivo, do tamanho redimensionado, no lugar do visualizador.
  renderHTML({ HTMLAttributes, node }) {
    return [
      "div",
      mergeAttributes(HTMLAttributes, { "data-pdf-embed": "", class: "pdf-embed-static" }),
      ["span", {}, `📄 ${node.attrs.title || "PDF"}`],
    ];
  },

  addNodeView() {
    return ReactNodeViewRenderer(PdfEmbedView);
  },
});
