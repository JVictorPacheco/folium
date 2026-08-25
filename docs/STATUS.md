# Status do Projeto

> Ponto de retomada. Atualizado em: 2026-08-24.

## Onde paramos

MVP do **Folium** (caderno digital na nuvem) implementado e **parcialmente
verificado**. O sistema ainda **não foi testado de ponta a ponta** (smoke test
manual adiado).

### O que está pronto

- **Metodologia SDD**: `memory/constitution.md` + `specs/001-caderno/{spec,plan,tasks}.md`.
- **Backend (FastAPI)** — completo:
  - Auth (cadastro/login, JWT + bcrypt), isolamento por `user_id`.
  - CRUD de cadernos e páginas.
  - Autosave com versionamento otimista (`revision`) → `PUT /pages/{id}/content`.
  - Upload de imagem/PDF (`POST /assets`) com validação e storage (port + adaptador local).
  - Alembic (migração inicial) + Dockerfile.
- **Frontend (React + TS + Vite)** — completo:
  - Login/cadastro, lista de cadernos (criar/renomear/excluir).
  - Editor TipTap: negrito/itálico/sublinhado, cor de caneta, marcação, listas,
    títulos (H1-H3), link, imagem, PDF embutido (node custom).
  - Linhas de caderno via CSS + modo de página fixo vs. contínuo.
  - Autosave com debounce + flush no `beforeunload` + indicador de status.

### Verificado (automatizado)

- ✅ Backend: imagem Docker compilada e **10 testes passando** (`pytest`).
- ✅ Frontend: `tsc --noEmit` limpo, build Vite OK, **1 teste passando** (`vitest`).

### NÃO verificado (pendente)

- ❌ **Smoke test manual de ponta a ponta** (cadastro → caderno → editar → recarregar).
- ❌ `docker compose up --build` completo (backend + postgres + frontend juntos).
- ❌ Upload real de imagem/PDF pela UI (testado só por unit/API no backend).

### O que falta (próximo passo)

1. Rodar `docker compose up --build` e validar o fluxo completo no navegador.
2. Aumentar cobertura de testes do frontend (componentes: Toolbar, EditorPage, autosave).
3. Testes E2E (ex.: Playwright) para o fluxo principal.
4. Configurar CI (ex.: GitHub Actions) rodando `pytest` + `vitest`.

### Fora do MVP (backlog futuro)

- Colaboração em tempo real (Yjs/Hocuspocus).
- Exportar para PDF, histórico de versões, busca, tags, app mobile.
- Modo dark (tema escuro).

## Como continuar (GitFlow)

Branches principais: `main` (produção) e `develop` (integração).

```bash
git checkout develop
git pull
git checkout -b feature/<nome>   # trabalho novo sai de develop
# ... implementa, testa ...
git add . && git commit -m "feat: ..."
git push -u origin feature/<nome>
# abrir PR de feature/<nome> -> develop
```

Regras rápidas:
- `main` só recebe merge de `develop` (releases) via PR.
- Funcionalidades novas = branch `feature/*` a partir de `develop`.
- Correções = branch `fix/*`; releases = `release/*`; hotfix = `hotfix/*`.
- Nunca commitar direto em `main` ou `develop`.
- Rodar `pytest` (backend) e `npm test`/`npm run typecheck` (frontend) antes de abrir PR.
