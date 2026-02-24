"""
Library database seed (authors, books, readers, loans).
Uses the database name defined in config.toml.
Usage (after poetry install): python -m bd_exemplos.scripts.seed_biblioteca
"""
from __future__ import annotations

from pathlib import Path

from dataclasses import dataclass
from datetime import date, timedelta
from random import Random

from bd_exemplos.config import load_config
from bd_exemplos.db import connect_mysql

# config.toml at repository root (3 levels up from this file)
CONFIG_PATH = Path(__file__).resolve().parent.parent.parent / "config.toml"


# -----------------------------
# Models
# -----------------------------
@dataclass(frozen=True)
class Autor:
    id_autor: int
    nome: str
    pais: str


@dataclass(frozen=True)
class Livro:
    id_livro: int
    titulo: str
    id_autor: int
    ano: int
    isbn: str


@dataclass(frozen=True)
class Leitor:
    id_leitor: int
    nome: str
    email: str
    data_inscricao: date


@dataclass(frozen=True)
class Emprestimo:
    id_emprestimo: int
    id_livro: int
    id_leitor: int
    data_emprestimo: date
    data_devolucao: date | None


# -----------------------------
# Static data
# -----------------------------
def build_autores() -> list[Autor]:
    return [
        Autor(1, "José Saramago", "Portugal"),
        Autor(2, "Fernando Pessoa", "Portugal"),
        Autor(3, "Agatha Christie", "Reino Unido"),
        Autor(4, "Gabriel García Márquez", "Colômbia"),
        Autor(5, "Mia Couto", "Moçambique"),
    ]


def build_livros() -> list[Livro]:
    return [
        Livro(1, "Memorial do Convento", 1, 1982, "972-21-0123-4"),
        Livro(2, "Ensaio sobre a Cegueira", 1, 1995, "972-21-0124-2"),
        Livro(3, "O Livro do Desassossego", 2, 1982, "972-44-1001-1"),
        Livro(4, "Morte no Nilo", 3, 1937, "978-0-00-711931-8"),
        Livro(5, "O Assassinato de Roger Ackroyd", 3, 1926, "978-0-00-711932-5"),
        Livro(6, "Cem Anos de Solidão", 4, 1967, "978-0-06-088328-7"),
        Livro(7, "O Amor nos Tempos de Cólera", 4, 1985, "978-0-14-024492-2"),
        Livro(8, "Terra Sonâmbula", 5, 1992, "972-21-0501-3"),
        Livro(9, "Um Rio Chamado Tempo, uma Casa Chamada Terra", 5, 2003, "972-21-0512-9"),
        Livro(10, "O Evangelho segundo Jesus Cristo", 1, 1991, "972-21-0125-0"),
    ]


def build_leitores() -> list[Leitor]:
    return [
        Leitor(1, "Maria Oliveira", "maria.oliveira@mail.pt", date(2022, 3, 10)),
        Leitor(2, "António Nunes", "antonio.nunes@mail.pt", date(2022, 5, 22)),
        Leitor(3, "Catarina Lopes", "catarina.lopes@mail.pt", date(2023, 1, 15)),
        Leitor(4, "Rui Ferreira", "rui.ferreira@mail.pt", date(2023, 8, 7)),
        Leitor(5, "Sandra Teixeira", "sandra.teixeira@mail.pt", date(2024, 2, 28)),
    ]


def build_emprestimos(rng: Random) -> list[Emprestimo]:
    """Build sample loans (some returned, some still out)."""
    emprestimos: list[Emprestimo] = []
    pid = 1
    # Past loans (returned)
    for (id_livro, id_leitor, emp, dev) in [
        (1, 1, date(2024, 1, 5), date(2024, 1, 25)),
        (3, 2, date(2024, 2, 10), date(2024, 3, 10)),
        (6, 1, date(2024, 3, 1), date(2024, 3, 28)),
        (4, 3, date(2024, 4, 12), date(2024, 5, 10)),
        (8, 2, date(2024, 5, 20), date(2024, 6, 18)),
        (2, 4, date(2024, 6, 1), date(2024, 6, 29)),
        (7, 1, date(2024, 7, 15), date(2024, 8, 12)),
        (5, 3, date(2024, 8, 1), date(2024, 8, 30)),
        (9, 5, date(2024, 9, 10), date(2024, 10, 8)),
        (10, 4, date(2024, 10, 1), date(2024, 10, 29)),
    ]:
        emprestimos.append(Emprestimo(pid, id_livro, id_leitor, emp, dev))
        pid += 1
    # Current loans (no return date yet)
    for (id_livro, id_leitor, emp) in [
        (1, 3, date(2025, 1, 6)),
        (4, 5, date(2025, 1, 15)),
        (6, 2, date(2025, 2, 1)),
    ]:
        emprestimos.append(Emprestimo(pid, id_livro, id_leitor, emp, None))
        pid += 1
    # A few more random ones
    for _ in range(12):
        id_livro = rng.randint(1, 10)
        id_leitor = rng.randint(1, 5)
        start = date(2024, 1, 1) + timedelta(days=rng.randint(0, 300))
        dev = start + timedelta(days=rng.randint(14, 45)) if rng.random() < 0.7 else None
        if dev and dev > date.today():
            dev = None
        emprestimos.append(Emprestimo(pid, id_livro, id_leitor, start, dev))
        pid += 1
    return emprestimos


# -----------------------------
# DDL
# -----------------------------
def ddl_biblioteca(database: str) -> list[str]:
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
        CREATE TABLE IF NOT EXISTS autores (
          ID_Autor   INT          NOT NULL,
          Nome       VARCHAR(120) NOT NULL,
          Pais       VARCHAR(60)  NOT NULL,
          PRIMARY KEY (ID_Autor)
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS livros (
          ID_Livro   INT          NOT NULL,
          Titulo     VARCHAR(200) NOT NULL,
          ID_Autor   INT          NOT NULL,
          Ano        SMALLINT     NOT NULL,
          ISBN       VARCHAR(20)  NOT NULL,
          PRIMARY KEY (ID_Livro),
          UNIQUE KEY uq_livros_isbn (ISBN),
          KEY idx_livros_autor (ID_Autor),
          CONSTRAINT fk_livros_autor
            FOREIGN KEY (ID_Autor)
            REFERENCES autores (ID_Autor)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS leitores (
          ID_Leitor        INT          NOT NULL,
          Nome             VARCHAR(120) NOT NULL,
          Email            VARCHAR(100) NOT NULL,
          Data_Inscricao   DATE         NOT NULL,
          PRIMARY KEY (ID_Leitor),
          UNIQUE KEY uq_leitores_email (Email)
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS emprestimos (
          ID_Emprestimo     INT      NOT NULL,
          ID_Livro          INT      NOT NULL,
          ID_Leitor         INT      NOT NULL,
          Data_Emprestimo   DATE     NOT NULL,
          Data_Devolucao    DATE     NULL,
          PRIMARY KEY (ID_Emprestimo),
          KEY idx_emp_livro (ID_Livro),
          KEY idx_emp_leitor (ID_Leitor),
          KEY idx_emp_datas (Data_Emprestimo, Data_Devolucao),
          CONSTRAINT fk_emp_livro
            FOREIGN KEY (ID_Livro)
            REFERENCES livros (ID_Livro)
            ON UPDATE CASCADE
            ON DELETE RESTRICT,
          CONSTRAINT fk_emp_leitor
            FOREIGN KEY (ID_Leitor)
            REFERENCES leitores (ID_Leitor)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
        ) ENGINE=InnoDB
        """,
    ]


def main() -> None:
    cfg = load_config(CONFIG_PATH)
    database = cfg.database
    rng = Random(42)

    autores = build_autores()
    livros = build_livros()
    leitores = build_leitores()
    emprestimos = build_emprestimos(rng)

    conn = connect_mysql(
        host=cfg.host,
        port=cfg.port,
        user=cfg.user,
        password=cfg.password,
    )
    conn.autocommit = False

    try:
        cur = conn.cursor()
        for stmt in ddl_biblioteca(database):
            cur.execute(stmt)

        # Clear tables (respect FK order)
        cur.execute(f"DELETE FROM {database}.emprestimos")
        cur.execute(f"DELETE FROM {database}.livros")
        cur.execute(f"DELETE FROM {database}.leitores")
        cur.execute(f"DELETE FROM {database}.autores")

        cur.executemany(
            f"INSERT INTO {database}.autores (ID_Autor, Nome, Pais) VALUES (%s, %s, %s)",
            [(a.id_autor, a.nome, a.pais) for a in autores],
        )
        cur.executemany(
            f"INSERT INTO {database}.livros (ID_Livro, Titulo, ID_Autor, Ano, ISBN) VALUES (%s, %s, %s, %s, %s)",
            [(l.id_livro, l.titulo, l.id_autor, l.ano, l.isbn) for l in livros],
        )
        cur.executemany(
            f"INSERT INTO {database}.leitores (ID_Leitor, Nome, Email, Data_Inscricao) VALUES (%s, %s, %s, %s)",
            [(r.id_leitor, r.nome, r.email, r.data_inscricao) for r in leitores],
        )
        cur.executemany(
            f"INSERT INTO {database}.emprestimos (ID_Emprestimo, ID_Livro, ID_Leitor, Data_Emprestimo, Data_Devolucao) VALUES (%s, %s, %s, %s, %s)",
            [(e.id_emprestimo, e.id_livro, e.id_leitor, e.data_emprestimo, e.data_devolucao) for e in emprestimos],
        )

        conn.commit()
        print("DONE — Database created:", database)
        print(f"  authors:  {len(autores)}")
        print(f"  books:    {len(livros)}")
        print(f"  readers:  {len(leitores)}")
        print(f"  loans:    {len(emprestimos)}")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
