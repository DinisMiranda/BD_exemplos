"""Clinic database seed script.

Populates a MySQL database with deterministic and random data for the domain:
doctors (medicos), patients (pacientes), and appointments (consultas).
The database name and connection settings are read from ``config.toml`` at
the repository root.

Usage:
    From the repo root after ``poetry install``::

        python -m bd_exemplos.scripts.seed_clinica

    The script creates the database and tables if they do not exist, clears
    existing data, then inserts the seed data and prints row counts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta
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
class Medico:
    """A doctor (médico) entity.

    Attributes:
        id_medico: Primary key.
        nome: Doctor name.
        especialidade: Specialty (e.g. Clínica Geral, Cardiologia).
    """

    id_medico: int
    nome: str
    especialidade: str


@dataclass(frozen=True)
class Paciente:
    """A patient (paciente) entity.

    Attributes:
        id_paciente: Primary key.
        nome: Full name.
        data_nascimento: Date of birth.
        nif: Tax ID (unique in schema).
    """

    id_paciente: int
    nome: str
    data_nascimento: date
    nif: str


@dataclass(frozen=True)
class Consulta:
    """An appointment (consulta) entity.

    Attributes:
        id_consulta: Primary key.
        id_medico: Foreign key to Medico.
        id_paciente: Foreign key to Paciente.
        data_consulta: Appointment date and time.
        notas: Optional notes (can be empty).
    """

    id_consulta: int
    id_medico: int
    id_paciente: int
    data_consulta: datetime
    notas: str


# -----------------------------
# Static data
# -----------------------------
def build_medicos() -> list[Medico]:
    """Build the fixed set of doctors for the clinic seed.

    Returns:
        A list of 5 doctors (deterministic). Used to populate the ``medicos`` table.
    """
    return [
        Medico(1, "Dra. Ana Martins", "Clínica Geral"),
        Medico(2, "Dr. Bruno Sousa", "Cardiologia"),
        Medico(3, "Dra. Carla Reis", "Pediatria"),
        Medico(4, "Dr. Duarte Lopes", "Ortopedia"),
        Medico(5, "Dra. Eduarda Ferreira", "Dermatologia"),
    ]


def build_pacientes() -> list[Paciente]:
    """Build the fixed set of patients for the clinic seed.

    Returns:
        A list of 8 patients (deterministic). Used to populate the ``pacientes`` table.
    """
    return [
        Paciente(1, "João Silva", date(1985, 4, 12), "123456789"),
        Paciente(2, "Maria Santos", date(1990, 8, 3), "234567890"),
        Paciente(3, "Pedro Oliveira", date(1978, 1, 25), "345678901"),
        Paciente(4, "Inês Costa", date(2001, 11, 7), "456789012"),
        Paciente(5, "Ricardo Almeida", date(1965, 6, 18), "567890123"),
        Paciente(6, "Sofia Pereira", date(1995, 2, 28), "678901234"),
        Paciente(7, "Tiago Rodrigues", date(1982, 9, 14), "789012345"),
        Paciente(8, "Beatriz Nunes", date(2010, 5, 30), "890123456"),
    ]


def build_consultas(rng: Random) -> list[Consulta]:
    """Build sample appointments: fixed and random.

    Args:
        rng: Random number generator for reproducibility.

    Returns:
        A list of Consulta instances. Used to populate the ``consultas`` table.
    """
    consultas: list[Consulta] = []
    cid = 1
    base = datetime(2025, 2, 1, 9, 0, 0)
    notas_opts = ["", "Controlo anual.", "Seguimento.", "Queixas de dores."]
    for _ in range(50):
        id_medico = rng.randint(1, 5)
        id_paciente = rng.randint(1, 8)
        dt = base + timedelta(
            days=rng.randint(0, 60),
            hours=rng.randint(0, 8),
            minutes=rng.choice([0, 15, 30, 45]),
        )
        notas = rng.choice(notas_opts)
        consultas.append(Consulta(cid, id_medico, id_paciente, dt, notas))
        cid += 1
    return consultas


# -----------------------------
# DDL
# -----------------------------
def ddl_clinica(database: str) -> list[str]:
    """Return SQL statements to create the clinic database and its tables.

    Creates the database (if not exists) with utf8mb4, then tables in
    dependency order: medicos, pacientes, consultas, with foreign
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
        CREATE TABLE IF NOT EXISTS medicos (
          ID_Medico       INT          NOT NULL,
          Nome            VARCHAR(120) NOT NULL,
          Especialidade   VARCHAR(80)  NOT NULL,
          PRIMARY KEY (ID_Medico)
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS pacientes (
          ID_Paciente       INT          NOT NULL,
          Nome              VARCHAR(120) NOT NULL,
          Data_Nascimento   DATE         NOT NULL,
          NIF               VARCHAR(20)  NOT NULL,
          PRIMARY KEY (ID_Paciente),
          UNIQUE KEY uq_pacientes_nif (NIF)
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS consultas (
          ID_Consulta     INT           NOT NULL,
          ID_Medico       INT           NOT NULL,
          ID_Paciente     INT           NOT NULL,
          Data_Consulta   DATETIME      NOT NULL,
          Notas           VARCHAR(500)  NULL,
          PRIMARY KEY (ID_Consulta),
          KEY idx_consultas_medico (ID_Medico),
          KEY idx_consultas_paciente (ID_Paciente),
          KEY idx_consultas_data (Data_Consulta),
          CONSTRAINT fk_consultas_medico
            FOREIGN KEY (ID_Medico)
            REFERENCES medicos (ID_Medico)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
          CONSTRAINT fk_consultas_paciente
            FOREIGN KEY (ID_Paciente)
            REFERENCES pacientes (ID_Paciente)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
        ) ENGINE=InnoDB
        """,
    ]


def main() -> None:
    """Entry point: load config, seed the clinic database, and print insert counts.

    Reads ``config.toml`` from the repository root, builds doctors, patients,
    and appointments, connects to MySQL, creates the database and tables
    if needed, clears existing data, inserts seed data, commits, and prints
    the number of rows inserted per table.
    """
    cfg = load_config(CONFIG_PATH)
    database = cfg.database
    rng = Random(42)

    medicos = build_medicos()
    pacientes = build_pacientes()
    consultas = build_consultas(rng)

    conn = connect_mysql(
        host=cfg.host,
        port=cfg.port,
        user=cfg.user,
        password=cfg.password,
    )
    conn.autocommit = False

    try:
        cur = conn.cursor()
        for stmt in ddl_clinica(database):
            cur.execute(stmt)

        cur.execute(f"DELETE FROM {database}.consultas")
        cur.execute(f"DELETE FROM {database}.pacientes")
        cur.execute(f"DELETE FROM {database}.medicos")

        cur.executemany(
            f"INSERT INTO {database}.medicos (ID_Medico, Nome, Especialidade) VALUES (%s, %s, %s)",
            [(m.id_medico, m.nome, m.especialidade) for m in medicos],
        )
        cur.executemany(
            f"INSERT INTO {database}.pacientes (ID_Paciente, Nome, Data_Nascimento, NIF) VALUES (%s, %s, %s, %s)",
            [(p.id_paciente, p.nome, p.data_nascimento, p.nif) for p in pacientes],
        )
        cur.executemany(
            f"INSERT INTO {database}.consultas (ID_Consulta, ID_Medico, ID_Paciente, Data_Consulta, Notas) VALUES (%s, %s, %s, %s, %s)",
            [
                (c.id_consulta, c.id_medico, c.id_paciente, c.data_consulta, c.notas)
                for c in consultas
            ],
        )

        conn.commit()
        print("DONE — Database created:", database)
        print(f"  doctors:       {len(medicos)}")
        print(f"  patients:      {len(pacientes)}")
        print(f"  appointments:  {len(consultas)}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
