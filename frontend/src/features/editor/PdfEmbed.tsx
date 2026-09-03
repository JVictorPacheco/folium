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
      width: { default: null },
      height: { default: null },
      x: { default: null },
      y: { default: null },
    };
  },

  parseHTML() {
    return [{ tag: "div[data-pdf-embed]" }];
  },

  renderHTML({ HTMLAttributes }) {
    return ["div", mergeAttributes(HTMLAttributes, { "data-pdf-embed": "" })];
  },

  addNodeView() {
    return ReactNodeViewRenderer(PdfEmbedView);
  },
});
