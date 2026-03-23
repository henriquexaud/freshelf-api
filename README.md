# Freshelf API

API REST para controle de validade de produtos perecíveis, permitindo cadastrar, listar e remover itens.

## Instalação

### Requisitos

- Python 3
- pip

### Passos

1. Clone o repositório e entre na pasta do projeto.

```bash
git clone <url-do-repositorio>
cd freshelf-api
```

2. Crie e ative um ambiente virtual.

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Instale as dependências.

```bash
pip install -r requirements.txt
```

## Inicialização

Execute a aplicação com:

```bash
python app.py
```

A API ficará disponível em http://localhost:5001.

## Observações

- O banco SQLite é criado automaticamente na primeira execução.
- Para validar se a API está no ar, acesse http://localhost:5001/health.
