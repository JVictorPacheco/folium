import { useRef, type ChangeEvent } from "react";
import type { Editor } from "@tiptap/react";

import { uploadAsset } from "../../api/client";
import { FONT_FAMILIES, FONT_SIZES } from "./extensions";

export default function Toolbar({ editor }: { editor: Editor }) {
  const imageInput = useRef<HTMLInputElement>(null);
  const pdfInput = useRef<HTMLInputElement>(null);

  async function onImage(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const asset = await uploadAsset(file, "image");
    editor.chain().focus().setImage({ src: asset.url }).run();
    e.target.value = "";
  }

  async function onPdf(e: ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    const asset = await uploadAsset(file, "pdf");
    editor
      .chain()
      .focus()
      .insertContent({ type: "pdfEmbed", attrs: { src: asset.url, title: file.name } })
      .run();
    e.target.value = "";
  }

  function setLink() {
    const href = window.prompt("URL do link:");
    if (href) editor.chain().focus().setLink({ href }).run();
  }

  const cls = (active: boolean) => `toolbar-btn${active ? " active" : ""}`;

  return (
    <div className="toolbar">
      <button className={cls(editor.isActive("bold"))} onClick={() => editor.chain().focus().toggleBold().run()} title="Negrito">
        B
      </button>
      <button className={cls(editor.isActive("italic"))} onClick={() => editor.chain().focus().toggleItalic().run()} title="Itálico">
        I
      </button>
      <button className={cls(editor.isActive("underline"))} onClick={() => editor.chain().focus().toggleUnderline().run()} title="Sublinhado">
        U
      </button>

      <span className="separator" />

      <button className={cls(editor.isActive("heading", { level: 1 }))} onClick={() => editor.chain().focus().toggleHeading({ level: 1 }).run()} title="Título 1">
        H1
      </button>
      <button className={cls(editor.isActive("heading", { level: 2 }))} onClick={() => editor.chain().focus().toggleHeading({ level: 2 }).run()} title="Título 2">
        H2
      </button>
      <button className={cls(editor.isActive("heading", { level: 3 }))} onClick={() => editor.chain().focus().toggleHeading({ level: 3 }).run()} title="Título 3">
        H3
      </button>

      <span className="separator" />

      <button className={cls(editor.isActive("bulletList"))} onClick={() => editor.chain().focus().toggleBulletList().run()} title="Lista">
        • Lista
      </button>
      <button className={cls(editor.isActive("orderedList"))} onClick={() => editor.chain().focus().toggleOrderedList().run()} title="Lista numerada">
        1. Lista
      </button>

      <span className="separator" />

      <label className="toolbar-btn" title="Cor da caneta">
        Cor
        <input
          type="color"
          className="color-input"
          onChange={(e) => editor.chain().focus().setColor(e.target.value).run()}
        />
      </label>
      <button className={cls(editor.isActive("highlight"))} onClick={() => editor.chain().focus().toggleHighlight().run()} title="Marcador">
        Marca
      </button>

      <span className="separator" />

      <select
        className="toolbar-select"
        title="Fonte do trecho selecionado"
        value={editor.getAttributes("textStyle").fontFamily ?? ""}
        onChange={(e) => {
          const value = e.target.value;
          if (value) editor.chain().focus().setFontFamily(value).run();
          else editor.chain().focus().unsetFontFamily().run();
        }}
      >
        <option value="">Fonte</option>
        {FONT_FAMILIES.map((f) => (
          <option key={f.value} value={f.value}>
            {f.label}
          </option>
        ))}
      </select>

      <select
        className="toolbar-select"
        title="Tamanho do trecho selecionado"
        value={editor.getAttributes("textStyle").fontSize ?? ""}
        onChange={(e) => {
          const value = e.target.value;
          if (value) editor.chain().focus().setFontSize(value).run();
          else editor.chain().focus().unsetFontSize().run();
        }}
      >
        {FONT_SIZES.map((s) => (
          <option key={s.label} value={s.value}>
            {s.label}
          </option>
        ))}
      </select>

      <span className="separator" />

      <button className="toolbar-btn" onClick={setLink} title="Inserir link">
        Link
      </button>
      <button className="toolbar-btn" onClick={() => imageInput.current?.click()} title="Inserir imagem">
        Imagem
      </button>
      <button className="toolbar-btn" onClick={() => pdfInput.current?.click()} title="Inserir PDF">
        PDF
      </button>

      <input ref={imageInput} type="file" accept="image/png,image/jpeg,image/webp,image/gif" hidden onChange={onImage} />
      <input ref={pdfInput} type="file" accept="application/pdf" hidden onChange={onPdf} />
    </div>
  );
}
