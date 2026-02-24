"""Tests for bd_exemplos.scripts.seed_biblioteca DDL and data."""
from __future__ import annotations

import pytest

from bd_exemplos.scripts.seed_biblioteca import ddl_biblioteca


def test_ddl_biblioteca_returns_create_and_use() -> None:
    """ddl_biblioteca returns CREATE DATABASE, USE, and CREATE TABLEs."""
    stmts = ddl_biblioteca("LIB_TEST")
    assert len(stmts) >= 2
    assert "CREATE DATABASE" in stmts[0]
    assert "USE" in stmts[1] or "LIB_TEST" in stmts[1]
    full = " ".join(stmts)
    assert "autores" in full
    assert "livros" in full
    assert "leitores" in full
    assert "emprestimos" in full


def test_ddl_biblioteca_empty_database_raises() -> None:
    """ddl_biblioteca with empty database name raises."""
    with pytest.raises(ValueError, match="database must be non-empty"):
        ddl_biblioteca("")
    with pytest.raises(ValueError, match="database must be non-empty"):
        ddl_biblioteca("   ")
