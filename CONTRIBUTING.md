# Contributing

Thanks for your interest in contributing. Here’s how to get started.

## Development setup

1. **Clone and install**

   ```bash
   git clone https://github.com/YOUR_ORG/BD_exemplos.git
   cd BD_exemplos
   poetry install
   ```

2. **Config**

   Copy the config template and set your local MySQL settings (optional for running tests):

   ```bash
   cp config.toml.example config.toml
   # Edit config.toml with your host, user, password, database
   ```

## Running tests

```bash
poetry run pytest tests/ -v
poetry run pytest tests/ --cov=bd_exemplos --cov-report=term-missing
```

## Code style and linting

- Code is formatted with **Ruff** and type-checked where applicable.
- Run the linter before pushing:

  ```bash
  poetry run ruff check bd_exemplos tests
  poetry run ruff format bd_exemplos tests --check
  ```

- Fix auto-fixable issues:

  ```bash
  poetry run ruff check bd_exemplos tests --fix
  poetry run ruff format bd_exemplos tests
  ```

## Pull requests

1. Open an issue first for larger changes, or go straight to a PR for small fixes.
2. Branch from `main` (or `master`), e.g. `fix/description` or `feat/new-seed`.
3. Ensure tests pass and the linter is clean.
4. Update the README or docs if behaviour or setup changes.
5. Fill in the PR template; a maintainer will review.

## Commit messages

- Use clear, present-tense messages: e.g. "Add library seed script", "Fix config for empty password".
- Reference issues when relevant: "Fix #12: allow empty password in config".

## Questions

Open a [Discussion](https://github.com/YOUR_ORG/BD_exemplos/discussions) or an issue if you have questions.
