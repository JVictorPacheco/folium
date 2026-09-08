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

## Fase 12 — Refinamento de Auth (login/registro + reset de senha)

- [x] T12.1 Login/registro: mensagem de erro amigável (`detail`), mostrar/ocultar senha, autocomplete, autofocus, tema e alerta
- [x] T12.2 Recuperação de senha: modelo/repo/service + endpoints `forgot-password`/`reset-password` (token com validade)
- [x] T12.3 Notificação: `EmailSender` port + adaptador de log (console) + migração Alembic
- [x] T12.4 Frontend: telas "esqueci senha" e "nova senha" + link no login + rotas
- [x] T12.5 Testes de reset de senha (backend)
- [x] T12.6 Envio por SMTP (`SmtpEmailSender`) + Mailpit no dev (caixa de entrada local)
- [x] T12.7 SMTP real configurado (Gmail com senha de app) — reset de senha
      testado de ponta a ponta com entrega em caixa real. Credenciais em `.env`
      (raiz e `backend/.env`, fora do git). Limite ~500 envios/dia.

## Fase 13 — Refinamento tela a tela (UX/visual)

> Revisão visual pós-MVP, tela a tela. Critério de pronto: revisado no navegador
> (claro + escuro), sem regressão em `vitest`/`tsc`/E2E.

- [x] T13.1 Editor: limitar largura da "folha" (como papel real), com sombra/moldura
      separando do fundo, ao invés de ocupar 100% da tela. Inclui margem vermelha
      lateral (clássica de caderno).
- [x] T13.2 Editor: toolbar com aparência de botão no estado padrão (não só no
      hover/ativo) e seletor de cor da caneta com moldura.
- [x] T13.3 Telas de auth: estilizar links (`Cadastre-se`, `Esqueci minha senha?`,
      `Entrar`) com a paleta do design system em vez da cor azul padrão do navegador.
- [x] T13.4 Lista de cadernos: revisado — já está centralizada (`max-width: 640px`
      + `margin: auto`); o espaço vazio visto antes era só efeito de ter poucos
      cadernos, não um bug de layout. Nenhuma mudança necessária.

## Fase 14 — Tipografia expandida no editor

- [x] T14.1 Extensão `FontSize` (mark inline sobre `TextStyle`, atributo
      `fontSize`) — aplica a qualquer seleção, sem virar bloco de título.
- [x] T14.2 Extensão `FontFamily` (`@tiptap/extension-font-family`) com fontes
      curadas: Kalam (padrão), Caveat, Patrick Hand, Nunito.
- [x] T14.3 Toolbar: seletor de tamanho ("Pequeno/Normal/Grande/Enorme") e
      seletor de fonte, com o mesmo estilo visual dos demais controles.
- [x] T14.4 Verificação manual: selecionar trecho no meio de uma frase e
      aplicar tamanho/fonte afeta só o trecho, resto do parágrafo intacto.
      Confirmado pelo usuário no navegador em 2026-09-03. **Fase 14 completa.**

## Fase 15 — Mídia embutida: redimensionar, mover e link clicável

> Decisões de UX (2026-09-03): redimensionar imagem trava proporção (PDF não);
> voltar do modo flutuante pro fluxo do texto é via Ctrl+Z nesta versão, sem
> botão dedicado.

- [x] T15.1 Atributos `width`/`height`/`x`/`y` (px, nullable) nos nós `Image`
      (via `.extend()`) e `PdfEmbed`.
- [x] T15.2 Componente compartilhado `ResizableEmbed`: alça de mover (arrasta
      posição) + alça de redimensionar (arrasta tamanho); atualiza o DOM
      direto durante o arrasto e só grava os atributos do nó (via
      `updateAttributes`) no `mouseup`, pra não disparar autosave a cada pixel.
      Inclui "escudo" transparente sobre o conteúdo durante o arrasto (o
      `<iframe>` do PDF captura eventos de mouse e engasgava o rastreamento)
      e limpeza dos listeners de `window` se o node view desmontar no meio
      de um arrasto.
- [x] T15.3 Integrar `ResizableEmbed` no `ImageView` (`lockAspect: true`) e no
      `PdfEmbedView` (`lockAspect: false`).
- [x] T15.4 CSS das alças (mover/redimensionar, visíveis no hover) + wrapper
      `position: absolute` relativo a `.paper-lines` (já `position: relative`)
      quando o nó estiver "flutuante" (`x`/`y` definidos).
- [x] T15.5 Link: `openOnClick: true` no `@tiptap/extension-link`
      (`target="_blank"`, `rel="noopener noreferrer"`) + estilo padronizado
      (sublinhado, cor de acento, cursor pointer) em `.ProseMirror a`. Corrigido
      também: inserir link sem texto selecionado não aparecia (marca em cima de
      seleção vazia); e a marca "grudava" em texto digitado logo depois do link
      (mark inclusiva por causa do `autolink`) — resolvido inserindo um espaço
      neutro após o link.
- [x] T15.6 Verificação manual: redimensionar imagem mantém proporção;
      redimensionar PDF permite largura/altura independentes; mover
      imagem/PDF pela página; posição/tamanho sobrevivem a um recarregamento;
      clicar em link abre em nova aba. Confirmado pelo usuário no navegador e
      re-testado via automação (Playwright): link com/sem seleção, `href`/
      `target`/`rel` corretos, abre aba nova de fato, texto após o link não
      herda a marca, e persiste após reload. **Fase 15 completa.**

## Fase 16 — Exportar caderno como PDF

> Decisão de arquitetura (2026-09-04): impressão nativa do navegador
> (`window.print()`), não geração no backend — zero dependência nova pesada,
> mesma aparência (mesmo CSS das linhas), só frontend. Escopo: caderno
> inteiro (todas as páginas), não só a página atual.
>
> Decisão de implementação (2026-09-04, durante T16.2): a ideia inicial era
> usar o pacote `@tiptap/html` (`generateHTML`). Testado e **descartado**:
> ele serializa num DOM headless (`zeed-dom`), que não sincroniza
> `element.style.cssText` de volta pro atributo `style` — toda formatação
> baseada em `style` (cor, fonte, tamanho, largura de imagem) saía sem
> efeito no HTML exportado, confirmado com um teste isolado antes de mudar
> de abordagem. Como o app roda só no navegador, a correção foi usar o
> `DOMSerializer` do ProseMirror (`@tiptap/pm/model`, já dependência
> transitiva) direto com o `document` real — sem precisar de dependência
> nova nenhuma.

- [x] T16.1 `renderHTML` explícito de `width`/`height` em `ImageEmbed` e
      `PdfEmbed` (aplica o tamanho redimensionado como `style` no HTML
      estático). `x`/`y` (posição flutuante) não entra no `renderHTML` —
      export sempre segue o fluxo normal do documento. `PdfEmbed` também
      ganhou um placeholder visual ("📄 nome do arquivo", classe
      `pdf-embed-static`) pro `renderHTML` — antes era uma `<div>` vazia sem
      conteúdo, invisível fora do NodeView React (só usado no editor).
- [x] T16.2 Util `pageHtml(page)`: gera o HTML de cada página via
      `DOMSerializer` (`@tiptap/pm/model`) + `getSchema(editorExtensions)`,
      passando o `document` real do navegador. **Não** usar `@tiptap/html`
      (testado e descartado — ver decisão acima).
- [x] T16.3 View de impressão: monta `.paper`/`.paper-lines` por página
      (linhas, cor, fontes) com o HTML gerado, uma por página do caderno.
- [x] T16.4 CSS de impressão (`@media print`): esconde topbar/sidebar/
      toolbar, `print-color-adjust: exact` nas linhas do papel, quebra de
      página (`page-break-after`) entre páginas do caderno.
- [x] T16.5 Botão "Exportar PDF" no topbar do editor: `flush()` do autosave
      → busca páginas frescas do servidor (não do cache do React Query, pra
      não exportar conteúdo desatualizado de páginas editadas antes na
      mesma sessão — e pra não notificar o `useQuery` de `pages` no meio da
      mesma renderização) → monta view de impressão → `window.print()` →
      desmonta em `afterprint`.
- [x] T16.6 Verificação automatizada (Playwright, contra o app rodando):
      caderno com 2 páginas, título H1, imagem redimensionada, link, texto
      com fonte/tamanho customizados. Confirmado: `#print-root` com 2
      `.print-sheet` (uma por página); `<img style="width: ...">` e
      `<span style="font-family: ...; font-size: ...">` corretos no HTML
      exportado (só funcionaram depois da correção do T16.2); UI do app
      (`#root`) com `display: none` e `checkVisibility() === false` em modo
      impressão; `#print-root` visível; `page-break-after` correto (`page`
      em todas menos a última); `print-color-adjust: exact` aplicado;
      screenshot confirmou papel/linhas/margem vermelha visíveis. Placeholder
      do PDF embutido testado depois com um arquivo real, mostrando o nome
      correto ("📄 relatorio.pdf") na exportação. Confirmado pelo usuário no
      navegador. **Fase 16 completa.**

## Fase 17 — Histórico de versões

> Decisão de arquitetura (2026-09-08): snapshot "troteado" no próprio
> caminho do autosave (só guarda uma versão se a última tiver mais de
> 5min), em vez de uma versão por save — evita explosão de linhas sem
> precisar de job/cron. Restaurar sempre tira um snapshot do estado atual
> antes de sobrescrever, então nunca é destrutivo.

- [x] T17.1 Modelo `PageVersion` + migração `0003` (tabela `page_versions`,
      FK `page_id` com `ON DELETE CASCADE`, índice em `page_id`).
- [x] T17.2 `PageVersionRepository`: `list_by_page_for_user`,
      `get_for_user` (isolamento via `JOIN` até `notebooks.user_id`),
      `has_recent` (throttle), `create`, `prune` (retenção de 50).
- [x] T17.3 `ContentService`: snapshot do conteúdo anterior antes de cada
      `update`, se a última versão tiver mais de 5min (ou não existir);
      `list_versions`, `get_version`, `restore` (snapshota o estado atual
      antes de sobrescrever).
- [x] T17.4 Rotas: `GET /pages/{id}/versions`, `GET
      /pages/{id}/versions/{version_id}`, `POST
      /pages/{id}/versions/{version_id}/restore`.
- [x] T17.5 Testes backend: throttle (não cria versão em edição imediata
      seguinte, cria após a janela passar), restore reverte conteúdo e
      snapshota o estado pré-restore, isolamento entre usuários (404),
      versão não encontrada quando `page_id` não bate.
- [x] T17.6 Frontend: `contentToHtml` extraído de `exportPdf.ts`
      (reutilizável fora da exportação) + `VersionHistoryModal` (lista de
      versões, prévia sob demanda, botão restaurar) + botão "Histórico" no
      topbar do editor + `handleRestored` atualiza o editor ao vivo sem
      precisar recarregar a página.
- [x] T17.7 Verificação: 26 testes backend + 21 frontend passando, `tsc`
      limpo, build OK, E2E (Playwright) verde. Migração `0003` testada
      contra Postgres real (`docker compose up`). Fluxo completo testado
      via automação de navegador (Playwright) contra o app rodando:
      digitar → autosave cria 1ª versão (snapshot do conteúdo anterior) →
      abrir Histórico → pré-visualizar → restaurar → editor volta ao
      conteúdo restaurado → conteúdo persiste após recarregar a página.
      **Fase 17 completa.**

## Fase 18 — Busca e tags

> Decisão de arquitetura (2026-09-08): busca é uma varredura em Python
> sobre as páginas do usuário (não SQL full-text) — volume esperado é
> baixo (poucas dezenas de páginas por usuário), evita depender de
> recurso específico de dialeto (Postgres vs. SQLite dos testes). Tags
> são um conjunto por caderno, substituído inteiro a cada `PATCH`, nomes
> normalizados em minúsculas pra evitar duplicata por caixa.

- [x] T18.1 Modelo `Tag` + tabela de associação `notebook_tags` (M2M) +
      migração `0004` (`UNIQUE(user_id, name)` em `tags`).
- [x] T18.2 `TagRepository` (`list_by_user`, `get_or_create_many` com
      normalização/dedupe) + `NotebookRepository` com `selectinload` de
      tags e filtro opcional por tag em `list_by_user`.
- [x] T18.3 `NotebookService.update` resolve `tags: list[str]` pra `Tag`
      antes de persistir; `NotebookOut` serializa `tags` como lista de
      nomes (ordenada). Rota `GET /tags` (lista as tags do usuário) e
      `GET /notebooks?tag=` (filtro).
- [x] T18.4 `PageRepository.list_for_user` (todas as páginas do usuário,
      isolado via join, com `Notebook` eager-carregado via
      `contains_eager`, filtro opcional por tag) + `SearchService`
      (`page_plain_text` extrai texto do JSON do editor, `_snippet`
      recorta contexto ao redor do termo) + rota `GET /search?q=&tag=`.
- [x] T18.5 Testes backend: normalização/dedupe de tags, filtro de
      cadernos por tag, isolamento de tags entre usuários; busca por
      conteúdo/título/nome do caderno, snippet, filtro por tag,
      isolamento entre usuários.
- [x] T18.6 Frontend: `NotebookListPage` — campo de busca (debounce
      300ms) que troca a lista por resultados (caderno · página +
      trecho) e navega direto pra página encontrada; filtro por tag
      (`<select>`); editar tags de um caderno via `window.prompt`
      (mesmo padrão do renomear); chips de tag na listagem.
      `EditorPage` lê `?page=` da URL pra abrir direto na página do
      resultado de busca.
- [x] T18.7 Verificação: 34 testes backend (8 novos) + 24 frontend (3
      novos) passando, `tsc` limpo, build OK, E2E verde. Migração `0004`
      testada contra Postgres real (`docker compose up`). Fluxo completo
      testado via automação de navegador contra o app rodando: criar tag
      num caderno → chip aparece → filtrar lista pela tag → digitar
      termo no campo de busca → resultado com trecho de contexto → clicar
      abre o editor direto na página certa. **Fase 18 completa.**

## Fase 19 — Compartilhamento de cadernos

> Decisões de arquitetura (2026-09-08): compartilhar exige e-mail de conta
> já cadastrada (sem link público/acesso anônimo); dois níveis apenas
> (`viewer`/`editor`) — cobre "mostrar" vs. "trabalhar junto", sem
> granularidade extra. Edição simultânea/tempo real segue fora de escopo
> (ver Não-metas). Toda checagem de acesso passou a viver num único lugar
> (`NotebookAccessService`), substituindo os `WHERE user_id = :dono`
> espalhados pelos repositórios.

- [x] T19.1 Modelo `NotebookShare` + migração `0005` (tabela
      `notebook_shares`, `UNIQUE(notebook_id, shared_with_user_id)`).
- [x] T19.2 `NotebookShareRepository` (`list_by_notebook`,
      `list_shared_with_user`, `get`, `get_for_notebook_and_user`,
      `upsert`, `delete`) + `NotebookRepository.get_by_id` (sem filtro de
      dono, usado pela resolução de acesso).
- [x] T19.3 `NotebookAccessService` (`app/services/access.py`):
      `AccessLevel` (`OWNER`/`EDITOR`/`VIEWER`), `resolve`/`require` — o
      ponto único de "esse usuário pode fazer X neste caderno".
- [x] T19.4 Refatoração de `NotebookService`, `PageService` e
      `ContentService` pra checar acesso via `NotebookAccessService` em
      vez de filtrar `user_id` direto no repositório; `PageRepository`/
      `PageVersionRepository` simplificados (sem `JOIN` de isolamento
      próprio, o serviço já garante o acesso antes de chamar).
      `NotebookService.list` passou a unir cadernos próprios + 
      compartilhados, cada um com `role` anotado.
- [x] T19.5 `ShareService` + rotas `GET`/`POST`/`DELETE
      /notebooks/{id}/shares` (owner-only): convite por e-mail (404 se a
      conta não existir), upsert em vez de duplicar, recusa
      auto-compartilhamento (400).
- [x] T19.6 `PageRepository.list_for_user` (busca) estendido com `LEFT
      JOIN` em `notebook_shares` — busca cobre cadernos compartilhados.
- [x] T19.7 Testes backend (`test_shares.py`, 9 casos): viewer não edita/
      cria página/restaura/gerencia caderno (404 em cada); editor edita e
      restaura mas não mexe no caderno; convite exige conta existente
      (404) e recusa auto-share (400); convite duplicado atualiza nível
      em vez de duplicar; revogação remove acesso; estranho sem relação
      não acessa nada; busca inclui caderno compartilhado.
- [x] T19.8 Frontend: `Notebook.role` no tipo; `NotebookListPage` mostra
      selo "compartilhado · pode editar/só ver" e esconde botões de dono
      pra quem não é dono; `ShareModal` (listar/convidar/revogar).
      `EditorPage`: `role !== "owner"` esconde toolbar/"+Página"/excluir
      página/cor da linha; `role === "viewer"` também esconde
      "Restaurar" no histórico e torna o editor não-editável.
- [x] T19.9 Bug encontrado e corrigido durante verificação ao vivo:
      `editor.setEditable(canEdit)` (sem o 2º argumento) dispara um
      evento `update` do TipTap na própria troca de permissão, agendando
      um autosave que dava 404 pra quem só tem acesso de leitura — UI
      mostrava "Erro ao salvar" mesmo sem o usuário ter digitado nada.
      Corrigido com `editor.setEditable(canEdit, false)` (suprime o
      evento nessa troca).
- [x] T19.10 Verificação: 43 testes backend (9 novos) + 27 frontend (4
      novos) passando, `tsc` limpo, build OK. Migração `0005` testada
      contra Postgres real. Fluxo completo (dona compartilha como editor
      → colega edita e salva → dona rebaixa pra viewer → colega vê
      conteúdo mas sem toolbar/restaurar/edição, status "Salvo" correto)
      testado via automação de navegador contra o app rodando, com dois
      usuários reais alternando sessão. E2E (`smoke.spec.ts`) confirmado
      funcionalmente correto (passou com timeout maior; o timeout padrão
      de 5s ficou justo pela lentidão do Docker Desktop nesta sessão
      depois de várias reconstruções de imagem — não uma regressão de
      código, confirmado via `curl` direto no endpoint). **Fase 19
      completa.**

## Fase 20 — Colar e arrastar imagem

> Pedido do usuário (2026-09-08): colar imagem com Ctrl+V ou arrastar do
> computador com o mouse, sem precisar do seletor de arquivo.

- [x] T20.1 `editorProps.handlePaste`/`handleDrop` no `useEditor` de
      `EditorPage`: filtra por `image/*`, reaproveita `uploadAsset` (mesmo
      usado pelo botão "Imagem" da toolbar), guardado por `canEditRef`
      (viewer não pode colar/soltar).
- [x] T20.2 Bug encontrado e corrigido durante verificação ao vivo:
      inserir uma segunda imagem em sequência substituía a primeira (nó
      de imagem é átomo → seleção vira `NodeSelection` nele →
      `insertContent` numa `NodeSelection` substitui em vez de inserir do
      lado). Corrigido inserindo imagem + parágrafo vazio juntos numa só
      chamada (`insertContent([...])`), cursor termina em posição de
      texto normal. Arquivos de um drop múltiplo processados um de cada
      vez (`for...of` + `await`), não em paralelo.
- [x] T20.3 Verificação: `tsc` limpo, 27 testes frontend passando (sem
      teste dedicado de unidade pro paste/drop — TipTap/ProseMirror sobre
      jsdom não reproduz `ClipboardEvent`/`DragEvent` de forma confiável;
      verificado ao vivo via automação de navegador contra o app rodando,
      simulando paste/drop com `ClipboardEvent`/`DragEvent` sintéticos e
      arquivos reais: colar uma imagem insere e persiste após reload;
      soltar dois arquivos de uma vez insere os dois lado a lado (não um
      substituindo o outro) — confirmado antes e depois da correção do
      T20.2. **Fase 20 completa.**

## Grupos paralelos seguros

- Fase 1: T1.1 ∥ T1.2 ∥ T1.3
- Fase 6: T6.1 ∥ T6.2 ∥ T6.3
- Backend (Fases 2–5) pode evoluir em paralelo com Frontend (Fases 6–7) após a Fase 1.
