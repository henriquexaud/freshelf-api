from flask import jsonify, request
from services import product_service
from validators.product_validators import validar_produto


def cadastrar_produto():
    dados = request.get_json(silent=True)
    produto, erro = validar_produto(dados)
    if erro:
        return jsonify({"erro": erro}), 400
    produto_id = product_service.cadastrar(produto)
    return jsonify({"id": produto_id, "mensagem": "Produto cadastrado com sucesso"}), 201


def listar_produtos():
    return jsonify(product_service.listar_todos())


def listar_vencendo():
    return jsonify(product_service.listar_vencendo())


def estatisticas():
    return jsonify(product_service.obter_estatisticas())


def remover_produto(produto_id):
    removidos = product_service.remover(produto_id)
    if removidos == 0:
        return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"mensagem": "Produto removido com sucesso"})
