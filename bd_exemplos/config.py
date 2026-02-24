"""Load MySQL configuration from a TOML file.

This module parses a ``[mysql]`` section and returns a frozen dataclass
suitable for connecting to MySQL and selecting a database. The password
field is optional (defaults to empty string) for local development.

Example:
    Config file ``config.toml``::

        [mysql]
        host = "127.0.0.1"
        port = 3306
        user = "root"
        password = ""
        database = "BD_TESTE"

    Usage::

        from pathlib import Path
        from bd_exemplos.config import load_config

        cfg = load_config(Path("config.toml"))
        # cfg.host, cfg.port, cfg.user, cfg.password, cfg.database
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import toml


@dataclass(frozen=True)
class MySQLConfig:
    """MySQL connection and database settings.

    Attributes:
        host: MySQL server hostname or address.
        port: MySQL server port (positive integer).
        user: MySQL user name.
        password: MySQL password (may be empty for local dev).
        database: Database name to use.
    """

    host: str
    port: int
    user: str
    password: str
    database: str


def _require_str(d: dict[str, Any], key: str) -> str:
    """Extract a required non-empty string from a dict.

    Args:
        d: Dictionary containing the key.
        key: Key to look up.

    Returns:
        Stripped string value.

    Raises:
        ValueError: If key is missing, value is not a string, or value is empty
            after stripping.
    """
    v = d.get(key)
    if not isinstance(v, str) or not v.strip():
        raise ValueError(f"Invalid or missing '{key}' (expected non-empty string).")
    return v.strip()


def _optional_str(d: dict[str, Any], key: str, default: str = "") -> str:
    """Extract an optional string from a dict, with default for missing/empty.

    Used for optional fields such as password (empty string for no password).

    Args:
        d: Dictionary containing the key.
        key: Key to look up.
        default: Value to return if key is missing or value is empty. Defaults to "".

    Returns:
        Stripped string value, or default.

    Raises:
        ValueError: If value is present but not a string.
    """
    v = d.get(key)
    if v is None:
        return default
    if not isinstance(v, str):
        raise ValueError(f"Invalid '{key}' (expected string or missing).")
    return v.strip() if v.strip() else default


def _require_int(d: dict[str, Any], key: str) -> int:
    """Extract a required positive integer from a dict.

    Args:
        d: Dictionary containing the key.
        key: Key to look up.

    Returns:
        Integer value.

    Raises:
        ValueError: If key is missing, value is not an int, or value is not positive.
    """
    v = d.get(key)
    if not isinstance(v, int) or v <= 0:
        raise ValueError(f"Invalid or missing '{key}' (expected positive int).")
    return v


def load_config(path: Path) -> MySQLConfig:
    """Load MySQL configuration from a TOML file.

    The file must contain a top-level ``[mysql]`` section with the following
    keys: ``host``, ``port``, ``user``, ``database`` (all required),
    and ``password`` (optional; defaults to empty string).

    Args:
        path: Path to the TOML file (e.g. ``config.toml``). File must exist
            and be readable as UTF-8.

    Returns:
        A frozen ``MySQLConfig`` instance with all fields populated.

    Raises:
        FileNotFoundError: If ``path`` does not exist.
        ValueError: If the file is not valid TOML, the ``[mysql]`` section
            is missing, or any required field is missing or invalid (e.g. port
            not a positive integer, host empty).
    """
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
    password = _optional_str(mysql, "password", default="")
    database = _require_str(mysql, "database")

    return MySQLConfig(host=host, port=port, user=user, password=password, database=database)
