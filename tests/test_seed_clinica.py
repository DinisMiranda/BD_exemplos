"""Tests for bd_exemplos.scripts.seed_clinica DDL and data."""

from __future__ import annotations

import pytest
from bd_exemplos.scripts.seed_clinica import (
    build_consultas,
    build_medicos,
    build_pacientes,
    ddl_clinica,
)


def test_ddl_clinica_returns_create_and_use() -> None:
    """ddl_clinica returns CREATE DATABASE, USE, and CREATE TABLEs."""
    stmts = ddl_clinica("CLINICA_TEST")
    assert len(stmts) >= 2
    assert "CREATE DATABASE" in stmts[0]
    assert "USE" in stmts[1] or "CLINICA_TEST" in stmts[1]
    full = " ".join(stmts)
    assert "medicos" in full
    assert "pacientes" in full
    assert "consultas" in full


def test_ddl_clinica_empty_database_raises() -> None:
    """ddl_clinica with empty database name raises."""
    with pytest.raises(ValueError, match="database must be non-empty"):
        ddl_clinica("")
    with pytest.raises(ValueError, match="database must be non-empty"):
        ddl_clinica("   ")


def test_build_medicos() -> None:
    """build_medicos returns deterministic list of doctors."""
    medicos = build_medicos()
    assert len(medicos) == 5
    assert medicos[0].id_medico == 1
    assert medicos[0].especialidade == "Clínica Geral"


def test_build_pacientes() -> None:
    """build_pacientes returns deterministic list of patients."""
    pacientes = build_pacientes()
    assert len(pacientes) == 8
    assert pacientes[0].nif == "123456789"


def test_build_consultas_reproducible() -> None:
    """build_consultas is reproducible with same seed."""
    from random import Random

    c1 = build_consultas(Random(42))
    c2 = build_consultas(Random(42))
    assert len(c1) == 50
    assert len(c1) == len(c2)
    assert [x.id_consulta for x in c1] == [x.id_consulta for x in c2]
