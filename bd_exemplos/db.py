"""Shared MySQL connection helper for seed scripts.

This module provides a single function to open a MySQL connection with
basic validation of host and port. Used by both the shop and library
seed scripts to avoid code duplication.
"""

from __future__ import annotations

import mysql.connector
from mysql.connector.connection import MySQLConnection


def connect_mysql(*, host: str, port: int, user: str, password: str) -> MySQLConnection:
    """Open a connection to a MySQL server.

    Args:
        host: Server hostname or IP address. Must be non-empty.
        port: Server port. Must be a positive integer (e.g. 3306).
        user: MySQL user name.
        password: MySQL password (may be empty string if the server allows
            no password for this user).

    Returns:
        An open ``MySQLConnection``. The caller is responsible for closing
        it (e.g. with a ``finally`` block or context manager).

    Raises:
        ValueError: If ``host`` is empty or ``port`` is not positive.
        mysql.connector.Error: If the connection fails (e.g. wrong credentials,
            server unreachable).
    """
    if not host:
        raise ValueError("host must be non-empty")
    if port <= 0:
        raise ValueError("port must be > 0")
    return mysql.connector.connect(host=host, port=port, user=user, password=password)
