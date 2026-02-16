from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import toml


@dataclass(frozen=True)
class MySQLConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


def _require_str(d: Dict[str, Any], key: str) -> str:
    v = d.get(key)
    if not isinstance(v, str) or not v.strip():
        raise ValueError(f"Invalid or missing '{key}' (expected non-empty string).")
    return v.strip()


def _require_int(d: Dict[str, Any], key: str) -> int:
    v = d.get(key)
    if not isinstance(v, int) or v <= 0:
        raise ValueError(f"Invalid or missing '{key}' (expected positive int).")
    return v


def load_config(path: Path) -> MySQLConfig:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    data = toml.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Config root must be a TOML table/object.")

    mysql = data.get("mysql")
    if not isinstance(mysql, dict):
        raise ValueError("Missing [mysql] section in config.")

    host = _require_str(mysql, "host")
    port = _require_int(mysql, "port")
    user = _require_str(mysql, "user")
    password = _require_str(mysql, "password")
    database = _require_str(mysql, "database")

    return MySQLConfig(host=host, port=port, user=user, password=password, database=database)
