"""Tests for bd_exemplos.scripts.seed_loja helpers and DDL."""

from __future__ import annotations

from decimal import Decimal
from random import Random
from unittest.mock import MagicMock

import pytest
from bd_exemplos.scripts.seed_loja import (
    build_orders_and_lines,
    build_static_entities,
    choose_size_for_product,
    chunked,
    compute_practiced_price,
    daterange_days,
    ddl_statements,
    exec_many,
    money,
    quant2,
)


def test_money_parses_and_rounds() -> None:
    """money() parses string and rounds to 2 decimal places."""
    assert money("19.99") == Decimal("19.99")
    assert money("19.996") == Decimal("20.00")
    assert money("0") == Decimal("0.00")


def test_quant2_rounds_decimal() -> None:
    """quant2() rounds Decimal to 2 places."""
    assert quant2(Decimal("10.999")) == Decimal("11.00")
    assert quant2(Decimal("10.001")) == Decimal("10.00")


def test_chunked_yields_batches() -> None:
    """chunked() yields lists of at most size elements."""
    data = [(1,), (2,), (3,), (4,), (5,)]
    assert list(chunked(data, 2)) == [[(1,), (2,)], [(3,), (4,)], [(5,)]]
    assert list(chunked(data, 5)) == [data]
    assert list(chunked([], 1)) == []


def test_chunked_invalid_size_raises() -> None:
    """chunked() raises ValueError for size <= 0."""
    with pytest.raises(ValueError, match="chunk size must be > 0"):
        list(chunked([(1,)], 0))
    with pytest.raises(ValueError, match="chunk size must be > 0"):
        list(chunked([(1,)], -1))


def test_daterange_days_returns_in_range() -> None:
    """daterange_days returns a date in [start, end_exclusive)."""
    from datetime import date

    rng = Random(42)
    start = date(2024, 1, 1)
    end = date(2024, 1, 31)
    for _ in range(20):
        d = daterange_days(start, end, rng)
        assert start <= d < end


def test_daterange_days_invalid_range_raises() -> None:
    """daterange_days raises ValueError when end <= start."""
    from datetime import date

    rng = Random(42)
    with pytest.raises(ValueError, match="Invalid date range"):
        daterange_days(date(2024, 1, 10), date(2024, 1, 10), rng)
    with pytest.raises(ValueError, match="Invalid date range"):
        daterange_days(date(2024, 1, 10), date(2024, 1, 5), rng)


def test_choose_size_for_product_shoes_returns_numeric() -> None:
    """Product 1 (shoes) gets numeric size."""
    rng = Random(42)
    sizes = {choose_size_for_product(1, rng) for _ in range(50)}
    assert sizes.issubset({"40", "41", "42", "43", "44", "45"})


def test_choose_size_for_product_apparel_returns_sml() -> None:
    """Products 2,5,6 get S/M/L/XL."""
    rng = Random(42)
    for pid in (2, 5, 6):
        s = choose_size_for_product(pid, rng)
        assert s in ("S", "M", "L", "XL")


def test_choose_size_for_product_one_size_returns_u() -> None:
    """Products 4,7,8,9 get U."""
    rng = Random(42)
    for pid in (4, 7, 8, 9):
        assert choose_size_for_product(pid, rng) == "U"


def test_compute_practiced_price_in_range() -> None:
    """compute_practiced_price returns value between 90% and 100% of base."""
    rng = Random(12345)
    base = Decimal("100.00")
    for _ in range(100):
        p = compute_practiced_price(base, rng)
        assert Decimal("90.00") <= p <= Decimal("100.00")
        assert p == quant2(p)


def test_build_orders_and_lines_minimal() -> None:
    """build_orders_and_lines with total_orders=50 returns orders and lines."""
    rng = Random(999)
    _, products, clients = build_static_entities()
    orders, lines = build_orders_and_lines(
        rng=rng,
        products=products,
        clients=clients,
        total_orders=50,
    )
    assert len(orders) == 50
    assert len(lines) >= 50
    order_nums = {o.num_encomenda for o in orders}
    for line in lines:
        assert line.num_encomenda in order_nums
        assert 1 <= line.id_produto <= 23
        assert line.quantidade >= 1


def test_build_orders_and_lines_too_few_raises() -> None:
    """build_orders_and_lines with total_orders < 50 raises."""
    rng = Random(42)
    _, products, clients = build_static_entities()
    with pytest.raises(ValueError, match="total_orders should be reasonably large"):
        build_orders_and_lines(
            rng=rng,
            products=products,
            clients=clients,
            total_orders=49,
        )


def test_ddl_statements_returns_create_and_use() -> None:
    """ddl_statements returns CREATE DATABASE, USE, and CREATE TABLEs."""
    stmts = ddl_statements("TEST_DB")
    assert len(stmts) >= 2
    assert "CREATE DATABASE" in stmts[0]
    assert "USE" in stmts[1] or "TEST_DB" in stmts[1]
    full = " ".join(stmts)
    assert "fornecedores" in full
    assert "produtos" in full
    assert "clientes" in full
    assert "encomendas" in full
    assert "detalhes_venda" in full


def test_ddl_statements_empty_database_raises() -> None:
    """ddl_statements with empty database name raises."""
    with pytest.raises(ValueError, match="database must be non-empty"):
        ddl_statements("")
    with pytest.raises(ValueError, match="database must be non-empty"):
        ddl_statements("   ")


def test_exec_many_empty_rows_returns_zero() -> None:
    """exec_many with no rows returns 0."""
    cur = MagicMock()
    n = exec_many(cur, "INSERT INTO t VALUES (%s)", [], batch=10)
    assert n == 0
    cur.executemany.assert_not_called()


def test_exec_many_batches_correctly() -> None:
    """exec_many calls executemany in batches."""
    cur = MagicMock()
    rows = [(i,) for i in range(5)]
    n = exec_many(cur, "INSERT INTO t VALUES (%s)", rows, batch=2)
    assert n == 5
    assert cur.executemany.call_count == 3  # 2+2+1
    cur.executemany.assert_any_call("INSERT INTO t VALUES (%s)", [(0,), (1,)])
    cur.executemany.assert_any_call("INSERT INTO t VALUES (%s)", [(2,), (3,)])
    cur.executemany.assert_any_call("INSERT INTO t VALUES (%s)", [(4,)])
