from contextlib import closing
from flask import Blueprint, request, jsonify
from datetime import date, timedelta
from database import get_db

DIAS_ALERTA = 7
TAMANHO_MAX_NOME = 100

bp = Blueprint("produtos", __name__)


def _validar_payload_produto():
    dados = request.get_json(silent=True)
    if not isinstance(dados, dict):
        return None, (jsonify({"erro": "Envie um JSON válido no corpo da requisição"}), 400)

    campos = ["nome", "quantidade", "data_validade"]
    for campo in campos:
        if campo not in dados or dados[campo] in (None, ""):
            return None, (jsonify({"erro": f"Campo '{campo}' é obrigatório"}), 400)

    nome = dados["nome"]
    if not isinstance(nome, str):
        return None, (jsonify({"erro": "Nome deve ser um texto válido"}), 400)

    nome = nome.strip()
    if not nome:
        return None, (jsonify({"erro": "Nome não pode ficar em branco"}), 400)
    if len(nome) > TAMANHO_MAX_NOME:
        return None, (
            jsonify({"erro": f"Nome deve ter no máximo {TAMANHO_MAX_NOME} caracteres"}),
            400,
        )

    try:
        quantidade = int(dados["quantidade"])
        if quantidade < 0:
            raise ValueError
    except (ValueError, TypeError):
        return None, (jsonify({"erro": "Quantidade deve ser um inteiro não negativo"}), 400)

    try:
        data_validade = date.fromisoformat(dados["data_validade"])
    except ValueError:
        return None, (jsonify({"erro": "Data de validade inválida (use AAAA-MM-DD)"}), 400)

    return {
        "nome": nome,
        "quantidade": quantidade,
        "data_validade": data_validade.isoformat(),
    }, None


@bp.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados, erro = _validar_payload_produto()
    if erro:
        return erro

    with closing(get_db()) as conn:
        cursor = conn.execute(
            "INSERT INTO produtos (nome, quantidade, data_validade) VALUES (?, ?, ?)",
            (dados["nome"], dados["quantidade"], dados["data_validade"]),
        )
        conn.commit()
        produto_id = cursor.lastrowid

    return jsonify({"id": produto_id, "mensagem": "Produto cadastrado com sucesso"}), 201


@bp.route("/produtos", methods=["GET"])
def listar_produtos():
    with closing(get_db()) as conn:
        rows = conn.execute("SELECT * FROM produtos ORDER BY data_validade ASC").fetchall()

    return jsonify([dict(r) for r in rows])


@bp.route("/produtos/vencendo", methods=["GET"])
def listar_vencendo():
    limite = date.today() + timedelta(days=DIAS_ALERTA)
    with closing(get_db()) as conn:
        rows = conn.execute(
            "SELECT * FROM produtos WHERE data_validade <= ? ORDER BY data_validade ASC",
            (limite.isoformat(),),
        ).fetchall()

    return jsonify([dict(r) for r in rows])


@bp.route("/produtos/estatisticas", methods=["GET"])
def estatisticas():
    hoje = date.today().isoformat()
    limite = (date.today() + timedelta(days=DIAS_ALERTA)).isoformat()
    with closing(get_db()) as conn:
        total = conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
        vencidos = conn.execute(
            "SELECT COUNT(*) FROM produtos WHERE data_validade < ?", (hoje,)
        ).fetchone()[0]
        vencendo = conn.execute(
            "SELECT COUNT(*) FROM produtos WHERE data_validade >= ? AND data_validade <= ?",
            (hoje, limite),
        ).fetchone()[0]

    ok = total - vencidos - vencendo
    return jsonify({"total": total, "ok": ok, "vencendo": vencendo, "vencidos": vencidos})


@bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def remover_produto(produto_id):
    with closing(get_db()) as conn:
        cursor = conn.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        conn.commit()
        removidos = cursor.rowcount

    if removidos == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"mensagem": "Produto removido com sucesso"})
