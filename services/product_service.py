from datetime import date, timedelta
from config import DIAS_ALERTA
from repository import product_repository


def cadastrar(dados):
    return product_repository.inserir(dados)


def listar_todos():
    return [produto.to_dict(dias_alerta=DIAS_ALERTA) for produto in product_repository.buscar_todos()]


def listar_vencendo():
    limite = date.today() + timedelta(days=DIAS_ALERTA)
    return [produto.to_dict(dias_alerta=DIAS_ALERTA) for produto in product_repository.buscar_por_validade_ate(limite)]


def obter_estatisticas():
    hoje = date.today()
    limite = date.today() + timedelta(days=DIAS_ALERTA)
    total, vencidos, vencendo = product_repository.contar_estatisticas(hoje, limite)
    ok = total - vencidos - vencendo
    return {"total": total, "ok": ok, "vencendo": vencendo, "vencidos": vencidos}


def remover(produto_id):
    return product_repository.deletar(produto_id)
