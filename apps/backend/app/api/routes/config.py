import json
from pathlib import Path

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter()

BASE_DIR = Path(__file__).resolve().parents[3]  # apps/backend/


@router.get("/config")
async def get_config() -> dict:
    client_id = get_settings().client_id
    path = BASE_DIR / "clients" / client_id / "config.json"
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return {"bot_name": data["bot_name"]}
