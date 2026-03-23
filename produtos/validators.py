from datetime import date
from config import TAMANHO_MAX_NOME


def validar_produto(dados):
    if not isinstance(dados, dict):
        return None, "Envie um JSON válido no corpo da requisição"

    campos = ["nome", "quantidade", "data_validade"]
    for campo in campos:
        if campo not in dados or dados[campo] in (None, ""):
            return None, f"Campo '{campo}' é obrigatório"

    nome = dados["nome"]
    if not isinstance(nome, str):
        return None, "Nome deve ser um texto válido"

    nome = nome.strip()
    if not nome:
        return None, "Nome não pode ficar em branco"
    if len(nome) > TAMANHO_MAX_NOME:
        return None, f"Nome deve ter no máximo {TAMANHO_MAX_NOME} caracteres"

    try:
        quantidade = int(dados["quantidade"])
        if quantidade < 0:
            raise ValueError
    except (ValueError, TypeError):
        return None, "Quantidade deve ser um inteiro não negativo"

    try:
        data_validade = date.fromisoformat(dados["data_validade"])
    except ValueError:
        return None, "Data de validade inválida (use AAAA-MM-DD)"

    return {
        "nome": nome,
        "quantidade": quantidade,
        "data_validade": data_validade.isoformat(),
    }, None
