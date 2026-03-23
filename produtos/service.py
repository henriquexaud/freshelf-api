from datetime import date, timedelta
from config import DIAS_ALERTA
from produtos import repository


def _calcular_status(data_validade_str):
    hoje = date.today()
    validade = date.fromisoformat(data_validade_str)
    diff = (validade - hoje).days
    if diff < 0:
        return "vencido"
    if diff == 0:
        return "vence_hoje"
    if diff <= DIAS_ALERTA:
        return "vencendo"
    return "ok"


def _enriquecer(produto):
    produto["status"] = _calcular_status(produto["data_validade"])
    return produto


def cadastrar(dados):
    return repository.inserir(dados["nome"], dados["quantidade"], dados["data_validade"])


def listar_todos():
    return [_enriquecer(p) for p in repository.buscar_todos()]


def listar_vencendo():
    limite = (date.today() + timedelta(days=DIAS_ALERTA)).isoformat()
    return [_enriquecer(p) for p in repository.buscar_por_validade_ate(limite)]


def obter_estatisticas():
    hoje = date.today().isoformat()
    limite = (date.today() + timedelta(days=DIAS_ALERTA)).isoformat()
    total, vencidos, vencendo = repository.contar_estatisticas(hoje, limite)
    ok = total - vencidos - vencendo
    return {"total": total, "ok": ok, "vencendo": vencendo, "vencidos": vencidos}


def remover(produto_id):
    return repository.deletar(produto_id)
