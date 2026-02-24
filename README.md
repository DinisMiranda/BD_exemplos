# BD_exemplos

Sample databases for testing (MySQL).

## Repository structure

```
BD_exemplos/
├── config.toml.example   # Config template (copy to config.toml)
├── pyproject.toml        # Poetry project (poetry install)
├── bd_exemplos/          # Python package
│   ├── config.py         # Config loader
│   ├── db.py             # Shared MySQL connection
│   └── scripts/          # Seed scripts (run with python -m)
│       ├── seed_loja.py       # Shop: suppliers, products, clients, orders
│       └── seed_biblioteca.py # Library: authors, books, readers, loans
├── tests/                # Tests (pytest)
│   ├── test_config.py    # load_config
│   └── test_builders.py  # build_static_entities, build_autores, etc.
├── requirements.txt
├── README.md
└── LICENSE
```

## Configuration

The `config.toml` file (with your MySQL password) **is not in the repository** for security. Use the template:

1. **Copy the example** to create your config file:
   ```bash
   cp config.toml.example config.toml
   ```
2. **Edit `config.toml`** and set:
   - `password` — your MySQL password (e.g. MySQL Workbench). Can be empty if your local server has no password.
   - `database` — database name (e.g. `BD_TESTE` or `BD_TESTE2`).
   - Optionally adjust `host`, `port`, `user`.

## How to run

If you don't have **Poetry** installed yet:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Restart your terminal (or run `source ~/.zshrc`) so the `poetry` command is available.

1. **Install dependencies** (from the repository root):

   ```bash
   poetry install
   ```

2. **Run the seeds** (`config.toml` must be in the repo root):

   ```bash
   # Shop seed (uses database from config.toml)
   poetry run python -m bd_exemplos.scripts.seed_loja

   # Library seed
   poetry run python -m bd_exemplos.scripts.seed_biblioteca
   ```

With `poetry install`, Poetry creates the virtual environment and installs the package; no need for `PYTHONPATH`.

## Tests

Minimal tests with pytest (config and data builders):

```bash
poetry run pytest tests/ -v
```

## Dependencies

- Python ^3.9
- Managed in `pyproject.toml`: `toml`, `mysql-connector-python`

Install: `poetry install`. To generate `requirements.txt` (e.g. for CI/Docker): `poetry export -f requirements.txt --without-hashes`.
