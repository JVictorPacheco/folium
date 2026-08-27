# Tasks 001 — Caderno Folium (MVP)

> Lista de tarefas derivada de `plan.md`. Marcador `[P]` = paralelizável.
> Ordem respeita dependências. Executar em fases.

## Fase 1 — Fundação

- [x] T1.1 [P] Scaffold backend FastAPI (estrutura de pastas, `pyproject.toml`, Uvicorn, healthcheck)
- [x] T1.2 [P] Scaffold frontend Vite + React + TypeScript (com ESLint/Prettier)
- [x] T1.3 [P] Docker + Docker Compose (Postgres + backend + frontend)
- [x] T1.4 Configurar Alembic e primeira migração (tabelas `users`, `notebooks`, `pages`, `assets`)

## Fase 2 — Auth

- [x] T2.1 Modelo `User` + `UserRepository` (get_by_email, create)
- [x] T2.2 `AuthService` (hash bcrypt, geração/validação JWT)
- [x] T2.3 Schemas e rotas `/auth/register` e `/auth/login`
- [x] T2.4 Dependência `get_current_user` (decodifica JWT)
- [x] T2.5 Testes de auth (unit + integração)

## Fase 3 — Cadernos e Páginas

- [x] T3.1 Modelos `Notebook` e `Page` + repositórios
- [x] T3.2 `NotebookService` (CRUD com isolamento por `user_id`)
- [x] T3.3 `PageService` (criar/ordenar/excluir páginas)
- [x] T3.4 Rotas REST de notebooks e páginas + schemas
- [x] T3.5 Testes de notebooks/páginas (inclui teste de isolamento entre usuários)

## Fase 4 — Conteúdo e Autosave

- [x] T4.1 `ContentService` + rota `PUT /pages/{id}/content` (revision, concorrência otimista)
- [x] T4.2 Testes de versionamento/concorrência

## Fase 5 — Upload de Assets

- [x] T5.1 `StoragePort` + adaptador `LocalStorage`
- [x] T5.2 `AssetService` + rota `POST /assets` (validação tipo/tamanho)
- [x] T5.3 Testes de upload/validação

## Fase 6 — Frontend: Auth e Navegação

- [x] T6.1 [P] Client HTTP tipado + armazenamento do token
- [x] T6.2 [P] Telas de login/cadastro + `AuthContext`
- [x] T6.3 [P] Lista de cadernos + criar/renomear/excluir
- [x] T6.4 Navegação de páginas (lista + seleção)

## Fase 7 — Frontend: Editor

- [x] T7.1 Integrar TipTap (StarterKit + Color + Highlight + Link + Image + nó PDF)
- [x] T7.2 Toolbar (bold, italic, underline, cor de caneta, marcação, listas, títulos)
- [x] T7.3 `useAutosave` (debounce + flush em `beforeunload` + retry + indicador de status)
- [x] T7.4 Upload de imagem e PDF integrado ao editor (colar/inserir)
- [x] T7.5 Linhas de caderno via CSS (cor/espaçamento/margem) + seleção de modo (fixo vs contínuo)

## Fase 8 — Testes E2E e Polimento

- [x] T8.1 Testes de componentes e hooks (Vitest + Testing Library)
- [x] T8.2 Smoke test manual do fluxo completo (cadastro → caderno → editar → recarregar)
- [x] T8.3 README com instruções de setup/execução

## Fase 9 — Modo Dark (tema escuro)

- [x] T9.1 `ThemeContext` (estado light/dark, persistência em `localStorage`, `data-theme` no `<html>`)
- [x] T9.2 CSS do tema dark (variáveis sobrescritas + papel preto com linhas brancas e texto claro)
- [x] T9.3 Toggle de tema no topbar (lista de cadernos e editor)
- [x] T9.4 Seletor de cor da linha no editor (`PATCH line_color`) + tratamento do default como "auto"
- [x] T9.5 Teste do tema (claro ↔ escuro; smoke test visual pendente)

## Fase 10 — Design System e Fix de Autosave

- [x] T10.1 Design system "caderno" (paleta folha de papel + fontes Kalam/Nunito) em claro/escuro
- [x] T10.2 Fix autosave em caderno vazio (cria a 1ª página automaticamente)
- [x] T10.3 Guard no `useAutosave` para `pageId <= 0` (mantém pendente, não salva)
- [x] T10.4 Teste do guard `pageId <= 0` no `useAutosave`

## Fase 11 — Infra e QA (CI + E2E)

- [x] T11.1 CI (GitHub Actions: `pytest` backend + `vitest`/`typecheck` frontend)
- [x] T11.2 E2E (Playwright: fluxo cadastro → caderno → editar → recarregar)
- [x] T11.3 Fix: evitar página duplicada no reload (auto-create aguarda carregar as páginas)

## Grupos paralelos seguros

- Fase 1: T1.1 ∥ T1.2 ∥ T1.3
- Fase 6: T6.1 ∥ T6.2 ∥ T6.3
- Backend (Fases 2–5) pode evoluir em paralelo com Frontend (Fases 6–7) após a Fase 1.
