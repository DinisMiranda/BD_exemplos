"""Tests for bd_exemplos.scripts.seed_cinema DDL and data."""

from __future__ import annotations

import pytest
from bd_exemplos.scripts.seed_cinema import (
    build_bilhetes,
    build_filmes,
    build_salas,
    build_sessoes,
    ddl_cinema,
)


def test_ddl_cinema_returns_create_and_use() -> None:
    """ddl_cinema returns CREATE DATABASE, USE, and CREATE TABLEs."""
    stmts = ddl_cinema("CINEMA_TEST")
    assert len(stmts) >= 2
    assert "CREATE DATABASE" in stmts[0]
    assert "USE" in stmts[1] or "CINEMA_TEST" in stmts[1]
    full = " ".join(stmts)
    assert "filmes" in full
    assert "salas" in full
    assert "sessoes" in full
    assert "bilhetes" in full


def test_ddl_cinema_empty_database_raises() -> None:
    """ddl_cinema with empty database name raises."""
    with pytest.raises(ValueError, match="database must be non-empty"):
        ddl_cinema("")
    with pytest.raises(ValueError, match="database must be non-empty"):
        ddl_cinema("   ")


def test_build_filmes() -> None:
    """build_filmes returns deterministic list of films."""
    filmes = build_filmes()
    assert len(filmes) == 6
    assert filmes[0].id_filme == 1
    assert filmes[0].titulo == "O Pátio das Cantigas"
    assert filmes[0].duracao_min == 95
    assert filmes[0].ano == 1942


def test_build_salas() -> None:
    """build_salas returns deterministic list of rooms."""
    salas = build_salas()
    assert len(salas) == 3
    assert salas[0].nome == "Sala 1"
    assert salas[0].capacidade == 120


def test_build_sessoes_reproducible() -> None:
    """build_sessoes is reproducible with same seed."""
    from random import Random

    s1 = build_sessoes(Random(42))
    s2 = build_sessoes(Random(42))
    assert len(s1) == len(s2)
    assert [x.id_sessao for x in s1] == [x.id_sessao for x in s2]


def test_build_bilhetes_uses_sessoes() -> None:
    """build_bilhetes produces tickets for given sessions."""
    from random import Random

    sessoes = build_sessoes(Random(42))
    bilhetes = build_bilhetes(Random(42), sessoes)
    assert len(bilhetes) >= len(sessoes)
    sessao_ids = {s.id_sessao for s in sessoes}
    for b in bilhetes:
        assert b.id_sessao in sessao_ids
