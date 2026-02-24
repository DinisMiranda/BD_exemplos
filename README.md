# BD_exemplos

Bases de dados para teste (MySQL).

## Estrutura do repositório

```
BD_exemplos/
├── config.toml.example # Modelo de configuração (copiar para config.toml)
├── bd_exemplos/        # Código partilhado
│   └── config.py       # Leitura da configuração
├── scripts/            # Scripts de seed
│   ├── seed_loja.py    # Loja: fornecedores, produtos, clientes, encomendas
│   └── seed_biblioteca.py  # Biblioteca: autores, livros, leitores, empréstimos
├── requirements.txt
├── README.md
└── LICENSE
```

## Configuração

O ficheiro `config.toml` (com a password do MySQL) **não está no repositório** por segurança. Usa o modelo:

1. **Copiar o exemplo** para criar o teu ficheiro de configuração:
   ```bash
   cp config.toml.example config.toml
   ```
2. **Editar `config.toml`** e preencher:
   - `password` — password do MySQL (ex.: MySQL Workbench). Pode ficar vazia se o teu servidor local não usar password.
   - `database` — nome da base de dados (podes usar, por exemplo, `BD_TESTE` ou `BD_TESTE2`).
   - Opcionalmente ajustar `host`, `port`, `user`.
</think>
Verificando se o config carrega com password vazia:
<｜tool▁calls▁begin｜><｜tool▁call▁begin｜>
Shell

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
