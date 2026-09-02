import Image from "@tiptap/extension-image";
import { NodeViewWrapper, ReactNodeViewRenderer, type NodeViewProps } from "@tiptap/react";

function ImageView({ node, deleteNode }: NodeViewProps) {
  const { src, alt, title } = node.attrs as { src: string; alt?: string; title?: string };
  return (
    <NodeViewWrapper className="image-embed">
      <img src={src} alt={alt} title={title} />
      <button className="asset-remove" type="button" onClick={deleteNode} title="Remover imagem">
        ✕
      </button>
    </NodeViewWrapper>
  );
}

export const ImageEmbed = Image.extend({
  addNodeView() {
    return ReactNodeViewRenderer(ImageView);
  },
});
