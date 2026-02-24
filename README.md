# BD_exemplos

Bases de dados para teste (MySQL).

## Estrutura do repositório

```
BD_exemplos/
├── config.toml.example   # Modelo de configuração (copiar para config.toml)
├── pyproject.toml       # Projeto Poetry (poetry install)
├── bd_exemplos/          # Pacote Python
│   ├── config.py        # Leitura da configuração
│   ├── db.py            # Conexão MySQL partilhada
│   └── scripts/         # Scripts de seed (executar com python -m)
│       ├── seed_loja.py      # Loja: fornecedores, produtos, clientes, encomendas
│       └── seed_biblioteca.py # Biblioteca: autores, livros, leitores, empréstimos
├── tests/              # Testes (pytest)
│   ├── test_config.py  # load_config
│   └── test_builders.py # build_static_entities, build_autores, etc.
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

Se ainda não tiveres o **Poetry** instalado:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Reinicia o terminal (ou faz `source ~/.zshrc`) para que o comando `poetry` fique disponível.

1. **Instalar dependências** (na raiz do repositório):

   ```bash
   poetry install
   ```

2. **Executar os seeds** (o `config.toml` deve estar na raiz do repo):

   ```bash
   # Seed Loja (usa o database definido em config.toml)
   poetry run python -m bd_exemplos.scripts.seed_loja

   # Seed Biblioteca
   poetry run python -m bd_exemplos.scripts.seed_biblioteca
   ```

Com `poetry install`, o Poetry cria o ambiente virtual e instala o pacote; não é preciso `PYTHONPATH`.

## Testes

Testes mínimos com pytest (config e builders de dados):

```bash
poetry run pytest tests/ -v
```

## Dependências

- Python ^3.9
- Geridas pelo Poetry em `pyproject.toml`: `toml`, `mysql-connector-python`

Instalação: `poetry install`. Para gerar `requirements.txt` (ex.: CI/Docker): `poetry export -f requirements.txt --without-hashes`.
