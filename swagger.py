from flask import Blueprint, jsonify, render_template_string
from config import DIAS_ALERTA

bp = Blueprint("docs", __name__)

SPEC = {
    "openapi": "3.0.3",
    "info": {
        "title": "Freshelf API",
        "description": "API REST para controle de validade de produtos perecíveis.",
        "version": "1.0.0",
    },
    "paths": {
        "/health": {
            "get": {
                "tags": ["Infra"],
                "summary": "Verificar se a API está ativa",
                "responses": {
                    "200": {
                        "description": "API disponível",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "status": {"type": "string", "example": "ok"}
                                    },
                                }
                            }
                        },
                    }
                },
            }
        },
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
                                "schema": {"type": "array", "items": {"$ref": "#/components/schemas/Produto"}}
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
                "description": f"Retorna produtos com validade em até {DIAS_ALERTA} dias, incluindo já vencidos.",
                "responses": {
                    "200": {
                        "description": "Lista de produtos vencendo ou vencidos",
                        "content": {
                            "application/json": {
                                "schema": {"type": "array", "items": {"$ref": "#/components/schemas/Produto"}}
                            }
                        },
                    }
                },
            }
        },
        "/produtos/estatisticas": {
            "get": {
                "tags": ["Produtos"],
                "summary": "Estatísticas por status de validade",
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
                    "quantidade": {"type": "integer"},
                    "data_validade": {"type": "string", "format": "date"},
                    "status": {
                        "type": "string",
                        "enum": ["ok", "vencendo", "vence_hoje", "vencido"],
                        "description": "Status calculado com base na data de validade",
                    },
                },
            },
            "ProdutoInput": {
                "type": "object",
                "required": ["nome", "quantidade", "data_validade"],
                "properties": {
                    "nome": {
                        "type": "string",
                        "maxLength": 100,
                        "example": "Leite Integral",
                    },
                    "quantidade": {"type": "integer", "minimum": 0, "example": 6},
                    "data_validade": {"type": "string", "format": "date", "example": "2026-04-15"},
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

_UI = """<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"/>
    <title>Freshelf API — Documentação</title>
  <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css">
</head>
<body>
  <div id="swagger-ui"></div>
  <script src="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
  <script>SwaggerUIBundle({ url: "/openapi.json", dom_id: "#swagger-ui" });</script>
</body></html>"""


@bp.route("/openapi.json")
def openapi_spec():
    return jsonify(SPEC)


@bp.route("/docs")
def swagger_ui():
    return render_template_string(_UI)
