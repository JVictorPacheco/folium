# Tasks 001 — Caderno Folium (MVP)

> Lista de tarefas derivada de `plan.md`. Marcador `[P]` = paralelizável.
> Ordem respeita dependências. Executar em fases.

## Fase 1 — Fundação

- [ ] T1.1 [P] Scaffold backend FastAPI (estrutura de pastas, `pyproject.toml`, Uvicorn, healthcheck)
- [ ] T1.2 [P] Scaffold frontend Vite + React + TypeScript (com ESLint/Prettier)
- [ ] T1.3 [P] Docker + Docker Compose (Postgres + backend + frontend)
- [ ] T1.4 Configurar Alembic e primeira migração (tabelas `users`, `notebooks`, `pages`, `assets`)

## Fase 2 — Auth

- [ ] T2.1 Modelo `User` + `UserRepository` (get_by_email, create)
- [ ] T2.2 `AuthService` (hash bcrypt, geração/validação JWT)
- [ ] T2.3 Schemas e rotas `/auth/register` e `/auth/login`
- [ ] T2.4 Dependência `get_current_user` (decodifica JWT)
- [ ] T2.5 Testes de auth (unit + integração)

## Fase 3 — Cadernos e Páginas

- [ ] T3.1 Modelos `Notebook` e `Page` + repositórios
- [ ] T3.2 `NotebookService` (CRUD com isolamento por `user_id`)
- [ ] T3.3 `PageService` (criar/ordenar/excluir páginas)
- [ ] T3.4 Rotas REST de notebooks e páginas + schemas
- [ ] T3.5 Testes de notebooks/páginas (inclui teste de isolamento entre usuários)

## Fase 4 — Conteúdo e Autosave

- [ ] T4.1 `ContentService` + rota `PUT /pages/{id}/content` (revision, concorrência otimista)
- [ ] T4.2 Testes de versionamento/concorrência

## Fase 5 — Upload de Assets

- [ ] T5.1 `StoragePort` + adaptador `LocalStorage`
- [ ] T5.2 `AssetService` + rota `POST /assets` (validação tipo/tamanho)
- [ ] T5.3 Testes de upload/validação

## Fase 6 — Frontend: Auth e Navegação

- [ ] T6.1 [P] Client HTTP tipado + armazenamento do token
- [ ] T6.2 [P] Telas de login/cadastro + `AuthContext`
- [ ] T6.3 [P] Lista de cadernos + criar/renomear/excluir
- [ ] T6.4 Navegação de páginas (lista + seleção)

## Fase 7 — Frontend: Editor

- [ ] T7.1 Integrar TipTap (StarterKit + Color + Highlight + Link + Image + nó PDF)
- [ ] T7.2 Toolbar (bold, italic, underline, cor de caneta, marcação, listas, títulos)
- [ ] T7.3 `useAutosave` (debounce + flush em `beforeunload` + retry + indicador de status)
- [ ] T7.4 Upload de imagem e PDF integrado ao editor (colar/inserir)
- [ ] T7.5 Linhas de caderno via CSS (cor/espaçamento/margem) + seleção de modo (fixo vs contínuo)

## Fase 8 — Testes E2E e Polimento

- [ ] T8.1 Testes de componentes e hooks (Vitest + Testing Library)
- [ ] T8.2 Smoke test manual do fluxo completo (cadastro → caderno → editar → recarregar)
- [ ] T8.3 README com instruções de setup/execução

## Grupos paralelos seguros

- Fase 1: T1.1 ∥ T1.2 ∥ T1.3
- Fase 6: T6.1 ∥ T6.2 ∥ T6.3
- Backend (Fases 2–5) pode evoluir em paralelo com Frontend (Fases 6–7) após a Fase 1.
