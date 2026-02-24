"""Shop (e-commerce) database seed script.

Populates a MySQL database with deterministic and random data for the domain:
suppliers (fornecedores), products (produtos), clients (clientes), orders
(encomendas), and order line items (detalhes_venda). The database name and
connection settings are read from ``config.toml`` at the repository root.

Usage:
    From the repo root after ``poetry install``::

        python -m bd_exemplos.scripts.seed_loja

    The script creates the database and tables if they do not exist, clears
    existing data, then inserts the seed data and prints row counts.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import ROUND_HALF_UP, Decimal
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
class Supplier:
    """A supplier (fornecedor) entity.

    Attributes:
        id_fornecedor: Primary key.
        nome: Supplier name.
        email: Contact email (unique in schema).
    """

    id_fornecedor: int
    nome: str
    email: str


@dataclass(frozen=True)
class Product:
    """A product (produto) entity.

    Attributes:
        id_produto: Primary key.
        nome: Product name.
        preco_base: Base price (decimal, 2 places).
        id_fornecedor: Foreign key to Supplier.
    """

    id_produto: int
    nome: str
    preco_base: Decimal
    id_fornecedor: int


@dataclass(frozen=True)
class Client:
    """A client (cliente) entity.

    Attributes:
        email: Primary key (email address).
        nome: Full name.
        rua: Street address.
        localidade: City/locality.
        codigo_postal: Postal code.
    """

    email: str
    nome: str
    rua: str
    localidade: str
    codigo_postal: str


@dataclass(frozen=True)
class Order:
    """An order (encomenda) header.

    Attributes:
        num_encomenda: Primary key (order number).
        data: Order date.
        email_cliente: Foreign key to Client.
    """

    num_encomenda: str
    data: date
    email_cliente: str


@dataclass(frozen=True)
class OrderLine:
    """A line item in an order (detalhes_venda).

    Attributes:
        num_encomenda: Foreign key to Order.
        id_produto: Foreign key to Product.
        tamanho: Size (e.g. S, M, L or numeric).
        quantidade: Quantity ordered.
        preco_praticado: Applied unit price (may differ from product base price).
    """

    num_encomenda: str
    id_produto: int
    tamanho: str
    quantidade: int
    preco_praticado: Decimal


# -----------------------------
# Helpers
# -----------------------------
def money(x: str) -> Decimal:
    """Parse a string as a decimal and round to two decimal places (half-up).

    Args:
        x: String representation of a number (e.g. "19.99").

    Returns:
        Decimal rounded to 2 decimal places.
    """
    return Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def quant2(x: Decimal) -> Decimal:
    """Round a decimal to two decimal places (half-up).

    Args:
        x: Value to round.

    Returns:
        Decimal rounded to 2 decimal places.
    """
    return x.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def chunked(seq: Sequence[tuple], size: int) -> Iterable[list[tuple]]:
    """Yield successive fixed-size chunks of a sequence.

    Args:
        seq: Sequence of tuples (e.g. row data for executemany).
        size: Maximum number of elements per chunk. Must be positive.

    Yields:
        Lists of up to ``size`` elements from ``seq``.

    Raises:
        ValueError: If ``size`` is less than or equal to zero.
    """
    if size <= 0:
        raise ValueError("chunk size must be > 0")
    for i in range(0, len(seq), size):
        yield list(seq[i : i + size])


def daterange_days(start: date, end_exclusive: date, rng: Random) -> date:
    """Return a uniformly random date in the half-open interval [start, end_exclusive).

    Args:
        start: Start of the range (inclusive).
        end_exclusive: End of the range (exclusive).
        rng: Random number generator for reproducibility.

    Returns:
        A date in [start, end_exclusive).

    Raises:
        ValueError: If end_exclusive <= start (empty or invalid range).
    """
    delta = (end_exclusive - start).days
    if delta <= 0:
        raise ValueError("Invalid date range")
    return start + timedelta(days=rng.randrange(delta))


# -----------------------------
# Dataset builder
# -----------------------------
def build_static_entities() -> tuple[list[Supplier], list[Product], list[Client]]:
    """Build the fixed set of suppliers, products, and clients for the shop seed.

    Data is deterministic and designed to support specific query exercises
    (e.g. products that are never sold, a supplier intentionally omitted).

    Returns:
        A tuple (suppliers, products, clients). Lengths: 3 suppliers, 23 products
        (including 3 never-sold), 10 clients.
    """
    # Adidas NOT included on purpose (query h)
    suppliers: list[Supplier] = [
        Supplier(1, "Nike", "sales@nike.pt"),
        Supplier(2, "LuxuryCo", "sales@luxuryco.pt"),
        Supplier(3, "Casa do Norte", "contacto@casadonorte.pt"),
    ]

    products: list[Product] = [
        # Nike
        Product(1, "Nike Air Max Pro", money("600.00"), 1),  # critical for query c
        Product(2, "Nike Running Jacket", money("550.00"), 1),
        Product(3, "Nike Socks Pack", money("19.99"), 1),
        Product(4, "Nike Smartwatch", money("799.00"), 1),
        Product(5, "Nike Cap", money("24.99"), 1),
        Product(6, "Nike Training Bag", money("45.00"), 1),
        # LuxuryCo
        Product(7, "Luxury Watch X", money("1200.00"), 2),
        Product(8, "Luxury Handbag", money("950.00"), 2),
        Product(9, "Luxury Sunglasses", money("320.00"), 2),
        # Casa do Norte
        Product(10, "Queijo Curado", money("8.50"), 3),
        Product(11, "Azeite Virgem", money("9.70"), 3),
        Product(12, "Enchido Regional", money("5.90"), 3),
        Product(13, "Mel Multifloral", money("6.10"), 3),
        Product(14, "Chá Verde", money("3.80"), 3),
        Product(15, "Bolachas de Aveia", money("3.20"), 3),
        Product(16, "Compota de Figo", money("4.20"), 3),
        Product(17, "Doce de Abóbora", money("4.00"), 3),
        Product(18, "Café Moído", money("4.90"), 3),
        Product(19, "Granola Artesanal", money("6.40"), 3),
        Product(20, "Chocolate Negro", money("2.90"), 3),
        # NEVER SOLD products (critical for query e)
        Product(21, "Nike Limited Edition Sneakers", money("1500.00"), 1),
        Product(22, "Luxury Perfume", money("180.00"), 2),
        Product(23, "Queijo Especial", money("14.90"), 3),
    ]

    clients: list[Client] = [
        Client("ana.silva@email.pt", "Ana Silva", "Rua das Flores 10", "Porto", "4000-100"),
        Client("joao.pereira@email.pt", "João Pereira", "Av. da República 50", "Gaia", "4400-200"),
        Client("rita.costa@email.pt", "Rita Costa", "Travessa do Sol 3", "Braga", "4700-300"),
        Client("miguel.santos@email.pt", "Miguel Santos", "Rua do Campo 8", "Aveiro", "3800-010"),
        Client("ines.martins@email.pt", "Inês Martins", "Av. Central 120", "Lisboa", "1100-020"),
        Client("tiago.ferreira@email.pt", "Tiago Ferreira", "Rua Nova 23", "Coimbra", "3000-050"),
        Client("sofia.rocha@email.pt", "Sofia Rocha", "Av. do Mar 9", "Faro", "8000-060"),
        Client("carla.mendes@email.pt", "Carla Mendes", "Rua da Ponte 1", "Viseu", "3500-070"),
        Client("pedro.lima@email.pt", "Pedro Lima", "Rua do Pinhal 77", "Leiria", "2400-080"),
        Client(
            "beatriz.sousa@email.pt", "Beatriz Sousa", "Rua do Mercado 5", "Setúbal", "2900-090"
        ),
    ]

    return suppliers, products, clients


def choose_size_for_product(pid: int, rng: Random) -> str:
    """Choose a size string for a product based on its id.

    Product-specific rules: numeric sizes for shoes, S/M/L/XL for apparel,
    "U" for one-size items, and volume for liquids.

    Args:
        pid: Product id (e.g. 1–23 in the seed set).
        rng: Random number generator (used for variety within allowed sizes).

    Returns:
        A size string (e.g. "42", "M", "U", "1L").
    """
    if pid in {1}:
        return str(rng.choice([40, 41, 42, 43, 44, 45]))
    if pid in {2, 5, 6}:
        return rng.choice(["S", "M", "L", "XL"])
    if pid in {4, 7, 8, 9}:
        return "U"
    if pid in {11}:
        return rng.choice(["0.5L", "1L"])
    return rng.choice(["S", "M", "L"])


def compute_practiced_price(base: Decimal, rng: Random) -> Decimal:
    """Compute a practiced (possibly discounted) unit price from the base price.

    Applies no discount (70% chance), 5% off (25%), or 10% off (5%), then
    rounds to two decimal places.

    Args:
        base: Base unit price.
        rng: Random number generator.

    Returns:
        Decimal rounded to 2 decimal places.
    """
    u = rng.random()
    if u < 0.70:
        factor = Decimal("1.00")
    elif u < 0.95:
        factor = Decimal("0.95")
    else:
        factor = Decimal("0.90")
    return quant2(base * factor)


def build_orders_and_lines(
    *,
    rng: Random,
    products: list[Product],
    clients: list[Client],
    total_orders: int,
) -> tuple[list[Order], list[OrderLine]]:
    """Build orders and order line items with guaranteed cases plus random bulk.

    Inserts fixed orders (e.g. Dec 2023, monthly 2025, one large order with
    >10 distinct products) and fills the remainder with random orders and
    lines. Products 21–22–23 are never sold (asserted).

    Args:
        rng: Random number generator (seed for reproducibility).
        products: Full list of products (must include ids 1–23).
        clients: List of clients to assign to orders.
        total_orders: Total number of orders to generate. Must be at least 50
            to accommodate the fixed guarantees.

    Returns:
        Tuple (orders, order_lines) with consistent references (order numbers,
        product ids, client emails).

    Raises:
        ValueError: If total_orders < 50 or any invariant is violated.
        AssertionError: If never-sold products appear in lines or guarantees fail.
    """
    if total_orders < 50:
        raise ValueError("total_orders should be reasonably large (>=50)")

    base_by_id: dict[int, Decimal] = {p.id_produto: p.preco_base for p in products}

    never_sold_ids = {21, 22, 23}
    all_product_ids = [p.id_produto for p in products]
    sellable_ids = [pid for pid in all_product_ids if pid not in never_sold_ids]

    orders: list[Order] = []
    lines: list[OrderLine] = []

    def add_line(num: str, pid: int, qty: int) -> None:
        if pid in never_sold_ids:
            raise AssertionError("Never-sold product was selected for a line.")
        if qty <= 0:
            raise ValueError("qty must be > 0")
        size = choose_size_for_product(pid, rng)
        price = compute_practiced_price(base_by_id[pid], rng)
        lines.append(OrderLine(num, pid, size, qty, price))

    # -----------------------------
    # Guarantees block
    # -----------------------------
    fixed_2023_orders = [
        ("E2023-1201-0001", date(2023, 12, 1), clients[0].email),
        ("E2023-1201-0002", date(2023, 12, 1), clients[1].email),
    ]
    for num, d, email in fixed_2023_orders:
        orders.append(Order(num, d, email))

    add_line("E2023-1201-0001", 1, 1)
    add_line("E2023-1201-0002", 1, 1)
    add_line("E2023-1201-0001", 10, 2)
    add_line("E2023-1201-0002", 3, 3)

    for m in range(1, 13):
        num = f"E2025-{m:02d}-FIX01"
        orders.append(Order(num, date(2025, m, 15), clients[2].email))
        add_line(num, 7, 1)
        add_line(num, 3, 2)
        add_line(num, 13, 2)
        if m % 3 == 0:
            add_line(num, 2, 1)

    big_num = "E2025-06-BIG01"
    orders.append(Order(big_num, date(2025, 6, 20), clients[4].email))

    big_ids = rng.sample([pid for pid in sellable_ids if pid != 1], k=10) + [1]
    big_ids = list(dict.fromkeys(big_ids))
    while len(big_ids) < 11:
        pid = rng.choice(sellable_ids)
        if pid not in big_ids and pid not in never_sold_ids:
            big_ids.append(pid)

    for pid in big_ids[:11]:
        add_line(big_num, pid, rng.choice([1, 2, 3]))

    # -----------------------------
    # Random bulk orders
    # -----------------------------
    remaining = total_orders - len(orders)
    if remaining < 0:
        raise ValueError("total_orders too small to include fixed guarantees")

    for idx in range(1, remaining + 1):
        num = f"E-RND-{idx:04d}"

        if rng.random() < 0.65:
            d = daterange_days(date(2025, 1, 1), date(2026, 1, 1), rng)
        else:
            d = daterange_days(date(2024, 1, 1), date(2025, 1, 1), rng)

        email = rng.choice(clients).email
        orders.append(Order(num, d, email))

        u = rng.random()
        if u < 0.75:
            k_items = rng.randint(1, 6)
        elif u < 0.95:
            k_items = rng.randint(7, 10)
        else:
            k_items = rng.randint(1, 6)

        chosen = rng.sample(sellable_ids, k=min(k_items, len(sellable_ids)))

        if rng.random() < 0.20 and 1 not in chosen:
            chosen[0] = 1

        for pid in chosen:
            add_line(num, pid, rng.randint(1, 4))

    # sanity checks
    used_pids = {line.id_produto for line in lines}
    if used_pids & never_sold_ids:
        raise AssertionError("Never-sold products ended up being sold.")
    big_count = len({line.id_produto for line in lines if line.num_encomenda == big_num})
    if big_count <= 10:
        raise AssertionError("Big order does not have >10 different items.")
    if not any(o.data == date(2023, 12, 1) for o in orders):
        raise AssertionError("Missing 2023-12-01 orders.")
    for m in range(1, 13):
        if not any(o.data.year == 2025 and o.data.month == m for o in orders):
            raise AssertionError(f"Missing orders for 2025-{m:02d}.")

    return orders, lines


# -----------------------------
# DB / Schema
# -----------------------------
def ddl_statements(database: str) -> list[str]:
    """Return SQL statements to create the shop database and its tables.

    Creates the database (if not exists) with utf8mb4, then tables in
    dependency order: fornecedores, produtos, clientes, encomendas,
    detalhes_venda, with foreign keys and indexes.

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
        CREATE TABLE IF NOT EXISTS fornecedores (
          ID_Fornecedor   INT          NOT NULL,
          Nome_Fornecedor VARCHAR(100) NOT NULL,
          Contacto_Email  VARCHAR(100) NOT NULL,
          PRIMARY KEY (ID_Fornecedor),
          UNIQUE KEY uq_fornecedores_email (Contacto_Email),
          UNIQUE KEY uq_fornecedores_nome  (Nome_Fornecedor)
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS produtos (
          ID_Produto     INT           NOT NULL,
          Nome_Produto   VARCHAR(120)  NOT NULL,
          Preco_Base     DECIMAL(10,2) NOT NULL,
          ID_Fornecedor  INT           NOT NULL,
          PRIMARY KEY (ID_Produto),
          KEY idx_produtos_fornecedor (ID_Fornecedor),
          KEY idx_produtos_preco (Preco_Base),
          CONSTRAINT fk_produtos_fornecedores
            FOREIGN KEY (ID_Fornecedor)
            REFERENCES fornecedores (ID_Fornecedor)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS clientes (
          Email_Cliente  VARCHAR(100) NOT NULL,
          Nome_Cliente   VARCHAR(120) NOT NULL,
          Rua            VARCHAR(150) NOT NULL,
          Localidade     VARCHAR(80)  NOT NULL,
          Codigo_Postal  VARCHAR(20)  NOT NULL,
          PRIMARY KEY (Email_Cliente)
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS encomendas (
          Num_Encomenda  VARCHAR(30)  NOT NULL,
          Data           DATE         NOT NULL,
          Email_Cliente  VARCHAR(100) NOT NULL,
          PRIMARY KEY (Num_Encomenda),
          KEY idx_encomendas_data (Data),
          KEY idx_encomendas_cliente (Email_Cliente),
          CONSTRAINT fk_encomendas_clientes
            FOREIGN KEY (Email_Cliente)
            REFERENCES clientes (Email_Cliente)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
        ) ENGINE=InnoDB
        """,
        """
        CREATE TABLE IF NOT EXISTS detalhes_venda (
          Num_Encomenda   VARCHAR(30)   NOT NULL,
          ID_Produto      INT           NOT NULL,
          Tamanho         VARCHAR(10)   NOT NULL,
          Quantidade      INT           NOT NULL,
          Preco_Praticado DECIMAL(10,2) NOT NULL,
          PRIMARY KEY (Num_Encomenda, ID_Produto, Tamanho),
          KEY idx_dv_produto (ID_Produto),
          CONSTRAINT fk_dv_encomendas
            FOREIGN KEY (Num_Encomenda)
            REFERENCES encomendas (Num_Encomenda)
            ON UPDATE CASCADE
            ON DELETE CASCADE,
          CONSTRAINT fk_dv_produtos
            FOREIGN KEY (ID_Produto)
            REFERENCES produtos (ID_Produto)
            ON UPDATE CASCADE
            ON DELETE RESTRICT
        ) ENGINE=InnoDB
        """,
    ]


def exec_many(cur, sql: str, rows: Sequence[tuple], batch: int) -> int:
    """Execute a parameterized statement for all rows in batches.

    Uses the cursor's executemany in chunks of ``batch`` rows to avoid
    huge single round-trips.

    Args:
        cur: Database cursor (e.g. from MySQLConnection.cursor()).
        sql: Parameterized SQL (e.g. "INSERT INTO t (a,b) VALUES (%s,%s)").
        rows: Sequence of parameter tuples (one per row).
        batch: Maximum rows per executemany call.

    Returns:
        Total number of rows executed (len(rows) when non-empty, else 0).
    """
    if not rows:
        return 0
    total = 0
    for part in chunked(list(rows), batch):
        cur.executemany(sql, part)
        total += len(part)
    return total


# -----------------------------
# Main
# -----------------------------
def main() -> None:
    """Entry point: load config, seed the shop database, and print insert counts.

    Reads ``config.toml`` from the repository root, builds all entities and
    orders, connects to MySQL, creates the database and tables if needed,
    clears existing data, inserts seed data in batches, commits, and prints
    the number of rows inserted per table. On any exception, the transaction
    is rolled back and the connection closed.
    """
    cfg = load_config(CONFIG_PATH)
    host = cfg.host
    port = cfg.port
    user = cfg.user
    password = cfg.password
    database = cfg.database

    total_orders = 1000
    seed = 12345
    batch_size = 5000

    rng = Random(seed)

    suppliers, products, clients = build_static_entities()
    orders, lines = build_orders_and_lines(
        rng=rng,
        products=products,
        clients=clients,
        total_orders=total_orders,
    )

    conn = connect_mysql(host=host, port=port, user=user, password=password)
    conn.autocommit = False

    try:
        cur = conn.cursor()

        for stmt in ddl_statements(database):
            cur.execute(stmt)

        # Clear tables (respect FK order)
        cur.execute(f"DELETE FROM {database}.detalhes_venda")
        cur.execute(f"DELETE FROM {database}.encomendas")
        cur.execute(f"DELETE FROM {database}.produtos")
        cur.execute(f"DELETE FROM {database}.clientes")
        cur.execute(f"DELETE FROM {database}.fornecedores")

        n_sup = exec_many(
            cur,
            f"INSERT INTO {database}.fornecedores (ID_Fornecedor, Nome_Fornecedor, Contacto_Email) VALUES (%s, %s, %s)",
            [(s.id_fornecedor, s.nome, s.email) for s in suppliers],
            batch=batch_size,
        )
        n_prod = exec_many(
            cur,
            f"INSERT INTO {database}.produtos (ID_Produto, Nome_Produto, Preco_Base, ID_Fornecedor) VALUES (%s, %s, %s, %s)",
            [(p.id_produto, p.nome, str(p.preco_base), p.id_fornecedor) for p in products],
            batch=batch_size,
        )
        n_cli = exec_many(
            cur,
            f"INSERT INTO {database}.clientes (Email_Cliente, Nome_Cliente, Rua, Localidade, Codigo_Postal) VALUES (%s, %s, %s, %s, %s)",
            [(c.email, c.nome, c.rua, c.localidade, c.codigo_postal) for c in clients],
            batch=batch_size,
        )
        n_ord = exec_many(
            cur,
            f"INSERT INTO {database}.encomendas (Num_Encomenda, Data, Email_Cliente) VALUES (%s, %s, %s)",
            [(o.num_encomenda, o.data, o.email_cliente) for o in orders],
            batch=batch_size,
        )
        n_lines = exec_many(
            cur,
            f"INSERT INTO {database}.detalhes_venda (Num_Encomenda, ID_Produto, Tamanho, Quantidade, Preco_Praticado) VALUES (%s, %s, %s, %s, %s)",
            [
                (
                    row.num_encomenda,
                    row.id_produto,
                    row.tamanho,
                    row.quantidade,
                    str(row.preco_praticado),
                )
                for row in lines
            ],
            batch=batch_size,
        )

        conn.commit()

        print("DONE")
        print(f"Inserted suppliers:  {n_sup}")
        print(f"Inserted products:   {n_prod}")
        print(f"Inserted clients:   {n_cli}")
        print(f"Inserted orders:    {n_ord}")
        print(f"Inserted order lines: {n_lines}")

    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
