from contextlib import closing
from datetime import date, timedelta
from database import get_db
from config import DIAS_ALERTA


def cadastrar(dados):
    with closing(get_db()) as conn:
        cursor = conn.execute(
            "INSERT INTO produtos (nome, quantidade, data_validade) VALUES (?, ?, ?)",
            (dados["nome"], dados["quantidade"], dados["data_validade"]),
        )
        conn.commit()
        return cursor.lastrowid


def listar_todos():
    with closing(get_db()) as conn:
        rows = conn.execute("SELECT * FROM produtos ORDER BY data_validade ASC").fetchall()
    return [dict(r) for r in rows]


def listar_vencendo():
    limite = date.today() + timedelta(days=DIAS_ALERTA)
    with closing(get_db()) as conn:
        rows = conn.execute(
            "SELECT * FROM produtos WHERE data_validade <= ? ORDER BY data_validade ASC",
            (limite.isoformat(),),
        ).fetchall()
    return [dict(r) for r in rows]


def obter_estatisticas():
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
    return {"total": total, "ok": ok, "vencendo": vencendo, "vencidos": vencidos}


def remover(produto_id):
    with closing(get_db()) as conn:
        cursor = conn.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
        conn.commit()
        return cursor.rowcount
