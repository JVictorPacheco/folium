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

## Grupos paralelos seguros

- Fase 1: T1.1 ∥ T1.2 ∥ T1.3
- Fase 6: T6.1 ∥ T6.2 ∥ T6.3
- Backend (Fases 2–5) pode evoluir em paralelo com Frontend (Fases 6–7) após a Fase 1.
