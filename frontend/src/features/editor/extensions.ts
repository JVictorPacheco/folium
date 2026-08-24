import Color from "@tiptap/extension-color";
import Highlight from "@tiptap/extension-highlight";
import Image from "@tiptap/extension-image";
import Link from "@tiptap/extension-link";
import Placeholder from "@tiptap/extension-placeholder";
import TextStyle from "@tiptap/extension-text-style";
import Underline from "@tiptap/extension-underline";
import StarterKit from "@tiptap/starter-kit";

import { PdfEmbed } from "./PdfEmbed";

export const editorExtensions = [
  StarterKit.configure({ heading: { levels: [1, 2, 3] } }),
  Underline,
  TextStyle,
  Color,
  Highlight.configure({ multicolor: true }),
  Link.configure({ openOnClick: false, autolink: true }),
  Image.configure({ inline: false }),
  Placeholder.configure({ placeholder: "Escreva aqui..." }),
  PdfEmbed,
];
