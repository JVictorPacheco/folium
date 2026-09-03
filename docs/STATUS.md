# Status do Projeto

> Ponto de retomada. Atualizado em: 2026-09-03.

## Onde paramos

MVP do **Folium** (caderno digital na nuvem) implementado e **testado de ponta
a ponta** (smoke test manual + E2E aprovados). Backend e frontend completos,
com modo dark e design system "caderno". Testes automatizados (unit, integração
e E2E) e CI (GitHub Actions) configurados.

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
  - Tipografia expandida no editor: tamanho de fonte e família de fonte como
    marcas inline (`FontSize`/`FontFamily`), aplicáveis a qualquer trecho
    selecionado — independente dos títulos H1-H3, que continuam afetando o
    parágrafo inteiro (Fase 14).
  - Imagem e PDF redimensionáveis (alça de canto — imagem trava proporção,
    PDF não) e movíveis livremente pela página (alça dedicada, sai do fluxo
    do texto); link clicável (abre em nova aba) com estilo padronizado
    (Fase 15).
  - Remover imagem/PDF (botão `✕` sobre o item).
  - Linhas de caderno via CSS + modo de página fixo vs. contínuo + cor da linha.
  - Autosave com debounce + flush no `beforeunload` + indicador de status +
    revision por página (evita conflito `409`).
  - **Modo dark**: `ThemeContext` + toggle, papel preto com linhas e texto claro.
  - **Design system "caderno"**: paleta folha de papel + fontes Kalam/Nunito.
- **Infra**: `DATABASE_URL` configurável via `.env` da raiz (`docker-compose.yml`)
  — sem `.env`, usa o Postgres local do compose; com `.env`, aponta pra um
  Postgres gerenciado (testado com Supabase via Session Pooler).

### Verificado (automatizado + manual)

- ✅ Backend: **21 testes passando** (`pytest`).
- ✅ Frontend: **18 testes passando** (`vitest`), `tsc --noEmit` limpo, build OK.
- ✅ **E2E (Playwright)**: fluxo cadastro → caderno → editar → recarregar passando.
- ✅ **CI (GitHub Actions)**: `pytest` + `vitest`/`typecheck` rodam a cada PR/push.
- ✅ `docker compose up --build` completo (db + backend + frontend).
- ✅ Smoke test manual: cadastro → caderno → editar → recarregar.
- ✅ Upload real de imagem/PDF pela UI + remover + alternância de tema claro/escuro.
- ✅ Backend com Supabase (Postgres gerenciado, Session Pooler): migrações,
  registro/login e persistência testados de ponta a ponta.
- ✅ Tipografia expandida (Fase 14): confirmada pelo usuário no navegador —
  selecionar trecho no meio de uma frase e aplicar tamanho/fonte afeta só o
  trecho selecionado.
- ✅ Mídia embutida (Fase 15): redimensionar/mover imagem e PDF confirmados
  pelo usuário no navegador. Link testado via automação de navegador
  (Playwright) contra o app rodando: com e sem texto selecionado, `href`/
  `target="_blank"`/`rel` corretos, clique abre aba nova de verdade, texto
  digitado depois não herda a marca, e persiste após reload.
- ✅ E2E (Playwright) reinstalado e rodando nesta máquina (Chromium do
  Playwright não estava presente; instalado via `npx playwright install`).

### Próximo passo

- Merge da branch `feature/tipografia-expandida` (PR #14, agora com Fase 14
  e Fase 15) em `develop`.
- **Refinamento tela a tela**: revisar cada tela e propor melhorias de UX/visual.
- (opcional) Proteção de branch no GitHub (bloquear merge com CI falhando).

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
- **2026-08-27** — CI (GitHub Actions: `pytest` + `vitest`/`typecheck`) configurado e ativo (PR #5).
- **2026-08-27** — E2E (Playwright) do fluxo principal + fix de página duplicada no reload (PR #6).
- **2026-08-27** — Refinamento de auth (login/registro) + recuperação de senha: endpoints
  `forgot-password`/`reset-password`, token com validade, `EmailSender` (SMTP) e Mailpit no dev (PR #8).
- **2026-09-02** — Início do "Refinamento tela a tela" (branch `feature/refinamento-editor`,
  a partir de `develop`, que estava 30 commits à frente de `main` — release para `main` ainda
  pendente). Editor: folha com largura limitada, sombra/moldura e margem vermelha (T13.1);
  toolbar com aparência de botão (T13.2). Corrigido hot-reload do Vite no Docker (bind mount
  do Windows não disparava HMR sem `usePolling`). SMTP real configurado com Gmail (senha de
  app) — reset de senha testado de ponta a ponta com entrega em caixa real (T12.7); Mailpit
  segue como padrão do dev, Gmail via `.env`. T13.3 (links de auth com a paleta do design
  system) e T13.4 (lista de cadernos revisada — já estava centralizada, sem bug real)
  concluídos. **Fase 13 completa.**
- **2026-09-03** — PR #13 mergeada em `develop`: `DATABASE_URL` configurável via
  `.env` da raiz no `docker-compose.yml` (`${DATABASE_URL:-...}`), sem mudar o
  comportamento padrão. Testado com Supabase (Postgres gerenciado, Session
  Pooler) — migrações, registro/login e persistência OK.
- **2026-09-03** — Início da Fase 14 (tipografia expandida no editor, branch
  `feature/tipografia-expandida`): extensão `FontSize` (mark inline sobre
  `textStyle`, própria) e `FontFamily` (`@tiptap/extension-font-family`) com
  fontes curadas (Kalam, Caveat, Patrick Hand, Nunito); seletores na toolbar.
  Resolve a limitação de H1-H3 (nó de bloco) não servir pra aumentar só um
  trecho selecionado — tamanho/fonte agora são marcas inline, como bold/cor.
  FR-20/FR-21 e Fase 14 registrados em `spec.md`/`tasks.md`. Verificado:
  `tsc --noEmit` limpo, 18 testes frontend passando, build OK; T14.4
  confirmado pelo usuário no navegador. **Fase 14 completa.** PR #14 aberta,
  CI verde, aguardando merge em `develop`.
- **2026-09-03** — Fase 15 (mídia embutida) implementada e testada, mesma
  branch `feature/tipografia-expandida`: componente `ResizableEmbed`
  compartilhado (alça de mover + alça de redimensionar; atualiza o DOM
  direto durante o arrasto, só grava atributos no `mouseup`) integrado em
  `ImageEmbed` (proporção travada) e `PdfEmbed` (livre); atributos
  `width`/`height`/`x`/`y` persistem via `content_json`, sem mudança de
  backend. Link: `openOnClick: true` + `target="_blank"`. Dois bugs achados
  e corrigidos numa varredura: (1) iframe do PDF capturava eventos de mouse
  e engasgava o arrasto — corrigido com um "escudo" transparente por cima
  durante o drag; (2) listeners de `window` vazavam se o node view
  desmontasse no meio de um arrasto — corrigido com limpeza no unmount.
  Também corrigidos, a pedido do usuário: link não aparecia quando inserido
  sem texto selecionado (marca em cima de seleção vazia) — agora insere a
  própria URL como texto; e a marca de link "grudava" em texto digitado
  logo depois (mark inclusiva por causa do `autolink`) — corrigido com um
  espaço neutro após o link. FR-22 a FR-25 e Fase 15 registrados em
  `spec.md`/`plan.md`/`tasks.md`. Verificado: `tsc --noEmit` limpo, 18
  testes frontend + 21 backend passando, build OK, E2E (Playwright) verde
  (browser reinstalado nesta máquina). Redimensionar/mover confirmados pelo
  usuário no navegador; link testado via automação de navegador (Playwright)
  contra o app rodando — abre aba nova de verdade, `href`/`target`/`rel`
  corretos, sobrevive a reload. **Fase 15 completa.**
