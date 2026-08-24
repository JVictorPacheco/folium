import { Node, mergeAttributes } from "@tiptap/core";
import { NodeViewWrapper, ReactNodeViewRenderer, type NodeViewProps } from "@tiptap/react";

function PdfEmbedView({ node }: NodeViewProps) {
  const { src, title } = node.attrs as { src: string; title: string };
  return (
    <NodeViewWrapper className="pdf-embed">
      <iframe src={src} title={title} />
    </NodeViewWrapper>
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
