"""bd_exemplos: sample MySQL databases for testing.

This package provides configuration loading (``config``), a shared MySQL
connection helper (``db``), and seed scripts for two domains:

- **Shop** (``scripts.seed_loja``): suppliers, products, clients, orders, order lines.
- **Library** (``scripts.seed_biblioteca``): authors, books, readers, loans.

Run seeds with::

    python -m bd_exemplos.scripts.seed_loja
    python -m bd_exemplos.scripts.seed_biblioteca

Configuration is read from a ``config.toml`` file at the repository root
(see ``config.toml.example``).
"""
