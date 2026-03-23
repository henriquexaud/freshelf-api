from flask import Blueprint
from controllers import product_controller

bp = Blueprint("produtos", __name__)


@bp.post("/produtos")
def cadastrar_produto():
	return product_controller.cadastrar_produto()


@bp.get("/produtos")
def listar_produtos():
	return product_controller.listar_produtos()


@bp.get("/produtos/vencendo")
def listar_vencendo():
	return product_controller.listar_vencendo()


@bp.get("/produtos/estatisticas")
def estatisticas():
	return product_controller.estatisticas()


@bp.delete("/produtos/<int:produto_id>")
def remover_produto(produto_id):
	return product_controller.remover_produto(produto_id)
