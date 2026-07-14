from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL


PROJECT_ROOT = Path(__file__).resolve().parent
ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)
DATASET_MODE = os.getenv(
    "DATASET_MODE",
    "demo",
).strip().lower()

if DATASET_MODE not in {"demo", "synthetic"}:
    raise RuntimeError(
        "DATASET_MODE 只能是 demo 或 synthetic"
    )

def require_env(name: str) -> str:
    """读取必需环境变量，不存在时给出明确错误。"""

    value = os.getenv(name)

    if value is None or value.strip() == "":
        raise RuntimeError(
            f"缺少环境变量 {name}，请检查项目根目录下的 .env 文件。"
        )

    return value


DB_URL = URL.create(
    drivername=require_env("DB_DRIVER"),
    username=require_env("DB_USER"),
    password=require_env("DB_PASSWORD"),
    host=require_env("DB_HOST"),
    port=int(require_env("DB_PORT")),
    database=require_env("DB_NAME"),
)

engine = create_engine(
    DB_URL,
    pool_pre_ping=True,
)