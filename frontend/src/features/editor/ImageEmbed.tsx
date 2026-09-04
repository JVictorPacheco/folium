import Image from "@tiptap/extension-image";
import { ReactNodeViewRenderer, type NodeViewProps } from "@tiptap/react";

import { ResizableEmbed } from "./ResizableEmbed";

function ImageView({ node, updateAttributes, deleteNode }: NodeViewProps) {
  const { src, alt, title, width, height, x, y } = node.attrs as {
    src: string;
    alt?: string;
    title?: string;
    width: number | null;
    height: number | null;
    x: number | null;
    y: number | null;
  };
  return (
    <ResizableEmbed
      className="image-embed"
      x={x}
      y={y}
      width={width}
      height={height}
      lockAspect
      minWidth={60}
      onChange={(patch) => updateAttributes(patch)}
    >
      <img
        src={src}
        alt={alt}
        title={title}
        draggable={false}
        style={width !== null ? { width: "100%", height: "auto" } : undefined}
      />
      <button className="asset-remove" type="button" onClick={deleteNode} title="Remover imagem">
        ✕
      </button>
    </ResizableEmbed>
  );
}

export const ImageEmbed = Image.extend({
  addAttributes() {
    return {
      ...this.parent?.(),
      width: {
        default: null,
        // Aplica o tamanho redimensionado como style no HTML estático
        // (usado na exportação em PDF, que não passa pelo NodeView React).
        renderHTML: (attributes) => {
          if (attributes.width == null) return {};
          return { style: `width: ${attributes.width}px` };
        },
      },
      // height não é renderizado à parte: imagem trava proporção (largura
      // controla, altura acompanha automaticamente).
      height: { default: null, renderHTML: () => ({}) },
      // Posição flutuante (Fase 15) é só para a edição ao vivo — a
      // exportação em PDF sempre segue o fluxo normal do documento (FR-28).
      x: { default: null, renderHTML: () => ({}) },
      y: { default: null, renderHTML: () => ({}) },
    };
  },
  addNodeView() {
    return ReactNodeViewRenderer(ImageView);
  },
});
