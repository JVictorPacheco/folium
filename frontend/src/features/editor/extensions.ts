import Color from "@tiptap/extension-color";
import FontFamily from "@tiptap/extension-font-family";
import Highlight from "@tiptap/extension-highlight";
import Link from "@tiptap/extension-link";
import Placeholder from "@tiptap/extension-placeholder";
import TextStyle from "@tiptap/extension-text-style";
import Underline from "@tiptap/extension-underline";
import StarterKit from "@tiptap/starter-kit";

import { FontSize } from "./FontSize";
import { ImageEmbed } from "./ImageEmbed";
import { PdfEmbed } from "./PdfEmbed";

export const FONT_FAMILIES = [
  { label: "Kalam", value: "Kalam, cursive" },
  { label: "Caveat", value: "Caveat, cursive" },
  { label: "Patrick Hand", value: '"Patrick Hand", cursive' },
  { label: "Nunito", value: "Nunito, sans-serif" },
];

export const FONT_SIZES = [
  { label: "Pequeno", value: "0.85rem" },
  { label: "Normal", value: "" },
  { label: "Grande", value: "1.3rem" },
  { label: "Enorme", value: "1.8rem" },
];

export const editorExtensions = [
  StarterKit.configure({ heading: { levels: [1, 2, 3] } }),
  Underline,
  TextStyle,
  Color,
  FontFamily,
  FontSize,
  Highlight.configure({ multicolor: true }),
  Link.configure({ openOnClick: false, autolink: true }),
  ImageEmbed.configure({ inline: false }),
  Placeholder.configure({ placeholder: "Escreva aqui..." }),
  PdfEmbed,
];
