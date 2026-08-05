# Projeto Flask com PostgreSQL

## Variáveis de ambiente

Crie um arquivo `.env` na raiz com:

```env
FLASK_ENV=development
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/banco2
MONGODB_URI=mongodb://localhost:27017/banco2
PORT=5000
```

Antes de rodar, crie o banco PostgreSQL local:

```bash
createdb banco2
```

E deixe um MongoDB disponível em `MONGODB_URI` (por exemplo `mongodb://localhost:27017/banco2`).

## Executar localmente

```bash
python -m pip install -r requirements.txt
python app/main.py
```

## Deploy

No Render/Railway, configure a variável `DATABASE_URL` no painel do serviço.
