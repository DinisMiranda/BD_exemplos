# BD_exemplos

Bases de dados para teste (MySQL).

## Estrutura do repositório

```
BD_exemplos/
├── config.toml          # Configuração MySQL (host, port, user, password, database)
├── bd_exemplos/         # Código partilhado
│   └── config.py        # Leitura da configuração
├── scripts/             # Scripts de seed
│   ├── seed_loja.py     # Loja: fornecedores, produtos, clientes, encomendas
│   └── seed_biblioteca.py  # Biblioteca: autores, livros, leitores, empréstimos
├── README.md
└── LICENSE
```

## Configuração

**Importante (em `config.toml`):**

- No campo `password` deve colocar a password do seu MySQL (ex.: MySQL Workbench).
- Para importar uma base de dados diferente, altere o campo `database` em `config.toml`.

## Como executar

A partir da **raiz do repositório**:

```bash
# Garantir que o módulo bd_exemplos é encontrado
export PYTHONPATH=.

# Seed Loja (usa o database definido em config.toml)
python scripts/seed_loja.py

# Seed Biblioteca (usa o database definido em config.toml)
python scripts/seed_biblioteca.py
```

Ou com `python3`:

```bash
PYTHONPATH=. python3 scripts/seed_loja.py
PYTHONPATH=. python3 scripts/seed_biblioteca.py
```

## Dependências

- Python 3.10+
- `toml`
- `mysql-connector-python`

Instalação:

```bash
pip install toml mysql-connector-python
```

(Opcional: criar um ambiente virtual antes.)
