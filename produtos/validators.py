from flask import request, jsonify
from datetime import date
from config import TAMANHO_MAX_NOME


def validar_payload_produto():
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
