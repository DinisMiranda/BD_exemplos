"""Tests for bd_exemplos.db.connect_mysql."""
from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from bd_exemplos.db import connect_mysql


def test_connect_mysql_success_returns_connection() -> None:
    """With valid args, connect_mysql returns the result of mysql.connector.connect."""
    fake_conn = MagicMock()
    with patch("bd_exemplos.db.mysql.connector.connect", return_value=fake_conn) as mock_connect:
        conn = connect_mysql(host="localhost", port=3306, user="u", password="p")
    assert conn is fake_conn
    mock_connect.assert_called_once_with(
        host="localhost", port=3306, user="u", password="p"
    )


def test_connect_mysql_empty_host_raises() -> None:
    """Empty host raises ValueError."""
    with pytest.raises(ValueError, match="host must be non-empty"):
        connect_mysql(host="", port=3306, user="u", password="p")


def test_connect_mysql_port_zero_raises() -> None:
    """Port 0 raises ValueError."""
    with pytest.raises(ValueError, match="port must be > 0"):
        connect_mysql(host="localhost", port=0, user="u", password="p")


def test_connect_mysql_negative_port_raises() -> None:
    """Negative port raises ValueError."""
    with pytest.raises(ValueError, match="port must be > 0"):
        connect_mysql(host="localhost", port=-1, user="u", password="p")
