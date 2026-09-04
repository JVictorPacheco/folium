# Folium

Caderno digital na nuvem: páginas com linhas simulando um caderno real,
formatação rica (cor de caneta, marcação, negrito, listas, títulos, tamanho e
família de fonte), inserção de imagens, links e PDFs — redimensionáveis e
movíveis pela página —, exportação do caderno completo em PDF preservando a
aparência do papel, com autenticação e sincronização individual.

## Stack

- **Backend**: Python 3.12 + FastAPI + SQLAlchemy 2.0 (async) + Alembic + PostgreSQL
- **Frontend**: React 18 + TypeScript + Vite + TipTap + TanStack Query
- **Infra**: Docker + Docker Compose

## Executando com Docker

```bash
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend/API (OpenAPI): http://localhost:8000/docs
- Healthcheck: http://localhost:8000/health

O backend roda `alembic upgrade head` automaticamente no start.

Por padrão o backend usa o Postgres do container `db`. Para apontar para um
Postgres gerenciado (ex.: Supabase, via Session Pooler), defina `DATABASE_URL`
num `.env` na raiz do projeto (mesmo formato do `backend/.env.example`) antes
de subir o compose — sem `.env`, nada muda.

## Executando sem Docker (desenvolvimento)

Backend (requer Python 3.12 e Postgres):

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Crie um `.env` no frontend com `VITE_API_URL=http://localhost:8000` (ou use o
`.env.example`).

## Testes

```bash
# Backend (usa SQLite em memória)
cd backend && pytest -q

# Frontend
cd frontend && npm test
```

## Estrutura de specs (Spec-Driven Development)

- `memory/constitution.md` — princípios do projeto (SOLID, Clean Code, patterns)
- `specs/001-caderno/spec.md` — especificação da feature (o quê)
- `specs/001-caderno/plan.md` — plano técnico (como)
- `specs/001-caderno/tasks.md` — tarefas (execução)
