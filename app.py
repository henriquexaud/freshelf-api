from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import date, timedelta
import sqlite3
import os

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(os.path.dirname(__file__), "produtos.db")
DIAS_ALERTA_VENCIMENTO = 7


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            data_validade TEXT NOT NULL,
            local_armazenamento TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


init_db()


@app.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados = request.get_json()
    campos = ["nome", "categoria", "quantidade", "data_validade", "local_armazenamento"]
    for campo in campos:
        if campo not in dados or dados[campo] in (None, ""):
            return jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400

    try:
        quantidade = int(dados["quantidade"])
        if quantidade < 0:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({"erro": "Quantidade deve ser um inteiro não negativo"}), 400

    try:
        date.fromisoformat(dados["data_validade"])
    except ValueError:
        return jsonify({"erro": "Data de validade inválida (use AAAA-MM-DD)"}), 400

    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO produtos (nome, categoria, quantidade, data_validade, local_armazenamento) VALUES (?, ?, ?, ?, ?)",
        (dados["nome"], dados["categoria"], quantidade, dados["data_validade"], dados["local_armazenamento"]),
    )
    conn.commit()
    produto_id = cursor.lastrowid
    conn.close()
    return jsonify({"id": produto_id, "mensagem": "Produto cadastrado com sucesso"}), 201


@app.route("/produtos", methods=["GET"])
def listar_produtos():
    conn = get_db()
    rows = conn.execute("SELECT * FROM produtos ORDER BY data_validade ASC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/produtos/vencendo", methods=["GET"])
def listar_vencendo():
    limite = date.today() + timedelta(days=DIAS_ALERTA_VENCIMENTO)
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM produtos WHERE data_validade <= ? ORDER BY data_validade ASC",
        (limite.isoformat(),),
    ).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


@app.route("/produtos/<int:produto_id>", methods=["DELETE"])
def remover_produto(produto_id):
    conn = get_db()
    cursor = conn.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
    conn.commit()
    removidos = cursor.rowcount
    conn.close()
    if removidos == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"mensagem": "Produto removido com sucesso"})


@app.route("/produtos/estatisticas", methods=["GET"])
def estatisticas():
    hoje = date.today().isoformat()
    limite = (date.today() + timedelta(days=DIAS_ALERTA_VENCIMENTO)).isoformat()
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
    vencidos = conn.execute(
        "SELECT COUNT(*) FROM produtos WHERE data_validade < ?", (hoje,)
    ).fetchone()[0]
    vencendo = conn.execute(
        "SELECT COUNT(*) FROM produtos WHERE data_validade >= ? AND data_validade <= ?",
        (hoje, limite),
    ).fetchone()[0]
    ok = total - vencidos - vencendo
    conn.close()
    return jsonify({"total": total, "ok": ok, "vencendo": vencendo, "vencidos": vencidos})


_OPENAPI_SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "FreshElf API",
        "description": "API REST para controle de validade de produtos perecíveis.",
        "version": "1.0.0",
    },
    "paths": {
        "/produtos": {
            "get": {
                "tags": ["Produtos"],
                "summary": "Listar todos os produtos",
                "description": "Retorna todos os produtos cadastrados, ordenados pela data de validade.",
                "responses": {
                    "200": {
                        "description": "Lista de produtos",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Produto"},
                                }
                            }
                        },
                    }
                },
            },
            "post": {
                "tags": ["Produtos"],
                "summary": "Cadastrar um novo produto",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": "#/components/schemas/ProdutoInput"}
                        }
                    },
                },
                "responses": {
                    "201": {"description": "Produto cadastrado com sucesso"},
                    "400": {"description": "Dados inválidos ou campos ausentes"},
                },
            },
        },
        "/produtos/vencendo": {
            "get": {
                "tags": ["Produtos"],
                "summary": "Listar produtos próximos do vencimento ou vencidos",
                "description": f"Retorna produtos com validade igual ou inferior a {DIAS_ALERTA_VENCIMENTO} dias a partir de hoje, incluindo já vencidos.",
                "responses": {
                    "200": {
                        "description": "Lista de produtos vencendo ou vencidos",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "array",
                                    "items": {"$ref": "#/components/schemas/Produto"},
                                }
                            }
                        },
                    }
                },
            }
        },
        "/produtos/estatisticas": {
            "get": {
                "tags": ["Produtos"],
                "summary": "Estatísticas do estoque por status de validade",
                "responses": {
                    "200": {
                        "description": "Contagem de produtos por status",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": "#/components/schemas/Estatisticas"}
                            }
                        },
                    }
                },
            }
        },
        "/produtos/{id}": {
            "delete": {
                "tags": ["Produtos"],
                "summary": "Remover um produto",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "integer"},
                        "description": "ID do produto",
                    }
                ],
                "responses": {
                    "200": {"description": "Produto removido com sucesso"},
                    "404": {"description": "Produto não encontrado"},
                },
            }
        },
    },
    "components": {
        "schemas": {
            "Produto": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "nome": {"type": "string"},
                    "categoria": {"type": "string"},
                    "quantidade": {"type": "integer"},
                    "data_validade": {"type": "string", "format": "date"},
                    "local_armazenamento": {"type": "string"},
                },
            },
            "ProdutoInput": {
                "type": "object",
                "required": ["nome", "categoria", "quantidade", "data_validade", "local_armazenamento"],
                "properties": {
                    "nome": {"type": "string", "example": "Leite Integral"},
                    "categoria": {"type": "string", "example": "Laticínios"},
                    "quantidade": {"type": "integer", "example": 6},
                    "data_validade": {"type": "string", "format": "date", "example": "2026-04-15"},
                    "local_armazenamento": {"type": "string", "example": "Geladeira"},
                },
            },
            "Estatisticas": {
                "type": "object",
                "properties": {
                    "total": {"type": "integer"},
                    "ok": {"type": "integer"},
                    "vencendo": {"type": "integer"},
                    "vencidos": {"type": "integer"},
                },
            },
        }
    },
}

_SWAGGER_UI = """<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"/>
  <title>FreshElf API — Documentação</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>SwaggerUIBundle({ url: "/openapi.json", dom_id: "#swagger-ui" });</script>
</body></html>"""


@app.route("/openapi.json")
def openapi_spec():
    return jsonify(_OPENAPI_SPEC)


@app.route("/docs")
def swagger_ui():
    return render_template_string(_SWAGGER_UI)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
