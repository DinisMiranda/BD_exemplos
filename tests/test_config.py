"""Testes para bd_exemplos.config.load_config."""
from __future__ import annotations

from pathlib import Path

import pytest

from bd_exemplos.config import MySQLConfig, load_config


def test_load_config_valid_toml(tmp_path: Path) -> None:
    """load_config devolve MySQLConfig quando o TOML é válido."""
    toml_file = tmp_path / "config.toml"
    toml_file.write_text(
        """
[mysql]
host = "127.0.0.1"
port = 3306
user = "root"
password = "secret"
database = "BD_TESTE"
""",
        encoding="utf-8",
    )
    cfg = load_config(toml_file)
    assert isinstance(cfg, MySQLConfig)
    assert cfg.host == "127.0.0.1"
    assert cfg.port == 3306
    assert cfg.user == "root"
    assert cfg.password == "secret"
    assert cfg.database == "BD_TESTE"


def test_load_config_accepts_empty_password(tmp_path: Path) -> None:
    """load_config aceita password vazia (desenvolvimento local)."""
    toml_file = tmp_path / "config.toml"
    toml_file.write_text(
        """
[mysql]
host = "localhost"
port = 3306
user = "root"
password = ""
database = "BD"
""",
        encoding="utf-8",
    )
    cfg = load_config(toml_file)
    assert cfg.password == ""


def test_load_config_missing_password_uses_default(tmp_path: Path) -> None:
    """Quando password está ausente no TOML, usa string vazia."""
    toml_file = tmp_path / "config.toml"
    toml_file.write_text(
        """
[mysql]
host = "localhost"
port = 3306
user = "root"
database = "BD"
""",
        encoding="utf-8",
    )
    cfg = load_config(toml_file)
    assert cfg.password == ""


def test_load_config_file_not_found() -> None:
    """Ficheiro inexistente levanta FileNotFoundError."""
    with pytest.raises(FileNotFoundError, match="Config file not found"):
        load_config(Path("/nao/existe/config.toml"))


def test_load_config_missing_mysql_section(tmp_path: Path) -> None:
    """TOML sem secção [mysql] levanta ValueError."""
    toml_file = tmp_path / "config.toml"
    toml_file.write_text(
        """
[other]
key = "value"
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="Missing \\[mysql\\] section"):
        load_config(toml_file)


def test_load_config_port_must_be_int(tmp_path: Path) -> None:
    """port deve ser inteiro positivo."""
    toml_file = tmp_path / "config.toml"
    toml_file.write_text(
        """
[mysql]
host = "localhost"
port = "3306"
user = "root"
password = ""
database = "BD"
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="expected positive int"):
        load_config(toml_file)


def test_load_config_port_must_be_positive(tmp_path: Path) -> None:
    """port deve ser > 0."""
    toml_file = tmp_path / "config.toml"
    toml_file.write_text(
        """
[mysql]
host = "localhost"
port = 0
user = "root"
password = ""
database = "BD"
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="expected positive int"):
        load_config(toml_file)


def test_load_config_required_str_empty_fails(tmp_path: Path) -> None:
    """Campos obrigatórios (host, user, database) não podem ser vazios."""
    toml_file = tmp_path / "config.toml"
    toml_file.write_text(
        """
[mysql]
host = ""
port = 3306
user = "root"
password = ""
database = "BD"
""",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="host"):
        load_config(toml_file)
