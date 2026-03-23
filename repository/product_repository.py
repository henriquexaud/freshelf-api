from contextlib import closing
from infrastructure import get_db
from models import ProductModel


def inserir(produto):
    with closing(get_db()) as conn:
        cursor = conn.execute(
            "INSERT INTO produtos (nome, quantidade, data_validade) VALUES (?, ?, ?)",
            (produto.nome, produto.quantidade, produto.data_validade.isoformat()),
        )
        conn.commit()
        return cursor.lastrowid


def buscar_todos():
    with closing(get_db()) as conn:
        rows = conn.execute(
            "SELECT * FROM produtos ORDER BY data_validade ASC"
        ).fetchall()
    return [ProductModel.from_row(r) for r in rows]


def buscar_por_validade_ate(data_limite):
    with closing(get_db()) as conn:
        rows = conn.execute(
            "SELECT * FROM produtos WHERE data_validade <= ? ORDER BY data_validade ASC",
            (data_limite.isoformat(),),
        ).fetchall()
    return [ProductModel.from_row(r) for r in rows]


def contar_estatisticas(hoje, limite):
    with closing(get_db()) as conn:
        total = conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
        vencidos = conn.execute(
            "SELECT COUNT(*) FROM produtos WHERE data_validade < ?", (hoje.isoformat(),)
        ).fetchone()[0]
        vencendo = conn.execute(
            "SELECT COUNT(*) FROM produtos WHERE data_validade >= ? AND data_validade <= ?",
            (hoje.isoformat(), limite.isoformat()),
        ).fetchone()[0]
    return total, vencidos, vencendo


def deletar(produto_id):
    with closing(get_db()) as conn:
        cursor = conn.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        conn.commit()
        return cursor.rowcount
