export interface Notebook {
  id: number;
  name: string;
  page_mode: "fixed" | "continuous";
  line_color: string;
  line_spacing: number;
  created_at: string;
  updated_at: string;
}

export interface Page {
  id: number;
  notebook_id: number;
  title: string;
  position: number;
  content_json: Record<string, unknown>;
  revision: number;
  created_at: string;
  updated_at: string;
}

export interface Asset {
  id: number;
  kind: "image" | "pdf";
  filename: string;
  mime: string;
  size: number;
  url: string;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}
