# Plan 001 — Caderno Folium (MVP)

> Plano técnico gerado a partir da `spec.md`. Aqui vive o **como**.
> Stack e arquitetura escolhidas após análise de opções (ver pesquisa).

## Stack

| Camada | Tecnologia |
|---|---|
| Backend | Python 3.12 + FastAPI + Uvicorn (ASGI) |
| ORM/Migrations | SQLAlchemy 2.0 (async) + Alembic |
| Validação | Pydantic v2 |
| Banco | PostgreSQL 16 (JSONB para conteúdo); local via Docker Compose por padrão, ou gerenciado (ex.: Supabase) via `DATABASE_URL` |
| Auth | JWT (`python-jose`) + bcrypt (`passlib`) |
| Frontend | React 18 + TypeScript + Vite |
| Editor | TipTap (@tiptap/react + StarterKit + Color + Highlight + Link + Image + FontFamily + FontSize) |
| Estado/Servidor | TanStack Query (dados) + Zustand (UI) |
| Testes | pytest (back) / vitest + Testing Library (front) |
| Container | Docker + Docker Compose |

## Arquitetura (backend — camadas)

```
api/ (rotas FastAPI, só orquestração)
 └─ services/ (regras de negócio)
     └─ repositories/ (acesso a dados, interfaces)
         └─ domain/ (entidades, enums)
schemas/ (DTOs Pydantic)
core/ (config, security JWT, deps)
storage/ (port + adapters: local / S3)
```

- **Ports & Adapters**: `StoragePort` (save/get/delete) com adaptador `LocalStorage` no MVP e `S3Storage` futuramente.
- **Repository pattern**: `UserRepository`, `NotebookRepository`, `PageRepository`, `AssetRepository` atrás de interfaces.
- **Service layer**: `AuthService`, `NotebookService`, `PageService`, `AssetService`, `ContentService`.
- **DI**: tudo injetado via `Depends` (FastAPI).

## Arquitetura (frontend — estrutura)

```
src/
├─ api/            (client HTTP + tipagem das rotas)
├─ features/
│  ├─ auth/        (login, register, AuthContext)
│  ├─ theme/       (ThemeContext, alternância claro/escuro)
│  ├─ notebooks/   (lista, criação)
│  ├─ editor/      (TipTap + toolbar + autosave)
│  └─ pages/       (navegação, página)
├─ components/     (UI reutilizável)
├─ hooks/          (useAutosave, useDebounce)
├─ store/          (Zustand)
└─ styles/         (linhas de caderno, tema)
```

## Modelo de Dados (SQL)

```sql
users(id PK, email UNIQUE, password_hash, created_at)

notebooks(id PK, user_id FK->users ON DELETE CASCADE,
          name, page_mode ENUM('fixed','continuous'),
          line_color, line_spacing, created_at, updated_at)

pages(id PK, notebook_id FK->notebooks ON DELETE CASCADE,
      title, position INT, content_json JSONB,
      revision INT DEFAULT 1, created_at, updated_at)

assets(id PK, user_id FK->users ON DELETE CASCADE,
       kind ENUM('image','pdf'), filename, mime, size,
       storage_key, url, created_at)
```

- Índices: `notebooks(user_id)`, `pages(notebook_id, position)`, `assets(user_id)`.
- **Conteúdo**: `content_json` guarda o documento TipTap (ProseMirror JSON), não HTML.
- **Concorrência otimista**: `PUT /pages/{id}/content` exige `revision`; servidor valida e incrementa.

## Contratos de API (resumo)

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/v1/auth/register` | cadastro |
| POST | `/api/v1/auth/login` | login → JWT |
| GET | `/api/v1/notebooks` | lista cadernos |
| POST | `/api/v1/notebooks` | cria caderno |
| PATCH | `/api/v1/notebooks/{id}` | renomeia/configura |
| DELETE | `/api/v1/notebooks/{id}` | exclui caderno |
| GET | `/api/v1/notebooks/{id}/pages` | lista páginas |
| POST | `/api/v1/notebooks/{id}/pages` | cria página |
| PUT | `/api/v1/pages/{id}/content` | autosave (revision) |
| DELETE | `/api/v1/pages/{id}` | exclui página |
| POST | `/api/v1/assets` | upload (multipart) → retorna url |
| GET | `/health` | healthcheck público |

## Fluxo de Autosave

1. Digitação → TipTap `onUpdate` → debounce 1s → `PUT content`.
2. `beforeunload` dispara save imediato (flush) se houver mudança pendente.
3. Falha → fila de retry + indicador "offline/não salvo" na UI.
4. Sucesso → atualiza `revision` local e indicador "salvo".

## Design Patterns aplicados

| Pattern | Onde |
|---|---|
| Repository | `repositories/` |
| Service Layer | `services/` |
| Dependency Injection | `Depends` (back) / hooks + props (front) |
| Ports & Adapters | `storage/` |
| DTO | `schemas/` (Pydantic) |
| Strategy | `StoragePort` (local vs S3) |
| Observer (implícito) | TipTap `onUpdate` → autosave |

## Decisões e Trade-offs

- **TipTap sobre Lexical/Slate**: melhor ecossistema de extensões e caminho direto para Yjs no futuro; trade-off = bundle maior (~50–70KB gz).
- **Sem Hocuspocus no MVP**: sincronização individual via REST; schema JSON pronto para colaboração futura.
- **JSONB em vez de colunas por campo**: conteúdo livre/estruturado, flexível para migrações de formato.
- **Vite SPA em vez de Next.js**: app autenticado, sem SEO; build e deploy mais simples.

## Modo Dark (tema escuro)

- **ThemeContext** (React Context) com estado `light` | `dark`, persistido em
  `localStorage` (`folium_theme`) e aplicado via `data-theme` no `<html>`.
- **CSS Variables** já usadas em `global.css`; o modo dark é um bloco
  `[data-theme="dark"]` que sobrescreve as variáveis (`--bg` preto, `--surface`
  escuro, `--ink` claro, `--paper-bg` e `--paper-line`).
- **Papel do caderno**: em dark, fundo preto (`--paper-bg`) e linhas brancas
  (`--paper-line`). A cor de linha customizada por caderno (`line_color` no
  `PATCH /notebooks/{id}`) sobrescreve o padrão do tema.
- **Cor da caneta**: já existe via TipTap (`setColor`); texto sem cor explícita
  herda `--ink`, então no dark o texto padrão fica claro.
- **Toggle** de tema exposto no topbar (lista de cadernos e editor).
- **Cor da linha**: input de cor no editor que faz `PATCH line_color`. O valor
  default `#9db3c8` é tratado como "auto" (segue o tema); valores customizados
  valem nos dois temas.

## Tipografia expandida (Fase 14)

- **`FontSize`**: extensão própria (`Extension.create`), adiciona o atributo
  `fontSize` à marca `textStyle` já usada pelo `Color`. Mesmo mecanismo de
  bold/cor — aplica a qualquer seleção via `chain().setMark("textStyle", ...)`.
- **`FontFamily`**: pacote oficial `@tiptap/extension-font-family`, também
  sobre `textStyle`. Fontes curadas: Kalam (padrão), Caveat, Patrick Hand,
  Nunito — carregadas via Google Fonts em `index.html`.
- **Por que marca, não bloco**: título (H1-H3) é um nó de bloco no ProseMirror
  — sempre afeta o parágrafo inteiro. Tamanho/fonte precisavam funcionar em
  qualquer trecho selecionado dentro de uma frase, então são marcas inline
  (como bold/itálico/cor), não uma variação de heading.
- **Toolbar**: dois `<select>` nativos (fonte, tamanho), mesmo estilo visual
  dos demais controles.

## Mídia embutida: redimensionar, mover e link clicável (Fase 15)

- **Atributos de posição/tamanho**: `width`, `height`, `x`, `y` (px, nullable)
  adicionados aos nós `Image` (extend) e `PdfEmbed`. Por serem atributos de
  nó do ProseMirror, persistem automaticamente no `content_json` via
  `editor.getJSON()` — sem qualquer mudança no backend/schema.
- **`ResizableEmbed`**: componente React compartilhado entre `ImageView` e
  `PdfEmbedView`, com duas alças:
  - **Mover** (canto superior esquerdo, ícone de grip): ao arrastar, o nó sai
    do fluxo do documento (`position: absolute`), ancorado em `.paper-lines`
    (já `position: relative`), e passa a flutuar livremente sobre a página,
    podendo se sobrepor ao texto.
  - **Redimensionar** (canto inferior direito): ajusta `width`/`height`.
    Imagem trava proporção (`lockAspect: true`); PDF ajusta largura/altura
    de forma independente (`lockAspect: false`).
- **Performance do arrasto**: durante o `mousemove`, o estilo é aplicado
  direto no DOM (sem disparar transação do ProseMirror a cada pixel); os
  atributos do nó (`updateAttributes`) — e por consequência o autosave — só
  são gravados no `mouseup`, ao soltar o mouse.
- **Antes de mover/redimensionar** (atributos ainda `null`): renderiza como
  hoje, dentro do fluxo normal do texto, sem `position: absolute`.
- **Reverter**: não há um botão dedicado para "voltar ao fluxo" nesta versão
  — desfazer com Ctrl+Z (histórico nativo do ProseMirror) resolve.
- **Link**: `openOnClick: true` no `@tiptap/extension-link` (antes era
  `false`), abrindo a URL em nova aba (`target="_blank"`,
  `rel="noopener noreferrer"`) com estilo padronizado (sublinhado, cor de
  acento, cursor pointer) em vez do estilo cru do navegador.
