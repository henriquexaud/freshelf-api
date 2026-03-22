from flask import Blueprint, jsonify
from produtos import service
from produtos.validators import validar_payload_produto

bp = Blueprint("produtos", __name__)


@bp.route("/produtos", methods=["POST"])
def cadastrar_produto():
    dados, erro = validar_payload_produto()
    if erro:
        return erro
    produto_id = service.cadastrar(dados)
    return jsonify({"id": produto_id, "mensagem": "Produto cadastrado com sucesso"}), 201


@bp.route("/produtos", methods=["GET"])
def listar_produtos():
    return jsonify(service.listar_todos())


@bp.route("/produtos/vencendo", methods=["GET"])
def listar_vencendo():
    return jsonify(service.listar_vencendo())


@bp.route("/produtos/estatisticas", methods=["GET"])
def estatisticas():
    return jsonify(service.obter_estatisticas())


@bp.route("/produtos/<int:produto_id>", methods=["DELETE"])
def remover_produto(produto_id):
    removidos = service.remover(produto_id)
    if removidos == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"mensagem": "Produto removido com sucesso"})
