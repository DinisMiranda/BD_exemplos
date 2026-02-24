# BD_exemplos

[![CI](https://github.com/DinisMiranda/BD_exemplos/actions/workflows/tests.yml/badge.svg)](https://github.com/DinisMiranda/BD_exemplos/actions/workflows/tests.yml)
[![codecov](https://codecov.io/gh/DinisMiranda/BD_exemplos/graph/badge.svg)](https://codecov.io/gh/DinisMiranda/BD_exemplos)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Sample databases for testing (MySQL). Replace `DinisMiranda` in the badges with your GitHub org or username.

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
│       ├── seed_biblioteca.py # Library: authors, books, readers, loans
│       ├── seed_cinema.py     # Cinema: films, rooms, sessions, tickets
│       └── seed_clinica.py    # Clinic: doctors, patients, appointments
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
   # Shop (suppliers, products, clients, orders)
   poetry run python -m bd_exemplos.scripts.seed_loja

   # Library (authors, books, readers, loans)
   poetry run python -m bd_exemplos.scripts.seed_biblioteca

   # Cinema (films, rooms, sessions, tickets)
   poetry run python -m bd_exemplos.scripts.seed_cinema

   # Clinic (doctors, patients, appointments)
   poetry run python -m bd_exemplos.scripts.seed_clinica
   ```

With `poetry install`, Poetry creates the virtual environment and installs the package; no need for `PYTHONPATH`.

## Tests

```bash
poetry run pytest tests/ -v
poetry run pytest tests/ --cov=bd_exemplos --cov-report=term-missing
```

## Development

- **Lint:** `poetry run ruff check bd_exemplos tests` and `poetry run ruff format bd_exemplos tests --check`
- **Fix style:** `poetry run ruff check bd_exemplos tests --fix` and `poetry run ruff format bd_exemplos tests`
- See [CONTRIBUTING.md](CONTRIBUTING.md) for full setup and PR process.

## Dependencies

- Python ^3.9
- Managed in `pyproject.toml`: `toml`, `mysql-connector-python`

Install: `poetry install`. To generate `requirements.txt` (e.g. for CI/Docker): `poetry export -f requirements.txt --without-hashes`.
