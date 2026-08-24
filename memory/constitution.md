# Constituição do Projeto Folium

> Princípios imutáveis que governam como as especificações viram código.
> Toda implementação, plano e tarefa devem respeitar estes artigos.

## Propósito

Folium é um caderno digital na nuvem: páginas com linhas simulando um caderno
real, formatação rica (cor de caneta, marcação, negrito, listas), inserção de
imagens, links e PDFs, com autenticação e sincronização individual.

## Artigo I — Spec-Driven Development (SDD)

- A especificação é a fonte primária da verdade. O código é a expressão dela.
- Nenhum código é escrito antes da spec, do plano e das tarefas correspondentes.
- Mudanças começam pela evolução das specs (`specs/001-caderno/*.md`), não pelo código.

## Artigo II — SOLID

- **S**ingle Responsibility: cada classe/módulo tem uma única razão para mudar.
- **O**pen/Closed: aberto para extensão, fechado para modificação.
- **L**iskov: subtipos substituíveis sem quebrar o contrato.
- **I**nterface Segregation: interfaces pequenas e específicas.
- **D**ependency Inversion: dependa de abstrações, não de implementações.

## Artigo III — Clean Code

- Nomes significativos e pronunciáveis.
- Funções pequenas, com um único nível de abstração.
- Sem comentários redundantes; o código deve se explicar sozinho.
- Tratamento de erros explícito (exceções, nunca códigos de retorno).
- Zero duplicação (DRY), exceto quando a abstração custaria mais que a repetição.

## Artigo IV — Design Patterns

- **Repository**: acesso a dados isolado atrás de interfaces (SQL, storage).
- **Service Layer**: regras de negócio orquestradas em serviços, fora de rotas e repositórios.
- **Dependency Injection**: dependências injetadas via `Depends` (FastAPI) / props (React).
- **Ports & Adapters (Hexagonal)**: domínio não conhece Postgres, S3 ou JWT diretamente.
- **DTOs**: Pydantic schemas na fronteira; entidades de domínio internas.

## Artigo V — Test-First

- Nenhum código de produção sem teste (unit/integration) definido antes.
- Cobertura obrigatória de serviços e repositórios; contratos de API testados.
- Rodar `pytest` (backend) e `vitest` (frontend) antes de considerar tarefa concluída.

## Artigo VI — Segurança e Isolamento

- Toda rota protegida exige autenticação (JWT), exceto cadastro/login/health.
- Um usuário jamais acessa dados de outro (isolamento por `user_id` em todas as queries).
- Segredos nunca no código-fonte; somente via variáveis de ambiente.
- Uploads validados por tipo/tamanho; senhas com hash bcrypt.

## Artigo VII — Simplicidade e Anti-Abstração

- MVP primeiro: sincronização individual, sem colaboração em tempo real.
- Não criar abstração genérica antes de existirem pelo menos dois casos reais de uso.
- Escolher a solução mais simples que resolva o problema atual.

## Artigo VIII — Colaboração futura (sem rework)

- O schema e a camada de dados devem evoluir para Yjs/Hocuspocus sem migração destrutiva.
- Conteúdo de página armazenado em JSON estruturado (ProseMirror/TipTap), nunca HTML cru.
- Versionamento de conteúdo desde o início (`revision`, `updated_at`).
