"""Shared MySQL connection used by seed scripts."""
from __future__ import annotations

import mysql.connector
from mysql.connector.connection import MySQLConnection


def connect_mysql(*, host: str, port: int, user: str, password: str) -> MySQLConnection:
    if not host:
        raise ValueError("host must be non-empty")
    if port <= 0:
        raise ValueError("port must be > 0")
    return mysql.connector.connect(host=host, port=port, user=user, password=password)
