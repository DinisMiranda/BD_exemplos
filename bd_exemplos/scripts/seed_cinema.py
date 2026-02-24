"""Cinema database seed script.

Populates a MySQL database with deterministic and random data for the domain:
films (filmes), rooms (salas), sessions (sessoes), and tickets (bilhetes).
The database name and connection settings are read from ``config.toml`` at
the repository root.

Usage:
    From the repo root after ``poetry install``::

        python -m bd_exemplos.scripts.seed_cinema

    The script creates the database and tables if they do not exist, clears
    existing data, then inserts the seed data and prints row counts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
from random import Random

from bd_exemplos.config import load_config
from bd_exemplos.db import connect_mysql

# config.toml at repository root (3 levels up from this file)
CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.toml"


# -----------------------------
# Models
# -----------------------------
@dataclass(frozen=True)
class Filme:
    """A film (filme) entity.

    Attributes:
        id_filme: Primary key.
        titulo: Film title.
        duracao_min: Duration in minutes.
        ano: Release year.
    """

    id_filme: int
    titulo: str
    duracao_min: int
    ano: int


@dataclass(frozen=True)
class Sala:
    """A cinema room (sala) entity.

    Attributes:
        id_sala: Primary key.
        nome: Room name.
        capacidade: Seat capacity.
    """

    id_sala: int
    nome: str
    capacidade: int


@dataclass(frozen=True)
class Sessao:
    """A screening session (sessao) entity.

    Attributes:
        id_sessao: Primary key.
        id_filme: Foreign key to Filme.
        id_sala: Foreign key to Sala.
        data_hora: Session date and time.
    """

    id_sessao: int
    id_filme: int
    id_sala: int
    data_hora: datetime


@dataclass(frozen=True)
class Bilhete:
    """A ticket (bilhete) entity.

    Attributes:
        id_bilhete: Primary key.
        id_sessao: Foreign key to Sessao.
        preco: Ticket price.
    """

    id_bilhete: int
    id_sessao: int
    preco: Decimal


# -----------------------------
# Static data
# -----------------------------
def build_filmes() -> list[Filme]:
    """Build the fixed set of films for the cinema seed.

    Returns:
        A list of 6 films (deterministic). Used to populate the ``filmes`` table.
    """
    return [
        Filme(1, "O Pátio das Cantigas", 95, 1942),
        Filme(2, "Aniki-Bóbó", 71, 1942),
        Filme(3, "A Canção de Lisboa", 95, 1933),
        Filme(4, "O Leão da Estrela", 88, 1947),
        Filme(5, "O Costa do Castelo", 98, 1943),
        Filme(6, "Fado, História d'uma Cantadeira", 95, 1948),
    ]


def build_salas() -> list[Sala]:
    """Build the fixed set of rooms for the cinema seed.

    Returns:
        A list of 3 rooms (deterministic). Used to populate the ``salas`` table.
    """
    return [
        Sala(1, "Sala 1", 120),
        Sala(2, "Sala 2", 80),
        Sala(3, "Sala 3", 50),
    ]


def build_sessoes(rng: Random) -> list[Sessao]:
    """Build sample sessions: fixed and random screenings.

    Args:
        rng: Random number generator for reproducibility.

    Returns:
        A list of Sessao instances. Used to populate the ``sessoes`` table.
    """
    sessoes: list[Sessao] = []
    base = datetime(2025, 3, 1, 10, 0, 0)
    sid = 1
    for day in range(14):
        for film_id in (1, 2, 3, 4, 5, 6):
            for room_id in (1, 2, 3):
                if (film_id + room_id + day) % 3 == 0:  # subset of combinations
                    dt = base + timedelta(days=day, hours=rng.randint(0, 12))
                    sessoes.append(Sessao(sid, film_id, room_id, dt))
                    sid += 1
    return sessoes


def build_bilhetes(rng: Random, sessoes: list[Sessao]) -> list[Bilhete]:
    """Build sample tickets for the given sessions.

    Args:
        rng: Random number generator for reproducibility.
        sessoes: List of sessions to attach tickets to.

    Returns:
        A list of Bilhete instances. Used to populate the ``bilhetes`` table.
    """
    precos = [Decimal("5.00"), Decimal("7.50"), Decimal("10.00")]
    bilhetes: list[Bilhete] = []
    bid = 1
    for sessao in sessoes:
        n = rng.randint(1, 20)
        for _ in range(n):
            preco = rng.choice(precos)
            bilhetes.append(Bilhete(bid, sessao.id_sessao, preco))
            bid += 1
    return bilhetes


# -----------------------------
# DDL
# -----------------------------
def ddl_cinema(database: str) -> list[str]:
    """Return SQL statements to create the cinema database and its tables.

    Creates the database (if not exists) with utf8mb4, then tables in
    dependency order: filmes, salas, sessoes, bilhetes, with foreign
    keys and indexes.

    Args:
        database: Database name (whitespace is stripped). Must be non-empty.

    Returns:
        List of SQL strings (CREATE DATABASE, USE, CREATE TABLE ...). Execute
        in order.

    Raises:
        ValueError: If ``database`` is empty after stripping.
    """
    db = database.strip()
    if not db:
        raise ValueError("database must be non-empty")
    return [
        f"""
        CREATE DATABASE IF NOT EXISTS {db}
          DEFAULT CHARACTER SET utf8mb4
          DEFAULT COLLATE utf8mb4_0900_ai_ci
        """,
        f"USE {db}",
        """
        CREATE TABLE IF NOT EXISTS filmes (
          ID_Filme     INT          NOT NULL,
          Titulo       VARCHAR(200) NOT NULL,
          Duracao_Min  INT          NOT NULL,
          Ano          SMALLINT     NOT NULL,
          PRIMARY KEY (ID_Filme)
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS salas (
          ID_Sala      INT          NOT NULL,
          Nome         VARCHAR(80)  NOT NULL,
          Capacidade   INT          NOT NULL,
          PRIMARY KEY (ID_Sala)
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS sessoes (
          ID_Sessao    INT       NOT NULL,
          ID_Filme     INT       NOT NULL,
          ID_Sala      INT       NOT NULL,
          Data_Hora    DATETIME  NOT NULL,
          PRIMARY KEY (ID_Sessao),
          KEY idx_sessoes_filme (ID_Filme),
          KEY idx_sessoes_sala (ID_Sala),
          KEY idx_sessoes_data (Data_Hora),
          CONSTRAINT fk_sessoes_filme
            FOREIGN KEY (ID_Filme)
            REFERENCES filmes (ID_Filme)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
          CONSTRAINT fk_sessoes_sala
            FOREIGN KEY (ID_Sala)
            REFERENCES salas (ID_Sala)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS bilhetes (
          ID_Bilhete   INT           NOT NULL,
          ID_Sessao    INT           NOT NULL,
          Preco        DECIMAL(10,2) NOT NULL,
          PRIMARY KEY (ID_Bilhete),
          KEY idx_bilhetes_sessao (ID_Sessao),
          CONSTRAINT fk_bilhetes_sessao
            FOREIGN KEY (ID_Sessao)
            REFERENCES sessoes (ID_Sessao)
            ON UPDATE CASCADE
            ON DELETE CASCADE
        ) ENGINE=InnoDB
        """,
    ]


def main() -> None:
    """Entry point: load config, seed the cinema database, and print insert counts.

    Reads ``config.toml`` from the repository root, builds films, rooms,
    sessions, and tickets, connects to MySQL, creates the database and tables
    if needed, clears existing data, inserts seed data, commits, and prints
    the number of rows inserted per table.
    """
    cfg = load_config(CONFIG_PATH)
    database = cfg.database
    rng = Random(42)

    filmes = build_filmes()
    salas = build_salas()
    sessoes = build_sessoes(rng)
    bilhetes = build_bilhetes(rng, sessoes)

    conn = connect_mysql(
        host=cfg.host,
        port=cfg.port,
        user=cfg.user,
        password=cfg.password,
    )
    conn.autocommit = False

    try:
        cur = conn.cursor()
        for stmt in ddl_cinema(database):
            cur.execute(stmt)

        cur.execute(f"DELETE FROM {database}.bilhetes")
        cur.execute(f"DELETE FROM {database}.sessoes")
        cur.execute(f"DELETE FROM {database}.filmes")
        cur.execute(f"DELETE FROM {database}.salas")

        cur.executemany(
            f"INSERT INTO {database}.filmes (ID_Filme, Titulo, Duracao_Min, Ano) VALUES (%s, %s, %s, %s)",
            [(f.id_filme, f.titulo, f.duracao_min, f.ano) for f in filmes],
        )
        cur.executemany(
            f"INSERT INTO {database}.salas (ID_Sala, Nome, Capacidade) VALUES (%s, %s, %s)",
            [(sala.id_sala, sala.nome, sala.capacidade) for sala in salas],
        )
        cur.executemany(
            f"INSERT INTO {database}.sessoes (ID_Sessao, ID_Filme, ID_Sala, Data_Hora) VALUES (%s, %s, %s, %s)",
            [(sess.id_sessao, sess.id_filme, sess.id_sala, sess.data_hora) for sess in sessoes],
        )
        cur.executemany(
            f"INSERT INTO {database}.bilhetes (ID_Bilhete, ID_Sessao, Preco) VALUES (%s, %s, %s)",
            [(b.id_bilhete, b.id_sessao, str(b.preco)) for b in bilhetes],
        )

        conn.commit()
        print("DONE — Database created:", database)
        print(f"  films:    {len(filmes)}")
        print(f"  rooms:    {len(salas)}")
        print(f"  sessions: {len(sessoes)}")
        print(f"  tickets:  {len(bilhetes)}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
