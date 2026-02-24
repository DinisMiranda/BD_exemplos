"""Tests for data builders (seed_loja and seed_biblioteca)."""

from __future__ import annotations

from random import Random

from bd_exemplos.scripts.seed_biblioteca import (
    build_autores,
    build_emprestimos,
    build_leitores,
    build_livros,
)
from bd_exemplos.scripts.seed_loja import build_static_entities

# --- Shop: build_static_entities ---


def test_build_static_entities_returns_three_lists() -> None:
    """build_static_entities returns (suppliers, products, clients)."""
    suppliers, products, clients = build_static_entities()
    assert isinstance(suppliers, list)
    assert isinstance(products, list)
    assert isinstance(clients, list)


def test_build_static_entities_suppliers_count_and_first() -> None:
    """Suppliers: 3 entities, first is Nike."""
    suppliers, _, _ = build_static_entities()
    assert len(suppliers) == 3
    assert suppliers[0].nome == "Nike"
    assert suppliers[0].id_fornecedor == 1
    assert suppliers[0].email == "sales@nike.pt"


def test_build_static_entities_products_count() -> None:
    """Products: 23 (includes never-sold)."""
    _, products, _ = build_static_entities()
    assert len(products) == 23


def test_build_static_entities_clients_count() -> None:
    """Clients: 10."""
    _, _, clients = build_static_entities()
    assert len(clients) == 10


# --- Library: build_autores, build_livros, build_leitores, build_emprestimos ---


def test_build_autores_count_and_first() -> None:
    """Authors: 5, first is José Saramago."""
    autores = build_autores()
    assert len(autores) == 5
    assert autores[0].nome == "José Saramago"
    assert autores[0].id_autor == 1
    assert autores[0].pais == "Portugal"


def test_build_livros_count_and_first() -> None:
    """Books: 10, first is Memorial do Convento."""
    livros = build_livros()
    assert len(livros) == 10
    assert livros[0].titulo == "Memorial do Convento"
    assert livros[0].id_autor == 1
    assert livros[0].ano == 1982


def test_build_leitores_count_and_first() -> None:
    """Readers: 5."""
    leitores = build_leitores()
    assert len(leitores) == 5
    assert leitores[0].nome == "Maria Oliveira"
    assert leitores[0].email == "maria.oliveira@mail.pt"


def test_build_emprestimos_returns_list() -> None:
    """build_emprestimos returns a list of loans."""
    rng = Random(42)
    emprestimos = build_emprestimos(rng)
    assert isinstance(emprestimos, list)
    assert len(emprestimos) >= 10  # fixed + random
    first = emprestimos[0]
    assert first.id_emprestimo == 1
    assert first.id_livro == 1
    assert first.id_leitor == 1
    assert first.data_devolucao is not None  # first one is returned
