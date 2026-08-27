# Status do Projeto

> Ponto de retomada. Atualizado em: 2026-08-27.

## Onde paramos

MVP do **Folium** (caderno digital na nuvem) implementado e **testado de ponta
a ponta** (smoke test manual aprovado). Backend e frontend completos, com modo
dark e design system "caderno". Testes automatizados cobrindo serviços,
repositórios, hooks e componentes.

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
  - Remover imagem/PDF (botão `✕` sobre o item).
  - Linhas de caderno via CSS + modo de página fixo vs. contínuo + cor da linha.
  - Autosave com debounce + flush no `beforeunload` + indicador de status +
    revision por página (evita conflito `409`).
  - **Modo dark**: `ThemeContext` + toggle, papel preto com linhas e texto claro.
  - **Design system "caderno"**: paleta folha de papel + fontes Kalam/Nunito.

### Verificado (automatizado + manual)

- ✅ Backend: **17 testes passando** (`pytest`).
- ✅ Frontend: **16 testes passando** (`vitest`), `tsc --noEmit` limpo, build OK.
- ✅ `docker compose up --build` completo (db + backend + frontend).
- ✅ Smoke test manual: cadastro → caderno → editar → recarregar.
- ✅ Upload real de imagem/PDF pela UI + remover + alternância de tema claro/escuro.

### O que falta (próximo passo)

1. Testes E2E (ex.: Playwright) para o fluxo principal.
2. Configurar CI (ex.: GitHub Actions) rodando `pytest` + `vitest`.

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
  `T9.5` (tema). `greenlet` adicionado a `requirements.txt` (dependência do SQLAlchemy async).
- **2026-08-25** — Integração do PR #1 (`feature/tema-caderno`, do andfmp): design system
  "caderno" (paleta + fontes) e fix de autosave em caderno vazio.
- **2026-08-27** — Smoke test manual (T8.2) aprovado. Correções aplicadas: URL de assets,
  botão de remover imagem/PDF, autosave com revision por página (409) e cor da linha no tema.
