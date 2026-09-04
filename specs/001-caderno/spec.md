# Spec 001 — Caderno Folium (MVP)

> Especificação da feature inicial do Folium.
> Foco no **o quê** e no **porquê** — detalhes técnicos ficam no `plan.md`.

## Resumo

Um caderno digital na nuvem onde o usuário, após autenticar, cria cadernos
com páginas que simulam um caderno real (linhas de fundo), edita texto com
formatação rica e insere imagens, links e PDFs, com sincronização automática
individual na nuvem.

## Metas

- Permitir criar, listar, renomear e excluir cadernos.
- Permitir criar, navegar e excluir páginas dentro de um caderno.
- Oferecer editor de texto rico com: negrito, itálico, sublinhado, cor do
  texto ("caneta"), marcação ("marcador"), listas e títulos.
- Renderizar linhas de caderno no fundo das páginas.
- Permitir inserir imagens, links e PDFs (embutidos/colados).
- Autenticação com e-mail e senha (JWT).
- Autosave do conteúdo na nuvem com feedback de sincronização.

## Não-metas (fora do MVP)

- Colaboração em tempo real (Yjs/Hocuspocus) — evolução futura.
- Exportar para PDF, versões/histórico visual, busca, tags, app mobile.
- Compartilhamento entre usuários.

## Personas

- **Estudante/Anotador**: quer um caderno bonito e simples para anotações que
  ficam salvas na nuvem automaticamente.

## User Stories

1. Como usuário, quero me cadastrar e entrar com e-mail/senha para acessar meus cadernos.
2. Como usuário, quero criar, renomear e excluir cadernos para organizar meu conteúdo.
3. Como usuário, quero criar e excluir páginas dentro de um caderno.
4. Como usuário, quero escolher, por caderno, entre páginas fixas (como um caderno real) e rolagem contínua.
5. Como usuário, quero ver linhas de caderno no fundo das páginas.
6. Como usuário, quero formatar texto (negrito, itálico, sublinhado, cor de caneta, marcação, listas, títulos).
7. Como usuário, quero inserir imagens, links e PDFs na página.
8. Como usuário, quero que minhas edições sejam salvas automaticamente na nuvem, com indicador de status.
9. Como usuário, quero sair (logout) e ter minha sessão encerrada.
10. Como usuário, quero alternar entre tema claro e escuro, com o modo escuro
    parecendo um caderno preto real (fundo preto, linhas brancas, texto claro).
11. Como usuário, quero recuperar minha senha caso esqueça (receber um link de
    reset por e-mail e definir uma nova senha).
12. Como usuário, quero redimensionar imagens e PDFs inseridos na página,
    arrastando um cantinho.
13. Como usuário, quero mover imagens e PDFs livremente pela página, arrastando
    por uma alça, saindo do fluxo do texto se eu quiser.
14. Como usuário, quero que um link inserido seja de fato clicável (abre a URL),
    com um estilo padronizado em vez da formatação crua do navegador.
15. Como usuário, quero exportar meu caderno inteiro como PDF, mantendo a
    aparência das linhas e do papel, para ter uma cópia autêntica fora do app.

## Requisitos Funcionais

- **FR-01**: Cadastro de usuário com e-mail único e senha (mín. 8 caracteres).
- **FR-02**: Login que retorna token JWT (acesso).
- **FR-03**: CRUD de cadernos (nome obrigatório, `page_mode` = `fixed` | `continuous`, `line_style`).
- **FR-04**: CRUD de páginas associadas a um caderno, com ordenação.
- **FR-05**: Conteúdo da página persistido como JSON estruturado (ProseMirror).
- **FR-06**: Autosave com debounce (ex.: 1s) via `PUT /pages/{id}/content`.
- **FR-07**: Formatação rica: bold, italic, underline, textColor, highlight, listas (bullet/ordered), títulos (H1-H3).
- **FR-08**: Inserir imagem por upload (PNG/JPG/WebP/GIF, máx. 10MB), com URL retornada.
- **FR-09**: Inserir link externo.
- **FR-10**: Inserir/embutir PDF por upload (máx. 25MB), renderizado como visualizador embutido.
- **FR-11**: Linhas de caderno renderizadas via CSS (cor, espaçamento e margem configuráveis).
- **FR-12**: Isolamento total: toda query filtra por `user_id` do token.
- **FR-13**: Logout no cliente (descarte do token).
- **FR-14**: Alternância de tema claro/escuro (modo dark: fundo preto, linhas do
  caderno brancas e texto claro por padrão), mantendo a possibilidade de o
  usuário escolher a cor da caneta e a cor da linha.
- **FR-15**: Identidade visual de caderno (design system): paleta "folha de
  papel" (terracota/oliva/creme), fontes manuscritas (Kalam) para títulos e
  corpo (Nunito), aplicada de forma consistente aos temas claro e escuro.
- **FR-16**: Recuperação de senha: solicitar link de reset por e-mail
  (`POST /auth/forgot-password`), token com validade (1h) e definição de nova
  senha (`POST /auth/reset-password`). Resposta genérica no "esqueci minha
  senha" (não revela se o e-mail existe). Entrega via SMTP (`EmailSender` port):
  Mailpit no dev, provedor transacional (Resend/SendGrid/SES) em produção via env.
- **FR-17**: A folha do editor deve ter largura limitada (como papel real), com
  moldura/sombra separando-a do fundo da aplicação, em vez de ocupar 100% da tela.
- **FR-18**: Controles da toolbar do editor devem ter aparência de botão mesmo
  fora do hover/estado ativo (affordance clara de que são clicáveis).
- **FR-19**: Links nas telas de autenticação devem seguir a paleta do design
  system, não a cor padrão do navegador.
- **FR-20**: Tamanho de fonte é uma marca inline (aplicável a qualquer trecho
  selecionado, como bold/cor), não um estilo de bloco — diferente de título
  (H1-H3), que sempre afeta o parágrafo inteiro.
- **FR-21**: Fonte do texto é uma marca inline selecionável entre um conjunto
  curado (Kalam, Caveat, Patrick Hand, Nunito), aplicável a qualquer trecho
  selecionado.
- **FR-22**: Imagem inserida pode ser redimensionada arrastando uma alça no
  cantinho, mantendo a proporção original (largura/altura travadas).
- **FR-23**: PDF inserido pode ser redimensionado arrastando uma alça no
  cantinho, com largura e altura ajustáveis de forma independente (sem travar
  proporção).
- **FR-24**: Imagem e PDF inseridos podem ser movidos livremente pela página
  (arrastar por uma alça dedicada de "mover"), saindo do fluxo normal do
  texto e podendo se sobrepor a ele. Posição e tamanho persistem via autosave
  (atributos do nó no `content_json`, sem mudança de schema no backend).
  Reverter para o fluxo original, se o usuário arrastar por engano, é feito
  via desfazer (Ctrl+Z) — sem um botão dedicado nesta versão.
- **FR-25**: Link inserido é clicável (abre a URL numa nova aba) e usa um
  estilo visual padronizado (sublinhado, cor de acento, cursor de ponteiro),
  em vez de depender da formatação padrão do navegador.
- **FR-26**: Exportar o caderno completo (todas as páginas, na ordem) como
  PDF via impressão nativa do navegador — botão "Exportar PDF" na tela do
  editor aciona `window.print()` numa view dedicada de impressão, sem
  depender de um serviço novo no backend.
- **FR-27**: A view de impressão preserva a identidade visual do caderno
  (linhas de fundo, cor de linha configurada, fontes, formatação rica,
  tamanho/família de fonte) — cada página do caderno vira uma página do PDF
  (quebra de página entre elas), e a interface do app (topbar, sidebar,
  toolbar) não aparece no resultado.
- **FR-28**: Imagem e PDF embutidos aparecem na exportação respeitando o
  tamanho definido (se redimensionados), sempre no fluxo normal do
  documento — a posição "flutuante" (FR-24) não é preservada na impressão
  nesta versão.

## Requisitos Não-Funcionais

- **NFR-01**: Autosave não pode perder dados em refresh/fechamento (save antes de `unload` + retry).
- **NFR-02**: Editor fluido (< 100ms de latência de digitação percebida).
- **NFR-03**: API com validação Pydantic e contratos documentados (OpenAPI).
- **NFR-04**: Testes unitários e de integração nos serviços e repositórios.
- **NFR-05**: Código em TypeScript (front) e Python 3.12 com tipos (back).
- **NFR-06**: Segredos via variáveis de ambiente; senhas com bcrypt.

## Modelo de Dados Conceitual

- **User** (id, email, password_hash, created_at)
- **Notebook** (id, user_id, name, page_mode, line_style, created_at, updated_at)
- **Page** (id, notebook_id, title, position, content_json, revision, created_at, updated_at)
- **Asset** (id, user_id, kind [image|pdf], filename, mime, size, storage_key, url, created_at)

## Critérios de Aceitação

- [x] Um usuário novo consegue cadastrar, logar e criar um caderno.
- [x] Usuário A não consegue acessar cadernos/páginas do usuário B (HTTP 403/404).
- [x] Digitar com formatação (bold, cor, marcação) reflete no JSON persistido e reabre igual.
- [x] Imagem e PDF enviados aparecem embutidos na página após recarregar.
- [x] Autosave persiste a última edição mesmo com refresh imediato após digitar.
- [x] Caderno alterna entre modo de páginas fixas e rolagem contínua.
- [x] Linhas de caderno visíveis e configuráveis (cor/espaçamento).
- [x] Usuário alterna entre tema claro e escuro; no escuro o fundo é preto, as
      linhas do caderno são brancas e o texto é claro por padrão.
- [x] A folha do editor tem largura limitada, com moldura/sombra, em vez de
      ocupar 100% da tela (claro e escuro).
- [x] Botões da toolbar do editor têm aparência de botão (borda/fundo sutil)
      mesmo sem hover.
- [x] Links das telas de autenticação usam a paleta do design system.
- [x] Arrastar o cantinho de uma imagem redimensiona mantendo a proporção; o
      mesmo gesto num PDF ajusta largura/altura de forma independente.
- [x] Arrastar a alça de mover tira a imagem/PDF do fluxo do texto e permite
      posicioná-la livremente na página; a posição/tamanho persistem após recarregar.
- [x] Clicar num link inserido no editor abre a URL numa nova aba, com
      sublinhado/cor de acento/cursor de ponteiro visíveis.
- [x] "Exportar PDF" abre o diálogo de impressão nativo com uma prévia de
      todas as páginas do caderno, uma por página, linhas de fundo visíveis.
- [x] PDF gerado preserva formatação rica (negrito, cor, tamanho/fonte) e
      imagem/PDF redimensionados; sem a interface do app (toolbar/sidebar).
