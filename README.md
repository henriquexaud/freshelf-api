# Freshelf API

API REST para controle de validade de produtos perecíveis. Permite cadastrar, listar e remover produtos, com alerta automático para itens próximos do vencimento.

---

## Tecnologias

- Python 3 + Flask
- SQLite (banco de dados local, sem instalação adicional)
- Flask-CORS (permite acesso da SPA)

---

## Instalação

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd freshelf-api
```

### 2. Crie e ative o ambiente virtual

```bash
python3 -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate         # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

---

## Inicialização

```bash
python app.py
```

## Estrutura

```text
app.py
config/
controllers/
docs/
infrastructure/
repository/
routes/
services/
validators/
```

A API estará disponível em `http://localhost:5001`.

Por padrão, a aplicação sobe apenas em ambiente local com debug desligado. Para ativar debug localmente:

```bash
FLASK_DEBUG=1 python app.py
```

O banco de dados `produtos.db` é criado automaticamente na primeira execução.

Se existir uma base antiga com os campos de categoria ou local de armazenamento, a aplicação migra a tabela automaticamente na inicialização e preserva os produtos já cadastrados.

### Health check

```text
http://localhost:5001/health
```

Resposta esperada:

```json
{
  "status": "ok"
}
```

---

## Documentação interativa (Swagger)

Com a API em execução, acesse:

```
http://localhost:5001/docs
```

O spec OpenAPI 3.0 em JSON está disponível em:

```
http://localhost:5001/openapi.json
```

---

## Rotas disponíveis

| Método | Rota                     | Descrição                                            |
|--------|--------------------------|------------------------------------------------------|
| GET    | `/health`                | Verifica se a API está ativa                         |
| POST   | `/produtos`              | Cadastra um novo produto                             |
| GET    | `/produtos`              | Lista todos os produtos (ordenados por validade)     |
| GET    | `/produtos/vencendo`     | Lista produtos vencidos ou com vencimento em ≤ 7 dias|
| GET    | `/produtos/estatisticas` | Retorna contagem de produtos por status de validade  |
| DELETE | `/produtos/<id>`         | Remove um produto pelo ID                            |

### Exemplo de corpo para `POST /produtos`

```json
{
  "nome": "Leite Integral",
  "quantidade": 6,
  "data_validade": "2026-04-15"
}
```

### Códigos de status

| Código | Situação                        |
|--------|---------------------------------|
| 200    | Operação realizada com sucesso  |
| 201    | Produto cadastrado com sucesso  |
| 400    | Dados inválidos ou ausentes     |
| 404    | Produto não encontrado          |

### Regras de validação

- `nome` deve ser texto, não pode ficar em branco e aceita no máximo 100 caracteres
- `quantidade` deve ser um inteiro maior ou igual a 0
- `data_validade` deve seguir o formato `AAAA-MM-DD`
- o corpo da requisição deve ser um JSON válido
