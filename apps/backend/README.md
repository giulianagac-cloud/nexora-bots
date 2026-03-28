# Backend

FastAPI starter service for TrenBot Enterprise.

## Run

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn app.main:app --reload
```

## Endpoints

- `GET /health`
- `POST /chat`

