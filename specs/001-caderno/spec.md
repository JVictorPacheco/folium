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

- [ ] Um usuário novo consegue cadastrar, logar e criar um caderno.
- [ ] Usuário A não consegue acessar cadernos/páginas do usuário B (HTTP 403/404).
- [ ] Digitar com formatação (bold, cor, marcação) reflete no JSON persistido e reabre igual.
- [ ] Imagem e PDF enviados aparecem embutidos na página após recarregar.
- [ ] Autosave persiste a última edição mesmo com refresh imediato após digitar.
- [ ] Caderno alterna entre modo de páginas fixas e rolagem contínua.
- [ ] Linhas de caderno visíveis e configuráveis (cor/espaçamento).
- [ ] Usuário alterna entre tema claro e escuro; no escuro o fundo é preto, as
      linhas do caderno são brancas e o texto é claro por padrão.
