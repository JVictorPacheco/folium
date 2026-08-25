# Status do Projeto

> Ponto de retomada. Atualizado em: 2026-08-25.

## Onde paramos

MVP do **Folium** (caderno digital na nuvem) implementado, incluindo o **modo
dark**, e **parcialmente verificado**. O sistema ainda **não foi testado de
ponta a ponta** (smoke test manual adiado).

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
  - **Modo dark**: `ThemeContext` + toggle no topbar, papel preto com linhas
    brancas e texto claro, seletor de cor da linha (`PATCH line_color`).

### Verificado (automatizado)

- ✅ Backend: **17 testes passando** (`pytest`) — inclui upload/validação de assets.
- ✅ Frontend: **11 testes passando** (`vitest`), `tsc --noEmit` limpo, build Vite OK.

### NÃO verificado (pendente)

- ❌ **Smoke test manual de ponta a ponta** (cadastro → caderno → editar → recarregar).
- ❌ `docker compose up --build` completo (backend + postgres + frontend juntos).
- ❌ Upload real de imagem/PDF pela UI (testado só por unit/API no backend).
- ❌ Smoke test visual do tema (alternância claro ↔ escuro no navegador).

### O que falta (próximo passo)

1. **T8.2** — Smoke test manual do fluxo completo + rodar `docker compose up --build`
   e validar no navegador (inclui upload real pela UI e alternância visual de tema).
2. Testes E2E (ex.: Playwright) para o fluxo principal.
3. Configurar CI (ex.: GitHub Actions) rodando `pytest` + `vitest`.

### Fora do MVP (backlog futuro)

- Colaboração em tempo real (Yjs/Hocuspocus).
- Exportar para PDF, histórico de versões, busca, tags, app mobile.

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

## Registro de trabalho (para não perder o fio)

- **2026-08-24** — MVP inicial implementado (backend + frontend), 10 testes backend + 1 frontend.
- **2026-08-24** — Modo dark, caderno em tela cheia e alinhamento do texto às linhas (commit `79aba42`).
- **2026-08-25** — GitFlow corrigido (`develop` sincronizado com `main`) e STATUS.md atualizado.
- **2026-08-25** — Testes pendentes concluídos: `T5.3` (assets), `T8.1` (hooks/componentes) e
  `T9.5` (tema). 17 testes backend + 11 frontend. `greenlet` adicionado a `requirements.txt`
  (dependência do SQLAlchemy async).
